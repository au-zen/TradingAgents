# 🏗️ A股数据源增强配置指南

本指南将帮助您配置聚宽JQData、Tushare和Alltick等A股数据源，以获得更丰富和准确的A股市场数据。

---

## 📋 概述

TradingAgents现在支持多个A股数据源：

1. **聚宽JQData** - 专业的量化数据平台，提供高质量的A股数据
2. **Tushare** - 免费的金融数据接口，支持A股、港股、美股等
3. **Alltick** - 实时行情数据服务，提供高频数据
4. **AKShare** - 原有的免费数据源（继续支持）

---

## 🚀 快速开始

### 1. 安装依赖包

```bash
# 进入项目目录
cd TradingAgents

# 激活虚拟环境
source .venv/bin/activate

# 安装可选的数据源包
pip install jqdatasdk tushare requests
```

### 2. 配置环境变量

复制并编辑环境变量文件：

```bash
cp .env.example .env
```

在`.env`文件中添加您的API密钥：

```bash
# 聚宽JQData (A股数据增强)
# 获取地址: https://www.joinquant.com/default/index/sdk
JQDATA_USERNAME=your_jqdata_username_here
JQDATA_PASSWORD=your_jqdata_password_here

# Tushare Token (A股数据增强)
# 获取地址: https://tushare.pro/register
TUSHARE_TOKEN=your_tushare_token_here

# Alltick Token (A股实时数据)
# 获取地址: https://alltick.co/
ALLTICK_TOKEN=your_alltick_token_here
```

---

## 🔑 获取API密钥

### 聚宽JQData

1. 访问 [聚宽官网](https://www.joinquant.com/default/index/sdk)
2. 注册账号并登录
3. 进入"数据API"页面
4. 获取用户名和密码
5. **免费额度**: 每日可查询500次

### Tushare

1. 访问 [Tushare官网](https://tushare.pro/register)
2. 注册账号并登录
3. 进入"个人中心" -> "接口TOKEN"
4. 复制您的Token
5. **免费额度**: 每分钟120次调用

### Alltick

1. 访问 [Alltick官网](https://alltick.co/)
2. 注册账号并登录
3. 进入API管理页面
4. 创建API密钥
5. **免费额度**: 每日1000次调用

---

## 🧪 测试配置

运行测试脚本验证配置：

```bash
python scripts/test_openrouter_models_and_data_sources.py
```

预期输出：
```
🧪 测试A股数据源...

📋 A股数据源状态检查:
  ✅ jqdata: 可用
  ✅ tushare: 可用
  ✅ alltick: 可用

🔍 测试数据源初始化:
  ✅ JQData: 可用
  ✅ Tushare: 可用
  ✅ Alltick: 可用
```

---

## 📊 数据源优先级

系统会按以下优先级尝试数据源：

### 股票价格数据
1. **china_enhanced** (JQData → Tushare → Alltick)
2. **akshare** (原有数据源)
3. **yfin** (Yahoo Finance)

### 公司基本信息
1. **china_enhanced** (Tushare → JQData)
2. **akshare** (原有数据源)

### 基本面数据
1. **china_enhanced** (JQData基本面数据)
2. **akshare** (原有数据源)
3. **finnhub** (美股数据源)

---

## 💡 使用示例

### 获取股票数据

```python
from tradingagents.dataflows.china_stock_data_sources import get_china_stock_data

# 获取A股数据
data = get_china_stock_data("603127.SH", "2024-01-01", "2024-01-31")
print(data.head())
```

### 获取公司信息

```python
from tradingagents.dataflows.china_stock_data_sources import get_china_company_info

# 获取公司信息
info = get_china_company_info("603127.SH")
print(info)
```

### 使用增强数据源管理器

```python
from tradingagents.dataflows.enhanced_data_source_manager import EnhancedDataSourceManager

manager = EnhancedDataSourceManager()

# 获取增强的股票数据（自动故障转移）
data = manager.get_stock_data_enhanced("603127.SH", "2024-01-01", "2024-01-31")

# 获取增强的公司信息
info = manager.get_company_info_enhanced("603127.SH")
```

---

## 🔧 故障排除

### 常见问题

#### 1. JQData连接失败
```
jqdatasdk not installed. Install with: pip install jqdatasdk
```
**解决方案**: 安装jqdatasdk包
```bash
pip install jqdatasdk
```

#### 2. Tushare Token无效
```
Tushare token not found in environment variables
```
**解决方案**: 检查`.env`文件中的`TUSHARE_TOKEN`配置

#### 3. Alltick API调用失败
```
Alltick get_stock_data error: HTTP 401 Unauthorized
```
**解决方案**: 检查API Token是否正确，是否超出调用限制

### 调试模式

启用详细日志：

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# 然后运行您的代码
```

---

## 📈 性能优化

### 缓存配置

增强数据源管理器支持智能缓存：

```python
manager = EnhancedDataSourceManager()

# 使用缓存（默认6小时有效期）
data = manager.get_stock_data_enhanced(
    "603127.SH", 
    "2024-01-01", 
    "2024-01-31",
    use_cache=True,
    max_cache_age=6  # 小时
)
```

### 批量数据获取

对于多只股票，建议使用批量接口：

```python
symbols = ["603127.SH", "000001.SZ", "600036.SH"]

for symbol in symbols:
    try:
        data = get_china_stock_data(symbol, "2024-01-01", "2024-01-31")
        print(f"✅ {symbol}: {len(data)} records")
    except Exception as e:
        print(f"❌ {symbol}: {e}")
```

---

## 🎯 最佳实践

### 1. 数据源选择
- **高频交易**: 优先使用Alltick
- **基本面分析**: 优先使用JQData
- **免费使用**: 优先使用Tushare和AKShare

### 2. 错误处理
- 始终使用try-catch处理API调用
- 实现重试机制处理网络问题
- 监控API调用限制

### 3. 数据质量
- 对比多个数据源的结果
- 检查数据的完整性和一致性
- 定期验证数据准确性

---

## 📞 支持

如果您在配置过程中遇到问题：

1. 查看测试脚本输出的详细信息
2. 检查API密钥是否正确配置
3. 确认网络连接正常
4. 查看相关数据源的官方文档

---

## 🎉 完成

配置完成后，您的TradingAgents将能够：

- ✅ 使用多个高质量的A股数据源
- ✅ 自动故障转移确保数据可用性
- ✅ 智能缓存提高性能
- ✅ 获得更准确的分析结果

现在您可以开始使用增强的A股数据进行投资分析了！
