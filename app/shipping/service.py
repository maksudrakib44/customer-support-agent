from app.shipping.request import ShippingRequest, ShippingResponse, ShippingMethod
from app.core.backend_client import backend_client

class ShippingService:
    @staticmethod
    async def estimate_shipping(request: ShippingRequest) -> ShippingResponse:
        data = await backend_client.estimate_shipping(
            request.product_ids,
            request.postal_code,
            request.country
        )
        methods = []
        if data and data.get("methods"):
            for m in data["methods"]:
                methods.append(ShippingMethod(**m))
        return ShippingResponse(methods=methods)