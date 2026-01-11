# RAG Chatbot HRDI 🤖

A Retrieval-Augmented Generation (RAG) chatbot built with LangChain, OpenAI, and Streamlit for HRDI (Human Resources Development and Innovation) purposes. This chatbot allows you to upload documents and ask questions about them using AI-powered natural language processing.

## Features

- 📄 **Document Upload**: Support for PDF and TXT files
- 🔍 **Intelligent Retrieval**: Uses vector embeddings to find relevant context
- 💬 **Conversational AI**: Maintains chat history for contextual conversations
- 📚 **Source Citations**: Shows which parts of documents were used to generate answers
- 🎨 **User-Friendly Interface**: Clean Streamlit web interface
- 💾 **Persistent Storage**: Save and load knowledge bases using ChromaDB

## Architecture

The chatbot uses the RAG (Retrieval-Augmented Generation) pattern:

1. **Document Processing**: Documents are loaded and split into chunks
2. **Embedding**: Text chunks are converted to vector embeddings using OpenAI's embedding model
3. **Vector Storage**: Embeddings are stored in ChromaDB for efficient retrieval
4. **Query Processing**: User questions are embedded and matched against stored vectors
5. **Response Generation**: Relevant context is retrieved and sent to GPT for answer generation

## Installation

### Prerequisites

- Python 3.8 or higher
- OpenAI API key

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/sisca77/rag_chatbot_hrdi.git
   cd rag_chatbot_hrdi
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit the `.env` file and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Usage

### Running the Web Application

Start the Streamlit app:

```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`.

### Using the Chatbot

1. **Upload Documents**
   - Click on the sidebar file uploader
   - Select one or more PDF or TXT files
   - Click "Process Documents" to index them

2. **Ask Questions**
   - Type your question in the chat input
   - Press Enter to get an AI-generated response
   - View source documents by expanding the "View Sources" section

3. **Load Existing Knowledge Base**
   - If you've previously processed documents, click "Load Existing Knowledge Base"
   - This loads the saved vector database without re-processing

4. **Clear Chat History**
   - Click "Clear Chat History" to start a fresh conversation

## Configuration

You can customize the chatbot behavior by editing the `.env` file:

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | Required |
| `EMBEDDING_MODEL` | OpenAI embedding model | `text-embedding-ada-002` |
| `LLM_MODEL` | OpenAI language model | `gpt-3.5-turbo` |
| `CHROMA_DB_PATH` | Path to ChromaDB storage | `./chroma_db` |
| `MAX_TOKENS` | Maximum tokens in response | `500` |
| `TEMPERATURE` | LLM temperature (0-1) | `0.7` |
| `CHUNK_SIZE` | Document chunk size | `1000` |
| `CHUNK_OVERLAP` | Overlap between chunks | `200` |

## Project Structure

```
rag_chatbot_hrdi/
├── app.py                  # Streamlit web interface
├── chatbot.py             # RAG chatbot implementation
├── config.py              # Configuration management
├── document_processor.py  # Document loading and processing
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## Core Components

### `config.py`
Manages application configuration and environment variables.

### `document_processor.py`
Handles document loading, text splitting, and vector store creation/management.

### `chatbot.py`
Implements the RAG chatbot using LangChain's ConversationalRetrievalChain.

### `app.py`
Streamlit web interface for user interaction.

## Technologies Used

- **LangChain**: Framework for building LLM applications
- **OpenAI**: GPT models for text generation and embeddings
- **ChromaDB**: Vector database for embedding storage
- **Streamlit**: Web framework for the user interface
- **PyPDF**: PDF document processing
- **Python-dotenv**: Environment variable management

## Tips for Best Results

1. **Document Quality**: Upload clear, well-formatted documents for better results
2. **Specific Questions**: Ask specific questions rather than general ones
3. **Context**: The chatbot remembers conversation history, so you can ask follow-up questions
4. **Sources**: Always check the source documents to verify the accuracy of responses

## Troubleshooting

### "OPENAI_API_KEY is not set" Error
- Make sure you've created a `.env` file with your API key
- Verify the API key is valid and has credits

### Documents Not Processing
- Check that your files are in PDF or TXT format
- Ensure the files are not corrupted or password-protected

### Slow Responses
- This is normal for large documents or complex questions
- Consider using GPT-4 for higher quality (but slower) responses

## Security Notes

- Never commit your `.env` file or API keys to version control
- Keep your OpenAI API key secure and don't share it
- The `.gitignore` file is configured to exclude sensitive files

## License

This project is open source and available for educational and commercial use.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues or questions, please open an issue on the GitHub repository.
