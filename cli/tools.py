from langchain.tools import Tool
from tradingagents.dataflows import akshare_utils
from tradingagents.utils import formatters

def get_tools(ticker: str, start_date: str, end_date: str):
    """
    Factory function to create and configure tools with dynamic ticker and dates.
    """

    # Wrapper functions to format inputs before calling the actual data function
    def get_daily_data_formatted(ticker, start_date, end_date):
        return akshare_utils.get_stock_zh_a_daily(ticker, start_date, end_date)

    def get_financial_data_formatted(ticker):
        return akshare_utils.get_stock_zh_a_financial(ticker)

    def get_news_formatted(ticker):
        # News function uses the full symbol with suffix
        return akshare_utils.get_stock_zh_a_news(ticker)

    def get_indicator_formatted(ticker, start_date, end_date):
        return akshare_utils.get_stock_zh_a_indicator(ticker, start_date, end_date)

    def get_lhb_detail_formatted(ticker, start_date, end_date):
        return akshare_utils.get_stock_lhb_detail(ticker, start_date, end_date)
    
    def get_cg_lg_formatted(ticker):
        return akshare_utils.get_stock_cg_lg(ticker)

    def get_dzjy_detail_formatted(ticker, start_date, end_date):
        return akshare_utils.get_stock_dzjy_detail(ticker, start_date, end_date)

    def get_report_formatted(ticker):
        return akshare_utils.get_stock_report(ticker)

    tools = [
        Tool(
            name="get_stock_data",
            func=lambda: get_daily_data_formatted(ticker, start_date, end_date),
            description=f"Get the stock price data for {ticker} from {start_date} to {end_date}. It provides daily open, high, low, close prices and volume."
        ),
        Tool(
            name="get_stock_financial",
            func=lambda: get_financial_data_formatted(ticker),
            description=f"Get the key financial statements and indicators for {ticker}. Provides an overview of the company's financial health."
        ),
        Tool(
            name="get_stock_news",
            func=lambda: get_news_formatted(ticker),
            description=f"Get the latest news related to {ticker}. Useful for understanding market sentiment and recent developments."
        ),
        Tool(
            name="get_stock_indicator",
            func=lambda: get_indicator_formatted(ticker, start_date, end_date),
            description=f"Get technical indicators for {ticker} from {start_date} to {end_date}. Includes MACD, RSI, etc."
        ),
        Tool(
            name="get_stock_lhb_detail",
            func=lambda: get_lhb_detail_formatted(ticker, start_date, end_date),
            description=f"Get the Longhu Bang (Dragon and Tiger List) details for {ticker}, showing top trading departments."
        ),
        Tool(
            name="get_stock_cg_lg",
            func=lambda: get_cg_lg_formatted(ticker),
            description=f"Get institutional holdings (机构持股) data for {ticker}."
        ),
        Tool(
            name="get_stock_dzjy_detail",
            func=lambda: get_dzjy_detail_formatted(ticker, start_date, end_date),
            description=f"Get block trade (大宗交易) details for {ticker}."
        ),
        Tool(
            name="get_stock_report",
            func=lambda: get_report_formatted(ticker),
            description=f"Get analyst reports and ratings for {ticker}."
        ),
    ]
    return tools
