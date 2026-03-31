🧠 Corrective RAG (CRAG) Agent with LangGraph
A high-performance, Agentic RAG system built with LangGraph and Groq. This project demonstrates a "self-correcting" retrieval pipeline that autonomously evaluates the relevance of local documents and triggers a web-search fallback (Tavily) if the local context is insufficient.

🚀 Key Features
Stateful Agentic Workflow: Uses LangGraph to manage cycles and conditional logic between nodes.

Self-Grading Retrieval: An LLM "Grader" node evaluates local document relevance before generating an answer.

Multi-Source Context: Combines a local FAISS Vector Store with real-time Tavily Web Search.

Ultra-Fast Inference: Powered by Llama 3.3-70B on Groq (LPU technology) for near-instant responses.

Local Embeddings: Uses all-MiniLM-L6-v2 via HuggingFace, optimized for low-latency and cost-efficiency.

CI/CD Integrated: Automated graph validation and linting via GitHub Actions.

🛠️ Tech Stack
Framework: LangGraph, LangChain

LLM: Llama 3.3-70B (via Groq)

Vector Database: FAISS

Embeddings: HuggingFace (sentence-transformers)

Search API: Tavily

Automation: GitHub Actions (CI/CD)

📁 Project Structure
Plaintext
Corrective-RAG/
├── .github/workflows/
│   └── ci.yml             # GitHub Actions CI pipeline
├── .env                   # Environment variables (API Keys)
├── C_RAG_agent.py         # Main Agent logic and LangGraph definition
├── test_agent.py          # Unit tests for CI/CD validation
├── requirements.txt       # Project dependencies
└── README.md
⚙️ Setup & Installation
Clone the repository:

Bash
git clone https://github.com/yourusername/corrective-rag-agent.git
cd corrective-rag-agent
Set up Virtual Environment:

Bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install Dependencies:

Bash
pip install -r requirements.txt
Configure Environment Variables:
Create a .env file and add your keys:

Plaintext
Groq_API=gsk_your_groq_key
Tavily_API=tvly-your_tavily_key
🧪 Automated Testing (CI/CD)
This project includes a CI/CD pipeline that automatically triggers on every push. It verifies:

Dependency Installation: Ensures the environment is reproducible.

Graph Compilation: Validates that the LangGraph state machine has no dead-ends or broken edges.

To run tests locally:

Bash
python test_agent.py