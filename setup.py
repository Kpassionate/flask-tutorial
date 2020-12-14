#!/user/bin/python
# _*_ coding:utf-8 _*_
__author__ = "super.gyk"

from setuptools import find_packages, setup

setup(
    name='flaskr',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)
