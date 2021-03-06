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
import sharedfunctions
def distanceBetweenVertices(vertex1,vertex2):
    return (((vertex1[0] - vertex2[0])**2) + ((vertex1[1] - vertex2[1])**2))**0.5

class Bee:
    summaryText = open('assets/summary/bee.txt','r').read()
    detailString = open('assets/detail/bee.txt','r').read()
    selected = False
    state = "Idle"
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
        self.stateTime = 0
        self.subStateTime = 0
        self.memoryStore = []
        self.distanceTravelled = 0
        self.visitedFlowers = []
        self.hive.beeArray.append(self)

        #waggle dance variables
        self.wdLength = 0
        self.wdAmp = 0
        self.wdStart = (0,0)
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
        import random, math
        if self.state == "Moving to dance floor":
            self.state = "Attending dance"
        elif self.state == "Returning to hive":
            if self.roundDanced: #disables round dance after some time
                roundDanceChance = random.random()
                if roundDanceChance < 0.1:
                    self.roundDanced = False
            self.state = "Idle"
            self.stateTime = random.randint(60,240)
            self.visitedFlowers = []
            self.sortMemory()
        elif self.state == "Searching local area":
            self.subStateTime = 0
        elif self.state == "Preparing to dance": #create dance, recruit bees
            if self.memoryStore[0].distance < 200: #round dance
                self.state = "Performing round dance"
                self.stateTime = 600
                self.directionIncrement = 4
                self.yPos = self.yPos - 13
                self.direction = 0
            else:
                self.state = "Performing waggle dance"
                self.stateTime = 600
                self.wdLength = ((self.memoryStore[0].distance/1000)
                * (self.target.radius * 2))
                self.wdAmp = (self.memoryStore[0].flower.pollenRate * 2)
                self.direction = self.memoryStore[0].direction
                self.wdStart = (((0 - self.wdLength*0.5) * (math.cos(math.radians(self.direction)))) + self.target.xPos,
                ((0 - self.wdLength*0.5) * (math.sin(math.radians(self.direction)))) + self.target.yPos)
                self.xPos = self.wdStart[0]
                self.yPos = self.wdStart[1]
                self.distanceTravelled = 0
            for bee in self.hive.beeArray: #recruit bees
                if bee.state == "Idle":
                    chance = random.random()
                    if chance > 0.5:
                        bee.state = "Moving to dance floor"
                        bee.target = sharedfunctions.pointAround(self.target,
                        self.target.radius)
                        self.target.beesOnFloor.append(bee)

        elif self.state == "Idle": #probably the most complex
            decision = random.random()
            if decision < 0.1:
                self.state = "Idle"
                self.stateTime = random.randint(60,240)
            elif decision < 0.7 and self.roundDanced:
                self.state = "Searching local area"
                self.stateTime = random.randint(600,900)
                self.subStateTime = 0
            elif decision < 0.7 and self.memoryStore != []:
                self.state = "Moving to known food source"
                self.target = self.memoryStore[0]
                self.distanceTravelled = 0
            elif decision < 0.9 and sharedfunctions.danceFloorFree(self.hive) and self.memoryStore != []:
                #do your dance at the space jam
                for danceFloor in self.hive.danceFloors:
                    if danceFloor.occupied == False:
                        self.target = danceFloor
                self.target.occupied = True
                self.state = "Preparing to dance"
            else:
                self.stateTime = random.randint(600,900)
                self.subStateTime = 0
                self.state = "Foraging randomly"
                self.direction = random.randrange(0,360)
        elif self.state == "Moving to flower":#docking request accepted
            self.state = "Harvesting pollen"
            self.subStateTime = self.stateTime #use substate as holder
            self.stateTime = round(200 / self.target.pollenRate)
    def moveTowardsMemory(self):#moves towards memory using distance and dir
        import random
        if self.distanceTravelled > self.target.distance:
            self.state = "Foraging randomly"
            self.distanceTravelled = 0
            self.stateTime = random.randint(600,900)
        else:
            self.direction = self.target.direction + random.randint(-3,3)
            self.updatePosition()
            self.distanceTravelled = self.distanceTravelled + self.vel
    def createMemoryAbout(self,flower):
        import math, sharedfunctions
        memoryExists = False
        for memory in self.memoryStore:
            if memory.flower == flower:
                memoryExists = True
        if memoryExists == False:
            #find direction from hive
            flowerVector = math.degrees(math.atan2((flower.yPos - self.hive.yPos)
            ,(flower.xPos - self.hive.xPos)))
            flowerDistance = sharedfunctions.distanceBetweenVertices(
            (flower.xPos,flower.yPos),(self.hive.xPos,self.hive.yPos))
            self.memoryStore.append(Memory(flowerVector,flowerDistance,flower))
    def returnToHive(self):
        import random
        self.state = "Returning to hive"
        self.target = sharedfunctions.pointAround(self.hive,
        random.randint(0,self.hive.radius))
    def sortMemory(self):#Simple one-run bubble sort
        if self.memoryStore != []:
            for memory in self.memoryStore:
                if memory.flower.pollenRate > self.memoryStore[0].flower.pollenRate:
                    swapIndex = self.memoryStore.index(memory)
                    holdingMemory = self.memoryStore[0] #excuse the mess, necessary for lists
                    self.memoryStore[0] = memory
                    self.memoryStore[swapIndex] = holdingMemory
    def attendDance(self,danceFloor):
        import random
class Memory:
    direction = 0.0
    distance = 0.0
    flower = None
    def __init__(self,direction,distance,flower):
        self.direction = direction
        self.distance = distance
        self.flower = flower

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
        self.danceFloors = []
        self.beeArray = []

class Flower:
    summaryText = open('assets/summary/flower.txt','r').read()
    detailString = open('assets/detail/flower.txt','r').read()
    radius = 10
    occupied = False
    occupant = None
    def __init__(self,xPos,yPos,colour,pollenRate):
        self.xPos = xPos
        self.yPos = yPos
        self.colour = colour
        self.pollenRate = pollenRate
        self.occupied = False
    def acceptBee(self,bee):
        self.occupant = bee
        self.occupied = True
    def doneWithBee(self):
        self.occupant = None
        self.occupied = False