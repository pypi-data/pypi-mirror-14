import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-dbase-storage',
    version='0.1',
    packages=['django-dbase-storage'],
    include_package_data=True,
    license='BSD License',
    description='Database storage for Django files',
    long_description=README,
    author='Stan Misiurev',
    author_email='smisiurev@gmail.com',
    install_requires=['django']
)
