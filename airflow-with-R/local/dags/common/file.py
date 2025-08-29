from common.initialize import load
from pyarrow import csv as arrow

class file:

    def __init__(self, files=None) -> None:
        self.__files = files

    def find(self, filename=None) -> str:
        if self.__files:
            self.__file = "".join(self.__files) if type(
                    self.__files) == list and len(self.__files) == 1 else None 
            if not self.__file:
                if filename:
                    return self.find_by_name(filename)
                raise Exception(f"""'{load.variable('MESSAGE_FILE_NOT_FOUND')}' in: @find""")
            return self.__file
        raise Exception(load.variable('MESSAGE_NOT_DECLARED') % 'files')
    
    def find_by_name(self, filename: str) -> str:
        return "".join([item for item in self.__files if filename in item])

    def load_csv(self, fields: list, types: dict, filename=None, sep=None) -> object:
        return arrow.read_csv(
            self.find(filename),
            parse_options=arrow.ParseOptions(delimiter=sep if sep else ';'),
            read_options=arrow.ReadOptions(
                encoding=load.variable('ENCODE_LATIN'), 
                column_names=fields, skip_rows=1
            ), convert_options=arrow.ConvertOptions(column_types=types)
        )