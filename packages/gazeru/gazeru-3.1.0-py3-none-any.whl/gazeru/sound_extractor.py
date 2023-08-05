import subprocess
import os


class SoundExtractor:
    TMP_FILE = '/tmp/gazeru_tmp'

    def extract(self, video):
        file_handler = open(self.TMP_FILE, 'wb')
        file_handler.write(video)
        file_handler.close()
        return self._extract()

    def get_sound_type(self):
        return self._get_sound_type()

    def _extract(self):
        raise NotImplementedError()

    def _get_sound_type(self):
        raise NotImplementedError()


class Mp3ExtractorFromFlv(SoundExtractor):

    def _extract(self):
        SOUND_FILE = '{0}.mp3'.format(self.TMP_FILE)
        subprocess.call('ffmpeg -i {0} -acodec copy {1} > /dev/null 2>&1'
                        .format(self.TMP_FILE, SOUND_FILE), shell=True)
        file_handler = open(SOUND_FILE, 'rb')
        sound = file_handler.read()
        file_handler.close()
        os.remove(self.TMP_FILE)
        os.remove(SOUND_FILE)
        return sound

    def _get_sound_type(self):
        return 'mp3'


class Mp3ExtractorFromSwf(SoundExtractor):

    def _extract(self):
        SOUND_FILE = '{0}.mp3'.format(self.TMP_FILE)
        subprocess.call('swfextract -m {0} -o {1} > /dev/null 2>&1'
                        .format(self.TMP_FILE, SOUND_FILE), shell=True)
        file_handler = open(SOUND_FILE, 'rb')
        sound = file_handler.read()
        file_handler.close()
        os.remove(self.TMP_FILE)
        os.remove(SOUND_FILE)
        return sound

    def _get_sound_type(self):
        return 'mp3'


class M4aExtractorFromMp4(SoundExtractor):

    def _extract(self):
        SOUND_FILE = '{0}.mp4'.format(self.TMP_FILE)
        subprocess.call('ffmpeg -i {0} -vn -acodec copy {1} > /dev/null 2>&1'
                        .format(self.TMP_FILE, SOUND_FILE), shell=True)
        file_handler = open(SOUND_FILE, 'rb')
        sound = file_handler.read()
        file_handler.close()
        os.remove(self.TMP_FILE)
        os.remove(SOUND_FILE)
        return sound

    def _get_sound_type(self):
        return 'm4a'


class SoundExtractorFactory:

    def build(self, video, video_type):
        if (video_type == 'flv'):
            return Mp3ExtractorFromFlv()
        elif (video_type == 'mp4'):
            return M4aExtractorFromMp4()
        elif (video_type == 'swf'):
            return Mp3ExtractorFromSwf()
