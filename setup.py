# -*- encoding: utf-8 -*-
# flake8: noqa
# pylint: skip-file
"""
Python setup file for the freckle_client app.

In order to register your app at pypi.python.org, create an account at
pypi.python.org and login, then register your new app like so:

    python setup.py register

If your name is still free, you can now make your first release but first you
should check if you are uploading the correct files:

    python setup.py sdist

Inspect the output thoroughly. There shouldn't be any temp files and if your
app includes staticfiles or templates, make sure that they appear in the list.
If something is wrong, you need to edit MANIFEST.in and run the command again.

If all looks good, you can make your first release:

    python setup.py sdist upload

For new releases, you need to bump the version number in
freckle_client/__init__.py and re-run the above command.

For more information on creating source distributions, see
http://docs.python.org/2/distutils/sourcedist.html

"""
import os

from setuptools import find_packages, setup

import noko_client as app

dev_requires = [
    "black",
    "flake8",
    "isort",
    "mypy",
    "pylint",
]

install_requires = ["requests", "pydantic", "python-dateutil"]


def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ""


setup(
    name="python-freckle-client",
    version=app.__version__,
    description="A super simple Freckle/Noko API client implementation.",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    license="The MIT License",
    platforms=["OS Independent"],
    keywords="nokotime, noko, api, client, freckle",
    author="OmbuLabs - The Lean Software Boutique, LLC",
    author_email="hello@ombulabs.com",
    url="https://github.com/ombulabs/python-freckle-client",
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    extras_require={
        "dev": dev_requires,
    },
)
