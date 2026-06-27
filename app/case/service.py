from app.case.request import CaseStatusRequest, CaseStatusResponse
from app.core.backend_client import backend_client

class CaseService:
    @staticmethod
    async def update_case_status(request: CaseStatusRequest) -> CaseStatusResponse:
        data = await backend_client.update_case_status(
            request.conversation_id,
            request.status,
            request.resolution_summary
        )
        if data and data.get("success"):
            return CaseStatusResponse(success=True)
        return CaseStatusResponse(success=False, message="Update failed")