import allure
import pytest

from enums.constants import Constants
from checkers.common_checkers import CommonCheckers
from conftest import order_search_data_by_id


class TestMerchantAdminPermission:

    @allure.description("Creating order for merchant account under admin role")
    @pytest.mark.case("QA-T274 (1.0)")
    def test_merchant_admin_order_create(self, merchant_admin_creds, order, api_clients):
        with allure.step("create user"):
            user = api_clients.auth_api.create_user(merchant_admin_creds)
        with allure.step("get signature for order"):
            api_clients.auth_api.set_sign_order_to_user(user, order)
        with allure.step("create order"):
            order_resp = api_clients.order_api.create_order(user, Constants.SHOP_ID, order).text
        with allure.step("order status should be 'registered' & sessions status should be 'created'"):
            assert order_resp.get('status') == 'registered', \
                f"expected status 'registered', but actual {order_resp.get('status')}"
            assert order_resp.get('sessions')[0].get('status') == 'created', \
                f"expected session status 'created', but actual {order_resp.get('sessions')[0].get('status')}"

    @allure.description("Viewing company shop order list for Merchant Account under admin role")
    @pytest.mark.case("QA-T275 (1.0)")
    def test_merchant_admin_order_list(self, merchant_admin_creds, order_list, api_clients, order):
        with allure.step("create user"):
            user = api_clients.auth_api.create_user(merchant_admin_creds)
        with allure.step("get signature for order"):
            api_clients.auth_api.set_sign_order_to_user(user, order)
        with allure.step("create order"):
            api_clients.order_api.create_order(user, Constants.SHOP_ID, order)
        with allure.step("get shop order list"):
            response = api_clients.merchant_api.get_order_list(order_list, user).text
            assert response.get("orderList"), "Value for key 'orderList' is empty"

    @allure.description("Viewing order details for the Merchant Account under the Admin role")
    @pytest.mark.case("QA-T277 (1.0)")
    @pytest.mark.skip(reason="https://*********")
    def test_merchant_admin_order_details(self, merchant_admin_creds, api_clients, order_list):
        with allure.step("create user"):
            user = api_clients.auth_api.create_user(merchant_admin_creds)
        with allure.step("get shop order list"):
            resp_list = api_clients.merchant_api.get_order_list(order_list, user).text
            order_id = resp_list["orderList"][0]["orderId"]
        with allure.step("get order details"):
            api_clients.merchant_api.get_order_details(order_id)

    @allure.description("Viewing order details for the Merchant Account under the admin role")
    @pytest.mark.case("QA- (1.0)")
    def test_merchant_admin_order_search(self, merchant_admin_creds, api_clients, order_list):
        with allure.step("create user"):
            user = api_clients.auth_api.create_user(merchant_admin_creds)
        with allure.step("get shop order list"):
            resp_list = api_clients.merchant_api.get_order_list(order_list, user).text
            order_number = resp_list["orderList"][0]["number"]
        with allure.step("get order details"):
            order_search_data = order_search_data_by_id(order_number)
            order_resp = api_clients.merchant_api.get_order_search(order_search_data, user).text
            CommonCheckers.assert_val(lambda: order_resp[0], "number", order_number)
