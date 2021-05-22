import io
from setuptools import (
    setup,
    find_packages,
)  # pylint: disable=no-name-in-module,import-error


def dependencies(file):
    with open(file) as f:
        return f.read().splitlines()


with io.open("README.md", encoding="utf-8") as infile:
    long_description = infile.read()

setup(
    name="hades-cli",
    packages=find_packages(),
    version="0.0.1",
    license="MIT",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
    ],
    python_requires=">=3.4",
    description="A slick CLI tool to monitor coinbase crypto.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Punid Ramesh",
    author_email="punidramesh@gmail.com",
    url="https://github.com/punidramesh/Hades",
    keywords=[
        "wallet",
        "console",
        "coinbase",
        "crypto",
        "cli",
        "terminal",
        "term",
    ],
    install_requires=dependencies("requirements.txt"),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "hades=cli.__main__:main",
        ]
    }
)