#!/usr/bin/env python

import os

from io import open
from setuptools import setup, find_packages


here = os.path.dirname(__file__)
with open(os.path.join(here, 'README.rst'), 'r', encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='holocron-clear-theme',
    version='1.0.0',

    description='Holocron Clear Theme',
    long_description=long_description,
    license='MIT',
    url='http://github.com/ikalnitsky/holocron-clear-theme/',
    keywords='holocron blog generator theme clear simplicity',

    author='Igor Kalnitsky',
    author_email='igor@kalnitsky.org',

    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    zip_safe=False,

    install_requires=[
        'holocron >= 0.3.0',
    ],

    entry_points={
        'holocron.ext': [
            'clear-theme = holocron_clear_theme:ClearTheme',
        ],
    },

    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',

        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Information Technology',

        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Terminals',

        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
