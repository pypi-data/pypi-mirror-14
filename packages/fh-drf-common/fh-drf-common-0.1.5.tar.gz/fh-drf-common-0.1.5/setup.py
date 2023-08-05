import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='fh-drf-common',
    version='0.1.5',
    packages=['rest_framework_common'],
    include_package_data=True,
    description='A library to provide common functionality for Django Rest Framework projects.',
    long_description=README,
    url='https://gitlab.com/futurehaus/drf-common',
    install_requires=['base32-crockford', 'six', 'django-enumfield']
)
