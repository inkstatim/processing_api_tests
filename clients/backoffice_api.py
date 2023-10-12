from custom_requests.requester import Requester
from entities.user import User
from enums.request_methods import RequestMethods
from enums.status_codes import StatusCodes


class BackofficeApiEndpoints:
    company = "/api/backoffice/company"
    shop = "/api/backoffice/shop"


class BackofficeApi(Requester):
    def __init__(self, session):
        super().__init__()
        self.session = session

    @classmethod
    def _make_absolute_url(cls, url):
        return cls.BASE_URL + url

    # toDO check: user should have role service_admin
    def create_and_get_id_backoffice_company(self, user: User, company_json, expected_status_code=StatusCodes.SC_OK) \
            -> int:
        self._update_headers(**{'X-SIGNATURE': user.signature,
                                'X-API-KEY': user.public_key,
                                'Cookie': user.cookies})
        backoffice_company_resp = self.request_api(url=BackofficeApiEndpoints.company,
                                                   method=RequestMethods.POST,
                                                   return_code=expected_status_code,
                                                   json=company_json,
                                                   headers=self.headers)
        # toDO в остальных местах также сделать
        try:
            company_id = backoffice_company_resp.text['id']
        except KeyError as e:
            raise KeyError(f"An error occurred for field 'company id': {e}")
        return company_id

    def create_and_get_id_shop(self, user: User, shop_json, expected_status_code=StatusCodes.SC_OK):
        self._update_headers(**{'X-SIGNATURE': user.signature,
                                'X-API-KEY': user.public_key,
                                'Cookie': user.cookies})
        shop_resp = self.request_api(url=BackofficeApiEndpoints.shop,
                                     method=RequestMethods.POST,
                                     return_code=expected_status_code,
                                     json=shop_json,
                                     headers=self.headers)
        try:
            company_id = shop_resp.text['id']
        except KeyError as e:
            raise KeyError(f"An error occurred for field 'shop id': {e}")
        return company_id
