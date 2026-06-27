from app.core.backend_client import backend_client

async def handle_estimate_shipping(arguments: dict):
    product_ids = arguments.get("product_ids")
    postal_code = arguments.get("postal_code")
    country = arguments.get("country")
    if not all([product_ids, postal_code, country]):
        return {"error": "Missing required fields"}
    result = await backend_client.estimate_shipping(product_ids, postal_code, country)
    return result or {"methods": []}