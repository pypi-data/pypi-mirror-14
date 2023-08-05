#!/usr/bin/env python

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils import setup, find_packages
import sys

if sys.version_info < (3, 3):
    install_requires = ['ipaddress']
else:
    install_requires = []

setup(
    name='pypcalc',
    version='0.1',
    author='James Brown',
    author_email='jbrown@easypost.com',
    url='https://github.com/easypost/pypcalc',
    license='ISC',
    packages=find_packages(exclude=['tests']),
    keywords=['networking'],
    description='Simple command-line tool for analyzing network addresses',
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'pypcalc = pypcalc.main:main',
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Intended Audience :: End Users/Desktop',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Topic :: System :: Networking'
    ]
)
