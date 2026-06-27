from app.core.backend_client import backend_client

async def handle_forward_to_human(arguments: dict, email: str = None):
    reason = arguments.get("reason", "No reason")
    if not email:
        return {"error": "email required"}
    result = await backend_client.forward_to_human(
        conversation_id=f"conv_{email}",
        customer_email=email,
        question="",
        ai_attempt=reason
    )
    return result or {"ticket_id": "ERROR", "oss_url": ""}