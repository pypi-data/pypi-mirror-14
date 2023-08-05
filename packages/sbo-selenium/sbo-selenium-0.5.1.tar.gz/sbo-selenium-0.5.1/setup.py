#!/usr/bin/env python

import codecs
import os
from pip.download import PipSession
from pip.index import PackageFinder
from pip.req import parse_requirements
from setuptools import setup, find_packages

install_requires = [
    'Django>=1.5',
    'requests',
    'selenium',
]

on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
if on_rtd:
    root_dir = os.path.abspath(os.path.dirname(__file__))
    session = PipSession()
    requirements_path = os.path.join(root_dir, 'requirements', 'documentation.txt')
    finder = PackageFinder([], [], session=session)
    requirements = parse_requirements(requirements_path, finder, session=session)
    install_requires.extend([str(r.req) for r in requirements])

with codecs.open('README.rst', 'r', 'utf-8') as f:
    long_description = f.read()


version = '0.5.1'  # Remember to update docs/CHANGELOG.rst when this changes

setup(
    name="sbo-selenium",
    version=version,
    packages=find_packages(),
    zip_safe=False,
    description="Selenium testing framework for Django applications",
    long_description=long_description,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development',
        'Topic :: Software Development :: Testing',
    ],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='',
    author='Jeremy Bowman',
    author_email='jbowman@safaribooksonline.com',
    url='https://github.com/safarijv/sbo-selenium',
    include_package_data=True,
    install_requires=install_requires,
)
