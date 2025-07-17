import os
from datetime import datetime, timedelta
import pandas as pd
import yfinance as yf
from stockstats import StockDataFrame
from typing import Optional, Union

def get_stock_indicators(symbol: str, start_date: str, end_date: str) -> Optional[pd.DataFrame]:
    """
    Get technical indicators for a stock using yfinance and stock-pandas.

    Args:
        symbol (str): The stock symbol.
        start_date (str): The start date in 'YYYY-MM-DD' format.
        end_date (str): The end date in 'YYYY-MM-DD' format.

    Returns:
        Optional[pd.DataFrame]: A DataFrame with technical indicators, or None if data retrieval fails.
    """
    try:
        # Download historical stock data
        data = yf.download(
            symbol,
            start=start_date,
            end=end_date,
            progress=False,
            auto_adjust=True,
        )

        if data.empty:
            return None

        # Convert to StockDataFrame
        stock_df = StockDataFrame.retype(data)

        # Calculate common technical indicators
        stock_df[['macd', 'macds', 'macdh']]
        stock_df['rsi_14']
        stock_df['boll']

        # Select relevant columns and drop rows with NaN values
        indicator_df = stock_df[['open', 'high', 'low', 'close', 'volume', 'macd', 'rsi_14', 'boll']].copy()
        indicator_df.dropna(inplace=True)

        return indicator_df

    except Exception as e:
        print(f"Error getting stock indicators for {symbol}: {e}")
        return None


class StockstatsUtils:
    """Utility functions to calculate technical indicators using `stockstats`.

    This class provides a single public static method `get_stock_stats` that
    is used by `tradingagents.dataflows.interface`.  Keeping everything inside
    a class avoids polluting the module namespace and allows for easy future
    expansion.
    """

    _DEFAULT_LOOKBACK_DAYS = 400  # days of data to download when online

    @staticmethod
    def _download_price_data(symbol: str, end_date: str, lookback_days: int | None = None) -> pd.DataFrame:
        """Download OHLCV data from Yahoo Finance and prepare columns for StockStats."""
        if lookback_days is None:
            lookback_days = StockstatsUtils._DEFAULT_LOOKBACK_DAYS

        end_dt = datetime.strptime(end_date, "%Y-%m-%d")
        start_dt = end_dt - timedelta(days=lookback_days)

        df = yf.download(
            symbol,
            start=start_dt.strftime("%Y-%m-%d"),
            end=(end_dt + timedelta(days=1)).strftime("%Y-%m-%d"),  # make *end* inclusive
            auto_adjust=True,
            progress=False,
        )
        if df.empty:
            raise ValueError(f"No online data received for {symbol} in the period {start_dt.date()} – {end_dt.date()}")

        # StockStats expects lowercase column names: open/high/low/close/volume
        df.columns = [c.lower().replace("adj close", "close") if c.lower() == "adj close" else c.lower() for c in df.columns]
        return df

    @staticmethod
    def _read_cached_price_data(symbol: str, data_dir: str) -> pd.DataFrame:
        """Read cached CSV price data created by the project (offline mode)."""
        for fname in os.listdir(data_dir):
            if fname.lower().startswith(symbol.lower()) and fname.lower().endswith(".csv"):
                df = pd.read_csv(os.path.join(data_dir, fname))
                # Ensure a proper datetime index for StockStats
                if "Date" in df.columns:
                    df["Date"] = pd.to_datetime(df["Date"])
                    df = df.set_index("Date")
                df.columns = [c.lower() for c in df.columns]
                return df
        raise FileNotFoundError(f"Cached price data for {symbol} not found in {data_dir}.")

    @staticmethod
    def _to_stockstats(df: pd.DataFrame) -> StockDataFrame:
        """Convert a pandas OHLCV dataframe into a StockDataFrame object."""
        df.index = pd.to_datetime(df.index)
        return StockDataFrame.retype(df)

    @staticmethod
    def get_stock_stats(
        symbol: str,
        indicator: str,
        date_str: str,
        data_dir: str,
        online: bool = True,
    ) -> float | str:
        """Return the *indicator* value for *symbol* on *date_str*.

        If *online* is True, fresh data is downloaded from Yahoo Finance.  When
        running offline we expect to find a cached CSV in *data_dir* (the path
        is controlled by `dataflows.config.DATA_DIR`).
        """
        # Acquire price data
        if online:
            price_df = StockstatsUtils._download_price_data(symbol, date_str)
        else:
            price_df = StockstatsUtils._read_cached_price_data(symbol, data_dir)
            # Trim to historical dates up to *date_str*
            max_date = datetime.strptime(date_str, "%Y-%m-%d")
            price_df = price_df[price_df.index <= max_date]
            if price_df.empty:
                raise ValueError(f"Offline data for {symbol} does not cover {date_str}.")

        # Compute indicators via stockstats
        ss_df = StockstatsUtils._to_stockstats(price_df)
        # Trigger calculation if not yet present
        _ = ss_df[indicator]

        # Safely extract value at (or before) date_str
        target_date = datetime.strptime(date_str, "%Y-%m-%d")
        if target_date in ss_df.index:
            value = ss_df.loc[target_date, indicator]
        else:
            # fallback: the last available value before the date
            value_series = ss_df[indicator][ss_df.index <= target_date]
            if value_series.empty:
                raise ValueError(f"Indicator {indicator} unavailable for {symbol} on {date_str}.")
            value = value_series.iloc[-1]

        return value.item() if hasattr(value, "item") else value
