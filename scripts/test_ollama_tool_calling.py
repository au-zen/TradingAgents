#!/usr/bin/env python3
"""
测试Ollama工具调用功能
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_ollama_connection():
    """测试Ollama连接"""
    print("🔍 测试Ollama连接...")
    
    try:
        import requests
        
        response = requests.get('http://localhost:11434/api/tags', timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            print(f"✅ Ollama服务正在运行，可用模型: {len(models)}个")
            
            # 显示推荐的模型
            recommended_models = ['qwen3:latest', 'llama3.1:latest', 'mistral:latest']
            available_recommended = []
            
            for model in models:
                model_name = model.get('name', '')
                if model_name in recommended_models:
                    available_recommended.append(model_name)
                    size_gb = model.get('size', 0) / (1024**3)
                    print(f"  ✅ {model_name} ({size_gb:.1f}GB)")
            
            if not available_recommended:
                print("⚠️  推荐的模型未安装，请运行:")
                print("  ollama pull qwen3")
                print("  ollama pull llama3.1")
                return False
            
            return True
        else:
            print(f"❌ Ollama服务响应异常: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 连接Ollama失败: {e}")
        return False

def test_ollama_model_capabilities():
    """测试Ollama模型能力配置"""
    print("\n🧪 测试Ollama模型能力配置...")
    
    try:
        from tradingagents.config.model_capabilities import MODEL_CAPABILITIES
        
        ollama_config = MODEL_CAPABILITIES.get('ollama', {})
        tool_calling_models = ollama_config.get('tool_calling_models', [])
        
        print(f"📋 配置的工具调用模型: {len(tool_calling_models)}个")
        for model in tool_calling_models:
            print(f"  - {model}")
        
        # 检查推荐配置
        recommended = ollama_config.get('recommended_configs', {}).get('production', {})
        deep_model = recommended.get('deep_think_llm')
        quick_model = recommended.get('quick_think_llm')
        
        print(f"\n📋 推荐配置:")
        print(f"  深度思考模型: {deep_model}")
        print(f"  快速思考模型: {quick_model}")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试模型能力配置失败: {e}")
        return False

def test_simple_ollama_call():
    """测试简单的Ollama调用"""
    print("\n🧪 测试简单的Ollama调用...")
    
    try:
        from langchain_community.llms import Ollama
        
        # 测试qwen3模型
        llm = Ollama(model="qwen3:latest", base_url="http://localhost:11434")
        
        response = llm.invoke("你好，请用中文回答：1+1等于多少？")
        print(f"✅ Ollama响应: {response[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ 简单调用失败: {e}")
        return False

def test_trading_graph_with_ollama():
    """测试TradingGraph与Ollama的集成"""
    print("\n🧪 测试TradingGraph与Ollama集成...")
    
    try:
        from tradingagents.graph.trading_graph import TradingAgentsGraph
        from tradingagents.default_config import DEFAULT_CONFIG
        
        # 创建Ollama配置
        config = DEFAULT_CONFIG.copy()
        config.update({
            "llm_provider": "ollama",
            "quick_think_llm": "qwen3:latest",
            "deep_think_llm": "qwen3:latest",
            "backend_url": "http://localhost:11434/v1"
        })
        
        print("📋 测试配置:")
        print(f"  提供商: {config['llm_provider']}")
        print(f"  快速模型: {config['quick_think_llm']}")
        print(f"  深度模型: {config['deep_think_llm']}")
        print(f"  后端URL: {config['backend_url']}")
        
        # 尝试创建TradingGraph
        ta = TradingAgentsGraph(config=config, debug=True)
        print("✅ TradingAgentsGraph创建成功")
        
        return True
        
    except Exception as e:
        print(f"❌ TradingGraph集成测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("🧪 Ollama工具调用功能测试")
    print("=" * 50)
    
    tests = [
        ("Ollama连接", test_ollama_connection),
        ("模型能力配置", test_ollama_model_capabilities),
        ("简单Ollama调用", test_simple_ollama_call),
        ("TradingGraph集成", test_trading_graph_with_ollama),
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
        print("\n🎉 Ollama配置正常！")
        print("\n💡 使用建议:")
        print("1. 选择 'Ollama (本地, 完全免费)' 作为提供商")
        print("2. 推荐使用 qwen3:latest 作为主要模型")
        print("3. 如果遇到工具调用问题，尝试使用其他模型")
        return 0
    else:
        print("\n⚠️  部分测试失败，请检查Ollama配置")
        
        if passed == 0:
            print("\n🔧 故障排除建议:")
            print("1. 确保Ollama服务正在运行: ollama serve")
            print("2. 安装推荐模型: ollama pull qwen3")
            print("3. 检查防火墙设置")
        
        return 1

if __name__ == "__main__":
    sys.exit(main())
