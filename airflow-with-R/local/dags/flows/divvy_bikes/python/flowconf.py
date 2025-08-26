from common.initialize import load
from common.httpEx import httpEx


class flowconf:

    def setname(self):
        pass

    @staticmethod
    def pull():
        return httpEx.save(
            flowpath=load().flow, 
            url='https://divvy-tripdata.s3.amazonaws.com/202007-divvy-tripdata.zip'
        )