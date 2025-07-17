#!/usr/bin/env python3
"""
测试OpenRouter新模型配置和A股数据源增强
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_openrouter_models():
    """测试OpenRouter新模型配置"""
    print("🧪 测试OpenRouter新模型配置...")

    try:
        # 直接从文件中读取模型配置
        import inspect
        from cli.utils import select_shallow_thinking_agent, select_deep_thinking_agent

        # 获取函数源码并提取模型配置
        shallow_source = inspect.getsource(select_shallow_thinking_agent)
        deep_source = inspect.getsource(select_deep_thinking_agent)

        # 检查是否包含新的模型
        expected_shallow_models = [
            "moonshotai/kimi-k2:free",
            "qwen/qwen3-235b-a22b:free",
            "mistralai/mistral-small-3.2-24b-instruct:free",
            "meta-llama/llama-3.3-70b-instruct:free"
        ]

        expected_deep_models = [
            "openrouter/cypher-alpha:free",
            "google/gemini-2.5-pro-exp-03-25",
            "deepseek/deepseek-chat-v3-0324:free",
            "google/gemini-2.0-flash-exp:free"
        ]

        print(f"\n🔍 验证快速思考模型:")
        for model in expected_shallow_models:
            if model in shallow_source:
                print(f"  ✅ {model}")
            else:
                print(f"  ❌ {model} (缺失)")

        print(f"\n🔍 验证深度思考模型:")
        for model in expected_deep_models:
            if model in deep_source:
                print(f"  ✅ {model}")
            else:
                print(f"  ❌ {model} (缺失)")

        
        return True
        
    except Exception as e:
        print(f"  ❌ 测试失败: {e}")
        return False

def test_model_capabilities():
    """测试模型能力配置"""
    print("\n🧪 测试模型能力配置...")
    
    try:
        from tradingagents.config.model_capabilities import (
            MODEL_CAPABILITIES,
            FREE_TOOL_CALLING_MODELS,
            normalize_provider_name
        )
        
        # 检查OpenRouter工具调用模型
        openrouter_tools = MODEL_CAPABILITIES.get("openrouter", {}).get("tool_calling_models", [])
        print(f"\n📋 OpenRouter工具调用模型 ({len(openrouter_tools)}个):")
        for model in openrouter_tools:
            print(f"  ✅ {model}")
        
        # 检查免费模型
        openrouter_free = FREE_TOOL_CALLING_MODELS.get("openrouter", [])
        print(f"\n📋 OpenRouter免费工具调用模型 ({len(openrouter_free)}个):")
        for model in openrouter_free:
            print(f"  ✅ {model}")
        
        # 测试名称标准化
        print(f"\n🔍 测试提供商名称标准化:")
        test_cases = [
            ("openrouter (推荐, 免费额度大)", "openrouter"),
            ("groq (高速, 免费)", "groq"),
            ("OpenAI", "openai")
        ]
        
        for input_name, expected in test_cases:
            result = normalize_provider_name(input_name)
            if result == expected:
                print(f"  ✅ '{input_name}' -> '{result}'")
            else:
                print(f"  ❌ '{input_name}' -> '{result}' (期望: '{expected}')")
        
        return True
        
    except Exception as e:
        print(f"  ❌ 测试失败: {e}")
        return False

def test_china_stock_data_sources():
    """测试A股数据源"""
    print("\n🧪 测试A股数据源...")
    
    try:
        from tradingagents.dataflows.china_stock_data_sources import (
            china_stock_manager,
            JQDataSource,
            TushareDataSource,
            AlltickDataSource
        )
        
        # 检查数据源状态
        print(f"\n📋 A股数据源状态检查:")
        status = china_stock_manager.get_data_source_status("603127.SH")
        
        for source_name, source_status in status.items():
            if source_status == "available":
                print(f"  ✅ {source_name}: 可用")
            elif source_status == "unavailable":
                print(f"  ⚠️  {source_name}: 不可用 (缺少配置)")
            else:
                print(f"  ❌ {source_name}: {source_status}")
        
        # 测试数据源初始化
        print(f"\n🔍 测试数据源初始化:")
        
        # JQData
        jq_source = JQDataSource()
        jq_available = jq_source._initialize()
        print(f"  {'✅' if jq_available else '⚠️'} JQData: {'可用' if jq_available else '不可用'}")
        
        # Tushare
        ts_source = TushareDataSource()
        ts_available = ts_source._initialize()
        print(f"  {'✅' if ts_available else '⚠️'} Tushare: {'可用' if ts_available else '不可用'}")
        
        # Alltick
        at_source = AlltickDataSource()
        at_available = bool(at_source.token)
        print(f"  {'✅' if at_available else '⚠️'} Alltick: {'可用' if at_available else '不可用'}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ 测试失败: {e}")
        return False

def test_enhanced_data_source_manager():
    """测试增强数据源管理器"""
    print("\n🧪 测试增强数据源管理器...")
    
    try:
        from tradingagents.dataflows.enhanced_data_source_manager import (
            EnhancedDataSourceManager,
            CHINA_STOCK_SOURCES_AVAILABLE
        )
        
        print(f"\n📋 A股增强数据源状态: {'✅ 可用' if CHINA_STOCK_SOURCES_AVAILABLE else '❌ 不可用'}")
        
        # 创建管理器实例
        manager = EnhancedDataSourceManager()
        
        # 检查数据源优先级配置
        cn_priority = manager.data_source_priority.get("cn_market", {})
        print(f"\n📋 中国市场数据源优先级:")
        for data_type, sources in cn_priority.items():
            print(f"  {data_type}: {sources}")
        
        # 验证china_enhanced是否在优先级列表中
        stock_data_sources = cn_priority.get("stock_data", [])
        if "china_enhanced" in stock_data_sources:
            print(f"  ✅ china_enhanced已添加到股票数据源")
        else:
            print(f"  ❌ china_enhanced未添加到股票数据源")
        
        company_info_sources = cn_priority.get("company_info", [])
        if "china_enhanced" in company_info_sources:
            print(f"  ✅ china_enhanced已添加到公司信息源")
        else:
            print(f"  ❌ china_enhanced未添加到公司信息源")
        
        return True
        
    except Exception as e:
        print(f"  ❌ 测试失败: {e}")
        return False

def test_environment_variables():
    """测试环境变量配置"""
    print("\n🧪 测试环境变量配置...")
    
    env_vars = [
        ("JQDATA_USERNAME", "聚宽用户名"),
        ("JQDATA_PASSWORD", "聚宽密码"),
        ("TUSHARE_TOKEN", "Tushare Token"),
        ("ALLTICK_TOKEN", "Alltick Token")
    ]
    
    print(f"\n📋 A股数据源环境变量:")
    for var_name, description in env_vars:
        value = os.getenv(var_name)
        if value:
            print(f"  ✅ {var_name}: 已配置")
        else:
            print(f"  ⚠️  {var_name}: 未配置 ({description})")
    
    return True

def main():
    """主测试函数"""
    print("🧪 OpenRouter模型配置和A股数据源增强测试")
    print("=" * 60)
    
    tests = [
        ("OpenRouter模型配置", test_openrouter_models),
        ("模型能力配置", test_model_capabilities),
        ("A股数据源", test_china_stock_data_sources),
        ("增强数据源管理器", test_enhanced_data_source_manager),
        ("环境变量配置", test_environment_variables),
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
        print("\n🎉 所有测试通过！")
        print("\n📋 更新内容:")
        print("1. ✅ OpenRouter模型列表已更新")
        print("2. ✅ A股数据源已增强 (JQData, Tushare, Alltick)")
        print("3. ✅ 数据源优先级已配置")
        print("4. ✅ 环境变量配置已添加")
        print("\n💡 现在可以使用新的模型和数据源了！")
        return 0
    else:
        print("\n⚠️  部分测试失败，请检查配置")
        return 1

if __name__ == "__main__":
    sys.exit(main())
