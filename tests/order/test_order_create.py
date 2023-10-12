import allure
import pytest
from jsonschema import validate

from checkers.common_checkers import CommonCheckers
from enums.constants import Constants
from json_resp_schemes.order import OrderSchema
from data.order import OrderCreateResponse, EXPECTED_ORDER_RESPONSE


class TestOrderCreate:

    @allure.description("Order create")
    @pytest.mark.case("QA (1.0)")
    def test_order_create(self, user_creds, order, api_clients):
        with allure.step("create user"):
            user = api_clients.auth_api.create_user(user_creds)
        with allure.step("get signature for order"):
            api_clients.auth_api.set_sign_order_to_user(user, order)
        with allure.step("create order"):
            order_resp = api_clients.order_api.create_order(user, Constants.SHOP_ID, order).text
            validate(order_resp, OrderSchema.POST)
        with allure.step("order status should be 'registered' & sessions status should be 'created'"):
            assert OrderCreateResponse.model_validate(
                EXPECTED_ORDER_RESPONSE
            ) == OrderCreateResponse.model_validate(order_resp)

    @allure.description("Create order without time limit")
    @pytest.mark.case("QA-T199 (1.0)")
    def test_order_without_time_limit_create(self, user_creds, order_without_time_limit, api_clients):
        with allure.step("create user"):
            user = api_clients.auth_api.create_user(user_creds)
        with allure.step("get signature for order"):
            api_clients.auth_api.set_sign_order_to_user(user, order_without_time_limit)
        with allure.step("create order without timelimit"):
            order_without_time_limit_resp = \
                api_clients.order_api.create_order(user, Constants.SHOP_ID, order_without_time_limit).text
        with allure.step("order status should be 'registered' & sessions status should be 'created'"):
            order_without_timelimit_status = order_without_time_limit_resp.get("status", {})
            assert order_without_timelimit_status == "registered", \
                f"actual status of order {order_without_timelimit_status}, but expected 'registered'"
            CommonCheckers.assert_all(order_without_time_limit_resp, "sessions.status", "created")

    @allure.description("Create order with expired time limit")
    @pytest.mark.case("QA (1.0)")
    @pytest.mark.negative
    def test_order_create_past_time_limit(self, user_creds, order_with_past_time_limit, api_clients):
        with allure.step("create user"):
            user = api_clients.auth_api.create_user(user_creds)
        with allure.step("get signature for order"):
            api_clients.auth_api.set_sign_order_to_user(user, order_with_past_time_limit)
        with allure.step("attempt to create order with past timelimit"):
            response_errors = api_clients.order_api.create_order_error(user, Constants.SHOP_ID,
                                                                       order_with_past_time_limit)
        with allure.step("check msg for main error & property_path should be 'timeLimit'"):
            CommonCheckers.assert_all(response_errors, "property_path", "timeLimit")
            main_error = next(e for e in response_errors if e["code"] is None)
            assert main_error.get("message", {}) == 'Time limit cannot be in the past.'

    @allure.description("Create order without customer information")
    @pytest.mark.case("QA-T215 (1.0)")
    @pytest.mark.skip(reason="**********")
    @pytest.mark.negative
    def test_order_create_with_empty_customer_data(self, user_creds, order_with_empty_customer_data, api_clients):
        with allure.step("create user"):
            user = api_clients.auth_api.create_user(user_creds)
        with allure.step("get signature for order"):
            api_clients.auth_api.set_sign_order_to_user(user, order_with_empty_customer_data)
        with ((allure.step("create order"))):
            order_with_empty_customer_resp = \
                lambda: api_clients.order_api.create_order(user, Constants.SHOP_ID, order_with_empty_customer_data).text
        with allure.step("order status should be 'registered' & sessions status should be 'created'"):
            # CommonCheckers.assert_val(order_with_empty_customer_resp, "status", "registered")  # toDO without repeat
            CommonCheckers.assert_all(order_with_empty_customer_resp(), "sessions.status", "created")
