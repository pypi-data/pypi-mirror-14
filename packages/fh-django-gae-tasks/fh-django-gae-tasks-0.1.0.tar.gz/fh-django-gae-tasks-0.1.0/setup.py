import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='fh-django-gae-tasks',
    version='0.1.0',
    packages=['gae_tasks'],
    include_package_data=True,
    description="Django GAE tasks improves upon App Engine's Deferred library and is forked from FreshPlanet's project.",  # nopep8
    long_description=README,
    url='https://gitlab.com/futurehaus/django-gae-tasks',
)
