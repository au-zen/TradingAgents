#!/usr/bin/env python3
"""
Test script to verify Ollama embedding model configuration
"""

import os
import sys
from openai import OpenAI

def test_ollama_embedding():
    """Test Ollama embedding model"""
    
    # Configure for Ollama
    config = {
        "backend_url": "http://localhost:11434/v1",
        "embedding_model": "nomic-embed-text:latest"
    }
    
    try:
        # Initialize OpenAI client with Ollama backend
        # Ollama doesn't require a real API key, so we use a dummy one
        client = OpenAI(
            base_url=config["backend_url"],
            api_key="ollama"  # Dummy API key for Ollama
        )
        
        # Test text for embedding
        test_text = "This is a test sentence for embedding generation."
        
        print(f"Testing Ollama embedding with model: {config['embedding_model']}")
        print(f"Test text: {test_text}")
        
        # Generate embedding
        response = client.embeddings.create(
            model=config["embedding_model"],
            input=test_text
        )
        
        embedding = response.data[0].embedding
        
        print(f"✅ Success! Generated embedding with {len(embedding)} dimensions")
        print(f"First 5 values: {embedding[:5]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing Ollama embedding: {e}")
        print("\nTroubleshooting tips:")
        print("1. Make sure Ollama is running: ollama serve")
        print("2. Pull the model: ollama pull nomic-embed-text:latest")
        print("3. Check if the model is available: ollama list")
        return False

def test_openai_embedding():
    """Test OpenAI embedding model as fallback"""
    
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY not set, skipping OpenAI embedding test")
        return False
    
    config = {
        "backend_url": "https://api.openai.com/v1",
        "embedding_model": "text-embedding-ada-002"
    }
    
    try:
        client = OpenAI(base_url=config["backend_url"])
        
        test_text = "This is a test sentence for embedding generation."
        
        print(f"Testing OpenAI embedding with model: {config['embedding_model']}")
        print(f"Test text: {test_text}")
        
        response = client.embeddings.create(
            model=config["embedding_model"],
            input=test_text
        )
        
        embedding = response.data[0].embedding
        
        print(f"✅ Success! Generated embedding with {len(embedding)} dimensions")
        print(f"First 5 values: {embedding[:5]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing OpenAI embedding: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing TradingAgents Embedding Configuration")
    print("=" * 50)
    
    # Test Ollama first
    print("\n1. Testing Ollama embedding...")
    ollama_success = test_ollama_embedding()
    
    # Test OpenAI as fallback
    print("\n2. Testing OpenAI embedding...")
    openai_success = test_openai_embedding()
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print(f"Ollama embedding: {'✅ PASS' if ollama_success else '❌ FAIL'}")
    print(f"OpenAI embedding: {'✅ PASS' if openai_success else '❌ FAIL'}")
    
    if ollama_success:
        print("\n🎉 Ollama embedding is working correctly!")
        print("You can now use TradingAgents with local models.")
    elif openai_success:
        print("\n⚠️  Ollama not available, but OpenAI embedding works.")
        print("Consider setting up Ollama for local development.")
    else:
        print("\n❌ No embedding models are working.")
        print("Please check your configuration and API keys.")
        sys.exit(1) 