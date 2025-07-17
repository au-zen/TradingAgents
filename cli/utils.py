import questionary
from typing import List, Optional, Tuple, Dict

from cli.models import AnalystType

ANALYST_ORDER = [
    ("Market Analyst", AnalystType.MARKET),
    ("Social Media Analyst", AnalystType.SOCIAL),
    ("News Analyst", AnalystType.NEWS),
    ("Fundamentals Analyst", AnalystType.FUNDAMENTALS),
]


def get_ticker() -> str:
    """Prompt the user to enter a ticker symbol."""
    ticker = questionary.text(
        "Enter the ticker symbol to analyze:",
        validate=lambda x: len(x.strip()) > 0 or "Please enter a valid ticker symbol.",
        style=questionary.Style(
            [
                ("text", "fg:green"),
                ("highlighted", "noinherit"),
            ]
        ),
    ).ask()

    if not ticker:
        console.print("\n[red]No ticker symbol provided. Exiting...[/red]")
        exit(1)

    return ticker.strip().upper()


def get_analysis_date() -> str:
    """Prompt the user to enter a date in YYYY-MM-DD format."""
    import re
    from datetime import datetime

    def validate_date(date_str: str) -> bool:
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):
            return False
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    date = questionary.text(
        "Enter the analysis date (YYYY-MM-DD):",
        validate=lambda x: validate_date(x.strip())
        or "Please enter a valid date in YYYY-MM-DD format.",
        style=questionary.Style(
            [
                ("text", "fg:green"),
                ("highlighted", "noinherit"),
            ]
        ),
    ).ask()

    if not date:
        console.print("\n[red]No date provided. Exiting...[/red]")
        exit(1)

    return date.strip()


def select_analysts() -> List[AnalystType]:
    """Select analysts using an interactive checkbox."""
    choices = questionary.checkbox(
        "Select Your [Analysts Team]:",
        choices=[
            questionary.Choice(display, value=value) for display, value in ANALYST_ORDER
        ],
        instruction="\n- Press Space to select/unselect analysts\n- Press 'a' to select/unselect all\n- Press Enter when done",
        validate=lambda x: len(x) > 0 or "You must select at least one analyst.",
        style=questionary.Style(
            [
                ("checkbox-selected", "fg:green"),
                ("selected", "fg:green noinherit"),
                ("highlighted", "noinherit"),
                ("pointer", "noinherit"),
            ]
        ),
    ).ask()

    if not choices:
        console.print("\n[red]No analysts selected. Exiting...[/red]")
        exit(1)

    return choices


def select_research_depth() -> int:
    """Select research depth using an interactive selection."""

    # Define research depth options with their corresponding values
    DEPTH_OPTIONS = [
        ("Shallow - Quick research, few debate and strategy discussion rounds", 1),
        ("Medium - Middle ground, moderate debate rounds and strategy discussion", 3),
        ("Deep - Comprehensive research, in depth debate and strategy discussion", 5),
    ]

    choice = questionary.select(
        "Select Your [Research Depth]:",
        choices=[
            questionary.Choice(display, value=value) for display, value in DEPTH_OPTIONS
        ],
        instruction="\n- Use arrow keys to navigate\n- Press Enter to select",
        style=questionary.Style(
            [
                ("selected", "fg:yellow noinherit"),
                ("highlighted", "fg:yellow noinherit"),
                ("pointer", "fg:yellow noinherit"),
            ]
        ),
    ).ask()

    if choice is None:
        console.print("\n[red]No research depth selected. Exiting...[/red]")
        exit(1)

    return choice


