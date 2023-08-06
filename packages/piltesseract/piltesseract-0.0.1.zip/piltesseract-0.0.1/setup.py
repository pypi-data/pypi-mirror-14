#!/usr/bin/env python
import codecs
import json
import os
from setuptools import setup
    

modules = ["piltesseract",]
version_path = os.path.join("piltesseract", "_version.py")
with codecs.open(version_path) as f:
    version = '.'.join(str(e) for e in json.load(f))
with codecs.open('README.md', 'r', 'utf-8') as f:
    readme = f.read()


setup(
    name = "piltesseract",
    version=version,
    description = "Image-to-text Tesseract command line wrapper.",
    author='Christopher Digirolamo',
    author_email = "chrisdigirolamo@gmail.com",
    url = "https://github.com/Digirolamo/PILtesseract/",
    download_url = "https://github.com/Digirolamo/PILtesseract",
    license = "MIT License",
    py_modules = modules,
    test_suite='tests',
    data_files=[('', ['LICENSE'])],
    install_requires=['six>=1.8.0'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        ]
    )