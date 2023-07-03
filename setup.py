# -*- coding: utf-8 -*-

"""Installation script of the package."""

import os
from setuptools import find_packages, setup

def get_version():
    """Extract the package's version number from the ``VERSION`` file."""
    filename = os.path.join(os.path.dirname(__file__), "src", "uranie_launcher", "VERSION")
    with open(filename, encoding = 'utf-8') as file:
        return file.read().strip()


setup(
    name = "uranie-launcher",
    version = get_version(),
    author = "Clément STUTZ",
    author_email = "clement.stutz@cea.fr",
    description = "Uranie launcher for your own calculation scripts",
    package_dir = {"": "src"},
    packages = find_packages(where = "src"),
    entry_points = {
        'console_scripts': [
            'uranie-launcher-unitary=uranie_launcher._run_unitary:run_unitary',
        ]},
    install_requires = ["numpy>=1.19.5",
                    #   "URANIE",
                    #   "ROOT"
                      ],
    extras_require = {
            'dev' : ["pytest"]
        },
    package_data={
        "uranie_launcher": [
            "VERSION",
        ],
    },
    )
