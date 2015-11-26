#!/usr/bin/env python

"""Setup script for pydiff distributions"""

from setuptools import setup, find_packages
import pydiff


def main():
    setup(
        name='pydiff',
        version=pydiff.__version__,
        description='Computes deep differences between objects',
        author='PagesJaunes',
        author_email='fdepaulis@pagesjaunes.fr',
        url='https://github.com/pagesjaunes/pydiff',
        packages=find_packages(),
        install_requires=[]
    )

if __name__ == "__main__":
    main()
