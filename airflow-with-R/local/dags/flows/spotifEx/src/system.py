from ast import literal_eval
from dbus import SessionBus, Interface
from json import dumps
from os import getenv
from subprocess import run, PIPE


class System:
    
    @staticmethod
    def dbus() -> dict or bool:
        try:
            return dict(
                (key.split(':')[1], value) for key, value in literal_eval(
                    dumps(
                        Interface(
                            SessionBus().get_object(
                                getenv('NAME'), getenv('OBJECT_PATH')
                            ), 
                            getenv('METHOD')
                        ).Get(
                            getenv('INTERFACE'), getenv('PROPERTIE')
                        )
                    )
                ).items()
            )
        except Exception:
            return False

    @staticmethod
    def exceptions(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as error:
                run(
                    getenv('NOTIFY_SEND') % (
                        f'''"           👉 {getenv('TITLE')}@{str(func).split(' ')[1]} 👈
                        \n""{error}\n"'''
                    ), shell=True, stdout=PIPE, text=True
                )
                return False
        return wrapper
