#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import find_packages, setup


description = 'Adapt botocore to paste'
here = os.path.abspath(os.path.dirname(__file__))
try:
    readme = open(os.path.join(here, 'README.rst')).read()
    changes = open(os.path.join(here, 'CHANGES.txt')).read()
    long_description = '\n\n'.join([readme, changes])
except:
    long_description = description


install_requires = [
    'botocore',
]


tests_require = [
]


setup(
    name='botocore_paste',
    version='0.2',
    description=description,
    long_description=long_description,
    author='OCHIAI, Gouji',
    author_email='gjo.ext@gmail.com',
    url='https://github.com/gjo/botocore_paste',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    test_suite='botocore_paste',
    tests_require=tests_require,
    extras_require={
        'testing': tests_require,
    },
    classifiers=[
        'Framework :: Paste',
        'Framework :: Pyramid',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
    ],
)
