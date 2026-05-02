import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import CharacterTextSplitter

load_dotenv()

# 1. SETUP THE KNOWLEDGE BASE
def initialize_knowledge_base():
    with open("my_career.txt", "r") as f:
        raw_text = f.read()
    
    # Split the text into smaller chunks so the AI can find specific facts
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    texts = text_splitter.split_text(raw_text)
    
    # Create the vector store (this is where your "knowledge" lives)
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts, embeddings)
    return vectorstore

# Global variable to hold the knowledge
vector_db = initialize_knowledge_base()

memory_store = {}

def get_chat_response(user_input: str, session_id: str):
    if session_id not in memory_store:
        memory_store[session_id] = [
            SystemMessage(content="You are a professional Career Assistant. Use the provided context about the candidate to answer recruiter questions. If the information isn't in the context, say you don't know—don't make things up.")
        ]
    
    # 2. RETRIEVE RELEVANT FACTS
    # Search your text file for parts relevant to the user's question
    relevant_docs = vector_db.similarity_search(user_input, k=3)
    context = "\n".join([doc.page_content for doc in relevant_docs])
    
    # 3. CONSTRUCT THE PROMPT
    # We "stuff" the retrieved facts into the message
    augmented_user_input = f"Context about the candidate:\n{context}\n\nQuestion: {user_input}"
    
    history = memory_store[session_id]
    if len(history) > 11:
        history = [history[0]] + history[-10:]
    
    history.append(HumanMessage(content=augmented_user_input))
    
    # 4. CALL LLM
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0) # Lower temperature for factual accuracy
    response = llm.invoke(history)
    
    history.append(AIMessage(content=response.content))
    memory_store[session_id] = history
    
    return response.content