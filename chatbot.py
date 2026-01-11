from langchain_openai import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from config import Config
from document_processor import DocumentProcessor

class RAGChatbot:
    """RAG Chatbot for HRDI using LangChain"""
    
    def __init__(self, vector_store=None):
        # OpenAI API key is automatically read from OPENAI_API_KEY environment variable
        self.llm = ChatOpenAI(
            model=Config.LLM_MODEL,
            temperature=Config.TEMPERATURE,
            max_tokens=Config.MAX_TOKENS
        )
        
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )
        
        self.vector_store = vector_store
        self.qa_chain = None
        
        if self.vector_store:
            self._initialize_chain()
    
    def _initialize_chain(self):
        """Initialize the conversational retrieval chain"""
        retriever = self.vector_store.as_retriever(
            search_kwargs={"k": 3}
        )
        
        self.qa_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=retriever,
            memory=self.memory,
            return_source_documents=True,
            verbose=False
        )
    
    def set_vector_store(self, vector_store):
        """Set or update the vector store"""
        self.vector_store = vector_store
        self._initialize_chain()
    
    def ask(self, question):
        """Ask a question to the chatbot"""
        if not self.qa_chain:
            return {
                "answer": "Please upload documents first to enable the chatbot.",
                "source_documents": []
            }
        
        response = self.qa_chain({"question": question})
        return response
    
    def reset_memory(self):
        """Clear the conversation history"""
        self.memory.clear()
