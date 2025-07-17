#!/usr/bin/env python3
"""
Test script to verify all fixes for the TradingAgents issues
"""

import sys
import os
from tradingagents.agents.utils.agent_utils import Toolkit
from tradingagents.default_config import DEFAULT_CONFIG

def test_company_name_extraction():
    """Test that get_stock_individual_info correctly extracts company name"""
    
    print("=== Company Name Extraction Test ===\n")
    
    toolkit = Toolkit(config=DEFAULT_CONFIG)
    
    # Test A-share ticker
    ticker = "603127.SH"
    print(f"Testing ticker: {ticker}")
    
    try:
        result = toolkit.get_stock_individual_info.invoke({"ticker": ticker})
        print(f"Raw result:\n{result}\n")
        
        # Parse company name
        lines = result.split('\n')
        company_name = None
        for line in lines:
            if line.startswith("公司名称:"):
                company_name = line.replace("公司名称:", "").strip()
                break
        
        if company_name:
            print(f"✓ Successfully extracted company name: {company_name}")
            if "昭衍新药" in company_name:
                print("✓ Company name is correct (昭衍新药)")
                return True
            else:
                print(f"✗ Company name seems incorrect: {company_name}")
                return False
        else:
            print("✗ Failed to extract company name")
            return False
            
    except Exception as e:
        print(f"✗ Error testing company name extraction: {e}")
        return False

def test_analyst_prompts():
    """Test that analyst prompts require Chinese output"""
    
    print("\n=== Analyst Prompts Language Test ===\n")
    
    # Check key analyst files for Chinese language requirements
    analyst_files = [
        "tradingagents/agents/analysts/market_analyst.py",
        "tradingagents/agents/analysts/social_media_analyst.py", 
        "tradingagents/agents/analysts/news_analyst.py",
        "tradingagents/agents/analysts/fundamentals_analyst.py",
        "tradingagents/agents/researchers/bull_researcher.py",
        "tradingagents/agents/researchers/bear_researcher.py",
        "tradingagents/agents/managers/research_manager.py",
        "tradingagents/agents/managers/risk_manager.py",
        "tradingagents/agents/risk_mgmt/aggresive_debator.py",
        "tradingagents/agents/risk_mgmt/conservative_debator.py",
        "tradingagents/agents/risk_mgmt/neutral_debator.py",
    ]
    
    chinese_requirements = [
        "简体中文",
        "中文",
        "必须完全使用简体中文",
        "你的所有分析和论证必须完全使用简体中文"
    ]
    
    all_passed = True
    
    for file_path in analyst_files:
        print(f"Checking {file_path}...")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            has_chinese_requirement = any(req in content for req in chinese_requirements)
            
            if has_chinese_requirement:
                print(f"  ✓ Contains Chinese language requirement")
            else:
                print(f"  ✗ Missing Chinese language requirement")
                all_passed = False
                
        except Exception as e:
            print(f"  ✗ Error reading file: {e}")
            all_passed = False
    
    return all_passed

def test_state_structure():
    """Test that AgentState includes both ticker and company_name fields"""
    
    print("\n=== State Structure Test ===\n")
    
    try:
        from tradingagents.agents.utils.agent_states import AgentState
        
        # Check if AgentState has the required annotations
        annotations = getattr(AgentState, '__annotations__', {})
        
        required_fields = ['company_of_interest', 'company_name']
        missing_fields = []
        
        for field in required_fields:
            if field in annotations:
                print(f"✓ AgentState has {field} field")
            else:
                print(f"✗ AgentState missing {field} field")
                missing_fields.append(field)
        
        if not missing_fields:
            print("✓ AgentState structure is correct")
            return True
        else:
            print(f"✗ AgentState missing fields: {missing_fields}")
            return False
            
    except Exception as e:
        print(f"✗ Error testing state structure: {e}")
        return False

def test_cli_parameter_passing():
    """Test that CLI correctly handles company name parameter"""
    
    print("\n=== CLI Parameter Passing Test ===\n")
    
    try:
        # Check if CLI main.py has the correct parameter passing
        with open("cli/main.py", 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for correct company name handling
        if 'initial_state["company_name"] = selections["company_name"]' in content:
            print("✓ CLI correctly sets company_name in initial state")
            return True
        else:
            print("✗ CLI does not correctly set company_name in initial state")
            return False
            
    except Exception as e:
        print(f"✗ Error testing CLI parameter passing: {e}")
        return False

def test_toolkit_invoke_calls():
    """Test that analyst files use correct .invoke() syntax"""
    
    print("\n=== Toolkit Invoke Calls Test ===\n")
    
    analyst_files = [
        "tradingagents/agents/analysts/market_analyst.py",
        "tradingagents/agents/analysts/social_media_analyst.py", 
        "tradingagents/agents/analysts/news_analyst.py",
        "tradingagents/agents/analysts/fundamentals_analyst.py",
    ]
    
    all_passed = True
    
    for file_path in analyst_files:
        print(f"Checking {file_path}...")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for correct invoke syntax
            if 'get_stock_individual_info.invoke({"ticker": ticker})' in content:
                print(f"  ✓ Uses correct .invoke() syntax")
            elif 'get_stock_individual_info(ticker)' in content:
                print(f"  ✗ Uses incorrect direct call syntax")
                all_passed = False
            else:
                print(f"  ? No get_stock_individual_info call found")
                
        except Exception as e:
            print(f"  ✗ Error reading file: {e}")
            all_passed = False
    
    return all_passed

def main():
    """Run all verification tests"""
    
    print("TradingAgents Fixes Verification\n")
    print("=" * 50)
    
    tests = [
        ("Company Name Extraction", test_company_name_extraction),
        ("Analyst Prompts Language", test_analyst_prompts),
        ("State Structure", test_state_structure),
        ("CLI Parameter Passing", test_cli_parameter_passing),
        ("Toolkit Invoke Calls", test_toolkit_invoke_calls),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("VERIFICATION SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All fixes verified successfully!")
        return 0
    else:
        print("❌ Some issues remain to be fixed.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
