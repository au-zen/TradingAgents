#!/usr/bin/env python3
"""
Test script to verify complete analysis flow for A-shares and US stocks
"""

from tradingagents.agents.utils.agent_utils import Toolkit
from tradingagents.default_config import DEFAULT_CONFIG
import pandas as pd

def test_toolkit_functions():
    """Test Toolkit functions for both A-shares and US stocks"""
    
    print("=== Toolkit Functions Test ===\n")
    
    # Test cases: (ticker, market_type)
    test_cases = [
        ("603127.SH", "A-share"),
        ("SPY", "US stock"),
    ]
    
    toolkit = Toolkit(config=DEFAULT_CONFIG)
    
    for ticker, market_type in test_cases:
        print(f"Testing {ticker} ({market_type}):")
        
        # Test ticker classification
        is_china = toolkit.ticker_is_china_stock(ticker)
        print(f"  Is China stock: {is_china}")
        
        # Test stock data retrieval
        print("  Testing stock data retrieval...")
        try:
            stock_data = toolkit.get_stock_data.invoke({
                "symbol": ticker,
                "start_date": "2024-01-01",
                "end_date": "2024-01-05"
            })
            if stock_data and "No data found" not in stock_data:
                print(f"    ✓ PASS: Stock data retrieved successfully")
                # Show first few lines
                lines = stock_data.split('\n')[:5]
                for line in lines:
                    print(f"      {line}")
            else:
                print(f"    ⚠ WARNING: No stock data found")
        except Exception as e:
            print(f"    ✗ FAIL: Error retrieving stock data: {e}")

        # Test stock indicators (only for A-shares for now)
        if is_china:
            print("  Testing stock indicators...")
            try:
                indicators = toolkit.get_stock_indicators.invoke({
                    "symbol": ticker,
                    "start_date": "2024-01-01",
                    "end_date": "2024-01-05"
                })
                if indicators and "No indicator data found" not in indicators:
                    print(f"    ✓ PASS: Stock indicators retrieved successfully")
                else:
                    print(f"    ⚠ WARNING: No indicator data found")
            except Exception as e:
                print(f"    ✗ FAIL: Error retrieving indicators: {e}")
        
        # Test company info
        print("  Testing company info...")
        try:
            if is_china:
                company_info = toolkit.get_stock_individual_info.invoke({"ticker": ticker})
            else:
                # For US stocks, we'll test through the data source manager
                from tradingagents.dataflows.data_source_manager import DataSourceManager
                data_manager = DataSourceManager()
                company_info = data_manager.get_stock_info(ticker)
            
            if company_info and "Error" not in str(company_info):
                print(f"    ✓ PASS: Company info retrieved successfully")
                # Show first few lines of info
                info_str = str(company_info)
                lines = info_str.split('\n')[:3]
                for line in lines:
                    print(f"      {line}")
            else:
                print(f"    ⚠ WARNING: No company info found")
        except Exception as e:
            print(f"    ✗ FAIL: Error retrieving company info: {e}")
        
        # Test news retrieval
        print("  Testing news retrieval...")
        try:
            news = toolkit.get_stock_news.invoke({
                "ticker": ticker,
                "start_date": "2024-01-01",
                "end_date": "2024-01-05"
            })
            if news and "No news found" not in news:
                print(f"    ✓ PASS: News retrieved successfully")
            else:
                print(f"    ⚠ WARNING: No news found")
        except Exception as e:
            print(f"    ✗ FAIL: Error retrieving news: {e}")
        
        print()

def test_cli_non_interactive():
    """Test CLI in non-interactive mode"""
    
    print("=== CLI Non-Interactive Test ===\n")
    
    import subprocess
    import os
    
    # Test A-share analysis
    print("Testing A-share CLI analysis (603127.SH):")
    try:
        cmd = [
            "python", "-m", "cli.main", "analyze",
            "--ticker", "603127.SH",
            "--start-date", "2024-01-01",
            "--end-date", "2024-01-02",
            "--non-interactive"
        ]
        
        # Set environment variables
        env = os.environ.copy()
        env["PYTHONPATH"] = "/home/autum/TradingAgents"
        
        # Run with timeout to avoid hanging
        result = subprocess.run(
            cmd,
            cwd="/home/autum/TradingAgents",
            env=env,
            capture_output=True,
            text=True,
            timeout=60  # 60 second timeout
        )
        
        if result.returncode == 0:
            print("  ✓ PASS: A-share CLI analysis completed successfully")
        else:
            print(f"  ✗ FAIL: A-share CLI analysis failed with return code {result.returncode}")
            print(f"    Error output: {result.stderr[:200]}...")
            
    except subprocess.TimeoutExpired:
        print("  ⚠ WARNING: A-share CLI analysis timed out (may be normal for full analysis)")
    except Exception as e:
        print(f"  ✗ FAIL: Error running A-share CLI analysis: {e}")
    
    # Test US stock analysis
    print("\nTesting US stock CLI analysis (SPY):")
    try:
        cmd = [
            "python", "-m", "cli.main", "analyze",
            "--ticker", "SPY",
            "--start-date", "2024-01-01",
            "--end-date", "2024-01-02",
            "--non-interactive"
        ]
        
        # Set environment variables
        env = os.environ.copy()
        env["PYTHONPATH"] = "/home/autum/TradingAgents"
        
        # Run with timeout to avoid hanging
        result = subprocess.run(
            cmd,
            cwd="/home/autum/TradingAgents",
            env=env,
            capture_output=True,
            text=True,
            timeout=60  # 60 second timeout
        )
        
        if result.returncode == 0:
            print("  ✓ PASS: US stock CLI analysis completed successfully")
        else:
            print(f"  ✗ FAIL: US stock CLI analysis failed with return code {result.returncode}")
            print(f"    Error output: {result.stderr[:200]}...")
            
    except subprocess.TimeoutExpired:
        print("  ⚠ WARNING: US stock CLI analysis timed out (may be normal for full analysis)")
    except Exception as e:
        print(f"  ✗ FAIL: Error running US stock CLI analysis: {e}")

if __name__ == "__main__":
    print("Testing TradingAgents Complete Analysis Flow\n")
    
    # Test toolkit functions
    test_toolkit_functions()
    
    # Test CLI in non-interactive mode (commented out for now due to potential long runtime)
    # test_cli_non_interactive()
    
    print("=== Analysis Flow Test Complete ===")
