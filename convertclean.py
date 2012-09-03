#!/bin/env python
# -*- coding: utf-8 -*-
import os


def convert_clean_images():
    def get_files():
        return [filename for filename in os.listdir('.')
                if filename[-3:] in ['png', 'jpg', 'gif']]

    for filename in get_files():
        os.rename(filename, filename.lower())

    for filename in get_files():
        basename, extension = os.path.splitext(filename)
        result = os.system('convert -resize 200x200 "%s" "%s"' %
                           (filename, basename + '.png'))
        if result == 0 and not filename.endswith('.png'):
            os.remove(filename)

    for filename in get_files():
        basename, extension = os.path.splitext(filename)
        if '_' in basename:
            word, sequence = basename.split('_')
            os.rename(filename, word + extension)

if __name__ == '__main__':
    os.chdir('media_def')
    convert_clean_images()

