#!/usr/bin/env python3
"""
检查API密钥配置状态
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def check_api_keys():
    """检查API密钥配置"""
    print("🔍 API密钥配置检查")
    print("=" * 50)
    
    # 加载环境变量
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        print("❌ python-dotenv未安装，请运行: pip install python-dotenv")
        return False
    
    # 检查关键API密钥
    api_keys = [
        ("OPENAI_API_KEY", "OpenAI/OpenRouter API密钥"),
        ("OPENROUTER_API_KEY", "OpenRouter API密钥"),
        ("GROQ_API_KEY", "Groq API密钥"),
        ("TOGETHER_API_KEY", "Together AI API密钥"),
    ]
    
    configured_keys = 0
    total_keys = len(api_keys)
    
    for key_name, description in api_keys:
        value = os.getenv(key_name)
        
        if value and not value.startswith("your_") and len(value) > 10:
            print(f"✅ {key_name}: 已配置")
            configured_keys += 1
        else:
            print(f"❌ {key_name}: 未配置或使用占位符")
            print(f"   描述: {description}")
    
    print("\n" + "=" * 50)
    print(f"📊 配置状态: {configured_keys}/{total_keys} 个API密钥已配置")
    
    if configured_keys == 0:
        print("\n⚠️  没有配置任何API密钥！")
        print("请按照以下步骤配置：")
        print("1. 访问 https://openrouter.ai/keys 获取OpenRouter API密钥")
        print("2. 编辑 .env 文件")
        print("3. 将 your_openrouter_api_key_here 替换为真实的API密钥")
        return False
    elif configured_keys < total_keys:
        print("\n⚠️  部分API密钥未配置，某些功能可能不可用")
        return True
    else:
        print("\n🎉 所有API密钥都已配置！")
        return True

def test_openrouter_connection():
    """测试OpenRouter连接"""
    print("\n🧪 测试OpenRouter连接...")
    
    try:
        import requests
        
        # 获取API密钥
        api_key = os.getenv('OPENROUTER_API_KEY') or os.getenv('OPENAI_API_KEY')
        
        if not api_key or api_key.startswith("your_"):
            print("❌ OpenRouter API密钥未配置")
            return False
        
        # 测试API连接
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        # 简单的模型列表请求
        response = requests.get(
            'https://openrouter.ai/api/v1/models',
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ OpenRouter API连接成功")
            models = response.json().get('data', [])
            print(f"   可用模型数量: {len(models)}")
            return True
        elif response.status_code == 401:
            print("❌ OpenRouter API密钥无效 (401 Unauthorized)")
            print("   请检查API密钥是否正确")
            return False
        else:
            print(f"❌ OpenRouter API连接失败 (状态码: {response.status_code})")
            return False
            
    except Exception as e:
        print(f"❌ 连接测试失败: {e}")
        return False

def main():
    """主函数"""
    print("🔧 TradingAgents API密钥诊断工具")
    print("=" * 60)
    
    # 检查API密钥配置
    keys_ok = check_api_keys()
    
    if keys_ok:
        # 测试OpenRouter连接
        connection_ok = test_openrouter_connection()
        
        if connection_ok:
            print("\n🎉 配置检查完成！")
            print("现在可以正常使用TradingAgents了。")
            return 0
        else:
            print("\n⚠️  API密钥配置有问题，请检查并更新。")
            return 1
    else:
        print("\n❌ 请先配置API密钥再使用TradingAgents。")
        return 1

if __name__ == "__main__":
    sys.exit(main())
