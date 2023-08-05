#!/usr/bin/env python
# encoding: utf-8

from setuptools import setup, find_packages

setup(name='CuteR',
      version='1.0',
      description='Custom QR Code with picture',
      author='Chinuno Usami',
      author_email='usami@chinuno.com',
      url='https://github.com/chinuno-usami/CuteR',
      license = 'GPLv3',
      packages=['CuteR',],
      install_requires=['qrcode', 'Pillow'],
      entry_points="""
        [console_scripts]
        CuteR = CuteR.CuteR:main
        """,
     )
