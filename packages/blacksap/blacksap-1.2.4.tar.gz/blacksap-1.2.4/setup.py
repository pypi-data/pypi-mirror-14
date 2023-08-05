#!/usr/bin/env python
# coding=utf-8
"""Setup script for blacksap project"""

from setuptools import setup
from distutils.util import get_platform

setup(name='blacksap',
      version='1.2.4',
      description='Track torrent RSS feeds',
      author='Jesse Almanrode',
      author_email='jesse@almanrode.com',
      url='https://bitbucket.org/isaiah1112/blacksap',
      py_modules=['blacksap'],
      license='GNU General Public License v3 or later (GPLv3+)',
      install_requires=['Click==6.3',
                        'colorama==0.3.6',
                        'feedparser==5.2.1',
                        'requests==2.9.1',
                        ],
      platforms=['macosx-10.11',
                 'macosx-10.10',
                 ],
      entry_points="""
            [console_scripts]
            blacksap=blacksap:cli
      """,
      classifiers=[
          'Programming Language :: Python',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
          'Natural Language :: English',
          'Development Status :: 5 - Production/Stable',
          'Operating System :: MacOS :: MacOS X',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          ],
      )