def select_shallow_thinking_agent(provider) -> str:
    """Select shallow thinking llm engine using an interactive selection."""

    # 提取提供商名称（去除描述文字）
    provider_name = provider.lower().split()[0] if provider else ""

    # Define shallow thinking llm engine options with their corresponding model names
    # 标注支持工具调用的模型
    SHALLOW_AGENT_OPTIONS = {
        "openai": [
            ("GPT-4o-mini - Fast and efficient for quick tasks", "gpt-4o-mini"),
            ("GPT-4.1-nano - Ultra-lightweight model for basic operations", "gpt-4.1-nano"),
            ("GPT-4.1-mini - Compact model with good performance", "gpt-4.1-mini"),
            ("GPT-4o - Standard model with solid capabilities", "gpt-4o"),
        ],
        "anthropic": [
            ("Claude Haiku 3.5 - Fast inference and standard capabilities", "claude-3-5-haiku-latest"),
            ("Claude Sonnet 3.5 - Highly capable standard model", "claude-3-5-sonnet-latest"),
            ("Claude Sonnet 3.7 - Exceptional hybrid reasoning and agentic capabilities", "claude-3-7-sonnet-latest"),
            ("Claude Sonnet 4 - High performance and excellent reasoning", "claude-sonnet-4-0"),
        ],
        "google": [
            ("Gemini 2.0 Flash-Lite - Cost efficiency and low latency", "gemini-2.0-flash-lite"),
            ("Gemini 2.0 Flash - Next generation features, speed, and thinking", "gemini-2.0-flash"),
            ("Gemini 2.5 Flash - Adaptive thinking, cost efficiency", "gemini-2.5-flash-preview-05-20"),
        ],
        "openrouter": [
           ("Qwen3-14B (免费, 支持工具调用)", "qwen/qwen3-14b:free"),
           ("DeepSeek R1 Distill Qwen-14B (免费, 支持工具调用)", "deepseek/deepseek-r1-distill-qwen-14b:free"),
           ("Google Gemini Flash 1.5 (免费)", "google/gemini-flash-1.5"),
           ("Qwen2.5-14B Instruct (支持工具调用)", "qwen/qwen2.5-14b-instruct"),
           ("Meta Llama 3.1-8B Instruct (支持工具调用)", "meta-llama/llama-3.1-8b-instruct"),
           ("Mistral 7B Instruct (免费)", "mistralai/mistral-7b-instruct:free"),
        ],
        "groq": [
           ("Llama3 Groq 8B Tool Use (免费, 支持工具调用)", "llama3-groq-8b-8192-tool-use-preview"),
           ("Llama3.1-8B Instant (免费, 支持工具调用)", "llama-3.1-8b-instant"),
           ("Mixtral 8x7B (免费, 支持工具调用)", "mixtral-8x7b-32768"),
        ],
        "together": [
           ("Qwen2.5-7B Instruct (免费, 支持工具调用)", "Qwen/Qwen2.5-7B-Instruct"),
           ("Meta Llama 3-8B Chat (免费, 支持工具调用)", "meta-llama/Llama-3-8b-chat-hf"),
        ],
        "ollama": [
            ("qwen3:latest (local, 8B, multilingual, fast)", "qwen3:latest"),
            ("llama3.2:latest (local, 3.2B, compact)", "llama3.2:latest"),
            ("llama3.1:latest (local, 8B, general)", "llama3.1:latest"),
            ("mistral:latest (local, 7B, efficient)", "mistral:latest"),
            ("llama2:latest (local, 7B, legacy)", "llama2:latest"),
        ]
    }

    choice = questionary.select(
        "Select Your [Quick-Thinking LLM Engine]:",
        choices=[
            questionary.Choice(display, value=value)
            for display, value in SHALLOW_AGENT_OPTIONS.get(provider_name, [])
        ] if SHALLOW_AGENT_OPTIONS.get(provider_name) else [
            questionary.Choice("No models available for this provider", value="")
        ],
        instruction="\n- Use arrow keys to navigate\n- Press Enter to select",
        style=questionary.Style(
            [
                ("selected", "fg:magenta noinherit"),
                ("highlighted", "fg:magenta noinherit"),
                ("pointer", "fg:magenta noinherit"),
            ]
        ),
    ).ask()

    if choice is None:
        console.print(
            "\n[red]No shallow thinking llm engine selected. Exiting...[/red]"
        )
        exit(1)

    return choice


