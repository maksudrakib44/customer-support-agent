from app.stock.request import StockRequest, StockResponse
from app.core.backend_client import backend_client

class StockService:
    @staticmethod
    async def check_stock(request: StockRequest) -> StockResponse:
        data = await backend_client.check_stock(request.sku)
        if not data:
            return StockResponse(in_stock=False, quantity=0)
        return StockResponse(**data)