import pandas as pd
import sys
import os
from tradingagents.dataflows import akshare_utils

class SuppressOutput:
    def __enter__(self):
        self.stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, type, value, traceback):
        sys.stdout.close()
        sys.stdout = self.stdout

def run_tests():
    print("--- Testing tradingagents/dataflows/akshare_utils.py ---")

    # Test Data
    test_ticker = '603127.SH'
    test_start_date = '20240101'
    test_end_date = '20240110'

    # 1. Test get_stock_zh_a_info
    print(f"\n--- 1. Testing get_stock_zh_a_info for {test_ticker} ---")
    try:
        with SuppressOutput():
            info_df = akshare_utils.get_stock_zh_a_info(test_ticker)
        print("Result:")
        print(info_df.head())
    except Exception as e:
        print(f"Error: {e}")

    # 2. Test get_stock_zh_a_financial
    print(f"\n--- 2. Testing get_stock_zh_a_financial for {test_ticker} ---")
    try:
        fin_df = akshare_utils.get_stock_zh_a_financial(test_ticker, period="按年度")
        print("Result:")
        print(fin_df.head())
    except Exception as e:
        print(f"Error: {e}")

    # 3. Test get_stock_zh_a_daily
    print(f"\n--- 3. Testing get_stock_zh_a_daily for {test_ticker} ---")
    try:
        with SuppressOutput():
            daily_df = akshare_utils.get_stock_zh_a_daily(test_ticker, start_date=test_start_date, end_date=test_end_date)
        print("Result:")
        print(daily_df.head())
    except Exception as e:
        print(f"Error: {e}")

    # 4. Test get_stock_zh_a_news
    print(f"\n--- 4. Testing get_stock_zh_a_news for {test_ticker} ---")
    try:
        with SuppressOutput():
            news_df = akshare_utils.get_stock_zh_a_news(test_ticker)
        print("Result:")
        print(news_df.head())
    except Exception as e:
        print(f"Error: {e}")

    # 5. Test get_stock_zh_a_indicator
    print(f"\n--- 5. Testing get_stock_zh_a_indicator for {test_ticker} ---")
    try:
        with SuppressOutput():
            indicator_df = akshare_utils.get_stock_zh_a_indicator(test_ticker, start_date=test_start_date, end_date=test_end_date)
        print("Result:")
        print(indicator_df.head())
    except Exception as e:
        print(f"Error: {e}")

    # 6. Test get_stock_lhb_detail
    print(f"\n--- 6. Testing get_stock_lhb_detail for {test_ticker} ---")
    try:
        with SuppressOutput():
            lhb_df = akshare_utils.get_stock_lhb_detail(test_ticker, start_date=test_start_date, end_date=test_end_date)
        print("Result:")
        print(lhb_df.head())
    except Exception as e:
        print(f"Error: {e}")

    # 7. Test get_stock_cg_lg
    print(f"\n--- 7. Testing get_stock_cg_lg for {test_ticker} ---")
    try:
        with SuppressOutput():
            cg_lg_df = akshare_utils.get_stock_cg_lg(test_ticker)
        print("Result:")
        print(cg_lg_df.head())
    except Exception as e:
        print(f"Error: {e}")

    # 8. Test get_stock_dzjy_detail
    print(f"\n--- 8. Testing get_stock_dzjy_detail for {test_ticker} ---")
    try:
        with SuppressOutput():
            dzjy_df = akshare_utils.get_stock_dzjy_detail(test_ticker, start_date=test_start_date, end_date=test_end_date)
        print("Result:")
        print(dzjy_df.head())
    except Exception as e:
        print(f"Error: {e}")

    # 9. Test get_stock_report
    print(f"\n--- 9. Testing get_stock_report for {test_ticker} ---")
    try:
        with SuppressOutput():
            report_df = akshare_utils.get_stock_report(test_ticker)
        print("Result:")
        print(report_df.head())
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_tests()
