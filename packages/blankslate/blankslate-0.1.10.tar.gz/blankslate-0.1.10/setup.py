from setuptools import setup, find_packages, Command
from setuptools.command.test import test
from setuptools.command.install import install

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
                             '-m',
                             'unittest',
                             'discover']))

import blankslate

install_requires = ['procboy','click',]
setup(
    name = "blankslate",
    version = blankslate.version,
    description = "Blank Slate - A foundation for complex projects",
    url = "http://github.com/futurice/blankslate",
    author = "Jussi Vaihia",
    author_email = "jussi.vaihia@futurice.com",
    packages = ["blankslate"],
    include_package_data = True,
    keywords = 'blankslate blank slate',
    license = 'BSD',
    install_requires = install_requires,
    entry_points={
        'console_scripts': [
            'slate = blankslate.cli:main',
        ],
    },
    cmdclass = {
        'test': TestCommand,
    },
)
