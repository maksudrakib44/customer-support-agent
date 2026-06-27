TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "get_order_status",
            "description": "Get delivery/shipping status of an order. Use this when customer asks about their order, delivery, or shipment.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_number": {
                        "type": "string",
                        "description": "The order number provided by the customer"
                    },
                    "email": {
                        "type": "string",
                        "description": "Customer email address for verification (optional)"
                    }
                },
                "required": ["order_number"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_stock",
            "description": "Check if a product is in stock and when it will be restocked. Use this when customer asks about product availability.",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_sku": {
                        "type": "string",
                        "description": "The product SKU (e.g., YAM-F115, YAM-SKIT-01)"
                    }
                },
                "required": ["product_sku"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_products",
            "description": "Search for products on Billigpropel.dk or YamahaReservedele.dk. Use this when customer asks for recommendations or wants to find specific products.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query (e.g., propeller, service kit, Yamaha 115)"
                    },
                    "site": {
                        "type": "string",
                        "enum": ["billigpropel", "yamahareservedele"],
                        "description": "Which site to search. Use billigpropel for main products, yamahareservedele for Yamaha parts."
                    }
                },
                "required": ["query", "site"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "estimate_shipping",
            "description": "Estimate shipping time and cost for products. Use this when customer asks about delivery time or shipping cost.",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of product IDs to estimate shipping for"
                    },
                    "postal_code": {
                        "type": "string",
                        "description": "Customer postal code"
                    },
                    "country": {
                        "type": "string",
                        "description": "Customer country code (e.g., DK)"
                    }
                },
                "required": ["product_ids", "postal_code", "country"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "forward_to_human",
            "description": "Forward conversation to human support. Use this when: 1) You cannot answer the question, 2) The customer asks to speak to a human, 3) The query requires human judgment.",
            "parameters": {
                "type": "object",
                "properties": {
                    "reason": {
                        "type": "string",
                        "description": "Reason for forwarding to human"
                    }
                },
                "required": ["reason"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "close_case",
            "description": "Close the support case after successful resolution. Call this when the customer's question has been fully answered.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "reopen_case",
            "description": "Reopen a previously closed case. Call this when a customer with a closed case sends a new message.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }
]