# LLM Integration Guide

This guide provides instructions on how to integrate and configure Large Language Models (LLMs) with the TradingAgents framework.

## Supported LLM Providers

The framework supports the following LLM providers:

- **OpenAI**: For using models like GPT-4, GPT-3.5, etc.
- **Ollama**: For running local LLMs on your machine.
- **OpenRouter**: For accessing a variety of LLMs from different providers.
- **Anthropic**: For using models like Claude 3.
- **Google**: For using models like Gemini.

## Configuration

You can configure the LLM provider and models in the `tradingagents/default_config.py` file or by setting environment variables.

### `default_config.py`

```python
DEFAULT_CONFIG = {
    # ... other settings
    "llm_provider": "openrouter",
    "deep_think_llm": "qwen/qwen3-30b-a3b:free",
    "quick_think_llm": "qwen/qwen3-14b:free",
    "backend_url": "https://openrouter.ai/api/v1",
    # ... other settings
}
```

### Environment Variables

You can also use environment variables to override the default settings:

- `LLM_PROVIDER`: The LLM provider to use (e.g., `openai`, `ollama`, `openrouter`, `anthropic`, `google`).
- `DEEP_THINK_LLM`: The model to use for deep thinking tasks.
- `QUICK_THINK_LLM`: The model to use for quick thinking tasks.
- `BACKEND_URL`: The API endpoint for the LLM provider.
- `OPENAI_API_KEY`: Your API key for OpenAI or OpenRouter.

## Embedding Models

The framework uses embedding models to create numerical representations of text data. You can configure the embedding model in `default_config.py` or by using environment variables.

### `default_config.py`

```python
DEFAULT_CONFIG = {
    # ... other settings
    "embedding_model": "nomic-embed-text",
    # ... other settings
}
```

### Environment Variables

- `EMBEDDING_PROVIDER`: The embedding provider to use (e.g., `http://localhost:11434/v1` for Ollama).
- `EMBEDDING_MODEL`: The embedding model to use (e.g., `nomic-embed-text`).

## Analyst Tooling & Routing

TradingAgents routes analyst tool calls through the `Toolkit` layer. For most tasks, the agent code uses generic helpers like `get_fundamentals()`; the Toolkit decides which underlying implementation to invoke:

- **US Tickers** – default OpenAI/Finnhub/SimFin pipelines
- **A-Share Tickers** – AkShare based utilities

This routing is transparent to the LLM configuration—you only need to ensure the LLMs have access to the tool descriptions (handled automatically).

### Online vs. Offline tools

If you run TradingAgents fully offline (no Internet), set the following env variable to disable web-based APIs and depend solely on AkShare/YFinance local data caches:

```bash
export ONLINE_TOOLS=false
```

When `ONLINE_TOOLS=false`, Toolkit will skip calls that rely on remote APIs and fall back to local data where possible.

## Usage

Once you have configured the LLM and embedding models, you can run the application as usual. The framework will automatically use the specified models for the different tasks.
