# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from os import path

version_file = path.join(path.dirname(__file__), 'VERSION')
version = open(version_file).read().strip()

setup(
    name='invoice2data',
    version=version,
    author='Manuel Riel',
    author_email='github@snapdragon.cc',
    url='https://github.com/manuelRiel/invoice2data',
    description='Python parser to extract data from pdf invoice',
    license="MIT",
    long_description=open(path.join(path.dirname(__file__), 'README.md')).read(),
    package_data = {
        'invoice2data': ['templates/*.yml', 'templates/fr/*.yml'],
        'invoice2data.test': ['pdfs/*.pdf']
        },
    packages=find_packages(),
    install_requires=[
        r.strip() for r in open('requirements.txt').read().splitlines()],
    zip_safe=False,
    entry_points = {
              'console_scripts': [
                  'invoice2data = invoice2data.main:main',                  
              ],              
          },
)
