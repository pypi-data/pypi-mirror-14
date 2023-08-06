from setuptools import setup, find_packages
from codecs import open
from os import path

__version__ = '0.1.0'

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='wordpad',
    version=__version__,
    description='Adds padding to the right or left of a given string',
    long_description=long_description,
    url='https://github.com/scisco/wordpad',
    download_url='https://github.com/scisco/wordpad/tarball/' + __version__,
    license='CC0',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: Freeware',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='',
    packages=find_packages(exclude=['docs', 'tests*']),
    include_package_data=True,
    author='Alireza J (scisco)',
    author_email='scisco7@gmail.com',
    test_suite='tests',
)
