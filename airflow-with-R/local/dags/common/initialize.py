# from airflow.sdk import Variable # -- version 3 --
from airflow.models import Variable
from ast import literal_eval
from cryptography.fernet import Fernet
from datetime import datetime
from importlib.util import module_from_spec, spec_from_file_location
from inspect import currentframe, getmodule
from json import dump, load
from glob import glob
from os import listdir, path, remove
from pytz import timezone
import sys


class load:

    default = None

    sys.path.append(path.dirname(__file__))
    def __init__(self) -> None:
        self.__flows = load.variable('FLOWS')
        self.__flow_inference = getmodule(currentframe().f_back)
        self.__flow = self.default
    
    @property
    def __flowname_inference(self):
        if path.dirname(self.__flow_inference.__file__) == path.dirname(self.__flows):
            return path.basename(self.__flow_inference.__file__).split('.py')[0]
        if self.__flows in self.__flow_inference.__file__:
            return self.__flow_inference.__file__.split('/')[-3]
        
    @property
    def flow(self):
        if not self.__flow:
            self.set_flow_by_name = self.__flowname_inference
        return self.__flow
    
    @flow.setter
    def set_flow_by_name(self, name: str):
        if not name or str(name).lower() not in listdir(self.__flows):
            raise ValueError(
                load.variable('MESSAGE_FLOW_NOT_FOUND')
            )
        for dir in ['datasets', 'python', 'r']:
            if dir not in listdir(f'{self.__flows}/{str(name).lower()}'):
                raise Exception(
                    load.variable('MESSAGE_FLOW_STRUCTURE_INCORRECT') % dir
                )
        self.__flow = f'{self.__flows}/{str(name).lower()}'

    @property
    def __flow_not_declared(self):
        return load.variable('MESSAGE_NOT_DECLARED') % 'load.set_flow_by_name'

    @property
    def __flowconf(self):
        if not self.flow:
            raise Exception(self.__flow_not_declared)
        if 'flowconf.py' not in listdir(self.flow + '/python'):
            raise Exception(
                load.variable('MESSAGE_FLOWCONF_NOT_FOUND')
            )
        self.__module_spec = spec_from_file_location(
            'flowconf.py', self.flow + '/python/flowconf.py'
        )
        self.__module = module_from_spec(self.__module_spec)
        self.__module_spec.loader.exec_module(self.__module)
        return dir(getattr(self.__module,'flowconf'))
    
    def state(self):
        if 'pull' not in self.__flowconf:
            raise Exception(
                load.variable('MESSAGE_NOT_DECLARED') % 
                f'"self.pull" was supposed to be in "{self.flow + "/python/flowconf.py"}"'
            )

    def __files(self, type: str):
        if not self.flow:
            raise Exception(self.__flow_not_declared)
        return glob(load.variable(type) % self.flow)
    
    @property
    def csv_files(self):
        return self.__files('CSV_FILES')
    
    @property
    def parquet_files(self):
        return self.__files('PARQUET_FILES')
    
    @property
    def excel_files(self):
        return self.__files('EXCEL_FILES')
    
    def __cleanup(self, files: list):
        for file in files:
            remove(file)
        return load.variable('MESSAGE_SUCCESS')

    def cleanup_datasets(self) -> str:
        return self.__cleanup(self.csv_files + self.parquet_files + self.excel_files)
    
    def cleanup_others(self, files: str) -> str:
        return self.__cleanup(files)

    @staticmethod
    def crypto(fernet_key: str) -> object:
        return Fernet(load.variable(fernet_key, encode=True))

    @staticmethod
    def variable(var: str|bytes, encode=False, decode=False, eval=False) -> str:
        if decode:
            return var.decode()
        else:
            var = Variable.get(var)
        return var.encode() if encode else literal_eval(var) if eval else var
    
    @staticmethod
    def context(context: dict) -> dict:
        return dict(
            zip(
                ['summary','task','info','time','message'],
                list(
                    str(context.get(key)).replace('<','').replace('>','')
                    for key in context.keys() if key in load.variable(
                        'CONTEXT_AIRFLOW_KEYS', eval=True
                    )
                )
            )
        )
    
    @staticmethod
    def jsonfile(path: str, data=None):
        with open(path, 'w' if data else 'r') as jsonfile:
            if not data:
                return load(jsonfile)
            dump(data, jsonfile, indent=5)

    @staticmethod
    def timezone_default() -> str:
        return load.variable('TIMEZONE_DEFAULT')

    @staticmethod
    def now():
        return datetime.now(tz=timezone(load.timezone_default())).isoformat()
    
    @staticmethod
    def iso_8601(str_datetime: str):
        return datetime.fromisoformat(str_datetime).astimezone(timezone(load.timezone_default()))
    
        
class add:

    @staticmethod
    def exception(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as error:
                raise Exception(f"{error} (👉 @{str(func).split(' ')[1]} 👈)")
        return wrapper