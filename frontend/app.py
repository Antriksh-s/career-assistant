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
st.title("🤖 AI Assistant")
st.caption("Powered by RAG (Retrieval-Augmented Generation) & GPT-4o-mini")


# 5. Prompt Suggestions
st.markdown("### 💡 Explore Antriksh's Expertise")

# Create two rows of three buttons for a clean grid
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

def handle_click(prompt):
    st.session_state.suggestion_clicked = prompt

# Row 1
cols1 = st.columns(3)
for i, prompt in enumerate(suggestions_row1):
    if cols1[i].button(prompt, use_container_width=True):
        handle_click(prompt)

# Row 2
cols2 = st.columns(3)
for i, prompt in enumerate(suggestions_row2):
    if cols2[i].button(prompt, use_container_width=True):
        handle_click(prompt)

# Logic to handle the click and trigger the RAG response
if "suggestion_clicked" in st.session_state and st.session_state.suggestion_clicked:
    current_prompt = st.session_state.suggestion_clicked
    st.session_state.suggestion_clicked = None  # Reset state
    
    # Add user message to UI
    st.session_state.messages.append({"role": "user", "content": current_prompt})
    with st.chat_message("user", avatar="👨‍💻"):
        st.markdown(current_prompt)

    with st.chat_message("assistant", avatar="🤖"):
        message_placeholder = st.empty()
        message_placeholder.markdown("🔍 *Scanning career database...*")
        try:
            # Directly calling the engine (Monolith Approach)
            full_response = get_chat_response(current_prompt, st.session_state.session_id)
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"Error: {e}")


# 6. State Management
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []

# 7. Display Chat History with Professional Avatars
for msg in st.session_state.messages:
    avatar = "👨‍💻" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# 8. Chat Input & Direct Logic Execution
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