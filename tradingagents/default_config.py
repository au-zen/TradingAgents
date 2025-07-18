import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DEFAULT_CONFIG = {
    "project_dir": os.path.abspath(os.path.join(os.path.dirname(__file__), ".")),
    "results_dir": os.getenv("TRADINGAGENTS_RESULTS_DIR", "./results"),
    "data_dir": "./data",
    "data_cache_dir": os.path.join(
        os.path.abspath(os.path.join(os.path.dirname(__file__), ".")),
        "dataflows/data_cache",
    ),
    # =============================================================================
    # LLM Provider Configuration
    # =============================================================================
    "llm_provider": os.getenv("LLM_PROVIDER", "openrouter"),

    # OpenRouter Configuration (推荐主要使用)
    "openrouter_api_key": os.getenv("OPENROUTER_API_KEY"),
    "deep_think_llm": os.getenv("DEEP_THINK_LLM", "deepseek/deepseek-r1-distill-qwen-14b:free"),  # 支持工具调用
    "quick_think_llm": os.getenv("QUICK_THINK_LLM", "qwen/qwen3-14b:free"),  # 支持工具调用
    "backend_url": os.getenv("BACKEND_URL", "https://openrouter.ai/api/v1"),

    # Alternative API Configurations
    "groq_api_key": os.getenv("GROQ_API_KEY"),
    "together_api_key": os.getenv("TOGETHER_API_KEY"),
    "huggingface_api_key": os.getenv("HUGGINGFACE_API_KEY"),
    "google_api_key": os.getenv("GOOGLE_API_KEY"),
    "zhipuai_api_key": os.getenv("ZHIPUAI_API_KEY"),

    # API Endpoints
    "api_endpoints": {
        "openrouter": "https://openrouter.ai/api/v1",
        "groq": "https://api.groq.com/openai/v1",
        "together": "https://api.together.xyz/v1",
        "huggingface": "https://api-inference.huggingface.co",
        "google": "https://generativelanguage.googleapis.com/v1beta",
        "zhipuai": "https://open.bigmodel.cn/api/paas/v4"
    },

    # =============================================================================
    # Model Options by Provider
    # =============================================================================
    "model_options": {
        "openrouter": {
            "free_models": [
                "qwen/qwen3-30b-a3b:free",
                "qwen/qwen3-14b:free",
                "deepseek/deepseek-r1-distill-qwen-14b:free",
                "meta-llama/llama-3.2-3b-instruct:free",
                "microsoft/phi-3-mini-128k-instruct:free"
            ],
            "recommended": {
                "deep_think": "qwen/qwen3-30b-a3b:free",
                "quick_think": "qwen/qwen3-14b:free"
            }
        },
        "groq": {
            "free_models": [
                "llama3-groq-70b-8192-tool-use-preview",
                "llama3-groq-8b-8192-tool-use-preview",
                "mixtral-8x7b-32768",
                "gemma2-9b-it"
            ],
            "recommended": {
                "deep_think": "llama3-groq-70b-8192-tool-use-preview",
                "quick_think": "llama3-groq-8b-8192-tool-use-preview"
            }
        },
        "together": {
            "free_models": [
                "meta-llama/Llama-3-70b-chat-hf",
                "meta-llama/Llama-3-8b-chat-hf",
                "Qwen/Qwen2-72B-Instruct",
                "mistralai/Mixtral-8x7B-Instruct-v0.1"
            ],
            "recommended": {
                "deep_think": "Qwen/Qwen2-72B-Instruct",
                "quick_think": "meta-llama/Llama-3-8b-chat-hf"
            }
        },
        "ollama": {
            "recommended_models": [
                "qwen3:14b",
                "qwen3:8b",
                "deepseek-r1:14b",
                "llama3.1:8b"
            ],
            "recommended": {
                "deep_think": "qwen3:14b",
                "quick_think": "qwen3:8b"
            }
        },
        "google": {
            "free_models": [
                "gemini-1.5-flash",
                "gemini-1.5-pro"
            ],
            "recommended": {
                "deep_think": "gemini-1.5-pro",
                "quick_think": "gemini-1.5-flash"
            }
        },
        "zhipuai": {
            "free_models": [
                "glm-z1-flash",
                "glm-4-flash"
            ],
            "recommended": {
                "deep_think": "glm-z1-flash",
                "quick_think": "glm-4-flash"
            }
        }
    },
    # =============================================================================
    # Embedding Model Configuration
    # =============================================================================
    "embedding_provider": os.getenv("EMBEDDING_PROVIDER", "ollama"),
    "embedding_model": os.getenv("EMBEDDING_MODEL", "nomic-embed-text:latest"),
    "ollama_base_url": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),

    # =============================================================================
    # Application Settings
    # =============================================================================
    "max_debate_rounds": int(os.getenv("MAX_DEBATE_ROUNDS", "1")),
    "max_risk_discuss_rounds": int(os.getenv("MAX_RISK_DISCUSS_ROUNDS", "1")),
    "max_recur_limit": int(os.getenv("MAX_RECUR_LIMIT", "100")),
    "online_tools": os.getenv("ONLINE_TOOLS", "true").lower() == "true",

    # =============================================================================
    # Data Source API Keys
    # =============================================================================
    "akshare_token": os.getenv("AKSHARE_TOKEN"),
    "finnhub_api_key": os.getenv("FINNHUB_API_KEY"),
    "alpha_vantage_api_key": os.getenv("ALPHA_VANTAGE_API_KEY"),
    "news_api_key": os.getenv("NEWS_API_KEY"),

    # Reddit API Configuration
    "reddit_client_id": os.getenv("REDDIT_CLIENT_ID"),
    "reddit_client_secret": os.getenv("REDDIT_CLIENT_SECRET"),
    "reddit_user_agent": os.getenv("REDDIT_USER_AGENT", "TradingAgents/1.0"),
    # =============================================================================
    # Market Settings
    # =============================================================================
    "market_settings": {
        "cn_market": {
            "primary_data_source": "akshare",
            "backup_data_sources": []
        },
        "us_market": {
            "primary_data_source": "yfin",
            "backup_data_sources": ["finnhub"]
        }
    },

    # =============================================================================
    # Environment and Logging
    # =============================================================================
    "environment": os.getenv("ENVIRONMENT", "development"),
    "log_level": os.getenv("LOG_LEVEL", "INFO"),

    # =============================================================================
    # Database Configuration (Optional)
    # =============================================================================
    "database_url": os.getenv("DATABASE_URL"),
    "redis_url": os.getenv("REDIS_URL"),

    # =============================================================================
    # Security Configuration
    # =============================================================================
    "secret_key": os.getenv("SECRET_KEY"),
    "jwt_secret": os.getenv("JWT_SECRET"),
}
