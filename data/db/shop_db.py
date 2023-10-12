class ShopsDb:
    SHOP_PAYMENT_TYPE = lambda shop_id, created_at: {
        "shop_id": shop_id,
        "instrument_type": "card",
        "settings_id": 1,
        "is_default": True,
        "created_at": created_at
    }
