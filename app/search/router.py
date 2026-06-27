from fastapi import APIRouter, Depends
from app.search.request import SearchRequest, SearchResponse
from app.search.service import SearchService

router = APIRouter(prefix="/product", tags=["Search"])

@router.get("/search", response_model=SearchResponse)
async def search_products(request: SearchRequest = Depends()):
    return await SearchService.search_products(request)