#!/usr/bin/env python

from distutils.core import setup
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='FTPwalker',
      packages=['FTPwalker', "FTPwalker/daemons"],
      version='0.4',
      description='Optimally traversing extremely large FTP directory trees.',
      author='Bohdan Khomtchouk and Kasra Vand',
      author_email='khomtchoukmed@gmail.com, kasraavand@gmail.com',
      url='https://github.com/Bohdan-Khomtchouk/FTPwalker',
      download_url='https://github.com/Bohdan-Khomtchouk/FTPwalker/tarball/0.1',
      keywords=['FTP', 'traverse', 'directory tree', 'optimized'],
      classifiers=[],
      long_description=read("README"))
