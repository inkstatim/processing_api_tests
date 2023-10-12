from custom_requests.requester import Requester
from entities.response import JsonResponse, ResponseType
from enums.request_methods import RequestMethods
from enums.status_codes import StatusCodes


class CardPaymentApiEndpoints:
    card = "/api/payment"
    refund = "/api/payment/refund"


class CardPaymentApi(Requester):
    def __init__(self, session):
        super().__init__()
        self.session = session

    @classmethod
    def _make_absolute_url(cls, url):
        return cls.BASE_URL + url

    def make_payment(self, session_id: int, page_id: int, card, expected_status_codes=StatusCodes.SC_OK) \
            -> JsonResponse:
        return self.request_api(url=f"{CardPaymentApiEndpoints.card}/card/session/{session_id}/page/{page_id}",
                                method=RequestMethods.POST,
                                return_code=expected_status_codes,
                                response_format=ResponseType.JSON,
                                json=card)

    def make_payment_error(self, session_id: int, page_id: int, card, expected_status_codes=StatusCodes.BAD_REQ) \
            -> JsonResponse:
        errors = self.request_api(url=f"{CardPaymentApiEndpoints.card}/card/session/{session_id}/page/{page_id}",
                                  method=RequestMethods.POST,
                                  return_code=expected_status_codes,
                                  response_format=ResponseType.JSON,
                                  json=card)\
            .text.get('errors', {})
        if errors == {}:
            raise AssertionError("should be 1 and more errors!")
        return errors

    def cancel_order(self, cancel_order_json) -> JsonResponse:
        return self.request_api(url=f"{CardPaymentApiEndpoints.card}/card/cancel",
                                method=RequestMethods.POST,
                                json=cancel_order_json)

    def refund_payment(self, order_id: int, refund_payment) -> JsonResponse:
        return self.request_api(url=f"{CardPaymentApiEndpoints.refund}/{order_id}",
                                method=RequestMethods.POST,
                                json=refund_payment,
                                return_code=StatusCodes.NO_CONTENT)
