# -*- coding: utf-8 -*-
"""Setuptools."""

from setuptools import setup
import re
import sys

version = ''
with open('flask_hookserver.py') as f:
    version = re.search(r'__version__\s*=\s*\'(.+)\'', f.read()).group(1)

if not version:
    raise RuntimeError('Couldn\'t find version string')

with open('README.rst', 'r') as f:
    readme = f.read()

with open('HISTORY.rst', 'r') as f:
    history = f.read()

requirements = [
    'Flask>=0.9',
    'Werkzeug>=0.7',
    'requests[security]>=2.3.0',
]
if sys.version_info < (3, 3):
    requirements.append('ipaddress>=1.0.3')

setup(
    name='Flask-Hookserver',
    version=version,
    url='https://github.com/nickfrostatx/flask-hookserver',
    author='Nick Frost',
    author_email='nickfrostatx@gmail.com',
    description='Server for GitHub webhooks using Flask',
    long_description=readme + '\n\n' + history,
    license='MIT',
    py_modules=['flask_hookserver'],
    install_requires=requirements,
    keywords=['github', 'webhooks', 'flask'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development',
    ],
)
