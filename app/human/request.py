from pydantic import BaseModel

class ForwardRequest(BaseModel):
    conversation_id: str
    customer_email: str
    question: str
    ai_attempt: str

class ForwardResponse(BaseModel):
    ticket_id: str
    oss_url: str