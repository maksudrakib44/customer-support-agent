orders = [
    {"order_number": "ORD-001", "customer_email": "john@example.com", "status": "shipped", "tracking_number": "GL987654321", "carrier": "GLS", "estimated_delivery": "2026-06-30", "shipped_date": "2026-06-26"},
    {"order_number": "ORD-002", "customer_email": "sarah@example.com", "status": "processing", "tracking_number": None, "carrier": None, "estimated_delivery": "2026-07-03", "shipped_date": None}
]
products = [
    {"sku": "YAM-F115", "name": "Yamaha F115 Propeller", "price": 2999, "site": "billigpropel", "in_stock": True, "quantity": 15, "url": "https://...", "compatibility": "F115"},
    {"sku": "YAM-SKIT-01", "name": "Service Kit", "price": 899, "site": "billigpropel", "in_stock": False, "quantity": 0, "restock_date": "2026-07-10", "url": "https://...", "compatibility": "F115"}
]
shipping_methods = [{"name": "GLS", "days_min": 1, "days_max": 2, "cost": 49}]
context_data = [{"keywords": ["propeller", "F115"], "context": "Previous customer asked about F115. We had 5 in stock.", "source": "past"}]
conversation_history = {
    "john@example.com": [{"role": "user", "content": "Hello"}, {"role": "assistant", "content": "Hi!"}]
}