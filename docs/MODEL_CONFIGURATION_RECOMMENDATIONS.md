# TradingAgents 模型配置建议
**日期**: 2025年7月17日  
**版本**: v1.2.0  

---

## 📋 概述

本文档提供了TradingAgents项目的完整模型配置建议，包括OpenRouter免费模型、Ollama本地模型、embedding模型选择以及其他免费外部API配置。

---

## 🌐 OpenRouter 免费模型推荐

### 推荐模型（支持Function Calling）

#### 1. **Qwen3-30B-A3B (免费)** ⭐⭐⭐⭐⭐
```yaml
model_id: "qwen/qwen3-30b-a3b:free"
特点:
  - 支持工具调用/函数调用
  - 优秀的中文支持
  - 30B参数，性能强劲
  - 完全免费
适用场景: 深度思考任务、复杂分析
```

#### 2. **Qwen3-14B (免费)** ⭐⭐⭐⭐
```yaml
model_id: "qwen/qwen3-14b:free"
特点:
  - 支持工具调用
  - 良好的中文支持
  - 14B参数，平衡性能和速度
  - 完全免费
适用场景: 快速思考任务、对话
```

#### 3. **DeepSeek-R1-Distill-Qwen-14B (免费)** ⭐⭐⭐⭐
```yaml
model_id: "deepseek/deepseek-r1-distill-qwen-14b:free"
特点:
  - 推理能力强
  - 支持工具调用
  - 中文支持优秀
  - 完全免费
适用场景: 复杂推理、分析任务
```

### 当前配置更新建议
```python
# tradingagents/default_config.py
DEFAULT_CONFIG = {
    # 推荐免费深度模型（推理/复杂任务）
    "deep_think_llm": "qwen/qwen3-30b-a3b:free",
    # 推荐免费快速模型（对话/轻量任务）
    "quick_think_llm": "qwen/qwen3-14b:free",
    "backend_url": "https://openrouter.ai/api/v1",
}
```

---

## 🖥️ Ollama 本地模型推荐

### 推荐模型（按性能排序）

#### 1. **Qwen3:14b** ⭐⭐⭐⭐⭐
```bash
ollama pull qwen3:14b
```
- **优势**: 最新Qwen3系列，支持工具调用，中文支持优秀
- **参数**: 14B
- **内存需求**: ~8GB
- **适用**: 主要推理模型

#### 2. **Qwen3:8b** ⭐⭐⭐⭐
```bash
ollama pull qwen3:8b
```
- **优势**: 平衡性能和资源消耗
- **参数**: 8B
- **内存需求**: ~5GB
- **适用**: 快速响应模型

#### 3. **DeepSeek-R1:14b** ⭐⭐⭐⭐
```bash
ollama pull deepseek-r1:14b
```
- **优势**: 强推理能力，适合复杂分析
- **参数**: 14B
- **内存需求**: ~8GB
- **适用**: 深度分析任务

#### 4. **Llama3.1:8b** ⭐⭐⭐
```bash
ollama pull llama3.1:8b
```
- **优势**: 稳定可靠，工具调用支持好
- **参数**: 8B
- **内存需求**: ~5GB
- **适用**: 备用模型

### 配置建议
```python
# 本地模型配置
OLLAMA_CONFIG = {
    "primary_model": "qwen3:14b",
    "fallback_model": "qwen3:8b",
    "reasoning_model": "deepseek-r1:14b",
    "base_url": "http://localhost:11434"
}
```

---

## 🔍 Embedding 模型推荐

### 1. **nomic-embed-text** (Ollama) ⭐⭐⭐⭐⭐
```bash
ollama pull nomic-embed-text
```
- **优势**: 高性能，大上下文窗口，免费
- **维度**: 768
- **上下文**: 8192 tokens
- **适用**: 主要embedding模型

### 2. **mxbai-embed-large** (Ollama) ⭐⭐⭐⭐
```bash
ollama pull mxbai-embed-large
```
- **优势**: 最新技术，性能优秀
- **维度**: 1024
- **适用**: 高精度需求

### 3. **bge-m3** (Ollama) ⭐⭐⭐⭐
```bash
ollama pull bge-m3
```
- **优势**: 多语言支持，中文友好
- **维度**: 1024
- **适用**: 多语言场景

### 配置建议
```python
# Embedding配置
EMBEDDING_CONFIG = {
    "provider": "ollama",
    "model": "nomic-embed-text:latest",
    "base_url": "http://localhost:11434"
}
```

---

## 🌍 其他免费外部API推荐

### 1. **Groq** ⭐⭐⭐⭐⭐
```yaml
提供商: Groq
免费额度: 每天14,400 requests
支持模型:
  - llama3-groq-70b-8192-tool-use-preview
  - llama3-groq-8b-8192-tool-use-preview
  - mixtral-8x7b-32768
特点:
  - 极快推理速度
  - 支持工具调用
  - 稳定可靠
API端点: https://api.groq.com/openai/v1
```

