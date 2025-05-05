from json import dump, load
from os import getenv, path, remove
from PIL import Image
from shutil import copyfile
from system import System


class File:

    def __init__(self) -> None:
        self.dir = path.dirname(__file__)
    
    @System.exceptions
    def read(self, file: str) -> object:
        if ".json" in getenv(file):
            return load(open(self.dir + getenv(file)))
        return open(self.dir + getenv(file)).read().strip()
    
    @System.exceptions
    def write(self, file: str, content: str or dict or bytes) -> str:
        self.type_write = 'wb' if type(content) == bytes else 'w'
        if ".json" in getenv(file):
            dump(content, open(self.dir + getenv(file), 'r+'), indent=5)
        else:
            open(self.dir + getenv(file), self.type_write).write(content)
        return getenv(file)

    @System.exceptions
    def exists(self, file: str) -> bool:
        if not path.isfile(self.dir + getenv(file)):
            self.write(file, 'VOID')
        return True

    @System.exceptions
    def new(self, source: str, destination: str) -> str:
        if ".jpeg" in source:
            Image.open(self.dir + source).save(
                self.dir + getenv(destination)
            )
            remove(self.dir + getenv('ORIGINAL_IMAGE'))
            return getenv(destination)
        return copyfile(
            self.dir + source, self.dir + getenv(destination)
        )