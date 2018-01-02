#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import re

from setuptools import setup, find_packages


def requires_from_file(filename):
    requirements = []
    with open(filename, 'r') as requirements_fp:
        for line in requirements_fp.readlines():
            match = re.search('^\s*([a-zA-Z][^#]+?)(\s*#.+)?\n$', line)
            if match:
                requirements.append(match.group(1))
    return requirements

setup(
    name='borgprune',
    version='0.1',

    author='Felix Schwarz',
    author_email='felix.schwarz@oss.schwarz.eu',

    packages=find_packages(),
    namespace_packages = ['schwarz'],
    scripts=[
        'scripts/borgprune',
    ],
)