### 2. **Together AI** ⭐⭐⭐⭐
```yaml
提供商: Together AI
免费额度: $5 免费额度
支持模型:
  - meta-llama/Llama-3-70b-chat-hf
  - meta-llama/Llama-3-8b-chat-hf
  - Qwen/Qwen2-72B-Instruct
特点:
  - 开源模型丰富
  - 支持工具调用
  - 中文模型支持好
API端点: https://api.together.xyz/v1
```

### 3. **Hugging Face Inference API** ⭐⭐⭐⭐
```yaml
提供商: Hugging Face
免费额度: 每月30,000 tokens
支持模型:
  - microsoft/DialoGPT-medium
  - Qwen/Qwen2.5-7B-Instruct
  - meta-llama/Llama-3.2-3B-Instruct
特点:
  - 模型选择丰富
  - 开源友好
  - 社区支持强
API端点: https://api-inference.huggingface.co
```

### 4. **Google AI Studio** ⭐⭐⭐
```yaml
提供商: Google
免费额度: 每分钟15 requests
支持模型:
  - gemini-1.5-flash
  - gemini-1.5-pro
特点:
  - Google最新模型
  - 支持工具调用
  - 多模态支持
API端点: https://generativelanguage.googleapis.com/v1beta
```

---

## 🔐 环境变量配置

### .env 文件模板
```bash
# OpenRouter
OPENROUTER_API_KEY=your_openrouter_api_key_here

# Groq
GROQ_API_KEY=your_groq_api_key_here

# Together AI
TOGETHER_API_KEY=your_together_api_key_here

# Hugging Face
HUGGINGFACE_API_KEY=your_huggingface_api_key_here

# Google AI Studio
GOOGLE_API_KEY=your_google_api_key_here

# Ollama (本地)
OLLAMA_BASE_URL=http://localhost:11434

# 数据源API Keys
AKSHARE_TOKEN=your_akshare_token_here
FINNHUB_API_KEY=your_finnhub_api_key_here
```

### 配置文件更新
```python
# tradingagents/default_config.py
import os
from dotenv import load_dotenv

load_dotenv()

DEFAULT_CONFIG = {
    # LLM Provider配置
    "llm_provider": "openrouter",  # openrouter, groq, together, huggingface, google
    
    # OpenRouter配置
    "openrouter_api_key": os.getenv("OPENROUTER_API_KEY"),
    "deep_think_llm": "qwen/qwen3-30b-a3b:free",
    "quick_think_llm": "qwen/qwen3-14b:free",
    
    # 备用API配置
    "groq_api_key": os.getenv("GROQ_API_KEY"),
    "together_api_key": os.getenv("TOGETHER_API_KEY"),
    "huggingface_api_key": os.getenv("HUGGINGFACE_API_KEY"),
    "google_api_key": os.getenv("GOOGLE_API_KEY"),
    
    # Embedding配置
    "embedding_provider": "ollama",
    "embedding_model": "nomic-embed-text:latest",
    "ollama_base_url": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
    
    # API端点
    "api_endpoints": {
        "openrouter": "https://openrouter.ai/api/v1",
        "groq": "https://api.groq.com/openai/v1",
        "together": "https://api.together.xyz/v1",
        "huggingface": "https://api-inference.huggingface.co",
        "google": "https://generativelanguage.googleapis.com/v1beta"
    }
}
```

---

## 🚀 使用建议

### 1. **生产环境配置**
- 主要使用: OpenRouter (qwen3-30b-a3b:free)
- 备用: Groq (llama3-groq-70b-tool-use)
- 本地: Ollama (qwen3:14b)

### 2. **开发环境配置**
- 主要使用: Ollama (qwen3:8b)
- 测试: OpenRouter免费模型

### 3. **资源受限环境**
- 使用: Groq API (速度快)
- 备用: Together AI

### 4. **离线环境**
- 使用: Ollama本地模型
- 推荐: qwen3:8b + nomic-embed-text

---

## 📊 性能对比

| 模型类型 | 推理速度 | 中文支持 | 工具调用 | 成本 | 推荐度 |
|---------|---------|---------|---------|------|--------|
| Qwen3-30B (OpenRouter) | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 免费 | ⭐⭐⭐⭐⭐ |
| Groq Llama3-70B | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | 免费额度 | ⭐⭐⭐⭐ |
| Ollama Qwen3:14b | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 免费 | ⭐⭐⭐⭐⭐ |
| Together AI Qwen2-72B | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 免费额度 | ⭐⭐⭐⭐ |

---

**配置完成时间**: 2025年7月17日  
**建议更新频率**: 每月检查一次新模型  
**维护状态**: 持续更新 ✅
