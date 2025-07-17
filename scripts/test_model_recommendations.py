#!/usr/bin/env python3
"""
测试模型推荐配置功能
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_model_recommendations():
    """测试模型推荐功能"""
    print("🧪 测试模型推荐配置功能...")
    
    try:
        from tradingagents.config.model_recommendations import model_recommendations
        
        # 测试1: 加载所有配置
        print("\n1️⃣ 测试配置加载...")
        configs = model_recommendations.get_all_recommendations()
        print(f"✅ 成功加载 {len(configs)} 个配置")
        
        for key, config in configs.items():
            print(f"  • {config['name']} ({config['provider']})")
        
        # 测试2: 场景推荐
        print("\n2️⃣ 测试场景推荐...")
        scenarios = ["个人投资", "专业分析", "企业部署", "开发测试"]
        for scenario in scenarios:
            recommendations = model_recommendations.get_recommendation_by_use_case(scenario)
            print(f"  • {scenario}: {recommendations}")
        
        # 测试3: 预算推荐
        print("\n3️⃣ 测试预算推荐...")
        budgets = ["免费", "低预算", "中预算", "高预算"]
        for budget in budgets:
            recommendations = model_recommendations.get_recommendation_by_budget(budget)
            print(f"  • {budget}: {recommendations}")
        
        # 测试4: 配置命令生成
        print("\n4️⃣ 测试配置命令生成...")
        test_configs = ["high_speed_free", "balanced_recommended", "local_deployment"]
        for config_key in test_configs:
            commands = model_recommendations.generate_setup_commands(config_key)
            config = model_recommendations.get_recommendation(config_key)
            print(f"  • {config['name']}: 生成 {len(commands)} 字符的配置命令")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_web_app_integration():
    """测试Web应用集成"""
    print("\n🌐 测试Web应用集成...")
    
    try:
        # 检查Web应用文件
        web_app_file = project_root / "web_app" / "app.py"
        if not web_app_file.exists():
            print("❌ Web应用文件不存在")
            return False
        
        # 检查导入
        with open(web_app_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if "model_recommendations" in content:
                print("✅ Web应用已集成模型推荐功能")
            else:
                print("❌ Web应用未集成模型推荐功能")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Web应用集成测试失败: {e}")
        return False

def test_cli_integration():
    """测试CLI集成"""
    print("\n💻 测试CLI集成...")
    
    try:
        # 检查CLI文件
        cli_file = project_root / "cli" / "utils.py"
        if not cli_file.exists():
            print("❌ CLI文件不存在")
            return False
        
        # 检查更新
        with open(cli_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if "支持工具调用" in content:
                print("✅ CLI已更新模型选择界面")
            else:
                print("❌ CLI未更新模型选择界面")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ CLI集成测试失败: {e}")
        return False

def test_documentation():
    """测试文档"""
    print("\n📚 测试文档...")
    
    try:
        # 检查配置指南
        guide_file = project_root / "docs" / "MODEL_CONFIGURATION_GUIDE.md"
        if guide_file.exists():
            print("✅ 模型配置指南存在")
            
            with open(guide_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if len(content) > 1000:
                    print(f"✅ 配置指南内容丰富 ({len(content)} 字符)")
                else:
                    print("⚠️  配置指南内容较少")
        else:
            print("❌ 模型配置指南不存在")
            return False
        
        # 检查配置助手
        assistant_file = project_root / "scripts" / "model_config_assistant.py"
        if assistant_file.exists():
            print("✅ 配置助手脚本存在")
        else:
            print("❌ 配置助手脚本不存在")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ 文档测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🧪 TradingAgents 模型配置功能测试")
    print("=" * 50)
    
    tests = [
        ("模型推荐配置", test_model_recommendations),
        ("Web应用集成", test_web_app_integration),
        ("CLI集成", test_cli_integration),
        ("文档完整性", test_documentation),
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
        print("\n🎉 所有模型配置功能测试通过！")
        print("\n📋 可用功能:")
        print("1. 智能模型推荐: python scripts/model_config_assistant.py")
        print("2. Web界面配置: python scripts/start_web_app.py")
        print("3. 配置验证: python scripts/validate_model_config.py")
        print("4. 查看指南: docs/MODEL_CONFIGURATION_GUIDE.md")
        return 0
    else:
        print("\n⚠️  部分功能需要进一步完善")
        return 1

if __name__ == "__main__":
    sys.exit(main())
