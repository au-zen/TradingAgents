"""
模型能力配置
定义不同API提供商和模型的工具调用支持情况
"""

# 支持工具调用的模型配置
MODEL_CAPABILITIES = {
    "openrouter": {
        "tool_calling_models": [
            # Moonshot系列 - 支持工具调用
            "moonshotai/kimi-k2:free",

            # Qwen系列 - 支持工具调用
            "qwen/qwen3-235b-a22b:free",

            # Mistral系列 - 支持工具调用
            "mistralai/mistral-small-3.2-24b-instruct:free",
            "mistralai/devstral-small-2505:free",
            "mistralai/mistral-small-3.1-24b-instruct:free",
            "mistralai/mistral-7b-instruct:free",

            # Meta Llama系列 - 支持工具调用
            "meta-llama/llama-3.3-70b-instruct:free",

            # OpenRouter系列 - 支持工具调用
            "openrouter/cypher-alpha:free",

            # Google系列 - 支持工具调用
            "google/gemini-2.5-pro-exp-03-25",
            "google/gemini-2.0-flash-exp:free",

            # DeepSeek系列 - 支持工具调用
            "deepseek/deepseek-chat-v3-0324:free",
        ],
        "non_tool_calling_models": [
            # 一些基础模型不支持工具调用
            "meta-llama/llama-2-7b-chat",
        ],
        "recommended_configs": {
            "production": {
                "deep_think_llm": "qwen/qwen3-235b-a22b:free",
                "quick_think_llm": "moonshotai/kimi-k2:free"
            },
            "development": {
                "deep_think_llm": "deepseek/deepseek-chat-v3-0324:free",
                "quick_think_llm": "mistralai/mistral-small-3.2-24b-instruct:free"
            },
            "high_performance": {
                "deep_think_llm": "google/gemini-2.5-pro-exp-03-25",
                "quick_think_llm": "meta-llama/llama-3.3-70b-instruct:free"
            }
        }
    },
    
    "groq": {
        "tool_calling_models": [
            "llama3-groq-70b-8192-tool-use-preview",
            "llama3-groq-8b-8192-tool-use-preview",
            "llama-3.1-70b-versatile",
            "llama-3.1-8b-instant",
            "mixtral-8x7b-32768",
        ],
        "non_tool_calling_models": [
            "llama2-70b-4096",
        ],
        "recommended_configs": {
            "production": {
                "deep_think_llm": "llama3-groq-70b-8192-tool-use-preview",
                "quick_think_llm": "llama3-groq-8b-8192-tool-use-preview"
            }
        }
    },
    
    "together": {
        "tool_calling_models": [
            "Qwen/Qwen2-72B-Instruct",
            "Qwen/Qwen2.5-7B-Instruct",
            "meta-llama/Llama-3-70b-chat-hf",
            "meta-llama/Llama-3-8b-chat-hf",
            "mistralai/Mixtral-8x7B-Instruct-v0.1",
        ],
        "non_tool_calling_models": [
            "togethercomputer/RedPajama-INCITE-7B-Chat",
        ],
        "recommended_configs": {
            "production": {
                "deep_think_llm": "Qwen/Qwen2-72B-Instruct",
                "quick_think_llm": "Qwen/Qwen2.5-7B-Instruct"
            }
        }
    },
    
    "google": {
        "tool_calling_models": [
            "gemini-1.5-pro",
            "gemini-1.5-flash",
            "gemini-1.0-pro",
        ],
        "non_tool_calling_models": [],
        "recommended_configs": {
            "production": {
                "deep_think_llm": "gemini-1.5-pro",
                "quick_think_llm": "gemini-1.5-flash"
            }
        }
    },
    
    "anthropic": {
        "tool_calling_models": [
            "claude-3-5-sonnet-20241022",
            "claude-3-haiku-20240307",
            "claude-3-opus-20240229",
        ],
        "non_tool_calling_models": [],
        "recommended_configs": {
            "production": {
                "deep_think_llm": "claude-3-5-sonnet-20241022",
                "quick_think_llm": "claude-3-haiku-20240307"
            }
        }
    },
    
    "ollama": {
        "tool_calling_models": [
            "qwen3:latest",
            "llama3.1:latest",
            "llama3.2:latest",
            "mistral:latest",
            "deepseek-coder-v2:latest",
            "deepseek-r1:latest",
        ],
        "non_tool_calling_models": [
            "llama2:latest",
            "codellama:latest",
        ],
        "recommended_configs": {
            "production": {
                "deep_think_llm": "qwen3:latest",
                "quick_think_llm": "llama3.1:latest"
            }
        }
    }
}

