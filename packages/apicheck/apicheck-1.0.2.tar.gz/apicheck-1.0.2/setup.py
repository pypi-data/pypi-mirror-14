from distutils.core import setup
from setuptools import setup

setup(
  name = 'apicheck',
  packages = ['apicheck'],
  version = '1.0.2',
  description = 'A Python API testing tool for JSON based APIs',
  entry_points = {
        "console_scripts": ['apicheck = apicheck.apicheck:main']
        },
  author = 'Brad Kuykendall',
  author_email = 'brad.kuykend@gmail.com',
  url = 'https://github.com/kuykendb/APICheck',
  download_url = 'https://github.com/kuykendb/APICheck/tarball/v1.0-beta.1', 
  keywords = ['testing', 'api', 'web', 'json', 'test'],
  classifiers = [],
)