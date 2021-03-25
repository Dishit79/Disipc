import os
import re
import sys

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

# 'setup.py publish' shortcut.

setuptools.setup(
    name="disipc",
    version='1.0',
    author="Dishit79",
    author_email="Dishit79@gmail.com",
    description="An easy to use discord python ipc server and client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Dishit79/DisIpc",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.4',
    install_requires=[
        "aiohttp >=3.7.4",
    ]

)
