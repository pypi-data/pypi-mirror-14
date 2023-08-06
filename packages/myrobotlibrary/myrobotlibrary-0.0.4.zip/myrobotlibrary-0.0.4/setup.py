from distutils.core import setup
from setuptools import setup, find_packages

setup(
    name = 'myrobotlibrary',
    version = '0.0.4',
    keywords = ('simple', 'test'),
    description = 'just a simple test',
    license = 'MIT License',

    author = 'jim',
    author_email = 'jim@126.com',

    packages = find_packages(),
    platforms = 'any',
)