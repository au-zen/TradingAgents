"""
Data source manager module for handling different market data sources
"""
from typing import Optional, Dict, List, Any
import logging
import time
try:
    import pandas as pd
except ImportError:
    raise ImportError("Please install pandas: pip install pandas>=2.0.0")

from .config import get_config
from . import akshare_utils, yfin_utils, finnhub_utils

# Configure logging
logger = logging.getLogger(__name__)
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

class DataSourceManager:
    """Manages data source selection and fallback logic based on market settings"""
    
    def __init__(self):
        self.config = get_config()
        self.market_settings = self.config["market_settings"]

    def get_market_for_symbol(self, symbol: str) -> Optional[str]:
        """Determine which market a symbol belongs to based on its suffix"""
        if symbol.upper().endswith((".SH", ".SZ")):
            return "cn_market"
        elif any(suffix in symbol.upper() for suffix in [":US", ".NYSE", ".NASDAQ"]):
            return "us_market"
        else:
            # Default to US market for symbols without specific suffixes (like SPY, AAPL, etc.)
            return "us_market"

    def get_data_sources_for_market(self, market: str) -> List[str]:
        """Get primary and backup data sources for a market"""
        if market not in self.market_settings:
            raise ValueError(f"Unsupported market: {market}")
        
        market_config = self.market_settings[market]
        sources = [market_config["primary_data_source"]]
        sources.extend(market_config["backup_data_sources"])
        return sources

    def get_stock_data(self, symbol: str, start_date: str, end_date: str) -> Optional[pd.DataFrame]:
        """Get stock data using the appropriate data source with fallback support"""
        logger.info(f"Fetching stock data for {symbol} from {start_date} to {end_date}")

        market = self.get_market_for_symbol(symbol)
        if not market:
            error_msg = f"Could not determine market for symbol: {symbol}"
            logger.error(error_msg)
            raise ValueError(error_msg)

        data_sources = self.get_data_sources_for_market(market)
        logger.info(f"Using data sources for {market}: {data_sources}")
        errors = []

        for i, source in enumerate(data_sources):
            try:
                logger.info(f"Attempting to fetch data from {source} (attempt {i+1}/{len(data_sources)})")
                start_time = time.time()

                result = None
                if source == "akshare" and market == "cn_market":
                    result = akshare_utils.get_stock_zh_a_daily(symbol, start_date, end_date)
                elif source == "finnhub":
                    # Convert dates to UTC for Finnhub
                    data_dir = self.config.get("data_cache_dir", "./data")
                    result = finnhub_utils.get_data_in_range(symbol, start_date, end_date, "stock_data", data_dir)
                elif source == "yfin":
                    result = yfin_utils.get_stock_data(symbol, start_date, end_date)

                if result is not None and not result.empty:
                    elapsed_time = time.time() - start_time
                    logger.info(f"Successfully fetched {len(result)} rows from {source} in {elapsed_time:.2f}s")
                    return result
                else:
                    logger.warning(f"No data returned from {source}")
                    errors.append(f"{source}: No data returned")

            except Exception as e:
                elapsed_time = time.time() - start_time
                error_msg = f"{source}: {str(e)}"
                logger.warning(f"Failed to fetch from {source} after {elapsed_time:.2f}s: {e}")
                errors.append(error_msg)
                continue

        error_summary = f"Failed to get data from all sources: {'; '.join(errors)}"
        logger.error(error_summary)
        raise Exception(error_summary)

    def get_stock_info(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Get company information using the appropriate data source"""
        logger.info(f"Fetching company info for {symbol}")

        market = self.get_market_for_symbol(symbol)
        if not market:
            error_msg = f"Could not determine market for symbol: {symbol}"
            logger.error(error_msg)
            raise ValueError(error_msg)

        data_sources = self.get_data_sources_for_market(market)
        logger.info(f"Using data sources for {market}: {data_sources}")
        errors = []

        for i, source in enumerate(data_sources):
            try:
                logger.info(f"Attempting to fetch company info from {source} (attempt {i+1}/{len(data_sources)})")
                start_time = time.time()

                result = None
                if source == "akshare" and market == "cn_market":
                    result = akshare_utils.get_stock_zh_a_info(symbol)
                elif source == "finnhub":
                    # Get company profile from Finnhub
                    result = finnhub_utils.get_company_profile(symbol)
                elif source == "yfin":
                    result = yfin_utils.get_company_info(symbol)

                if result is not None:
                    elapsed_time = time.time() - start_time
                    logger.info(f"Successfully fetched company info from {source} in {elapsed_time:.2f}s")
                    return result
                else:
                    logger.warning(f"No company info returned from {source}")
                    errors.append(f"{source}: No data returned")

            except Exception as e:
                elapsed_time = time.time() - start_time
                error_msg = f"{source}: {str(e)}"
                logger.warning(f"Failed to fetch company info from {source} after {elapsed_time:.2f}s: {e}")
                errors.append(error_msg)
                continue

        error_summary = f"Failed to get company info from all sources: {'; '.join(errors)}"
        logger.error(error_summary)
        raise Exception(error_summary)

    def get_stock_financials(self, symbol: str, report_type: str = "annual") -> Optional[Dict[str, Any]]:
        """Get financial reports using the appropriate data source"""
        market = self.get_market_for_symbol(symbol)
        if not market:
            raise ValueError(f"Could not determine market for symbol: {symbol}")

        data_sources = self.get_data_sources_for_market(market)
        errors = []

        for source in data_sources:
            try:
                if source == "akshare" and market == "cn_market":
                    return akshare_utils.get_stock_zh_a_financial(symbol, "年度" if report_type == "annual" else "季度")
                elif source == "finnhub":
                    # Get financial reports from Finnhub
                    return finnhub_utils.get_company_financials(symbol, report_type)
                elif source == "yfin":
                    return yfin_utils.get_financial_data(symbol, report_type)
            except Exception as e:
                errors.append(f"{source}: {str(e)}")
                continue

        raise Exception(f"Failed to get financial data from all sources: {'; '.join(errors)}")

    def get_stock_indicators(self, symbol: str, indicator: str, start_date: str, end_date: str) -> Optional[pd.DataFrame]:
        """Get technical indicators using the appropriate data source"""
        market = self.get_market_for_symbol(symbol)
        if not market:
            raise ValueError(f"Could not determine market for symbol: {symbol}")

        data_sources = self.get_data_sources_for_market(market)
        errors = []

        for source in data_sources:
            try:
                if source == "akshare" and market == "cn_market":
                    return akshare_utils.get_stock_zh_a_indicators(symbol, start_date, end_date)
                else:
                    # Fallback for other markets or if akshare fails
                    return stockstats_utils.get_stock_indicators(symbol, indicator, start_date, end_date)
            except Exception as e:
                errors.append(f"{source}: {str(e)}")
                continue

        raise Exception(f"Failed to get indicators from all sources: {'; '.join(errors)}")

    def get_market_news(self, symbol: str, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """Get market news using the appropriate data source"""
        market = self.get_market_for_symbol(symbol)
        if not market:
            raise ValueError(f"Could not determine market for symbol: {symbol}")

        data_sources = self.get_data_sources_for_market(market)
        errors = []

        for source in data_sources:
            try:
                if source == "akshare" and market == "cn_market":
                    return akshare_utils.get_stock_zh_a_news(symbol)
                elif source == "finnhub":
                    return finnhub_utils.get_company_news(symbol, start_date, end_date)
                elif source == "yfin":
                    return yfin_utils.get_company_news(symbol, start_date, end_date)
            except Exception as e:
                errors.append(f"{source}: {str(e)}")
                continue

        raise Exception(f"Failed to get news from all sources: {'; '.join(errors)}")