#!/bin/env python
# -*- coding: utf-8 -*-
import os
import random
import re
import sys
import time
import traceback
import urllib2

from BeautifulSoup import BeautifulSoup
from googlesearch import Google, ImageOptions, ImageType
from unidecode import unidecode


def logexceptions(function):
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except:
            name = function.__name__
            print >> sys.stderr, '**** Error running', name, repr(args)
            traceback.print_exc(file=sys.stderr)
    return wrapper


@logexceptions
def download_file(url, filename, dir):
    content = urllib2.urlopen(url, timeout=20)
    fileobj = open(os.path.join(dir, filename), 'wb')
    fileobj.write(content.read())
    fileobj.close()


@logexceptions
def download_sound_tfd(word):
    BASE_URL = 'http://de.thefreedictionary.com/'
    BASE_MP3 = 'http://img.tfd.com/pron/mp3/'
    page = urllib2.urlopen(BASE_URL + word)
    soup = BeautifulSoup(page)

    play_function = soup.findAll(text=re.compile('^playV2'))[0]
    media_location = play_function[8:-2]

    media_url = BASE_MP3 + media_location + '.mp3'
    filename = unidecode(word.decode('utf-8')) + '.mp3'
    download_file(media_url, filename, 'media_pre')


@logexceptions
def download_sound_forvo(word):
    BASE_URL = 'http://www.forvo.com/search-de/'
    BASE_MP3 = 'http://www.forvo.com/player-mp3Handler.php?path='

    page = urllib2.urlopen(BASE_URL + word)
    soup = BeautifulSoup(page)

    play_tag = soup.findAll(onclick=re.compile('^Play'))[0]

    media_location = play_tag['onclick'].split(',')[1][1:-1]
    media_url = BASE_MP3 + media_location
    filename = unidecode(word.decode('utf-8')) + '_forvo' + '.mp3'
    download_file(media_url, filename, 'media_pre')


@logexceptions
def download_images(word):
    result1 = Google.search_images(word)
    options = ImageOptions()
    options.image_type = ImageType.CLIPART
    result2 = Google.search_images(word, options)
    word = word.decode('utf-8')
    for i, result in enumerate(result1 + result2):
        if result.format not in ['jpg', 'png', 'gif']:
            continue
        filename = '%s_%d.%s' % (unidecode(word), i, result.format)
        download_file(result.link, filename, 'media_pre')


@logexceptions
def download_words(words_filename):
    for line in open(words_filename):
        word = line[4:].lower().strip()
        download_sound_tfd(word)
#        download_sound_forvo(word)
#        download_images(word)
#        time.sleep(random.randint(1, 5))

if __name__ == '__main__':
    filename = sys.argv[1]
    download_words(filename)
