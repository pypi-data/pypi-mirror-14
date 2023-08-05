from codecs import open
from os import path
from setuptools import setup

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = 'lh3api',
    version = '0.1.0',
    description = 'Utilities for easily working with the LibraryH3lp APIs.',
    long_description = long_description,
    url = 'https://github.com/libraryh3lp/libraryh3lp-sdk-python',
    author = 'Nub Games, Inc.',
    author_email = 'support@libraryh3lp.com',
    license = 'MIT',
    keywords = 'libraryh3lp api sdk',
    packages = ['lh3'],
    install_requires = ['future', 'requests'],

    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5'
    ]
)
