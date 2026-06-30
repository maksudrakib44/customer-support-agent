from app.core.backend_client import backend_client


async def handle_get_order_status(arguments: dict, email: str = None):
    order_number = arguments.get("order_number")
    customer_email = arguments.get("email") or email
    if not order_number:
        return {"error": "order_number is required"}
    result = await backend_client.get_order_status(order_number, customer_email)
    return result or {"error": "Order not found"}


async def handle_check_stock(arguments: dict):
    sku = arguments.get("product_sku")
    if not sku:
        return {"error": "product_sku is required"}
    result = await backend_client.check_stock(sku)
    return result or {"error": "Product not found"}


async def handle_search_products(arguments: dict, site: str = None):
    query = arguments.get("query")
    search_site = arguments.get("site") or site
    if not query:
        return {"error": "query is required"}
    if not search_site:
        return {"error": "site is required"}
    result = await backend_client.search_products(query, search_site)
    return result or {"products": []}


async def handle_estimate_shipping(arguments: dict):
    product_ids = arguments.get("product_ids")
    postal_code = arguments.get("postal_code")
    country = arguments.get("country")
    if not all([product_ids, postal_code, country]):
        return {"error": "Missing required fields"}
    result = await backend_client.estimate_shipping(product_ids, postal_code, country)
    return result or {"methods": []}


async def handle_forward_to_human(arguments: dict, email: str = None):
    reason = arguments.get("reason", "No reason")
    if not email:
        return {"error": "email required"}
    result = await backend_client.forward_to_human(
        conversation_id=f"conv_{email}",
        customer_email=email,
        question="",
        ai_attempt=reason,
    )
    return result or {"ticket_id": "ERROR", "oss_url": ""}


async def handle_close_case(arguments: dict, email: str = None):
    if not email:
        return {"error": "email required"}
    return await backend_client.update_case_status(f"conv_{email}", "closed", "Resolved by AI")


async def handle_reopen_case(arguments: dict, email: str = None):
    if not email:
        return {"error": "email required"}
    return await backend_client.update_case_status(f"conv_{email}", "reopened", None)
