"""
工具调用验证模块
确保LLM不会虚构工具调用结果
"""

import json
import logging
from typing import Any, Dict, List
from langchain_core.messages import AIMessage, ToolMessage

logger = logging.getLogger(__name__)

class ToolCallValidator:
    """工具调用验证器"""
    
    def __init__(self):
        self.tool_call_log = []
    
    def validate_tool_calls(self, messages: List[Any]) -> Dict[str, Any]:
        """
        验证消息中的工具调用是否真实执行
        
        Args:
            messages: 消息列表
            
        Returns:
            验证结果字典
        """
        validation_result = {
            "valid": True,
            "tool_calls_found": 0,
            "tool_responses_found": 0,
            "missing_responses": [],
            "fabricated_data": [],
            "warnings": []
        }
        
        tool_calls = []
        tool_responses = []
        
        # 收集工具调用和响应
        for message in messages:
            if isinstance(message, AIMessage) and hasattr(message, 'tool_calls'):
                for tool_call in message.tool_calls:
                    tool_calls.append({
                        "id": tool_call.get("id"),
                        "name": tool_call.get("name"),
                        "args": tool_call.get("args")
                    })
                    validation_result["tool_calls_found"] += 1
            
            elif isinstance(message, ToolMessage):
                tool_responses.append({
                    "tool_call_id": message.tool_call_id,
                    "content": message.content
                })
                validation_result["tool_responses_found"] += 1
        
        # 验证每个工具调用都有对应的响应
        for tool_call in tool_calls:
            call_id = tool_call["id"]
            response_found = any(resp["tool_call_id"] == call_id for resp in tool_responses)
            
            if not response_found:
                validation_result["missing_responses"].append(tool_call)
                validation_result["valid"] = False
        
        # 检查是否有虚构的数据
        self._check_for_fabricated_data(messages, validation_result)
        
        return validation_result
    
    def _check_for_fabricated_data(self, messages: List[Any], validation_result: Dict[str, Any]):
        """检查是否有虚构的数据"""
        
        # 常见的虚构数据模式
        fabrication_patterns = [
            "阿里巴巴 Group Co. Ltd.",  # 错误的公司名称
            "结果：阿里巴巴",
            "Apple Inc.",  # 对A股股票返回美股公司
            "Microsoft Corporation",
            "Google Inc.",
            "entaal-",  # 虚构的财务数据前缀
            "Poland Pharmaceutical",  # 虚构的公司名称
        ]
        
        for message in messages:
            if isinstance(message, AIMessage):
                content = str(message.content)
                
                for pattern in fabrication_patterns:
                    if pattern in content:
                        validation_result["fabricated_data"].append({
                            "pattern": pattern,
                            "message_content": content[:200] + "..." if len(content) > 200 else content
                        })
                        validation_result["valid"] = False
                        validation_result["warnings"].append(f"检测到可能的虚构数据: {pattern}")
    
    def log_tool_call(self, tool_name: str, args: Dict[str, Any], result: Any):
        """记录工具调用"""
        self.tool_call_log.append({
            "tool_name": tool_name,
            "args": args,
            "result": str(result)[:500] + "..." if len(str(result)) > 500 else str(result),
            "timestamp": __import__("datetime").datetime.now().isoformat()
        })
    
    def get_tool_call_summary(self) -> str:
        """获取工具调用摘要"""
        if not self.tool_call_log:
            return "没有记录到工具调用"
        
        summary = f"工具调用记录 ({len(self.tool_call_log)} 次调用):\n"
        for i, call in enumerate(self.tool_call_log, 1):
            summary += f"{i}. {call['tool_name']}({call['args']}) -> {call['result'][:100]}...\n"
        
        return summary

def create_validated_analyst(analyst_func, validator: ToolCallValidator = None):
    """
    创建带验证的分析师节点
    
    Args:
        analyst_func: 原始分析师函数
        validator: 工具调用验证器
        
    Returns:
        带验证的分析师函数
    """
    if validator is None:
        validator = ToolCallValidator()
    
    def validated_analyst_node(state):
        # 执行原始分析师
        result = analyst_func(state)
        
        # 验证工具调用
        if "messages" in result:
            validation_result = validator.validate_tool_calls(result["messages"])
            
            if not validation_result["valid"]:
                logger.warning(f"工具调用验证失败: {validation_result}")
                
                # 在结果中添加验证警告
                if isinstance(result["messages"][-1], AIMessage):
                    original_content = result["messages"][-1].content
                    warning_msg = "\n\n⚠️ **数据验证警告**: 检测到可能的数据问题，请谨慎参考此报告。"
                    
                    if validation_result["fabricated_data"]:
                        warning_msg += f"\n检测到可能的虚构数据: {validation_result['fabricated_data']}"
                    
                    if validation_result["missing_responses"]:
                        warning_msg += f"\n缺少工具响应: {validation_result['missing_responses']}"
                    
                    result["messages"][-1].content = original_content + warning_msg
        
        return result
    
    return validated_analyst_node

def enhance_system_message_with_validation(system_message: str) -> str:
    """
    增强系统消息，添加数据验证要求
    
    Args:
        system_message: 原始系统消息
        
    Returns:
        增强后的系统消息
    """
    validation_instructions = """

**数据验证要求**:
1. **严禁虚构**: 绝对不允许编造任何公司名称、财务数据或新闻内容
2. **工具优先**: 必须使用工具获取数据，不得基于训练数据推测
3. **明确标注**: 如果工具未返回数据，必须明确说明"无法获取相关数据"
4. **数据来源**: 在报告中明确标注每项数据的来源工具
5. **错误处理**: 如果工具调用失败，必须如实报告错误情况

**特别注意**:
- 对于A股股票（如603127.SH），公司名称必须通过get_stock_individual_info工具获取
- 不得将A股公司错误识别为美股公司（如阿里巴巴、苹果等）
- 财务数据必须来自真实的工具调用结果，不得使用虚构的数字
"""
    
    return system_message + validation_instructions
