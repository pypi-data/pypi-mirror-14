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
    name = "isfilled",
    version = "0.4",
    description = "Filledness for Models and ModelForms",
    url = "http://github.com/futurice/isfilled",
    author = "Jussi Vaihia",
    author_email = "jussi.vaihia@futurice.com",
    packages = ["isfilled"],
    include_package_data = True,
    keywords = 'django form filled condition',
    license = 'BSD',
    install_requires = install_requires,
    cmdclass = {
        'test': TestCommand,
    },
)
