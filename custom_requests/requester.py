import logging
import os

from entities.response import ResponseAbstract, ResponseType, JsonResponse, TextResponse
from enums.hosts import Hosts
from enums.request_methods import RequestMethods
from enums.status_codes import StatusCodes
from utils.waiter import Waiter


class APIException(Exception):
    pass


class Requester:
    BASE_URL = Hosts.BASE_URL
    base_headers = dict({"Content-Type": "application/json", "Accept": "application/json"})

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        if self.BASE_URL.startswith('http://'):
            raise Exception("Invalid protocol, use https")

    @classmethod
    def _make_absolute_url(cls, url):
        raise NotImplementedError

    def _update_headers(self, **kwargs):
        self.headers = self.base_headers.copy()
        for key, value in kwargs.items():
            self.headers[key] = value

    def request_api(self, url: str, method=RequestMethods.GET, return_code=StatusCodes.SC_OK,
                    response_format=ResponseType.JSON, is_need_retry=True, is_need_logging=True, **kwargs) \
            -> ResponseAbstract:
        url = self._make_absolute_url(url)

        if is_need_retry:
            response = Waiter.request_with_retry(self.session, url, method, **kwargs)
        else:
            response = self.session.request(method, url, **kwargs)

        is_codes_equals = response.status_code == return_code
        if is_need_logging:
            self.__logging(response, is_codes_equals)
        if not is_codes_equals:
            raise AssertionError(f"actual status_code: {response.status_code}, but expected: {return_code}")

        if response_format == ResponseType.JSON:
            return JsonResponse(response)
        elif response_format == ResponseType.TEXT:
            return TextResponse(response)
        else:
            raise Exception("response_format should be in ResponseType")

    def __logging(self, response, is_codes_equals):
        try:
            request = response.request
            GREEN = '\033[32m'
            RED = '\033[31m'
            RESET = '\033[0m'
            headers = " \\\n".join([f"-H '{header}: {value}'" for header, value in request.headers.items()])
            # toDO fix output full_test_name for parametrization tests (now output with [params]):
            full_test_name = f"pytest {os.environ.get('PYTEST_CURRENT_TEST', '').replace(' (call)', '')}"

            body = ""
            if hasattr(request, 'body') and request.body is not None:
                if isinstance(request.body, bytes):
                    body = request.body.decode('utf-8')
                body = f"-d '{body}' \n" if body != '{}' else ''

            self.logger.info(
                f"{GREEN}{full_test_name}{RESET}\n"
                f"curl -X {request.method} '{request.url}' \\\n"
                f"{headers} \\\n"
                f"{body}"
            )
            if not is_codes_equals:
                self.logger.info(f"\tRESPONSE:"
                                 f"\nSTATUS_CODE: {RED}{response.status_code}{RESET}"
                                 f"\nDATA: {RED}{response.text}{RESET}")
        except Exception as e:
            print(f"\nLogging went wrong: {type(e)} - {e}")
