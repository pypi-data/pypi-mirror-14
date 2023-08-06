#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

install_requires = []
try:
    with open('requirements.txt', 'rb') as req_file:
        install_requires = [r.strip() for r in req_file.readlines()]
except Exception, e:
    print 'Are you testing? %s' % e

test_requirements = []
try:
    with open('requirements_dev.txt', 'rb') as req_file:
        test_requirements = [r.strip() for r in req_file.readlines()]
except Exception, e:
    print 'Are you testing? %s ' % e

setup(
    name='vxscreenshots',
    version='2.6.19',
    description="vxscreenshots: Basic Screenshots manager pushing and sharing"
    " automatically to Amazon S3 alá Skitch",
    long_description=readme + '\n\n' + history,
    author="Vauxoo OpenSource Specialists",
    author_email='nhomar@vauxoo.com',
    maintainer='Nhomar Hernández',
    maintainer_email='nhomar@vauxoo.com',
    url='https://github.com/vauxoo/vxscreenshots',
    packages=[
        'vxscreenshots',
    ],
    package_dir={'vxscreenshots': 'vxscreenshots'},
    include_package_data=True,
    keywords='vxscreenshots',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Customer Service',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Natural Language :: Spanish',
        'Programming Language :: Python :: 2.7',
    ],
    license=open('LICENSE').read(),
    test_suite='tests',
    platforms=['Linux'],
    install_requires=install_requires,
    scripts=[
        'bin/screenshot.sh',
    ],
    entry_points='''
        [console_scripts]
        vxsswatcher=vxscreenshots.watch:cli
        vxssicon=vxscreenshots.vxscreenshots:cli
    '''
)
