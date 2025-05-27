from ast import literal_eval
from bs4 import BeautifulSoup
from inspect import currentframe
from os import getenv
from requests import get


class HttpExError(Exception):
    pass

class HttpEx:
    
    @staticmethod
    def httpEx(func):
        def wrapper(*args, **kwargs):
            request = get(
                "".join(args), params=kwargs.get('params'),
                headers=literal_eval(getenv('HEADERS')), timeout=2
            )
            if request.status_code == 200:
                kwargs['response'] = request.text if func.__name__ in (
                    'scrape') else request.content ### <-- add names methods...
                return func(*args, **kwargs)
            return HttpExError('Error in request.')
        return wrapper

    @httpEx
    @staticmethod
    def scrape(url: str, **kwargs) -> str:
        try:
            return BeautifulSoup(kwargs.get('response'),'lxml').find_all(kwargs.get('tag'))
        except Exception as error:
            print(f"{error} in: @{currentframe().f_code.co_name}")
            raise HttpExError

    @httpEx
    @staticmethod
    def content(url: str, **kwargs) -> bytes:
        try:
            return kwargs.get('response')
        except Exception as error:
            print(f"{error} in: @{currentframe().f_code.co_name}")
            raise HttpExError
