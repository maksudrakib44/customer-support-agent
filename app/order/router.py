from fastapi import APIRouter, Depends
from app.order.request import OrderStatusRequest, OrderStatusResponse
from app.order.service import OrderService

router = APIRouter(prefix="/order", tags=["Order"])

@router.get("/status", response_model=OrderStatusResponse)
async def get_order_status(request: OrderStatusRequest = Depends()):
    return await OrderService.get_order_status(request)