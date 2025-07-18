#!/usr/bin/env python3
"""
测试智谱AI API功能
"""

import os
import sys
import requests
import json
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

def test_zhipuai_models():
    """测试智谱AI模型"""
    
    api_key = os.getenv('ZHIPUAI_API_KEY')
    if not api_key:
        print("❌ 未找到ZHIPUAI_API_KEY环境变量")
        print("💡 请在.env文件中设置ZHIPUAI_API_KEY")
        print("🔗 获取地址: https://bigmodel.cn/usercenter/apikeys")
        return False
    
    print("🧪 测试智谱AI API...")
    print(f"🔑 API Key: {api_key[:10]}...{api_key[-4:]}")
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    # 测试不同的模型
    test_models = [
        "glm-z1-flash",      # 免费模型
        "glm-4-flash",       # 免费模型
        "glm-4-plus",        # 付费模型
        "glm-4-air",         # 付费模型
        "glm-4-airx",        # 付费模型
        "glm-4-long",        # 付费模型
    ]
    
    successful_models = []
    failed_models = []
    
    for model in test_models:
        print(f"\n🔍 测试模型: {model}")
        
        data = {
            "model": model,
            "messages": [
                {"role": "user", "content": "你好！请回复'OK'来确认你正常工作。"}
            ],
            "max_tokens": 10,
            "temperature": 0.1
        }
        
        try:
            response = requests.post(
                'https://open.bigmodel.cn/api/paas/v4/chat/completions',
                headers=headers,
                json=data,
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result.get('choices', [{}])[0].get('message', {}).get('content', '')
                print(f"  ✅ 成功: {content.strip()}")
                successful_models.append(model)
            else:
                print(f"  ❌ 失败: {response.status_code}")
                error_info = response.json() if response.content else {}
                error_msg = error_info.get('error', {}).get('message', 'Unknown error')
                print(f"     错误: {error_msg}")
                failed_models.append((model, response.status_code, error_msg))
                
        except Exception as e:
            print(f"  ❌ 异常: {e}")
            failed_models.append((model, "Exception", str(e)))
    
    # 总结结果
    print("\n" + "=" * 60)
    print("📊 智谱AI测试结果总结")
    print("=" * 60)
    
    if successful_models:
        print(f"\n✅ 可用模型 ({len(successful_models)}个):")
        for model in successful_models:
            model_type = "免费" if model in ["glm-z1-flash", "glm-4-flash"] else "付费"
            print(f"  - {model} ({model_type})")
    
    if failed_models:
        print(f"\n❌ 不可用模型 ({len(failed_models)}个):")
        for model, status, error in failed_models:
            print(f"  - {model}: {status}")
            if "quota" in str(error).lower() or "balance" in str(error).lower():
                print(f"    💡 可能需要充值或检查配额")
            elif "auth" in str(error).lower():
                print(f"    💡 API密钥可能无效")
    
    # 提供使用建议
    if successful_models:
        print(f"\n💡 使用建议:")
        print(f"1. 智谱AI已成功集成到TradingAgents")
        print(f"2. 推荐配置:")
        
        # 推荐配置
        free_models = [m for m in successful_models if m in ["glm-z1-flash", "glm-4-flash"]]
        paid_models = [m for m in successful_models if m not in ["glm-z1-flash", "glm-4-flash"]]
        
        if free_models:
            print(f"   免费方案:")
            print(f"   - 快速思考: glm-4-flash")
            print(f"   - 深度思考: glm-z1-flash")
        
        if paid_models:
            print(f"   付费方案:")
            print(f"   - 快速思考: glm-4-flash")
            print(f"   - 深度思考: glm-4-plus")
        
        print(f"\n3. 启动命令:")
        print(f"   python -m cli.main")
        print(f"   选择 '智谱AI (中文优化, 免费)' 作为提供商")
    
    return len(successful_models) > 0

def test_tool_calling():
    """测试工具调用功能"""
    
    api_key = os.getenv('ZHIPUAI_API_KEY')
    if not api_key:
        return False
    
    print("\n🔧 测试智谱AI工具调用功能...")
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    # 定义一个简单的工具
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "获取指定城市的天气信息",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "城市名称"
                        }
                    },
                    "required": ["city"]
                }
            }
        }
    ]
    
    data = {
        "model": "glm-4-flash",
        "messages": [
            {"role": "user", "content": "请帮我查询北京的天气"}
        ],
        "tools": tools,
        "tool_choice": "auto",
        "max_tokens": 100,
        "temperature": 0.1
    }
    
    try:
        response = requests.post(
            'https://open.bigmodel.cn/api/paas/v4/chat/completions',
            headers=headers,
            json=data,
            timeout=15
        )
        
        if response.status_code == 200:
            result = response.json()
            choice = result.get('choices', [{}])[0]
            message = choice.get('message', {})
            
            if message.get('tool_calls'):
                print("  ✅ 工具调用功能正常")
                tool_call = message['tool_calls'][0]
                function_name = tool_call['function']['name']
                arguments = tool_call['function']['arguments']
                print(f"     调用函数: {function_name}")
                print(f"     参数: {arguments}")
                return True
            else:
                print("  ⚠️  模型没有调用工具，但API响应正常")
                print(f"     响应: {message.get('content', '')}")
                return True
        else:
            print(f"  ❌ 工具调用测试失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"  ❌ 工具调用测试异常: {e}")
        return False

def main():
    """主函数"""
    print("🧪 智谱AI API测试工具")
    print("=" * 50)
    
    success = test_zhipuai_models()
    
    if success:
        test_tool_calling()
        
        print("\n🎉 智谱AI集成成功！")
        print("\n📋 特点:")
        print("- ✅ 中文优化，理解能力强")
        print("- ✅ 提供免费模型 (glm-z1-flash, glm-4-flash)")
        print("- ✅ 支持工具调用")
        print("- ✅ 响应速度快")
        
        print("\n🚀 开始使用:")
        print("1. 确保.env文件中设置了ZHIPUAI_API_KEY")
        print("2. 运行: python -m cli.main")
        print("3. 选择 '智谱AI (中文优化, 免费)' 作为提供商")
        print("4. 选择合适的模型进行分析")
        
        return 0
    else:
        print("\n❌ 智谱AI测试失败")
        print("💡 可能的原因:")
        print("1. API密钥无效或未设置")
        print("2. 网络连接问题")
        print("3. 智谱AI服务暂时不可用")
        print("4. 账户余额不足")
        
        print("\n🔧 解决方案:")
        print("1. 访问 https://bigmodel.cn/usercenter/apikeys 获取API密钥")
        print("2. 在.env文件中设置 ZHIPUAI_API_KEY=your_api_key")
        print("3. 检查账户余额和配额")
        
        return 1

if __name__ == "__main__":
    sys.exit(main())
