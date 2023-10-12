from custom_requests.requester import Requester
from entities.response import ResponseType, JsonResponse, ResponseAbstract
from entities.user import User
from enums.request_methods import RequestMethods
from enums.constants import Constants
from enums.status_codes import StatusCodes


class OrderApiEndpoints:
    shop = "/api/shop"


class OrderApi(Requester):
    def __init__(self, session):
        super().__init__()
        self.session = session

    @classmethod
    def _make_absolute_url(cls, url):
        return cls.BASE_URL + url

    def create_order(self, user: User, shop_id: Constants, order_json, expected_status_code=StatusCodes.SC_OK) -> \
            ResponseAbstract:
        """
        Отправка запроса на создание заказа.

        Args:
            user (User): Содержит подпись заказа.
            shop_id (int): ID магазина определяется в модулe constants.py. Является query параметром.
            order_json (dict): json с информацией о заказе. Находится в фикстуре order
            expected_status_code (tuple, optional): Ожидаемые статус-коды ответа от сервера.
                                             Например, StatusCodes.SC_OK.
                                             Используется для валидации ответа от сервера.
                                             По умолчанию ожидается 200 OK.

        Returns:
            response: Объект Response с ответом сервера на запрос.
        """
        if user.signature is None:
            raise KeyError("user.signature is None")
        self._update_headers(**{'X-SIGNATURE': user.signature,
                                'X-API-KEY': user.public_key})
        return self.request_api(url=f"{OrderApiEndpoints.shop}/{shop_id}/order",
                                method=RequestMethods.POST,
                                return_code=expected_status_code,
                                json=order_json,
                                headers=self.headers)

    def create_order_error(self, user: User, shop_id: Constants, order_json, expected_status_code=StatusCodes.BAD_REQ) \
            -> ResponseAbstract:
        self._update_headers(**{'X-SIGNATURE': user.signature,
                                'X-API-KEY': user.public_key})
        errors = self.request_api(url=f"{OrderApiEndpoints.shop}/{shop_id}/order",
                                  method=RequestMethods.POST,
                                  return_code=expected_status_code,
                                  json=order_json,
                                  headers=self.headers)\
            .text.get('errors', {})
        if errors == {}:
            raise AssertionError("should be 1 and more errors!")
        return errors

    def get_order_status(self, shop_id, order_id) -> JsonResponse:
        return self.request_api(url=f"{OrderApiEndpoints.shop}/{shop_id}/order/{order_id}",
                                method=RequestMethods.GET,
                                response_format=ResponseType.JSON,
                                headers=self.headers)
