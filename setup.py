"""Installs the package"""

from setuptools import find_packages, setup

setup(
    name="akshara",
    version="0.0.5",
    author="Arindam Saha",
    author_email="arindamsaha1507@gmail.com",
    url="https://github.com/arindamsaha1507/akshara",
    description="A project to help spelling in Sanskrit",
    long_description_content_type="text/markdown",
    long_description="A project to help spelling in Sanskrit",
    license="GNU GENERAL PUBLIC LICENSE",
    packages=find_packages(exclude=["test"]),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
    ],
)
