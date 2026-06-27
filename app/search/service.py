from app.search.request import SearchRequest, SearchResponse, Product
from app.core.backend_client import backend_client

class SearchService:
    @staticmethod
    async def search_products(request: SearchRequest) -> SearchResponse:
        data = await backend_client.search_products(request.query, request.site)
        products = []
        if data and data.get("products"):
            for p in data["products"]:
                products.append(Product(**p))
        return SearchResponse(products=products)