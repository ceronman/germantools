from BeautifulSoup import BeautifulSoup, Tag
import urllib2
from unidecode import unidecode
from download_media import download_file
import re

def download_sound_tfd(word):
    BASE_URL = 'http://www.forvo.com/search-de/'
    BASE_MP3 = 'http://www.forvo.com/player-mp3Handler.php?path='

    page = urllib2.urlopen(BASE_URL + word)
    soup = BeautifulSoup(page)

    play_tag = soup.findAll(onclick=re.compile('^Play'))[0]

    media_location = play_tag['onclick'].split(',')[1][1:-1]
    media_url = BASE_MP3 + media_location
    filename = unidecode(word.decode('utf-8')) + '_forvo' + '.mp3'
    download_file(media_url, filename, 'media')

download_sound_tfd('alsterwasser')
