"""
Copyright 2013 Štěpán Bahník

This file is part of Carousel Maze Manager.

Carousel Maze Manager is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Carousel Maze Manager is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Carousel Maze Manager.  If not, see <http://www.gnu.org/licenses/>.
"""

from collections import namedtuple, OrderedDict


from cm import CM
from mwm import MWM
from of import OF
from cmsf import CMSF
from parameters import ParametersCM, ParametersMWM, ParametersOF, ParametersCMSF


mode = None
CL = None
files = None
fs = {}
slaves = {}
name = ""
parameters = None


Task = namedtuple("Task", ["constructor", "files", "parameters"])
Slaves = namedtuple("Slaves", ["processor", "explorer", "controller"])

dispatch = {"CM": Task(CM, "pair", ParametersCM()),
            "MWM": Task(MWM, "one", ParametersMWM()),
            "OF": Task(OF, "one", ParametersOF()),
            "CMSF": Task(CMSF, "one", ParametersCMSF())}

fullname = OrderedDict()
fullname["CM"] = "Carousel maze"
fullname["CMSF"] = "Carousel maze (single frame)"
fullname["MWM"] = "Morris watter maze"
fullname["OF"] = "Open field"


time = {"CM": 20,
        "MWM": 1,
        "OF": 10,
        "CMSF": 20}


def changeMode(newMode):
    global mode, CL, files, name, parameters
    mode = newMode
    CL = dispatch[mode].constructor
    files = dispatch[mode].files
    name = fullname[mode]
    parameters = dispatch[mode].parameters


    
