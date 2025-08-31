from .flowconf import flowconf
from common.db import db
from common.initialize import load
from common.file import file
import pyarrow as arrow


class processing:

    flowconf.cols = db.columns(flowconf.schema, flowconf.table[1])

    @staticmethod
    def __data(csv_file: str):
        return file.load_csv(
            csv_file, flowconf.cols, dict(
                (col,arrow.string()) if col not in ('started_at','ended_at') 
                else (col,arrow.timestamp('ms')) for col in flowconf.cols
            ), sep=','
        )

    @staticmethod
    def unpack():
        for zip_file in load().zip_files:
            load.unzip(load.path(zip_file), suffix='.csv')
        if len(load().csv_files) < len(load().zip_files):
            raise Exception('')
        return load.variable('MESSAGE_SUCCESS')

    @staticmethod
    def load():
        for csv_file in load().csv_files:
            db.adbc(processing.data(csv_file), flowconf.schema, flowconf.table[1])
        return load.variable('MESSAGE_SUCCESS')