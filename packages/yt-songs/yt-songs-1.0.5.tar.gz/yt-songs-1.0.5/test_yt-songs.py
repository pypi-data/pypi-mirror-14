# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from tempfile import gettempdir
from subprocess import check_output


def test_free_songs():
    '''Tries to download a list of free songs'''
    result = run_cmd('yt-songs get -v test_songs ' + gettempdir())

    assert '3/3 songs downloaded successfully' in result


def run_cmd(cmd):
    '''Run a shell command `cmd` and return its output.'''
    return check_output(cmd, shell=True).decode('utf-8')
