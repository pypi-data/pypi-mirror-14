import os
from setuptools import setup

import sys

if sys.version_info[0] != 3 or sys.version_info[1] < 3:
    sys.exit('At least Python 3.3 is required for std-domain')

dependencies = [
    # Basic dependencies
    'tldextract',
    'idna',

    # Testing dependencies
    'nose',
    'coverage',
    'coveralls'
]

setup(
    name="std-domain",
    version="0.0.2",
    author="Evan Darwin",
    author_email="evan@relta.net",
    description=("A library for standarized Domain objects"),
    license="proprietary",
    keywords="international domain library",
    url="https://github.com/EvanDarwin/std-domain",
    install_requires=dependencies,
    classifiers=[
        "License :: Other/Proprietary License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Internationalization",
        "Topic :: Software Development :: Libraries",
    ],
)
