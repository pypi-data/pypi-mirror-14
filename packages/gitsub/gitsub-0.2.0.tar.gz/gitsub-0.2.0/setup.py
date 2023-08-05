from setuptools import setup, find_packages
import pypandoc

with open("VERSION", "r") as vfile:
    __version__ = vfile.readline().rstrip("\n")

long_description = pypandoc.convert('README.md','rst')

setup(
    name="gitsub",
    version=__version__,
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
    entry_points={
        "console_scripts": [
            "gitsub = gitsub.main:main",
        ]
    }

)
