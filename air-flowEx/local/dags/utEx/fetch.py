from ast import literal_eval
from bs4 import BeautifulSoup
from inspect import currentframe
from os import getenv
from requests import get

class FetchError(Exception):
    pass


class Fetch:

    def __init__(self) -> None:
        self.headers = literal_eval(getenv('HEADERS'))


    def scrape(self, url: str, tag: str, params=None) -> str:
        try:
            return BeautifulSoup(
                self._res_text(
                    get(
                        url, headers = self.headers, 
                        params = params
                    )
                ), 'lxml'
            ).find_all(tag)
        except Exception as error:
            print(f"{error} in: @{currentframe().f_code.co_name}")
            raise FetchError


    def content(self, url: str) -> bytes:
        try:
            return self._res_content(get(url, headers=self.headers))
        except Exception as error:
            print(f"{error} in: @{currentframe().f_code.co_name}")
            raise FetchError


    def _res_content(self, request: object) -> bytes or bool:
        try:
            return request.content if self._status(request) else False
        except Exception as error:
            print(f"{error} in: @{currentframe().f_code.co_name}")
            raise FetchError

    def _res_text(self, request: object) -> str or bool:
        try:
            return request.text if self._status(request) else False
        except Exception as error:
            print(f"{error} in: @{currentframe().f_code.co_name}")
            raise FetchError

    def _status(self, request: object) -> bool:
        try:
            return True if request.status_code == 200 else False
        except Exception as error:
            print(f"{error} in: @{currentframe().f_code.co_name}")
            raise FetchError