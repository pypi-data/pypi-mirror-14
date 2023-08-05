#!/usr/bin/env python

from setuptools import setup, find_packages
# import aerate
DESCRIPTION = ("Aerate REST APIs: falcons with bravado and swagger.")
with open('README.rst') as f:
    LONG_DESCRIPTION = f.read()

install_requires = [
    'Cython>=0.23.4,<0.24',
    'pyyaml>=3.1',
    'falcon>=0.3.0,<0.4',
    'simplejson>=3.3.0,<4.0',
    'six>=1.10.0,<1.11',
    'bravado_core>=4.0.0,<4.1.0',
    'pymongo>=3.2,<3.3'
]


setup(
    name='Aerate',
    version='0.0.1.dev26',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author='Kelly Caylor',
    author_email='kelly@arable.com',
    url='http://aerate.arable.com',
    license='BSD',
    platforms=["any"],
    packages=find_packages(),
    test_suite="aerate.tests",
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content'
    ],
)
