from fastapi import FastAPI
from backend.schemas import ChatRequest, ChatResponse
from backend.engine import get_chat_response

app = FastAPI(title="SRE Support Bot")

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    answer = get_chat_response(request.message, request.session_id)
    return ChatResponse(response=answer, session_id=request.session_id)