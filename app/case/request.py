from pydantic import BaseModel
from typing import Optional

class CaseStatusRequest(BaseModel):
    conversation_id: str
    status: str  # 'closed' or 'reopened'
    resolution_summary: Optional[str] = None

class CaseStatusResponse(BaseModel):
    success: bool
    message: str = "Case status updated"