"""
Package Setup Configurations.
"""

import os
from setuptools import find_packages, setup

import coinbaseadvanced

root = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(root, "requirements.txt"), "r", encoding="utf-8") as fh:
    requirements = fh.readlines()

with open("README.md", "r", encoding="utf-8") as fh:
    readme = fh.read()

setup(
    name='coinbaseadvanced',
    version=coinbaseadvanced.__version__,
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    license='MIT',
    description='Coinbase Advanced Trade API client library.',
    long_description=readme,
    long_description_content_type="text/markdown",
    url='https://github.com/KmiQ/coinbase-advanced-python/',
    download_url=f"https://github.com/KmiQ/coinbase-advanced-python/archive/refs/tags/{coinbaseadvanced.__version__}.tar.gz",
    author='Camilo Quintas',
    author_email='kmiloc89@gmail.com',
    keywords=['api', 'coinbase', 'bitcoin', 'client', 'crypto'],
    install_requires=[req for req in requirements],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
)
