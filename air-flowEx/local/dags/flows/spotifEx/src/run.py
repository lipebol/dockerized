#!/usr/bin/python3

from datetime import datetime
from dotenv import load_dotenv, find_dotenv
from file import File
from os import getenv
from web import Web
from system import System

class SpotifEx:
    
    load_dotenv(find_dotenv('.env'))
    def __init__(self) -> None:
        self.today = str(datetime.now().date())
        self._metadata = System.dbus()
        self._File = File(System())
        self._json = self._File.read('JSON_FILE')
        self._trackid = self._File.read('TRACKID') if self._File.exists('TRACKID') else False


    def trackFind(self) -> None or dict:
        if self.today not in self._json['spotifEx'].keys():
            self._json['spotifEx'].update({self.today: []})
        else:
            for idx, item in enumerate(self._json['spotifEx'][self.today]):
                if self._metadata['trackid'] == item['track']['trackid']:
                    return item


    def nextTrack(self) -> None or str:
        if self._metadata['trackid'] != self._trackid:
            return str(self._File.write('TRACKID', self._metadata['trackid']))


    def run(self):
        if self._metadata:
            self._Web = Web(System(), self._metadata)
            if self.nextTrack():
                self.find = self.trackFind()
                if not self.find:
                    self._metadata = self._Web.info()
                    if self._metadata:
                        self._json['spotifEx'][self.today].append(self._metadata)
                else:
                    self.find['listen'] += 1
                if self._File.new(
                    self._File.write('ORIGINAL_IMAGE', self._Web.image()), 'CURRENT_IMAGE'):
                    return self._File.write('JSON_FILE', self._json)
        

if __name__ == '__main__':
    app = SpotifEx()
    app.run()