from distutils.core import setup
from setuptools import setup

dependencies = ['requests']

setup(
  name = 'apicheck',
  packages = ['apicheck'],
  version = '1.0.4',

  description = 'A Python tool and framework for testing JSON based web APIs',
  entry_points = {
        "console_scripts": ['apicheck = apicheck.apicheck:main']
        },
  author = 'Brad Kuykendall',
  author_email = 'brad.kuykend@gmail.com',
  url = 'https://github.com/kuykendb/APICheck',
  download_url = 'https://github.com/kuykendb/APICheck/tarball/v1.0-beta.1', 
  install_requires=dependencies,
  keywords = ['testing', 'api', 'web', 'json', 'test'],
  classifiers = [],
)