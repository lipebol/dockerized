from common.db import db
from common.initialize import load
from common.httpEx import httpEx
from xmltodict import parse
import pyarrow as arrow


class flowconf:

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

    @staticmethod
    def pull():
        __url = load.variable('DIVVY_BIKES')
        __schema, __table = 'divvy_bikes', 'files'
        __files = db.select(__schema, __table)
        __newfiles = flowconf.to_table(
            httpEx.scrape(url=__url,type='xml',tag='Contents')
        )
        if len(__files):
            __newfiles = __newfiles.join(
                flowconf.to_table(__files), 
                keys='id', join_type='left anti'
            )
        if __newfiles.num_rows:
            for filename in __newfiles.select([0]).to_pydict().get('filename'):
                httpEx.save(flowpath=load().flow, url=__url + filename)
        return db.adbc(__newfiles, __schema, __table)