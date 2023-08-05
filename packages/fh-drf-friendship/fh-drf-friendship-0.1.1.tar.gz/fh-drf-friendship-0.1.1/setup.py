import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='fh-drf-friendship',
    version='0.1.1',
    packages=['rest_framework_friendship'],
    include_package_data=True,
    description='A library to provide ViewSets for django-friendship to use with Django Rest Framework projects.',
    long_description=README,
    url='http://www.futurehaus.com/',
    install_requires=['django==1.8', 'drf-extensions', 'rest_condition', 'django-friendship', 'fh-drf-common'],
)
