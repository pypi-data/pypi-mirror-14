#!/usr/bin/env python
from distutils.core import setup


VERSION = '0.1.3'

setup(
    name="nose-switch",
    packages=['nose_switch'],
    version=VERSION,
    author="Bogdan Popa",
    author_email="bogdititupopa@gmail.com",
    license="GNU GPL",
    description="Add special switches in code, based on options set when running tests.",
    url="https://github.com/popas90/nose-switch",
    download_url="https://github.com/popas90/nose-switch/tarball/0.1.0",
    classifiers=[],
    py_modules=['nose_switch'],
    entry_points={'nose.plugins': ['nose_switch = nose_switch:NoseSwitch']},
    install_requires=['nose'],
    test_suite='tests',
)
