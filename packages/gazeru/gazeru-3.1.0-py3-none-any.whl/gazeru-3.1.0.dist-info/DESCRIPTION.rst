gazeru
======

ニコニコ動画の音声ダウンローダです
マイリスト単位で登録して、指定されたディレクトリに保存します

installation
============

ffmpeg, swftools のインストール
-------------------------------

各ディストリのパッケージ管理ツールで入るとおもいます

pip で gazeru をインストール
----------------------------

::

    $ pip install gazeru

usage
=====

init でニコニコ動画のログイン情報とダウンロード先のディレクトリを指定

::

    $ gazeru init niconico_user niconico_password download_directory

http://www.nicovideo.jp/mylist/6280579

をダウンロードしたい場合 add で URL の末尾の数字を渡す

::

    $ gazeru add 6280579

pull でダウンロードが開始

::

    $ gazeru pull

その他

::

    $ gazeru -h


