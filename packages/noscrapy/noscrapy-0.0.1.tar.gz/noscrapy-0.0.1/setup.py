# -*- coding: utf-8 *-*
import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="noscrapy",
    version="0.0.1",
    author="Mathias Seidler",
    author_email="seishin@gmail.com",
    description=("Python port attempt of web-scraper-chrome-extension."),
    license="MIT",
    url="https://github.com/katakumpo/noscrapy",
    packages=find_packages(exclude=['noscrapy.tests*']),
    long_description=read('README.rst'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
)
