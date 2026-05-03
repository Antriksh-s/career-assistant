import sys
import os
import uuid
import streamlit as st
import time

# 1. PATH FIX
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.engine import get_chat_response

# 2. Page Configuration & Custom CSS
st.set_page_config(
    page_title="Antriksh Singh | AI Career Assistant",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS for colors, animations, and smooth UI
st.markdown("""
<style>
    /* Chat message styling */
    .stChatMessage {
        border-radius: 15px;
        padding: 10px;
        margin-bottom: 10px;
    }
    
    /* Custom Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #0e1117;
    }

    /* Pulse animation for the loader */
    @keyframes pulse {
        0% { opacity: 0.4; }
        50% { opacity: 1; }
        100% { opacity: 0.4; }
    }
    .loading-text {
        font-style: italic;
        color: #00ffa2;
        animation: pulse 1.5s infinite;
    }
</style>
""", unsafe_allow_html=True)

# 3. State Management
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []
if "active_prompt" not in st.session_state:
    st.session_state.active_prompt = None

# 4. Sidebar
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
    
    if st.button("Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# 5. Main Interface Header
st.title("🤖 AI Career Assistant")
st.caption("Advanced RAG Engine | GPT-4o-mini | SRE Knowledge Base")

# 6. Prompt Suggestions
st.markdown("#### 💡 Suggested Queries")
def handle_click(prompt_text):
    st.session_state.active_prompt = prompt_text

suggestions = [
    "Tell me about your AI-driven SLO breach prediction project.",
    "How did you reduce Datadog costs by 30%?",
    "Explain your experience with Self-Healing Infrastructure.",
    "What are your top skills in Agentic AI and RAG?",
    "Show me your automation work with Ansible and Python.",
    "Tell me about your cloud migrations to AWS ECS Fargate."
]

# Grid layout for suggestions
cols = st.columns(3)
for i, prompt in enumerate(suggestions):
    if cols[i % 3].button(prompt, use_container_width=True):
        handle_click(prompt)

# 7. Unified Input Logic
chat_input = st.chat_input("Ask about my experience...")
final_prompt = None

if chat_input:
    final_prompt = chat_input
elif st.session_state.active_prompt:
    final_prompt = st.session_state.active_prompt
    st.session_state.active_prompt = None

if final_prompt:
    st.session_state.messages.append({"role": "user", "content": final_prompt})
    st.rerun()

# 8. Display Chat History
chat_container = st.container()
with chat_container:
    for msg in st.session_state.messages:
        avatar = "👨‍💻" if msg["role"] == "user" else "🤖"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

# 9. Response Logic with Animation
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    last_user_prompt = st.session_state.messages[-1]["content"]
    
    with st.chat_message("assistant", avatar="🤖"):
        # Animated placeholder
        with st.status("🧠 Analyzing request and querying career logs...", expanded=True) as status:
            st.write("Searching vector database...")
            time.sleep(0.5) # Small aesthetic pause
            st.write("Retrieving SRE context...")
            
            try:
                full_response = get_chat_response(last_user_prompt, st.session_state.session_id)
                status.update(label="✅ Analysis Complete", state="complete", expanded=False)
                
                # Final display with auto-scroll focus
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                
                # Hidden anchor for auto-scroll
                st.markdown('<div id="end-of-chat"></div>', unsafe_allow_html=True)
                
            except Exception as e:
                status.update(label="❌ Error", state="error")
                st.error(f"Engine failure: {e}")