from pydantic import BaseModel

class StockRequest(BaseModel):
    sku: str

class StockResponse(BaseModel):
    in_stock: bool
    quantity: int
    restock_date: str = None