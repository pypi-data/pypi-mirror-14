from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='pybencoding',
    version='0.1.0',

    description="A python3 implementation of bittorrent's bencoding that "
                "actually works.",
    long_description=long_description,
    url='https://gitlab.com/clueless/pybencoding',
    author='clueless',
    author_email='clueless@thunked.org',
    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='bittorrent bencode',
    packages=['pybencoding'],
)

