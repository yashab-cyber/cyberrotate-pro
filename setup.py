#!/usr/bin/env python3
"""
CyberRotate Pro - Advanced IP Rotation & Anonymity Suite
Created by Yashab Alam - Founder & CEO of ZehraSec
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="cyberrotate-pro",
    version="1.0.0",
    author="Yashab Alam",
    author_email="yashabalam707@gmail.com",
    description="Advanced IP Rotation & Anonymity Suite for Cybersecurity Professionals",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yashab-cyber/cyberrotate-pro",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Information Technology",
        "Topic :: Security",
        "Topic :: System :: Networking",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "full": ["scapy>=2.5.0", "selenium>=4.15.0", "plotly>=5.17.0", "dash>=2.14.2"],
        "dev": ["pytest>=7.4.3", "black>=23.11.0", "flake8>=6.1.0", "mypy>=1.7.1"],
    },
    entry_points={
        "console_scripts": [
            "cyberrotate=ip_rotator:main",
            "cyberrotate-pro=ip_rotator:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.txt", "*.json", "*.md", "*.yaml", "*.yml"],
    },
    keywords="cybersecurity, anonymity, ip-rotation, proxy, vpn, tor, penetration-testing",
    project_urls={
        "Homepage": "https://www.zehrasec.com",
        "Bug Reports": "https://github.com/yashab-cyber/cyberrotate-pro/issues",
        "Source": "https://github.com/yashab-cyber/cyberrotate-pro",
        "Documentation": "https://github.com/yashab-cyber/cyberrotate-pro/docs",
    },
)
