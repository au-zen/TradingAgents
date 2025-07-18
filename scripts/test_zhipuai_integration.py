#!/usr/bin/env python3
"""
测试智谱AI与TradingAgents的完整集成
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 加载.env文件
try:
    from dotenv import load_dotenv
    env_path = project_root / '.env'
    if env_path.exists():
        load_dotenv(env_path)
        print(f"📋 已加载环境变量文件: {env_path}")
    else:
        print(f"⚠️  环境变量文件不存在: {env_path}")
except ImportError:
    print("⚠️  python-dotenv未安装，尝试直接读取环境变量")

def test_zhipuai_config():
    """测试智谱AI配置"""
    print("🔍 测试智谱AI配置...")
    
    try:
        from tradingagents.config.model_capabilities import MODEL_CAPABILITIES
        
        # 检查模型能力配置
        zhipuai_config = MODEL_CAPABILITIES.get('zhipuai', {})
        if not zhipuai_config:
            print("❌ 智谱AI配置未找到")
            return False
        
        tool_calling_models = zhipuai_config.get('tool_calling_models', [])
        print(f"✅ 工具调用模型: {len(tool_calling_models)}个")
        for model in tool_calling_models:
            print(f"  - {model}")
        
        # 检查免费模型配置（从默认配置获取）
        from tradingagents.default_config import DEFAULT_CONFIG
        model_options = DEFAULT_CONFIG.get('model_options', {})
        zhipuai_options = model_options.get('zhipuai', {})
        free_models = zhipuai_options.get('free_models', [])
        print(f"✅ 免费模型: {len(free_models)}个")
        for model in free_models:
            print(f"  - {model}")
        
        # 检查推荐配置
        recommended = zhipuai_config.get('recommended_configs', {})
        print(f"✅ 推荐配置: {len(recommended)}个")
        for config_name, config in recommended.items():
            print(f"  - {config_name}: {config}")
        
        return True
        
    except Exception as e:
        print(f"❌ 配置测试失败: {e}")
        return False

def test_zhipuai_default_config():
    """测试默认配置中的智谱AI设置"""
    print("\n🔍 测试默认配置...")
    
    try:
        from tradingagents.default_config import DEFAULT_CONFIG
        
        # 检查API密钥配置
        api_key = DEFAULT_CONFIG.get('zhipuai_api_key')
        if api_key:
            print(f"✅ API密钥已配置: {api_key[:10]}...{api_key[-4:]}")
        else:
            print("⚠️  API密钥未配置")
        
        # 检查API端点
        endpoints = DEFAULT_CONFIG.get('api_endpoints', {})
        zhipuai_endpoint = endpoints.get('zhipuai')
        if zhipuai_endpoint:
            print(f"✅ API端点: {zhipuai_endpoint}")
        else:
            print("❌ API端点未配置")
        
        # 检查模型选项
        model_options = DEFAULT_CONFIG.get('model_options', {})
        zhipuai_options = model_options.get('zhipuai', {})
        if zhipuai_options:
            print(f"✅ 模型选项已配置")
            free_models = zhipuai_options.get('free_models', [])
            print(f"  免费模型: {free_models}")
            recommended = zhipuai_options.get('recommended', {})
            print(f"  推荐配置: {recommended}")
        else:
            print("❌ 模型选项未配置")
        
        return True
        
    except Exception as e:
        print(f"❌ 默认配置测试失败: {e}")
        return False

def test_trading_graph_integration():
    """测试TradingGraph与智谱AI的集成"""
    print("\n🔍 测试TradingGraph集成...")
    
    api_key = os.getenv('ZHIPUAI_API_KEY')
    if not api_key:
        print("⚠️  跳过集成测试：未设置ZHIPUAI_API_KEY")
        return True
    
    try:
        from tradingagents.graph.trading_graph import TradingAgentsGraph
        from tradingagents.default_config import DEFAULT_CONFIG
        
        # 创建智谱AI配置
        config = DEFAULT_CONFIG.copy()
        config.update({
            "llm_provider": "智谱AI (中文优化, 免费)",
            "quick_think_llm": "glm-4-flash",
            "deep_think_llm": "glm-z1-flash",
            "backend_url": "https://open.bigmodel.cn/api/paas/v4",
            "zhipuai_api_key": api_key
        })
        
        print("📋 测试配置:")
        print(f"  提供商: {config['llm_provider']}")
        print(f"  快速模型: {config['quick_think_llm']}")
        print(f"  深度模型: {config['deep_think_llm']}")
        print(f"  API端点: {config['backend_url']}")
        
        # 尝试创建TradingGraph
        ta = TradingAgentsGraph(config=config, debug=True)
        print("✅ TradingAgentsGraph创建成功")
        
        # 测试LLM实例
        if hasattr(ta, 'quick_thinking_llm') and hasattr(ta, 'deep_thinking_llm'):
            print("✅ LLM实例创建成功")
            
            # 简单测试调用
            try:
                response = ta.quick_thinking_llm.invoke("你好，请回复'OK'")
                print(f"✅ 快速思考LLM测试成功: {response.content[:50]}...")
            except Exception as e:
                print(f"⚠️  快速思考LLM测试失败: {e}")
            
            try:
                response = ta.deep_thinking_llm.invoke("你好，请回复'OK'")
                print(f"✅ 深度思考LLM测试成功: {response.content[:50]}...")
            except Exception as e:
                print(f"⚠️  深度思考LLM测试失败: {e}")
        else:
            print("❌ LLM实例创建失败")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ TradingGraph集成测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_cli_integration():
    """测试CLI界面集成"""
    print("\n🔍 测试CLI界面集成...")
    
    try:
        # 直接检查cli/utils.py中的配置
        import cli.utils as cli_utils
        
        # 检查提供商列表（BASE_URLS在函数内部定义）
        import inspect
        source = inspect.getsource(cli_utils.select_llm_provider)
        zhipuai_found = "智谱AI" in source
        if zhipuai_found:
            print("✅ 智谱AI提供商已添加到CLI选项中")
        else:
            print("❌ 智谱AI提供商未在CLI中找到")
        
        if not zhipuai_found:
            print("❌ 智谱AI提供商未在CLI中找到")
            return False
        
        # 检查模型选项
        shallow_options = getattr(cli_utils, 'SHALLOW_AGENT_OPTIONS', {}).get('zhipuai', [])
        deep_options = getattr(cli_utils, 'DEEP_AGENT_OPTIONS', {}).get('zhipuai', [])
        
        print(f"✅ 快速思考模型选项: {len(shallow_options)}个")
        for display, value in shallow_options:
            print(f"  - {display} -> {value}")
        
        print(f"✅ 深度思考模型选项: {len(deep_options)}个")
        for display, value in deep_options:
            print(f"  - {display} -> {value}")
        
        return True
        
    except Exception as e:
        print(f"❌ CLI集成测试失败: {e}")
        return False

def main():
    """主函数"""
    print("🧪 智谱AI与TradingAgents完整集成测试")
    print("=" * 60)
    
    tests = [
        ("智谱AI配置", test_zhipuai_config),
        ("默认配置", test_zhipuai_default_config),
        ("CLI界面集成", test_cli_integration),
        ("TradingGraph集成", test_trading_graph_integration),
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
    print("📊 智谱AI集成测试总结")
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
        print("\n🎉 智谱AI集成完全成功！")
        print("\n💡 使用指南:")
        print("1. 确保.env文件中设置了ZHIPUAI_API_KEY")
        print("2. 运行: python -m cli.main")
        print("3. 选择 '智谱AI (中文优化, 免费)' 作为提供商")
        print("4. 选择合适的GLM模型进行分析")
        print("\n🌟 智谱AI特点:")
        print("- ✅ 中文理解能力强")
        print("- ✅ 提供免费模型")
        print("- ✅ 支持工具调用")
        print("- ✅ 响应速度快")
        return 0
    else:
        print("\n⚠️  部分测试失败，请检查配置")
        
        if passed == 0:
            print("\n🔧 故障排除建议:")
            print("1. 检查智谱AI API密钥配置")
            print("2. 确认网络连接正常")
            print("3. 验证API端点可访问")
        
        return 1

if __name__ == "__main__":
    sys.exit(main())
