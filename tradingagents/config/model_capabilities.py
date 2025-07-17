"""
模型能力配置
定义不同API提供商和模型的工具调用支持情况
"""

# 支持工具调用的模型配置
MODEL_CAPABILITIES = {
    "openrouter": {
        "tool_calling_models": [
            # Qwen系列 - 支持工具调用
            "qwen/qwen3-30b-a3b:free",
            "qwen/qwen3-14b:free", 
            "qwen/qwen2.5-72b-instruct",
            "qwen/qwen2.5-14b-instruct",
            
            # DeepSeek系列 - 支持工具调用
            "deepseek/deepseek-r1-distill-qwen-14b:free",
            "deepseek/deepseek-chat",
            "deepseek/deepseek-coder",
            
            # Meta Llama系列 - 支持工具调用
            "meta-llama/llama-3.1-70b-instruct",
            "meta-llama/llama-3.1-8b-instruct",
            "meta-llama/llama-3.2-11b-vision-instruct",
            
            # Anthropic Claude系列 - 支持工具调用
            "anthropic/claude-3.5-sonnet",
            "anthropic/claude-3-haiku",
            
            # OpenAI系列 - 支持工具调用
            "openai/gpt-4o",
            "openai/gpt-4o-mini",
            "openai/gpt-3.5-turbo",
            
            # Google系列 - 支持工具调用
            "google/gemini-pro-1.5",
            "google/gemini-flash-1.5",
        ],
        "non_tool_calling_models": [
            # 一些基础模型不支持工具调用
            "meta-llama/llama-2-7b-chat",
            "mistralai/mistral-7b-instruct",
        ],
        "recommended_configs": {
            "production": {
                "deep_think_llm": "qwen/qwen3-30b-a3b:free",
                "quick_think_llm": "qwen/qwen3-14b:free"
            },
            "development": {
                "deep_think_llm": "deepseek/deepseek-r1-distill-qwen-14b:free",
                "quick_think_llm": "qwen/qwen3-14b:free"
            },
            "high_performance": {
                "deep_think_llm": "anthropic/claude-3.5-sonnet",
                "quick_think_llm": "openai/gpt-4o-mini"
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
            "qwen3:14b",
            "qwen3:8b",
            "llama3.1:70b",
            "llama3.1:8b",
            "mistral:7b",
            "codellama:13b",
        ],
        "non_tool_calling_models": [
            "llama2:7b",
        ],
        "recommended_configs": {
            "production": {
                "deep_think_llm": "qwen3:14b",
                "quick_think_llm": "qwen3:8b"
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
        "qwen/qwen3-30b-a3b:free",
        "qwen/qwen3-14b:free",
        "deepseek/deepseek-r1-distill-qwen-14b:free",
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
        "qwen3:14b",
        "qwen3:8b",
        "llama3.1:8b",
    ]
}

def get_free_tool_calling_models(provider: str) -> list:
    """获取免费且支持工具调用的模型"""
    return FREE_TOOL_CALLING_MODELS.get(provider, [])
