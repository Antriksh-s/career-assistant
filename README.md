# 🤖 AI-Powered Career Assistant (RAG)

An intelligent Career Assistant built using **FastAPI**, **Streamlit**, and **LangChain**. This bot uses **Retrieval-Augmented Generation (RAG)** to answer questions based on my professional experience as a DevOps & Site Reliability Engineer (SRE).

## 🚀 Features
- **RAG Architecture**: Uses FAISS as a vector database to retrieve facts from a custom knowledge base (`my_career.txt`).
- **Decoupled Architecture**: FastAPI backend with a Streamlit frontend.
- **Modern Tech Stack**: Python 3.12, OpenAI GPT-4o-mini, and LangChain.
- **SRE Focused**: Highlights expertise in observability (Splunk/Datadog), automation (Ansible/Terraform), and AI Governance.

## 🛠️ Project Structure
```text
.
├── backend/
│   ├── engine.py       # RAG Logic & LLM Integration
│   ├── main.py         # FastAPI Endpoints
│   └── schemas.py      # Pydantic Models
├── frontend/
│   └── app.py          # Streamlit UI
├── my_career.txt       # Knowledge base (not tracked in Git)
├── .env                # API Keys (not tracked in Git)
└── requirements.txt    # Project Dependencies