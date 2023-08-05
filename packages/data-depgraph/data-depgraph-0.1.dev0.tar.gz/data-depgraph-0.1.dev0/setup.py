from setuptools import setup, find_packages

with open("README.rst", "r") as f:
    readme = f.read()

setup(
    name = "data-depgraph",
    version = "0.1dev",
    packages = find_packages(),

    author = "Nat Wilson",
    author_email = "njwilson23@gmail.com",
    description = "Small dependency resolution library for scientific datasets",
    long_description = readme,
    license = "MIT License",
    classifiers = ["Programming Language :: Python :: 2",
                   "Programming Language :: Python :: 2.7",
                   "Programming Language :: Python :: 3",
                   "Programming Language :: Python :: 3.4",
                   "Programming Language :: Python :: 3.5",
                   "License :: OSI Approved :: MIT License"],
)
