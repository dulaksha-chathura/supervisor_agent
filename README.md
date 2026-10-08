# Supervisor Agent

An LLM-based **Retail Intelligence Supervisor Agent** that uses **Qwen 3.8 27B via Groq** to intelligently select and orchestrate tools for answering retail business questions.

### Tools

- **SQLite** — sales, products, orders, and revenue analysis
- **ChromaDB + HuggingFace** — internal policy and document retrieval
- **Tavily** — live web search for external information

The main application is:

```text
supervisora_agent.ipynb
```

## Project Structure

```text
supervisor_agent/
├── supervisora_agent.ipynb
├── data/
│   ├── company.db
│   └── chroma_db/
├── .env
└── README.md
```

## Setup

Clone the repository:

```bash
git clone https://github.com/dulaksha-chathura/supervisor_agent.git
cd supervisor_agent
```

Create and activate a virtual environment:

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## API Keys

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

## Run

Start Jupyter:

```bash
jupyter notebook
```

Open:

```text
supervisora_agent.ipynb
```

Run the notebook cells **from top to bottom**. The final cell allows you to enter questions interactively.

Example:

```text
Enter your question: What are the top 5 products by revenue?
```

The supervisor automatically selects the appropriate tool(s), retrieves the required evidence, and generates the final answer.

## Requirements

- Python 3.10+
- Groq API key
- Tavily API key
- `data/company.db`
- `data/chroma_db/`

## Technologies

**Python · Jupyter · Groq · Qwen · SQLite · ChromaDB · HuggingFace · Tavily**
A local SQLite database provides structured business information.

