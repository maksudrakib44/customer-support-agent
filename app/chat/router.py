from fastapi import APIRouter, Depends, HTTPException
from app.chat.request import ChatRequest, ChatResponse
from app.chat.service import ChatService

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/message", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        return await ChatService.process_message(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))