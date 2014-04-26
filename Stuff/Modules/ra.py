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

from collections import OrderedDict
from math import sqrt

import os


from cm import CM


class RA(CM):
    cache = OrderedDict()

    def __init__(self, nameA, nameR = "auto"):
        "class RA represents data from robot avoidance; nameA - rat file; nameR - robot file"
        self.nameA = nameA
        self.data = []
        self.interpolated = set()
        self.indices = slice(7,9)

        # automatic room frame filename creation
        self._setRoomName(nameR)
        
        # in cache?
        if (self.nameA, self.nameR) in RA.cache:
            self.__dict__ = RA.cache[(self.nameA, self.nameR)]
            return
    
        # processing data from robot frame    
        with open(self.nameR, "r") as infile:
            self._processHeader(infile)
            self.radius = self.trackerResolution * self.arenaDiameter * 100 / 2
            self._processRoomFile(infile) # robot file generally internally corresponds to roomfile

        # processing data from rat file
        with open(self.nameA, "r") as infile:
            self._processArenaFile(infile) # rat file generally internally corresponds to arenafile

        self.centerX = self.centerY = self.radius

        # discards missing points from beginning of self.data
        self._correctMissingFromBeginning()
          
        # exception used for example when all lines are wrong (all positions are 0, 0)
        if not self.data:
            raise Exception("Failure in data initialization.")

        # caching
        RA.cache[(self.nameA, self.nameR)] = self.__dict__
        if len(RA.cache) > 10:
            CM.cache.popitem(last = False)


    def _setRoomName(self, name): # ZMENIT rob na robot???
        if name == "auto":
            splitname = os.path.split(self.nameA)
            if splitname[1].count("Rat") > 0:
                self.nameR = os.path.join(splitname[0], splitname[1].replace("Rat", "Rob"))
            elif splitname[1].count("rat") > 0:
                self.nameR = os.path.join(splitname[0], splitname[1].replace("rat", "rob"))
            else:
                raise IOError
        else:
            self.nameR = name


    def _evaluateLine(self, line, endsplit):
        temp = line.split()[:endsplit]
        if temp[2] != "0" or temp[3] != "0":
            temp[2] = float(temp[2]) - self.centerX + self.radius
            temp[3] = float(temp[3]) - self.centerY + self.radius
        else:
            temp[2:4] = [0, 0]
        return list(map(int, temp))


    def _addReinforcedSector(self, string, position):
        self.sectorRadius = eval(string[position+1])   
         
   
    def _cacheRemoval(self):
        if (self.nameA, self.nameR) in RA.cache:
            RA.cache.pop((self.nameA, self.nameR))   


    def _returnSame(self, missing):
        toDeleteRat = self._findSame(slice(7,9), missing)
        addMissing = {row[0] - 1 for row in self.data if tuple(row[7:9]) in toDeleteRat}
        return addMissing


    def removeReflections(self, points = None, deleteSame = True, bothframes = True):
        if points == None:
            ps = self.findReflections(time = "max", startTime = 0, results = "indices")
            ps = ps[0] + ps[1]
            ps += [line[0] for line in self.data if
                   sqrt((line[2] - line[7])**2 + (line[3] - line[8])**2) < 8]
        else:
            ps = points
        super().removeReflections(points = ps, deleteSame = deleteSame, bothframes = True)


    def _removalCondition(self, row, i, before, reflection):
        """conditions in order of appearance:
            large speed between the row and before row
            same position as in the reflection row
            we should expect the position to be closer to before row than to the
            reflection row - determined by speed
            wrong points in the row
        """
        old = self.data[row]
        new = self.data[row + i]
        return any((self._computeSpeed(new, before) > 250,
                    new[7:9] == old[7:9],
                    self._computeSpeed(reflection, new) * 30 < self._computeSpeed(before, new),
                    row + i in self.interpolated))


