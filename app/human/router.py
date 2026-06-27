from fastapi import APIRouter
from app.human.request import ForwardRequest, ForwardResponse
from app.human.service import HumanService

router = APIRouter(prefix="/human", tags=["Human"])

@router.post("/forward", response_model=ForwardResponse)
async def forward_to_human(request: ForwardRequest):
    return await HumanService.forward_to_human(request)