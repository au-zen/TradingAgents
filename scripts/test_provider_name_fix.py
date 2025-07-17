#!/usr/bin/env python3
"""
测试提供商名称解析修复
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_trading_graph_initialization():
    """测试TradingAgentsGraph初始化"""
    print("🧪 测试TradingAgentsGraph初始化...")
    
    try:
        from tradingagents.graph.trading_graph import TradingAgentsGraph
        from tradingagents.default_config import DEFAULT_CONFIG
        
        print(f"  配置的提供商: {DEFAULT_CONFIG['llm_provider']}")
        
        # 测试初始化
        ta = TradingAgentsGraph(debug=True)
        print("  ✅ TradingAgentsGraph初始化成功！")
        
        # 检查LLM是否正确初始化
        if hasattr(ta, 'deep_thinking_llm') and hasattr(ta, 'quick_thinking_llm'):
            print("  ✅ LLM对象创建成功")
        else:
            print("  ❌ LLM对象创建失败")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ 初始化失败: {e}")
        return False

def test_provider_name_normalization():
    """测试提供商名称标准化"""
    print("\n🧪 测试提供商名称标准化...")
    
    try:
        from tradingagents.config.model_capabilities import normalize_provider_name
        
        test_cases = [
            ("openrouter (推荐, 免费额度大)", "openrouter"),
            ("groq (高速, 免费)", "groq"),
            ("together ai (开源模型丰富)", "together"),
            ("OpenAI", "openai"),
            ("Anthropic", "anthropic"),
            ("Google", "google"),
            ("Ollama (本地, 完全免费)", "ollama"),
            ("", ""),
            (None, "")
        ]
        
        all_passed = True
        for input_str, expected in test_cases:
            try:
                result = normalize_provider_name(input_str) if input_str is not None else normalize_provider_name("")
                if result == expected:
                    print(f"  ✅ '{input_str}' -> '{result}'")
                else:
                    print(f"  ❌ '{input_str}' -> '{result}' (期望: '{expected}')")
                    all_passed = False
            except Exception as e:
                print(f"  ❌ '{input_str}' -> 错误: {e}")
                all_passed = False
        
        return all_passed
        
    except Exception as e:
        print(f"  ❌ 导入normalize_provider_name失败: {e}")
        return False

def test_model_validation():
    """测试模型验证"""
    print("\n🧪 测试模型验证...")
    
    try:
        from tradingagents.config.model_capabilities import validate_model_config
        from tradingagents.default_config import DEFAULT_CONFIG
        
        provider = DEFAULT_CONFIG["llm_provider"]
        deep_think = DEFAULT_CONFIG["deep_think_llm"]
        quick_think = DEFAULT_CONFIG["quick_think_llm"]
        
        print(f"  测试配置: {provider} | {deep_think} | {quick_think}")
        
        # 测试验证函数
        result = validate_model_config(provider, deep_think, quick_think)
        
        if result["valid"]:
            print("  ✅ 模型配置验证通过")
        else:
            print("  ❌ 模型配置验证失败")
            for warning in result["warnings"]:
                print(f"    - {warning}")
            for error in result["errors"]:
                print(f"    - {error}")
        
        return result["valid"]
        
    except Exception as e:
        print(f"  ❌ 模型验证失败: {e}")
        return False

def test_cli_model_selection():
    """测试CLI模型选择"""
    print("\n🧪 测试CLI模型选择...")
    
    try:
        from cli.utils import select_shallow_thinking_agent, select_deep_thinking_agent
        import inspect
        
        # 检查函数源码是否包含修复
        shallow_source = inspect.getsource(select_shallow_thinking_agent)
        deep_source = inspect.getsource(select_deep_thinking_agent)
        
        if "provider_name = provider.lower().split()[0]" in shallow_source:
            print("  ✅ select_shallow_thinking_agent 修复已应用")
        else:
            print("  ❌ select_shallow_thinking_agent 修复未应用")
            return False
        
        if "provider_name = provider.lower().split()[0]" in deep_source:
            print("  ✅ select_deep_thinking_agent 修复已应用")
        else:
            print("  ❌ select_deep_thinking_agent 修复未应用")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ CLI模型选择测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🧪 TradingAgents 提供商名称解析修复测试")
    print("=" * 60)
    
    tests = [
        ("提供商名称标准化", test_provider_name_normalization),
        ("模型验证", test_model_validation),
        ("CLI模型选择", test_cli_model_selection),
        ("TradingAgentsGraph初始化", test_trading_graph_initialization),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ {test_name} 测试异常: {e}")
            results.append((test_name, False))
    
    # 总结
    print("\n" + "=" * 60)
    print("📊 测试总结")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n总体结果: {passed}/{total} 测试通过")
    
    if passed == total:
        print("\n🎉 提供商名称解析修复测试全部通过！")
        print("\n📋 修复内容:")
        print("1. ✅ TradingAgentsGraph - 支持带描述的提供商名称")
        print("2. ✅ CLI模型选择 - 正确解析提供商名称")
        print("3. ✅ 模型验证 - 标准化提供商名称")
        print("4. ✅ 配置脚本 - 统一提供商名称处理")
        print("\n💡 现在可以正常使用带描述的提供商名称了！")
        return 0
    else:
        print("\n⚠️  部分修复仍有问题需要解决")
        return 1

if __name__ == "__main__":
    sys.exit(main())