def normalize_provider_name(provider: str) -> str:
    """标准化提供商名称，去除描述文字"""
    if not provider:
        return ""
    return provider.lower().split()[0]

def get_tool_calling_models(provider: str) -> list:
    """获取支持工具调用的模型列表"""
    provider = normalize_provider_name(provider)
    return MODEL_CAPABILITIES.get(provider, {}).get("tool_calling_models", [])

def is_tool_calling_supported(provider: str, model: str) -> bool:
    """检查指定模型是否支持工具调用"""
    provider = normalize_provider_name(provider)
    tool_calling_models = get_tool_calling_models(provider)
    return model in tool_calling_models

def get_recommended_config(provider: str, config_type: str = "production") -> dict:
    """获取推荐的模型配置"""
    provider = normalize_provider_name(provider)
    return MODEL_CAPABILITIES.get(provider, {}).get("recommended_configs", {}).get(config_type, {})

def validate_model_config(provider: str, deep_think_llm: str, quick_think_llm: str) -> dict:
    """验证模型配置是否支持工具调用"""
    # 标准化提供商名称
    provider = normalize_provider_name(provider)

    result = {
        "valid": True,
        "warnings": [],
        "errors": []
    }

    if provider not in MODEL_CAPABILITIES:
        result["errors"].append(f"不支持的提供商: {provider}")
        result["valid"] = False
        return result
    
    # 检查deep_think_llm
    if not is_tool_calling_supported(provider, deep_think_llm):
        result["warnings"].append(f"Deep-thinking模型 {deep_think_llm} 可能不支持工具调用")
        result["valid"] = False
    
    # 检查quick_think_llm
    if not is_tool_calling_supported(provider, quick_think_llm):
        result["warnings"].append(f"Quick-thinking模型 {quick_think_llm} 可能不支持工具调用")
        result["valid"] = False
    
    return result

# 免费模型推荐（支持工具调用）
FREE_TOOL_CALLING_MODELS = {
    "openrouter": [
        "moonshotai/kimi-k2:free",
        "qwen/qwen3-235b-a22b:free",
        "mistralai/mistral-small-3.2-24b-instruct:free",
        "mistralai/devstral-small-2505:free",
        "mistralai/mistral-small-3.1-24b-instruct:free",
        "meta-llama/llama-3.3-70b-instruct:free",
        "mistralai/mistral-7b-instruct:free",
        "openrouter/cypher-alpha:free",
        "google/gemini-2.0-flash-exp:free",
        "deepseek/deepseek-chat-v3-0324:free",
    ],
    "groq": [
        "llama3-groq-70b-8192-tool-use-preview",
        "llama3-groq-8b-8192-tool-use-preview",
    ],
    "google": [
        "gemini-1.5-flash",
        "gemini-1.5-pro",  # 有免费额度
    ],
    "ollama": [
        "qwen3:latest",
        "llama3.1:latest",
        "llama3.2:latest",
        "mistral:latest",
        "deepseek-r1:latest",
    ]
}

def get_free_tool_calling_models(provider: str) -> list:
    """获取免费且支持工具调用的模型"""
    return FREE_TOOL_CALLING_MODELS.get(provider, [])
