#!/usr/bin/env python3
"""
Test script to verify improved error handling and logging
"""

import logging
import sys
from tradingagents.dataflows.data_source_manager import DataSourceManager

# Configure logging to see the improved error handling
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def test_error_handling():
    """Test error handling with various scenarios"""
    
    print("=== Error Handling and Logging Test ===\n")
    
    data_manager = DataSourceManager()
    
    # Test 1: Valid A-share ticker
    print("1. Testing valid A-share ticker (603127.SH):")
    try:
        result = data_manager.get_stock_data("603127.SH", "2024-01-01", "2024-01-05")
        if result is not None and not result.empty:
            print(f"   ✓ SUCCESS: Retrieved {len(result)} rows")
        else:
            print("   ⚠ WARNING: No data returned")
    except Exception as e:
        print(f"   ✗ ERROR: {e}")
    print()
    
    # Test 2: Valid US stock ticker (may hit rate limits)
    print("2. Testing valid US stock ticker (SPY):")
    try:
        result = data_manager.get_stock_data("SPY", "2024-01-01", "2024-01-05")
        if result is not None and not result.empty:
            print(f"   ✓ SUCCESS: Retrieved {len(result)} rows")
        else:
            print("   ⚠ WARNING: No data returned")
    except Exception as e:
        print(f"   ⚠ EXPECTED ERROR (rate limits): {e}")
    print()
    
    # Test 3: Invalid ticker symbol
    print("3. Testing invalid ticker symbol (INVALID123):")
    try:
        result = data_manager.get_stock_data("INVALID123", "2024-01-01", "2024-01-05")
        print(f"   ⚠ UNEXPECTED: Got data for invalid ticker")
    except Exception as e:
        print(f"   ✓ EXPECTED ERROR: {e}")
    print()
    
    # Test 4: Unknown market ticker
    print("4. Testing unknown market ticker format:")
    try:
        result = data_manager.get_stock_data("UNKNOWN.MARKET", "2024-01-01", "2024-01-05")
        print(f"   ⚠ UNEXPECTED: Got data for unknown market")
    except Exception as e:
        print(f"   ✓ EXPECTED ERROR: {e}")
    print()
    
    # Test 5: Company info for A-share
    print("5. Testing company info for A-share (603127.SH):")
    try:
        result = data_manager.get_stock_info("603127.SH")
        if result is not None:
            print(f"   ✓ SUCCESS: Retrieved company info")
        else:
            print("   ⚠ WARNING: No company info returned")
    except Exception as e:
        print(f"   ✗ ERROR: {e}")
    print()
    
    # Test 6: Company info for US stock
    print("6. Testing company info for US stock (SPY):")
    try:
        result = data_manager.get_stock_info("SPY")
        if result is not None:
            print(f"   ✓ SUCCESS: Retrieved company info")
        else:
            print("   ⚠ WARNING: No company info returned")
    except Exception as e:
        print(f"   ⚠ EXPECTED ERROR (rate limits or placeholder): {e}")
    print()

def test_market_detection():
    """Test market detection logic"""
    
    print("=== Market Detection Test ===\n")
    
    data_manager = DataSourceManager()
    
    test_cases = [
        ("603127.SH", "cn_market"),
        ("000001.SZ", "cn_market"),
        ("SPY", "us_market"),
        ("AAPL", "us_market"),
        ("NVDA.NASDAQ", "us_market"),
        ("MSFT:US", "us_market"),
    ]
    
    for ticker, expected_market in test_cases:
        detected_market = data_manager.get_market_for_symbol(ticker)
        status = "✓" if detected_market == expected_market else "✗"
        print(f"{status} {ticker:12} -> {detected_market:10} (expected: {expected_market})")
    
    print()

def test_data_source_selection():
    """Test data source selection for different markets"""
    
    print("=== Data Source Selection Test ===\n")
    
    data_manager = DataSourceManager()
    
    markets = ["cn_market", "us_market"]
    
    for market in markets:
        try:
            sources = data_manager.get_data_sources_for_market(market)
            print(f"✓ {market:12} -> {sources}")
        except Exception as e:
            print(f"✗ {market:12} -> ERROR: {e}")
    
    print()

if __name__ == "__main__":
    print("Testing TradingAgents Error Handling and Logging\n")
    
    # Test market detection
    test_market_detection()
    
    # Test data source selection
    test_data_source_selection()
    
    # Test error handling
    test_error_handling()
    
    print("=== Error Handling Test Complete ===")
    print("Check the logs above to see improved error handling and logging in action.")
