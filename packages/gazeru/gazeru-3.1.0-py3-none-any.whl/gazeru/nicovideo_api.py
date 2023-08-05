import requests
import urllib.parse
import re
from pyquery import PyQuery as pq

class NotFoundError(Exception):
    pass

class NicovideoAPI:
    def __init__(self, mailaddress, password):
        self.login(mailaddress, password)

    def login(self, mailaddress, password):
        response = requests.post(
            "https://secure.nicovideo.jp/secure/login?site=niconico",
            data = {'mail_tel': mailaddress,
                    'password': password},
            allow_redirects = False
        )
        self._cookies = response.cookies

    def get_thumb_info(self, video_id):
        response = requests.get("http://ext.nicovideo.jp/api/getthumbinfo/{0}".format(video_id))
        dom = pq(response.content, parser='xml')
        return {'video_id': dom('video_id').text(),
                'title': dom('title').text(),
                'description': dom('desctiption').text(),
                'thumbnail_url': dom('thumbnail_url').text(),
                'first_retrieve': dom('first_retrieve').text(),
                'length': dom('length').text(),
                'movie_type': dom('movie_type').text(),
                'size_high': dom('size_high').text(),
                'size_low': dom('size_low').text(),
                'view_counter': dom('view_counter').text(),
                'comment_num': dom('comment_num').text(),
                'mylist_counter': dom('mylist_counter').text(),
                'last_res_body': dom('last_res_body').text(),
                'watch_url': dom('watch_url').text(),
                'thumb_type': dom('thumb_type').text(),
                'embeddable': dom('embeddable').text(),
                'no_live_play': dom('no_live_play').text(),
                'tags': [{'tag': tag.text(), 'lock': tag.attr('lock')} for tag in dom('tags').items('tag')],
                'user_id': dom('user_id').text(),
                'user_nickname': dom('user_nickname'),
                'user_icon_url': dom('user_icon_url')}

    def get_flv(self, video_id):
        flv_url = self._get_flv_url(video_id)
        response = requests.get(flv_url, cookies=self._cookies)
        content = response.content
        return content

    def get_mylist_info(self, mylist_id):
        response = requests.get('http://www.nicovideo.jp/mylist/{0}?rss=2.0&lkang=ja-jp'.format(mylist_id))
        if response.status_code == 404:
            raise NotFoundError()
        else:
            dom = pq(response.content, parser='xml')
            title = dom('channel > title').text()
            creator = dom('channel > dc\:creator').text()
            mylist = {'id': mylist_id,
                    'title': title,
                    'creator': creator,
                    'video_list': [re.search(r'[^/]*$', link.text).group(0) for link in dom('channel item link')]}
        return mylist

    def _get_flv_url(self, video_id):
        self._cookies.update(self._get_nicohistory_cookie(video_id))
        getflv_url = 'http://flapi.nicovideo.jp/api/getflv/{0}'.format(video_id)
        if video_id[:2] == 'nm':
            getflv_url = 'http://flapi.nicovideo.jp/api/getflv/{0}?as3=1'.format(video_id)
        response = requests.get(getflv_url, cookies=self._cookies)
        response_body = urllib.parse.unquote(response.text)
        flv_url = re.search(r'url=([^&]+)', response_body).group(1)
        return flv_url

    def _get_nicohistory_cookie(self, video_id):
        response = requests.get('http://www.nicovideo.jp/watch/' + video_id, cookies=self._cookies)
        return response.cookies
