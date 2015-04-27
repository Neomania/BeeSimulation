#-------------------------------------------------------------------------------
# Name:        main
# Purpose:     brings the other bee modules together
#
# Author:      Timothy
#
# Created:     22/1/2015
# Copyright:   (c) Timothy 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
def betweenVertices(selectionStart,selectionEnd,entity):
    inX = False
    inY = False
    if entity.xPos > selectionStart[0]:
        if entity.xPos < selectionEnd[0]:
            inX = True
    elif entity.xPos > selectionEnd[0]:
        inX = True
    if entity.yPos > selectionStart[1]:
        if entity.yPos < selectionEnd[1]:
            inY = True
    elif entity.yPos > selectionEnd[1]:
        inY = True
    if inX and inY:
        return True
    else:
        return False
def distanceBetweenVertices(vertex1,vertex2):
    return (((vertex1[0] - vertex2[0])**2) + ((vertex1[1] - vertex2[1])**2))**0.5

from pygame.locals import *
from physics import *
import pygame
pygame.init()
import sys, os, random, ui, math, globalcfg, fonts, physics
import pygame.freetype
import sharedfunctions
clock = pygame.time.Clock()
FPS = 60
DEVPINK = (255,0,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (0,255,255)
BLACK = (0,0,0)
WHITE = (255,255,255)
DETAILFONTCOLOUR = (147,161,161)
mousePos = (0,0)
displaySurface = pygame.display.set_mode(
(globalcfg.windowWidth,globalcfg.windowHeight))
scrollSpeed = 5
globalcfg.displayingDetail = False #DENOTES IF GAME IS DISPLAYING DETAIL PANEL
selectionStart = (0,0)
selecting = False

#PHYSICS
simHeight = 750
halfSimHeight = simHeight / 2
simWidth = 750
halfSimWidth = simWidth / 2
simSurface = pygame.Surface((simWidth,simHeight))
beeArray = []
flowerArray = []
danceFloorArray = []
globalcfg.selectedBeeArray = []

danceFloorArray.append(DanceFloor(40,0))
danceFloorArray.append(DanceFloor(-40,0))
danceFloorArray.append(DanceFloor(0,40))
danceFloorArray.append(DanceFloor(0,-40))

hiveArray = [] #in the odd case that we eventually add more hives

home = Hive(0.0,0.0)
hiveArray.append(home)
home.danceFloors.append(danceFloorArray[0])
home.danceFloors.append(danceFloorArray[1])
home.danceFloors.append(danceFloorArray[2])
home.danceFloors.append(danceFloorArray[3])

#FONTS
testString = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."

pygame.freetype.init()

infoFontSize = 12
infoFont = pygame.freetype.SysFont('Consolas',infoFontSize)
for i in range(0,25):
    beeArray.append(Bee(home))

flowerArray.append(Flower(305,300,GREEN,0.5))
flowerArray.append(Flower(305,305,GREEN,0.5))
flowerArray.append(Flower(300,300,GREEN,0.5))
flowerArray.append(Flower(310,310,GREEN,0.5))
flowerArray.append(Flower(300,310,GREEN,0.5))
flowerArray.append(Flower(200,200,BLUE,1))

detailOverlay = pygame.image.load('assets/ui/detailoverlay.png')
detailUnderlay = pygame.image.load('assets/ui/detailunderlay.png')
##detailButtons = [ui.Button(725,0,25,25,'assets/ui/closeDetail.png',closeDetail),
##                ui.Button(700,0,25,25,'assets/ui/refreshDetail.png',ui.updateDetail)]
for button in ui.detailButtons:
    button.clickable = globalcfg.displayingDetail

ui.updateSummary()

while True: #MAIN GAME LOOP
    displaySurface.fill(BLACK)
    mousePos = pygame.mouse.get_pos() #mousePosWorld gives world coords
    #ie. not screen coordinates
    mousePosWorld = (mousePos[0] - halfSimWidth, mousePos[1] - halfSimHeight)
    #PHYSICS, DECISION, ALL NON-UI ACTIONS
    if globalcfg.displayingDetail == False:
        for potato in range(0,globalcfg.speedMultiplier):
            for bee in beeArray:
                if bee.state == "Moving to dance floor":
                    bee.moveDirectlyTowards(bee.target)
                elif bee.state == "Returning to hive":
                    bee.moveDirectlyTowards(bee.target)
                elif bee.state == "Preparing to dance":
                    bee.moveDirectlyTowards(bee.target)
                elif bee.state == "Attending dance":
                    pass
                elif bee.state == "Performing round dance":
                    bee.updatePosition()
                    bee.direction = bee.direction + bee.directionIncrement
                    bee.stateTime = bee.stateTime - 1
                    if bee.stateTime <= 0:
                        for attendant in bee.target.beesOnFloor:
                            attendant.roundDanced = True
                            bee.target.beesOnFloor.remove(attendant)
                            attendant.returnToHive()
                        bee.target.occupied = False
                        bee.returnToHive()
                elif bee.state == "Performing waggle dance":
                    bee.stateTime = bee.stateTime - 1
                    if bee.distanceTravelled >= bee.wdLength:
                        bee.xPos = bee.wdStart[0]
                        bee.yPos = bee.wdStart[1]
                        bee.distanceTravelled = 0
                    else:
                        bee.updatePosition()
                        bee.distanceTravelled = bee.distanceTravelled + bee.vel
                    if bee.stateTime <= 0:
                        try:
                            bee.target.occupied = False
                        except:
                            print(bee.target)
                        for attendant in bee.target.beesOnFloor:
                            bee.target.beesOnFloor.remove(attendant)
                            attendant.createMemoryAbout(bee.memoryStore[0].flower)
                            attendant.returnToHive()
                        bee.returnToHive()
                elif bee.state == "Searching local area":
                    if bee.stateTime <= 0:
                        bee.returnToHive()
                    elif bee.subStateTime <= 0:
                        bee.target = sharedfunctions.pointAround(bee.hive,
                        random.randint(10,200))
                        bee.subStateTime = random.randint(200,240)
                    else:
                        bee.subStateTime = bee.subStateTime - 1
                        bee.stateTime = bee.stateTime - 1
                        #check for nearby unoccupied flower
                        nearestToBee = 9999999999.9
                        nearestFlower = None
                        for flower in flowerArray:
                            if flower.occupied == False and (flower not in bee.visitedFlowers):
                                distanceToBee = distanceBetweenVertices(
                                (flower.xPos,flower.yPos),(bee.xPos,bee.yPos))
                                if distanceToBee < nearestToBee and distanceToBee < 50:
                                    nearestToBee = distanceToBee
                                    nearestFlower = flower
                        if nearestFlower != None:
                            nearestFlower.acceptBee(bee)
                            bee.state = "Moving to flower"
                            bee.target = nearestFlower
                elif bee.state == "Idle":
                    bee.stateTime = bee.stateTime - 1
                    if bee.stateTime <= 0:
                        bee.decideNextState()
                elif bee.state == "Foraging randomly":
                    if bee.subStateTime <= 0:
                        bee.directionIncrement = random.randrange(-3,3)
                        bee.subStateTime = random.randint(0,60)
                    bee.subStateTime = bee.subStateTime - 1
                    bee.stateTime = bee.stateTime - 1
                    bee.direction = bee.direction + bee.directionIncrement
                    bee.updatePosition()
                    #check for nearby unoccupied flower
                    nearestToBee = 9999999999.9
                    nearestFlower = None
                    for flower in flowerArray:
                        if flower.occupied == False and (flower not in bee.visitedFlowers):
                            distanceToBee = distanceBetweenVertices(
                            (flower.xPos,flower.yPos),(bee.xPos,bee.yPos))
                            if distanceToBee < nearestToBee and distanceToBee < 50:
                                nearestToBee = distanceToBee
                                nearestFlower = flower
                    if nearestFlower != None:
                        nearestFlower.acceptBee(bee)
                        bee.state = "Moving to flower"
                        bee.target = nearestFlower
                    if bee.stateTime <= 0:
                        bee.returnToHive()
                elif bee.state == "Moving to flower":
                    bee.moveDirectlyTowards(bee.target)
                elif bee.state == "Harvesting pollen":
                    bee.stateTime = bee.stateTime - 1
                    if bee.stateTime <= 0: #done
                        bee.visitedFlowers.append(bee.target)
                        bee.createMemoryAbout(bee.target)
                        bee.target.doneWithBee()
                        if bee.roundDanced:
                            bee.state = "Searching local area"
                            bee.stateTime = bee.subStateTime
                            bee.subStateTime = random.randint(200,240)
                            bee.target = sharedfunctions.pointAround(
                            bee.hive,random.randint(10,200))
                        else:
                            bee.state = "Foraging randomly"
                            bee.stateTime = bee.subStateTime
                            bee.subStateTime = 0
                elif bee.state == "Moving to known food source":
                    bee.moveTowardsMemory()

    #USER INPUT HANDLING
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 5: #MOUSEWHEELDOWN
                for div in ui.textDivisionArray:
                    if div.rect.collidepoint(mousePos) and div.scrollable:
                        div.scrollAmount = div.scrollAmount - scrollSpeed
            elif event.button == 4:#MOUSEWHEELUP
                for div in ui.textDivisionArray:
                    if div.rect.collidepoint(mousePos) and div.scrollable and div.scrollAmount < 0:
                        div.scrollAmount = div.scrollAmount + scrollSpeed
            elif event.button == 1: #LEFT MOUSE CLICK
                if ui.detailTextDiv.rect.collidepoint(mousePos) and globalcfg.displayingDetail:
                    for element in ui.detailElements:
                        if type(element) is ui.Video:
                            if element.rect.collidepoint((mousePos[0],
                            mousePos[1] - 25 - ui.detailTextDiv.scrollAmount)):
                                if element.movie.get_busy():
                                    element.movie.stop()
                                else:
                                    for vid in ui.detailElements:
                                        if type(vid) is ui.Video:
                                            vid.movie.stop()
                                    element.play() #why does this fix the problem
                                    element.play() #this is an affront to everything I stand for
                elif mousePos[0] <= simWidth and globalcfg.flowerPlacing == True:
                    flowerArray.append(Flower(mousePosWorld[0],mousePosWorld[1],
                    globalcfg.createdFlowerColour,globalcfg.createdFlowerRate))
                elif mousePos[0] <= simWidth and globalcfg.displayingDetail == False:
                    if selecting == False:
                        selecting = True
                        selectionStart = mousePosWorld

        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                if globalcfg.displayingDetail == False:
                    if selecting and distanceBetweenVertices(selectionStart,mousePosWorld) > 10:
                        selecting = False
                        for bee in beeArray:
                            if betweenVertices(selectionStart,mousePosWorld,
                            bee):
                                bee.selected = True
                        globalcfg.selectedBeeArray = []
                        for bee in beeArray: #housekeeping
                            if bee.selected:
                                globalcfg.selectedBeeArray.append(bee)
                        if globalcfg.selectedBeeArray != []:
                            globalcfg.selectedItem = globalcfg.selectedBeeArray[0]
                            ui.updateSummary()
                    elif selecting:#click to deselect
                        selecting = False
                        globalcfg.selectedItem = None
                        ui.updateSummary()
                        for bee in globalcfg.selectedBeeArray:
                            bee.selected = False
                        globalcfg.selectedBeeArray = []
                        #Also: try selecting other entity, eg. dance floor
                        for entity in (hiveArray
                         + flowerArray
                         + danceFloorArray):#all non-bee, non-ui arrays here
                            if distanceBetweenVertices(mousePosWorld,
                            (entity.xPos,entity.yPos)) < entity.radius:
                                globalcfg.selectedItem = entity
                        ui.updateSummary()
                for button in (ui.buttonArray + ui.detailButtons):
                    if button.rect.collidepoint(mousePos) and button.clickable:
                        button.proc()
                        ui.speedDivision.textArray = ui.divideStringIntoList(
                        str("speed: " + str(globalcfg.speedMultiplier) + 'x'
                        ),ui.speedDivision.characterWidth)
                        print(ui.speedDivision.textArray)

    if globalcfg.selectedBeeArray == []:
        ui.selectNextButton.clickable = False
        ui.selectPrevButton.clickable = False
    else:
        ui.selectNextButton.clickable = True
        ui.selectPrevButton.clickable = True
    #DRAW SIMULATION
    simSurface.fill(BLACK)
    for hive in hiveArray:
        #DRAW HIVE
        pygame.draw.circle(simSurface,(125,125,0),
        (round(hive.xPos + (simWidth / 2)),
        round(hive.yPos + (simHeight/2))),hive.radius)
    for danceFloor in danceFloorArray:
        #DRAW DANCE FLOORS
        pygame.draw.circle(simSurface,(150,150,0),
        (round(danceFloor.xPos + (simWidth/2)),
        round(danceFloor.yPos + (simHeight/2))),danceFloor.radius)
    for flower in flowerArray:
        #DRAW FLOWERS
        pygame.draw.circle(simSurface,flower.colour,
        (round(flower.xPos + halfSimWidth),
        round(flower.yPos + halfSimHeight)),flower.radius)
        #DRAW BEES
    for bee in beeArray:
        pygame.draw.circle(simSurface,(255,255,0),
        (round(bee.xPos + (simWidth/2)),round(bee.yPos + (simHeight/2))
        ),2)
        if bee.selected:
            if bee == globalcfg.selectedItem:
                pygame.draw.circle(simSurface,RED,
                (round(bee.xPos + (simWidth/2)),round(bee.yPos + (simHeight/2))),
                10,2)
            else:
                pygame.draw.circle(simSurface,RED,
                (round(bee.xPos + (simWidth/2)),round(bee.yPos + (simHeight/2))),
                5,1)
    if selecting == True:
        selectionSize = (mousePosWorld[0] - selectionStart[0],mousePosWorld[1] - selectionStart[1])
        selectionRect = pygame.Rect((selectionStart[0] + halfSimWidth,
        selectionStart[1] + halfSimHeight),selectionSize)
        pygame.draw.rect(simSurface,RED,selectionRect,2)
    for fx in ui.expandingCircleArray:
        if fx.timeLived >= fx.timeToLive:
            ui.expandingCircleArray.remove(fx)
        else:
            pygame.draw.circle(simSurface,fx.colour,
            (round(fx.xPos + (simWidth/2)),round(fx.yPos + (simHeight/2))),
            fx.timeLived, fx.lineWidth)
            fx.timeLived = fx.timeLived + 1

    #APPLY SIMSURFACE TO DISPLAY SURFACE
    displaySurface.blit(simSurface,(0,0))
    #DRAW BASE UI
    displaySurface.blit(ui.baseUI,(0,0))
    #DETAIL BITS
    if globalcfg.displayingDetail == True:
        #DRAW DETAIL BASE
        ui.detailSurface.fill((0,43,54))
        pygame.draw.rect(displaySurface,(0,43,54),pygame.Rect(20,20,710,710))
        lineNumber = 0
        for element in ui.detailElements:
            if type(element) is str:
                if 25 + (lineNumber * (ui.detailTextDiv.fontSize[1] +
                ui.detailTextDiv.lineSpace)) + ui.detailTextDiv.scrollAmount >= 0:
                    fonts.detailedFont.render_to(ui.detailSurface,
                    (0,25 + (lineNumber * (ui.detailTextDiv.fontSize[1] +
                     ui.detailTextDiv.lineSpace)) + ui.detailTextDiv.scrollAmount)
                     ,element,DETAILFONTCOLOUR)
                lineNumber = lineNumber + 1
            elif type(element) is ui.Video:
                ui.detailSurface.blit(element.movieSurface,(element.rect.left,25 + (lineNumber * (ui.detailTextDiv.fontSize[1] +
                 ui.detailTextDiv.lineSpace)) + ui.detailTextDiv.scrollAmount))
            elif type(element) is ui.Image:
                ui.detailSurface.blit(element.imageSurface,(0,25 + (lineNumber * (ui.detailTextDiv.fontSize[1] +
                 ui.detailTextDiv.lineSpace)) + ui.detailTextDiv.scrollAmount))
        displaySurface.blit(ui.detailSurface,(25,0))
        displaySurface.blit(detailOverlay,(0,0))
        for button in ui.detailButtons:
            if button.rect.collidepoint(mousePos):
                if pygame.mouse.get_pressed()[0]:
                    displaySurface.blit(button.spriteSheet,
                    button.rect,
                    button.clickedRect)
                else:
                    displaySurface.blit(button.spriteSheet,
                    button.rect,
                    button.mouseOverRect)
            else:
                displaySurface.blit(button.spriteSheet,
                button.rect,
                button.neutralRect)
    #DRAW TEXT
    for div in ui.textDivisionArray:
        lineNumber = 0
        if div.textArray != None:
            for line in div.textArray:
                if (lineNumber * (div.fontSize[1] + div.lineSpace)) + div.scrollAmount >= 0 and (lineNumber * (div.fontSize[1] + div.lineSpace)) + div.scrollAmount <= div.height:
                    div.font.render_to(displaySurface,(div.xPos,div.yPos + div.scrollAmount + (lineNumber * (div.fontSize[1] + div.lineSpace))),line,WHITE)
                else:
                    #print(line)
                    pass
                lineNumber = lineNumber + 1
        else:
            print("NONE AAA")
    #DRAW BUTTONS
    for button in ui.buttonArray:
        if button.clickable:
            if button.rect.collidepoint(mousePos):
                if pygame.mouse.get_pressed()[0]:
                    displaySurface.blit(button.spriteSheet,
                    button.rect,
                    button.clickedRect)
                else:
                    displaySurface.blit(button.spriteSheet,
                    button.rect,
                    button.mouseOverRect)
            else:
                displaySurface.blit(button.spriteSheet,
                button.rect,
                button.neutralRect)
        else:
            displaySurface.blit(button.spriteSheet,
            button.rect,
            button.unclickableRect)
    print(ui.pollenRateDivision.textArray)
    pygame.display.update()
    clock.tick(FPS)

##if __name__ == '__main__':
##    from pygame.locals import *
##    from physics import *
##    main()