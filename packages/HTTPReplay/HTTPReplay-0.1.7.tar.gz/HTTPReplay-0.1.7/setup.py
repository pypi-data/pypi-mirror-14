#!/usr/bin/env python
# Copyright (C) 2015 Jurriaan Bremer <jbr@cuckoo.sh>
# This file is part of HTTPReplay - http://jbremer.org/httpreplay/
# See the file 'LICENSE' for copying permission.

from setuptools import setup

setup(
    name="HTTPReplay",
    version="0.1.7",
    author="Jurriaan Bremer",
    author_email="jbr@cuckoo.sh",
    packages=[
        "httpreplay",
    ],
    scripts=[
        "bin/httpreplay",
    ],
    license="GPLv3",
    description="Properly interpret, decrypt, and replay pcap files",
    install_requires=[
        "dpkt",
        "tlslite-ng",
    ],
)
