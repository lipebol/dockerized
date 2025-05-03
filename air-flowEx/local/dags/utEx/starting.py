from ast import literal_eval
from dotenv import load_dotenv
from os import getenv
from sys import path


class StartingError(Exception):
    pass

class Starting:

    load_dotenv()
    path.append(getenv('UTEX'))
    def __init__(self, properties: object) -> None:
        self.__properties = properties

    def init(self):
        for requirement in literal_eval(getenv('REQUIREMENTS')):
            if requirement not in dir(self.__properties):
                print(getenv('NOT_DECLARED') % f'"self.{requirement}"')
                raise StartingError