from clients.auth_api import AuthApi
from clients.backoffice_api import BackofficeApi
from clients.card_payment_api import CardPaymentApi
from clients.merchant_api import MerchantApi
from clients.order_api import OrderApi
from clients.payment_page_api import PaymentPageApi


class ApiManager:
    def __init__(self, session):
        self.auth_api = AuthApi(session)
        self.order_api = OrderApi(session)
        self.backoffice_api = BackofficeApi(session)
        self.card_payment_api = CardPaymentApi(session)
        self.merchant_api = MerchantApi(session)
        self.payment_page_api = PaymentPageApi(session)
