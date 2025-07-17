#!/usr/bin/env python3
"""
配置验证脚本
验证TradingAgents的环境变量配置是否正确
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tradingagents.default_config import DEFAULT_CONFIG

console = Console()

def check_env_file():
    """检查.env文件是否存在"""
    env_file = project_root / ".env"
    env_example = project_root / ".env.example"
    
    if env_file.exists():
        console.print("✅ .env 文件存在", style="green")
        load_dotenv(env_file)
        return True
    elif env_example.exists():
        console.print("⚠️  .env 文件不存在，但找到 .env.example", style="yellow")
        console.print("请复制 .env.example 为 .env 并填入您的API密钥", style="yellow")
        return False
    else:
        console.print("❌ .env 和 .env.example 文件都不存在", style="red")
        return False

def validate_api_keys():
    """验证API密钥配置"""
    api_configs = [
        ("OpenRouter API Key", "OPENROUTER_API_KEY", "推荐主要使用"),
        ("Groq API Key", "GROQ_API_KEY", "高速推理备用"),
        ("Together AI API Key", "TOGETHER_API_KEY", "开源模型丰富"),
        ("Hugging Face API Key", "HUGGINGFACE_API_KEY", "社区模型"),
        ("Google API Key", "GOOGLE_API_KEY", "Gemini模型"),
        ("AKShare Token", "AKSHARE_TOKEN", "A股数据源"),
        ("Finnhub API Key", "FINNHUB_API_KEY", "美股数据源"),
    ]
    
    table = Table(title="API密钥配置状态", box=box.ROUNDED)
    table.add_column("API服务", style="cyan")
    table.add_column("环境变量", style="magenta")
    table.add_column("状态", style="green")
    table.add_column("说明", style="yellow")
    
    configured_count = 0
    
    for name, env_var, description in api_configs:
        value = os.getenv(env_var)
        if value and value != f"your_{env_var.lower()}_here":
            status = "✅ 已配置"
            configured_count += 1
        else:
            status = "❌ 未配置"
        
        table.add_row(name, env_var, status, description)
    
    console.print(table)
    
    if configured_count == 0:
        console.print("\n⚠️  没有配置任何API密钥，系统将无法正常工作", style="red bold")
    elif configured_count < 3:
        console.print(f"\n⚠️  只配置了 {configured_count} 个API密钥，建议至少配置3个以确保稳定性", style="yellow")
    else:
        console.print(f"\n✅ 已配置 {configured_count} 个API密钥，配置良好！", style="green bold")
    
    return configured_count

def validate_ollama_connection():
    """验证Ollama连接"""
    try:
        import requests
        ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        
        response = requests.get(f"{ollama_url}/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            console.print(f"✅ Ollama连接成功，发现 {len(models)} 个模型", style="green")
            
            # 检查推荐模型
            recommended_models = ["qwen3:14b", "qwen3:8b", "nomic-embed-text"]
            available_models = [model["name"] for model in models]
            
            for model in recommended_models:
                if any(model in available for available in available_models):
                    console.print(f"  ✅ {model} 可用", style="green")
                else:
                    console.print(f"  ❌ {model} 不可用，建议运行: ollama pull {model}", style="yellow")
            
            return True
        else:
            console.print(f"❌ Ollama连接失败，状态码: {response.status_code}", style="red")
            return False
    except Exception as e:
        console.print(f"❌ Ollama连接失败: {e}", style="red")
        console.print("请确保Ollama已安装并运行: ollama serve", style="yellow")
        return False

def validate_config_values():
    """验证配置值"""
    config_checks = [
        ("LLM Provider", DEFAULT_CONFIG["llm_provider"], ["openrouter", "groq", "together", "huggingface", "google"]),
        ("Deep Think LLM", DEFAULT_CONFIG["deep_think_llm"], None),
        ("Quick Think LLM", DEFAULT_CONFIG["quick_think_llm"], None),
        ("Embedding Provider", DEFAULT_CONFIG["embedding_provider"], ["ollama", "openai", "huggingface"]),
        ("Embedding Model", DEFAULT_CONFIG["embedding_model"], None),
        ("Online Tools", DEFAULT_CONFIG["online_tools"], [True, False]),
    ]
    
    table = Table(title="配置值验证", box=box.ROUNDED)
    table.add_column("配置项", style="cyan")
    table.add_column("当前值", style="magenta")
    table.add_column("状态", style="green")
    
    for name, value, valid_values in config_checks:
        if valid_values and value not in valid_values:
            status = f"❌ 无效值，应为: {valid_values}"
        else:
            status = "✅ 有效"
        
        table.add_row(name, str(value), status)
    
    console.print(table)

def generate_setup_guide():
    """生成设置指南"""
    guide = """
🚀 快速设置指南:

1. 复制环境变量文件:
   cp .env.example .env

2. 编辑 .env 文件，至少配置以下API密钥:
   - OPENROUTER_API_KEY (推荐，免费额度大)
   - GROQ_API_KEY (备用，速度快)
   - AKSHARE_TOKEN (A股数据，可选)

3. 安装并启动Ollama (本地模型):
   # 安装Ollama
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # 启动服务
   ollama serve
   
   # 下载推荐模型
   ollama pull qwen3:14b
   ollama pull qwen3:8b
   ollama pull nomic-embed-text

4. 验证配置:
   python scripts/validate_config.py

5. 运行测试:
   python -m cli.main --ticker 603127.SH --start-date 2024-01-01 --end-date 2024-01-02 --non-interactive
"""
    
    console.print(Panel(guide, title="设置指南", border_style="blue"))

def main():
    """主函数"""
    console.print(Panel.fit("TradingAgents 配置验证", style="bold blue"))
    
    # 检查.env文件
    env_exists = check_env_file()
    
    if not env_exists:
        generate_setup_guide()
        return
    
    console.print("\n" + "="*60)
    
    # 验证API密钥
    api_count = validate_api_keys()
    
    console.print("\n" + "="*60)
    
    # 验证Ollama连接
    ollama_ok = validate_ollama_connection()
    
    console.print("\n" + "="*60)
    
    # 验证配置值
    validate_config_values()
    
    console.print("\n" + "="*60)
    
    # 总结
    if api_count >= 1 and ollama_ok:
        console.print("\n🎉 配置验证通过！系统可以正常运行。", style="green bold")
    elif api_count >= 1:
        console.print("\n⚠️  API配置正常，但Ollama未连接。建议安装Ollama以获得更好的性能。", style="yellow bold")
    else:
        console.print("\n❌ 配置验证失败！请检查API密钥配置。", style="red bold")
        generate_setup_guide()

if __name__ == "__main__":
    main()
