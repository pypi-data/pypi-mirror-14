#!/usr/bin/env python3
#
# Copyright 2016 JZQT <tjy.jzqt@qq.com>

from setuptools import setup, find_packages

import tornext

setup(
    name='tornext',
    version=tornext.__version__,
    packages=find_packages(exclude=[]),
    install_requires=['tornado'],
    description='Tornext is a web framework based on tornado.',
    author='JZQT',
    author_email='tjy.jzqt@qq.com',
    url='',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='web tornado tornext',
    scripts=['tornext/bin/tornext-admin'],
    entry_points={
        'console_scripts': [
            'tornext-admin = tornext.management:execute_command_line',
        ],
    }
)
