# -*- coding: utf-8 -*-
"""Setup file for easy installation"""
import sys
import os
from os.path import join, dirname, split
from setuptools import setup


PY3 = os.environ.get('BUILD_VERSION') == '3' or sys.version_info[0] == 3

version = "0.1.3"

LONG_DESCRIPTION = """
social share is package for share contents on social media networks.
"""


def long_description():
    """Return long description from README.rst if it's present
    because it doesn't get installed."""
    try:
        return open(join(dirname(__file__), 'README.rst')).read()
    except IOError:
        return LONG_DESCRIPTION


def path_tokens(path):
    if not path:
        return []
    head, tail = split(path)
    return path_tokens(head) + [tail]


def get_packages():
    exclude_pacakages = ('__pycache__',)
    packages = []
    for path_info in os.walk('socialshare'):
        tokens = path_tokens(path_info[0])
        if tokens[-1] not in exclude_pacakages:
            packages.append('.'.join(tokens))
    return packages


requirements = ['twython','oauth2','requests','django-sauth']

setup(
    name='socialshare',
    version=version,
    author='Renjith S Raj',
    author_email='renjith.r@tringapps.com',
    description='social share is package for share contents on social media networks.',
    license='MIT',
    keywords='django,social,share',
    url='https://github.com/renjith-tring/socialshare',
    packages=get_packages(),
    long_description=long_description(),
    install_requires=requirements,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Internet',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Environment :: Web Environment',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
    zip_safe=False
)
