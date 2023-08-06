#!/usr/bin/env python3

from setuptools import setup

VERSION = '0.2.1.2'

setup(name='twitter2rss',
      version=VERSION,
      description='Parse Twitter users and create RSS files',
      long_description=open('README.rst', encoding='utf-8').read(),
      author='drymer',
      author_email='drymer@autistici.org',
      url='http://daemons.cf/cgit/gnusrss/about/',
      scripts=['twitter2rss.py'],
      license="GPLv3",
      data_files = [
          ('/var/www/twitter2rss/', ['index.php', 'twitter2rss.css'])
          ],
      install_requires=[
          "requests>=2.9.0",
          "pyrss2gen>=1.1",
          ],
      classifiers=["Development Status :: 4 - Beta",
                   "Programming Language :: Python",
                   "Programming Language :: Python :: 3",
                   "Programming Language :: Python :: 3.5",
                   "Operating System :: OS Independent",
                   "Operating System :: POSIX",
                   "Intended Audience :: End Users/Desktop"]
      )
