#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Timothy
#
# Created:     03/02/2015
# Copyright:   (c) Timothy 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

class Bee:
    summaryText = open('assets/summary/bee.txt','r').read()
    detailString = open('assets/detail/bee.txt','r').read()
    selected = False
    def __init__(self,hive):
        self.xPos = hive.xPos
        self.yPos = hive.yPos
        self.vel = 0
        self.direction = 0
        self.selected = False
    def houseKeep(self):
        while self.direction > 360:
            self.direction = self.direction - 360
        while self.direction < 0:
            self.direction = self.direction + 360
    def updatePosition(self):
        import math
        self.xPos = self.xPos + (self.vel * math.cos(math.radians(self.direction)))
        self.yPos = self.yPos + (self.vel * math.sin(math.radians(self.direction)))
class DanceFloor:
    summaryText = open('assets/summary/dancefloor.txt','r').read()
    detailString = open('assets/detail/dancefloor.txt','r').read()
    radius = 20
    def __init__(self,xPos,yPos):
        self.xPos = xPos
        self.yPos = yPos
        self.occupied = False

class Hive:
    summaryText = open('assets/summary/hive.txt','r').read()
    detailString = open('assets/detail/hive.txt','r').read()
    radius = 20
    def __init__(self,xPos,yPos):
        self.xPos = xPos
        self.yPos = yPos
        self.pollenStore = 0
