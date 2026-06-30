from typing import List
from fastapi import APIRouter, Query
from app.shipping.request import ShippingRequest, ShippingResponse
from app.shipping.service import ShippingService

router = APIRouter(prefix="/shipping", tags=["Shipping"])

@router.get("/estimate", response_model=ShippingResponse)
async def estimate_shipping(
    product_ids: List[str] = Query(...),
    postal_code: str = Query(...),
    country: str = Query(...),
):
    request = ShippingRequest(
        product_ids=product_ids,
        postal_code=postal_code,
        country=country,
    )
    return await ShippingService.estimate_shipping(request)
