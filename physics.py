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
    state = "Foraging randomly"
    destination = None
    def __init__(self,hive):
        self.xPos = hive.xPos
        self.yPos = hive.yPos
        self.vel = 1
        self.direction = 0
        self.selected = False
        self.destination = None
        self.hive = hive
        self.roundDanced = False
        self.stateTime = 600
        self.subStateTime = 0
        self.memoryStore = []
        self.distanceTravelled = 0
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
                self.updatePosition()
        else:
            if distanceBetweenVertices((self.xPos,self.yPos),(target.xPos,target.yPos)) <= self.vel:
                self.xPos = target.xPos
                self.yPos = target.yPos
                self.decideNextState()
            else:
                self.direction = math.degrees(math.atan2((target.yPos - self.yPos),
                (target.xPos - self.xPos)))
                self.updatePosition()
    def updatePosition(self):
        import math
        self.xPos = self.xPos + (self.vel * math.cos(math.radians(self.direction)))
        self.yPos = self.yPos + (self.vel * math.sin(math.radians(self.direction)))
    def decideNextState(self):#Catch all event for end of state
        import random
        if self.state == "Moving to dance floor":
            self.target.beesOnFloor.append(self)
            self.state = "Attending dance"
        elif self.state == "Attending dance":
            self.target = (self.hive.xPos,self.hive.yPos)
            self.state = "Returning to hive"
        elif self.state == "Returning to hive":
            self.state = "Idle"
            self.stateTime = random.randint(60,240)
        elif self.state == "Idle": #probably the most complex
            if self.roundDanced: #if a round dance has been watched
                decision = random.random()
                if decision < 0.1:
                    self.state = "Idle"
                    self.stateTime = random.randint(60,240)
                elif decision < 0.7:
                    self.state = "Searching local area"
                elif decision < 0.8:
                    if self.memoryStore != []:
                        self.state = "Moving to known food source"
                        self.target = self.memoryStore[0]
                else: #Randomly wander
                    self.stateTime = random.randint(600,900)
                    self.state = "Foraging randomly"
                    self.direction = random.randrange(0,360)
            else:
                decision = random.random()
                if decision < 0.1:
                    self.state = "Idle"
                    self.stateTime = random.randint(60,240)
                elif decision < 0.8 and self.memoryStore != []:
                    self.state = "Moving to known food source"
                    self.target = self.memoryStore[0]
                else:
                    self.stateTime = random.randint(600,900)
                    self.state = "Foraging randomly"
                    self.direction = random.randrange(0,360)
    def moveTowardsMemory(self):#moves towards memory using distance and dir
        if self.distanceTravelled > self.target.distance:
            self.state = "Foraging randomly"
            self.distanceTravelled = 0
        else:
            self.direction = self.target.direction + random.randint(-3,3)
            self.updatePosition()
            self.distanceTravelled = self.distanceTravelled + self.vel

    def attendDance(self,danceFloor):
        import random
class Memory:
    direction = 0.0
    distance = 0.0
    def __init__(self,direction,distance):
        self.direction = direction
        self.distance = distance

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
