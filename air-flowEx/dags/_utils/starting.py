from ast import literal_eval
from dotenv import load_dotenv
from os import getenv
import sys


class StartingError(Exception):
    pass

class Starting:

    load_dotenv()
    sys.path.append(getenv('_UTILS'))
    def __init__(self, dag: object) -> None:
        self.__dag = dag

    def init(self):
        for requirement in literal_eval(getenv('REQUIREMENTS')):
            if requirement not in dir(self.__dag):
                print(getenv('NOT_DECLARED') % f'"self.{requirement}"')
                raise StartingError