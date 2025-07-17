#!/usr/bin/env python3
"""
测试A股分析修复效果
验证公司识别和新闻来源是否正确
"""

import sys
import os
from pathlib import Path
from tradingagents.agents.utils.agent_utils import Toolkit
from tradingagents.default_config import DEFAULT_CONFIG
from tradingagents.agents.analysts.fundamentals_analyst import create_fundamentals_analyst
from tradingagents.agents.analysts.news_analyst import create_news_analyst
from tradingagents.agents.analysts.social_media_analyst import create_social_media_analyst
from langchain_openai import ChatOpenAI

def test_company_identification():
    """测试公司识别功能"""
    print("=== 测试公司识别功能 ===\n")
    
    toolkit = Toolkit(config=DEFAULT_CONFIG)
    
    # 测试A股ticker
    ticker = "603127.SH"
    print(f"测试ticker: {ticker}")
    
    try:
        result = toolkit.get_stock_individual_info.invoke({"ticker": ticker})
        print(f"工具调用结果:\n{result}\n")
        
        # 解析公司名称
        lines = result.split('\n')
        company_name = None
        for line in lines:
            if line.startswith("公司名称:"):
                company_name = line.replace("公司名称:", "").strip()
                break
        
        if company_name:
            print(f"✅ 成功提取公司名称: {company_name}")
            expected_name = "昭衍新药"
            if expected_name in company_name:
                print(f"✅ 公司名称正确包含: {expected_name}")
                return True, company_name
            else:
                print(f"❌ 公司名称不正确，期望包含: {expected_name}")
                return False, company_name
        else:
            print("❌ 未能提取公司名称")
            return False, None
            
    except Exception as e:
        print(f"❌ 工具调用失败: {e}")
        return False, None

def test_news_sources():
    """测试新闻来源"""
    print("\n=== 测试新闻来源 ===\n")
    
    toolkit = Toolkit(config=DEFAULT_CONFIG)
    ticker = "603127.SH"
    
    # 测试A股新闻工具
    print("测试 get_stock_zh_a_news...")
    try:
        result = toolkit.get_stock_zh_a_news.invoke({"ticker": ticker, "limit": 3})
        print(f"A股新闻结果:\n{result[:500]}...\n")
        
        # 检查是否包含中文内容
        if "昭衍新药" in result or "603127" in result:
            print("✅ A股新闻包含相关公司信息")
            chinese_content = len([c for c in result if '\u4e00' <= c <= '\u9fff']) > 100
            if chinese_content:
                print("✅ A股新闻主要为中文内容")
                return True
            else:
                print("❌ A股新闻中文内容不足")
                return False
        else:
            print("❌ A股新闻不包含相关公司信息")
            return False
            
    except Exception as e:
        print(f"❌ A股新闻工具调用失败: {e}")
        return False

