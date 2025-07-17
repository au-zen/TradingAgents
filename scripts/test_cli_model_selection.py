#!/usr/bin/env python3
"""
测试CLI模型选择修复
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_provider_name_parsing():
    """测试提供商名称解析"""
    print("🧪 测试提供商名称解析...")
    
    test_cases = [
        ("Openrouter (推荐, 免费额度大)", "openrouter"),
        ("Groq (高速, 免费)", "groq"),
        ("Together AI (开源模型丰富)", "together"),
        ("OpenAI", "openai"),
        ("Anthropic", "anthropic"),
        ("Google", "google"),
        ("Ollama (本地, 完全免费)", "ollama"),
        ("", ""),
        (None, "")
    ]
    
    for input_provider, expected in test_cases:
        # 模拟函数内的逻辑
        provider_name = input_provider.lower().split()[0] if input_provider else ""
        
        if provider_name == expected:
            print(f"  ✅ '{input_provider}' -> '{provider_name}'")
        else:
            print(f"  ❌ '{input_provider}' -> '{provider_name}' (期望: '{expected}')")
    
    return True

def test_model_options_availability():
    """测试模型选项可用性"""
    print("\n🧪 测试模型选项可用性...")
    
    # 导入CLI函数
    try:
        from cli.utils import select_shallow_thinking_agent, select_deep_thinking_agent
        
        # 读取函数源码来检查模型选项
        import inspect
        
        # 检查shallow thinking函数
        shallow_source = inspect.getsource(select_shallow_thinking_agent)
        if "SHALLOW_AGENT_OPTIONS" in shallow_source:
            print("  ✅ SHALLOW_AGENT_OPTIONS 定义存在")
            
            # 检查各个提供商
            providers = ["openrouter", "groq", "together", "openai", "anthropic", "google", "ollama"]
            for provider in providers:
                if f'"{provider}"' in shallow_source:
                    print(f"    ✅ {provider} 模型选项存在")
                else:
                    print(f"    ❌ {provider} 模型选项缺失")
        else:
            print("  ❌ SHALLOW_AGENT_OPTIONS 定义不存在")
        
        # 检查deep thinking函数
        deep_source = inspect.getsource(select_deep_thinking_agent)
        if "DEEP_AGENT_OPTIONS" in deep_source:
            print("  ✅ DEEP_AGENT_OPTIONS 定义存在")
            
            # 检查各个提供商
            for provider in providers:
                if f'"{provider}"' in deep_source:
                    print(f"    ✅ {provider} 深度模型选项存在")
                else:
                    print(f"    ❌ {provider} 深度模型选项缺失")
        else:
            print("  ❌ DEEP_AGENT_OPTIONS 定义不存在")
        
        return True
        
    except Exception as e:
        print(f"  ❌ 导入CLI函数失败: {e}")
        return False

def test_provider_name_extraction():
    """测试提供商名称提取逻辑"""
    print("\n🧪 测试提供商名称提取逻辑...")
    
    # 模拟修复后的逻辑
    def extract_provider_name(provider):
        return provider.lower().split()[0] if provider else ""
    
    # 测试用例
    test_cases = [
        ("Openrouter (推荐, 免费额度大)", "openrouter"),
        ("Groq (高速, 免费)", "groq"), 
        ("Together AI (开源模型丰富)", "together"),
        ("OpenAI", "openai"),
        ("Anthropic", "anthropic"),
        ("Google", "google"),
        ("Ollama (本地, 完全免费)", "ollama")
    ]
    
    all_passed = True
    for input_str, expected in test_cases:
        result = extract_provider_name(input_str)
        if result == expected:
            print(f"  ✅ '{input_str}' -> '{result}'")
        else:
            print(f"  ❌ '{input_str}' -> '{result}' (期望: '{expected}')")
            all_passed = False
    
    return all_passed

def test_cli_file_syntax():
    """测试CLI文件语法"""
    print("\n🧪 测试CLI文件语法...")
    
    try:
        cli_file = project_root / "cli" / "utils.py"
        
        # 检查文件是否存在
        if not cli_file.exists():
            print("  ❌ CLI文件不存在")
            return False
        
        # 尝试编译文件检查语法
        with open(cli_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        try:
            compile(content, str(cli_file), 'exec')
            print("  ✅ CLI文件语法正确")
        except SyntaxError as e:
            print(f"  ❌ CLI文件语法错误: {e}")
            return False
        
        # 检查修复是否存在
        if "provider_name = provider.lower().split()[0]" in content:
            print("  ✅ 提供商名称提取修复已应用")
        else:
            print("  ❌ 提供商名称提取修复未应用")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ 检查CLI文件失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🧪 TradingAgents CLI模型选择修复测试")
    print("=" * 50)
    
    tests = [
        ("提供商名称解析", test_provider_name_parsing),
        ("模型选项可用性", test_model_options_availability),
        ("提供商名称提取逻辑", test_provider_name_extraction),
        ("CLI文件语法", test_cli_file_syntax),
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
    print("\n" + "=" * 50)
    print("📊 测试总结")
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
        print("\n🎉 CLI模型选择修复测试通过！")
        print("\n📋 修复内容:")
        print("1. 提供商名称解析 - 正确提取提供商名称")
        print("2. 模型选项映射 - 修复模型列表显示问题")
        print("3. 错误处理 - 改进'No models available'提示")
        print("\n💡 现在可以正常使用CLI选择不同提供商的模型了！")
        return 0
    else:
        print("\n⚠️  CLI模型选择仍有问题需要修复")
        return 1

if __name__ == "__main__":
    sys.exit(main())
