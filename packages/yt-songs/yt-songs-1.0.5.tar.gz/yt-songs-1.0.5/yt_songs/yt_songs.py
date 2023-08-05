#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function
from os import path, listdir, rmdir, environ
from bs4 import BeautifulSoup
from subprocess import call
from shutil import move
import youtube_dl
import grequests
import argparse
import yaml
import time
import re
try:
    from urllib.parse import unquote
except ImportError:
    from urlparse import unquote


class YTSongs:
    url_regex = ('(?:youtube\.com\/\S*(?:(?:\/e(?:mbed))?\/'
                 '|watch\/?\?(?:\S*?&?v\=))|youtu\.be\/)'
                 '([a-zA-Z0-9_-]{6,11})')

    def __init__(self, config_path, logger):
        self.count = [0, 0]
        self.errors = []
        self.yt_links = []
        self.searches = []

        with open(config_path) as config_file:
            config = yaml.safe_load(config_file)

            self.temp = path.expanduser(config['temp_folder'])
            self.name = config['name_template']
            self.replaces = config['replacements']

            self.ydl_opts = config['ydl_opts']
            self.ydl_opts['logger'] = logger(self)
            self.ydl_opts['outtmpl'] = path.join(self.temp, self.name)
            self.ydl_opts['progress_hooks'] = [self.__count_status]

    def apply_replaces(self, title):
        if not self.skip_norm:
            for replace in self.replaces:
                title = re.sub(replace[0], replace[1], title,
                               flags=re.IGNORECASE)

        return title

    def normalize(self, perm):
        for tmp_title in listdir(self.temp):
            move(
                path.join(self.temp, tmp_title),
                path.join(
                    perm,
                    self.apply_replaces(tmp_title)
                )
            )

        rmdir(self.temp)
        print('Files moved and normalized successfully')

    def download(self, url):
        if url not in self.yt_links:
            self.yt_links.append(url)
            print('Calling youtube-dl: ' + url)

            with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
                ydl.download([url])
        else:
            print('Ignored duplicate: ' + url)

    def download_hook(self, response, **kwargs):
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.findAll("a", rel="spf-prefetch")

        if not links:
            name = re.search(r'search_query=([^&]+)', unquote(response.url))
            print('Not found: "' + name.group(1) + '"')
        else:
            self.download('https://www.youtube.com' +
                          links[self.res_index].get('href'))

    def search(self, title, hook):
        print('Searching: "' + title + '"')
        self.searches.append(
            grequests.get(
                'https://www.youtube.com/results?search_query=' +
                title,
                hooks={'response': hook}
            )
        )

    def handle_line(self, line):
        if not line.startswith('#') and line.strip():
            line = line.rstrip('\n')
            self.count[1] += 1

            if re.search(self.url_regex, line):
                self.download(line)
            else:
                self.search(line, self.download_hook)

    def run(self, songs_file, dest, res_index=0, skip_norm=False):
        self.res_index = res_index
        self.skip_norm = skip_norm

        for line in open(songs_file):
            self.handle_line(line)

        grequests.map(self.searches)

        if not self.count[0]:
            print('No songs downloaded')
        else:
            print(str(self.count[0]) + '/' + str(self.count[1]),
                  'songs downloaded successfully')

        self.normalize(dest)

        if self.errors:
            print('Unknown errors occurred in youtube-dl:')
            print('\n'.join(self.errors))

    def __count_status(self, download):
        name = path.splitext(path.basename(download['filename']))[0]
        if download['status'] == 'finished':
            print('Downloaded:', name)
            self.count[0] += 1
        elif download['status'] == 'error':
            self.errors.append(name)

config_path = path.join(
    path.dirname(path.abspath(__file__)),
    'data', 'yt-songs.yaml'
)


def main():
    parser = argparse.ArgumentParser(
        description=('YT-Songs searches, downloads and normalizes'
                     ' the titles of a list of songs from youtube'
                     ' using youtube-dl.')
    )

    subparsers = parser.add_subparsers(dest='mode')

    config_parser = subparsers.add_parser('config')
    config_parser.add_argument('-e', '--edit', action='store_true',
                               help='Edit config file.')

    main_parser = subparsers.add_parser('get')
    main_parser.add_argument('FILE',
                             help='Songs file containing one title per line.')
    main_parser.add_argument('PATH', help='Destination folder.')
    main_parser.add_argument('-n', '--number', metavar='N',
                             nargs='?', default=1, type=int,
                             help='Number of the search result to download.')
    main_parser.add_argument('-c', '--config', metavar='CONFIG_FILE',
                             help='Use a different config file.')
    main_parser.add_argument('-s', '--skip', action='store_true',
                             help='Skip normalization.')
    main_parser.add_argument('-v', '--verbose', action='store_true',
                             help='Print youtube-dl output.')
    args = parser.parse_args()

    class Logger:
        def __init__(self, caller_self):
            self.caller_self = caller_self

        def debug(self, msg):
            if args.verbose:
                print(msg)

        def warning(self, msg):
            self.caller_self.errors.append(msg)

        def error(self, msg):
            self.caller_self.errors.append(msg)

    if args.mode == 'config':
        call([environ.get('EDITOR', 'vim'), config_path])
    elif args.mode == 'get':
        start_time = time.time()

        chosen_config = args.config or config_path
        yts = YTSongs(chosen_config, Logger)
        yts.run(args.FILE, args.PATH, args.number - 1, args.skip)

        print('(' + str(round(time.time() - start_time)) + ' seconds)')
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
