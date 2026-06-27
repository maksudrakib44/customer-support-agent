from app.core.backend_client import backend_client

async def handle_check_stock(arguments: dict):
    sku = arguments.get("product_sku")
    if not sku:
        return {"error": "product_sku is required"}
    result = await backend_client.check_stock(sku)
    return result or {"error": "Product not found"}