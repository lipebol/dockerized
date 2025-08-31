from common.initialize import load
from pyarrow import csv as arrow

class file:

    @staticmethod
    def load_csv(csv_file: str, fields: list, types: dict, sep=None) -> object:
        return arrow.read_csv(
            csv_file,
            parse_options=arrow.ParseOptions(delimiter=sep if sep else ';'),
            read_options=arrow.ReadOptions(
                encoding='latin1', column_names=fields, skip_rows=1
            ), convert_options=arrow.ConvertOptions(column_types=types)
        )