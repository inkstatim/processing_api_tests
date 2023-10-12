import allure
import pytest

from utils.otp_code import gen_otp_data
from data.user import GetUserResponse, EXPECTED_GET_OTP_USER_RESPONSE


class TestOTP:

    @allure.description("Auth by OTP")
    @pytest.mark.case("QA (1.0)")
    def test_otp_auth(self, api_clients, user_otp_creds):
        with allure.step("Auth by log/pass"):
            user = api_clients.auth_api.create_user(user_otp_creds)
        with allure.step("Pass OTP"):
            otp_code = gen_otp_data(user_otp_creds["otp_secret"])
            api_clients.auth_api.authenticate_by_otp(user, otp_code)
        with allure.step("Get user info"):
            resp = api_clients.auth_api.get_user().text
            assert GetUserResponse.model_validate(
                EXPECTED_GET_OTP_USER_RESPONSE
            ) == GetUserResponse.model_validate(resp)
