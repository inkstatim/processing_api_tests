class Cards:
    SUCCESS_CARD = lambda year: {
        "email": "card@success.com",
        "number": "4149011500000147",
        "expiry": {
            "month": "10",
            "year": year
        },
        "holder": "test user",
        "cvc": "123",
        "needSave": 'true'
    }

    EXPIRED_CARD = lambda year: {
        "email": "card@datainvalid.com",
        "number": "4149011500000147",
        "expiry": {
            "month": "10",
            "year": year
        },
        "holder": "test user",
        "cvc": "123",
        "needSave": 'false'
    }

    CARD_WITH_EMPTY_CVV = lambda year: {
        "email": "card@withoutcvv.com",
        "number": "4149011500000147",
        "expiry": {
            "month": "10",
            "year": year
        },
        "holder": "test user",
        "cvc": "",
        "needSave": 'false'
    }

    CARD_DECLINE_41 = lambda year: {
        "email": "card@decline41.com",
        "number": "4532904789286871",
        "expiry": {
            "month": "10",
            "year": year
        },
        "holder": "test user",
        "cvc": "123",
        "needSave": 'false'
    }

    CARD_DECLINE_51 = lambda year: {
        "email": "card@decline51.com",
        "number": "4024007119078466",
        "expiry": {
            "month": "10",
            "year": year
        },
        "holder": "test user",
        "cvc": "123",
        "needSave": 'false'
    }

    REFUND_PAYMENT = {
        "sum": "100",
        "currency": "USD",
        "cause": {
            "reason": "Requested by customer",
            "comment": "test comment"
        }
    }
