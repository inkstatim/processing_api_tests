# toDO когда реализуют создание магазинов через API:
class Merchant:
    SHOP = {
        "id": 2,
        "name": "myromashka eu",
        "paymentTypes": [
            "card"
        ]
    }

    ORDER_LIST = {
        "pages": {
            "quantity": 20,
            "page": 1
        }
    }

    ORDER_SEARCH = lambda order_number: {
        "number": order_number
    }
