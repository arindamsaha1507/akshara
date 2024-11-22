"""Installs the package"""

from pathlib import Path

from setuptools import find_packages, setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="akshara",
    version="1.1.0",
    author="Arindam Saha",
    author_email="arindamsaha1507@gmail.com",
    url="https://github.com/arindamsaha1507/akshara",
    description="A project to help spelling in Sanskrit (Devanaagari)",
    long_description_content_type="text/markdown",
    long_description=long_description,
    license="GNU GENERAL PUBLIC LICENSE",
    packages=find_packages(exclude=["test"]),
    install_requires=["pyyaml"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Linguistic",
    ],
    include_package_data=True,
)
