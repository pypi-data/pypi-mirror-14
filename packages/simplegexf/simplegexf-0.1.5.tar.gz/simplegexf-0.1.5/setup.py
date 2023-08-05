# -*- coding: utf-8 -*-
import os
from setuptools import setup

try:
    long_description = open("README.md").read()
except:
    long_description = ''

setup(
    name="simplegexf",
    version="0.1.5",
    py_modules=['simplegexf'],
    description="A simple .gexf parser/writer for python",
    license="MIT",
    url="https://github.com/demux/simplegexf",
    install_requires=['xmltodict==0.9.2'],
    long_description=long_description,
    keywords="simplegexf gephi gexf",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Development Status :: 3 - Alpha",
        "Topic :: Text Processing :: Markup :: XML",
        "Topic :: Scientific/Engineering :: Visualization",
        "License :: OSI Approved :: MIT License",
    ]
)