def select_deep_thinking_agent(provider) -> str:
    """Select deep thinking llm engine using an interactive selection."""

    # 提取提供商名称（去除描述文字）
    provider_name = provider.lower().split()[0] if provider else ""

    # Define deep thinking llm engine options with their corresponding model names
    DEEP_AGENT_OPTIONS = {
        "openai": [
            ("GPT-4.1-nano - Ultra-lightweight model for basic operations", "gpt-4.1-nano"),
            ("GPT-4.1-mini - Compact model with good performance", "gpt-4.1-mini"),
            ("GPT-4o - Standard model with solid capabilities", "gpt-4o"),
            ("o4-mini - Specialized reasoning model (compact)", "o4-mini"),
            ("o3-mini - Advanced reasoning model (lightweight)", "o3-mini"),
            ("o3 - Full advanced reasoning model", "o3"),
            ("o1 - Premier reasoning and problem-solving model", "o1"),
        ],
        "anthropic": [
            ("Claude Haiku 3.5 - Fast inference and standard capabilities", "claude-3-5-haiku-latest"),
            ("Claude Sonnet 3.5 - Highly capable standard model", "claude-3-5-sonnet-latest"),
            ("Claude Sonnet 3.7 - Exceptional hybrid reasoning and agentic capabilities", "claude-3-7-sonnet-latest"),
            ("Claude Sonnet 4 - High performance and excellent reasoning", "claude-sonnet-4-0"),
            ("Claude Opus 4 - Most powerful Anthropic model", "\tclaude-opus-4-0"),
        ],
        "google": [
            ("Gemini 2.0 Flash-Lite - Cost efficiency and low latency", "gemini-2.0-flash-lite"),
            ("Gemini 2.0 Flash - Next generation features, speed, and thinking", "gemini-2.0-flash"),
            ("Gemini 2.5 Flash - Adaptive thinking, cost efficiency", "gemini-2.5-flash-preview-05-20"),
            ("Gemini 2.5 Pro", "gemini-2.5-pro-preview-06-05"),
        ],
        "openrouter": [
            ("Qwen3-30B-A3B (免费, 支持工具调用)", "qwen/qwen3-30b-a3b:free"),
            ("DeepSeek R1 Distill Qwen-14B (免费, 支持工具调用)", "deepseek/deepseek-r1-distill-qwen-14b:free"),
            ("Qwen2.5-72B Instruct (支持工具调用)", "qwen/qwen2.5-72b-instruct"),
            ("Claude 3.5 Sonnet (支持工具调用)", "anthropic/claude-3.5-sonnet"),
            ("Meta Llama 3.1-70B Instruct (支持工具调用)", "meta-llama/llama-3.1-70b-instruct"),
            ("Google Gemini Flash 1.5 (免费)", "google/gemini-flash-1.5"),
        ],
        "groq": [
            ("Llama3 Groq 70B Tool Use (免费, 支持工具调用)", "llama3-groq-70b-8192-tool-use-preview"),
            ("Llama3.1-70B Versatile (免费, 支持工具调用)", "llama-3.1-70b-versatile"),
            ("Mixtral 8x7B (免费, 支持工具调用)", "mixtral-8x7b-32768"),
        ],
        "together": [
            ("Qwen2-72B Instruct (免费, 支持工具调用)", "Qwen/Qwen2-72B-Instruct"),
            ("Meta Llama 3-70B Chat (免费, 支持工具调用)", "meta-llama/Llama-3-70b-chat-hf"),
            ("Mixtral 8x7B Instruct (支持工具调用)", "mistralai/Mixtral-8x7B-Instruct-v0.1"),
        ],
        "ollama": [
            ("qwen3:latest (local, 8B, multilingual, deep)", "qwen3:latest"),
            ("llama3.1:latest (local, 8B, general)", "llama3.1:latest"),
            ("llama3.2:latest (local, 3.2B, compact)", "llama3.2:latest"),
            ("mistral:latest (local, 7B, efficient)", "mistral:latest"),
            ("deepseek-coder-v2:latest (local, 15.7B, code)", "deepseek-coder-v2:latest"),
        ]
    }
    
    choice = questionary.select(
        "Select Your [Deep-Thinking LLM Engine]:",
        choices=[
            questionary.Choice(display, value=value)
            for display, value in DEEP_AGENT_OPTIONS.get(provider_name, [])
        ] if DEEP_AGENT_OPTIONS.get(provider_name) else [
            questionary.Choice("No models available for this provider", value="")
        ],
        instruction="\n- Use arrow keys to navigate\n- Press Enter to select",
        style=questionary.Style(
            [
                ("selected", "fg:magenta noinherit"),
                ("highlighted", "fg:magenta noinherit"),
                ("pointer", "fg:magenta noinherit"),
            ]
        ),
    ).ask()

    if choice is None:
        console.print("\n[red]No deep thinking llm engine selected. Exiting...[/red]")
        exit(1)

    return choice

def select_llm_provider() -> tuple[str, str]:
    """Select the OpenAI api url using interactive selection."""
    # Define LLM provider options with their corresponding endpoints
    BASE_URLS = [
        ("OpenAI", "https://api.openai.com/v1"),
        ("Anthropic", "https://api.anthropic.com/"),
        ("Google", "https://generativelanguage.googleapis.com/v1"),
        ("Openrouter (推荐, 免费额度大)", "https://openrouter.ai/api/v1"),
        ("Groq (高速, 免费)", "https://api.groq.com/openai/v1"),
        ("Together AI (开源模型丰富)", "https://api.together.xyz/v1"),
        ("Ollama (本地, 完全免费)", "http://localhost:11434/v1"),
    ]
    
    choice = questionary.select(
        "Select your LLM Provider:",
        choices=[
            questionary.Choice(display, value=(display, value))
            for display, value in BASE_URLS
        ],
        instruction="\n- Use arrow keys to navigate\n- Press Enter to select",
        style=questionary.Style(
            [
                ("selected", "fg:magenta noinherit"),
                ("highlighted", "fg:magenta noinherit"),
                ("pointer", "fg:magenta noinherit"),
            ]
        ),
    ).ask()
    
    if choice is None:
        console.print("\n[red]no OpenAI backend selected. Exiting...[/red]")
        exit(1)
    
    display_name, url = choice
    print(f"You selected: {display_name}\tURL: {url}")
    
    return display_name, url
