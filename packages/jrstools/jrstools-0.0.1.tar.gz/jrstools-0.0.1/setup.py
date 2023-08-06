#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup
from jrstools import __version__

setup(
    name="jrstools",
    version=__version__,
    url="http://pythonhosted.org/jrs#jrstools",
    description="json: [rpc, schema] tools",
    license='MIT',
    author="Stepan Perlov",
    author_email="stepanperlov@gmail.com",
    install_requires=["PyYAML", "jinja2"],
    packages=["jrstools"],
    package_data={'jrstools': ['templates/*.j2']},
    platforms=["linux"]
)
