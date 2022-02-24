#!/usr/bin/env python

from distutils.core import setup

setup(
    name="fry-bot",
    version="1.0",
    description="Pindropt Bot",
    author="Chris Moultrie",
    author_email="821688+tebriel@users.noreply.github.com",
    url="https://github.com/tebriel/fry-bot/",
    packages=["bot"],
    install_requires=[
        "hikari",
        "azure-storage-blob",
        "azure-data-tables",
        "azure-identity",
        "azure-keyvault-secrets",
        "azure-search-documents",
        "azure-core",
    ],
)
