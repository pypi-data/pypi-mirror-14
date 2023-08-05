# coding=utf-8

from os import path
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

VERSION = '0.0.4'

BASE_DIR = path.abspath(path.dirname(__file__))

packages = [
    'metacrawler',
    'metacrawler/template',
    'metacrawler/template/elements'
]

requires = [
    'configobj',
    'lxml',
    'requests',
]

with open(path.join(BASE_DIR, 'README.rst')) as f:
    long_description = f.read()

setup(
    name='metacrawler',
    version=VERSION,
    packages=packages,
    install_requires=requires,
    include_package_data=True,
    package_data={
        'metacrawler/template': ['*.config'],
    },
    description='Create your own crawler.',
    long_description=long_description,
    author='Vitalii Maslov',
    author_email='me@pyvim.com',
    url='https://github.com/pyvim/metacrawler',
    download_url='https://github.com/pyvim/metacrawler/tarball/master',
    license='MIT',
    keywords='parser,crawler',
    entry_points={
        'console_scripts': ['metacrawler = metacrawler.commands:execute']
    },
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
)
