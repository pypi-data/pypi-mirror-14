#!/usr/bin/env python
from setuptools import setup

setup(
    name='facebook-signed-request',
    version='3.0.3',
    maintainer="Tomasz Wysocki",
    maintainer_email="tomasz@wysocki.info",
    install_requires=(
        'django>=1.7.1',
    ),
    packages=[
        'facebook_signed_request',
    ],
)
