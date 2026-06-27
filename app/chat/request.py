from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    email: str = Field(..., pattern=r"^[^@]+@[^@]+\.[^@]+$")
    site: str = Field(..., pattern=r"^(billigpropel|yamahareservedele)$")

class ChatResponse(BaseModel):
    answer: str
    conversation_id: str