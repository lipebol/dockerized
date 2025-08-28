from common.initialize import add, load
from bs4 import BeautifulSoup
from requests import get
from time import sleep


class httpEx:
    
    @add.exception
    @staticmethod
    def __getdata(func):
        def wrapper(**kwargs):
            r = get(
                kwargs.get('url'), params=kwargs.get('params'),
                headers=load.variable('HEADERS', eval=True), timeout=2
            )
            sleep(5)
            if r.status_code == 200:
                if 'scrape' in func.__name__:
                    kwargs['text'] = True
                kwargs['response'] = r.text if kwargs.get('text') else r.content
                return func(**kwargs)
            return Exception('Error in request.')
        return wrapper

    @add.exception
    @__getdata
    @staticmethod
    def scrape(**kwargs) -> str:
        return BeautifulSoup(
            kwargs.get('response'), kwargs.get('type') ### <-- 'xml' or 'lxml'
        ).find_all(kwargs.get('tag'))
        
    @add.exception
    @__getdata
    @staticmethod
    def save(**kwargs):
        if not kwargs.get('filename'):
            kwargs['filename'] = kwargs.get('url').split('/')[-1]
        open(
            kwargs.get('flowpath') + '/datasets/' + kwargs.get('filename'), 'wb'
        ).write(kwargs.get('response'))
        return load.variable('MESSAGE_SUCCESS')