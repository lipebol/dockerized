from common.db import db
from common.initialize import load
from common.httpEx import httpEx
from xmltodict import parse
import pyarrow as arrow


class flowconf:

    __schema, __table = 'divvy_bikes', 'files'

    @property
    def __url(self) -> str:
        return load.variable('DIVVY_BIKES')
    
    @staticmethod
    def to_table(data: list) -> object:
        def parser(content: str|tuple) -> dict:
            if 'Contents' in str(content):
                content = [
                    str(value.strip('"')) 
                    for key, value in parse(content.encode()).get('Contents').items() 
                    if key in ('Key','LastModified','ETag','Size')
                ]
            return dict(zip(['filename','last_modified','id','size'], content))
        return arrow.Table.from_pylist(list(map(parser, data)))

    
    def pull(self):
        self.__files = flowconf.to_table(
            httpEx.scrape(url=self.__url,type='xml',tag='Contents')
        ).join(
            flowconf.to_table(db.select(self.__schema, self.__table)), 
            keys='id', join_type='left anti'
        )
        if self.__files.num_rows:
            for filename in self.__files.select([0]).to_pydict().get('filename'):
                httpEx.save(flowpath=load().flow, url=self.__url + filename)
        return db.adbc(self.__files, self.__schema, self.__table)