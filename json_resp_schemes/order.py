class OrderSchema:
    POST = {
        "type": "object",
        "properties": {
            "customOrderId": {"type": "string"},
            "id": {"type": "integer"},
            "sessions": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "status": {"type": "string"},
                        "url": {"type": "string"}
                    },
                    "required": ["id", "status", "url"]
                }
            },
            "status": {"type": "string"}
        },
        "required": ["customOrderId", "id", "sessions", "status"]
    }
