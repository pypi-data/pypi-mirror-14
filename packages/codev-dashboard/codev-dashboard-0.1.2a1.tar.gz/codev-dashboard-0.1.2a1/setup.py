# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

NAME = "codev-dashboard"
DESCRIPTION = "codev dashboard"
AUTHOR = "Jan Češpivo"
AUTHOR_EMAIL = "jan.cespivo@gmail.com"
URL = ""
VERSION = '0.1.2a1'


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="Apache 2.0",
    url=URL,
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
    install_requires=[
        "flask", "flask-sqlalchemy"
    ],
)
