def format_date(date_str: str) -> str:
    """
    Converts a date string from 'YYYY-MM-DD' to 'YYYYMMDD'.
    """
    if not isinstance(date_str, str):
        return date_str
    return date_str.replace('-', '')

def format_symbol(symbol: str) -> str:
    """
    Strips the exchange suffix (e.g., .SH, .SZ) from a stock symbol.
    """
    if not isinstance(symbol, str):
        return symbol
    return symbol.split('.')[0]
