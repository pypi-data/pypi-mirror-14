import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
        name='fh-django-assetmanager',
        version='0.2.2',
        packages=['assetmanager'],
        include_package_data=True,
        description='Django asset manager providing search (MySQL) and custom file field to use in models.',  # nopep8
        long_description=README,
        url='https://gitlab.com/futurehaus/django-assetmanager',
)
