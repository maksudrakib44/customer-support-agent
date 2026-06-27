from app.core.backend_client import backend_client

async def handle_search_products(arguments: dict, site: str = None):
    query = arguments.get("query")
    search_site = arguments.get("site") or site
    if not query:
        return {"error": "query is required"}
    if not search_site:
        return {"error": "site is required"}
    result = await backend_client.search_products(query, search_site)
    return result or {"products": []}