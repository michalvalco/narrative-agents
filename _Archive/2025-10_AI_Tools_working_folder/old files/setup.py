"""
Setup configuration for Narrative Agents package.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="narrative-agents",
    version="0.1.0",
    author="Michal Valčo",
    author_email="michal.valco@fpt.ku.sk",
    description="When Philosophy Drives Architecture: Narrative Identity Theory as Agent Memory",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/michaljesse/narrative-agents",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "colorama>=0.4.6",
        "tabulate>=0.9.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "mypy>=1.0.0",
            "flake8>=5.0.0",
        ],
        "docs": [
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.0.0",
        ],
    },
    keywords="ai agents philosophy narrative identity memory ricoeur aristotle",
    project_urls={
        "Bug Reports": "https://github.com/michaljesse/narrative-agents/issues",
        "Source": "https://github.com/michaljesse/narrative-agents",
        "LinkedIn": "https://linkedin.com/in/michalvalco",
    },
)
