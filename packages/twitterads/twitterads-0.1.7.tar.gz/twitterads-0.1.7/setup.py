import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# Don't import analytics-python module here, since deps may not be installed
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'twitterads'))

long_description = '''
twitterads is a python  client that wraps the Twitter ADS API.
'''

setup(
    name='twitterads',
    version= '0.1.7',
    url='https://github.com/asamat/python_twitter_ads',
    author='Arunim Samat',
    author_email='arunimsamat@gmail.com',
    packages=['twitterads', 'twitterads.helper'],
    license='MIT License',
    install_requires=[
        'requests',
    ],
    description='Wrapper to Twitter Ads Rest API.',
    long_description=long_description
)
