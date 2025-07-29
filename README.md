# 🎓 Educational Chat

An intelligent educational assistant that helps users generate exam-style questions from study materials using large language models (LLMs).  
This tool supports uploading custom files or selecting from preloaded curriculum content.

---

##  Key Capabilities

- Upload study materials (`PDF`, `DOCX`, `TXT`)
- Choose from stored curriculum by **grade & subject**
- Automatically generate questions:
  - MCQ
  - True/False
  - Short Answer
  - Essay
- Save, revisit, and download previously generated questions

---

## Features

- **RAG pipeline** powered by `LangChain` and `Chroma`
- HuggingFace `sentence-transformer` embeddings
- Prompt templates for different question types
- LLM-based question generation
- Memory support for follow-up questions
- Admin upload interface for educational content
- Question saving and management functionality

---

## 📁Project Structure

```bash
educational_chat/
├── modules/                  # Core logic (file loaders, LLM, memory, etc.)
├── pdf/                      # Uploaded or stored curriculum files
├── chroma/                   # Auto-generated vector indexes
├── saved_questions/          # Storage for saved questions
├── utils/                    # Utility scripts
├── main.py                   # Main application entry point
├── prepare_chroma_indexes.py # Optional batch indexing script
├── .env                      # API keys and config (not tracked)
├── requirements.txt          # Python dependencies
└── README.md                 # This file


## Setup Instructions

### 1. Clone the repository:
```bash
git clone https://github.com/Dai-ELsayed/educational_chat.git
cd educational_chat
2. Create and activate a virtual environment:
🪟 On Windows:

python -m venv venv
venv\Scripts\activate On Linux / macOS:
python3 -m venv venv
source venv/bin/activate

3. Install dependencies:
pip install -r requirements.txt

4. Set up environment variables:
Create a .env file in the root directory and add:


OPENROUTER_API_KEY=your_api_key_here
OPENAI_API_BASE=https://api.openai.com/v1

5. Run the application:
python main.py

