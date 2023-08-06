#!/usr/bin/env python

from setuptools import setup, find_packages
import hanglish

def readme():
    return open("README.md").read()

setup(
    name = 'hanglish',
    version = hanglish.__version__,
    keywords = ("hanglish", "hangman", "game", "xingming", "xiaoh", "english", "learning"),
    description = ("It is a simple tool for finding text you want to search from the folder you want."),
    long_description = readme(),

    author = 'xiaoh',
    author_email = 'xiaoh@about.me',
    url = 'https://github.com/pmars/hanglish',
    license="MIT Licence",

    packages = ['hanglish'],
    scripts = ['bin/hanglish'],
    data_files = [('bin', ['bin/words.dict'])]
)
