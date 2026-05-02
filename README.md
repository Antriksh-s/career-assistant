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



## 🚦 Getting Started

### 1. Prerequisites
*   **Python 3.12+**
*   **uv** (Recommended for high-performance dependency management)
*   **OpenAI API Key**

### 2. Installation
Clone the repository and navigate to the project root:
```bash
git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
cd your-repo-name

###3. Environment Setup
Create a .env file in the root directory to store your credentials:

Bash
echo "OPENAI_API_KEY=your_sk_key_here" > .env

Create a virtual environment and install dependencies using uv:

Bash
# Create the environment
uv venv --python 3.12 chat_env

# Activate the environment
source chat_env/bin/activate

# Install requirements
uv pip install -r requirements.txt

###4. Knowledge Base Configuration
Add your career details to my_career.txt in the root directory. This file is used by the RAG engine to provide factual answers about your experience.

Note: Ensure no personal contact details (phone, email) are included in my_career.txt for privacy before deploying publicly.

###5. Running the Application
The project uses a decoupled architecture. You will need to run the backend and frontend in separate terminal sessions.

Start the FastAPI Backend:

Bash
python -m uvicorn backend.main:app --reload

###6. Verification
Open your browser to http://localhost:8501. You should see the AI Career Assistant interface. Test the connection by asking: "What are your top technical skills?"



*   **Indentation:** Markdown is sensitive to indentation in lists; the version above uses standard 4-space indentation to ensure bullet points render correctly across all platforms.
*   **File naming:** Make sure your knowledge base file is named exactly `my_career.txt` to match your `engine.py` logic.
*   **Version Control:** Remember that `requirements.txt` is your "source of truth" for anyone cloning your repo, so keep it updated if you install more tools later!