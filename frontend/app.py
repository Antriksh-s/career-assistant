import sys
import os
import uuid
import streamlit as st
import time

# 1. PATH FIX
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.engine import get_chat_response

# 2. Page Configuration & Professional Minimalist Styling
st.set_page_config(
    page_title="Antriksh Singh | AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS for a clean, sophisticated look
st.markdown("""
<style>
    /* Remove unnecessary padding and borders */
    .block-container { padding-top: 2rem; padding-bottom: 0rem; }
    .stChatFloatingInputContainer { background-color: transparent; }
    
    /* Elegant typography and background */
    h1, h2, h3, h4 { font-weight: 300 !important; letter-spacing: -0.02em; }
    .stApp { background-color: #0f1115; }

    /* Minimalist buttons for suggestions */
    div.stButton > button {
        background-color: #1a1c23;
        border: 1px solid #2d2f39;
        color: #94a3b8;
        border-radius: 8px;
        transition: all 0.3s ease;
        font-size: 0.85rem;
    }
    div.stButton > button:hover {
        border-color: #10b981;
        color: #10b981;
        background-color: #10b9810a;
    }

    /* Subtle chat bubbles */
    [data-testid="stChatMessage"] {
        background-color: #161920;
        border: 1px solid #22252e;
        border-radius: 12px;
        margin-bottom: 1rem;
    }

    /* Animated typing indicator */
    .typing {
        color: #10b981;
        font-family: monospace;
        overflow: hidden;
        border-right: .15em solid #10b981;
        white-space: nowrap;
        margin: 0 auto;
        letter-spacing: .15em;
        animation: typing 2.5s steps(30, end), blink-caret .5s step-end infinite;
    }
    @keyframes typing { from { width: 0 } to { width: 100% } }
    @keyframes blink-caret { from, to { border-color: transparent } 50% { border-color: #10b981 } }
</style>
""", unsafe_allow_html=True)

# 3. State Management
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []
if "active_prompt" not in st.session_state:
    st.session_state.active_prompt = None

# 4. Sidebar (Simplified)
with st.sidebar:
    st.markdown("### Antriksh Singh")
    st.caption("SRE & DevOps Specialist")
    st.markdown("---")
    st.markdown("""
    - AWS Solutions Architect
    - Red Hat Certified Engineer
    """)
    if st.button("Reset Session", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# 5. Header
st.title("AI Assistant")
st.caption("Context-aware retrieval of professional history.")

# 6. Minimalist Grid for Suggestions
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

# 7. Logic Flow
chat_input = st.chat_input("Message the assistant...")
final_prompt = chat_input if chat_input else st.session_state.active_prompt

if final_prompt:
    st.session_state.messages.append({"role": "user", "content": final_prompt})
    st.session_state.active_prompt = None
    st.rerun()

# 8. Chat Display
for msg in st.session_state.messages:
    avatar = "👨‍💻" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# 9. Minimalist Loader & Response Execution
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    last_user_prompt = st.session_state.messages[-1]["content"]
    
    with st.chat_message("assistant", avatar="🤖"):
        # No more buttons/expanders. Just a clean, silent loader.
        placeholder = st.empty()
        placeholder.markdown("<p class='typing'>CONSULTING KNOWLEDGE BASE...</p>", unsafe_allow_html=True)
        
        try:
            full_response = get_chat_response(last_user_prompt, st.session_state.session_id)
            placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            # Scroll handling is native to st.chat_message and st.rerun
        except Exception as e:
            placeholder.error("System connection interrupted.")