import allure
from http.cookies import SimpleCookie

from custom_requests.requester import Requester
from entities.response import JsonResponse, ResponseType, ResponseAbstract
from entities.user import User, EmptyUser
from enums.request_methods import RequestMethods
from enums.status_codes import StatusCodes


class AuthApiEndpoints:
    sign_in = "/api/auth/sign-in"
    otp_sign_in = "/api/auth/2fa/totp/check"
    info = "/api/auth/info"


class SignatureApiEndpoints:
    signature_sign = "/api/signature/sign"
    signature_public = "/api/signature/public"


class AuthApi(Requester):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.headers = {'Cookie': 'RATE_LIMITS=false'}

    @classmethod
    def _make_absolute_url(cls, url):
        return cls.BASE_URL + url

    def authenticate(self, user_creds) -> ResponseAbstract:
        """
        Авторизация пользователя по email и паролю.

        user_creds:
            email (str): Email пользователя.
            password (str): Пароль пользователя.

        Returns:
            response: Объект Response с ответом сервера на запрос.
        """
        return self.request_api(url=AuthApiEndpoints.sign_in,
                                method=RequestMethods.POST,
                                json=user_creds,
                                headers=self.headers)

    def authenticate_by_otp(self, user, otp) -> ResponseAbstract:
        response = self.request_api(
            url=AuthApiEndpoints.otp_sign_in,
            method=RequestMethods.POST,
            return_code=StatusCodes.NO_CONTENT,
            json=otp,
            headers=self.headers
        )
        set_cookies = self.parse_set_cookies(response.headers.get("Set-Cookie"))
        self._update_headers(**set_cookies)
        user_data = {
            "access_token": set_cookies["Access-Token"],
            "refresh_token": set_cookies["Refresh-Token"]
        }
        user.update_user_data(**user_data)
        return user

    def get_public_key(self, access_token: str) -> str:
        """
        Получает публичный ключ пользователя.

        Args:
            access_token (str): Access token пользователя.

        Returns:
            response: Объект Response с ответом сервера на запрос.
        """
        self._update_headers(**{'Cookie': f'Access-Token={access_token}; RATE_LIMITS=false'})
        return self.request_api(url=SignatureApiEndpoints.signature_public,
                                method=RequestMethods.GET,
                                json={},
                                headers=self.headers) \
            .text.get('publicKey')

    def get_user(self, **kwargs) -> JsonResponse:
        if kwargs.get('headers'):
            self._update_headers(**kwargs.get('headers'))
        return self.request_api(url=AuthApiEndpoints.info,
                                method=RequestMethods.GET,
                                json={},
                                headers=self.headers)

    def create_user(self, user_creds) -> User:
        access_token = self.authenticate(user_creds).cookies.get('Access-Token')
        public_key = self.get_public_key(access_token)
        user_data = {'access_token': access_token,
                     'public_key': public_key}
        user = EmptyUser()
        user.update_user_data(**user_data)
        return user

    def get_sign_order(self, user: User, order_json) -> str:
        """
        Отправка запроса на подписание заказа.

        Args:
            user (User): Пользователь.
            order_json (dict): json с информацией о заказе. Находится в фикстуре order_json

        Returns:
            response: str Response с ответом сервера на запрос.
        """
        with allure.step(f"sign order for user with email: {user.email}"):
            self._update_headers(**{'X-API-KEY': user.public_key})
            return self.request_api(url=SignatureApiEndpoints.signature_sign,
                                    method=RequestMethods.POST,
                                    response_format=ResponseType.TEXT,
                                    json=order_json,
                                    headers=self.headers) \
                .text.strip('"')

    def set_sign_order_to_user(self, user: User, order_json):
        user.update_user_data(**{'signature': self.get_sign_order(user, order_json)})

    @staticmethod
    def parse_set_cookies(set_cookies: str) -> dict:
        cookies = SimpleCookie()
        cookies.load(set_cookies)
        return {k: v.value for k, v in cookies.items()}
