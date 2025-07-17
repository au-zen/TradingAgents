#!/usr/bin/env python3
"""
TradingAgents 模型配置助手
交互式帮助用户选择最适合的模型配置
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    import questionary
except ImportError:
    print("请先安装 questionary: pip install questionary")
    sys.exit(1)

from tradingagents.config.model_recommendations import model_recommendations
from tradingagents.config.model_capabilities import validate_model_config
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def welcome():
    """欢迎界面"""
    console.print(Panel.fit(
        "[bold blue]🤖 TradingAgents 模型配置助手[/bold blue]\n"
        "[green]帮助您选择最适合的模型配置[/green]",
        border_style="blue"
    ))

def get_user_requirements():
    """获取用户需求"""
    console.print("\n[bold yellow]📋 请回答几个问题，帮助我们为您推荐最佳配置[/bold yellow]")
    
    # 使用场景
    use_case = questionary.select(
        "您的主要使用场景是什么？",
        choices=[
            "个人投资 - 个人股票分析和投资决策",
            "专业分析 - 专业投资分析和研究",
            "企业部署 - 企业内部使用",
            "开发测试 - 开发和测试用途",
            "教学演示 - 教学和演示用途",
            "数据隐私 - 对数据隐私有严格要求",
            "高频交易 - 需要高速响应",
            "成本敏感 - 希望控制成本"
        ]
    ).ask()
    
    if not use_case:
        return None
    
    use_case_key = use_case.split(" - ")[0]
    
    # 预算范围
    budget = questionary.select(
        "您的预算范围是？",
        choices=[
            "免费 - 只使用免费服务",
            "低预算 - 每月 < $10",
            "中预算 - 每月 $10-50",
            "高预算 - 每月 > $50"
        ]
    ).ask()
    
    if not budget:
        return None
    
    budget_key = budget.split(" - ")[0]
    
    # 技术水平
    tech_level = questionary.select(
        "您的技术水平如何？",
        choices=[
            "新手 - 刚开始使用",
            "中级 - 有一定经验",
            "高级 - 技术专家"
        ]
    ).ask()
    
    if not tech_level:
        return None
    
    tech_level_key = tech_level.split(" - ")[0]
    
    # 特殊需求
    special_needs = questionary.checkbox(
        "您有以下特殊需求吗？（可多选）",
        choices=[
            "数据隐私保护",
            "离线使用",
            "高速响应",
            "高质量分析",
            "多语言支持",
            "企业级稳定性"
        ]
    ).ask()
    
    return {
        "use_case": use_case_key,
        "budget": budget_key,
        "tech_level": tech_level_key,
        "special_needs": special_needs or []
    }

def get_recommendations(requirements):
    """根据需求获取推荐"""
    if not requirements:
        return []
    
    # 根据使用场景获取推荐
    scenario_configs = model_recommendations.get_recommendation_by_use_case(requirements["use_case"])
    
    # 根据预算获取推荐
    budget_configs = model_recommendations.get_recommendation_by_budget(requirements["budget"])
    
    # 取交集
    recommended_keys = list(set(scenario_configs) & set(budget_configs))
    
    # 如果没有交集，使用场景推荐
    if not recommended_keys:
        recommended_keys = scenario_configs
    
    # 根据技术水平和特殊需求调整推荐
    if requirements["tech_level"] == "新手":
        # 新手优先推荐简单配置
        priority_order = ["high_speed_free", "balanced_recommended", "professional"]
    elif "数据隐私保护" in requirements["special_needs"] or "离线使用" in requirements["special_needs"]:
        # 隐私需求优先推荐本地部署
        priority_order = ["local_deployment", "high_speed_free", "balanced_recommended"]
    elif "高速响应" in requirements["special_needs"]:
        # 高速需求优先推荐Groq
        priority_order = ["high_speed_free", "local_deployment", "balanced_recommended"]
    else:
        priority_order = recommended_keys
    
    # 按优先级排序
    sorted_keys = []
    for key in priority_order:
        if key in recommended_keys:
            sorted_keys.append(key)
    
    # 添加其他推荐
    for key in recommended_keys:
        if key not in sorted_keys:
            sorted_keys.append(key)
    
    return sorted_keys[:3]  # 最多返回3个推荐

def display_recommendations(recommended_keys, requirements):
    """显示推荐配置"""
    if not recommended_keys:
        console.print("[red]❌ 没有找到合适的配置推荐[/red]")
        return
    
    console.print(f"\n[bold green]🎯 根据您的需求，我们为您推荐以下配置：[/bold green]")
    
    for i, config_key in enumerate(recommended_keys, 1):
        config = model_recommendations.get_recommendation(config_key)
        if not config:
            continue
        
        # 创建配置表格
        table = Table(title=f"{i}. {config['name']}", show_header=True, header_style="bold magenta")
        table.add_column("属性", style="cyan", width=15)
        table.add_column("值", style="white", width=40)
        
        table.add_row("提供商", config['provider'])
        table.add_row("深度思考模型", config['deep_think_llm'])
        table.add_row("快速思考模型", config['quick_think_llm'])
        table.add_row("成本", config['cost'])
        table.add_row("设置难度", config['setup_difficulty'])
        table.add_row("描述", config['description'])
        
        console.print(table)
        
        # 显示优缺点
        console.print(f"[green]✅ 优点:[/green]")
        for pro in config['pros']:
            console.print(f"  • {pro}")
        
        console.print(f"[yellow]⚠️  缺点:[/yellow]")
        for con in config['cons']:
            console.print(f"  • {con}")
        
        # 匹配度分析
        match_reasons = []
        if requirements["use_case"] in ["个人投资", "开发测试"] and config_key in ["high_speed_free", "balanced_recommended"]:
            match_reasons.append("适合个人使用")
        if requirements["budget"] == "免费" and config['cost'].startswith("免费"):
            match_reasons.append("符合免费预算")
        if "数据隐私保护" in requirements["special_needs"] and config_key == "local_deployment":
            match_reasons.append("满足数据隐私需求")
        if "高速响应" in requirements["special_needs"] and config_key == "high_speed_free":
            match_reasons.append("提供高速响应")
        
        if match_reasons:
            console.print(f"[blue]🎯 推荐理由: {', '.join(match_reasons)}[/blue]")
        
        console.print()

def setup_configuration():
    """配置设置"""
    console.print("[bold yellow]🔧 选择要设置的配置[/bold yellow]")
    
    all_configs = model_recommendations.get_all_recommendations()
    config_choices = [f"{config['name']}" for config in all_configs.values()]
    
    selected = questionary.select(
        "请选择要设置的配置：",
        choices=config_choices + ["返回主菜单"]
    ).ask()
    
    if not selected or selected == "返回主菜单":
        return
    
    # 找到对应的配置key
    selected_key = None
    for key, config in all_configs.items():
        if config['name'] == selected:
            selected_key = key
            break
    
    if not selected_key:
        console.print("[red]❌ 配置不存在[/red]")
        return
    
    # 生成配置命令
    setup_commands = model_recommendations.generate_setup_commands(selected_key)
    
    console.print(Panel(
        setup_commands,
        title=f"[bold green]{selected} 配置命令[/bold green]",
        border_style="green"
    ))
    
    # 询问是否保存到文件
    save_to_file = questionary.confirm("是否将配置命令保存到文件？").ask()
    
    if save_to_file:
        filename = f"setup_{selected_key}.sh"
        with open(filename, 'w') as f:
            f.write("#!/bin/bash\n")
            f.write(f"# {selected} 配置脚本\n")
            f.write(f"# 生成时间: {os.popen('date').read().strip()}\n\n")
            f.write(setup_commands)
        
        os.chmod(filename, 0o755)
        console.print(f"[green]✅ 配置命令已保存到 {filename}[/green]")
        console.print(f"[blue]💡 运行命令: ./{filename}[/blue]")

def validate_current_config():
    """验证当前配置"""
    console.print("[bold yellow]🔍 验证当前配置[/bold yellow]")
    
    try:
        from tradingagents.default_config import DEFAULT_CONFIG
        
        provider = DEFAULT_CONFIG.get("llm_provider", "未设置")
        deep_think = DEFAULT_CONFIG.get("deep_think_llm", "未设置")
        quick_think = DEFAULT_CONFIG.get("quick_think_llm", "未设置")

        # 提取提供商名称（去除描述文字）
        provider_name = provider.lower().split()[0] if provider and provider != "未设置" else ""

        console.print(f"当前配置:")
        console.print(f"  提供商: {provider}")
        if provider_name:
            console.print(f"  提取的提供商名称: {provider_name}")
        console.print(f"  深度思考模型: {deep_think}")
        console.print(f"  快速思考模型: {quick_think}")

        if provider != "未设置" and deep_think != "未设置" and quick_think != "未设置":
            result = validate_model_config(provider_name, deep_think, quick_think)
            
            if result["valid"]:
                console.print("[green]✅ 配置验证通过[/green]")
            else:
                console.print("[red]❌ 配置验证失败[/red]")
                for warning in result["warnings"]:
                    console.print(f"  ⚠️  {warning}")
        else:
            console.print("[yellow]⚠️  配置不完整[/yellow]")
    
    except Exception as e:
        console.print(f"[red]❌ 验证失败: {e}[/red]")

def main():
    """主函数"""
    welcome()
    
    while True:
        action = questionary.select(
            "请选择操作：",
            choices=[
                "🎯 智能推荐配置",
                "🔧 手动设置配置", 
                "🔍 验证当前配置",
                "📚 查看配置指南",
                "❌ 退出"
            ]
        ).ask()
        
        if not action or action == "❌ 退出":
            console.print("[blue]👋 感谢使用 TradingAgents 模型配置助手！[/blue]")
            break
        
        elif action == "🎯 智能推荐配置":
            requirements = get_user_requirements()
            if requirements:
                recommended_keys = get_recommendations(requirements)
                display_recommendations(recommended_keys, requirements)
        
        elif action == "🔧 手动设置配置":
            setup_configuration()
        
        elif action == "🔍 验证当前配置":
            validate_current_config()
        
        elif action == "📚 查看配置指南":
            guide_path = project_root / "docs" / "MODEL_CONFIGURATION_GUIDE.md"
            if guide_path.exists():
                console.print(f"[blue]📚 配置指南位置: {guide_path}[/blue]")
                console.print("[blue]💡 建议使用文本编辑器或浏览器打开查看[/blue]")
            else:
                console.print("[red]❌ 配置指南文件不存在[/red]")
        
        console.print()

if __name__ == "__main__":
    main()
