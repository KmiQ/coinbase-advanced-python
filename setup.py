"""
Package Setup Configurations.
"""

from setuptools import setup
import coinbaseadvanced

requirements = [
    'requests>=2.28.1',
    'requests-toolbelt>=0.10.1',
    'typed-ast>=1.5.4',
    'typing-extensions>=4.4.0',
]

with open("README.md", "r", encoding="utf-8") as fh:
    readme = fh.read()

setup(
    name='coinbaseadvanced',
    version=coinbaseadvanced.__version__,
    packages=['coinbaseadvanced', 'coinbaseadvanced.models'],
    include_package_data=True,
    license='MIT',
    description='Coinbase Advanced Trade API client library.',
    long_description=readme,
    long_description_content_type="text/markdown",
    url='https://github.com/KmiQ/coinbase-advanced-python/',
    download_url=f"https://github.com/KmiQ/coinbase-advanced-python/archive/refs/tags/{coinbaseadvanced.__version__}.tar.gz",
    author='Camilo Quintas',
    author_email='kmiloc89@gmail.com',
    keywords=['api', 'coinbase', 'bitcoin', 'client'],
    install_requires=requirements,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
)
