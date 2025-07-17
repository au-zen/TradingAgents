import akshare as ak
import pandas as pd
from stockstats import StockDataFrame
import signal
import logging
from ..utils import formatters

# Initialize logger
logger = logging.getLogger(__name__)

class TimeoutError(Exception):
    pass

def _handle_timeout(signum, frame):
    raise TimeoutError("Function call timed out")

def get_stock_zh_a_daily(symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    获取A股历史行情数据
    :param symbol: 股票代码，如 '000001.SZ'
    :param start_date: 开始日期，如 '2020-01-01'
    :param end_date: 结束日期，如 '2021-01-01'
    :return: pd.DataFrame
    """
    stock_code = formatters.format_symbol(symbol)
    start_date_formatted = formatters.format_date(start_date)
    end_date_formatted = formatters.format_date(end_date)
    try:
        df = ak.stock_zh_a_hist(symbol=stock_code, start_date=start_date_formatted, end_date=end_date_formatted, adjust="qfq")
        df['date'] = pd.to_datetime(df['日期'])
        df.set_index('date', inplace=True)
        df.rename(columns={
            '开盘': 'open',
            '收盘': 'close',
            '最高': 'high',
            '最低': 'low',
            '成交量': 'volume'
        }, inplace=True)
        return df
    except Exception as e:
        logger.error(f"Error getting daily data for {symbol}: {e}")
        return pd.DataFrame()

def get_stock_zh_a_info(symbol: str) -> pd.DataFrame:
    """
    获取A股公司基本信息（使用东方财富接口）
    :param symbol: 股票代码，如 '000001.SZ'
    :return: pd.DataFrame
    """
    cleaned_symbol = symbol.split('.')[0]
    stock_code = formatters.format_symbol(cleaned_symbol)
    try:
        df = ak.stock_individual_info_em(symbol=stock_code)
        if df is None or df.empty:
            logger.warning(f"akshare returned no data for {symbol}")
            return pd.DataFrame()
        df = df.set_index('item').T
        df.reset_index(drop=True, inplace=True)
        return df
    except Exception as e:
        logger.error(f"Error getting info for {symbol} from Eastmoney: {e}")
        return pd.DataFrame()

def get_stock_zh_a_financial(symbol: str, period: str = "按报告期") -> pd.DataFrame:
    """Get stock financial data for a given stock symbol from Tonghuashun."""
    signal.signal(signal.SIGALRM, _handle_timeout)
    signal.alarm(60)  # Set a 60-second timeout
    try:
        stock_code = formatters.format_symbol(symbol)
        df = ak.stock_financial_abstract_ths(symbol=stock_code, indicator=period)
        signal.alarm(0)  # Disable the alarm
        return df
    except Exception as e:
        logger.error(f"Failed to get financial data for {symbol}: {e}")
        signal.alarm(0)  # Disable the alarm
        return pd.DataFrame()

def get_stock_zh_a_news(symbol: str) -> pd.DataFrame:
    """
    获取A股公司的新闻数据
    :param symbol: 股票代码, e.g., '600519.SH'
    :return: pd.DataFrame
    """
    try:
        # stock_news_em expects the full symbol with suffix
        df = ak.stock_news_em(symbol=symbol)
        df.rename(columns={'发布时间': 'datetime', '新闻标题': 'title', '新闻内容': 'content'}, inplace=True)
        df['datetime'] = pd.to_datetime(df['datetime'])
        return df[['datetime', 'title', 'content']]
    except Exception as e:
        logger.error(f"Error getting news for {symbol}: {e}")
        return pd.DataFrame()

def get_stock_zh_a_indicator(symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    获取A股技术指标（使用stockstats）
    :param symbol: 股票代码
    :param start_date: 开始日期
    :param end_date: 结束日期
    :return: pd.DataFrame
    """
    try:
        daily_df = get_stock_zh_a_daily(symbol, start_date, end_date)
        if daily_df.empty:
            return pd.DataFrame()
        stock = StockDataFrame.retype(daily_df)
        # stockstats calculates indicators on access, so we just return the object.
        # The user can access indicators like stock['macd'], stock['rsi_14'], etc.
        return stock
    except Exception as e:
        logger.error(f"Error getting indicators for {symbol}: {e}")
        return pd.DataFrame()

def get_stock_individual_info_em(symbol: str, timeout: float = None) -> pd.DataFrame:
    """
    东方财富-个股-股票信息
    :param symbol: 股票代码, e.g., '600519.SH'
    :return: pd.DataFrame
    """
    # akshare expects the symbol without the exchange suffix, e.g., '600519' instead of '600519.SH'
    cleaned_symbol = symbol.split('.')[0]
    stock_code = formatters.format_symbol(cleaned_symbol)
    return ak.stock_individual_info_em(symbol=stock_code, timeout=timeout)

def get_stock_individual_basic_info_xq(symbol: str, token: str = None, timeout: float = None) -> pd.DataFrame:
    """
    雪球财经-个股-公司概况-公司简介
    :param symbol: 股票代码, e.g., 'SH600519'
    :return: pd.DataFrame
    """
    return ak.stock_individual_basic_info_xq(symbol=symbol, token=token, timeout=timeout)

def get_stock_lhb_detail(symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    获取A股个股龙虎榜详情（遍历所有有龙虎榜的日期，合并买入/卖出明细）
    :param symbol: 股票代码, e.g., '600519.SH'
    :param start_date: 开始日期，yyyy-mm-dd
    :param end_date: 结束日期，yyyy-mm-dd
    :return: pd.DataFrame
    """
    stock_code = formatters.format_symbol(symbol)
    try:
        # 获取所有有龙虎榜详情的日期
        date_list = ak.stock_lhb_stock_detail_date_em(symbol=stock_code)
        # 过滤在日期区间内的日期
        date_list = [d for d in date_list if start_date.replace('-', '') <= d <= end_date.replace('-', '')]
        all_df = []
        for date in date_list:
            for flag in ["买入", "卖出"]:
                try:
                    df = ak.stock_lhb_stock_detail_em(symbol=stock_code, date=date, flag=flag)
                    if df is not None and not df.empty:
                        df["龙虎榜日期"] = date
                        df["买卖方向"] = flag
                        all_df.append(df)
                except Exception as e:
                    logger.warning(f"Error fetching LHB detail for {symbol} on {date} {flag}: {e}")
        if all_df:
            return pd.concat(all_df, ignore_index=True)
        return pd.DataFrame()
    except Exception as e:
        logger.error(f"Error getting LHB detail for {symbol}: {e}")
        return pd.DataFrame()

def get_stock_cg_lg(symbol: str) -> pd.DataFrame:
    """
    获取A股机构参与度（主力控盘-机构参与度）
    :param symbol: 股票代码, e.g., '600519.SH'
    :return: pd.DataFrame
    """
    stock_code = formatters.format_symbol(symbol)
    try:
        df = ak.stock_comment_detail_zlkp_jgcyd_em(symbol=stock_code)
        return df
    except Exception as e:
        logger.error(f"Error getting institutional participation for {symbol}: {e}")
        return pd.DataFrame()

def get_stock_dzjy_detail(symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    获取A股大宗交易每日明细
    :param symbol: 股票代码, e.g., '600519.SH'
    :return: pd.DataFrame
    """
    stock_code = formatters.format_symbol(symbol)
    start_date_formatted = formatters.format_date(start_date)
    end_date_formatted = formatters.format_date(end_date)
    try:
        df = ak.stock_dzjy_mrmx(symbol="A股", start_date=start_date_formatted, end_date=end_date_formatted)
        # 用 '证券代码' 字段筛选目标股票
        df = df[df["证券代码"] == stock_code]
        return df
    except Exception as e:
        logger.error(f"Error getting block trade detail for {symbol}: {e}")
        return pd.DataFrame()

def get_stock_report(symbol: str) -> pd.DataFrame:
    """
    获取A股分析师报告/研报
    :param symbol: 股票代码, e.g., '600519.SH'
    :return: pd.DataFrame
    """
    stock_code = formatters.format_symbol(symbol)
    try:
        df = ak.stock_research_report_em(symbol=stock_code)
        return df
    except Exception as e:
        logger.error(f"Error getting research report for {symbol}: {e}")
        return pd.DataFrame()

def get_stock_comment_detail(symbol: str) -> pd.DataFrame:
    """
    获取A股评论/观点
    :param symbol: 股票代码, e.g., '600519.SH'
    :return: pd.DataFrame
    """
    stock_code = formatters.format_symbol(symbol)
    return ak.stock_comment_detail_scrd(symbol=stock_code)

def llm_summarize_event(text: str, llm=None) -> str:
    """
    公告/新闻等文本的LLM智能解读（摘要、分类、影响分析）
    :param text: 原文文本
    :param llm: 可选，LLM对象
    :return: 智能摘要/解读
    """
    # This is a placeholder for a real LLM call
    return f"Summary of: {text[:100]}..."
    if llm is not None:
        return llm.summarize(text)
    # 预留接口，实际可用本地Ollama等
    return "[LLM智能解读功能未启用]" 