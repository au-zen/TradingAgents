#!/usr/bin/env python3
"""
模型配置助手脚本
帮助用户选择和配置最适合的LLM模型
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv, set_key
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich import box

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tradingagents.default_config import DEFAULT_CONFIG

console = Console()

def display_model_options():
    """显示所有可用的模型选项"""
    
    console.print(Panel.fit("🤖 可用模型配置选项", style="bold blue"))
    
    model_options = DEFAULT_CONFIG["model_options"]
    
    for provider, config in model_options.items():
        console.print(f"\n📡 **{provider.upper()}**")
        
        if "free_models" in config:
            table = Table(title=f"{provider} 免费模型", box=box.ROUNDED)
            table.add_column("模型名称", style="cyan")
            table.add_column("推荐用途", style="green")
            
            for model in config["free_models"]:
                if model == config["recommended"]["deep_think"]:
                    usage = "深度思考 (推荐)"
                elif model == config["recommended"]["quick_think"]:
                    usage = "快速响应 (推荐)"
                else:
                    usage = "通用"
                table.add_row(model, usage)
            
            console.print(table)
        
        elif "recommended_models" in config:
            table = Table(title=f"{provider} 推荐模型", box=box.ROUNDED)
            table.add_column("模型名称", style="cyan")
            table.add_column("推荐用途", style="green")
            
            for model in config["recommended_models"]:
                if model == config["recommended"]["deep_think"]:
                    usage = "深度思考 (推荐)"
                elif model == config["recommended"]["quick_think"]:
                    usage = "快速响应 (推荐)"
                else:
                    usage = "通用"
                table.add_row(model, usage)
            
            console.print(table)

def configure_provider():
    """配置LLM提供商"""
    
    console.print("\n🔧 配置LLM提供商")
    
    providers = list(DEFAULT_CONFIG["model_options"].keys())
    
    console.print("可用的提供商:")
    for i, provider in enumerate(providers, 1):
        console.print(f"  {i}. {provider}")
    
    while True:
        choice = Prompt.ask("请选择提供商 (输入数字)", default="1")
        try:
            provider_index = int(choice) - 1
            if 0 <= provider_index < len(providers):
                selected_provider = providers[provider_index]
                break
            else:
                console.print("❌ 无效选择，请重试", style="red")
        except ValueError:
            console.print("❌ 请输入有效数字", style="red")
    
    return selected_provider

def configure_models(provider):
    """配置具体模型"""
    
    console.print(f"\n🎯 配置 {provider.upper()} 模型")
    
    model_config = DEFAULT_CONFIG["model_options"][provider]
    
    # 获取推荐配置
    recommended = model_config["recommended"]
    
    console.print(f"推荐配置:")
    console.print(f"  深度思考模型: {recommended['deep_think']}")
    console.print(f"  快速响应模型: {recommended['quick_think']}")
    
    use_recommended = Confirm.ask("使用推荐配置?", default=True)
    
    if use_recommended:
        return recommended["deep_think"], recommended["quick_think"]
    else:
        # 手动选择模型
        available_models = model_config.get("free_models", model_config.get("recommended_models", []))
        
        console.print("可用模型:")
        for i, model in enumerate(available_models, 1):
            console.print(f"  {i}. {model}")
        
        # 选择深度思考模型
        while True:
            choice = Prompt.ask("选择深度思考模型 (输入数字)", default="1")
            try:
                model_index = int(choice) - 1
                if 0 <= model_index < len(available_models):
                    deep_think_model = available_models[model_index]
                    break
                else:
                    console.print("❌ 无效选择，请重试", style="red")
            except ValueError:
                console.print("❌ 请输入有效数字", style="red")
        
        # 选择快速响应模型
        while True:
            choice = Prompt.ask("选择快速响应模型 (输入数字)", default="2")
            try:
                model_index = int(choice) - 1
                if 0 <= model_index < len(available_models):
                    quick_think_model = available_models[model_index]
                    break
                else:
                    console.print("❌ 无效选择，请重试", style="red")
            except ValueError:
                console.print("❌ 请输入有效数字", style="red")
        
        return deep_think_model, quick_think_model

def configure_api_key(provider):
    """配置API密钥"""
    
    console.print(f"\n🔑 配置 {provider.upper()} API密钥")
    
    key_mapping = {
        "openrouter": "OPENROUTER_API_KEY",
        "groq": "GROQ_API_KEY", 
        "together": "TOGETHER_API_KEY",
        "huggingface": "HUGGINGFACE_API_KEY",
        "google": "GOOGLE_API_KEY"
    }
    
    if provider not in key_mapping:
        console.print(f"⚠️  {provider} 不需要API密钥配置", style="yellow")
        return
    
    env_var = key_mapping[provider]
    current_key = os.getenv(env_var)
    
    if current_key and current_key != f"your_{env_var.lower()}_here":
        console.print(f"✅ 当前已配置 {env_var}", style="green")
        update_key = Confirm.ask("是否更新API密钥?", default=False)
        if not update_key:
            return
    
    # 获取API密钥获取指南
    key_guides = {
        "openrouter": "https://openrouter.ai/keys",
        "groq": "https://console.groq.com/keys",
        "together": "https://api.together.xyz/settings/api-keys",
        "huggingface": "https://huggingface.co/settings/tokens",
        "google": "https://aistudio.google.com/app/apikey"
    }
    
    console.print(f"获取API密钥: {key_guides[provider]}")
    
    api_key = Prompt.ask(f"请输入 {provider.upper()} API密钥", password=True)
    
    if api_key:
        # 更新.env文件
        env_file = project_root / ".env"
        set_key(str(env_file), env_var, api_key)
        console.print(f"✅ {env_var} 已保存到 .env 文件", style="green")
        
        # 如果是OpenRouter，同时设置OPENAI_API_KEY以保持兼容性
        if provider == "openrouter":
            set_key(str(env_file), "OPENAI_API_KEY", api_key)
            console.print("✅ OPENAI_API_KEY 已同步设置", style="green")

def update_config_file(provider, deep_think_model, quick_think_model):
    """更新配置文件"""
    
    console.print("\n💾 更新配置文件")
    
    env_file = project_root / ".env"
    
    # 更新环境变量
    set_key(str(env_file), "LLM_PROVIDER", provider)
    set_key(str(env_file), "DEEP_THINK_LLM", deep_think_model)
    set_key(str(env_file), "QUICK_THINK_LLM", quick_think_model)
    
    # 设置backend_url
    if provider in DEFAULT_CONFIG["api_endpoints"]:
        backend_url = DEFAULT_CONFIG["api_endpoints"][provider]
        set_key(str(env_file), "BACKEND_URL", backend_url)
    
    console.print("✅ 配置已保存到 .env 文件", style="green")

def test_configuration():
    """测试配置"""
    
    console.print("\n🧪 测试配置")
    
    test_confirm = Confirm.ask("是否运行配置测试?", default=True)
    
    if test_confirm:
        try:
            # 重新加载环境变量
            load_dotenv(override=True)
            
            # 运行验证脚本
            import subprocess
            result = subprocess.run([
                sys.executable, "scripts/validate_config.py"
            ], cwd=project_root, capture_output=True, text=True)
            
            if result.returncode == 0:
                console.print("✅ 配置测试通过!", style="green bold")
            else:
                console.print("❌ 配置测试失败", style="red")
                console.print(result.stdout)
                console.print(result.stderr)
                
        except Exception as e:
            console.print(f"❌ 测试过程中出错: {e}", style="red")

def main():
    """主函数"""
    
    console.print(Panel.fit("🚀 TradingAgents 模型配置助手", style="bold blue"))
    
    # 检查.env文件
    env_file = project_root / ".env"
    if not env_file.exists():
        console.print("⚠️  .env 文件不存在，将从 .env.example 创建", style="yellow")
        env_example = project_root / ".env.example"
        if env_example.exists():
            import shutil
            shutil.copy(env_example, env_file)
            console.print("✅ .env 文件已创建", style="green")
        else:
            console.print("❌ .env.example 文件不存在", style="red")
            return
    
    # 加载环境变量
    load_dotenv(env_file)
    
    # 显示模型选项
    display_model_options()
    
    # 配置提供商
    provider = configure_provider()
    
    # 配置模型
    deep_think_model, quick_think_model = configure_models(provider)
    
    # 配置API密钥
    configure_api_key(provider)
    
    # 更新配置文件
    update_config_file(provider, deep_think_model, quick_think_model)
    
    # 显示最终配置
    console.print("\n🎉 配置完成!")
    
    final_config = Table(title="最终配置", box=box.ROUNDED)
    final_config.add_column("配置项", style="cyan")
    final_config.add_column("值", style="green")
    
    final_config.add_row("LLM提供商", provider)
    final_config.add_row("深度思考模型", deep_think_model)
    final_config.add_row("快速响应模型", quick_think_model)
    
    console.print(final_config)
    
    # 测试配置
    test_configuration()
    
    console.print("\n🚀 现在可以运行 TradingAgents 了!")
    console.print("python -m cli.main --ticker 603127.SH --start-date 2024-01-01 --end-date 2024-01-02 --non-interactive")

if __name__ == "__main__":
    main()
