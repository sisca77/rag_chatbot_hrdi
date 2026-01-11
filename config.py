import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for the RAG Chatbot"""
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'text-embedding-ada-002')
    LLM_MODEL = os.getenv('LLM_MODEL', 'gpt-3.5-turbo')
    
    # ChromaDB Configuration
    CHROMA_DB_PATH = os.getenv('CHROMA_DB_PATH', './chroma_db')
    
    # Application Configuration
    MAX_TOKENS = int(os.getenv('MAX_TOKENS', 500))
    TEMPERATURE = float(os.getenv('TEMPERATURE', 0.7))
    CHUNK_SIZE = int(os.getenv('CHUNK_SIZE', 1000))
    CHUNK_OVERLAP = int(os.getenv('CHUNK_OVERLAP', 200))
    
    @staticmethod
    def validate():
        """Validate that required configuration is present"""
        if not Config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set. Please set it in your .env file.")
        return True
