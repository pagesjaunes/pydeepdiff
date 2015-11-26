#!/usr/bin/env python

"""Setup script for pydeepdiff distributions"""

from setuptools import setup, find_packages
import pydeepdiff


def main():
    setup(
        name='pydeepdiff',
        version=pydeepdiff.__version__,
        description='Computes deep differences between objects',
        long_description=open('README.md').read(),
        author='PagesJaunes',
        author_email='fdepaulis@pagesjaunes.fr',
        url='https://github.com/pagesjaunes/pydeepdiff',
        packages=find_packages(),
        install_requires=[]
    )

if __name__ == "__main__":
    main()
