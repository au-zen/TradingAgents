#!/usr/bin/env python3
"""
Test script to verify TradingAgents can initialize with Ollama
"""

from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

def test_tradingagents_ollama():
    """Test TradingAgents initialization with Ollama"""
    
    # Create config for Ollama
    config = DEFAULT_CONFIG.copy()
    config["llm_provider"] = "ollama"
    config["backend_url"] = "http://localhost:11434/v1"
    config["deep_think_llm"] = "llama3.1"
    config["quick_think_llm"] = "qwen3"
    
    try:
        print("🧪 Testing TradingAgents with Ollama...")
        print(f"Backend URL: {config['backend_url']}")
        print(f"Deep thinking LLM: {config['deep_think_llm']}")
        print(f"Quick thinking LLM: {config['quick_think_llm']}")
        
        # Initialize TradingAgents
        ta = TradingAgentsGraph(debug=True, config=config)
        
        print("✅ TradingAgents initialized successfully!")
        print("✅ Ollama configuration is working correctly!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error initializing TradingAgents with Ollama: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing TradingAgents Ollama Integration")
    print("=" * 50)
    
    success = test_tradingagents_ollama()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 TradingAgents is ready to use with Ollama!")
        print("You can now run: python -m cli.main")
        print("And select 'Ollama' as your LLM provider.")
    else:
        print("❌ TradingAgents initialization failed.")
        print("Please check your Ollama setup and try again.") 