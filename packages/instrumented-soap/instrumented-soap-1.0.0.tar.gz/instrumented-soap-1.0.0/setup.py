#!/usr/bin/env python
import codecs
import os.path
from setuptools import setup
from versiontag import get_version, cache_git_tag


packages = [
    'soap',
]

requires = [
    'Django>=1.8.11',
    'django-statsd-mozilla>=0.3.16',
    'suds-jurko>=0.6',
    'requests>=2.9.1',
    'versiontag>=1.0.0',
]

def fpath(name):
    return os.path.join(os.path.dirname(__file__), name)

def read(fname):
    return codecs.open(fpath(fname), encoding='utf-8').read()

cache_git_tag()

setup(
    name='instrumented-soap',
    description="Wrapper around suds-jurko that adds django_statsd instrumentation and improved proxy support.",
    version=get_version(pypi=True),
    long_description=open('README.rst').read(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Operating System :: Unix',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    author='Craig Weber',
    author_email='crgwbr@gmail.com',
    url='https://gitlab.com/thelabnyc/instrumented-soap',
    license='ISC',
    packages=packages,
    install_requires=requires
)
