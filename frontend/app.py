import sys
import os

# 1. PATH FIX: Adds the root directory to the python path 
# so Streamlit Cloud can find the 'backend' folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import uuid
# Import the engine logic directly for a monolith architecture
from backend.engine import get_chat_response

# 2. Page Configuration
st.set_page_config(
    page_title="Antriksh Singh | AI Career Assistant",
    page_icon="🤖",
    layout="wide"
)

# 3. Sidebar for Portfolio Details
with st.sidebar:
    st.title("👨‍💻 Candidate Profile")
    st.markdown("""
    **Antriksh Singh**  
    *DevOps & SRE Specialist*  
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

# 4. Main Interface Header
st.title("🤖 AI Career Assistant")
st.caption("Powered by RAG (Retrieval-Augmented Generation) & GPT-4o-mini")

# 5. State Management
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []

# 6. Display Chat History with Professional Avatars
for msg in st.session_state.messages:
    avatar = "👨‍💻" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# 7. Chat Input & Direct Logic Execution
if prompt := st.chat_input("Ask me about Antriksh's experience..."):
    # Add user message to UI
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👨‍💻"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🤖"):
        message_placeholder = st.empty()
        message_placeholder.markdown("🔍 *Scanning career database...*")
        
        try:
            # MONOLITH UPDATE: Calling the function directly instead of using requests.post
            full_response = get_chat_response(prompt, st.session_state.session_id)
            
            # Display result
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
                
        except Exception as e:
            # Helpful error message for missing secrets/environment variables
            if "OPENAI_API_KEY" in str(e):
                st.error("Missing OpenAI API Key. Please add it to your Streamlit Secrets.")
            else:
                st.error(f"An unexpected error occurred: {e}")