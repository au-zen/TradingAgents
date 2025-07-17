#!/usr/bin/env python3
"""
工具绑定调试脚本
深入调试分析师工具绑定问题
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tradingagents.default_config import DEFAULT_CONFIG
from tradingagents.agents.utils.agent_utils import Toolkit
from tradingagents.agents.analysts.fundamentals_analyst import create_fundamentals_analyst
from tradingagents.agents.analysts.news_analyst import create_news_analyst
from tradingagents.agents.analysts.market_analyst import create_market_analyst
from tradingagents.agents.analysts.social_media_analyst import create_social_media_analyst
from langchain_openai import ChatOpenAI
from langchain_core.tools import BaseTool

def debug_toolkit_methods():
    """调试Toolkit的方法"""
    print("🔍 调试Toolkit方法...")
    
    toolkit = Toolkit(DEFAULT_CONFIG)
    
    # 检查关键方法
    key_methods = [
        'get_stock_individual_info',
        'get_stock_zh_a_news',
        'get_fundamentals',
        'get_stock_report',
        'get_stock_cg_lg',
        'get_stock_dzjy_detail'
    ]
    
    for method_name in key_methods:
        if hasattr(toolkit, method_name):
            method = getattr(toolkit, method_name)
            print(f"  ✅ {method_name}: {type(method)}")
            print(f"     是否为BaseTool: {isinstance(method, BaseTool)}")
            print(f"     是否有name属性: {hasattr(method, 'name')}")
            if hasattr(method, 'name'):
                print(f"     工具名称: {method.name}")
        else:
            print(f"  ❌ {method_name}: 不存在")
    
    return True

def debug_toolize_function():
    """调试_toolize函数"""
    print("\n🔧 调试_toolize函数...")
    
    from langchain_core.tools import BaseTool, tool
    
    def _toolize(fn):
        if isinstance(fn, BaseTool):
            return fn
        try:
            return tool(fn)
        except ValueError:
            return fn
    
    toolkit = Toolkit(DEFAULT_CONFIG)
    
    # 测试_toolize函数
    test_method = toolkit.get_stock_individual_info
    print(f"  原始方法类型: {type(test_method)}")
    print(f"  是否为BaseTool: {isinstance(test_method, BaseTool)}")
    
    toolized = _toolize(test_method)
    print(f"  _toolize后类型: {type(toolized)}")
    print(f"  _toolize后是否为BaseTool: {isinstance(toolized, BaseTool)}")
    
    if hasattr(toolized, 'name'):
        print(f"  工具名称: {toolized.name}")
    
    # 测试工具调用
    try:
        result = toolized.invoke({"ticker": "603127.SH"})
        print(f"  工具调用成功: {len(result)} 字符")
        if "昭衍新药" in result:
            print("  ✅ 返回正确的公司名称")
        else:
            print("  ❌ 返回的公司名称不正确")
    except Exception as e:
        print(f"  ❌ 工具调用失败: {e}")
    
    return True

def debug_analyst_tool_binding(analyst_name, create_analyst_func):
    """调试特定分析师的工具绑定"""
    print(f"\n🎯 调试{analyst_name}工具绑定...")
    
    try:
        # 创建LLM（使用支持工具调用的模型）
        llm = ChatOpenAI(
            model="deepseek/deepseek-r1-distill-qwen-14b:free",
            base_url=DEFAULT_CONFIG["backend_url"],
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        toolkit = Toolkit(DEFAULT_CONFIG)
        
        # 创建分析师
        analyst = create_analyst_func(llm, toolkit)
        
        # 准备测试状态
        test_state = {
            "company_of_interest": "603127.SH",
            "company_name": "603127.SH",
            "trade_date": "2025-07-17",
            "messages": []
        }
        
        print(f"  测试股票: {test_state['company_of_interest']}")
        print(f"  LLM模型: {llm.model_name}")
        
        # 尝试运行分析师（但不完整执行，只检查工具绑定）
        # 我们需要手动检查工具绑定过程
        
        # 模拟分析师内部的工具绑定逻辑
        ticker = test_state["company_of_interest"]
        
        from langchain_core.tools import BaseTool, tool
        def _toolize(fn):
            if isinstance(fn, BaseTool):
                return fn
            try:
                return tool(fn)
            except ValueError:
                return fn
        
        # 根据分析师类型确定工具配置
        if analyst_name == "fundamentals_analyst":
            if toolkit.ticker_is_china_stock(ticker):
                base_funcs = [
                    toolkit.get_stock_individual_info,
                    toolkit.get_fundamentals,
                    toolkit.get_stock_report,
                    toolkit.get_stock_cg_lg,
                    toolkit.get_stock_dzjy_detail,
                ]
                tools = [_toolize(f) for f in base_funcs]
            else:
                tools = [_toolize(toolkit.get_fundamentals)]
        
        elif analyst_name == "news_analyst":
            if toolkit.ticker_is_china_stock(ticker):
                base_funcs = [
                    toolkit.get_stock_individual_info,
                    toolkit.get_stock_zh_a_news,
                    toolkit.get_stock_notice_report,
                    toolkit.get_global_news_openai,
                ]
                tools = [_toolize(f) for f in base_funcs]
            else:
                base_funcs = [toolkit.get_global_news_openai, toolkit.get_google_news]
                tools = [_toolize(f) for f in base_funcs]
        
        elif analyst_name == "market_analyst":
            if toolkit.ticker_is_china_stock(ticker):
                base_funcs = [
                    toolkit.get_stock_individual_info,
                    toolkit.get_stock_news_openai,
                    toolkit.get_stock_lhb_detail,
                    toolkit.get_stock_cg_lg,
                    toolkit.get_stock_dzjy_detail,
                    toolkit.get_stock_report,
                    toolkit.get_stock_data,
                ]
                tools = [_toolize(f) for f in base_funcs]
            else:
                base_funcs = [toolkit.get_stock_data, toolkit.get_stock_indicators]
                tools = [_toolize(f) for f in base_funcs]
        
        elif analyst_name == "social_media_analyst":
            if toolkit.ticker_is_china_stock(ticker):
                base_funcs = [
                    toolkit.get_stock_individual_info,
                    toolkit.get_stock_zh_a_news,
                ]
                tools = [_toolize(f) for f in base_funcs]
            else:
                tools = [_toolize(toolkit.get_stock_news_openai)]
        
        else:
            tools = []
        
        print(f"  配置的工具数量: {len(tools)}")
        
        for i, tool_obj in enumerate(tools):
            tool_name = getattr(tool_obj, 'name', f'tool_{i}')
            tool_type = type(tool_obj).__name__
            print(f"    {i+1}. {tool_name} ({tool_type})")
            
            # 测试工具是否可调用
            if hasattr(tool_obj, 'invoke'):
                try:
                    if tool_name == 'get_stock_individual_info':
                        result = tool_obj.invoke({"ticker": ticker})
                        if "昭衍新药" in result:
                            print(f"       ✅ 工具调用成功，返回正确数据")
                        else:
                            print(f"       ⚠️  工具调用成功，但数据可能不正确")
                    else:
                        print(f"       ℹ️  工具可调用（未测试）")
                except Exception as e:
                    print(f"       ❌ 工具调用失败: {e}")
            else:
                print(f"       ❌ 工具不可调用")
        
        # 测试LLM工具绑定
        try:
            bound_llm = llm.bind_tools(tools)
            print(f"  ✅ LLM工具绑定成功")
            
            # 检查绑定后的工具
            if hasattr(bound_llm, 'kwargs') and 'tools' in bound_llm.kwargs:
                bound_tools = bound_llm.kwargs['tools']
                print(f"  绑定到LLM的工具数量: {len(bound_tools)}")
            
        except Exception as e:
            print(f"  ❌ LLM工具绑定失败: {e}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ {analyst_name}调试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主调试函数"""
    print("🐛 TradingAgents 工具绑定深度调试")
    print("=" * 60)
    
    # 检查环境
    print("检查环境...")
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print("✅ API密钥已配置")
    else:
        print("❌ API密钥未配置")
        return 1
    
    # 调试步骤
    debug_steps = [
        ("Toolkit方法检查", debug_toolkit_methods),
        ("_toolize函数测试", debug_toolize_function),
        ("fundamentals_analyst工具绑定", lambda: debug_analyst_tool_binding("fundamentals_analyst", create_fundamentals_analyst)),
        ("news_analyst工具绑定", lambda: debug_analyst_tool_binding("news_analyst", create_news_analyst)),
        ("market_analyst工具绑定", lambda: debug_analyst_tool_binding("market_analyst", create_market_analyst)),
        ("social_media_analyst工具绑定", lambda: debug_analyst_tool_binding("social_media_analyst", create_social_media_analyst)),
    ]
    
    results = []
    
    for step_name, step_func in debug_steps:
        try:
            print(f"\n{'='*20} {step_name} {'='*20}")
            result = step_func()
            results.append((step_name, result))
        except Exception as e:
            print(f"\n❌ {step_name} 异常: {e}")
            results.append((step_name, False))
    
    # 总结
    print("\n" + "=" * 60)
    print("🔍 调试总结")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for step_name, result in results:
        status = "✅ 正常" if result else "❌ 异常"
        print(f"{status} {step_name}")
        if result:
            passed += 1
    
    print(f"\n总体结果: {passed}/{total} 步骤正常")
    
    if passed == total:
        print("\n🎉 工具绑定调试完成，所有步骤正常！")
        return 0
    else:
        print("\n⚠️  发现工具绑定问题，需要进一步修复")
        return 1

if __name__ == "__main__":
    sys.exit(main())
