#!/usr/bin/env python3
"""
检查Groq API当前可用的模型
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

def check_groq_models():
    """检查Groq API可用模型"""
    
    # 从环境变量获取API密钥
    api_key = os.getenv('GROQ_API_KEY')
    
    if not api_key:
        print("❌ 未找到GROQ_API_KEY环境变量")
        print("💡 请在.env文件中设置GROQ_API_KEY")
        return False
    
    print("🔍 检查Groq API可用模型...")
    print(f"🔑 API Key: {api_key[:10]}...{api_key[-4:]}")
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    try:
        # 尝试不同的API端点
        endpoints = [
            'https://api.groq.com/openai/v1/models',
            'https://api.groq.com/v1/models'
        ]

        response = None
        for endpoint in endpoints:
            print(f"🔗 尝试端点: {endpoint}")
            try:
                response = requests.get(endpoint, headers=headers, timeout=10)
                if response.status_code == 200:
                    print(f"✅ 端点可用: {endpoint}")
                    break
                else:
                    print(f"❌ 端点失败: {endpoint} - {response.status_code}")
            except Exception as e:
                print(f"❌ 端点错误: {endpoint} - {e}")

        if response and response.status_code == 200:
            models_data = response.json()
            models = models_data.get('data', [])
            
            print(f"✅ 成功获取模型列表，共 {len(models)} 个模型")
            print("\n📋 可用模型:")
            print("-" * 80)
            
            # 按类型分组显示
            llama_models = []
            mixtral_models = []
            other_models = []
            
            for model in models:
                model_id = model.get('id', '')
                created = model.get('created', 0)
                
                if 'llama' in model_id.lower():
                    llama_models.append((model_id, created))
                elif 'mixtral' in model_id.lower():
                    mixtral_models.append((model_id, created))
                else:
                    other_models.append((model_id, created))
            
            # 显示Llama模型
            if llama_models:
                print("\n🦙 Llama模型:")
                for model_id, created in sorted(llama_models):
                    print(f"  - {model_id}")
            
            # 显示Mixtral模型
            if mixtral_models:
                print("\n🔀 Mixtral模型:")
                for model_id, created in sorted(mixtral_models):
                    print(f"  - {model_id}")
            
            # 显示其他模型
            if other_models:
                print("\n🔧 其他模型:")
                for model_id, created in sorted(other_models):
                    print(f"  - {model_id}")
            
            # 检查配置中的模型是否可用
            print("\n" + "=" * 80)
            print("🔍 检查配置中的模型可用性:")
            
            config_models = [
                "llama3-groq-70b-8192-tool-use-preview",
                "llama3-groq-8b-8192-tool-use-preview", 
                "llama-3.1-70b-versatile",
                "llama-3.1-8b-instant",
                "mixtral-8x7b-32768"
            ]
            
            available_model_ids = [m.get('id', '') for m in models]
            
            for model in config_models:
                if model in available_model_ids:
                    print(f"  ✅ {model} - 可用")
                else:
                    print(f"  ❌ {model} - 不可用")
                    
                    # 寻找相似的模型
                    similar = []
                    for available in available_model_ids:
                        if any(part in available.lower() for part in model.lower().split('-')):
                            similar.append(available)
                    
                    if similar:
                        print(f"     💡 相似模型: {', '.join(similar[:3])}")
            
            return True
            
        else:
            if response:
                print(f"❌ 所有API端点都失败，最后状态码: {response.status_code}")
                print(f"响应: {response.text}")
            else:
                print("❌ 无法连接到任何API端点")
            return False
            
    except Exception as e:
        print(f"❌ 检查模型时出错: {e}")
        return False

def test_model_call():
    """测试模型调用"""
    
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key:
        return False
    
    print("\n🧪 测试模型调用...")
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    # 测试一个简单的调用
    test_models = [
        "llama-3.1-8b-instant",
        "llama3-groq-8b-8192-tool-use-preview",
        "mixtral-8x7b-32768"
    ]
    
    for model in test_models:
        try:
            data = {
                "model": model,
                "messages": [
                    {"role": "user", "content": "Hello, respond with just 'OK'"}
                ],
                "max_tokens": 10,
                "temperature": 0
            }
            
            response = requests.post(
                'https://api.groq.com/openai/v1/chat/completions',
                headers=headers,
                json=data,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result.get('choices', [{}])[0].get('message', {}).get('content', '')
                print(f"  ✅ {model}: {content.strip()}")
                return True
            else:
                print(f"  ❌ {model}: {response.status_code} - {response.text[:100]}")
                
        except Exception as e:
            print(f"  ❌ {model}: {e}")
    
    return False

def main():
    """主函数"""
    print("🔍 Groq API模型检查工具")
    print("=" * 50)
    
    success = check_groq_models()
    
    if success:
        test_model_call()
        
        print("\n" + "=" * 50)
        print("💡 使用建议:")
        print("1. 使用上面显示为'可用'的模型")
        print("2. 如果配置的模型不可用，选择相似的替代模型")
        print("3. 更新cli/utils.py中的模型配置")
        
        return 0
    else:
        print("\n❌ 检查失败")
        print("💡 可能的解决方案:")
        print("1. 检查GROQ_API_KEY是否正确")
        print("2. 检查网络连接")
        print("3. 确认Groq服务状态")
        
        return 1

if __name__ == "__main__":
    sys.exit(main())
