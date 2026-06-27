from fastapi import APIRouter, Depends
from app.shipping.request import ShippingRequest, ShippingResponse
from app.shipping.service import ShippingService

router = APIRouter(prefix="/shipping", tags=["Shipping"])

@router.get("/estimate", response_model=ShippingResponse)
async def estimate_shipping(request: ShippingRequest = Depends()):
    return await ShippingService.estimate_shipping(request)