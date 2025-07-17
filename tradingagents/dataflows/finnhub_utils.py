import json
import os


def get_data_in_range(ticker, start_date, end_date, data_type, data_dir, period=None):
    """
    Gets finnhub data saved and processed on disk.
    Args:
        start_date (str): Start date in YYYY-MM-DD format.
        end_date (str): End date in YYYY-MM-DD format.
        data_type (str): Type of data from finnhub to fetch. Can be insider_trans, SEC_filings, news_data, insider_senti, or fin_as_reported.
        data_dir (str): Directory where the data is saved.
        period (str): Default to none, if there is a period specified, should be annual or quarterly.
    """

    if period:
        data_path = os.path.join(
            data_dir,
            "finnhub_data",
            data_type,
            f"{ticker}_{period}_data_formatted.json",
        )
    else:
        data_path = os.path.join(
            data_dir, "finnhub_data", data_type, f"{ticker}_data_formatted.json"
        )

    data = open(data_path, "r")
    data = json.load(data)

    # filter keys (date, str in format YYYY-MM-DD) by the date range (str, str in format YYYY-MM-DD)
    filtered_data = {}
    for key, value in data.items():
        if start_date <= key <= end_date and len(value) > 0:
            filtered_data[key] = value
    return filtered_data


def get_company_profile(symbol):
    """
    Placeholder function for getting company profile from Finnhub.
    This would typically require API calls to Finnhub.
    """
    # This is a placeholder implementation
    # In a real implementation, you would make API calls to Finnhub
    return {
        "name": f"Company {symbol}",
        "ticker": symbol,
        "exchange": "Unknown",
        "industry": "Unknown"
    }


def get_company_financials(symbol, report_type):
    """
    Placeholder function for getting company financials from Finnhub.
    This would typically require API calls to Finnhub.
    """
    # This is a placeholder implementation
    # In a real implementation, you would make API calls to Finnhub
    return {
        "symbol": symbol,
        "report_type": report_type,
        "data": "No financial data available (placeholder)"
    }


def get_company_news(symbol, start_date, end_date):
    """
    Placeholder function for getting company news from Finnhub.
    This would typically require API calls to Finnhub.
    """
    # This is a placeholder implementation
    # In a real implementation, you would make API calls to Finnhub
    return [
        {
            "headline": f"Sample news for {symbol}",
            "datetime": start_date,
            "source": "Finnhub",
            "summary": "This is a placeholder news item."
        }
    ]
