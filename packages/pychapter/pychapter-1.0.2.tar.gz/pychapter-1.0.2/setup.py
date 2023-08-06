#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup, find_packages


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'guessit',
    'kat',
    'addic7ed-cli',
    'PyQuery',
    'humanfriendly',
    'aiohttp',
    'xmltodict',
    'dill',
    'torrentstream'
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='pychapter',
    version='1.0.2',
    description="TV Series management tool",
    long_description=readme + '\n\n' + history,
    author="David Francos Cuartero",
    author_email='opensource@davidfrancos.net',
    entry_points = {'console_scripts':['pychapter=pychapter.api:server']},
    url='https://github.com/XayOn/pychapter',
    packages=find_packages(),
    package_dir={'pychapter':
                 'pychapter'},
    include_package_data=True,
    install_requires=requirements,
    license="ISCL",
    zip_safe=False,
    keywords='pychapter',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
