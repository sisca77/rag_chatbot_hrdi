#!/usr/bin/env python3
"""
Test script for the RAG Chatbot HRDI
This script tests the core functionality without requiring API keys
"""

import os
import sys

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    try:
        import streamlit
        print("✓ Streamlit imported successfully")
    except ImportError as e:
        print(f"✗ Error importing Streamlit: {e}")
        return False
    
    try:
        import langchain
        print("✓ LangChain imported successfully")
    except ImportError as e:
        print(f"✗ Error importing LangChain: {e}")
        return False
    
    try:
        import chromadb
        print("✓ ChromaDB imported successfully")
    except ImportError as e:
        print(f"✗ Error importing ChromaDB: {e}")
        return False
    
    try:
        from config import Config
        print("✓ Config module imported successfully")
    except ImportError as e:
        print(f"✗ Error importing Config: {e}")
        return False
    
    try:
        from document_processor import DocumentProcessor
        print("✓ DocumentProcessor imported successfully")
    except ImportError as e:
        print(f"✗ Error importing DocumentProcessor: {e}")
        return False
    
    try:
        from chatbot import RAGChatbot
        print("✓ RAGChatbot imported successfully")
    except ImportError as e:
        print(f"✗ Error importing RAGChatbot: {e}")
        return False
    
    return True

def test_config():
    """Test configuration loading"""
    print("\nTesting configuration...")
    try:
        from config import Config
        
        # Check that config attributes exist
        assert hasattr(Config, 'OPENAI_API_KEY'), "Missing OPENAI_API_KEY"
        assert hasattr(Config, 'EMBEDDING_MODEL'), "Missing EMBEDDING_MODEL"
        assert hasattr(Config, 'LLM_MODEL'), "Missing LLM_MODEL"
        assert hasattr(Config, 'CHROMA_DB_PATH'), "Missing CHROMA_DB_PATH"
        assert hasattr(Config, 'MAX_TOKENS'), "Missing MAX_TOKENS"
        assert hasattr(Config, 'TEMPERATURE'), "Missing TEMPERATURE"
        assert hasattr(Config, 'CHUNK_SIZE'), "Missing CHUNK_SIZE"
        assert hasattr(Config, 'CHUNK_OVERLAP'), "Missing CHUNK_OVERLAP"
        
        print("✓ All configuration attributes exist")
        
        # Check default values
        print(f"  - Embedding Model: {Config.EMBEDDING_MODEL}")
        print(f"  - LLM Model: {Config.LLM_MODEL}")
        print(f"  - ChromaDB Path: {Config.CHROMA_DB_PATH}")
        print(f"  - Max Tokens: {Config.MAX_TOKENS}")
        print(f"  - Temperature: {Config.TEMPERATURE}")
        print(f"  - Chunk Size: {Config.CHUNK_SIZE}")
        print(f"  - Chunk Overlap: {Config.CHUNK_OVERLAP}")
        
        return True
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        return False

def test_file_structure():
    """Test that all required files exist"""
    print("\nTesting file structure...")
    required_files = [
        'config.py',
        'document_processor.py',
        'chatbot.py',
        'app.py',
        'requirements.txt',
        '.env.example',
        '.gitignore',
        'README.md'
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file} exists")
        else:
            print(f"✗ {file} missing")
            all_exist = False
    
    return all_exist

def test_sample_documents():
    """Test that sample documents exist"""
    print("\nTesting sample documents...")
    sample_dir = 'sample_documents'
    
    if not os.path.exists(sample_dir):
        print(f"✗ {sample_dir} directory missing")
        return False
    
    print(f"✓ {sample_dir} directory exists")
    
    files = os.listdir(sample_dir)
    if len(files) > 0:
        print(f"✓ Found {len(files)} sample document(s):")
        for file in files:
            print(f"  - {file}")
        return True
    else:
        print(f"✗ No sample documents found")
        return False

def test_text_splitting():
    """Test document text splitting functionality"""
    print("\nTesting text splitting...")
    try:
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        from config import Config
        
        # Create a sample text
        sample_text = "This is a test document. " * 100
        
        # Create text splitter
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP
        )
        
        # Split the text
        chunks = text_splitter.split_text(sample_text)
        
        print(f"✓ Text splitting successful")
        print(f"  - Original text length: {len(sample_text)} characters")
        print(f"  - Number of chunks: {len(chunks)}")
        print(f"  - Average chunk size: {sum(len(c) for c in chunks) / len(chunks):.0f} characters")
        
        return True
    except Exception as e:
        print(f"✗ Text splitting test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("RAG Chatbot HRDI - Functionality Tests")
    print("=" * 60)
    
    results = []
    
    # Run tests
    results.append(("Import Test", test_imports()))
    results.append(("Configuration Test", test_config()))
    results.append(("File Structure Test", test_file_structure()))
    results.append(("Sample Documents Test", test_sample_documents()))
    results.append(("Text Splitting Test", test_text_splitting()))
    
    # Print summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "PASSED" if result else "FAILED"
        symbol = "✓" if result else "✗"
        print(f"{symbol} {test_name}: {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! The application is ready to use.")
        print("\nNext steps:")
        print("1. Copy .env.example to .env")
        print("2. Add your OPENAI_API_KEY to the .env file")
        print("3. Run: streamlit run app.py")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
