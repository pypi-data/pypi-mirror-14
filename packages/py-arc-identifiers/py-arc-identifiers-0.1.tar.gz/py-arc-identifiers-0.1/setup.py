from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='py-arc-identifiers',
    version='0.1',
    description='generate Arc UUIDs in python',
    long_description=long_description,
    url='https://github.com/MPMedia/py-arc-identifiers',
    download_url='https://github.com/WPMedia/py-arc-identifiers/tarball/0.2.4',
    author='patharer',
    author_email='rohan.pathare@washpost.com',
    license='MIT',
    packages=['ArcUUID', 'test'],
)