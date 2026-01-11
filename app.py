import streamlit as st
import os
import tempfile
from config import Config
from document_processor import DocumentProcessor
from chatbot import RAGChatbot

# Page configuration
st.set_page_config(
    page_title="RAG Chatbot HRDI",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #e3f2fd;
    }
    .bot-message {
        background-color: #f5f5f5;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'doc_processor' not in st.session_state:
        st.session_state.doc_processor = None
    if 'vector_store' not in st.session_state:
        st.session_state.vector_store = None

def display_chat_history():
    """Display the chat history"""
    for message in st.session_state.chat_history:
        if message['role'] == 'user':
            st.markdown(f'<div class="chat-message user-message"><strong>You:</strong> {message["content"]}</div>', 
                       unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message bot-message"><strong>Bot:</strong> {message["content"]}</div>', 
                       unsafe_allow_html=True)
            if 'sources' in message and message['sources']:
                with st.expander("📚 View Sources"):
                    for i, source in enumerate(message['sources'], 1):
                        st.write(f"**Source {i}:**")
                        st.write(source.page_content[:300] + "...")
                        st.write("---")

def main():
    """Main application function"""
    st.markdown('<h1 class="main-header">🤖 RAG Chatbot HRDI</h1>', unsafe_allow_html=True)
    st.markdown("Welcome to the HRDI RAG Chatbot! Upload your documents and start asking questions.")
    
    # Initialize session state
    initialize_session_state()
    
    # Sidebar for document upload and settings
    with st.sidebar:
        st.header("📄 Document Management")
        
        # File uploader
        uploaded_files = st.file_uploader(
            "Upload documents (PDF or TXT)",
            type=['pdf', 'txt'],
            accept_multiple_files=True
        )
        
        if uploaded_files and st.button("Process Documents"):
            with st.spinner("Processing documents..."):
                try:
                    # Validate configuration
                    Config.validate()
                    
                    # Initialize document processor
                    if st.session_state.doc_processor is None:
                        st.session_state.doc_processor = DocumentProcessor()
                    
                    all_chunks = []
                    
                    # Process each uploaded file
                    for uploaded_file in uploaded_files:
                        # Validate file extension
                        file_ext = os.path.splitext(uploaded_file.name)[1].lower()
                        if file_ext not in ['.pdf', '.txt']:
                            st.warning(f"Skipping unsupported file: {uploaded_file.name}")
                            continue
                        
                        # Save to temporary file with secure permissions
                        tmp_fd, tmp_path = tempfile.mkstemp(suffix=file_ext)
                        try:
                            # Write file content
                            with os.fdopen(tmp_fd, 'wb') as tmp_file:
                                tmp_file.write(uploaded_file.getvalue())
                            
                            # Load and process document
                            documents = st.session_state.doc_processor.load_document(tmp_path)
                            chunks = st.session_state.doc_processor.process_documents(documents)
                            all_chunks.extend(chunks)
                        finally:
                            # Always clean up temporary file
                            try:
                                os.unlink(tmp_path)
                            except OSError:
                                pass  # File may already be deleted
                    
                    # Create vector store
                    st.session_state.vector_store = st.session_state.doc_processor.create_vector_store(all_chunks)
                    
                    # Initialize or update chatbot
                    if st.session_state.chatbot is None:
                        st.session_state.chatbot = RAGChatbot(st.session_state.vector_store)
                    else:
                        st.session_state.chatbot.set_vector_store(st.session_state.vector_store)
                    
                    st.success(f"✅ Successfully processed {len(uploaded_files)} document(s) with {len(all_chunks)} chunks!")
                    
                except ValueError as e:
                    st.error(f"Configuration Error: {str(e)}")
                    st.info("Please create a .env file with your OPENAI_API_KEY. See .env.example for reference.")
                except Exception as e:
                    st.error(f"Error processing documents: {str(e)}")
        
        st.markdown("---")
        
        # Load existing vector store
        if st.button("Load Existing Knowledge Base"):
            try:
                Config.validate()
                
                if st.session_state.doc_processor is None:
                    st.session_state.doc_processor = DocumentProcessor()
                
                st.session_state.vector_store = st.session_state.doc_processor.load_vector_store()
                
                if st.session_state.chatbot is None:
                    st.session_state.chatbot = RAGChatbot(st.session_state.vector_store)
                else:
                    st.session_state.chatbot.set_vector_store(st.session_state.vector_store)
                
                st.success("✅ Loaded existing knowledge base!")
                
            except ValueError as e:
                st.error(f"Configuration Error: {str(e)}")
            except Exception as e:
                st.error(f"Error loading knowledge base: {str(e)}")
        
        st.markdown("---")
        
        # Clear chat history
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history = []
            if st.session_state.chatbot:
                st.session_state.chatbot.reset_memory()
            st.rerun()
    
    # Main chat interface
    st.header("💬 Chat Interface")
    
    # Display chat history
    display_chat_history()
    
    # Chat input
    user_question = st.text_input("Ask a question about your documents:", key="user_input")
    
    if user_question:
        # Add user message to history
        st.session_state.chat_history.append({
            'role': 'user',
            'content': user_question
        })
        
        # Get bot response
        with st.spinner("Thinking..."):
            try:
                if st.session_state.chatbot is None:
                    st.session_state.chatbot = RAGChatbot()
                
                response = st.session_state.chatbot.ask(user_question)
                
                # Add bot response to history
                st.session_state.chat_history.append({
                    'role': 'bot',
                    'content': response['answer'],
                    'sources': response.get('source_documents', [])
                })
                
            except Exception as e:
                st.error(f"Error generating response: {str(e)}")
        
        st.rerun()

if __name__ == "__main__":
    main()
