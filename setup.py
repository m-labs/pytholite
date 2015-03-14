#!/usr/bin/env python3

import sys
import os
from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))

required_version = (3, 3)
if sys.version_info < required_version:
    raise SystemExit("Pytholite requires python {0} or greater".format(
        ".".join(map(str, required_version))))

setup(
    name="pytholite",
    version="unknown",
    description="Python to gateware compiler",
    author="Sebastien Bourdeauducq",
    author_email="sb@m-labs.hk",
    url="http://m-labs.hk",
    download_url="https://github.com/m-labs/pytholite",
    packages=find_packages(here),
    license="BSD",
    install_requires=["migen"],
    platforms=["Any"],
    keywords="HDL ASIC FPGA hardware design",
    classifiers=[
        "Topic :: Scientific/Engineering :: "
            "Electronic Design Automation (EDA)",
        "Environment :: Console",
        "Development Status :: Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
)
