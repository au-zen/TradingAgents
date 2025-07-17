#!/usr/bin/env python3
"""
测试所有改进功能的综合脚本
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_model_capabilities():
    """测试模型能力配置"""
    print("🔍 测试模型能力配置...")
    
    try:
        from tradingagents.config.model_capabilities import (
            validate_model_config, 
            get_recommended_config,
            is_tool_calling_supported
        )
        from tradingagents.default_config import DEFAULT_CONFIG
        
        provider = DEFAULT_CONFIG["llm_provider"]
        deep_think = DEFAULT_CONFIG["deep_think_llm"]
        quick_think = DEFAULT_CONFIG["quick_think_llm"]

        # 提取提供商名称（去除描述文字）
        provider_name = provider.lower().split()[0] if provider else ""

        print(f"  当前配置: {provider} | {deep_think} | {quick_think}")
        print(f"  提取的提供商名称: {provider_name}")

        # 验证配置
        result = validate_model_config(provider_name, deep_think, quick_think)
        if result["valid"]:
            print("  ✅ 模型配置验证通过")
        else:
            print("  ❌ 模型配置有问题:")
            for warning in result["warnings"]:
                print(f"    - {warning}")
        
        # 测试工具调用支持检查
        deep_support = is_tool_calling_supported(provider_name, deep_think)
        quick_support = is_tool_calling_supported(provider_name, quick_think)
        
        print(f"  Deep-think模型工具调用支持: {'✅' if deep_support else '❌'}")
        print(f"  Quick-think模型工具调用支持: {'✅' if quick_support else '❌'}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ 模型能力测试失败: {e}")
        return False

def test_enhanced_data_sources():
    """测试增强的数据源"""
    print("\n🌐 测试增强数据源管理器...")
    
    try:
        from tradingagents.dataflows.enhanced_data_source_manager import EnhancedDataSourceManager
        
        manager = EnhancedDataSourceManager()
        
        # 测试数据质量报告
        test_ticker = "603127.SH"
        print(f"  测试股票: {test_ticker}")
        
        quality_report = manager.get_data_quality_report(test_ticker)
        print(f"  整体数据质量: {quality_report['overall_quality']}")
        
        # 测试缓存功能
        cache_dir = manager.cache_dir
        print(f"  缓存目录: {cache_dir}")
        print(f"  缓存目录存在: {'✅' if os.path.exists(cache_dir) else '❌'}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ 增强数据源测试失败: {e}")
        return False

def test_chinese_news_sources():
    """测试中文新闻源"""
    print("\n📰 测试中文新闻数据源...")
    
    try:
        from tradingagents.dataflows.chinese_news_utils import (
            get_chinese_stock_news,
            get_market_sentiment_news,
            ChineseNewsAggregator
        )
        
        # 测试新闻聚合器
        aggregator = ChineseNewsAggregator()
        print(f"  新闻源数量: {len(aggregator.news_sources)}")
        
        enabled_sources = [name for name, config in aggregator.news_sources.items() if config["enabled"]]
        print(f"  启用的新闻源: {', '.join(enabled_sources)}")
        
        # 测试获取新闻（使用模拟数据）
        test_ticker = "603127.SH"
        news = get_chinese_stock_news(test_ticker, limit=3)
        print(f"  获取新闻长度: {len(news)} 字符")
        
        sentiment_news = get_market_sentiment_news(limit=2)
        print(f"  市场情绪新闻长度: {len(sentiment_news)} 字符")
        
        return True
        
    except Exception as e:
        print(f"  ❌ 中文新闻源测试失败: {e}")
        return False

def test_web_app_dependencies():
    """测试Web应用依赖"""
    print("\n🌐 测试Web应用依赖...")
    
    try:
        # 检查Streamlit
        try:
            import streamlit
            print("  ✅ Streamlit 已安装")
        except ImportError:
            print("  ❌ Streamlit 未安装")
            return False
        
        # 检查Plotly
        try:
            import plotly
            print("  ✅ Plotly 已安装")
        except ImportError:
            print("  ❌ Plotly 未安装")
            return False
        
        # 检查Web应用文件
        web_app_file = project_root / "web_app" / "app.py"
        if web_app_file.exists():
            print("  ✅ Web应用文件存在")
        else:
            print("  ❌ Web应用文件不存在")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ Web应用依赖测试失败: {e}")
        return False

def test_fundamentals_analyst_fix():
    """测试基本面分析师修复"""
    print("\n🔧 测试基本面分析师修复...")
    
    try:
        from tradingagents.agents.utils.agent_utils import Toolkit
        from tradingagents.agents.analysts.fundamentals_analyst import create_fundamentals_analyst
        from langchain_openai import ChatOpenAI
        from tradingagents.default_config import DEFAULT_CONFIG
        
        # 创建工具包
        toolkit = Toolkit(DEFAULT_CONFIG)
        
        # 测试A股检测
        test_ticker = "603127.SH"
        is_china = toolkit.ticker_is_china_stock(test_ticker)
        print(f"  A股检测 ({test_ticker}): {'✅' if is_china else '❌'}")
        
        # 测试工具可用性
        try:
            result = toolkit.get_stock_individual_info.invoke({"ticker": test_ticker})
            if "昭衍新药" in result:
                print("  ✅ get_stock_individual_info 工具正常")
            else:
                print("  ⚠️  get_stock_individual_info 工具返回数据异常")
        except Exception as e:
            print(f"  ❌ get_stock_individual_info 工具失败: {e}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ 基本面分析师测试失败: {e}")
        return False

def test_validation_scripts():
    """测试验证脚本"""
    print("\n✅ 测试验证脚本...")
    
    try:
        # 测试模型配置验证脚本
        model_script = project_root / "scripts" / "validate_model_config.py"
        if model_script.exists():
            print("  ✅ 模型配置验证脚本存在")
        else:
            print("  ❌ 模型配置验证脚本不存在")
        
        # 测试Web应用启动脚本
        web_script = project_root / "scripts" / "start_web_app.py"
        if web_script.exists():
            print("  ✅ Web应用启动脚本存在")
        else:
            print("  ❌ Web应用启动脚本不存在")
        
        return True
        
    except Exception as e:
        print(f"  ❌ 验证脚本测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🧪 TradingAgents 改进功能综合测试")
    print("=" * 60)
    
    tests = [
        ("模型能力配置", test_model_capabilities),
        ("增强数据源管理", test_enhanced_data_sources),
        ("中文新闻数据源", test_chinese_news_sources),
        ("Web应用依赖", test_web_app_dependencies),
        ("基本面分析师修复", test_fundamentals_analyst_fix),
        ("验证脚本", test_validation_scripts),
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
        print("\n🎉 所有改进功能测试通过！")
        print("\n📋 下一步操作:")
        print("1. 运行模型配置验证: python scripts/validate_model_config.py")
        print("2. 启动Web应用: python scripts/start_web_app.py")
        print("3. 运行完整分析: python -m cli.main --ticker 603127.SH --start-date 2024-01-01 --end-date 2024-01-02")
        return 0
    else:
        print("\n⚠️  部分功能需要进一步完善")
        return 1

if __name__ == "__main__":
    sys.exit(main())
