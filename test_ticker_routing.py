#!/usr/bin/env python3
"""
Test script to verify ticker routing logic for A-shares and US stocks
"""

from tradingagents.agents.utils.agent_utils import Toolkit
from tradingagents.dataflows.data_source_manager import DataSourceManager

def test_ticker_routing():
    """Test ticker routing for various ticker formats"""
    
    # Test cases: (ticker, expected_market, expected_is_china_stock)
    test_cases = [
        # A-share tickers
        ("603127.SH", "cn_market", True),
        ("000001.SZ", "cn_market", True),
        ("603127.sh", "cn_market", True),  # lowercase
        ("000001.sz", "cn_market", True),  # lowercase
        
        # US stock tickers
        ("SPY", "us_market", False),
        ("AAPL", "us_market", False),
        ("NVDA", "us_market", False),
        ("TSLA", "us_market", False),
        ("MSFT", "us_market", False),
        
        # US stock tickers with explicit suffixes
        ("AAPL:US", "us_market", False),
        ("SPY.NYSE", "us_market", False),
        ("NVDA.NASDAQ", "us_market", False),
        
        # Edge cases
        ("BRK.A", "us_market", False),  # Berkshire Hathaway Class A
        ("BRK.B", "us_market", False),  # Berkshire Hathaway Class B
    ]
    
    data_manager = DataSourceManager()
    
    print("=== Ticker Routing Test Results ===\n")
    
    all_passed = True
    
    for ticker, expected_market, expected_is_china in test_cases:
        # Test Toolkit.ticker_is_china_stock
        is_china_result = Toolkit.ticker_is_china_stock(ticker)
        
        # Test DataSourceManager.get_market_for_symbol
        market_result = data_manager.get_market_for_symbol(ticker)
        
        # Check results
        toolkit_passed = is_china_result == expected_is_china
        market_passed = market_result == expected_market
        
        status = "✓ PASS" if (toolkit_passed and market_passed) else "✗ FAIL"
        
        print(f"{status} {ticker:12} | Market: {market_result:10} | Is China: {is_china_result:5} | Expected: {expected_market:10}/{expected_is_china}")
        
        if not (toolkit_passed and market_passed):
            all_passed = False
            if not toolkit_passed:
                print(f"      Toolkit error: expected {expected_is_china}, got {is_china_result}")
            if not market_passed:
                print(f"      Market error: expected {expected_market}, got {market_result}")
    
    print(f"\n=== Overall Result: {'✓ ALL TESTS PASSED' if all_passed else '✗ SOME TESTS FAILED'} ===")
    
    return all_passed

def test_data_source_selection():
    """Test data source selection for different markets"""
    
    print("\n=== Data Source Selection Test ===\n")
    
    data_manager = DataSourceManager()
    
    # Test A-share data sources
    cn_sources = data_manager.get_data_sources_for_market("cn_market")
    print(f"A-share (cn_market) data sources: {cn_sources}")
    
    # Test US stock data sources
    us_sources = data_manager.get_data_sources_for_market("us_market")
    print(f"US stock (us_market) data sources: {us_sources}")
    
    # Test specific ticker data source selection
    test_tickers = ["603127.SH", "SPY", "AAPL"]
    
    for ticker in test_tickers:
        market = data_manager.get_market_for_symbol(ticker)
        if market:
            sources = data_manager.get_data_sources_for_market(market)
            print(f"{ticker:12} -> {market:10} -> {sources}")
        else:
            print(f"{ticker:12} -> Unknown market")

if __name__ == "__main__":
    # Run ticker routing tests
    routing_passed = test_ticker_routing()
    
    # Run data source selection tests
    test_data_source_selection()
    
    # Exit with appropriate code
    exit(0 if routing_passed else 1)
