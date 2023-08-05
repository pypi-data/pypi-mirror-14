from setuptools import setup, find_packages

with open("VERSION", "r") as vfile:
    __version__ = vfile.readline().rstrip("\n")

setup(
    name="gitsub",
    version=__version__,
    description="Track git repositories updates",
    author="Aufar Gilbran",
    author_email="aufargilbran@gmail.com",
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
