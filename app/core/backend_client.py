import httpx
import logging
from typing import Optional, Any
from config import settings

logger = logging.getLogger(__name__)

# We need to import settings from root. 
# Wait, root config is at project root, but we use `from config import settings`.
# Since main.py is at root, and app/core is subdir, we need relative or absolute.
# Let's use absolute import from root.
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))
from config import settings

class BackendClient:
    def __init__(self):
        self.base_url = settings.BACKEND_BASE_URL.rstrip('/')
        self.client = httpx.AsyncClient(
            timeout=settings.REQUEST_TIMEOUT,
            headers={"Authorization": f"Bearer {settings.API_KEY}"}
        )
    
    async def close(self):
        await self.client.aclose()
    
    async def _request(self, method: str, endpoint: str, **kwargs) -> Optional[Any]:
        url = f"{self.base_url}{endpoint}"
        try:
            response = await self.client.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Backend request failed: {e}")
            return None
    
    async def get_order_status(self, order_number: str, email: str = None):
        params = {"order_number": order_number}
        if email: params["email"] = email
        return await self._request("GET", "/api/order/status", params=params)
    
    async def check_stock(self, sku: str):
        return await self._request("GET", "/api/product/stock", params={"sku": sku})
    
    async def search_products(self, query: str, site: str):
        return await self._request("GET", "/api/product/search", params={"query": query, "site": site})
    
    async def estimate_shipping(self, product_ids: list, postal_code: str, country: str):
        return await self._request("GET", "/api/shipping/estimate", params={"product_ids": product_ids, "postal_code": postal_code, "country": country})
    
    async def forward_to_human(self, conversation_id: str, customer_email: str, question: str, ai_attempt: str):
        body = {"conversation_id": conversation_id, "customer_email": customer_email, "question": question, "ai_attempt": ai_attempt}
        return await self._request("POST", "/api/forward-to-human", json=body)
    
    async def update_case_status(self, conversation_id: str, status: str, resolution_summary: str = None):
        body = {"conversation_id": conversation_id, "status": status, "resolution_summary": resolution_summary}
        return await self._request("POST", "/api/case/status", json=body)
    
    async def log_conversation(self, conversation_id: str, customer_email: str, question: str, ai_answer: str, redirected_to_human: bool, timestamp: str, was_helpful: bool = None):
        body = {"conversation_id": conversation_id, "customer_email": customer_email, "question": question, "ai_answer": ai_answer, "was_helpful": was_helpful, "redirected_to_human": redirected_to_human, "timestamp": timestamp}
        return await self._request("POST", "/api/conversation/log", json=body)
    
    async def get_context(self, query: str, email: str = None):
        params = {"query": query}
        if email: params["email"] = email
        return await self._request("GET", "/api/context", params=params)
    
    async def get_conversation_history(self, email: str, limit: int = 10):
        return await self._request("GET", "/api/conversation/history", params={"email": email, "limit": limit}) or []

backend_client = BackendClient()