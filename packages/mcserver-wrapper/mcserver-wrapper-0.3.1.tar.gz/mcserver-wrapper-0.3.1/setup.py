#!/usr/bin/env python3
from setuptools import setup, find_packages
from os import path
import pypandoc

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
long_description = pypandoc.convert(long_description, 'rst', format='md')


setup(
    name='mcserver-wrapper',
    version='0.3.1',
    description="Minecraft server wrapper",
    long_description=long_description,
    url="https://github.com/Cynerd/mcserver-wrapper",
    author="Cynerd",
    author_email="cynerd@email.cz",
    license="GPLv2",
    install_requires=['pypandoc'],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        ],
    keywords='Minecraft wrapper server',

    packages=['mcwrapper'],
    entry_points={
        'console_scripts': [
            'mcwrapper=mcwrapper:main'
            ]
        }
    )
