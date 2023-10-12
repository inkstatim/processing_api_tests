from pydantic import ConfigDict, BaseModel, Field, AliasPath


EXPECTED_ORDER_RESPONSE = {
    "id": 2230,
    "status": "registered",
    "customOrderId": "27_1694100549",
    "sessions": [
        {
            "id": "1ee4d934-a3d1-67e0-bc76-dba0a4693872",
            "status": "created",
            "url": "/session/1ee4d934-a3d1-67e0-bc76-dba0a4693872"
        }
    ]
}


class Order:
    ORDER = lambda time_limit: {
        "order": {
            "sum": {
                "sum": "100",
                "currency": "USD"
            }
        },
        "customer": {
            "name": "John",
            "middleName": "John",
            "surname": "Doe",
            "phone": "+79999999999",
            "email": "john@example.com"
        },
        "paymentSettings": {
            "paymentType": "card",
            "entryMode": "card_present"
        },
        "timeLimit": time_limit
    }

    ORDER_WITHOUT_TIME_LIMIT = {
        "order": {
            "sum": {
                "sum": "100",
                "currency": "USD"
            }
        },
        "customer": {
            "name": "John",
            "middleName": "John",
            "surname": "Doe",
            "phone": "+79999999999",
            "email": "john@example.com"
        },
        "paymentSettings": {
            "paymentType": "card",
            "entryMode": "card_present"
        }
    }

    ORDER_CANCELLED = lambda order_id: {
        "orderId": order_id,
        "originator": {
            "type": "string",
            "id": 0
        }
    }

    ORDER_WITH_EMPTY_CUSTOMER_DATA = lambda time_limit: {
        "order": {
            "sum": {
                "sum": "100",
                "currency": "USD"
            }
        },
        "customer": {
            "name": "",
            "middleName": "",
            "surname": "",
            "phone": "",
            "email": ""
        },
        "paymentSettings": {
            "paymentType": "card",
            "entryMode": "card_present"
        },
        "timeLimit": time_limit
    }


class OrderCreateResponse(BaseModel):
    order_status: str = Field(validation_alias='status')
    session_status: str = Field(validation_alias=AliasPath('sessions', 0, 'status'))

    model_config = ConfigDict(extra='ignore')
