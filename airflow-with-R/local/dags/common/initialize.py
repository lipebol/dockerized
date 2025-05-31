from ast import literal_eval
from dotenv import load_dotenv
from os import getenv
from sys import path


class Starting:

    load_dotenv()
    path.append(getenv('COMMON'))
    def __init__(self, properties: object) -> None:
        self.__properties = properties

    def init(self):
        for requirement in literal_eval(getenv('REQUIREMENTS')):
            if requirement not in dir(self.__properties):
                raise Exception(getenv('NOT_DECLARED') % f'"self.{requirement}"')
            
class add:

    @staticmethod
    def exception(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as error:
                raise Exception(f"{error} (👉 @{str(func).split(' ')[1]} 👈)")
        return wrapper