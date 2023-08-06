#!/usr/bin/env python3

from setuptools import setup

setup(
        name='tinycm',
        version='0.1.3',
        packages=['tinycm', 'tinycm.definitions'],
        url='https://github.com/MartijnBraam/TinyCM',
        license='MIT',
        author='Martijn Braam',
        author_email='martijn@brixit.nl',
        description='Tiny Configuration Management tool',
        keywords=["configuration management", "puppet"],
        classifiers=[
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "Development Status :: 4 - Beta",
            "Operating System :: POSIX :: Linux",
            "License :: OSI Approved :: MIT License"
        ],
        entry_points={
            'console_scripts': [
                'tinycm = tinycm.__main__:main'
            ]
        },
        install_requires=[
            'distro',
            'networkx',
            'requests',
            'ruamel.yaml',
            'tabulate',
            'boolexp',
            'pyparsing'
        ]
)
