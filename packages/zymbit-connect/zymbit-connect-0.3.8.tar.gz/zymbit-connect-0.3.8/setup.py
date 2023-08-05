#!/usr/bin/env python
import os

from distutils.core import setup

SCRIPT_DIR = os.path.dirname(__file__)
if not SCRIPT_DIR:
        SCRIPT_DIR = os.getcwd()

README = os.path.join(SCRIPT_DIR, 'README.md')
if not os.path.exists(README):
    with open(README, 'wb') as fh:
        with open(os.path.join(SCRIPT_DIR, '..', 'README.md'), 'rb') as fh2:
            fh.write(fh2.read())

# put together list of requirements to install
install_requires = []
with open(os.path.join(SCRIPT_DIR, 'requirements.txt')) as fh:
    for line in fh.readlines():
        if line.startswith('-'):
            continue

        install_requires.append(line.strip())

data_files = []

setup(name='zymbit-connect',
      version='0.3.8',
      description='Zymbit Connect',
      author='Roberto Aguilar',
      author_email='roberto@zymbit.com',
      packages=[
          'zymbit',
          'zymbit.connect',
          'zymbit.upstream',
          'zymbit.util',
      ],
      scripts=[
          'scripts/connect',
          'scripts/write_auth_token',
      ],
      data_files=data_files,
      long_description=open('README.md').read(),
      url='http://zymbit.com/',
      license='LICENSE',
      install_requires=install_requires,
)
