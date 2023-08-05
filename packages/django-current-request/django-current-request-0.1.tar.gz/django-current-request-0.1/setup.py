#!/usr/bin/env python
from setuptools import setup, find_packages, Command
from setuptools.command.test import test

import os, sys, subprocess

class TestCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        raise SystemExit(
            subprocess.call([sys.executable,
                             'app_test_runner.py',
                             'test']))

install_requires = ['']

setup(
    name = "django-current-request",
    version = "0.1",
    description = "For that time when you need the request",
    url = "http://github.com/futurice/django-current-request",
    author = "Jussi Vaihia",
    author_email = "jussi.vaihia@futurice.com",
    packages = ["djangocurrentrequest"],
    include_package_data = True,
    keywords = 'django current request',
    license = 'BSD',
    install_requires = install_requires,
    cmdclass = {
        'test': TestCommand,
    },
)
