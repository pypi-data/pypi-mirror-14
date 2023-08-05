from setuptools import setup
from os import path

setup(name="SkPy",
      description="An unofficial Python library for interacting with the Skype HTTP API.",
      long_description=open(path.join(path.abspath(path.dirname(__file__)), "README.rst"), "r").read(),
      author="Ollie Terrance",
      version="0.1",
      packages=["skpy"],
      install_requires=["beautifulsoup4", "requests"],
      url="https://github.com/OllieTerrance/SkPy",
      download_url="https://github.com/OllieTerrance/SkPy/releases",
      classifiers=["Development Status :: 3 - Alpha",
                   "Intended Audience :: Developers",
                   "Topic :: Communications :: Chat",
                   "Topic :: Software Development :: Libraries"])
