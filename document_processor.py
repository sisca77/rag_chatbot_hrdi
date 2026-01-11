from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from config import Config
import os

class DocumentProcessor:
    """Handle document loading and processing for the RAG system"""
    
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP
        )
        # OpenAI API key is automatically read from OPENAI_API_KEY environment variable
        self.embeddings = OpenAIEmbeddings(
            model=Config.EMBEDDING_MODEL
        )
        
    def load_document(self, file_path):
        """Load a document based on its file type"""
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension == '.pdf':
            loader = PyPDFLoader(file_path)
        elif file_extension == '.txt':
            loader = TextLoader(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")
        
        documents = loader.load()
        return documents
    
    def process_documents(self, documents):
        """Split documents into chunks"""
        chunks = self.text_splitter.split_documents(documents)
        return chunks
    
    def create_vector_store(self, chunks, collection_name="hrdi_documents"):
        """Create a vector store from document chunks"""
        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory=Config.CHROMA_DB_PATH,
            collection_name=collection_name
        )
        return vector_store
    
    def load_vector_store(self, collection_name="hrdi_documents"):
        """Load an existing vector store"""
        vector_store = Chroma(
            persist_directory=Config.CHROMA_DB_PATH,
            embedding_function=self.embeddings,
            collection_name=collection_name
        )
        return vector_store
