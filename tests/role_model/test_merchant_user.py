import allure
import pytest

from checkers.common_checkers import CommonCheckers


class TestMerchantUserPermission:

    @allure.description("Viewing company shop order list for the Merchant Account under the User role")
    @pytest.mark.case("QA- (1.0)")
    @pytest.mark.skip(reason="https://************")
    def test_merchant_user_order_list(self, merchant_user_creds, order_list, api_clients):
        with allure.step("create user"):
            user = api_clients.auth_api.create_user(merchant_user_creds)
        with allure.step("get shop order list"):
            api_clients.merchant_api.get_order_list(order_list, user)

    @allure.description("Viewing order details for the Merchant Account under the User role")
    @pytest.mark.case("QA-T277 (1.0)")
    @pytest.mark.skip(reason="https://*********")
    def test_merchant_user_order_details(self, merchant_user_creds, api_clients, order_list):
        with allure.step("create user"):
            user = api_clients.auth_api.create_user(merchant_user_creds)
        with allure.step("get shop order list"):
            resp_list = api_clients.merchant_api.get_order_list(order_list, user).text
            order_id = resp_list["orderList"][0]["orderId"]
        with allure.step("get order details"):
            api_clients.merchant_api.get_order_details(order_id)

    @allure.description("Viewing order details for the Merchant Account under the User role")
    @pytest.mark.case("QA-T278 (1.0)")
    @pytest.mark.skip(reason="https://**********")
    def test_merchant_user_order_search(self, merchant_user_creds, api_clients, order_list, order_search_data_by_id):
        with allure.step("create user"):
            user = api_clients.auth_api.create_user(merchant_user_creds)
        with allure.step("get shop order list"):
            resp_list = api_clients.merchant_api.get_order_list(order_list, user).text
            order_number = resp_list["orderList"][0]["number"]
        with allure.step("get order details"):
            order_search_data = order_search_data_by_id(order_number)
            order_resp = api_clients.merchant_api.get_order_search(order_search_data, user).text
            CommonCheckers.assert_val(lambda: order_resp[0], "number", order_number)
