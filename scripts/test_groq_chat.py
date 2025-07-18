#!/usr/bin/env python3
"""
测试Groq API聊天功能
"""

import os
import sys
import requests
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

def test_groq_chat():
    """测试Groq聊天API"""
    
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key:
        print("❌ 未找到GROQ_API_KEY环境变量")
        return False
    
    print("🧪 测试Groq聊天API...")
    print(f"🔑 API Key: {api_key[:10]}...{api_key[-4:]}")
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    # 测试不同的模型
    test_models = [
        "llama-3.1-8b-instant",
        "llama-3.1-70b-versatile", 
        "llama3-groq-8b-8192-tool-use-preview",
        "llama3-groq-70b-8192-tool-use-preview",
        "mixtral-8x7b-32768",
        "gemma2-9b-it",
        "llama3-8b-8192",
        "llama3-70b-8192"
    ]
    
    successful_models = []
    failed_models = []
    
    for model in test_models:
        print(f"\n🔍 测试模型: {model}")
        
        data = {
            "model": model,
            "messages": [
                {"role": "user", "content": "Hello! Please respond with just 'OK' to confirm you're working."}
            ],
            "max_tokens": 10,
            "temperature": 0
        }
        
        try:
            response = requests.post(
                'https://api.groq.com/openai/v1/chat/completions',
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
                if response.status_code == 400:
                    error_info = response.json().get('error', {})
                    print(f"     错误: {error_info.get('message', 'Unknown error')}")
                failed_models.append((model, response.status_code, response.text[:100]))
                
        except Exception as e:
            print(f"  ❌ 异常: {e}")
            failed_models.append((model, "Exception", str(e)))
    
    # 总结结果
    print("\n" + "=" * 60)
    print("📊 测试结果总结")
    print("=" * 60)
    
    if successful_models:
        print(f"\n✅ 可用模型 ({len(successful_models)}个):")
        for model in successful_models:
            print(f"  - {model}")
    
    if failed_models:
        print(f"\n❌ 不可用模型 ({len(failed_models)}个):")
        for model, status, error in failed_models:
            print(f"  - {model}: {status}")
            if "not found" in str(error).lower() or "does not exist" in str(error).lower():
                print(f"    💡 模型可能已被弃用或重命名")
    
    # 提供修复建议
    if successful_models:
        print(f"\n💡 修复建议:")
        print(f"1. 更新cli/utils.py中的Groq模型配置")
        print(f"2. 使用以下可用模型:")
        
        # 推荐配置
        quick_models = [m for m in successful_models if '8b' in m or 'instant' in m]
        deep_models = [m for m in successful_models if '70b' in m or 'versatile' in m]
        
        if quick_models:
            print(f"   快速思考模型: {quick_models[0]}")
        if deep_models:
            print(f"   深度思考模型: {deep_models[0]}")
    
    return len(successful_models) > 0

def main():
    """主函数"""
    print("🧪 Groq API聊天测试工具")
    print("=" * 50)
    
    success = test_groq_chat()
    
    if success:
        print("\n🎉 Groq API工作正常！")
        return 0
    else:
        print("\n❌ Groq API测试失败")
        print("💡 可能的原因:")
        print("1. API密钥无效或过期")
        print("2. 网络连接问题")
        print("3. Groq服务暂时不可用")
        print("4. 所有测试的模型都已被弃用")
        return 1

if __name__ == "__main__":
    sys.exit(main())
