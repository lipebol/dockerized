from os.path import abspath, dirname, join
from sys import path

path.insert(0, abspath(join(dirname(__file__), '..', '..', '..')))

from ast import literal_eval
from inspect import currentframe
from os import getenv
from utEx.fetch import Fetch


class Web:

    def __init__(self, System, metadata: dict) -> None:
        self._System, self.__metadata, self._Fetch = System, metadata, Fetch()
    
    def info(self) -> dict or bool:
        try:
            if self.__metadata:
                if self.__metadata['title'] != getenv('AD'):
                    self._artist = "".join(self.__metadata['artist'])
                    if getenv('SINGLE_QUOTE') in self._artist: ### Example: Joseph O'Brien
                        self.idx = self._artist.find(getenv('SINGLE_QUOTE'))
                        ### 'r' (raw string) for 'escape' (Joseph O\'Brien)
                        self._artist = "".join(
                            fr"{self._artist[:self.idx]}\{self._artist[self.idx:]}"
                        )
                    self.__soup = self._Fetch.scrape(
                        getenv('EVERY_NOISE') + 'lookup.cgi', 'a',
                        literal_eval(getenv('PARAMS') % self._artist)
                    )
                    return {
                        "listen": 1, 
                        "track": self._mergeInfo(
                            [
                                {
                                    (
                                        i.text if str(i.text) != "â\x93\x98" else ""
                                    ) : getenv('EVERY_NOISE') + self.__soup[idx]['href']
                                } for idx, i in enumerate(self.__soup)
                            ]
                        )
                    }
            return False
        except Exception as error:
            self._System.notify(f"{error} in: @{currentframe().f_code.co_name}")
            return False


    def _mergeInfo(self, info: list) -> dict:
        for dictio in info:
            if "".join(dictio.keys()) == "":
                self.__metadata['artist'] = {
                    "name": self._artist.replace(getenv('BACKSLASH'), getenv('VOID')),
                    "profile": "".join(dictio.values())
                }
        self.__metadata['genres'] = info[:-1]
        self.__metadata.pop('albumArtist')
        return self.__metadata


    def image(self) -> bytes or bool:
        try:
            return self._Fetch.content(self.__metadata['artUrl'])
        except Exception as error:
            self._System.notify(f"{error} in: @{currentframe().f_code.co_name}")
            return False


    