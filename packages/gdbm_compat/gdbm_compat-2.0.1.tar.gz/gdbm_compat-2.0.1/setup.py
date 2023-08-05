#!/usr/bin/env python

import os
from setuptools import setup


dirName = os.path.dirname(__file__)
if dirName and os.getcwd() != dirName:
    os.chdir(dirName)


if __name__ == '__main__':
    with open('README.rst', 'rt') as f:
        long_description = f.read()

    setup(name='gdbm_compat',
            version='2.0.1',
            packages=['gdbm_compat'],
            author='Tim Savannah',
            author_email='kata198@gmail.com',
            maintainer='Tim Savannah',
            maintainer_email='kata198@gmail.com',
            description='Allows using gdbm files created with version 1.8 or 1.10, without magic number errors.',
            long_description=long_description,
            license='Public Domain',
            keywords=['gdbm', '1.8', '1.10', 'compat', 'bad', 'magic', 'number', 'traceback', 'el6', 'el7', 'centos', 'open', 'database'],
            classifiers=['Development Status :: 5 - Production/Stable',
                         'Programming Language :: Python',
                         'License :: Public Domain',
                         'Programming Language :: Python :: 2',
                          'Programming Language :: Python :: 2',
                          'Programming Language :: Python :: 2.6',
                          'Programming Language :: Python :: 2.7',
                          'Programming Language :: Python :: 3',
                          'Programming Language :: Python :: 3.3',
                          'Programming Language :: Python :: 3.4',
                          'Topic :: Software Development :: Libraries :: Python Modules',
            ]
    )



