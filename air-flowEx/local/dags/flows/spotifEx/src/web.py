from os.path import abspath, dirname, join
from sys import path

path.insert(0, abspath(join(dirname(__file__), '..', '..', '..')))

from ast import literal_eval
from os import getenv
from utEx.httpEx import HttpEx
from system import System


class Web:

    def __init__(self, metadata: dict) -> None:
        self.__metadata = metadata
    
    @System.exceptions
    def info(self) -> dict or bool:
        if self.__metadata:
            if self.__metadata['title'] != getenv('AD'):
                self._artist = "".join(self.__metadata['artist'])
                if getenv('SINGLE_QUOTE') in self._artist: ### Example: Joseph O'Brien
                    self.idx = self._artist.find(getenv('SINGLE_QUOTE'))
                    ### 'r' (raw string) for 'escape' (Joseph O\'Brien)
                    self._artist = "".join(
                        fr"{self._artist[:self.idx]}\{self._artist[self.idx:]}"
                    )
                self.__soup = HttpEx.scrape(
                    getenv('EVERY_NOISE') + 'lookup.cgi', tag='a',
                    params=literal_eval(getenv('PARAMS') % self._artist)
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

    @System.exceptions
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

    @System.exceptions
    def image(self) -> bytes or bool:
        return HttpEx.content(self.__metadata['artUrl'])


    