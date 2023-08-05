# coding: utf-8
from __future__ import absolute_import, division, print_function

__author__ = "Johannes Köster"
__copyright__ = "Copyright 2015, Johannes Köster, Liu lab"
__email__ = "koester@jimmy.harvard.edu"
__license__ = "MIT"


import sys

try:
    from setuptools import setup
except ImportError:
    print("Could not load setuptools. Please install the setuptools package.", file=sys.stderr)


# load version info
exec(open("vispr/version.py").read())


setup(
    name="vispr",
    version=__version__,
    author="Johannes Köster",
    author_email="koester@jimmy.harvard.edu",
    description="Interactive HTML5 visualization for CRISPR/Cas9 knockout screen experiments.",
    license="MIT",
    url="https://bitbucket.org/johanneskoester/vispr",
    packages=["vispr", "vispr.results"],
    include_package_data=True,
    zip_safe=False,
    install_requires=["flask", "numpy", "pandas>=0.17.0", "pyyaml", "scikit-learn", "scipy", "appdirs"],
    entry_points={"console_scripts": ["vispr = vispr.cli:main"]},
    classifiers=[
        "Development Status :: 4 - Beta",
        #"Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2",
        "Topic :: Scientific/Engineering :: Bio-Informatics"
    ]
)
