#!/usr/bin/env python

from setuptools import setup, find_packages

with open('requirements.txt') as f:
        requirements = f.read().splitlines()

with open('README.rst') as f:
        long_description = f.read().decode('utf-8')

version = '0.0.1'

setup(
    name='resumeos',
    packages=find_packages(),
    version=version,
    install_requires=requirements,
    author='Matti Jokitulppo',
    author_email='melonmanchan@gmail.com',
    include_package_data=True,
    url='https://github.com/melonmanchan/ResumeOS',
    license='MIT',
    description='Easily bootstrap an OS project to fool HR departments and pad your resume.',
    long_description=long_description,
    entry_points={
        'console_scripts': [
            'resumeos = resumeos.resumeos:main'
        ]
    },
    keywords = ['OS', 'resume', 'filler', 'lazy']
)

