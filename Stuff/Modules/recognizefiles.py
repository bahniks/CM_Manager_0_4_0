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

from collections import deque
import os


import mode as m


def recognizeFiles(filenames):
    """from list of filenames provided by parameter recognizes matching files and returns two lists
    - first containing names of non-matching files and second containing list of arenafiles with
    matching room files counterparts
    matching files are those for which other file with the same name except from 'room' 'Arena'
    etc. exists in the same directory"""
    filenames.sort()
    if m.files == "one":
        return [], [os.path.normpath(file) for file in filenames]
    filenames = deque(os.path.normpath(file) for file in filenames)
    arenaFiles = []
    nonmatchingFiles = []
    while filenames:
        first = filenames.popleft()
        name = os.path.basename(first)
        splitName = os.path.split(first)
        if "Arena" in name or "arena" in name:
            base = splitName[1].replace("Arena", "Room").replace("arena", "room")
            roomName = os.path.join(splitName[0], base)
            if roomName in filenames:
                arenaFiles.append(first)             
                filenames.remove(roomName)
            elif os.path.exists(roomName):
                arenaFiles.append(first)  
            else:
                nonmatchingFiles.append(first)
        elif "Room" in name or "room" in name:
            base = splitName[1].replace("Room", "Arena").replace("room", "arena")
            arenaName = os.path.join(splitName[0], base)
            if arenaName in filenames:
                arenaFiles.append(arenaName)
                filenames.remove(arenaName)
            elif os.path.exists(arenaName):
                arenaFiles.append(arenaName)
            else:
                nonmatchingFiles.append(first)                      
        else:
            nonmatchingFiles.append(first)
    return nonmatchingFiles, arenaFiles
