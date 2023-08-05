#!/usr/bin/python3


import setuptools

setuptools.setup(
    name = "trackdeps",
    version = "1.0.2",
    url = "http://trackdeps.pietroalbini.io",

    license = 'MIT',

    author = "Pietro Albini",
    author_email = "pietro@pietroalbini.io",

    install_requires = [
        'packaging',
        'requests',
        'setuptools',
        'jinja2',
        'pyyaml',
        'click',
        'csscompressor',
        'django-htmlmin',
    ],

    packages = [
        'trackdeps',
    ],

    entry_points = {
        "console_scripts": [
            "trackdeps-report = trackdeps.__main__:cli",
        ],
    },

    zip_safe = False,
    include_package_data = True,

    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries",
        "Topic :: System :: Systems Administration",
        "Topic :: System :: Software Distribution",
    ],
)
