#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='django-glitter-events',
    version='0.1',
    description='Glitter Events for Django',
    long_description=open('README.rst').read(),
    url='https://github.com/blancltd/django-glitter-events',
    maintainer='Blanc Ltd',
    maintainer_email='studio@blanc.ltd.uk',
    platforms=['any'],
    packages=find_packages(),
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    license='BSD',
)
