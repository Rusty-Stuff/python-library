import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = "0.0.1"
PACKAGE_NAME = "rusty-forms"
AUTHOR = "Franz Geffke"
AUTHOR_EMAIL = "m@f-a.nz"
URL = "https://github.com/Rusty-Stuff/python-library"

DESCRIPTION = "Python library that makes working with Rusty Forms a breeze"
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = ["requests", "nostr"]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    install_requires=INSTALL_REQUIRES,
    packages=find_packages(),
    zip_safe=False,
)
