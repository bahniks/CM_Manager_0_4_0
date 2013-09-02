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

from collections import namedtuple


from cm import CM
from mwm import MWM
from openfield import OF


mode = "CM"
CL = CM 
files = "pair"

Task = namedtuple("Task", ["constructor", "files"])

dispatch = {"CM": Task(CM, "pair"),
            "MWM": Task(MWM, "one"),
            "OF": Task(OF, "one")}

def changeMode(newMode):
    global mode, CL, files
    mode = newMode
    CL = dispatch[mode].constructor
    files = dispatch[mode].files
    print("new mode is " + mode)
