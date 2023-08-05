import os
import json
import logging
import re
from logging import FileHandler, Formatter
import requests
import mutagen.mp3
import mutagen.id3
import nicopy
from .config import Config
from .mp3extractor import Mp3ExtractorFactory
from .exception import *


class Gazeru:

    def __init__(self):
        self.config = Config()
        self.sound_extractor_factory = Mp3ExtractorFactory()
        self.dot_gazeru = '{0}/.gazeru'.format(self.config.get_directory())
        self.GAZEL_HOME = '{0}/.gazeru'.format(os.environ['HOME'])
        self.setup_logger()

    def setup_logger(self):
        logging.basicConfig(
            level=logging.ERROR, format='%(asctime)s- %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        file_handler = FileHandler('{0}/log/gazeru.log'
                                   .format(self.GAZEL_HOME), 'a+')
        file_handler.level = logging.INFO
        file_handler.formatter = Formatter(fmt='%(asctime)s %(message)s',
                                           datefmt='%Y/%m/%d %p %I:%M:%S')
        self.logger.addHandler(file_handler)
        return self

    def get_mylists(self):
        return self.config.get_mylists()

    def set_account(self, user, password):
        self.config.set_user(user)
        self.config.set_password(password)
        # login 失敗したら nicopy.FailedLoginError を投げる
        nicopy.login(self.config.get_user(), self.config.get_password())
        self.logger.info('set user and password')
        return self

    def set_directory(self, directory):
        self.config.set_directory(directory)
        self.dot_gazeru = '{0}/.gazeru'.format(self.config.get_directory())
        self.logger.info('set directory to {0}'.format(directory))
        return self

    def add_mylist(self, mylist_id):
        registered_mylist_id_list = [mylist['id']
                                     for mylist in self.config.get_mylists().values()]
        if mylist_id in registered_mylist_id_list:
            raise AlreadyRegisteredMylistError()
        try:
            mylist_info = nicopy.get_mylist_info(mylist_id)
        except NotFoundError:
            raise NotFoundMylistError()
        self.config.add_mylist({mylist_id:
                                {'id': mylist_id,
                                 'creator': mylist_info['creator'],
                                 'title': mylist_info['title']}})
        self.logger.info('add mylist {0}'.format(mylist_id))

    def remove_mylist(self, mylist_id):
        registered_mylist_id_list = [mylist['id']
                                     for mylist in self.config.get_mylists().values()]
        if mylist_id not in registered_mylist_id_list:
            raise NotRegisteredMylistError()
        self.config.remove_mylist(mylist_id)
        self.logger.info('remove mylist {0}'.format(mylist_id))

    def get_uploaded_mylist_info(self):
        uploaded_mylist_info = {mylist['id']: nicopy.get_mylist_info(mylist['id'])
                                for mylist in self.config.get_mylists().values()}
        return uploaded_mylist_info

    def get_logged(self):
        with open(self.dot_gazeru, 'r') as file:
            downloaded = json.loads(file.read())
        return downloaded

    def get_existed(self):
        """
        {'164': {'マイリス': [], 'mylis2': []}, 'sasakureUK': {'マイリス': []}}
        """
        download_directory = self.config.get_directory()
        existed = {creator:
                   {mylist:
                    os.listdir('{0}/{1}/{2}'
                               .format(download_directory, creator, mylist))
                    for mylist in os.listdir('{0}/{1}'.format(download_directory, creator))
                    if os.path.isdir('{0}/{1}/{2}'.format(download_directory, creator, mylist))}
                   for creator in os.listdir(download_directory)
                   if os.path.isdir('{0}/{1}'.format(download_directory, creator))}
        return existed

    def remove_extension(self, filename):
        filename = filename.replace('.mp3', '')\
                           .replace('.m4a', '')
        return filename

    def pull(self):
        if not os.path.exists(self.dot_gazeru):
            self.create_dot_gazeru()
            self.logger.info('create {0}'.format(self.dot_gazeru))

        existed = self.get_existed()
        uploaded_mylist_info = self.get_uploaded_mylist_info()
        # uploaded_mylist_info にあって existed にないものを列挙する
        downloading = {}
        for mylist in uploaded_mylist_info.values():
            creator = self.escape(mylist['creator'])
            mylist_title = self.escape(mylist['title'])
            if creator not in downloading:
                downloading[creator] = {}
            if mylist_title not in downloading[creator]:
                downloading[creator][mylist_title] = []

            for video in mylist['items']:
                video_title = self.escape(video['title'])
                if creator not in existed \
                   or mylist_title not in existed[creator] \
                   or video_title not in [self.remove_extension(video) for video in existed[creator][mylist_title]]:
                    downloading[creator][mylist_title].append(video)

        self.logger.info('downloading {0}'.format(downloading))
        download_directory = self.config.get_directory()
        for creator, mylists in downloading.items():
            for mylist_title, video_infos in mylists.items():
                for video_info in video_infos:
                    print('downloading {0}'.format(video_info['title']))
                    video, video_type = self.download_video(video_info['id'])
                    sound, sound_type = self.extract_sound(video, video_type)
                    sound_file_directory = '{0}/{1}/{2}'.format(
                        download_directory, self.escape(creator), self.escape(mylist_title))
                    os.makedirs(sound_file_directory, exist_ok=True)
                    sound_file_path = '{0}/{1}.{2}'.format(
                        sound_file_directory, self.escape(video_info['title']), sound_type)
                    with open(sound_file_path, 'wb') as file:
                        file.write(sound)

                    video_info_detail = nicopy.get_video_info(video_info['id'])
                    self.edit_id3(sound_file_path,
                                  mylist_title,
                                  video_info_detail['user_nickname'],
                                  video_info_detail['title'],
                                  video_info['position'],
                                  requests.get(video_info_detail['thumbnail_url']).content)
        return downloading

    def edit_id3(self, sound_file_path, album, artist, title, tracknumber, thumbnail):
        mp3 = mutagen.mp3.MP3(sound_file_path)
        try:
            mp3.add_tags(ID3=mutagen.id3.ID3)
        except mutagen.id3.error:
            pass
        mp3['TALB'] = mutagen.id3.TALB(encoding=3,
                                       text=album)
        mp3['TPE1'] = mutagen.id3.TPE1(encoding=3,
                                       text=artist)
        mp3['TIT2'] = mutagen.id3.TIT2(encoding=3,
                                       text=title)
        mp3['TRCK'] = mutagen.id3.TRCK(encoding=3,
                                       text=[str(tracknumber)])
        mp3.tags.add(
            mutagen.id3.APIC(
                encoding=3,
                mime='image/jpeg',
                type=3,
                desc='Cover',
                data=thumbnail
            )
        )
        mp3.save()

    def escape(self, string):
        string = string.replace("/", "＼")
        return string

    def extract_sound(self, video, video_info):
        self.logger.info('start exstacting {0}'.format(video_info['video_id']))
        sound_extractor = self.sound_extractor_factory.build(
            video, video_info['movie_type'])
        result = (sound_extractor.extract(video),
                  sound_extractor.get_sound_type())
        self.logger.info('finished exstracting {0}'.format(
            video_info['video_id']))
        return result

    def download_video(self, video_id):
        self.logger.info('start downloading {0}'.format(video_id))
        cookie = nicopy.login(self.config.get_user(),
                              self.config.get_password())
        video_info = nicopy.get_video_info(video_id)
        video_type = video_info['movie_type']
        flv = nicopy.get_flv(video_id, cookie)
        result = (flv, video_info)
        self.logger.info('finished downloading {0}'.format(video_id))
        return result

    def create_dot_gazeru(self):
        """
        {'sasakureUK': {'mylist': {'id': 12313, 'video_list': {'hogehoge': 'sm12312'}}}}
        {'sasakureUK': [{'id': 123123, 'video_list': {'hogehoge'}}]}
        """
        dot_gazeru = {mylist['creator']:
                      {mylist['title']:
                       {'id': mylist['id'], 'video_list': {}}
                       }
                      for mylist in self.config.get_mylists().values()}
        with open(self.dot_gazeru, 'w') as file:
            file.write(json.dumps(dot_gazeru))
        return self
