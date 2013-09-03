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



from cm import CM


class MWM(CM):
    def __init__(self, nameA, *_):

        self.nameA = nameA
        self.data = []
        self.interpolated = set()
        self.indices = slice(2,4)

        # processing data from arena frame
        with open(self.nameA, "r") as infile:
            self._processHeader(infile)
            self.centerAngle = self._angle(self.platformX, self.platformY)
            endsplit = 6 if self.tracker == "Tracker" else 7
            self._processRoomFile(infile, endsplit = endsplit)

        # discards missing points from beginning of self.data
        self._correctMissingFromBeginning()
          
        # exception used for example when all lines are wrong (all positions are 0, 0)
        if not self.data:
            raise Exception("Failure in data initialization.")


    def _addReinforcedSector(self, string, position):
        self.platformX = eval(string[position+1])   
        self.platformY = eval(string[position+2])         
        self.platformRadius = eval(string[position+3])


    def _correctMissingFromBeginning(self):
        beginMiss = 0
        
        for line in self.data:
            if (line[2] == 0 and line[3] == 0):
                beginMiss += 1
            else:
                if beginMiss != 0:
                    self.data = self.data[beginMiss:]
                    for i in range(len(self.data)):
                        self.data[i][0] -= beginMiss
                    self.interpolated = {p - beginMiss for p in self.interpolated}
                break


    def _computeSpeed(self, row1, row2):
        speed = ((row1[2] - row2[2])**2 + (row1[3] - row2[3])**2)**0.5 / \
                ((abs(row2[1] - row1[1]) / 1000) * self.trackerResolution)
        return speed # cm/s

   
    def _removalCondition(self, row, i, before, reflection):
        """conditions in order of appearance:
            large speed between the row and before row
            same position as in the reflection row
            we should expect the position to be closer to before row than to the
            reflection row - determined by speed
            wrong points in the row
        """
        return any((self._computeSpeed(self.data[row + i], before) > 250,
                    self.data[row + i][2:4] == self.data[row][2:4],
                    self._computeSpeed(reflection, self.data[row + i]) * 30 <
                    self._computeSpeed(before, self.data[row + i]),
                    row + i in self.interpolated))


    def _returnSame(self, missing):
        toDeleteRoom = self._findSame(slice(2,4), missing)
        addMissing = {row[0] - 1 for row in self.data if tuple(row[2:4]) in toDeleteRoom}
        return addMissing


    def removeReflections(self, *args, bothframes = False, **kwargs):
        super().removeReflections(*args, bothframes = bothframes, **kwargs)
        
