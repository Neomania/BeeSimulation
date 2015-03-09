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
def distanceBetweenVertices(vertex1,vertex2):
    return (((vertex1[0] - vertex2[0])**2) + ((vertex1[1] - vertex2[1])**2))**0.5

class Bee:
    summaryText = open('assets/summary/bee.txt','r').read()
    detailString = open('assets/detail/bee.txt','r').read()
    selected = False
    state = "Idle"
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
    def moveDirectlyTowards(self,target):#used for close range movement to a specific point
        import math
        if type(target) == tuple:
            if distanceBetweenVertices((self.xPos,self.yPos),target) <= self.vel:
                self.xPos = target[0]
                self.yPos = target[1]
                self.decideNextState()
            else:
                self.direction = math.degrees(math.atan2((target[1] - self.yPos) , (target[0] - self.xPos)))
        else:
            if distanceBetweenVertices((self.xPos,self.yPos),(target.xPos,target.yPos)) <= self.vel:
                self.xPos = target.xPos
                self.yPos = target.yPos
                self.decideNextState()
            else:
                self.direction = math.degrees(math.atan2((target.yPos - self.yPos),
                (target.xPos - self.xPos)))
    def updatePosition(self):
        import math
        self.xPos = self.xPos + (self.vel * math.cos(math.radians(self.direction)))
        self.yPos = self.yPos + (self.vel * math.sin(math.radians(self.direction)))
    def decideNextState(self):#Catch all event for end of state
        if self.state == "Moving to dance floor":
            self.target.beesOnFloor.append(self)
class DanceFloor:
    summaryText = open('assets/summary/dancefloor.txt','r').read()
    detailString = open('assets/detail/dancefloor.txt','r').read()
    radius = 20
    beesOnFloor = []
    def __init__(self,xPos,yPos):
        self.xPos = xPos
        self.yPos = yPos
        self.occupied = False
        self.beesOnFloor = []

class Hive:
    summaryText = open('assets/summary/hive.txt','r').read()
    detailString = open('assets/detail/hive.txt','r').read()
    radius = 20
    def __init__(self,xPos,yPos):
        self.xPos = xPos
        self.yPos = yPos
        self.pollenStore = 0
