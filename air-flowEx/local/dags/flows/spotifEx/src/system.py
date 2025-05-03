from ast import literal_eval
from dbus import SessionBus, Interface
from glob import glob
from inspect import currentframe
from json import dumps
from os import getenv, path
from subprocess import run, PIPE
from shutil import copyfile


class System:

    def __init__(self) -> None:
        self.dir = path.dirname(__file__)

    @staticmethod
    def dbus() -> dict or bool:
        try:
            #self.set_wallpaper({"LVDS": "CURRENT_IMAGE", "VGA": "SPOTIFY_IMAGE"})
            #self.set_glava('ON_BARS')
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
        except Exception as error:
            #self.set_wallpaper({"LVDS": "UBUNTU_IMAGE", "VGA": "CANONICAL_IMAGE"})
            #self.set_glava('OFF_BARS')
            return False


    def notify(self, message: str) -> str or bool:
        try:
            if "@" in message:
                self._icon = self.dir + getenv('ERROR_ICON')
            return self.__shell(
                getenv('NOTIFY_SEND') % (self._icon, f'"{getenv('TITLE')}\n""{message}"')
            )
        except Exception as error:
            self.__err = f"{error} in: @{currentframe().f_code.co_name}"
            self.__shell(
                getenv('NOTIFY_SEND') % (self._icon, f'"{getenv('TITLE')}\n""{self.__err}"')
            )
            return False

    def set_wallpaper(self, args: dict) -> None:
        try:
            for key, value in args.items():
                self.__shell(getenv('SET_WALLPAPER') % (getenv(key), self.dir + getenv(value)))
        except Exception as error:
            self.notify(f"{error} in: @{currentframe().f_code.co_name}")

    def set_glava(self, env_dir: str) -> None:
        try:
            for file in glob(self.dir + getenv(env_dir)):
                copyfile(file, getenv('SET_GLAVA') % file.split(getenv('SLASH'))[-1])
        except Exception as error:
            self.notify(f"{error} in: @{currentframe().f_code.co_name}")

    @staticmethod
    def __shell(command: str) -> str or bool:
        try:
            return run(command, shell=True, stdout=PIPE, text=True)
        except Exception as error:
            print(f"{error} in: @{currentframe().f_code.co_name}")
            return False