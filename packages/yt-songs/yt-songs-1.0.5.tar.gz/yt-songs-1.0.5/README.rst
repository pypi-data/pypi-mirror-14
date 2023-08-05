===============================
yt-songs
===============================

.. image:: https://badge.fury.io/py/yt-songs.png
    :target: http://badge.fury.io/py/yt-songs

.. image:: https://travis-ci.org/MinikOlsen/yt-songs.png?branch=master
        :target: https://travis-ci.org/MinikOlsen/yt-songs


YT Songs searches, downloads and normalizes the titles of a list of songs from youtube using youtube-dl.

Installation
------------

Install with pip:

.. code:: bash

        pip install -U yt-songs

Usage
-------

Create a songs file like test_songs_ and run:

.. _test_songs: https://github.com/MinikOlsen/yt-songs/blob/master/test_songs

.. code:: bash

        yt-songs get SONGS_FILE DST_FOLDER

Options:

- **-v** or **--verbose** to print the full youtube-dl output.
- **-s** or **--skip** to skip the normalization.
- **-n** NUMBER or **--number** NUMBER to download a search result other than the first.
- **-c** FILE or **--config** FILE to use a different  config file. It may be useful to have multiple config files for different needs.

Configuration
-------------

Since yt-songs runs on top of youtube-dl, any `youtube-dl option`_ can be used for yt-songs, with exception of *logger* and *progress_hooks*, which are set internally.

The following command opens the YAML config file in the user's preferred editor:

.. code:: bash

        yt-songs config -e

.. _`youtube-dl option`: https://github.com/rg3/youtube-dl/blob/master/youtube_dl/YoutubeDL.py#L121-L269

The options for yt-songs are:

name_template
    A `name template`_ for youtube-dl's output. This option overwrites its youtube-dl analogue outtmpl in ydl_opts.

    .. _`name template`: https://github.com/rg3/youtube-dl#output-template

temp_folder
  A temporary folder to store the files before normalizing the titles.

replacements
  The replacements to perform with regular expressions in order to normalize the titles.

ydl_opts
  Youtube-dl options.

Requirements
------------

- FFmpeg_ or Libav_
- Python >= 2.7 or >= 3.3

.. _FFmpeg: http://ffmpeg.org/
.. _Libav: https://libav.org/download/

License
-------

MIT licensed. See the bundled `LICENSE <https://github.com/MinikOlsen/yt-songs/blob/master/LICENSE>`_ file for more details.
