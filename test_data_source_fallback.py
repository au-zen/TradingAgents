#!/usr/bin/env python3
"""
Test script to verify data source fallback mechanisms
"""

from tradingagents.dataflows.data_source_manager import DataSourceManager
from tradingagents.default_config import DEFAULT_CONFIG
import pandas as pd

def test_data_source_configuration():
    """Test data source configuration completeness"""
    
    print("=== Data Source Configuration Test ===\n")
    
    config = DEFAULT_CONFIG
    market_settings = config.get("market_settings", {})
    
    required_markets = ["cn_market", "us_market"]
    required_fields = ["primary_data_source", "backup_data_sources"]
    
    all_passed = True
    
    for market in required_markets:
        print(f"Testing {market} configuration:")
        
        if market not in market_settings:
            print(f"  ✗ FAIL: {market} not found in market_settings")
            all_passed = False
            continue
            
        market_config = market_settings[market]
        
        for field in required_fields:
            if field not in market_config:
                print(f"  ✗ FAIL: {field} not found in {market} config")
                all_passed = False
            else:
                value = market_config[field]
                print(f"  ✓ {field}: {value}")
        
        # Check if primary data source is specified
        primary = market_config.get("primary_data_source")
        if not primary:
            print(f"  ✗ FAIL: No primary data source specified for {market}")
            all_passed = False
        
        print()
    
    return all_passed

def test_data_source_fallback():
    """Test data source fallback logic"""
    
    print("=== Data Source Fallback Test ===\n")
    
    data_manager = DataSourceManager()
    
    # Test cases: (ticker, market)
    test_cases = [
        ("603127.SH", "cn_market"),
        ("SPY", "us_market"),
        ("AAPL", "us_market"),
    ]
    
    for ticker, expected_market in test_cases:
        print(f"Testing {ticker} ({expected_market}):")
        
        # Test market detection
        detected_market = data_manager.get_market_for_symbol(ticker)
        if detected_market != expected_market:
            print(f"  ✗ FAIL: Expected {expected_market}, got {detected_market}")
            continue
        
        # Test data source selection
        data_sources = data_manager.get_data_sources_for_market(detected_market)
        print(f"  Data sources: {data_sources}")
        
        # Test actual data retrieval (with error handling)
        try:
            # Use a recent date range for testing
            start_date = "2024-01-01"
            end_date = "2024-01-10"
            
            df = data_manager.get_stock_data(ticker, start_date, end_date)
            
            if df is not None and not df.empty:
                print(f"  ✓ PASS: Successfully retrieved {len(df)} rows of data")
                print(f"    Columns: {list(df.columns)}")
            else:
                print(f"  ⚠ WARNING: No data returned (may be expected for some tickers)")
                
        except Exception as e:
            print(f"  ✗ FAIL: Error retrieving data: {e}")
        
        print()

def test_individual_data_sources():
    """Test individual data source availability"""
    
    print("=== Individual Data Source Test ===\n")
    
    # Test akshare for A-shares
    print("Testing akshare (A-shares):")
    try:
        from tradingagents.dataflows import akshare_utils
        df = akshare_utils.get_stock_zh_a_daily("603127.SH", "2024-01-01", "2024-01-05")
        if df is not None and not df.empty:
            print("  ✓ PASS: akshare working")
        else:
            print("  ⚠ WARNING: akshare returned no data")
    except Exception as e:
        print(f"  ✗ FAIL: akshare error: {e}")
    
    # Test yfinance for US stocks
    print("\nTesting yfinance (US stocks):")
    try:
        from tradingagents.dataflows import yfin_utils
        df = yfin_utils.get_stock_data("SPY", "2024-01-01", "2024-01-05")
        if df is not None and not df.empty:
            print("  ✓ PASS: yfinance working")
        else:
            print("  ⚠ WARNING: yfinance returned no data")
    except Exception as e:
        print(f"  ✗ FAIL: yfinance error: {e}")
    
    # Test finnhub for US stocks (backup)
    print("\nTesting finnhub (US stocks backup):")
    try:
        from tradingagents.dataflows import finnhub_utils
        # Note: finnhub requires API key, so this might fail
        df = finnhub_utils.get_data_in_range("SPY", "2024-01-01", "2024-01-05", "stock_data")
        if df is not None and not df.empty:
            print("  ✓ PASS: finnhub working")
        else:
            print("  ⚠ WARNING: finnhub returned no data")
    except Exception as e:
        print(f"  ⚠ EXPECTED: finnhub error (likely missing API key): {e}")

if __name__ == "__main__":
    print("Testing TradingAgents Data Source Configuration and Fallback\n")
    
    # Test configuration
    config_passed = test_data_source_configuration()
    
    # Test fallback logic
    test_data_source_fallback()
    
    # Test individual data sources
    test_individual_data_sources()
    
    print(f"\n=== Configuration Test Result: {'✓ PASSED' if config_passed else '✗ FAILED'} ===")
