from app.core.backend_client import backend_client

async def handle_get_order_status(arguments: dict, email: str = None):
    order_number = arguments.get("order_number")
    customer_email = arguments.get("email") or email
    if not order_number:
        return {"error": "order_number is required"}
    result = await backend_client.get_order_status(order_number, customer_email)
    return result or {"error": "Order not found"}