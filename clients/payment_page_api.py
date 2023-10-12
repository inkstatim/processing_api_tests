from custom_requests.requester import Requester
from entities.response import JsonResponse, ResponseType
from enums.request_methods import RequestMethods


class PaymentPage:
    session = "/api/session"


class PaymentPageApi(Requester):
    def __init__(self, session):
        super().__init__()
        self.session = session

    @classmethod
    def _make_absolute_url(cls, url):
        return cls.BASE_URL + url

    def create_payment_page(self, session_id: int) -> JsonResponse:
        return self.request_api(url=f"{PaymentPage.session}/{session_id}",
                                method=RequestMethods.PUT,
                                response_format=ResponseType.JSON)

    def get_payment_page(self, session_id: int, page_id: int) -> JsonResponse:
        return self.request_api(url=f"{PaymentPage.session}/{session_id}/page/{page_id}",
                                method=RequestMethods.GET,
                                response_format=ResponseType.JSON)
