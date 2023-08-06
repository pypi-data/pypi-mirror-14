#!/usr/bin/env python
from codecs import open

from setuptools import find_packages, setup


with open('README.rst', 'r', 'utf-8') as f:
    readme = f.read()


setup(
    name='django-glitter-news',
    version='0.1.1',
    description='Django Glitter News for Django',
    long_description=readme,
    url='https://github.com/blancltd/django-glitter-news',
    maintainer='Blanc Ltd',
    maintainer_email='studio@blanc.ltd.uk',
    platforms=['any'],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'django-glitter',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    license='BSD',
)
