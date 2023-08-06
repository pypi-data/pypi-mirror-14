#!/usr/bin/env python
from setuptools import setup
from os import path

setup(
    name = 'bambu-mail',
    version = '3.4',
    description = 'A shortcut function for sending template-based emails in HTML and plain-text format',
    author = 'Steadman',
    author_email = 'mark@steadman.io',
    url = 'https://github.com/iamsteadman/bambu-mail',
    long_description = open(path.join(path.dirname(__file__), 'README')).read(),
    install_requires = [
        'Django>=1.8',
        'bambu-markup>=3.0',
        'httplib2'
    ],
    packages = [
        'bambu_mail',
        'bambu_mail.newsletter',
        'bambu_mail.backends'
    ],
    package_data = {
        'bambu_mail': [
            'templates/mail/*.html',
            'templates/mail/*.txt'
        ]
    },
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django'
    ]
)
