from pydantic import BaseModel
from typing import List, Optional

class Product(BaseModel):
    id: str
    sku: str
    name: str
    price: float
    in_stock: bool
    url: str
    compatibility: Optional[str] = None

class SearchRequest(BaseModel):
    query: str
    site: str  # 'billigpropel' or 'yamahareservedele'

class SearchResponse(BaseModel):
    products: List[Product]