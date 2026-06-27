import time

def generate_conversation_id(email: str) -> str:
    timestamp = int(time.time())
    return f"conv_{email}_{timestamp}"

def format_price(price: float, currency: str = "DKK") -> str:
    return f"{price:.2f} {currency}"