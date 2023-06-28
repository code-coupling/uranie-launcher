# pylint: disable=unused-import, no-member, no-name-in-module, import-error
""" Script to use ROOT library in uranie_launcher.
"""
import ROOT

#Create shortcuts if uranie exists
urasys = ROOT.TString( ROOT.gSystem.Getenv("URANIESYS"))
if not urasys.EqualTo("") :
    from ROOT.URANIE import DataServer
    from ROOT.URANIE import Sampler
    from ROOT.URANIE import Launcher
    from ROOT.URANIE import Relauncher
    from ROOT.URANIE import Reoptimizer
    from ROOT.URANIE import Sensitivity
    from ROOT.URANIE import Optimizer
    from ROOT.URANIE import Modeler
    from ROOT.URANIE import UncertModeler
    from ROOT.URANIE import Reliability
    from ROOT.URANIE import MpiRelauncher

##General graphical style
WHITE = 0

##PlotStyle
ROOT.gStyle.SetPalette(1)
ROOT.gStyle.SetOptDate(21)

##Legend
ROOT.gStyle.SetLegendBorderSize(0)
ROOT.gStyle.SetFillStyle(0)

## Pads
ROOT.gStyle.SetPadColor(WHITE)
ROOT.gStyle.SetTitleFillColor(WHITE)
ROOT.gStyle.SetStatColor(WHITE)

ROOT.PyConfig.IgnoreCommandLineOptions = False
ROOT.gROOT.SetBatch(True)
##  ====================  Hint ====================
##
##    Might be practical to store this in a convenient place (for instance
##    the ".python" folder in your home directory) or any other place where
##    your $PYTHONPATH is pointing.
##
##    example : export PYTHONPATH=$PYTHONPATH:${HOME}/.mypython/
##
##    It should then be called as "from rootlogon import *"
##    This would replace the shortcuts created and import done in the rest of the scripts
##
##    Many style issue can be set once and for all here.
##    toto=DataServer.TDataServer()
##
