import pytest


class TestAuthHealthCheck:

    @pytest.mark.health_check
    def test_get_access_token(self, user_creds, api_clients):
        access_token = api_clients.auth_api.authenticate(user_creds) \
            .cookies.get('Access-Token')
        assert type(access_token) is str, \
            f"actual type of 'access_token': '{type(access_token)}', but expected 'str'"

    @pytest.mark.health_check
    def test_get_refresh_token(self, user_creds, api_clients):
        refresh_token = api_clients.auth_api.authenticate(user_creds) \
            .cookies.get('Refresh-Token')
        assert type(refresh_token) is str, \
            f"actual type of 'refresh_token': '{type(refresh_token)}', but expected 'str'"

    @pytest.mark.health_check
    def test_get_public_key(self, user_creds, api_clients):
        access_token = api_clients.auth_api.authenticate(user_creds) \
            .cookies.get('Access-Token')
        x_api_key = api_clients.auth_api.get_public_key(access_token)
        assert type(x_api_key) is str, \
            f"actual type of 'x_api_key': '{type(x_api_key)}', but expected 'str'"
        assert len(x_api_key) == 64, \
            f"actual length of 'x_api_key': '{x_api_key}' is '{len(x_api_key)}', but expected '64'"

    @pytest.mark.health_check
    def test_sign_order(self, user_creds, order, api_clients):
        user = api_clients.auth_api.create_user(user_creds)
        signature = api_clients.auth_api.get_sign_order(user, order)
        assert type(signature) is str, \
            f"actual type of 'signature': '{type(signature)}', but expected 'str'"
        assert len(signature) == 64, \
            f"actual length of 'signature': '{signature}' is '{len(signature)}', but expected '64'"
