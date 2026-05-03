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

# 3. Separate Configs for Light & Dark Modes
# Using @media (prefers-color-scheme) to prevent "faded" or "weird" UI crossovers.
st.markdown("""
<style>
    /* Global Styles */
    .block-container { padding-top: 2rem; }
    h1, h2, h3 { font-weight: 300 !important; }

    /* TYPEWRITER ANIMATION for the loader */
    .typewriter-loader {
        color: #10b981;
        font-family: monospace;
        overflow: hidden;
        border-right: .15em solid #10b981;
        white-space: nowrap;
        margin: 0 auto;
        letter-spacing: .10em;
        width: fit-content;
        animation: typing 2s steps(30, end), blink-caret .5s step-end infinite;
    }
    @keyframes typing { from { width: 0 } to { width: 100% } }
    @keyframes blink-caret { from, to { border-color: transparent } 50% { border-color: #10b981 } }

    /* DARK MODE SPECIFIC OVERRIDES */
    @media (prefers-color-scheme: dark) {
        section[data-testid="stSidebar"] {
            background-color: #0e1117 !important; /* Deep solid black/grey */
        }
        [data-testid="stChatMessageUser"] {
            background-color: rgba(59, 130, 246, 0.15); /* Stronger blue for dark */
            border: 1px solid rgba(59, 130, 246, 0.2);
        }
        [data-testid="stChatMessageAssistant"] {
            background-color: #1a1c23; /* Solid dark for assistant */
            border: 1px solid #2d2f39;
        }
    }

    /* LIGHT MODE SPECIFIC OVERRIDES */
    @media (prefers-color-scheme: light) {
        section[data-testid="stSidebar"] {
            background-color: #f8fafc !important; /* Soft professional slate white */
        }
        [data-testid="stChatMessageUser"] {
            background-color: #f0f7ff; /* Vivid soft blue */
            border: 1px solid #cce3ff;
            color: #1e3a8a;
        }
        [data-testid="stChatMessageAssistant"] {
            background-color: #f0fdf4; /* Vivid soft emerald */
            border: 1px solid #dcfce7;
            color: #064e3b;
        }
    }

    /* Suggestion Buttons - Common Styles */
    div.stButton > button {
        border-radius: 10px;
        transition: all 0.3s ease;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    div.stButton > button:hover {
        border-color: #10b981;
        background-color: rgba(16, 185, 129, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# 4. State Management
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []
if "active_prompt" not in st.session_state:
    st.session_state.active_prompt = None

# 5. Sidebar
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
st.caption("RAG-powered exploration of Antriksh's professional background.")

# 7. Suggestion Grid
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
chat_input = st.chat_input("Ask about my experience...")
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

# 10. Execution with Typewriter Loader
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    last_user_prompt = st.session_state.messages[-1]["content"]
    
    with st.chat_message("assistant", avatar="🤖"):
        placeholder = st.empty()
        # Restored the letter-by-letter typing animation
        placeholder.markdown("<div class='typewriter-loader'>CONSULTING KNOWLEDGE BASE...</div>", unsafe_allow_html=True)
        
        try:
            full_response = get_chat_response(last_user_prompt, st.session_state.session_id)
            placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            placeholder.error("Service connection interrupted.")