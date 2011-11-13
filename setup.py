#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os

from distutils.core import setup


__author__ = "Diego Muñoz Escalante"
__license__ = "GPL 3"
__version__ = "0.5.1"
__email__ = "escalant3@gmail.com"
__url__ = "https://github.com/escalant3/pyblueprints"
__description__ = """A Python version of the Blueprints
                    property graph model interface"""
__status__ = "Development"


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(
    name='pyblueprints',
    version=__version__,
    author=__author__,
    author_email=__email__,
    url=__url__,
    description=__description__,
    long_description=read('README.txt') + "\n\n" + read('CHANGES.txt'),
    license=__license__,
    keywords="""property graph model interface graphdb graphdatabase
                database blueprints orientdb neo4j""",
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        ],
    zip_safe=False,
    packages=[
        "pyblueprints",
    ],
    include_package_data=True,
    install_requires=[
        'neo4jrestclient',
        'python-rexster',
    ],
)