def test_fundamentals_analyst():
    """测试基本面分析师"""
    print("\n=== 测试基本面分析师 ===\n")
    
    try:
        # 初始化LLM和工具 - 使用支持工具调用的模型
        llm = ChatOpenAI(
            model="deepseek/deepseek-r1-distill-qwen-14b:free",  # 支持工具调用的免费模型
            base_url=DEFAULT_CONFIG["backend_url"],
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        toolkit = Toolkit(config=DEFAULT_CONFIG)
        
        # 创建基本面分析师
        fundamentals_analyst = create_fundamentals_analyst(llm, toolkit)
        
        # 准备测试状态
        test_state = {
            "company_of_interest": "603127.SH",
            "company_name": "603127.SH",  # 初始值，应该被工具调用更新
            "trade_date": "2025-07-17",
            "messages": []
        }
        
        print("运行基本面分析师...")
        result = fundamentals_analyst(test_state)
        
        print(f"分析师返回消息数: {len(result.get('messages', []))}")
        
        if result.get("messages"):
            last_message = result["messages"][-1]
            content = str(last_message.content)
            
            print(f"分析师输出内容长度: {len(content)}")
            print(f"分析师输出预览:\n{content[:300]}...\n")
            
            # 检查是否包含正确的公司名称
            if "昭衍新药" in content:
                print("✅ 基本面分析包含正确的公司名称")
            else:
                print("❌ 基本面分析未包含正确的公司名称")
                if "阿里巴巴" in content:
                    print("❌ 检测到错误的公司名称: 阿里巴巴")
            
            # 检查是否有工具调用
            if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
                print(f"✅ 检测到 {len(last_message.tool_calls)} 个工具调用")
                for tool_call in last_message.tool_calls:
                    print(f"  - {tool_call.get('name', 'unknown')}({tool_call.get('args', {})})")
            else:
                print("⚠️  未检测到工具调用")
            
            # 检查是否为中文内容
            chinese_chars = len([c for c in content if '\u4e00' <= c <= '\u9fff'])
            if chinese_chars > 100:
                print("✅ 分析报告主要为中文内容")
            else:
                print("❌ 分析报告中文内容不足")
            
            return True
        else:
            print("❌ 基本面分析师未返回消息")
            return False
            
    except Exception as e:
        print(f"❌ 基本面分析师测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_news_analyst():
    """测试新闻分析师"""
    print("\n=== 测试新闻分析师 ===\n")
    
    try:
        # 初始化LLM和工具 - 使用支持工具调用的模型
        llm = ChatOpenAI(
            model="deepseek/deepseek-r1-distill-qwen-14b:free",  # 支持工具调用的免费模型
            base_url=DEFAULT_CONFIG["backend_url"],
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        toolkit = Toolkit(config=DEFAULT_CONFIG)
        
        # 创建新闻分析师
        news_analyst = create_news_analyst(llm, toolkit)
        
        # 准备测试状态
        test_state = {
            "company_of_interest": "603127.SH",
            "company_name": "昭衍新药",
            "trade_date": "2025-07-17",
            "messages": []
        }
        
        print("运行新闻分析师...")
        result = news_analyst(test_state)
        
        print(f"分析师返回消息数: {len(result.get('messages', []))}")
        
        if result.get("messages"):
            last_message = result["messages"][-1]
            content = str(last_message.content)
            
            print(f"分析师输出内容长度: {len(content)}")
            print(f"分析师输出预览:\n{content[:300]}...\n")
            
            # 检查是否包含正确的公司名称
            if "昭衍新药" in content:
                print("✅ 新闻分析包含正确的公司名称")
            else:
                print("❌ 新闻分析未包含正确的公司名称")
            
            # 检查是否主要为中文内容
            chinese_chars = len([c for c in content if '\u4e00' <= c <= '\u9fff'])
            english_chars = len([c for c in content if c.isalpha() and ord(c) < 256])
            
            if chinese_chars > english_chars:
                print("✅ 新闻分析主要为中文内容")
            else:
                print("❌ 新闻分析英文内容过多")
                print(f"  中文字符: {chinese_chars}, 英文字符: {english_chars}")
            
            return True
        else:
            print("❌ 新闻分析师未返回消息")
            return False
            
    except Exception as e:
        print(f"❌ 新闻分析师测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("A股分析修复效果测试\n")
    print("=" * 50)
    
    tests = [
        ("公司识别功能", test_company_identification),
        ("新闻来源", test_news_sources),
        ("基本面分析师", test_fundamentals_analyst),
        ("新闻分析师", test_news_analyst),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, result))
            status = "✅ 通过" if result else "❌ 失败"
            print(f"\n{test_name}: {status}")
        except Exception as e:
            print(f"\n❌ {test_name} 测试异常: {e}")
            results.append((test_name, False))
    
    # 总结
    print("\n" + "=" * 50)
    print("测试总结")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n总体结果: {passed}/{total} 测试通过")
    
    if passed == total:
        print("🎉 所有测试通过！A股分析修复成功！")
        return 0
    else:
        print("⚠️  部分测试失败，需要进一步修复。")
        return 1

if __name__ == "__main__":
    sys.exit(main())
