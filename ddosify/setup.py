#!/usr/bin/env python3
"""
DDoSify Setup Script
For PyPI distribution and installation
"""

from setuptools import setup, find_packages
import os

# Read README for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="ddosify",
    version="1.0.0",
    author="Security Research",
    author_email="security@research.local",
    description="Kali Linux Network Stress Testing Tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ddosify",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology",
        "Topic :: Security",
        "Topic :: System :: Networking",
        "Topic :: System :: Systems Administration",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Environment :: Console",
        "Environment :: X11 Applications :: Qt",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "gui": ["tkinter"],
        "kali": [],
        "dev": ["pytest", "pytest-cov", "flake8", "black"],
    },
    entry_points={
        "console_scripts": [
            "ddosify=ddosify:main",
            "ddosify-gui=ddosify_gui:main",
        ],
    },
    include_package_data=True,
    package_data={
        "ddosify": ["README.md", "LICENSE", "CHANGELOG.md", "install_kali.sh"],
    },
    keywords="ddos stress testing security pentesting kali linux education",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/ddosify/issues",
        "Source": "https://github.com/yourusername/ddosify",
        "Documentation": "https://github.com/yourusername/ddosify/blob/main/README.md",
    },
)
