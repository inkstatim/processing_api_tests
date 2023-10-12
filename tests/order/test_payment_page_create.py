from jsonschema.validators import validate

import allure
import pytest

from enums.constants import Constants
from json_resp_schemes.payment_page import PaymentPageSchema


class TestPaymentPageCreate:

    @allure.description("Creating payment page")
    @pytest.mark.case("QA-T101 (1.0)")
    def test_payment_page_create(self, user_creds, order, api_clients):
        with allure.step("create user"):
            user = api_clients.auth_api.create_user(user_creds)
        with allure.step("set sign order to user"):
            api_clients.auth_api.set_sign_order_to_user(user, order)
        with allure.step("create order & extract session_id"):
            order_resp = api_clients.order_api.create_order(user, Constants.SHOP_ID, order).text
            session_id = order_resp["sessions"][0]["id"]
        with allure.step("create payment page"):
            payment_page_resp = api_clients.payment_page_api.create_payment_page(session_id).text
            validate(payment_page_resp, PaymentPageSchema.PUT_GET)
        with allure.step("check payment page status"):
            payment_page_status = payment_page_resp['paymentPage'].get('status', {})
            assert payment_page_status == 'created', \
                f"actual status of payment_page {payment_page_status}, but expected 'created'"
