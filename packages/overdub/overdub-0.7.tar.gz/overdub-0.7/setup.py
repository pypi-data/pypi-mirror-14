#!/usr/bin/env python
from setuptools import setup, find_packages
import versioneer

setup(
    name='overdub',
    version=versioneer.get_version(),
    author='Xavier Barbosa',
    author_email='clint.northwood@gmail.com',
    description='layered configuration aggregator',
    packages=find_packages(),
    install_requires=[],
    extras_require={
        'yaml': ['pyyaml']
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    keywords=['configuration', 'layer', 'yaml'],
    url='http://py.errorist.io/overdub',
    license='MIT',
    cmdclass=versioneer.get_cmdclass()
)
