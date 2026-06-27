from app.chat.request import ChatRequest, ChatResponse
from app.core.agent import agent

class ChatService:
    @staticmethod
    async def process_message(request: ChatRequest) -> ChatResponse:
        result = await agent.run(
            message=request.message,
            email=request.email,
            site=request.site
        )
        return ChatResponse(
            answer=result["answer"],
            conversation_id=result["conversation_id"]
        )