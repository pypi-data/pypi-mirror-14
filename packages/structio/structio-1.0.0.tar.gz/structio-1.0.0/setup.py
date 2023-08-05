from setuptools import setup
import sys

NAME = 'structio'
VERSION = '1.0.0'

install_requires = []

if sys.version < '3.4':
    install_requires.append('enum34')

setup(
    name=NAME,
    version=VERSION,
    py_modules=['structio'],
    description="Convenient, readable, struct-based stream I/O",

    author='Peter Ruibal',
    author_email='ruibalp@gmail.com',
    license='MIT',
    keywords='stream struct BytesIO StringIO',
    url='http://github.com/fmoo/python-structio',
    download_url='https://github.com/fmoo/python-structio/%s.tar.gz' % VERSION,

    install_requires=install_requires,
    #test_suite="tests",

    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
    ],
)
