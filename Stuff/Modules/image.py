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

from math import radians, cos, sin


import os


from optionget import optionGet
from graphs import getGraphTypes, Graphs, SvgGraph, SpeedGraph, DistanceFromCenterGraph
from graphs import AngleGraph, DistanceFromPlatformGraph, DistanceFromRobotGraph
import mode as m


def svgSave(cm, filename, what, root):
    "saves image for one file"
    directory = optionGet("ImageDirectory", os.getcwd(), "str", True)

##    what = root.saveWhatVar.get()
##    start = int(root.timeFrame.startTimeVar.get())
##    end = int(root.timeFrame.timeVar.get())
##    graph = eval(root.graphTypeVar.get()[:-1] + ', cm, purpose = "svg")')

    if what == "both frames":
        components = ["arena", "room"]
    elif what == "arena frame":
        components = ["arena"]
    elif what == "room frame":
        components = ["room"]
    elif what == "graph":
        components = ["graph"]
    elif what == "all":
        components = ["arena", "room", "graph"]

    svg = SVG(cm, components)    
    svg.save(os.path.join(directory, os.path.splitext(os.path.basename(filename))[0] +
                          "_" + what.replace(" ", "_") + ".svg")) # upravit
        





class SVG():
    "represents .svg file - text of the file is stored in self.content"
    def __init__(self, cm, components):
        self.cm = cm
        self.components = components
        self.scale = 1
        self.main = "Main"
        self.xgap = 10
        self.ygap = 10
        self.xlab = "xlab"
        self.ylab = "ylab"
        self.xticks = True
        self.yticks = True

        self.addComponents()
        self.computeSize()
        self.addIntro()

        for component in self.components:           
            if component in ["xgap", "ygap"]:
                continue
            elif component == "main":
                self.addMain()
            elif component == "arena":
                self.addArena()
            elif component == "room":
                self.addRoom()
            elif component == "graph":
                self.addGraph()
            elif component == "xticks" and "graph" in self.components:
                self.addXticks()
            elif component == "yticks" and "graph" in self.components:
                self.addYticks()
            elif component == "xlab" and "graph" in self.components:
                self.addXlab()
            elif component == "ylab" and "graph" in self.components:
                self.addYlab()
                

    def addComponents(self):
        if self.main:
            self.components.append("main")
        if self.xgap and "room" in self.components and "arena" in self.components:
            self.components.append("xgap")
        if self.ygap and "graph" in self.components and "arena" in self.components:
            self.components.append("ygap")
        if self.xticks and "graph" in self.components:
            self.components.append("xticks")
        if self.yticks and "graph" in self.components:
            self.components.append("yticks")
        if self.xlab and "graph" in self.components:
            self.components.append("xlab")
        if self.ylab and "graph" in self.components:
            self.components.append("ylab")


    def computeSize(self):
        x = [0] * 6
        y = [0] * 7
        sizes = {"main": [(0, 0), (20, 1)],
                 "arena": [(300, 3), (300, 2)],
                 "room": [(300, 5), (300, 2)],
                 "graph": [(600, 5), (120, 4)],
                 "xgap": [(self.xgap, 4), (0, 0)],
                 "ygap": [(0, 0), (self.ygap, 3)],
                 "xticks": [(0, 0), (10, 5)],
                 "yticks": [(10, 2), (0, 0)],
                 "xlab": [(0, 0), (15, 6)],
                 "ylab": [(15, 1), (0, 0)]
                 }
        for component in self.components:
            xs, ys = sizes[component]
            for i in range(1, len(x)):
                if i >= xs[1] and (x[i-1] + xs[0]) < x[i]:
                    x[i] = x[i-1] + xs[0]
            for i in range(1, len(y)):
                if i >= ys[1] and (y[i-1] + ys[0]) < y[i]:
                    y[i] = y[i-1] + ys[0]
        self.x = x
        self.y = y


    def addIntro(self):
        t1 = '<svg viewbox = "0 0 {} {}" xmlns="http://www.w3.org/2000/svg">\n'
        self.content = t1.format(self.x[-1] * self.scale, self.y[-1] * self.scale)
        self.content += '<g transform="scale({0},{0})">\n'.format(self.scale)
        self.content += '<rect style="stroke:white;fill:none" x="0" y="0" ' + \
                        'width="{}" height="{}" />\n'.format(self.x[-1], self.y[-1])

    def add(self, new, x, y):
        self.content += '<g transform="translate({0},{0})">\n'.format(self.x[x], self.y[y])
        self.content += new + "\n"
        self.content += '</g>\n'        


    def addMain(self):
        main = '<text x="0" y="5" font-size="10" fill="black">{}</text>'.format(self.main)
        self.add(main, 2, 0)


    def addArena(self):
        pass

    def addRoom(self):
        pass

    def addGraph(self):
        pass

    def addXticks(self):
        pass

    def addYticks(self):
        pass

    def addXlab(self):
        pass

    def addYlab(self):
        pass

    
