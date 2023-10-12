from checkers.common_checkers import CommonCheckers
import allure
import pytest

from conftest import order_cancelled
from enums.constants import Constants


class TestOrderCancel:

    @allure.description("Order cancel by the user")
    @pytest.mark.case("******")
    @pytest.mark.skip(reason="https://***************")
    def test_order_cancel(self, user_creds, order, api_clients):
        with allure.step("create user"):
            user = api_clients.auth_api.create_user(user_creds)
        with allure.step("set signature for order"):
            api_clients.auth_api.set_sign_order_to_user(user, order)
        with allure.step("create order & extract session_id, order_id"):
            order_resp = api_clients.order_api.create_order(user, Constants.SHOP_ID, order).text
            session_id = order_resp["sessions"][0]["id"]
            order_id = order_resp["id"]
        with allure.step("create payment page & cancel order"):
            api_clients.payment_page_api.create_payment_page(session_id)
            api_clients.card_payment_api.cancel_order(order_cancelled(order_id))
        with allure.step("get order status"):
            order_status = lambda: api_clients.order_api.get_order_status(Constants.SHOP_ID, order_id).text
        with allure.step("check order status"):
            CommonCheckers.assert_val(order_status(), "status", "rejected")
