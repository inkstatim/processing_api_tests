import requests


class ResponseType:
    JSON = "json"
    TEXT = "text"


class ResponseAbstract:
    status_code = ""
    text = ""
    headers = ""
    cookies = ""

    def __init__(self, response: requests.Response):
        self.content = response.content


class TextResponse(ResponseAbstract):
    def __init__(self, response: requests.Response):
        super().__init__(response)
        self.status_code = response.status_code
        self.text = response.text
        self.headers = response.headers
        self.cookies = response.cookies


class JsonResponse(ResponseAbstract):
    def __init__(self, response: requests.Response):
        super().__init__(response)
        self.status_code = response.status_code
        self.text = response.json() if response.text != '' else {}
        self.headers = response.headers
        self.cookies = response.cookies
