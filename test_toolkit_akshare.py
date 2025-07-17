import sys
import os
from tradingagents.agents.utils.agent_utils import Toolkit

class SuppressOutput:
    def __enter__(self):
        self.stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')
    def __exit__(self, type, value, traceback):
        sys.stdout.close()
        sys.stdout = self.stdout

def run_toolkit_akshare_tests():
    print("--- Testing Toolkit A股相关方法 ---")
    test_ticker = '603127.SH'
    test_start_date = '2024-01-01'
    test_end_date = '2024-01-10'
    toolkit = Toolkit()

    # 1. 公司基本信息
    print(f"\n--- 1. get_stock_individual_info for {test_ticker} ---")
    try:
        print(toolkit.get_stock_individual_info.invoke({"ticker": test_ticker}))
    except Exception as e:
        print(f"Error: {e}")

    # 2. 新闻（ticker, limit）
    print(f"\n--- 2. get_stock_zh_a_news for {test_ticker} ---")
    try:
        print(toolkit.get_stock_zh_a_news.invoke({"ticker": test_ticker, "limit": 3}))
    except Exception as e:
        print(f"Error: {e}")

    # 3. 龙虎榜（ticker, start_date, end_date, limit）
    print(f"\n--- 3. get_stock_lhb_detail for {test_ticker} ---")
    try:
        print(toolkit.get_stock_lhb_detail.invoke({"ticker": test_ticker, "start_date": test_start_date, "end_date": test_end_date, "limit": 3}))
    except Exception as e:
        print(f"Error: {e}")

    # 4. 机构持仓（ticker, limit）
    print(f"\n--- 4. get_stock_cg_lg for {test_ticker} ---")
    try:
        print(toolkit.get_stock_cg_lg.invoke({"ticker": test_ticker, "limit": 3}))
    except Exception as e:
        print(f"Error: {e}")

    # 5. 大宗交易（ticker, start_date, end_date, limit）
    print(f"\n--- 5. get_stock_dzjy_detail for {test_ticker} ---")
    try:
        print(toolkit.get_stock_dzjy_detail.invoke({"ticker": test_ticker, "start_date": test_start_date, "end_date": test_end_date, "limit": 3}))
    except Exception as e:
        print(f"Error: {e}")

    # 6. 分析师报告（ticker, limit）
    print(f"\n--- 6. get_stock_report for {test_ticker} ---")
    try:
        print(toolkit.get_stock_report.invoke({"ticker": test_ticker, "limit": 3}))
    except Exception as e:
        print(f"Error: {e}")

    # 7. 财务报表（ticker, report_type）
    print(f"\n--- 7. get_stock_zh_a_financial for {test_ticker} ---")
    try:
        print(toolkit.get_stock_zh_a_financial.invoke({"ticker": test_ticker, "report_type": "按年度"}))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_toolkit_akshare_tests() 