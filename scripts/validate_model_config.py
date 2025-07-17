#!/usr/bin/env python3
"""
模型配置验证脚本
检查当前配置的模型是否支持工具调用
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tradingagents.default_config import DEFAULT_CONFIG
from tradingagents.config.model_capabilities import (
    validate_model_config, 
    get_recommended_config,
    get_free_tool_calling_models,
    is_tool_calling_supported
)

def main():
    """主验证函数"""
    print("🔍 TradingAgents 模型配置验证")
    print("=" * 50)
    
    # 获取当前配置
    provider = DEFAULT_CONFIG["llm_provider"]
    deep_think_llm = DEFAULT_CONFIG["deep_think_llm"]
    quick_think_llm = DEFAULT_CONFIG["quick_think_llm"]

    # 提取提供商名称（去除描述文字）
    provider_name = provider.lower().split()[0] if provider else ""

    print(f"当前配置:")
    print(f"  提供商: {provider}")
    print(f"  提取的提供商名称: {provider_name}")
    print(f"  Deep-thinking模型: {deep_think_llm}")
    print(f"  Quick-thinking模型: {quick_think_llm}")
    print()

    # 验证配置
    validation_result = validate_model_config(provider_name, deep_think_llm, quick_think_llm)
    
    if validation_result["valid"]:
        print("✅ 模型配置验证通过！")
        print("   所有模型都支持工具调用。")
    else:
        print("❌ 模型配置验证失败！")
        
        if validation_result["errors"]:
            print("\n错误:")
            for error in validation_result["errors"]:
                print(f"  ❌ {error}")
        
        if validation_result["warnings"]:
            print("\n警告:")
            for warning in validation_result["warnings"]:
                print(f"  ⚠️  {warning}")
    
    print()
    
    # 显示推荐配置
    print("💡 推荐配置:")
    recommended = get_recommended_config(provider_name, "production")
    if recommended:
        print(f"  生产环境:")
        print(f"    Deep-thinking: {recommended.get('deep_think_llm', 'N/A')}")
        print(f"    Quick-thinking: {recommended.get('quick_think_llm', 'N/A')}")
    
    recommended_dev = get_recommended_config(provider, "development")
    if recommended_dev:
        print(f"  开发环境:")
        print(f"    Deep-thinking: {recommended_dev.get('deep_think_llm', 'N/A')}")
        print(f"    Quick-thinking: {recommended_dev.get('quick_think_llm', 'N/A')}")
    
    print()
    
    # 显示免费模型选项
    print("🆓 免费且支持工具调用的模型:")
    free_models = get_free_tool_calling_models(provider)
    if free_models:
        for model in free_models:
            print(f"  ✅ {model}")
    else:
        print(f"  ❌ {provider} 没有免费的工具调用模型")
    
    print()
    
    # 显示其他提供商的免费选项
    print("🌐 其他提供商的免费工具调用模型:")
    other_providers = ["openrouter", "groq", "google", "ollama"]
    for other_provider in other_providers:
        if other_provider != provider:
            other_free = get_free_tool_calling_models(other_provider)
            if other_free:
                print(f"  {other_provider.upper()}:")
                for model in other_free[:2]:  # 只显示前2个
                    print(f"    ✅ {model}")
    
    print()
    
    # 提供修复建议
    if not validation_result["valid"]:
        print("🔧 修复建议:")
        print("1. 更新 .env 文件中的模型配置:")
        
        recommended = get_recommended_config(provider_name, "production")
        if recommended:
            print(f"   DEEP_THINK_LLM={recommended.get('deep_think_llm', deep_think_llm)}")
            print(f"   QUICK_THINK_LLM={recommended.get('quick_think_llm', quick_think_llm)}")
        
        print("\n2. 或者切换到支持工具调用的提供商:")
        print("   LLM_PROVIDER=groq")
        print("   DEEP_THINK_LLM=llama3-groq-70b-8192-tool-use-preview")
        print("   QUICK_THINK_LLM=llama3-groq-8b-8192-tool-use-preview")
        
        print("\n3. 本地部署选项 (Ollama):")
        print("   LLM_PROVIDER=ollama")
        print("   DEEP_THINK_LLM=qwen3:14b")
        print("   QUICK_THINK_LLM=qwen3:8b")
    
    print()
    print("📚 更多信息请查看: docs/MODEL_CONFIGURATION_RECOMMENDATIONS.md")
    
    return 0 if validation_result["valid"] else 1

if __name__ == "__main__":
    sys.exit(main())
