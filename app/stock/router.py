from fastapi import APIRouter, Depends
from app.stock.request import StockRequest, StockResponse
from app.stock.service import StockService

router = APIRouter(prefix="/product", tags=["Stock"])

@router.get("/stock", response_model=StockResponse)
async def check_stock(request: StockRequest = Depends()):
    return await StockService.check_stock(request)