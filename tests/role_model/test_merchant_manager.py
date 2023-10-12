import allure
import pytest

from data.order import EXPECTED_ORDER_RESPONSE, OrderCreateResponse
from enums.constants import Constants
from checkers.common_checkers import CommonCheckers
from conftest import order_search_data_by_id


class TestMerchantManagerPermission:

    @allure.description("Creating order for merchant account under manager's role")
    @pytest.mark.case("QA-T272 (1.0)")
    def test_merchant_manager_order_create(self, merchant_manager_creds, order, api_clients):
        with allure.step("create user"):
            user = api_clients.auth_api.create_user(merchant_manager_creds)
        with allure.step("get signature for order"):
            api_clients.auth_api.set_sign_order_to_user(user, order)
        with allure.step("create order"):
            order_resp = api_clients.order_api.create_order(user, Constants.SHOP_ID, order).text
        with allure.step("order status should be 'registered' & sessions status should be 'created'"):
            assert OrderCreateResponse.model_validate(
                EXPECTED_ORDER_RESPONSE
            ) == OrderCreateResponse.model_validate(order_resp)

    @allure.description("Viewing company shop order list for Merchant Account under manager's role")
    @pytest.mark.case("QA-T273 (1.0)")
    @pytest.mark.skip(reason="https://*********")
    def test_merchant_manager_order_list(self, merchant_manager_creds, order_list, api_clients, order):
        with allure.step("create user"):
            user = api_clients.auth_api.create_user(merchant_manager_creds)
        with allure.step("get signature for order"):
            api_clients.auth_api.set_sign_order_to_user(user, order)
        with allure.step("create order"):
            api_clients.order_api.create_order(user, Constants.SHOP_ID, order)
        with allure.step("get shop order list"):
            response = api_clients.merchant_api.get_order_list(order_list, user).text
            assert response.get("orderList"), "Value for key 'orderList' is empty"

    @allure.description("Viewing order details for the Merchant Account under the manager role")
    @pytest.mark.case("QA-T277 (1.0)")
    @pytest.mark.skip(reason="https://*************")
    def test_merchant_manager_order_details(self, merchant_manager_creds, api_clients, order_list):
        with allure.step("create user"):
            user = api_clients.auth_api.create_user(merchant_manager_creds)
        with allure.step("get shop order list"):
            resp_list = api_clients.merchant_api.get_order_list(order_list, user).text
            order_id = resp_list["orderList"][0]["orderId"]
        with allure.step("get order details"):
            api_clients.merchant_api.get_order_details(order_id)

    @allure.description("Viewing order details for the Merchant Account under the manager role")
    @pytest.mark.case("QA-T278 (1.0)")
    @pytest.mark.skip(reason="https://********")
    def test_merchant_manager_order_search(self, merchant_manager_creds, api_clients, order_list):
        with allure.step("create user"):
            user = api_clients.auth_api.create_user(merchant_manager_creds)
        with allure.step("get shop order list"):
            resp_list = api_clients.merchant_api.get_order_list(order_list, user).text
            order_number = resp_list["orderList"][0]["number"]
        with allure.step("get order details"):
            order_search_data = order_search_data_by_id(order_number)
            order_resp = api_clients.merchant_api.get_order_search(order_search_data, user).text
            CommonCheckers.assert_val(lambda: order_resp[0], "number", order_number)
