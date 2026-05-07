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

# 3. Final Multi-Theme CSS Overhaul
st.markdown("""
<style>
    /* Global alignment fix */
    .block-container { padding-top: 2rem; }
    
    /* REFINED TYPEWRITER ANIMATION 
       Fixes: Left-alignment, subtle weight, and precise reveal.
    */
    .typewriter-container {
        display: flex;
        justify-content: flex-start;
        width: 100%;
        margin-bottom: 10px;
    }

    .typewriter-loader {
        color: #10b981;
        font-family: 'Source Code Pro', monospace;
        font-size: 0.85rem;
        font-weight: 400;
        overflow: hidden;
        border-right: .15em solid #10b981;
        white-space: nowrap;
        margin: 0; /* Ensures it starts from the left */
        letter-spacing: .05em;
        animation: typing 3s steps(40, end), blink-caret .75s step-end infinite;
    }
    @keyframes typing { from { width: 0 } to { width: 22em } }
    @keyframes blink-caret { from, to { border-color: transparent } 50% { border-color: #10b981 } }

    /* DARK MODE SPECIFIC (System-driven) */
    @media (prefers-color-scheme: dark) {
        section[data-testid="stSidebar"] {
            background-color: #0e1117 !important;
        }
        section[data-testid="stSidebar"] * {
            color: #ffffff !important; /* Forces white text to stop fading */
        }
        [data-testid="stChatMessageUser"] {
            background-color: rgba(59, 130, 246, 0.15);
            border: 1px solid rgba(59, 130, 246, 0.2);
        }
        [data-testid="stChatMessageAssistant"] {
            background-color: #1a1c23;
            border: 1px solid #2d2f39;
        }
    }

    /* LIGHT MODE SPECIFIC (System-driven) */
    @media (prefers-color-scheme: light) {
        section[data-testid="stSidebar"] {
            background-color: #f1f5f9 !important; /* Solid Slate for visibility */
        }
        section[data-testid="stSidebar"] * {
            color: #1e293b !important; /* Strong slate text for light mode */
        }
        [data-testid="stChatMessageUser"] {
            background-color: #e6f0ff;
            border: 1px solid #cce3ff;
            color: #1e3a8a;
        }
        [data-testid="stChatMessageAssistant"] {
            background-color: #f0fdf4;
            border: 1px solid #dcfce7;
            color: #064e3b;
        }
    }

    /* Common Suggestion Button Styling */
    div.stButton > button {
        border-radius: 8px;
        transition: all 0.2s ease;
        border: 1px solid rgba(16, 185, 129, 0.2);
        background-color: transparent;
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
    st.caption("Senior DevOps & SRE Specialist")
    st.markdown("---")
    st.markdown("""
    **Core Credentials:**
    - ☁️ AWS Solutions Architect
    - 🐧 Red Hat Certified Engineer (RHCE)
    """)
    if st.button("Reset Session", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# 6. Header
st.title("AI Career Assistant")
st.caption("Context-aware retrieval of Antriksh's engineering experience.")

# 7. Suggestion Grid
suggestions = [
    "AI-driven SLO breach prediction",
    "Reduce Datadog costs by 30%",
    "Self-Healing Infrastructure",
    "Skills in Agentic AI and RAG",
    "Automated Vulnerability Management",
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

# 10. Response Logic with Left-Aligned Typewriter
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    last_user_prompt = st.session_state.messages[-1]["content"]
    
    with st.chat_message("assistant", avatar="🤖"):
        placeholder = st.empty()
        # Wrapper div to force left alignment
        placeholder.markdown("""
            <div class='typewriter-container'>
                <div class='typewriter-loader'>CONSULTING KNOWLEDGE BASE...</div>
            </div>
        """, unsafe_allow_html=True)
        
        try:
            full_response = get_chat_response(last_user_prompt, st.session_state.session_id)
            placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            placeholder.error("System connection interrupted.")