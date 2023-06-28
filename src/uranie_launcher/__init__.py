# -*- coding: utf-8 -*-

"""
This module allow you to use URANIE to run uncertainty propagation
with your own calculation scripts.
"""

__author__ = "Clement STUTZ"
__contact__ = "clement.stutz@cea.fr"
__copyright__ = "Copyright 2023, CEA"
__status__ = "Prototype"

import os
with open(os.path.join(os.path.dirname(__file__), "VERSION"), encoding = 'utf-8') as file:
    __version__ = file.read().strip()
