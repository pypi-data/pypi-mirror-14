import os
import argparse
import json
from nicovideo_api import NicovideoAPI
from sound_extractor import SoundExtractorFactory
from config import Config
from gazeru import Gazeru

if __name__ == '__main__':
    argparser = argparse.ArgumentParser(description='gazeru is niconico downloader')
    argparser.add_argument('-l', '--list',help='display registered mylist', action='store_true')
    argparser.add_argument('-a', '--add', help='add mylist')
    argparser.add_argument('-u', '--user', nargs=2, help='set user and password')
    argparser.add_argument('-d', '--directory', help='set download directory')
    args = argparser.parse_args()

    gazeru = Gazeru()
    if args.list:
        print('{0:10} {1:10} {2}'.format('id', 'creator', 'title'))
        for mylist in gazeru.get_mylists():
            print('{0:10} {1:10} {2}'.format(mylist['id'], mylist['creator'], mylist['title']))

    elif args.add:
        mylist_id = args.add
        try:
            gazeru.add_mylist(mylist_id)
        except AlreadyRegisteredMylistError:
            print('{0} is already registed'.format(mylist_id))

    elif args.user:
        user = args.user[0]
        password = args.user[1]
        gazeru.set_account(user, password)

    elif args.directory:
        """引数で渡されたディレクトリ を config ファイルに書き込んで、
        該当のディレクトリに.gazeruファイルを設置する
        .gazeruファイルは mylist_id: [{ダウンロードされたvideo_id: ファイル名}] という形式で書き込まれる
        """
        directory = args.directory
        gazeru.set_direcctory(directory)

        dot_gazeru = '{0}/.gazeru'.format(directory)
        with open(dot_gazeru, 'w') as file:
            config = Config()
            mylists = config.get_mylists()
            file.write(json.dumps({mylist['id']:[] for mylist in mylists}))
        config = Config()
        config.set_directory(directory)

    else:
        gazeru.pull()
