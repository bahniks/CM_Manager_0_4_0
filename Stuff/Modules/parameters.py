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

import os

from optionget import optionGet


class Parameters(list):
    "class containing list of parameters, their methods and options"
    def __init__(self):
        #zmenit na ordereddict pomoce inheritance
        self.parameters = [["Total distance", """cm.getDistance(time = time, startTime = startTime,
                            skip = optionGet('StrideParTotalDistance', 25, 'int'), minDifference =
                            optionGet('MinDiffParTotalDistance', 0, ['int', 'float']))""",
                            "basic", optionGet("DefParDistance", True, "bool"), "DefParDistance"],
                      ["Maximum time avoided", "cm.getMaxT(time = time, startTime = startTime)",
                       "basic", optionGet("DefParMaxT", True, "bool"), "DefParMaxT"],
                      ["Entrances", "cm.getEntrances(time = time, startTime = startTime)", "basic",
                       optionGet("DefParEntrances", False, "bool"), "DefParEntrances"],
                      ["Time to first", "cm.getT1(time = time, startTime = startTime)", "basic",
                       optionGet("DefParT1", False, "bool"), "DefParT1"],
                      ["Shocks", "cm.getShocks(time = time, startTime = startTime)", "basic",
                       optionGet("DefParShocks", False, "bool"), "DefParShocks"],
                      ["Time in target sector", """cm.getTimeInTarget(time = time, startTime =
                        startTime)""", "basic", optionGet("DefParTimeInTarget", False, "bool"),
                       "DefParTimeInTarget"],
                      ["Time in opposite sector", """cm.getTimeInOpposite(time = time, startTime =
                        startTime)""", "basic", optionGet("DefParTimeInOpposite", False, "bool"),
                       "DefParTimeInOpposite"],
                      ["Time in chosen sector", """cm.getTimeInChosenSector(time = time,
                        startTime = startTime, width = optionGet('WidthParTimeInChosen', 'default',
                        ['int', 'float']), center = optionGet('AngleParTimeInChosen', 0, ['int',
                        'float']))""", "advanced", optionGet("DefParTimeInChosen", False, "bool"),
                       "DefParTimeInChosen"],
                      ["Time in sectors", """cm.getAngleBoxes(time = time, startTime = startTime,
                        results = 'condensed', boxWidth = optionGet('WidthParTimeInSectors',
                        'default', ['int', 'float']))""", "advanced",
                       optionGet("DefParSectors", False, "bool"), "DefParSectors"],
                      ["Thigmotaxis", """cm.getThigmotaxis(time = time, startTime = startTime,
                        percentSize = optionGet("ThigmotaxisPercentSize", 20,
                        ["int", "float"]))""", "advanced",
                       optionGet("DefParThigmotaxis", False, "bool"), "DefParThigmotaxis"],
                        ["Directional mean", """cm.getDirectionalMean(time = time, startTime =
                        startTime)""", "advanced", optionGet("DefParDirectionalMean", False,
                                                             "bool"), "DefParDirectionalMean"],
                        ["Circular variance", """cm.getCircularVariance(time = time, startTime =
                        startTime)""", "advanced", optionGet("DefParCircularVariance", False,
                                                             "bool"), "DefParCircularVariance"],
                        ["Maximum time of immobility", """cm.getMaxTimeOfImmobility(time = time,
                        startTime = startTime, minSpeed = optionGet('MinSpeedMaxTimeImmobility',
                        10, ['int', 'float']), skip = optionGet('SkipMaxTimeImmobility', 12,
                        ['int']), smooth = optionGet('SmoothMaxTimeImmobility', 2,
                        ['int']))""", "experimental",
                         optionGet("DefParMaxTimeImmobility", False, "bool"),
                         "DefParMaxTimeImmobility"],
                        ["Periodicity", """cm.getPeriodicity(time = time, startTime = startTime,
                         minSpeed = optionGet('MinSpeedPeriodicity', 10, ['int', 'float']),
                         skip = optionGet('SkipPeriodicity', 12, ['int']),
                         smooth = optionGet('SmoothPeriodicity', 2, ['int']),
                         minTime = optionGet('MinTimePeriodicity', 9, ['int', 'float',
                         'list']))""", "experimental",
                         optionGet("DefParPeriodicity", False, "bool"), "DefParPeriodicity"],
                        ["Proportion of time moving", """cm.getPercentOfMobility(time = time,
                        startTime = startTime, minSpeed = optionGet('MinSpeedPercentMobility',
                        5, ['int', 'float']), skip = optionGet('SkipPercentMobility', 12,
                        ['int']), smooth = optionGet('SmoothPercentMobility', 2,
                        ['int']))""", "experimental",
                         optionGet("DefParPercentMobility", False, "bool"),
                         "DefParPercentMobility"],
                        ["Mean distance from center", """cm.getMeanDistanceFromCenter(time = time,
                        startTime = startTime)""", "advanced",
                         optionGet("DefParMeanDistanceFromCenter", False, "bool"),
                         "DefParMeanDistanceFromCenter"],
                        ["Median speed after shock", """cm.getSpeedAfterShock(time = time, 
                        startTime = startTime, after = optionGet('SkipSpeedAfterShock', 25,
                        ['int']), absolute = optionGet('AbsoluteSpeedAfterShock', False,
                        'bool'))""", "experimental", optionGet("DefParSpeedAfterShock", False,
                                                               "bool"), "DefParSpeedAfterShock"],                           
                        ["Angle of target sector", "cm.centerAngle", "info",
                         optionGet("DefParCenterAngle", False, "bool"), "DefParCenterAngle"],    
                        ["Width of target sector", "cm.width", "info",
                         optionGet("DefParSectorWidth", False, "bool"), "DefParSectorWidth"],
                        ["Real minimum time", "cm.realMinimumTime()", "info",
                         optionGet("DefParRealMinTime", False, "bool"), "DefParRealMinTime"],
                        ["Real maximum time", "cm.realMaximumTime()", "info",
                         optionGet("DefParRealMaxTime", False, "bool"), "DefParRealMaxTime"],
                        ["Room frame filename", "cm.nameR", "info",
                         optionGet("DefParRoomFrameFilename", False, "bool"),
                         "DefParRoomFrameFilename"]
                      ]
        
        self.options = {"Total distance": (("Computed from every [skip in rows]",
                                            optionGet('StrideParTotalDistance', 25, 'int')),
                                           ("Minimal distance counted [in pixels]",
                                            optionGet('MinDiffParTotalDistance', 0,
                                                      ['int', 'float']))),
                        "Thigmotaxis": [
                            ("Annulus width [percent of radius]", optionGet(
                                "ThigmotaxisPercentSize", 20, ["int", "float"]))
                            ],
                        "Time in chosen sector": (
                            ("Center of sector relative to the target [in degrees]",
                             optionGet('AngleParTimeInChosen', 0, ['int', 'float'])),
                            ("Width of sector ('default' if same as target; otherwise in degrees)",
                             optionGet('WidthParTimeInChosen', 'default', ['int', 'float']))
                            ),
                        "Time in sectors": [
                            ("Width of sector ('default' if same as target; otherwise in degrees)",
                             optionGet('WidthParTimeInSectors', 'default', ['int', 'float']))
                            ],
                        "Maximum time of immobility": (
                            ("Minimum speed counted [in cm/s]", optionGet(
                                'MinSpeedMaxTimeImmobility', 10, ['int', 'float'])),
                            ("Computed from every [skip in rows]", optionGet(
                                'SkipMaxTimeImmobility', 12, ['int'])),
                            ("Averaged across [intervals]", optionGet(
                                'SmoothMaxTimeImmobility', 2, ['int']))),
                        "Periodicity": (
                            ("Minimum speed counted [in cm/s]", optionGet(
                                'MinSpeedPeriodicity', 10, ['int', 'float'])),
                            ("Computed from every [skip in rows]", optionGet(
                                'SkipPeriodicity', 12, ['int'])),
                            ("Averaged across [intervals]", optionGet(
                                'SmoothPeriodicity', 2, ['int'])),
                            ("Minimum time of interval [in seconds]", optionGet(
                                'MinTimePeriodicity', 9, ['int', 'float', 'list']))
                            ),
                        "Proportion of time moving": (
                            ("Minimum speed counted [in cm/s]", optionGet(
                                'MinSpeedPercentMobility', 5, ['int', 'float'])),
                            ("Computed from every [skip in rows]", optionGet(
                                'SkipPercentMobility', 12, ['int'])),
                            ("Averaged across [intervals]", optionGet(
                                'SmoothPercentMobility', 2, ['int']))
                            ),
                        "Median speed after shock": (
                            ("Computed from every [skip in rows]", optionGet(
                                'SkipSpeedAfterShock', 25, ['int'])),
                            ("Computed from absolute values", optionGet(
                                'AbsoluteSpeedAfterShock', False, ['bool']))
                            )                                                  
                        }

        self.findParameters()
        

    def findParameters(self):
        "finds custom written parameters"
        for file in os.listdir(os.path.join(os.getcwd(), "Stuff", "Parameters")):
            splitted = os.path.splitext(file)
            omit = ["__init__", "template"]
            if len(splitted) > 1 and splitted[1] == ".py" and splitted[0] not in omit:
                exec("from Stuff.Parameters import {}".format(splitted[0]))
                option = "DefParCustom{}".format(
                    eval("{}.name".format(splitted[0])).strip().replace(" ", ""))
                newParameter = [eval("{}.name".format(splitted[0])),
                                "{}.parameter(cm, time = time, startTime = startTime)".format(
                                    splitted[0]), "custom", optionGet(option, False, "bool"),
                                option, splitted[0]]
                self.parameters.append(newParameter)  
