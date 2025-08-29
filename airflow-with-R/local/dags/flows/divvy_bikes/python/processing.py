from common.db import db
from common.initialize import load
from common.file import file


class processing:

    @staticmethod
    def __data(file: str):
        __schema, __table = 'divvy_bikes', 'tripdata'
        # return db.columns(__schema, __table)
        # return 

    @staticmethod
    def unpack():
        for zip_file in load().zip_files:
            load.unzip(load.path(zip_file), suffix='.csv')
        if len(load().csv_files) < len(load().zip_files):
            raise Exception('')
        return load.variable('MESSAGE_SUCCESS')
