from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

import sys
import gitsub

class PyTest(TestCommand):
    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

long_description = open('README.rst').read()

version = sys.version_info[:2]
if version < (3, 5):
    print('gitsub requires Python version 3.5 or later')
    sys.exit(1)

tests_require = [
    'pytest',
    'mock'
]

setup(
    name="gitsub",
    version=gitsub.__version__,
    description="Track git repositories updates",
    long_description=long_description,
    author="Aufar Gilbran",
    author_email="aufargilbran@gmail.com",
    url="https://github.com/aufarg/gitsub",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Version Control"
    ],
    packages=find_packages(),
    tests_require=tests_require,
    cmdclass = {'test': PyTest},
    entry_points={
        "console_scripts": [
            "gitsub = gitsub.main:main",
        ]
    }

)
