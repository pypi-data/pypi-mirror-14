#!/user/bin/env python

from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name='requests-aeaweb',
    version='0.0.1',
    description='Requests wrapper to log onto AEAweb.org.',
    long_description=readme(),
    author='Erin Hengel',
    url='http://www.erinhengel.com/software/requests-aeaweb/',
    packages = ['requests_aeaweb'],
    install_requires=['requests>=2.9.1', 'beautifulsoup4>=4.4.1'],
    package_data={'': ['README.rst', 'LICENSE']},
    include_package_data=True,
    author_email='erin.hengel@gmail.com',
    license='Apache 2.0',
    zip_safe=False,
)
