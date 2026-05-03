import sys
import os
import uuid
import streamlit as st

# 1. PATH FIX
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.engine import get_chat_response

# 2. Page Configuration
st.set_page_config(
    page_title="Antriksh Singh | AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# 3. Enhanced Dynamic Theme CSS
# This version adds a sophisticated color palette for Light Mode (Sky Blue/Emerald)
st.markdown("""
<style>
    /* 1. Global Background & Typography */
    .block-container { padding-top: 2rem; }
    h1, h2, h3 { font-weight: 300 !important; }

    /* 2. Suggestion Buttons - Professional Tones */
    div.stButton > button {
        background-color: rgba(16, 185, 129, 0.03);
        border: 1px solid rgba(16, 185, 129, 0.2);
        color: #10b981;
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: #10b981;
        color: white !important;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2);
    }

    /* 3. Adaptive Chat Bubbles */
    /* User Message: Subtle Blue */
    [data-testid="stChatMessageUser"] {
        background-color: rgba(59, 130, 246, 0.05); 
        border: 1px solid rgba(59, 130, 246, 0.1);
        border-radius: 15px 15px 0px 15px;
    }

    /* Assistant Message: Subtle Emerald */
    [data-testid="stChatMessageAssistant"] {
        background-color: rgba(16, 185, 129, 0.05);
        border: 1px solid rgba(16, 185, 129, 0.1);
        border-radius: 15px 15px 15px 0px;
    }

    /* 4. The Sidebar - Clean Slate */
    section[data-testid="stSidebar"] {
        background-color: rgba(248, 250, 252, 0.5);
    }

    /* 5. Animated Typing Indicator */
    .typing-text {
        color: #10b981;
        font-weight: 500;
        font-size: 0.85rem;
        letter-spacing: 0.05rem;
        animation: pulse 1.5s infinite;
    }
    @keyframes pulse { 0% { opacity: 0.5; } 50% { opacity: 1; } 100% { opacity: 0.5; } }
</style>
""", unsafe_allow_html=True)

# 4. State Management
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []
if "active_prompt" not in st.session_state:
    st.session_state.active_prompt = None

# 5. Sidebar (Professional Profile)
with st.sidebar:
    st.markdown("### Antriksh Singh")
    st.caption("Sr. DevOps & SRE Specialist")
    st.markdown("---")
    st.markdown("""
    **Core Credentials:**
    - ☁️ AWS Solutions Architect
    - 🐧 Red Hat Certified Engineer
    """)
    if st.button("Reset Session", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# 6. Main Header
st.title("AI Career Assistant")
st.caption("Leveraging RAG to explore Antriksh's engineering journey.")

# 7. Colorful Suggestion Grid
suggestions = [
    "AI-driven SLO breach prediction",
    "Reduce Datadog costs by 30%",
    "Self-Healing Infrastructure",
    "Skills in Agentic AI and RAG",
    "Automation with Ansible/Python",
    "AWS ECS Fargate Migrations"
]

cols = st.columns(3)
for i, prompt in enumerate(suggestions):
    if cols[i % 3].button(prompt, use_container_width=True):
        st.session_state.active_prompt = prompt

# 8. Unified Logic
chat_input = st.chat_input("Ask a question...")
final_prompt = chat_input if chat_input else st.session_state.active_prompt

if final_prompt:
    st.session_state.messages.append({"role": "user", "content": final_prompt})
    st.session_state.active_prompt = None
    st.rerun()

# 9. Chat Display
for msg in st.session_state.messages:
    avatar = "👨‍💻" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# 10. Execution with Animated Loader
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    last_user_prompt = st.session_state.messages[-1]["content"]
    
    with st.chat_message("assistant", avatar="🤖"):
        placeholder = st.empty()
        placeholder.markdown("<p class='typing-text'>⚡ RETRIEVING CAREER INSIGHTS...</p>", unsafe_allow_html=True)
        
        try:
            full_response = get_chat_response(last_user_prompt, st.session_state.session_id)
            placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            placeholder.error("Service temporarily unavailable.")