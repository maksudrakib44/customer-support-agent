from typing import List
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from mock_backend.dummy_data import orders, products, shipping_methods, context_data, conversation_history

app = FastAPI(title="Mock Backend")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/api/order/status")
async def order_status(order_number: str, email: str = None):
    for o in orders:
        if o["order_number"] == order_number:
            if email and o["customer_email"] != email: continue
            return {k: v for k, v in o.items() if k != "customer_email"}
    raise HTTPException(404, "Order not found")

@app.get("/api/product/stock")
async def check_stock(sku: str):
    for p in products:
        if p["sku"] == sku:
            return {"in_stock": p["in_stock"], "quantity": p.get("quantity", 0), "restock_date": p.get("restock_date")}
    raise HTTPException(404, "Product not found")

@app.get("/api/product/search")
async def search_products(query: str, site: str):
    return {"products": [p for p in products if query.lower() in p["name"].lower() and p["site"] == site]}

@app.get("/api/shipping/estimate")
async def estimate_shipping(product_ids: List[str] = Query(...), postal_code: str = "", country: str = ""):
    return {"methods": shipping_methods}

@app.post("/api/forward-to-human")
async def forward_to_human(body: dict):
    return {"ticket_id": "TICKET-001", "oss_url": "https://supportdesk.test/ticket/001"}

@app.post("/api/case/status")
async def case_status(body: dict):
    return {"success": True}

@app.post("/api/conversation/log")
async def log_conversation(body: dict):
    return {"success": True}

@app.get("/api/context")
async def get_context(query: str, email: str = None):
    for ctx in context_data:
        if any(k.lower() in query.lower() for k in ctx["keywords"]):
            return {"context": ctx["context"], "sources": [ctx["source"]]}
    return {"context": None, "sources": []}

@app.get("/api/conversation/history")
async def get_history(email: str, limit: int = 10):
    return conversation_history.get(email, [])[-limit:]
