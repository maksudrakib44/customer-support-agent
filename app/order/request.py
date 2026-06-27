from pydantic import BaseModel

class OrderStatusRequest(BaseModel):
    order_number: str
    email: str = None

class OrderStatusResponse(BaseModel):
    status: str
    tracking_number: str = None
    carrier: str = None
    estimated_delivery: str = None
    shipped_date: str = None