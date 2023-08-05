#!/usr/bin/env python

from setuptools import setup, find_packages


setup(
    name='Pyjoyment',
    version='0.0.1',
    description='An asynchronous, event driver web framework for the Python programming language.',
    long_description=''.join(open('README.md').readlines()[2:]),
    author='Piotr Roszatycki',
    author_email='piotr.roszatycki@gmail.com',
    url='http://github.com/dex4er/Pyjoyment',
    download_url='https://github.com/dex4er/Pyjoyment/archive/master.zip',
    license='Artistic',
    include_package_data=True,
    zip_safe=True,
    keywords='async framework html http mojo mojolicious pyjo pyjoyment tap test websocket wsgi',
    packages=find_packages(exclude=['t', 't.*']),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Artistic License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Server',
        'Topic :: Software Development :: Testing',
    ],
    test_suite='test.TestSuite',
    install_requires=[
    ],
    extras_require={
    },
)
