import sys
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name="TensegrityPY",
    version="0.1",
    description="Tensegrity robot framework",
    long_description=long_description,
    url="https://github.com/RumblingTurtle/TensegrityPY",
    author="Eduard Zalyaev",
    author_email="e.zalyaev@innopolis.ru",
    packages=find_packages("src"),
    package_dir={"": "src"},

    install_requires=[
      "numpy"
    ]
)
