#!/usr/bin/env python
__copyright__=''
__license__=''
__version__='2.0.0-1'

try:
  from setuptools import setup
except ImportError:
  from disutils.core import setup

setup(
    name='WintxREST',
    version=__version__,
    description='A Web API for the Wintx library.',
    long_description='The Wintx REST Service provides a web API for a '\
        'Wintx meteorological database instance.',
    author='Seth Cook',
    author_email='sethcook@purdue.edu',
    license=__license__,
    packages=['wintxrest'],
    classifiers=['Development Status :: 5 - Production/Stable',
                 'Environment :: Web Environment',
                 'Intended Audience :: Developers',
                 'Operating System :: Unix',
                 'Programming Language :: Python :: 2.6'],
    install_requires=['wintx >= 2.0.0',
                      'Flask >= 0.9',
                      'Werkzeug >= 0.8.3',
                      'Jinja2 >= 2.7.3',
                      'Flask-Cors >= 2.0.1']
)
