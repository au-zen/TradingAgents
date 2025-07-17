from langchain_core.messages import BaseMessage, HumanMessage, ToolMessage, AIMessage
from typing import List
from typing import Annotated
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import RemoveMessage
from langchain_core.tools import tool
from datetime import date, timedelta, datetime
import functools
import pandas as pd
import os
from dateutil.relativedelta import relativedelta
from langchain_openai import ChatOpenAI
import tradingagents.dataflows.interface as interface
from tradingagents.dataflows import akshare_utils
from tradingagents.utils import formatters
from tradingagents.dataflows.data_source_manager import DataSourceManager
from tradingagents.default_config import DEFAULT_CONFIG
from langchain_core.messages import HumanMessage


def create_msg_delete():
    def delete_messages(state):
        """Clear messages and add placeholder for Anthropic compatibility"""
        messages = state["messages"]
        
        # Remove all messages
        removal_operations = [RemoveMessage(id=m.id) for m in messages]
        
        # Add a minimal placeholder message
        placeholder = HumanMessage(content="Continue")
        
        return {"messages": removal_operations + [placeholder]}
    
    return delete_messages


class Toolkit:
    _config = DEFAULT_CONFIG.copy()

    @classmethod
    def update_config(cls, config):
        """Update the class-level configuration."""
        cls._config.update(config)

    @property
    def config(self):
        """Access the configuration."""
        return self._config

    def __init__(self, config=None):
        if config:
            self.update_config(config)

    @staticmethod
    def ticker_is_china_stock(ticker: str) -> bool:
        """判断ticker是否为A股（如以.SH或.SZ结尾）"""
        return ticker.upper().endswith(('.SH', '.SZ'))

    @staticmethod
    @tool
    def get_stock_data(
        symbol: Annotated[str, "ticker symbol of the company"],
        start_date: Annotated[str, "Start date in yyyy-mm-dd format"],
        end_date: Annotated[str, "End date in yyyy-mm-dd format"],
    ) -> str:
        """
        Retrieve the stock price data for a given ticker symbol using the appropriate data source.
        """
        try:
            if Toolkit.ticker_is_china_stock(symbol):
                df = akshare_utils.get_stock_zh_a_daily(symbol, start_date, end_date)
            else:
                data_manager = DataSourceManager()
                df = data_manager.get_stock_data(symbol, start_date, end_date)
            
            if df is not None and not df.empty:
                return df.to_markdown(index=False)
            return f"No data found for {symbol} from {start_date} to {end_date}."
        except Exception as e:
            return f"Error getting stock data for {symbol}: {e}"

    @staticmethod
    @tool
    def get_stock_indicators(
        symbol: Annotated[str, "ticker symbol for the company"],
        start_date: Annotated[str, "start date for retrieving stock price data, YYYY-mm-dd"],
        end_date: Annotated[str, "end date for retrieving stock price data, YYYY-mm-dd"],
    ) -> str:
        """
        Calculate the stock statistics for a given ticker symbol and date range.
        """
        try:
            if Toolkit.ticker_is_china_stock(symbol):
                indicator_data = akshare_utils.get_stock_zh_a_indicator(symbol, start_date, end_date)
            else:
                data_manager = DataSourceManager()
                # Assuming non-A-share indicators are handled by DataSourceManager
                # This part may need a more specific implementation if DataSourceManager doesn't handle it
                return "Indicator calculation for non-A-share stocks is not fully implemented in this tool."

            if indicator_data is not None and not indicator_data.empty:
                return indicator_data.to_markdown(index=False)
            return f"No indicator data found for {symbol} from {start_date} to {end_date}."
        except Exception as e:
            return f"Error getting stock indicators for {symbol}: {e}"

    @staticmethod
    @tool
    def get_stock_individual_info(
        ticker: Annotated[str, "A-share stock ticker, e.g., '603127.SH'"],
    ) -> str:
        """
        获取A股公司基本信息（公司名称、主营业务、行业等）。
        """
        if not Toolkit.ticker_is_china_stock(ticker):
            return "Error: This tool仅支持A股。"
        try:
            df = akshare_utils.get_stock_zh_a_info(ticker)
            if df is not None and not df.empty:
                info = df.iloc[0].to_dict()
                name = info.get("股票简称") or info.get("名称") or ""
                industry = info.get("行业", "")
                ipo_date = info.get("上市时间", "")
                total_shares = info.get("总股本", "")
                business = info.get("主营业务", "")
                return (
                    f"公司名称: {name}\n"
                    f"行业: {industry}\n"
                    f"上市时间: {ipo_date}\n"
                    f"总股本: {total_shares}\n"
                    f"主营业务: {business if business else '无'}"
                )
            return f"Error: 未获取到 {ticker} 的公司基本信息。"
        except Exception as e:
            return f"Error fetching company information for {ticker}: {e}"

    @staticmethod
    @tool
    def get_stock_news(
        ticker: Annotated[str, "Search query of a company, e.g. 'AAPL' or '600519.SH'"],
        start_date: Annotated[str, "Start date in yyyy-mm-dd format"],
        end_date: Annotated[str, "End date in yyyy-mm-dd format"],
    ) -> str:
        """
        Retrieve the latest news about a given stock within a date range.
        """
        try:
            if Toolkit.ticker_is_china_stock(ticker):
                df = akshare_utils.get_stock_news(ticker, start_date, end_date)
            else:
                data_manager = DataSourceManager()
                news_list = data_manager.get_market_news(ticker, start_date, end_date)
                df = pd.DataFrame(news_list)

            if df is not None and not df.empty:
                return df.to_markdown(index=False)
            return f"No news found for {ticker} from {start_date} to {end_date}."
        except Exception as e:
            return f"Error getting news for {ticker}: {e}"

    @staticmethod
    @tool
    def get_stock_financials(
        symbol: Annotated[str, "ticker symbol of the company"],
        report_type: Annotated[str, "Type of financial report, e.g., 'annual' or 'quarterly'"],
    ) -> str:
        """
        Retrieve financial statements for a given ticker symbol.
        """
        try:
            if Toolkit.ticker_is_china_stock(symbol):
                financials = akshare_utils.get_stock_financials(symbol, report_type)
            else:
                data_manager = DataSourceManager()
                financials = data_manager.get_stock_financials(symbol, report_type)

            if financials is not None and not financials.empty:
                return financials.to_markdown(index=False)
            return f"No financial data found for {symbol} for report type {report_type}."
        except Exception as e:
            return f"Error getting financials for {symbol}: {e}"

    @staticmethod
    @tool
    def get_stock_lhb_detail(
        ticker: Annotated[str, "A-share stock ticker, e.g., '603127.SH'"],
        start_date: Annotated[str, "Start date in yyyy-mm-dd format"],
        end_date: Annotated[str, "End date in yyyy-mm-dd format"],
        limit: Annotated[int, "返回条数"] = 5,
    ) -> str:
        """
        获取A股龙虎榜详情 (LHB detail for A-shares).
        """
        if not Toolkit.ticker_is_china_stock(ticker):
            return "Error: This tool仅支持A股。"
        try:
            df = akshare_utils.get_stock_lhb_detail(ticker, start_date, end_date)
            if df is not None and not df.empty:
                df = df.head(limit)
                return df.to_markdown(index=False)
            return f"未找到 {ticker} 的龙虎榜数据。"
        except Exception as e:
            return f"Error getting LHB data for {ticker}: {e}"

    @staticmethod
    @tool
    def get_stock_cg_lg(
        ticker: Annotated[str, "A-share stock ticker, e.g., '603127.SH'"],
        limit: Annotated[int, "返回条数"] = 5,
    ) -> str:
        """
        获取A股机构持仓 (Institutional holdings for A-shares).
        """
        if not Toolkit.ticker_is_china_stock(ticker):
            return "Error: This tool仅支持A股。"
        try:
            df = akshare_utils.get_stock_cg_lg(ticker)
            if df is not None and not df.empty:
                df = df.head(limit)
                return df.to_markdown(index=False)
            return f"未找到 {ticker} 的机构持仓数据。"
        except Exception as e:
            return f"Error getting institutional holdings data for {ticker}: {e}"

    @staticmethod
    @tool
    def get_stock_dzjy_detail(
        ticker: Annotated[str, "A-share stock ticker, e.g., '603127.SH'"],
        start_date: Annotated[str, "Start date in yyyy-mm-dd format"],
        end_date: Annotated[str, "End date in yyyy-mm-dd format"],
        limit: Annotated[int, "返回条数"] = 5,
    ) -> str:
        """
        获取A股大宗交易详情 (Block trade details for A-shares).
        """
        if not Toolkit.ticker_is_china_stock(ticker):
            return "Error: This tool仅支持A股。"
        try:
            df = akshare_utils.get_stock_dzjy_detail(ticker, start_date, end_date)
            if df is not None and not df.empty:
                df = df.head(limit)
                return df.to_markdown(index=False)
            return f"未找到 {ticker} 的大宗交易数据。"
        except Exception as e:
            return f"Error getting block trade data for {ticker}: {e}"

    @staticmethod
    @tool
    def get_stock_report(
        ticker: Annotated[str, "A-share stock ticker, e.g., '603127.SH'"],
        limit: Annotated[int, "返回条数"] = 5,
    ) -> str:
        """
        获取A股研报 (Analyst reports for A-shares).
        """
        if not Toolkit.ticker_is_china_stock(ticker):
            return "Error: This tool仅支持A股。"
        try:
            df = akshare_utils.get_stock_report(ticker)
            if df is not None and not df.empty:
                df = df.head(limit)
                return df.to_markdown(index=False)
            return f"未找到 {ticker} 的分析师研报。"
        except Exception as e:
            return f"Error getting analyst reports for {ticker}: {e}"

    @staticmethod
    @tool
    def llm_summarize_event(
        text: Annotated[str, "Text to be summarized by LLM"],
    ) -> str:
        """
        Summarizes text (e.g., announcements, news) using an LLM.
        """
        # This is a placeholder for the actual LLM summarization logic.
        # You would typically call a function that interacts with an LLM service.
        try:
            return akshare_utils.llm_summarize_event(text)
        except Exception as e:
            return f"Error summarizing text: {e}"
        return llm_summarize_event(text, llm)

    @staticmethod
    @tool
    def get_stock_zh_a_news(
        ticker: Annotated[str, "A股股票代码，如'603127.SH'"],
        limit: Annotated[int, "返回新闻条数"] = 5,
    ) -> str:
        """
        获取A股个股新闻（东方财富）。
        """
        from tradingagents.dataflows.akshare_utils import get_stock_zh_a_news
        df = get_stock_zh_a_news(ticker)
        if df is not None and not df.empty:
            df = df.head(limit)
            news_list = [
                f"{row['datetime'].strftime('%Y-%m-%d %H:%M')}: {row['title']}\n{row['content']}"
                for _, row in df.iterrows()
            ]
            return "\n\n".join(news_list)
        return f"未找到A股 {ticker} 的相关新闻。"

    @staticmethod
    @tool
    def get_stock_zh_a_financial(
        ticker: Annotated[str, "A股股票代码，如'603127.SH'"],
        report_type: Annotated[str, "年度/季度"],
    ) -> str:
        """
        获取A股财务报表（新浪/东方财富）。
        """
        from tradingagents.dataflows.akshare_utils import get_stock_zh_a_financial
        df = get_stock_zh_a_financial(ticker, report_type)
        if df is not None and not df.empty:
            return df.to_markdown(index=False)
        return f"未找到A股 {ticker} 的财务数据。"

    @staticmethod
    def get_stock_news_openai(ticker: str, curr_date: str) -> str:
        """
        Wrapper for get_stock_news_openai from dataflows.interface.
        """
        from tradingagents.dataflows.interface import get_stock_news_openai as _get_stock_news_openai
        return _get_stock_news_openai(ticker, curr_date)

    @staticmethod
    def get_reddit_stock_info(ticker: str, curr_date: str, look_back_days: int = 7, max_limit_per_day: int = 10) -> str:
        """
        Wrapper for get_reddit_company_news from dataflows.interface.
        """
        from tradingagents.dataflows.interface import get_reddit_company_news as _get_reddit_company_news
        start_date = curr_date  # Use curr_date as the end of the window
        return _get_reddit_company_news(ticker, start_date, look_back_days, max_limit_per_day)

    @staticmethod
    def get_global_news_openai(curr_date: str) -> str:
        """
        Wrapper for get_global_news_openai from dataflows.interface.
        """
        from tradingagents.dataflows.interface import get_global_news_openai as _get_global_news_openai
        return _get_global_news_openai(curr_date)

    @staticmethod
    def get_google_news(query: str, curr_date: str, look_back_days: int = 7) -> str:
        """
        Wrapper for get_google_news from dataflows.interface.
        """
        from tradingagents.dataflows.interface import get_google_news as _get_google_news
        return _get_google_news(query, curr_date, look_back_days)

    @staticmethod
    def get_finnhub_news(ticker: str, curr_date: str, look_back_days: int = 7) -> str:
        """
        Wrapper for get_finnhub_news from dataflows.interface.
        """
        from tradingagents.dataflows.interface import get_finnhub_news as _get_finnhub_news
        return _get_finnhub_news(ticker, curr_date, look_back_days)

    @staticmethod
    def get_reddit_news(curr_date: str, look_back_days: int = 7, max_limit_per_day: int = 10) -> str:
        """
        Wrapper for get_reddit_global_news from dataflows.interface.
        """
        from tradingagents.dataflows.interface import get_reddit_global_news as _get_reddit_global_news
        start_date = curr_date  # Use curr_date as the end of the window
        return _get_reddit_global_news(start_date, look_back_days, max_limit_per_day)

    @staticmethod
    def get_fundamentals_openai(ticker: str, curr_date: str) -> str:
        """
        Wrapper for get_fundamentals_openai from dataflows.interface.
        """
        from tradingagents.dataflows.interface import get_fundamentals_openai as _get_fundamentals_openai
        return _get_fundamentals_openai(ticker, curr_date)

    @staticmethod
    def get_fundamentals(ticker: str, curr_date: str) -> str:
        """
        Alias for get_fundamentals_openai for compatibility.
        """
        return Toolkit.get_fundamentals_openai(ticker, curr_date)

    @staticmethod
    def get_finnhub_company_insider_sentiment(ticker: str, curr_date: str, look_back_days: int = 30) -> str:
        """
        Wrapper for get_finnhub_company_insider_sentiment from dataflows.interface. Only supports US stocks.
        """
        if Toolkit.ticker_is_china_stock(ticker):
            return "A股暂不支持公司内部人情绪数据（仅美股/Finnhub 支持）"
        from tradingagents.dataflows.interface import get_finnhub_company_insider_sentiment as _get_finnhub_company_insider_sentiment
        return _get_finnhub_company_insider_sentiment(ticker, curr_date, look_back_days)

    @staticmethod
    def get_finnhub_company_insider_transactions(ticker: str, curr_date: str, look_back_days: int = 30) -> str:
        """
        Wrapper for get_finnhub_company_insider_transactions from dataflows.interface. Only supports US stocks.
        """
        if Toolkit.ticker_is_china_stock(ticker):
            return "A股暂不支持公司内部人交易数据（仅美股/Finnhub 支持）"
        from tradingagents.dataflows.interface import get_finnhub_company_insider_transactions as _get_finnhub_company_insider_transactions
        return _get_finnhub_company_insider_transactions(ticker, curr_date, look_back_days)

    @staticmethod
    def get_simfin_balance_sheet(ticker: str, freq: str, curr_date: str) -> str:
        """
        Wrapper for get_simfin_balance_sheet from dataflows.interface. Only supports US stocks.
        """
        if Toolkit.ticker_is_china_stock(ticker):
            return "A股暂不支持SimFin资产负债表（仅美股/SimFin 支持）"
        from tradingagents.dataflows.interface import get_simfin_balance_sheet as _get_simfin_balance_sheet
        return _get_simfin_balance_sheet(ticker, freq, curr_date)

    @staticmethod
    def get_simfin_cashflow(ticker: str, freq: str, curr_date: str) -> str:
        """
        Wrapper for get_simfin_cashflow from dataflows.interface. Only supports US stocks.
        """
        if Toolkit.ticker_is_china_stock(ticker):
            return "A股暂不支持SimFin现金流量表（仅美股/SimFin 支持）"
        from tradingagents.dataflows.interface import get_simfin_cashflow as _get_simfin_cashflow
        return _get_simfin_cashflow(ticker, freq, curr_date)

    @staticmethod
    def get_simfin_income_stmt(ticker: str, freq: str, curr_date: str) -> str:
        """
        Wrapper for get_simfin_income_statements from dataflows.interface. Only supports US stocks.
        """
        if Toolkit.ticker_is_china_stock(ticker):
            return "A股暂不支持SimFin利润表（仅美股/SimFin 支持）"
        from tradingagents.dataflows.interface import get_simfin_income_statements as _get_simfin_income_statements
        return _get_simfin_income_statements(ticker, freq, curr_date)

    @staticmethod
    @tool
    def get_stock_notice_report(ticker: str) -> str:
        """
        获取A股公告（如有实现），否则返回暂不支持。
        """
        if Toolkit.ticker_is_china_stock(ticker):
            # akshare_utils 可能有 get_stock_zh_a_notice 或类似公告接口
            try:
                from tradingagents.dataflows import akshare_utils
                if hasattr(akshare_utils, 'get_stock_zh_a_notice'):
                    df = akshare_utils.get_stock_zh_a_notice(ticker)
                    if df is not None and not df.empty:
                        return df.to_markdown(index=False)
                    return f"未找到A股 {ticker} 的公告数据。"
                else:
                    return "A股公告暂不支持（akshare无公告接口）。"
            except Exception as e:
                return f"获取A股公告出错: {e}"
        return "Only US stocks notice/announcement supported or not implemented."
