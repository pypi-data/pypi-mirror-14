# -*- coding: utf-8 -*-
import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand
from yt_songs import __version__


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)


def read(fname):
    with open(fname) as fp:
        content = fp.read()
    return content

setup(
    name='yt-songs',
    version=__version__,
    description=('YT Songs searches, downloads and normalizes the titles'
                 'of a list of songs from youtube using youtube-dl.'),
    long_description=read('README.rst'),
    author='Minik Olsen',
    author_email='minikolsen9@gmail.com',
    url='https://github.com/MinikOlsen/yt-songs',
    license=read('LICENSE'),
    zip_safe=False,
    keywords='yt-songs',
    install_requires=[
        'youtube-dl',
        'beautifulsoup4',
        'gevent==1.1b6',
        'grequests',
        'pyyaml'
    ],
    dependency_links=['https://github.com/rg3/youtube-dl/'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    packages=['yt_songs'],
    package_data={'yt_songs': ['data/yt-songs.yaml', 'data/yt-videos.yaml']},
    entry_points={
        'console_scripts': [
            'yt-songs = yt_songs.yt_songs:main'
        ]
    },
    tests_require=['pytest'],
    cmdclass={'test': PyTest}
)
