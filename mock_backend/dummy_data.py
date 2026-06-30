orders = [
    {"order_number": "ORD-001", "customer_email": "john@example.com", "status": "shipped", "tracking_number": "GL987654321", "carrier": "GLS", "estimated_delivery": "2026-06-30", "shipped_date": "2026-06-26"},
    {"order_number": "ORD-002", "customer_email": "sarah@example.com", "status": "processing", "tracking_number": None, "carrier": None, "estimated_delivery": "2026-07-03", "shipped_date": None},
    {"order_number": "ORD-1001", "customer_email": "john@example.com", "status": "delivered", "tracking_number": "DAO123456789", "carrier": "DAO", "estimated_delivery": "2026-06-28", "shipped_date": "2026-06-25"},
    {"order_number": "ORD-1002", "customer_email": "maria@example.com", "status": "processing", "tracking_number": None, "carrier": None, "estimated_delivery": "2026-07-04", "shipped_date": None},
    {"order_number": "ORD-1003", "customer_email": "test@example.com", "status": "shipped", "tracking_number": "GLS555000111", "carrier": "GLS", "estimated_delivery": "2026-07-01", "shipped_date": "2026-06-29"},
]
products = [
    {"id": "prod-001", "sku": "NDX-115", "name": "AquaDrive 115 Propeller", "price": 2999, "site": "northdock", "in_stock": True, "quantity": 15, "url": "https://northdock.test/products/ndx-115", "compatibility": "AquaDrive 115"},
    {"id": "prod-002", "sku": "MX-SKIT-01", "name": "AquaDrive 115 Service Kit", "price": 899, "site": "marinexparts", "in_stock": False, "quantity": 0, "restock_date": "2026-07-10", "url": "https://marinexparts.test/products/mx-skit-01", "compatibility": "AquaDrive 115"},
    {"id": "prod-003", "sku": "ND-PROP-13-19", "name": "13 x 19 Aluminium Propeller", "price": 1299, "site": "northdock", "in_stock": True, "quantity": 8, "url": "https://northdock.test/products/nd-prop-13-19", "compatibility": "AquaDrive 90-115 HP"},
    {"id": "prod-004", "sku": "MX-OIL-10W30", "name": "Marine Engine Oil 10W-30", "price": 159, "site": "marinexparts", "in_stock": True, "quantity": 42, "url": "https://marinexparts.test/products/mx-oil-10w30", "compatibility": "AquaDrive outboards"},
    {"id": "prod-005", "sku": "MX-FILTER-115", "name": "AquaDrive 115 Oil Filter", "price": 119, "site": "marinexparts", "in_stock": True, "quantity": 25, "url": "https://marinexparts.test/products/mx-filter-115", "compatibility": "AquaDrive 115"},
]
shipping_methods = [
    {"name": "GLS", "days_min": 1, "days_max": 2, "cost": 49},
    {"name": "DAO Home Delivery", "days_min": 2, "days_max": 4, "cost": 69},
    {"name": "Pickup Point", "days_min": 1, "days_max": 3, "cost": 39},
]
context_data = [
    {"keywords": ["propeller", "115"], "context": "Customers with AquaDrive 115 often ask for 13 x 19 aluminium propellers. Stock should still be verified through the stock tool.", "source": "past_conversation"},
    {"keywords": ["service kit", "filter", "oil"], "context": "For AquaDrive 115 maintenance, customers commonly buy a service kit, oil filter, and 10W-30 marine engine oil together.", "source": "support_article"},
    {"keywords": ["shipping", "delivery", "GLS"], "context": "GLS is usually the fastest shipping option in Denmark, while pickup point is the lowest-cost option.", "source": "shipping_faq"},
]
conversation_history = {
    "john@example.com": [{"role": "user", "content": "Hello"}, {"role": "assistant", "content": "Hi!"}],
    "maria@example.com": [{"role": "user", "content": "I need parts for my AquaDrive 115"}, {"role": "assistant", "content": "I can help find compatible AquaDrive 115 parts."}],
    "test@example.com": [],
}
