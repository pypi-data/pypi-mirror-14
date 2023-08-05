# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 17:16:52 2016

@author: Animesh Kumar Jha
"""

from setuptools import setup
#from distutils.core import setup
from codecs import open
import os

#here = path.abspath(path.dirname(__file__))
os.path.dirname(os.path.realpath('__file__'))

setup(
    name='new_my_json',
    version='1.0.0',
    author='Animesh Kumar Jha',
    author_email='animesh-kumar.jha@ucdconnect.ie',
    packages=['new_my_json'],
    #url='http://pypi.python.org/pypi/new_my_json',
    license='LICENSE.txt',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],    
    description='convert all the data to json',
    long_description=open('README.rst').read(),

)