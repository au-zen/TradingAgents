# 🤖 TradingAgents 模型配置完整指南

**版本**: v2.0.0  
**更新日期**: 2025年7月17日

---

## 📋 目录

1. [快速开始](#快速开始)
2. [推荐配置](#推荐配置)
3. [详细配置说明](#详细配置说明)
4. [故障排除](#故障排除)
5. [性能优化](#性能优化)

---

## 🚀 快速开始

### 一键配置推荐

```bash
# 1. 高速免费配置 (推荐新手)
export LLM_PROVIDER=groq
export DEEP_THINK_LLM=llama3-groq-70b-8192-tool-use-preview
export QUICK_THINK_LLM=llama3-groq-8b-8192-tool-use-preview

# 2. 验证配置
python scripts/validate_model_config.py

# 3. 开始使用
python -m cli.main --ticker AAPL --start-date 2024-01-01 --end-date 2024-01-02
```

---

## 💎 推荐配置

### 🚀 高速免费 (Groq) - 新手推荐

**适用场景**: 快速体验、学习使用、高频分析

```bash
# 配置设置
export LLM_PROVIDER=groq
export DEEP_THINK_LLM=llama3-groq-70b-8192-tool-use-preview
export QUICK_THINK_LLM=llama3-groq-8b-8192-tool-use-preview
export GROQ_API_KEY=your_groq_api_key

# 获取API密钥: https://console.groq.com/keys
```

**优势**:
- ⚡ 响应速度极快 (< 1秒)
- 💰 完全免费使用
- 🛠️ 支持工具调用
- 🔄 高并发处理

**限制**:
- 模型选择相对有限
- 需要稳定网络连接

---

### 💎 平衡推荐 (OpenRouter) - 日常使用

**适用场景**: 个人投资、日常分析、投资研究

```bash
# 配置设置
export LLM_PROVIDER=openrouter
export DEEP_THINK_LLM=deepseek/deepseek-r1-distill-qwen-14b:free
export QUICK_THINK_LLM=qwen/qwen3-14b:free
export OPENROUTER_API_KEY=your_openrouter_api_key

# 获取API密钥: https://openrouter.ai/keys
```

**优势**:
- 💰 免费额度充足
- 🧠 模型质量优秀
- 🌐 支持多种模型
- 🛠️ 工具调用稳定

---

### 🧠 智能优选 (OpenRouter Pro) - 专业分析

**适用场景**: 专业投资、机构研究、复杂策略

```bash
# 配置设置
export LLM_PROVIDER=openrouter
export DEEP_THINK_LLM=qwen/qwen2.5-72b-instruct
export QUICK_THINK_LLM=qwen/qwen2.5-14b-instruct
export OPENROUTER_API_KEY=your_openrouter_api_key

# 成本: $0.5-2/M tokens
```

**优势**:
- 🎯 顶级模型性能
- 🧠 复杂推理能力强
- 🌍 多语言支持优秀
- 📊 分析深度高

---

### 🏠 本地部署 (Ollama) - 隐私优先

**适用场景**: 敏感数据、离线环境、企业内部

```bash
# 1. 安装 Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# 2. 下载模型
ollama pull qwen3:14b
ollama pull qwen3:8b

# 3. 配置设置
export LLM_PROVIDER=ollama
export DEEP_THINK_LLM=qwen3:14b
export QUICK_THINK_LLM=qwen3:8b

# 4. 启动服务
ollama serve
```

**硬件要求**:
- **最低**: 16GB RAM, 8GB GPU VRAM
- **推荐**: 32GB RAM, 16GB GPU VRAM
- **存储**: 50GB+ 可用空间

**优势**:
- 💰 完全免费
- 🔒 数据隐私保护
- 🌐 无网络依赖
- ⚙️ 可自定义模型

---

### ⚡ 开源高速 (Together AI) - 性价比

**适用场景**: 开源项目、研究实验、成本敏感

```bash
# 配置设置
export LLM_PROVIDER=together
export DEEP_THINK_LLM=Qwen/Qwen2-72B-Instruct
export QUICK_THINK_LLM=Qwen/Qwen2.5-7B-Instruct
export TOGETHER_API_KEY=your_together_api_key

# 获取API密钥: https://api.together.xyz/settings/api-keys
# 成本: $0.2-1/M tokens
```

---

### 🔬 专业版 (OpenAI) - 企业级

**适用场景**: 企业应用、关键业务、高可靠性

```bash
# 配置设置
export LLM_PROVIDER=openai
export DEEP_THINK_LLM=gpt-4o
export QUICK_THINK_LLM=gpt-4o-mini
export OPENAI_API_KEY=your_openai_api_key

# 获取API密钥: https://platform.openai.com/api-keys
# 成本: $2.5-15/M tokens
```

---

## 🔧 详细配置说明

### 环境变量配置

```bash
# 方法1: 直接设置环境变量
export LLM_PROVIDER=your_provider
export DEEP_THINK_LLM=your_deep_model
export QUICK_THINK_LLM=your_quick_model
export API_KEY=your_api_key

# 方法2: 使用 .env 文件
echo "LLM_PROVIDER=your_provider" >> .env
echo "DEEP_THINK_LLM=your_deep_model" >> .env
echo "QUICK_THINK_LLM=your_quick_model" >> .env
echo "API_KEY=your_api_key" >> .env
```

### 配置验证

```bash
# 验证配置
python scripts/validate_model_config.py

# 测试功能
python scripts/test_all_improvements.py

# 调试工具绑定
python scripts/debug_tool_binding.py
```

---

## 🛠️ 故障排除

### 常见问题

#### 1. API密钥错误
```bash
# 检查API密钥是否正确设置
echo $OPENROUTER_API_KEY
echo $GROQ_API_KEY

# 重新设置API密钥
export OPENROUTER_API_KEY=your_correct_key
```

#### 2. 模型不支持工具调用
```bash
# 验证模型能力
python -c "
from tradingagents.config.model_capabilities import is_tool_calling_supported
print(is_tool_calling_supported('openrouter', 'qwen/qwen3-14b:free'))
"
```

#### 3. Ollama连接失败
```bash
# 检查Ollama服务状态
curl http://localhost:11434/api/tags

# 重启Ollama服务
ollama serve

# 检查模型是否下载
ollama list
```

#### 4. 网络连接问题
```bash
# 测试API连接
curl -H "Authorization: Bearer $OPENROUTER_API_KEY" \
     https://openrouter.ai/api/v1/models

# 设置代理 (如需要)
export HTTP_PROXY=http://your-proxy:port
export HTTPS_PROXY=http://your-proxy:port
```

---

## ⚡ 性能优化

### 模型选择策略

1. **快速响应**: 选择Groq提供商
2. **成本优化**: 使用免费模型或本地部署
3. **质量优先**: 选择大参数模型
4. **稳定性**: 选择OpenAI或成熟模型

### 并发优化

```bash
# 设置并发限制
export MAX_CONCURRENT_REQUESTS=5
export REQUEST_TIMEOUT=30

# 启用缓存
export ENABLE_CACHE=true
export CACHE_TTL=3600
```

### 内存优化

```bash
# 本地部署内存优化
export OLLAMA_NUM_PARALLEL=2
export OLLAMA_MAX_LOADED_MODELS=2
export OLLAMA_FLASH_ATTENTION=1
```

---

## 📊 配置对比表

| 配置 | 成本 | 速度 | 质量 | 隐私 | 设置难度 |
|------|------|------|------|------|----------|
| Groq | 免费 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| OpenRouter | 免费/付费 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Ollama | 免费 | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| Together AI | 付费 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| OpenAI | 付费 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## 🎯 使用建议

### 新手用户
1. 从 **Groq高速免费** 配置开始
2. 熟悉后升级到 **OpenRouter平衡** 配置
3. 有特殊需求时考虑其他配置

### 专业用户
1. 根据具体需求选择配置
2. 考虑成本和性能平衡
3. 建立多配置备份方案

### 企业用户
1. 优先考虑 **本地部署** 或 **OpenAI专业版**
2. 建立完整的监控和备份机制
3. 定期评估和优化配置

---

**需要帮助？** 运行 `python scripts/validate_model_config.py` 获取配置建议！
