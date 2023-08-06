#!/usr/bin/env python
from setuptools import setup
from os import path

setup(
    name = 'bambu-enquiries',
    version = '3.2',
    description = 'A simple model and contact form',
    author = 'Steadman',
    author_email = 'mark@steadman.io',
    url = 'https://github.com/iamsteadman/bambu-enquiries',
    long_description = open(path.join(path.dirname(__file__), 'README')).read(),
    install_requires = [
        'Django>=1.8',
        'requests',
        'bambu-mail'
    ],
    packages = [
        'bambu_enquiries',
        'bambu_enquiries.migrations'
    ],
    package_data = {
        'bambu_enquiries': [
            'templates/enquiries/*.html',
            'templates/enquiries/*.txt'
        ]
    },
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django'
    ]
)