##    def drawAAPA(self, cm, frame, startTime = 0, time = 20, origin = (0, 0), boundary = False,
##                 sector = False, shocks = False, size = 300, skip = 3):
##        "adds text into sefl.content corresponding to track from one frame of AAPA"
##
##        self.content += '<g transform="translate{}">\n'.format(origin)
##
##        if boundary:
##            self.content += '<rect style="stroke:black;fill:none" x="0" y="0" ' + \
##                            'width="{0}" height="{0}" />\n'.format(size)            
##
##        start = cm.findStart(startTime)
##        time = time * 60000
##        r = cm.radius
##
##        self.content += '<g transform="translate({0},{0})">\n'.format((size / 2) - r)
##
##        if sector:
##            self.angle = cm.centerAngle
##            self.width = cm.width
##            a1 = radians(self.angle - (self.width / 2))
##            a2 = radians(self.angle + (self.width / 2))
##            Sx1, Sy1 = r + (cos(a1) * r), r - (sin(a1) * r)
##            Sx2, Sy2 = r + (cos(a2) * r), r - (sin(a2) * r)
##            self.content += '<polyline fill="none" stroke="red" stroke-width="1.5" ' +\
##                            'points="{},{} {},{} {},{}"/>\n'.format(Sx1, Sy1, r, r, Sx2, Sy2)              
##
##        self.content += '<polyline points="'        
##        if frame == "room":
##            prev = (0, 0)
##            shock = False
##            shockPositions = []
##            for line in cm.data[start:]:
##                if line[1] > time:
##                    break
##                positions = line[2:4]
##                if positions != prev:
##                    self.content += ",".join(map(str, positions)) + " "
##                if line[6] > 0:
##                    if not shock:
##                        shock = True
##                        shockPositions.append(positions)
##                else:
##                    shock = False                        
##                prev = positions
##        elif frame == "arena":
##            prev = (0, 0)
##            for count, line in enumerate(cm.data[start:], skip):
##                if line[1] > time:
##                    break
##                positions = line[7:9]
##                if count % skip == 0 and positions != prev:
##                    self.content += ",".join(map(str, positions)) + " "
##                    prev = positions
##        self.content += '" style = "fill:none;stroke:black"/>\n'
##
##        if shocks and frame == "room": # u double avoidance odstranit frame podminku
##            for position in shockPositions:
##                self.content += '<circle fill="none" stroke="red" stroke-width="1.5" ' +\
##                                'cx="{}" cy="{}" r="3" />\n'.format(*position)
##
##        self.content += '<circle fill="none" stroke="black" ' +\
##                        'cx="{0}" cy="{0}" r="{0}" />\n'.format(r)
##
##        self.content += '</g>\n'
##        
##        self.content += '</g>\n'
##
##
##    def drawGraph(self, points, furtherText = "", origin = (0, 0), boundary = False):
##        "adds text containing information about graph in self.content"
##        size = (600, 120)
##        self.content += '<g transform="translate{0}">\n'.format(origin)
##        if boundary:
##            self.content += '<rect style="stroke:black;fill:none" x="0" y="0" ' + \
##                            'width="{}" height="{}" />\n'.format(*size)  
##        self.content += furtherText
##        if points:
##            self.content += '<polyline points="'
##            for pair in points:
##                self.content += ",".join(map(str, pair)) + " "      
##            self.content += '" style = "fill:none;stroke:black"/>\n'
##        self.content += '</g>\n'


##    def saveGraph(self, cm, origin = (0, 0)):
##        "saves info about graph in self.svg"
##        size = (600, 120)
##        graph = eval(self.graphTypeVar.get()[:-1] + ', cm, purpose = "svg")')
##        yCoordinates, maxY, furtherText = graph.saveGraph(cm)
##        points = []
##        if yCoordinates:
##            length = len(yCoordinates) - 1
##            for count, y in enumerate(yCoordinates):       
##                points.append(((count * size[0]) / length, size[1] - ((y * size[1]) / maxY)))
##        self.svg.drawGraph(points, furtherText = furtherText, origin = origin, boundary = True)        

    def save(self, file):
        "closes tags and saves self.content into a file"
        self.content += '</g>\n'
        self.content += "</svg>"
        infile = open(file, mode = "w")
        infile.write(self.content)
        infile.close()        




def main():
    from cm import CM
    import os
    import os.path
    svg = SVG(300, 300)
    cm = CM(os.path.join(os.getcwd(), "TestingFiles", "09aNO465_Arena.dat"))
    svg.drawAAPA(cm, "room", boundary = True, sector = True, shocks = True)
    output = os.path.join(os.getcwd(), "TestingFiles", "test.svg") 
    svg.save(output)
    os.startfile(output)




if __name__ == "__main__": main()
