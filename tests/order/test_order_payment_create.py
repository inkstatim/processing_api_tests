from checkers.common_checkers import CommonCheckers
from jsonschema.validators import validate

from data.cards import Cards
import allure
import pytest

from enums.constants import Constants
from json_resp_schemes.payment_page import PaymentPageSchema
from utils.date_hepler import DateHelper


class TestOrderPaymentCreate:

    @allure.description("Pay order with a credit card")
    @pytest.mark.case("QA-T192 (1.0)")
    @pytest.mark.skip(reason='https://*******')
    def test_make_payment(self, user_creds, order, card, api_clients):
        with allure.step("create user"):
            user = api_clients.auth_api.create_user(user_creds)
        with allure.step("set sign order to user"):
            api_clients.auth_api.set_sign_order_to_user(user, order)
        with allure.step("create order & extract session_id"):
            order_resp = api_clients.order_api.create_order(user, Constants.SHOP_ID, order).text
            session_id = order_resp["sessions"][0]["id"]
        with allure.step("create payment page and extract page_id"):
            payment_page_resp = api_clients.payment_page_api.create_payment_page(session_id).text
            page_id = payment_page_resp["paymentPage"]["id"]
        with allure.step("make payment via card"):
            api_clients.card_payment_api.make_payment(session_id, page_id, card)
        with allure.step("get payment page"):
            payment_page_resp = lambda: api_clients.payment_page_api.get_payment_page(session_id, page_id).text
            validate(payment_page_resp(), PaymentPageSchema.PUT_GET)
        with allure.step("check payment page statuses"):
            CommonCheckers.assert_val(payment_page_resp, "paymentPage.status", "result")
            # CommonCheckers.assert_val(payment_page_resp, "order.status", "completed")
            # CommonCheckers.assert_val(payment_page_resp, "operation.status", "completed")
            # CommonCheckers.assert_val(payment_page_resp, "paymentResponse.status", "completed")

    @allure.description("Pay order with decline_payable card")
    @pytest.mark.case("QA-T211 (1.0), QA-T212 (1.0)")
    @pytest.mark.negative
    @pytest.mark.parametrize('card', [Cards.CARD_DECLINE_41(DateHelper.get_year(1)),
                                      Cards.CARD_DECLINE_51(DateHelper.get_year(1))])
    def test_make_payment_with_decline_cards(self, user_creds, order, card, api_clients):
        with allure.step("create user"):
            user = api_clients.auth_api.create_user(user_creds)
        with allure.step("set sign order to user"):
            api_clients.auth_api.set_sign_order_to_user(user, order)
        with allure.step("create order, extract session_id"):
            order_resp = api_clients.order_api.create_order(user, Constants.SHOP_ID, order).text
            session_id = order_resp["sessions"][0]["id"]
        with allure.step("create payment page & extract page_id"):
            payment_page_resp = api_clients.payment_page_api.create_payment_page(session_id).text
            page_id = payment_page_resp["paymentPage"]["id"]
        with allure.step("make payment via decline card"):
            api_clients.card_payment_api.make_payment(session_id, page_id, card)
        with allure.step("check payment page status"):
            payment_page_resp = lambda: api_clients.payment_page_api.get_payment_page(session_id, page_id).text
        with allure.step("check payment page statuses"):
            # CommonCheckers.assert_val(payment_page_resp, "paymentPage.status", "result")
            CommonCheckers.assert_val(payment_page_resp, "order.status", "in_progress")
            # CommonCheckers.assert_val(payment_page_resp, "paymentResponse.status", "failed")

    @allure.description("Pay order with expired credit card")
    @pytest.mark.case("QA-T209 (1.0)")
    @pytest.mark.negative
    def test_make_payment_with_expired_data_card(self, user_creds, order, card_expire, api_clients):
        with allure.step("create user"):
            user = api_clients.auth_api.create_user(user_creds)
        with allure.step("set sign order to user"):
            api_clients.auth_api.set_sign_order_to_user(user, order)
        with allure.step("create order & extract session_id"):
            order_resp = api_clients.order_api.create_order(user, Constants.SHOP_ID, order).text
            session_id = order_resp["sessions"][0]["id"]
        with allure.step("create payment page & extract page_id"):
            payment_page_resp = api_clients.payment_page_api.create_payment_page(session_id).text
            page_id = payment_page_resp["paymentPage"]["id"]
        with allure.step("make payment via expired card"):
            payment_response_errors = api_clients.card_payment_api.make_payment_error(session_id, page_id, card_expire)
        with allure.step("check payment page errors"):
            assert len(payment_response_errors) == 2, \
                f"expected at least '2' errors in the response, but " \
                f"actual '{len(payment_response_errors)}'"
            assert payment_response_errors[0].get("message", {}) == "Expiration date cannot be in the past.", \
                f"expected 'Expiration date cannot be in the past.', but " \
                f"actual '{payment_response_errors[0].get('message', {})}'."
            assert payment_response_errors[0].get("property_path", {}) == "expiry", \
                f"expected 'expiry', but " \
                f"actual '{payment_response_errors[0].get('property_path', '')}'."
            current_year = DateHelper.get_year()
            assert payment_response_errors[1].get("message", {}) == \
                f"The expiration year must be greater than or equal to {current_year}.", \
                f"expected 'The expiration year must be greater than or equal to {current_year}.', but " \
                f"actual '{payment_response_errors[1].get('message', '')}'"
            assert payment_response_errors[1].get("property_path", {}) == "expiry.year", \
                f"expected 'expiry.year', but " \
                f"actual '{payment_response_errors[1].get('property_path', {})}'"

    @allure.description("Pay order with card without specifying CVV")
    @pytest.mark.case("QA-T210 (1.0)")
    @pytest.mark.negative
    def test_make_payment_without_cvv_card(self, user_creds, order, card_with_empty_cvv, api_clients):
        with allure.step("create user"):
            user = api_clients.auth_api.create_user(user_creds)
        with allure.step("set sign order to user"):
            api_clients.auth_api.set_sign_order_to_user(user, order)
        with allure.step("create order, extract session_id"):
            order_resp = api_clients.order_api.create_order(user, Constants.SHOP_ID, order).text
            session_id = order_resp["sessions"][0]["id"]
        with allure.step("create payment page and extract page_id"):
            payment_page_resp = api_clients.payment_page_api.create_payment_page(session_id).text
            page_id = payment_page_resp["paymentPage"]["id"]
        with allure.step("make payment via without cvv card"):
            payment_response_errors = api_clients.card_payment_api.make_payment_error(
                session_id, page_id, card_with_empty_cvv)
        with allure.step("check payment page errors"):
            assert len(payment_response_errors) == 3, \
                f"expected at least '3' errors in the response, but " \
                f"actual '{len(payment_response_errors)}'"
            assert payment_response_errors[0].get("message", {}) == "This value should not be blank.", \
                f"expected 'This value should not be blank.', but " \
                f"actual '{payment_response_errors[0].get('message', {})}'"
            assert all(error.get("property_path", {}) == 'cvc' for error in payment_response_errors), \
                "all property_path should be 'cvc'"
