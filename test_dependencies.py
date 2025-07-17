#!/usr/bin/env python3
"""
Test script to verify all dependencies are correctly installed
"""

import sys
import importlib
from typing import List, Tuple

def test_import(module_name: str, package_name: str = None) -> Tuple[bool, str]:
    """Test if a module can be imported"""
    try:
        importlib.import_module(module_name)
        return True, f"✓ {package_name or module_name}"
    except ImportError as e:
        return False, f"✗ {package_name or module_name}: {e}"

def test_dependencies():
    """Test all required dependencies"""
    
    print("=== Dependency Import Test ===\n")
    
    # Core dependencies
    dependencies = [
        # LangChain ecosystem
        ("langchain_openai", "langchain-openai"),
        ("langchain_experimental", "langchain-experimental"),
        ("langchain_anthropic", "langchain-anthropic"),
        ("langchain_google_genai", "langchain-google-genai"),
        ("langgraph", "langgraph"),
        
        # Data processing
        ("pandas", "pandas"),
        ("numpy", "numpy"),  # Usually comes with pandas
        
        # Financial data sources
        ("yfinance", "yfinance"),
        ("akshare", "akshare"),
        ("tushare", "tushare"),
        ("finnhub", "finnhub-python"),
        
        # Web scraping and parsing
        ("requests", "requests"),
        ("parsel", "parsel"),
        ("feedparser", "feedparser"),
        
        # Reddit API
        ("praw", "praw"),
        
        # Technical analysis
        ("stockstats", "stockstats"),
        ("backtrader", "backtrader"),
        
        # Database and storage
        ("chromadb", "chromadb"),
        ("redis", "redis"),
        
        # CLI and UI
        ("typer", "typer"),
        ("rich", "rich"),
        ("questionary", "questionary"),
        ("chainlit", "chainlit"),
        
        # Utilities
        ("tqdm", "tqdm"),
        ("pytz", "pytz"),
        ("dotenv", "python-dotenv"),
        ("typing_extensions", "typing-extensions"),
        
        # Other
        ("eodhd", "eodhd"),
        ("setuptools", "setuptools"),
    ]
    
    passed = 0
    failed = 0
    failed_imports = []
    
    for module_name, package_name in dependencies:
        success, message = test_import(module_name, package_name)
        print(message)
        
        if success:
            passed += 1
        else:
            failed += 1
            failed_imports.append(package_name)
    
    print(f"\n=== Results ===")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Total: {passed + failed}")
    
    if failed_imports:
        print(f"\nFailed imports: {', '.join(failed_imports)}")
        print("\nTo install missing dependencies:")
        print(f"pip install {' '.join(failed_imports)}")
    
    return failed == 0

def test_tradingagents_imports():
    """Test TradingAgents specific imports"""
    
    print("\n=== TradingAgents Module Test ===\n")
    
    tradingagents_modules = [
        ("tradingagents.default_config", "DEFAULT_CONFIG"),
        ("tradingagents.agents.utils.agent_utils", "Toolkit"),
        ("tradingagents.dataflows.data_source_manager", "DataSourceManager"),
        ("tradingagents.dataflows.akshare_utils", "akshare utilities"),
        ("tradingagents.dataflows.yfin_utils", "yfinance utilities"),
        ("tradingagents.dataflows.finnhub_utils", "finnhub utilities"),
        ("tradingagents.graph.trading_graph", "TradingAgentsGraph"),
        ("cli.main", "CLI main module"),
    ]
    
    passed = 0
    failed = 0
    
    for module_name, description in tradingagents_modules:
        success, message = test_import(module_name, description)
        print(message)
        
        if success:
            passed += 1
        else:
            failed += 1
    
    print(f"\n=== TradingAgents Module Results ===")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Total: {passed + failed}")
    
    return failed == 0

def test_python_version():
    """Test Python version compatibility"""
    
    print("=== Python Version Test ===\n")
    
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version >= (3, 10):
        print("✓ Python version is compatible (>=3.10)")
        return True
    else:
        print("✗ Python version is too old (requires >=3.10)")
        return False

if __name__ == "__main__":
    print("Testing TradingAgents Dependencies and Environment\n")
    
    # Test Python version
    python_ok = test_python_version()
    
    # Test dependencies
    deps_ok = test_dependencies()
    
    # Test TradingAgents modules
    modules_ok = test_tradingagents_imports()
    
    # Overall result
    all_ok = python_ok and deps_ok and modules_ok
    
    print(f"\n=== Overall Result ===")
    print(f"{'✓ ALL TESTS PASSED' if all_ok else '✗ SOME TESTS FAILED'}")
    
    if not all_ok:
        print("\nPlease fix the issues above before running TradingAgents.")
    
    sys.exit(0 if all_ok else 1)
