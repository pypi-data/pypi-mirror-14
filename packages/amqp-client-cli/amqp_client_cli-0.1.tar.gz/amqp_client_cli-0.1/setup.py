#! /usr/bin/env python
from setuptools import setup, find_packages
from io import open

setup(
    name='amqp_client_cli',
    packages=find_packages (),
    version='0.1',
    description='A command line interface for interacting with '
                'amqp exchanges',
    author='Dillon Dixon',
    author_email='dillondixon@gmail.com',
    url='https://github.com/ownaginatious/amqp-client-cli',
    download_url='https://github.com/ownaginatious'
                  '/amqp-client-cli/tarball/0.3.1',
    license='MIT',
    keywords=['amqp', 'cli', 'client', 'rabbitmq', 'amq'],
    classifiers=['Environment :: Console'],
    install_requires=[line.strip ()
                      for line in open ("requirements.txt", "r",
                                        encoding="utf-8").readlines ()],
    entry_points={
        "console_scripts": [
            "amqpcli = amqp_client_cli.main:main",
        ],
    },
)
