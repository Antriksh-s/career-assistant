import streamlit as st
import requests
import uuid

# 1. Page Configuration
st.set_page_config(
    page_title="Antriksh Singh | AI Career Assistant",
    page_icon="🤖",
    layout="wide"
)

# 2. Sidebar for Portfolio Details
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

# 3. Main Interface Header
st.title("🤖 AI Career Assistant")
st.caption("Powered by RAG (Retrieval-Augmented Generation) & GPT-4o-mini")

# 4. State Management
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. Display Chat History with Professional Avatars
for msg in st.session_state.messages:
    avatar = "👨‍💻" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# 6. Chat Input & Backend Logic
if prompt := st.chat_input("Ask me about Antriksh's experience..."):
    # Add user message to UI
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👨‍💻"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🤖"):
        message_placeholder = st.empty()
        message_placeholder.markdown("🔍 *Scanning career database...*")
        
        try:
            response = requests.post(
                "http://localhost:8000/chat",
                json={"message": prompt, "session_id": st.session_state.session_id},
                timeout=10
            )
            
            if response.status_code == 200:
                full_response = response.json()["response"]
                message_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            else:
                message_placeholder.error(f"Error: {response.status_code}")
                
        except Exception as e:
            message_placeholder.error("Backend unreachable. Ensure the FastAPI server is running.")