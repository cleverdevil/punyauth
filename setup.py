# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='punyauth',
    version='0.1',
    description='',
    author='',
    author_email='',
    install_requires=[
        "pecan",
    ],
    test_suite='punyauth',
    zip_safe=False,
    include_package_data=True,
    packages=find_packages(exclude=['ez_setup']),
    entry_points="""
    [pecan.command]
    hashpass=punyauth.cmds:GeneratePasswordHash
    """
)
