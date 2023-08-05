"""
Pybencoding
===========

Pybencoding is a simple python 3 implementation of bittorrent's bencoding.

 * `Gitlab page <https://gitlab.com/clueless/pybencoding>`_
 * `Documentation <https://pybencoding.readthedocs.org/en/latest/>`_
"""
from setuptools import setup
from codecs import open
from os import path

setup(
    name='pybencoding',
    version='0.1.1',

    description="A simple python3 implementation of bittorrent's bencoding.",
    long_description=__doc__,
    url='https://gitlab.com/clueless/pybencoding',
    author='clueless',
    author_email='clueless@thunked.org',
    license='MIT',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
				'Programming Language :: Python :: 3 :: Only',
				'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
				'Programming Language :: Python :: 3.5'
    ],
    keywords='bittorrent bencode',
    packages=['pybencoding'],
)

