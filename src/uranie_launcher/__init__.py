# -*- coding: utf-8 -*-

"""
This module allow you to use URANIE to run uncertainty propagation
with your own calculation scripts.
"""
import os

import ROOT

__author__ = "Clement STUTZ"
__contact__ = "clement.stutz@cea.fr"
__copyright__ = "Copyright 2023, CEA"
__status__ = "Prototype"

with open(os.path.join(os.path.dirname(__file__), "VERSION"), encoding='utf-8') as file:
    __version__ = file.read().strip()


def _rootlogon():
    """Setup done in rootlogon.py recommanded by """
    # pylint: disable=no-member,invalid-name
    # General graphical style
    WHITE = 0

    # PlotStyle
    ROOT.gStyle.SetPalette(1)
    ROOT.gStyle.SetOptDate(21)

    # Legend
    ROOT.gStyle.SetLegendBorderSize(0)
    ROOT.gStyle.SetFillStyle(0)

    # Pads
    ROOT.gStyle.SetPadColor(WHITE)
    ROOT.gStyle.SetTitleFillColor(WHITE)
    ROOT.gStyle.SetStatColor(WHITE)

    ROOT.PyConfig.IgnoreCommandLineOptions = False
    ROOT.gROOT.SetBatch(True)


_rootlogon()
