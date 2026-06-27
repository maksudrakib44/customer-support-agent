from app.core.backend_client import backend_client

async def handle_close_case(arguments: dict, email: str = None):
    if not email:
        return {"error": "email required"}
    return await backend_client.update_case_status(f"conv_{email}", "closed", "Resolved by AI")

async def handle_reopen_case(arguments: dict, email: str = None):
    if not email:
        return {"error": "email required"}
    return await backend_client.update_case_status(f"conv_{email}", "reopened", None)