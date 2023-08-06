# Script for setup and make sdist

import os
from setuptools import setup


def read(fname):
    "Return content of the specified file in the same directory."
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()

setup(
    name='noolite',
    version='1.4.0',
    author='Anton Balashov',
    author_email='sicness@darklogic.ru',
    maintainer='Anton Balashov',
    maintainer_email='sicness@darklogic.ru',
    description='Class for NooLite USB stick',
    py_modules=['noolite'],
    install_requires=['pyusb>=1.0.0b2'],
    license="GPLv3",
    platforms='any',
    url='https://github.com/Sicness/pyNooLite',
    keywords=["noolite", "USB", "smarthome", "PC118", "PC116", "PC1132"],
    long_description=read("README.txt"),
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Manufacturing",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Home Automation",
        "Topic :: System :: Hardware"
        ]
    )
