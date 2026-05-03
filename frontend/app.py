import sys
import os
import uuid
import streamlit as st

# 1. PATH FIX: Adds the root directory to the python path 
# so Streamlit Cloud can find the 'backend' folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the engine logic directly for a monolith architecture
from backend.engine import get_chat_response

# 2. Page Configuration
st.set_page_config(
    page_title="Antriksh Singh | AI Career Assistant",
    page_icon="🤖",
    layout="wide"
)

# 3. State Management (Must be initialized before UI interaction)
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []
if "active_prompt" not in st.session_state:
    st.session_state.active_prompt = None

# 4. Sidebar for Portfolio Details
with st.sidebar:
    st.title("👨‍💻 Candidate Profile")
    st.markdown("""
    **Antriksh Singh**  
    *Sr. DevOps & SRE Specialist*
    ---
    **Top Certifications:**
    - ☁️ AWS Solutions Architect
    - 🐧 Red Hat Certified Engineer (RHCE)
    
    **Specialties:**
    - AI-Enabled Observability
    - Self-Healing Infra
    - Kubernetes & Go
    """)
    
    st.info("This AI is trained on my professional history. Ask it about my projects, tech stack, or certifications.")
    
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# 5. Main Interface Header
st.title("🤖 AI Assistant")
st.caption("Powered by RAG (Retrieval-Augmented Generation) & GPT-4o-mini")

# 6. Prompt Suggestions Grid
st.markdown("### 💡 Explore Antriksh's Expertise")

def handle_click(prompt_text):
    st.session_state.active_prompt = prompt_text

suggestions_row1 = [
    "Tell me about your AI-driven SLO breach prediction project.",
    "How did you reduce Datadog costs by 30%?",
    "Explain your experience with Self-Healing Infrastructure."
]
suggestions_row2 = [
    "What are your top skills in Agentic AI and RAG?",
    "Show me your automation work with Ansible and Python.",
    "Tell me about your cloud migrations to AWS ECS Fargate."
]

cols1 = st.columns(3)
for i, prompt in enumerate(suggestions_row1):
    if cols1[i].button(prompt, use_container_width=True):
        handle_click(prompt)

cols2 = st.columns(3)
for i, prompt in enumerate(suggestions_row2):
    if cols2[i].button(prompt, use_container_width=True):
        handle_click(prompt)

# 7. Unified Input Logic (Buttons or Text Input)
chat_input = st.chat_input("Ask me about Antriksh's experience...")
final_prompt = None

if chat_input:
    final_prompt = chat_input
elif st.session_state.active_prompt:
    final_prompt = st.session_state.active_prompt
    st.session_state.active_prompt = None  # Clear the state immediately

if final_prompt:
    # Add user message to state and rerun to update UI before AI processing
    st.session_state.messages.append({"role": "user", "content": final_prompt})
    st.rerun()

# 8. Display Chat History with Professional Avatars
for msg in st.session_state.messages:
    avatar = "👨‍💻" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# 9. Generate AI Response (Triggered if the last message is from user)
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    last_user_prompt = st.session_state.messages[-1]["content"]
    
    with st.chat_message("assistant", avatar="🤖"):
        message_placeholder = st.empty()
        message_placeholder.markdown("🔍 *Scanning career database...*")
        
        try:
            # Direct call to the backend engine
            full_response = get_chat_response(last_user_prompt, st.session_state.session_id)
            
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
                
        except Exception as e:
            if "OPENAI_API_KEY" in str(e):
                st.error("Missing OpenAI API Key. Please add it to your Streamlit Secrets.")
            else:
                st.error(f"An unexpected error occurred: {e}")