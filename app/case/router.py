from fastapi import APIRouter
from app.case.request import CaseStatusRequest, CaseStatusResponse
from app.case.service import CaseService

router = APIRouter(prefix="/case", tags=["Case"])

@router.post("/status", response_model=CaseStatusResponse)
async def update_case_status(request: CaseStatusRequest):
    return await CaseService.update_case_status(request)