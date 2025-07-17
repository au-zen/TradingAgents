# TradingAgents 完整设置指南
**日期**: 2025年7月17日  
**版本**: v1.2.0  

---

## 📋 概述

本指南提供了TradingAgents项目的完整设置流程，包括修复应用、模型配置、环境变量管理等所有必要步骤。

---

## 🔧 1. 系统修复（已完成）

### 修复内容
- ✅ **工具调用错误修复**: 修复了`get_stock_individual_info`调用语法
- ✅ **报告语言修复**: 所有agent现在输出中文报告
- ✅ **状态管理修复**: 明确区分ticker和公司名称

### 验证修复
```bash
# 运行验证脚本
python test_fixes_verification.py

# 预期输出: 5/5 tests passed
```

---

## 🌐 2. 模型配置

### OpenRouter 免费模型（推荐）
```yaml
主要模型: qwen/qwen3-30b-a3b:free
快速模型: qwen/qwen3-14b:free
特点: 免费、支持工具调用、中文友好
```

### Ollama 本地模型
```bash
# 安装推荐模型
ollama pull qwen3:14b          # 主要模型
ollama pull qwen3:8b           # 快速模型  
ollama pull nomic-embed-text   # Embedding模型
```

### 其他免费API
- **Groq**: 极快推理速度，每天14,400请求
- **Together AI**: 开源模型丰富，$5免费额度
- **Hugging Face**: 社区模型，每月30,000 tokens
- **Google AI Studio**: Gemini模型，每分钟15请求

---

## 🔐 3. 环境变量配置

### 步骤1: 创建.env文件
```bash
# 复制模板文件
cp .env.example .env
```

### 步骤2: 配置API密钥
编辑`.env`文件，至少配置以下密钥：

```bash
# 必需配置（至少选择一个）
OPENROUTER_API_KEY=your_openrouter_api_key_here
GROQ_API_KEY=your_groq_api_key_here

# 数据源配置（推荐）
AKSHARE_TOKEN=your_akshare_token_here
FINNHUB_API_KEY=your_finnhub_api_key_here

# 本地模型配置
OLLAMA_BASE_URL=http://localhost:11434
```

### 步骤3: 验证配置
```bash
# 运行配置验证脚本
python scripts/validate_config.py
```

---

## 🚀 4. 快速开始

### 安装依赖
```bash
# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或 .venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 启动Ollama（可选但推荐）
```bash
# 安装Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# 启动服务
ollama serve

# 下载模型
ollama pull qwen3:14b
ollama pull nomic-embed-text
```

### 运行测试
```bash
# 测试A股分析
python -m cli.main --ticker 603127.SH --start-date 2024-01-01 --end-date 2024-01-02 --non-interactive

# 预期结果: 正确识别"昭衍新药"，生成中文报告
```

---

## 📊 5. 配置推荐

### 生产环境
```yaml
主要LLM: OpenRouter (qwen3-30b-a3b:free)
备用LLM: Groq (llama3-groq-70b-tool-use)
本地LLM: Ollama (qwen3:14b)
Embedding: Ollama (nomic-embed-text)
```

### 开发环境
```yaml
主要LLM: Ollama (qwen3:8b)
备用LLM: OpenRouter免费模型
Embedding: Ollama (nomic-embed-text)
```

### 资源受限环境
```yaml
主要LLM: Groq API (速度快)
备用LLM: Together AI
Embedding: Ollama (nomic-embed-text)
```

---

## 🔍 6. API密钥获取指南

### OpenRouter (推荐)
1. 访问: https://openrouter.ai/keys
2. 注册账户
3. 创建API密钥
4. 免费额度: 每月$10

### Groq (高速)
1. 访问: https://console.groq.com/keys
2. 注册账户
3. 创建API密钥
4. 免费额度: 每天14,400请求

### Together AI (开源丰富)
1. 访问: https://api.together.xyz/settings/api-keys
2. 注册账户
3. 创建API密钥
4. 免费额度: $5

### AKShare (A股数据)
1. 访问: https://www.akshare.xyz/
2. 注册账户
3. 获取Token
4. 免费使用

---

## 🛠️ 7. 故障排除

### 常见问题

#### 1. 公司名称显示错误
```bash
# 检查修复是否生效
python test_fixes_verification.py

# 如果失败，重新运行修复
git pull origin main
```

#### 2. 报告输出英文
```bash
# 验证agent配置
grep -r "简体中文" tradingagents/agents/

# 应该在所有agent文件中找到中文要求
```

#### 3. API连接失败
```bash
# 验证API密钥
python scripts/validate_config.py

# 检查网络连接
curl -H "Authorization: Bearer $OPENROUTER_API_KEY" https://openrouter.ai/api/v1/models
```

#### 4. Ollama连接失败
```bash
# 检查Ollama状态
ollama list

# 重启Ollama服务
pkill ollama
ollama serve
```

### 日志调试
```bash
# 启用详细日志
export LOG_LEVEL=DEBUG

# 查看日志文件
tail -f eval_results/*/message_tool.log
```

---

## 📈 8. 性能优化

### 模型选择策略
- **复杂分析**: 使用30B+参数模型
- **快速响应**: 使用8B-14B参数模型
- **离线使用**: 优先Ollama本地模型
- **在线使用**: 优先免费API

### 缓存配置
```bash
# 启用Redis缓存（可选）
REDIS_URL=redis://localhost:6379/0

# 配置数据缓存目录
DATA_CACHE_DIR=./data_cache
```

---

## 🔄 9. 更新和维护

### 定期检查
- **每月**: 检查新的免费模型
- **每周**: 验证API密钥状态
- **每天**: 监控系统运行状态

### 更新命令
```bash
# 更新代码
git pull origin main

# 更新依赖
pip install -r requirements.txt --upgrade

# 更新Ollama模型
ollama pull qwen3:14b
```

---

## 📞 10. 支持和帮助

### 文档资源
- [修复报告](./TRADING_AGENTS_FIXES_2025_07_17.md)
- [模型配置建议](./MODEL_CONFIGURATION_RECOMMENDATIONS.md)
- [API文档](../README.md)

### 验证工具
- `test_fixes_verification.py` - 修复验证
- `scripts/validate_config.py` - 配置验证

### 社区支持
- GitHub Issues: 报告问题
- 文档更新: 提交PR
- 经验分享: 创建Discussion

---

**设置完成时间**: 2025年7月17日  
**系统状态**: 完全可用 ✅  
**下次检查**: 建议每月更新一次配置
