#!/usr/bin/env python

import os

from setuptools import setup


__dirname = os.path.abspath(os.path.dirname(__file__))
VERSION = '1.0.1'

with open(os.path.join(__dirname, 'README.rst')) as readme:
    README = readme.read()

setup(
    name='httpobs-cli',
    version=VERSION,
    description='HTTP Observatory: a command line tool to scan your website',
    url='https://github.com/mozilla/http-observatory-cli',
    download_url='https://github.com/mozilla/http-observatory-cli/httpobs-cli/tarball/' + VERSION,
    license='MPL 2.0',
    long_description=README,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Natural Language :: English',
        'Topic :: Security',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
    ],
    author='April King',
    author_email='april@mozilla.com',
    packages=[],
    include_package_data=True,
    scripts=['httpobs-cli/scripts/httpobs'],
    zip_safe=False,
)
