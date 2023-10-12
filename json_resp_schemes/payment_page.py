class PaymentPageSchema:
    PUT_GET = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "shop": {
                "type": "object",
                "properties": {
                    "redirectToShopSuccessUrl": {"type": "string", "format": "uri"},
                    "name": {"type": "string"},
                    "redirectToShopFailUrl": {"type": "string", "format": "uri"},
                    "url": {"type": "string", "format": "uri"},
                    "logoUrl": {"type": "string", "format": "uri"}
                },
                "required": ["redirectToShopSuccessUrl", "name", "redirectToShopFailUrl", "url", "logoUrl"]
            },
            "order": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    # toDO fix amount_pattern after https://transfintech.atlassian.net/browse/API-481:
                    "amount": {"type": "string", "pattern": "^[0-9]+(\.[0-9]{1,9})?$"},  # noqa W605
                    "currency": {"type": "string"},
                    "status": {"type": "string"},
                    "expirationTimeout": {"type": "integer"}
                },
                "required": ["id", "amount", "currency", "status", "expirationTimeout"]
            },
            "paymentSession": {
                "type": "object",
                "properties": {
                    "status": {"type": "string"}
                },
                "required": ["status"]
            },
            "operation": {
                "type": "object",
                "properties": {
                    "status": {"type": "string"}
                },
                "required": ["status"]
            },
            "secure": {
                "type": "object",
                "properties": {
                    "status": {"type": "string"}
                },
                "required": ["status"]
            },
            "capture": {
                "type": "object",
                "properties": {
                    "status": {"type": "string"}
                },
                "required": ["status"]
            },
            "settlement": {
                "type": "object",
                "properties": {
                    "status": {"type": "string"}
                },
                "required": ["status"]
            },
            "isCardHolderNameRequired": {"type": "boolean"},
            "isBillEmailRequired": {"type": "boolean"},
            "paymentPage": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "status": {"type": "string"},
                    "secureUrl": {"type": ["string", "null"], "format": "uri"}
                },
                "required": ["id", "status"]
            },
            "paymentResponse": {
                "type": "object",
                "properties": {
                    "instrumentType": {"type": "string"},
                    "status": {"type": "string"}
                },
                "required": ["instrumentType", "status"]
            }
        },
        "required": ["shop", "order", "paymentSession", "operation", "secure", "capture", "settlement",
                     "isCardHolderNameRequired", "isBillEmailRequired", "paymentPage", "paymentResponse"]
    }
