import mutagen.mp3

sound = mutagen.mp3.MP3('/home/roronya/test.mp3')
print(sound)
sound['title'] = 'mikuchan'
sound['artist'] = 'miku'
sound['album'] = 'mikumiku'
print(sound)

sound.save()
