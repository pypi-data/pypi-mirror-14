from setuptools import setup
import os

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = 'dploy',
    version = '0.0.2',
    download_url = 'https://github.com/arecarn/dploy/tarball/0.0.2',
    license = 'CC0',
    description = '',
    long_description=read('README.rst'),

    author = 'Ryan Carney',
    author_email = 'arecarn@gmail.com',

    url = 'https://github.com/arecarn/dploy',

    packages = ['dploy'],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities',
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    entry_points = {
        'console_scripts': ['dploy=dploy.__main__:main']
    },
)
