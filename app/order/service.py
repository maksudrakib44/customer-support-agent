from app.order.request import OrderStatusRequest, OrderStatusResponse
from app.core.backend_client import backend_client

class OrderService:
    @staticmethod
    async def get_order_status(request: OrderStatusRequest) -> OrderStatusResponse:
        data = await backend_client.get_order_status(request.order_number, request.email)
        if not data:
            return OrderStatusResponse(status="not_found")
        return OrderStatusResponse(**data)