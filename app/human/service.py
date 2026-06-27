from app.human.request import ForwardRequest, ForwardResponse
from app.core.backend_client import backend_client

class HumanService:
    @staticmethod
    async def forward_to_human(request: ForwardRequest) -> ForwardResponse:
        data = await backend_client.forward_to_human(
            request.conversation_id,
            request.customer_email,
            request.question,
            request.ai_attempt
        )
        return ForwardResponse(**data)