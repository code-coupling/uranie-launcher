# -*- coding: utf-8 -*-

"""Installation script of the package."""

import pathlib
from setuptools import find_packages, setup


here = pathlib.Path(__file__).parent.resolve()


def get_version():
    """Extract the package's version number from the ``VERSION`` file."""
    return (here / "src" / "uranie_launcher" / "VERSION").read_text(encoding="utf-8").strip()


def get_long_description():
    """Extract README content"""
    return (here / "README.md").read_text(encoding="utf-8")


setup(
    name="uranie-launcher",
    version=get_version(),
    author="Clément STUTZ",
    author_email="clement.stutz@cea.fr",
    description="uranie-launcher help you to run your calculation scripts with Uranie",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    entry_points={
        'console_scripts': [
            'uranie-launcher-unitary=uranie_launcher._run_unitary:run_unitary',
            'test-run-unitary-calculation=tests.program_tester:run_unitary_calculation',
        ]},
    install_requires=[
                    #   "URANIE",
                    #   "ROOT"
                      ],
    extras_require={
            'dev' : ["pytest"]
        },
    package_data={
        "uranie_launcher": [
            "VERSION",
        ],
    },
    project_urls={  # Optional
        "Bug Reports": "https://github.com/clementstutz/uranie-launcher/issues",
        "Source": "https://github.com/clementstutz/uranie-launcher",
    },
    )
