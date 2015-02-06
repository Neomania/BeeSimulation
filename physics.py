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

class Entity:
    def __init__(self,xPos = 0.0,yPos = 0.0):
        self.summaryText = 'undefined'
        if summaryFilePath != None:
            summaryFile = open(summaryFilePath,'r')
            self.summaryText = summaryFile.read()
        else:
            self.summaryText = 'undefined'
        self.xPos = xPos
        self.yPos = yPos

class Bee(Entity):
    summaryText = open('assets/summary/bee.txt','r').read()
    def __init__(self,xPos,yPos):
        Entity.__init__(xPos,yPos)

    def houseKeep(self):
        while self.direction > 360:
            self.direction = self.direction - 360
        while self.direction < 0:
            self.direction = self.direction + 360
class danceFloor(Entity):
    def __init__(self,xPos,yPos):
        Entity.__init__(xPos,yPos)
        self.occupied = False
