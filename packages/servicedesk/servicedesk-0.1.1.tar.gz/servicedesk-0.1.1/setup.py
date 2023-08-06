#!/usr/bin/env python

from distutils.core import setup

setup(
    name='servicedesk', version='0.1.1',
    description='ManageEngine ServiceDesk API helper',
    author='Brandon Ingalls',
    author_email='Brandon@Ingalls.io',
    url='https://github.com/BrandonIngalls/servicedesk',
    install_requires=['python-cjson', 'requests'],
    packages=['servicedesk', 'servicedesk.classes'])
