import re
import ast
from setuptools import setup


_version_re = re.compile(r"__version__\s+=\s+(.*)")


with open("click_didyoumean/__init__.py", "rb") as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode("utf-8")).group(1)))


setup(
    name="click-didyoumean",
    author="Timo Furrer",
    author_email="tuxtimo@gmail.com",
    version=version,
    url="https://github.com/timofurrer/click-didyoumean",
    packages=["click_didyoumean"],
    install_requires=["click"],
    description="Enable git-like did-you-mean feature in click.",
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
)
