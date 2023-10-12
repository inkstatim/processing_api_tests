class MerchantSchema:
    GET = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
                "paymentTypes": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            },
            "required": ["id", "name", "paymentTypes"]
        }
    }
