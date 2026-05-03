import sys
import os
import uuid
import streamlit as st
import time

# 1. PATH FIX
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.engine import get_chat_response

# 2. Page Configuration
st.set_page_config(
    page_title="Antriksh Singh | AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# 3. Dynamic Theme CSS
# This CSS uses system-aware colors and variables to fix the 'black box' issue in light mode.
st.markdown("""
<style>
    /* Adaptive typography and spacing */
    .block-container { padding-top: 2rem; padding-bottom: 0rem; }
    h1, h2, h3, h4 { font-weight: 300 !important; letter-spacing: -0.02em; }

    /* Dynamic Button Styling (Minimalist) */
    div.stButton > button {
        background-color: rgba(128, 128, 128, 0.05);
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 8px;
        transition: all 0.3s ease;
        font-size: 0.85rem;
    }
    div.stButton > button:hover {
        border-color: #10b981;
        color: #10b981;
        background-color: rgba(16, 185, 129, 0.05);
    }

    /* Adaptive Chat Bubbles - Fixes the 'Black Box' issue */
    [data-testid="stChatMessage"] {
        background-color: rgba(128, 128, 128, 0.05); /* Transparent grey adapted to theme */
        border: 1px solid rgba(128, 128, 128, 0.1);
        border-radius: 12px;
        margin-bottom: 1rem;
    }

    /* Emerald Accent for the Bot */
    [data-testid="stChatMessageAssistant"] {
        border-left: 3px solid #10b981;
    }

    /* Animated typing indicator */
    .typing {
        color: #10b981;
        font-family: 'Source Code Pro', monospace;
        font-size: 0.8rem;
        letter-spacing: 0.1rem;
        animation: blink 1s infinite;
    }
    @keyframes blink { 0% { opacity: 0.4; } 50% { opacity: 1; } 100% { opacity: 0.4; } }
</style>
""", unsafe_allow_html=True)

# 4. State Management
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []
if "active_prompt" not in st.session_state:
    st.session_state.active_prompt = None

# 5. Sidebar (Minimalist & Clean)
with st.sidebar:
    st.markdown("### Antriksh Singh")
    st.caption("SRE & DevOps Specialist")
    st.markdown("---")
    st.markdown("""
    - AWS Solutions Architect
    - Red Hat Certified Engineer (RHCE)
    """)
    if st.button("Reset Session", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# 6. Header
st.title("AI Assistant")
st.caption("A context-aware retrieval engine built on professional history.")

# 7. Subtle Grid for Suggestions
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

# 8. Unified Logic Handler
chat_input = st.chat_input("Message the assistant...")
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

# 10. Minimalist Loader & Adaptive Execution
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    last_user_prompt = st.session_state.messages[-1]["content"]
    
    with st.chat_message("assistant", avatar="🤖"):
        placeholder = st.empty()
        placeholder.markdown("<p class='typing'>CONSULTING KNOWLEDGE BASE...</p>", unsafe_allow_html=True)
        
        try:
            # Monolith logic call
            full_response = get_chat_response(last_user_prompt, st.session_state.session_id)
            placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            placeholder.error("System connection interrupted.")