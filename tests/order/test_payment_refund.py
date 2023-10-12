import pytest

import allure
from enums.constants import Constants
from enums.db_tables import Tables


class TestPaymentRefund:

    @allure.description("Refund payment for order")
    @pytest.mark.case("QA- (1.0)")
    def test_payment_refund(self, user_creds, order, card, refund_payment, api_clients, db_connector):
        with allure.step("create user"):
            user = api_clients.auth_api.create_user(user_creds)
        with allure.step("set sign order to user"):
            api_clients.auth_api.set_sign_order_to_user(user, order)
        with allure.step("create order & extract session_id"):
            order_resp = api_clients.order_api.create_order(user, Constants.SHOP_ID, order).text
            session_id = order_resp["sessions"][0]["id"]
            order_id = order_resp["id"]
        with allure.step("create payment page and extract page_id"):
            payment_page_resp = api_clients.payment_page_api.create_payment_page(session_id).text
            page_id = payment_page_resp["paymentPage"]["id"]
        with allure.step("make payment via card"):
            api_clients.card_payment_api.make_payment(session_id, page_id, card)
        with allure.step("refund payment"):
            api_clients.card_payment_api.refund_payment(order_id, refund_payment)
        with allure.step("check payment & operation in db"):
            assert db_connector.select(Tables.PAYMENT, "order_id", order_id)
            assert db_connector.select(Tables.OPERATION, "order_id", order_id)
