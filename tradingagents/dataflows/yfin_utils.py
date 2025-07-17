# gets data/stats

import yfinance as yf
from typing import Annotated, Callable, Any, Optional
from pandas import DataFrame
import pandas as pd
from functools import wraps

from .utils import save_output, SavePathType, decorate_all_methods


def init_ticker(func: Callable) -> Callable:
    """Decorator to initialize yf.Ticker and pass it to the function."""

    @wraps(func)
    def wrapper(self, symbol: Annotated[str, "ticker symbol"], *args, **kwargs) -> Any:
        ticker = yf.Ticker(symbol)
        return func(self, ticker, *args, **kwargs)

    return wrapper


@decorate_all_methods(init_ticker)
class YFinanceUtils:

    def get_stock_data(
        self,
        ticker,  # This is now a yf.Ticker object from the decorator
        start_date: Annotated[
            str, "start date for retrieving stock price data, YYYY-mm-dd"
        ],
        end_date: Annotated[
            str, "end date for retrieving stock price data, YYYY-mm-dd"
        ],
        save_path: SavePathType = None,
    ) -> DataFrame:
        """retrieve stock price data for designated ticker symbol"""
        # add one day to the end_date so that the data range is inclusive
        end_date = pd.to_datetime(end_date) + pd.DateOffset(days=1)
        end_date = end_date.strftime("%Y-%m-%d")
        stock_data = ticker.history(start=start_date, end=end_date)
        # save_output(stock_data, f"Stock data for {ticker.ticker}", save_path)
        return stock_data

    def get_stock_info(
        self,
        ticker,  # This is now a yf.Ticker object from the decorator
    ) -> dict:
        """Fetches and returns latest stock information."""
        stock_info = ticker.info
        return stock_info

    def get_company_info(
        self,
        ticker,  # This is now a yf.Ticker object from the decorator
        save_path: Optional[str] = None,
    ) -> DataFrame:
        """Fetches and returns company information as a DataFrame."""
        info = ticker.info
        company_info = {
            "Company Name": info.get("shortName", "N/A"),
            "Industry": info.get("industry", "N/A"),
            "Sector": info.get("sector", "N/A"),
            "Country": info.get("country", "N/A"),
            "Website": info.get("website", "N/A"),
        }
        company_info_df = DataFrame([company_info])
        if save_path:
            company_info_df.to_csv(save_path)
            print(f"Company info for {ticker.ticker} saved to {save_path}")
        return company_info_df

    def get_stock_dividends(
        self,
        ticker,  # This is now a yf.Ticker object from the decorator
        save_path: Optional[str] = None,
    ) -> DataFrame:
        """Fetches and returns the latest dividends data as a DataFrame."""
        dividends = ticker.dividends
        if save_path:
            dividends.to_csv(save_path)
            print(f"Dividends for {ticker.ticker} saved to {save_path}")
        return dividends

    def get_income_stmt(self, ticker) -> DataFrame:
        """Fetches and returns the latest income statement of the company as a DataFrame."""
        income_stmt = ticker.financials
        return income_stmt

    def get_balance_sheet(self, ticker) -> DataFrame:
        """Fetches and returns the latest balance sheet of the company as a DataFrame."""
        balance_sheet = ticker.balance_sheet
        return balance_sheet

    def get_cash_flow(self, ticker) -> DataFrame:
        """Fetches and returns the latest cash flow statement of the company as a DataFrame."""
        cash_flow = ticker.cashflow
        return cash_flow

    def get_analyst_recommendations(self, ticker) -> tuple:
        """Fetches the latest analyst recommendations and returns the most common recommendation and its count."""
        recommendations = ticker.recommendations
        if recommendations.empty:
            return None, 0  # No recommendations available

        # Assuming 'period' column exists and needs to be excluded
        row_0 = recommendations.iloc[0, 1:]  # Exclude 'period' column if necessary

        # Find the maximum voting result
        max_votes = row_0.max()
        majority_voting_result = row_0[row_0 == max_votes].index.tolist()

        return majority_voting_result[0], max_votes


# Module-level functions for compatibility with DataSourceManager
_utils_instance = YFinanceUtils()

def get_stock_data(symbol: str, start_date: str, end_date: str) -> DataFrame:
    """Module-level wrapper for YFinanceUtils.get_stock_data"""
    return _utils_instance.get_stock_data(symbol, start_date, end_date)

def get_company_info(symbol: str) -> DataFrame:
    """Module-level wrapper for YFinanceUtils.get_company_info"""
    return _utils_instance.get_company_info(symbol)

def get_financial_data(symbol: str, report_type: str) -> DataFrame:
    """Module-level wrapper for financial data (using income statement as default)"""
    if report_type.lower() in ["annual", "yearly"]:
        return _utils_instance.get_income_stmt(symbol)
    else:
        # For quarterly or other types, also return income statement
        # This could be extended to handle different financial statement types
        return _utils_instance.get_income_stmt(symbol)

def get_company_news(symbol: str, start_date: str, end_date: str) -> list:
    """Module-level wrapper for company news (placeholder implementation)"""
    # Note: yfinance doesn't have a direct news API
    # This is a placeholder that returns empty list
    # In a real implementation, you might use a different news API
    return []
