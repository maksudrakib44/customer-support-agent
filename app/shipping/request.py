from pydantic import BaseModel
from typing import List

class ShippingMethod(BaseModel):
    name: str
    days_min: int
    days_max: int
    cost: float

class ShippingRequest(BaseModel):
    product_ids: List[str]
    postal_code: str
    country: str

class ShippingResponse(BaseModel):
    methods: List[ShippingMethod]