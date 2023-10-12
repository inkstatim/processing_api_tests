import allure
from custom_requests.requester import Requester
from enums.request_methods import RequestMethods
from entities.user import User
from entities.response import JsonResponse


class MerchantApiEndpoints:
    merchant_company = "/api/merchant/company"


class MerchantApi(Requester):
    def __init__(self, session):
        super().__init__()
        self.session = session

    @classmethod
    def _make_absolute_url(cls, url):
        return cls.BASE_URL + url

    def get_shops_details(self, user: User):
        with allure.step(f"getting shops information for the user {user.email}"):
            self._update_headers(**{'X-SIGNATURE': user.signature,
                                    'X-API-KEY': user.public_key,
                                    'Cookie': user.cookies})
            shops = self.request_api(url=f"{MerchantApiEndpoints.merchant_company}/shops/details",
                                     method=RequestMethods.GET,
                                     headers=self.headers)\
                .text.get('shops', {})
            if shops == {}:
                raise AssertionError("shops shouldn't be empty!")
        return shops

    def get_order_list(self, order_list_json, user: User) -> JsonResponse:
        self._update_headers(**{'Cookie': user.cookies})
        response = self.request_api(url=f"{MerchantApiEndpoints.merchant_company}/shops/order/list",
                                    method=RequestMethods.POST,
                                    json=order_list_json,
                                    headers=self.headers)
        order_list = response.text.get('orderList', {})
        if order_list == {}:
            raise AssertionError("orderList shouldn't be empty!")
        return response

    def get_order_details(self, order_id, user: User) -> JsonResponse:
        self._update_headers(**{'Cookie': user.cookies})
        return self.request_api(url=f"{MerchantApiEndpoints.merchant_company}/order/{order_id}/details",
                                method=RequestMethods.GET,
                                headers=self.headers)

    def get_order_search(self, order_number, user: User) -> JsonResponse:
        self._update_headers(**{'Cookie': user.cookies})
        return self.request_api(url=f"{MerchantApiEndpoints.merchant_company}/shops/order/search",
                                method=RequestMethods.POST,
                                json=order_number,
                                headers=self.headers)
