"""
TradingAgents Web应用
提供图形化界面进行股票分析
"""

import streamlit as st
import sys
import os
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tradingagents.default_config import DEFAULT_CONFIG
from tradingagents.agents.utils.agent_utils import Toolkit
from tradingagents.dataflows.enhanced_data_source_manager import EnhancedDataSourceManager
from tradingagents.config.model_capabilities import validate_model_config, get_recommended_config
from tradingagents.config.model_recommendations import model_recommendations

# 页面配置
st.set_page_config(
    page_title="TradingAgents - 智能股票分析",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .status-good {
        color: #28a745;
        font-weight: bold;
    }
    .status-warning {
        color: #ffc107;
        font-weight: bold;
    }
    .status-error {
        color: #dc3545;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """主应用函数"""
    
    # 标题
    st.markdown('<h1 class="main-header">📈 TradingAgents 智能股票分析平台</h1>', unsafe_allow_html=True)
    
    # 侧边栏
    with st.sidebar:
        st.header("🔧 配置")
        
        # 模型配置状态
        st.subheader("🤖 模型配置")

        # 当前配置显示
        provider = DEFAULT_CONFIG["llm_provider"]
        deep_think_llm = DEFAULT_CONFIG["deep_think_llm"]
        quick_think_llm = DEFAULT_CONFIG["quick_think_llm"]

        validation_result = validate_model_config(provider, deep_think_llm, quick_think_llm)

        if validation_result["valid"]:
            st.markdown('<p class="status-good">✅ 模型配置正常</p>', unsafe_allow_html=True)
        else:
            st.markdown('<p class="status-error">❌ 模型配置有问题</p>', unsafe_allow_html=True)
            for warning in validation_result["warnings"]:
                st.warning(warning)

        # 配置信息展示
        with st.expander("📋 当前配置详情", expanded=False):
            st.write(f"**提供商**: {provider}")
            st.write(f"**深度思考模型**: {deep_think_llm}")
            st.write(f"**快速思考模型**: {quick_think_llm}")

        # 推荐配置
        st.subheader("🚀 智能推荐配置")

        # 场景选择
        scenario = st.selectbox(
            "选择使用场景",
            options=["个人投资", "专业分析", "企业部署", "开发测试", "教学演示", "数据隐私", "高频交易", "成本敏感"],
            help="根据您的使用场景获取最佳配置推荐"
        )

        # 预算选择
        budget = st.selectbox(
            "选择预算范围",
            options=["免费", "低预算", "中预算", "高预算"],
            help="根据您的预算获取合适的配置"
        )

        # 获取推荐配置
        scenario_configs = model_recommendations.get_recommendation_by_use_case(scenario)
        budget_configs = model_recommendations.get_recommendation_by_budget(budget)

        # 取交集，如果没有交集则使用场景推荐
        recommended_keys = list(set(scenario_configs) & set(budget_configs))
        if not recommended_keys:
            recommended_keys = scenario_configs

        # 显示推荐配置
        for config_key in recommended_keys[:3]:  # 最多显示3个推荐
            config = model_recommendations.get_recommendation(config_key)
            if config:
                with st.expander(f"{config['name']}", expanded=False):
                    col1, col2 = st.columns(2)

                    with col1:
                        st.write(f"**提供商**: {config['provider']}")
                        st.write(f"**深度思考模型**: {config['deep_think_llm']}")
                        st.write(f"**快速思考模型**: {config['quick_think_llm']}")
                        st.write(f"**成本**: {config['cost']}")
                        st.write(f"**设置难度**: {config['setup_difficulty']}")

                    with col2:
                        st.write("**优点**:")
                        for pro in config['pros']:
                            st.write(f"• {pro}")

                        st.write("**缺点**:")
                        for con in config['cons']:
                            st.write(f"• {con}")

                    st.write(f"**描述**: {config['description']}")

                    if st.button(f"📋 获取 {config['name']} 配置", key=f"config_{config_key}"):
                        setup_commands = model_recommendations.generate_setup_commands(config_key)
                        st.code(setup_commands, language="bash")
                        st.success("配置命令已生成！请在终端中运行这些命令。")
        
        # 分析选项
        st.subheader("分析选项")
        
        # 股票代码输入
        ticker = st.text_input("股票代码", value="603127.SH", help="输入股票代码，如 603127.SH 或 AAPL")
        
        # 日期范围
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("开始日期", value=datetime.now() - timedelta(days=30))
        with col2:
            end_date = st.date_input("结束日期", value=datetime.now())
        
        # 分析师选择
        st.subheader("选择分析师")
        analysts = st.multiselect(
            "分析师类型",
            ["market", "news", "social", "fundamentals"],
            default=["market", "fundamentals"],
            help="选择要包含的分析师类型"
        )
        
        # 分析按钮
        analyze_button = st.button("🚀 开始分析", type="primary", use_container_width=True)
    
    # 主内容区域
    tab1, tab2, tab3, tab4 = st.tabs(["📊 快速分析", "📈 股价图表", "🔍 数据源状态", "⚙️ 系统状态"])
    
    with tab1:
        st.header("快速分析")
        
        if analyze_button and ticker:
            with st.spinner("正在进行分析..."):
                try:
                    # 初始化工具
                    toolkit = Toolkit(DEFAULT_CONFIG)
                    
                    # 获取基本信息
                    if toolkit.ticker_is_china_stock(ticker):
                        st.success(f"检测到A股: {ticker}")
                        company_info = get_company_info(ticker)
                        if company_info:
                            display_company_info(company_info)
                    else:
                        st.info(f"检测到美股: {ticker}")
                    
                    # 获取股价数据
                    stock_data = get_stock_data(ticker, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
                    if stock_data is not None:
                        display_stock_summary(stock_data)
                    
                    # 获取新闻
                    news_data = get_news_data(ticker)
                    if news_data:
                        display_news_summary(news_data)
                    
                except Exception as e:
                    st.error(f"分析过程中出现错误: {e}")
        else:
            st.info("请在左侧输入股票代码并点击'开始分析'按钮")
    
    with tab2:
        st.header("股价图表")
        
        if ticker:
            try:
                stock_data = get_stock_data(ticker, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
                if stock_data is not None and not stock_data.empty:
                    display_stock_chart(stock_data, ticker)
                else:
                    st.warning("无法获取股价数据")
            except Exception as e:
                st.error(f"获取股价数据时出错: {e}")
    
    with tab3:
        st.header("数据源状态")
        
        if ticker:
            display_data_source_status(ticker)
    
    with tab4:
        st.header("系统状态")
        display_system_status()

@st.cache_data(ttl=300)  # 缓存5分钟
def get_company_info(ticker):
    """获取公司信息"""
    try:
        toolkit = Toolkit(DEFAULT_CONFIG)
        result = toolkit.get_stock_individual_info.invoke({"ticker": ticker})
        return result
    except Exception as e:
        st.error(f"获取公司信息失败: {e}")
        return None

@st.cache_data(ttl=300)
def get_stock_data(ticker, start_date, end_date):
    """获取股价数据"""
    try:
        data_manager = EnhancedDataSourceManager()
        df = data_manager.get_stock_data_enhanced(ticker, start_date, end_date)
        return df
    except Exception as e:
        st.error(f"获取股价数据失败: {e}")
        return None

@st.cache_data(ttl=300)
def get_news_data(ticker):
    """获取新闻数据"""
    try:
        data_manager = EnhancedDataSourceManager()
        news = data_manager.get_news_enhanced(ticker, limit=5)
        return news
    except Exception as e:
        st.error(f"获取新闻数据失败: {e}")
        return None

def display_company_info(company_info):
    """显示公司信息"""
    st.subheader("📋 公司基本信息")
    
    # 解析公司信息
    lines = company_info.split('\n')
    info_dict = {}
    for line in lines:
        if ':' in line:
            key, value = line.split(':', 1)
            info_dict[key.strip()] = value.strip()
    
    col1, col2 = st.columns(2)
    with col1:
        if "公司名称" in info_dict:
            st.metric("公司名称", info_dict["公司名称"])
        if "行业" in info_dict:
            st.metric("所属行业", info_dict["行业"])
    
    with col2:
        if "上市时间" in info_dict:
            st.metric("上市时间", info_dict["上市时间"])
        if "总股本" in info_dict:
            st.metric("总股本", info_dict["总股本"])
    
    if "主营业务" in info_dict:
        st.write("**主营业务**:", info_dict["主营业务"])

def display_stock_summary(stock_data):
    """显示股价摘要"""
    st.subheader("📈 股价摘要")
    
    if stock_data.empty:
        st.warning("没有股价数据")
        return
    
    # 计算基本指标
    latest_price = stock_data.iloc[-1]['close'] if 'close' in stock_data.columns else stock_data.iloc[-1]['收盘']
    first_price = stock_data.iloc[0]['close'] if 'close' in stock_data.columns else stock_data.iloc[0]['收盘']
    price_change = latest_price - first_price
    price_change_pct = (price_change / first_price) * 100
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("最新价格", f"¥{latest_price:.2f}")
    
    with col2:
        st.metric("价格变化", f"¥{price_change:.2f}", f"{price_change_pct:.2f}%")
    
    with col3:
        high_col = 'high' if 'high' in stock_data.columns else '最高'
        period_high = stock_data[high_col].max()
        st.metric("期间最高", f"¥{period_high:.2f}")
    
    with col4:
        low_col = 'low' if 'low' in stock_data.columns else '最低'
        period_low = stock_data[low_col].min()
        st.metric("期间最低", f"¥{period_low:.2f}")

def display_stock_chart(stock_data, ticker):
    """显示股价图表"""
    if stock_data.empty:
        st.warning("没有数据可显示")
        return
    
    # 处理列名（中英文兼容）
    date_col = 'date' if 'date' in stock_data.columns else '日期'
    open_col = 'open' if 'open' in stock_data.columns else '开盘'
    high_col = 'high' if 'high' in stock_data.columns else '最高'
    low_col = 'low' if 'low' in stock_data.columns else '最低'
    close_col = 'close' if 'close' in stock_data.columns else '收盘'
    volume_col = 'volume' if 'volume' in stock_data.columns else '成交量'
    
    # 创建K线图
    fig = go.Figure(data=go.Candlestick(
        x=stock_data.index if date_col not in stock_data.columns else stock_data[date_col],
        open=stock_data[open_col],
        high=stock_data[high_col],
        low=stock_data[low_col],
        close=stock_data[close_col],
        name=ticker
    ))
    
    fig.update_layout(
        title=f"{ticker} 股价走势",
        yaxis_title="价格 (¥)",
        xaxis_title="日期",
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 成交量图表
    if volume_col in stock_data.columns:
        fig_volume = px.bar(
            x=stock_data.index if date_col not in stock_data.columns else stock_data[date_col],
            y=stock_data[volume_col],
            title=f"{ticker} 成交量"
        )
        fig_volume.update_layout(height=300)
        st.plotly_chart(fig_volume, use_container_width=True)

def display_news_summary(news_data):
    """显示新闻摘要"""
    st.subheader("📰 相关新闻")
    
    if news_data:
        st.text_area("新闻内容", news_data, height=300)
    else:
        st.info("暂无相关新闻")

def display_data_source_status(ticker):
    """显示数据源状态"""
    try:
        data_manager = EnhancedDataSourceManager()
        quality_report = data_manager.get_data_quality_report(ticker)
        
        st.subheader(f"📊 {ticker} 数据源质量报告")
        
        # 整体质量
        quality = quality_report["overall_quality"]
        if quality == "excellent":
            st.success(f"整体数据质量: {quality} ✅")
        elif quality == "good":
            st.info(f"整体数据质量: {quality} ℹ️")
        else:
            st.warning(f"整体数据质量: {quality} ⚠️")
        
        # 详细状态
        st.subheader("详细数据源状态")
        
        for data_type, sources in quality_report["data_sources"].items():
            st.write(f"**{data_type}**:")
            for source, status in sources.items():
                if status == "available":
                    st.success(f"  ✅ {source}: 可用")
                elif status == "no_data":
                    st.warning(f"  ⚠️ {source}: 无数据")
                elif status.startswith("error"):
                    st.error(f"  ❌ {source}: {status}")
                else:
                    st.info(f"  ℹ️ {source}: {status}")
    
    except Exception as e:
        st.error(f"获取数据源状态失败: {e}")



def display_system_status():
    """显示系统状态"""
    st.subheader("🖥️ 系统配置状态")
    
    # 配置信息
    config_data = {
        "LLM提供商": DEFAULT_CONFIG["llm_provider"],
        "深度思考模型": DEFAULT_CONFIG["deep_think_llm"],
        "快速思考模型": DEFAULT_CONFIG["quick_think_llm"],
        "在线工具": "启用" if DEFAULT_CONFIG["online_tools"] else "禁用",
        "最大辩论轮数": DEFAULT_CONFIG["max_debate_rounds"],
        "最大风险讨论轮数": DEFAULT_CONFIG["max_risk_discuss_rounds"]
    }
    
    for key, value in config_data.items():
        st.write(f"**{key}**: {value}")
    
    # API密钥状态
    st.subheader("🔑 API密钥状态")
    
    api_keys = {
        "OpenRouter": DEFAULT_CONFIG.get("openrouter_api_key"),
        "Groq": DEFAULT_CONFIG.get("groq_api_key"),
        "Together": DEFAULT_CONFIG.get("together_api_key"),
        "Google": DEFAULT_CONFIG.get("google_api_key"),
        "Finnhub": DEFAULT_CONFIG.get("finnhub_api_key")
    }
    
    for service, key in api_keys.items():
        if key:
            st.success(f"✅ {service}: 已配置")
        else:
            st.warning(f"⚠️ {service}: 未配置")

if __name__ == "__main__":
    main()
