#! /usr/bin/python

from distutils.core import setup
import distutils_pytest

setup(
    name = "distutils-pytest",
    version = distutils_pytest.__version__,
    description = distutils_pytest.__doc__.strip(),
    author = "Rolf Krahl",
    author_email = "rolf@rotkraut.de",
    url = "https://github.com/RKrahl/distutils-pytest",
    license = "Apache-2.0",
    py_modules = ["distutils_pytest"],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Build Tools",
    ],
)
