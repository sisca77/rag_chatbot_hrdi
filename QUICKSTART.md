# Quick Start Guide for RAG Chatbot HRDI

This guide will help you get the RAG Chatbot up and running quickly.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- An OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

## Installation (5 minutes)

### Step 1: Set up Python Virtual Environment

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- Streamlit (Web interface)
- LangChain (RAG framework)
- OpenAI (LLM and embeddings)
- ChromaDB (Vector database)
- PyPDF (PDF processing)
- And other dependencies

### Step 3: Configure API Key

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your OpenAI API key
# On macOS/Linux:
nano .env
# On Windows:
notepad .env
```

Replace `your_openai_api_key_here` with your actual OpenAI API key.

## Running the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`.

## First-Time Usage

1. **Upload Sample Documents** (Optional for testing)
   - The `sample_documents` folder contains example HRDI documents
   - Click "Browse files" in the sidebar
   - Select `hrdi_guidelines.txt` and/or `training_schedule.txt`
   - Click "Process Documents"
   - Wait for processing to complete

2. **Ask Questions**
   Try these example questions:
   - "How many days of annual leave do employees get?"
   - "What is the onboarding program?"
   - "When is the Python programming workshop?"
   - "What are the parental leave policies?"

3. **View Sources**
   - Each answer includes source citations
   - Click "View Sources" to see which document sections were used

## Tips for Success

### Getting Better Answers

1. **Be Specific**: Instead of "Tell me about training", ask "What training programs are available in Q1 2024?"

2. **Use Context**: The chatbot remembers conversation history. You can ask follow-up questions like "What about Q2?"

3. **Check Sources**: Always verify important information by checking the source documents

### Troubleshooting

| Problem | Solution |
|---------|----------|
| "OPENAI_API_KEY is not set" | Make sure `.env` file exists and contains your API key |
| "ModuleNotFoundError" | Run `pip install -r requirements.txt` |
| Slow responses | Normal for first query; subsequent queries are faster |
| "No documents found" | Upload documents using the sidebar before asking questions |

## Example Workflow

```
1. Start application: streamlit run app.py
2. Upload documents: Sample HRDI documents
3. Wait for processing: ~30 seconds for sample docs
4. Ask question: "What training is available in February?"
5. Get answer: Information about Python Programming workshop
6. View sources: See the relevant section from training_schedule.txt
7. Follow-up: "What are the prerequisites?"
8. Get answer: Based on conversation context
```

## File Upload Guidelines

### Supported Formats
- PDF files (.pdf)
- Text files (.txt)

### Best Practices
- Upload clear, well-formatted documents
- Avoid scanned PDFs (use OCR first)
- Break large documents into smaller sections
- Use descriptive file names

### File Size
- Recommended: Under 10MB per file
- Large files take longer to process
- Consider splitting very large documents

## Advanced Configuration

Edit `.env` to customize:

```env
# Use GPT-4 for higher quality (costs more)
LLM_MODEL=gpt-4

# Increase response length
MAX_TOKENS=1000

# More creative responses (0.0-1.0)
TEMPERATURE=0.9

# Smaller chunks for more precise retrieval
CHUNK_SIZE=500
```

## Cost Considerations

### OpenAI API Costs
- **Embeddings**: ~$0.0001 per 1,000 tokens
- **GPT-3.5**: ~$0.002 per 1,000 tokens
- **GPT-4**: ~$0.03 per 1,000 tokens

### Example Cost
Processing 10 PDF pages + 50 questions:
- With GPT-3.5: ~$0.50
- With GPT-4: ~$5.00

### Saving Costs
1. Use GPT-3.5 instead of GPT-4
2. Set lower MAX_TOKENS
3. Reuse existing knowledge base (Load instead of reprocessing)

## Next Steps

1. **Try Different Documents**: Upload your own HR policies, manuals, or guides
2. **Customize Settings**: Adjust chunk size and temperature for your needs
3. **Share**: The app can be shared with your team using Streamlit sharing
4. **Extend**: Add more document types (Word, Excel) by modifying `document_processor.py`

## Getting Help

- **Documentation**: See README.md for full documentation
- **Issues**: Check existing GitHub issues or create a new one
- **Community**: Join LangChain and Streamlit communities

## Security Reminder

⚠️ **Important**: 
- Never commit your `.env` file to version control
- Keep your OpenAI API key private
- Review uploaded documents for sensitive information
- Use environment variables for production deployments

---

**Ready to start?** Run `streamlit run app.py` and start chatting! 🚀
