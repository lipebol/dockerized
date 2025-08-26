from common.initialize import add, load
# from bs4 import BeautifulSoup
from requests import get


class httpEx:
    
    @add.exception
    @staticmethod
    def __getdata(func):
        def wrapper(*args, **kwargs):
            request = get(
                kwargs.get('url') if kwargs.get('url') else "".join(args), 
                params=kwargs.get('params'),
                headers=load.variable('HEADERS', eval=True), timeout=2
            )
            if request.status_code == 200:
                kwargs['response'] = request.text if kwargs.get('text') else request.content
                return func(*args, **kwargs)
            return Exception('Error in request.')
        return wrapper

    # @add.exception
    # @__getdata
    # @staticmethod
    # def scrape(**kwargs, text=True) -> str:
    #     return BeautifulSoup(kwargs.get('response'),'lxml').find_all(kwargs.get('tag'))
        

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