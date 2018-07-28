#!/usr/bin/env python3
# coding: utf-8

"""
A tool to download recurrent content from webpages. Main file.

Copyright (C) 2018 George Galanakis <galan87@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import configparser
import locale
import os
import shutil
from datetime import datetime
from urllib.request import urlretrieve

import pdfkit

locale.setlocale(locale.LC_ALL, 'el_GR.utf8')


def recursive_remove(folder):
    # http://stackoverflow.com/questions/185936/delete-folder-contents-in-python
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(e)


def download_weather(out_dir, cities_urls):
    # Manipulate the output directory
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    else:
        # Cleanup old files, if any
        recursive_remove(out_dir)

    # Get current date
    today = datetime.now()
    date_string = today.strftime('%d-%m-%Y')

    # Fire forecast image
    jpg_filename = today.strftime('%y%m%d') + '.jpg'  # e.g. '150712.jpg' for 15/07/2015
    fire_forecast_url = 'http://civilprotection.gr/sites/default/gscp_uploads/' + jpg_filename
    gif_file_path = out_dir + '/' + jpg_filename
    urlretrieve(fire_forecast_url, gif_file_path)
    os.rename(gif_file_path, os.path.join(out_dir, 'ΧΑΡΤΗΣ ΕΠΙΚΙΝΔΥΝΟΤΗΤΑΣ ' + date_string + '.jpg'))

    # Weather forecast PDFs
    options = {
        'page-size': 'A4',
        'no-background': None,
        'disable-internal-links': None,
        'margin-left': '2mm',
        'margin-right': '2mm'
    }

    for k in cities_urls.keys():
        pdfkit.from_url(cities_urls[k], os.path.join(out_dir, k + ' ' + date_string + '.pdf'), options=options)


def load_cities_urls(filepath):
    cities_urls = {}
    with open(filepath) as f:
        for i, l in enumerate(f):
            # Bypasss comments
            if l[0] == '#':
                continue
            name, url = l.partition(',')[::2]
            if not name or not url:
                raise ValueError('Malformed name, url pair in line {}.'.format(i))

            cities_urls[name.strip()] = url[:-1]

    return cities_urls


def main():
    # Read the configuration
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')

    out_dir = config.get('Settings', 'output_directory')

    out_dir += '/'

    # Manipulate the output directory
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    download_weather(os.path.join(out_dir, 'ΚΑΙΡΟΣ'), load_cities_urls('weather_urls'))

if __name__ == "__main__":
    main()
