#-------------------------------------------------------------------------------
# Name:        ui elements
# Purpose:
#
# Author:      Timothy
#
# Created:     20/01/2015
# Copyright:   (c) Timothy 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from functions import *
from fonts import *
import globalcfg, pygame

testString = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."


def divideStringIntoList(stringToDivide,lineLength):
    stringLength = len(stringToDivide) - 1
    spacePointer = 0
    endOfLastLinePointer = 0
    currentPointer = 0
    charactersSoFar = 0
    returnList = []

    while currentPointer < stringLength:
        charactersSoFar = 0
        while charactersSoFar < lineLength and currentPointer < stringLength:
            if stringToDivide[currentPointer] == ' ':
                spacePointer = currentPointer
            currentPointer = currentPointer + 1
            charactersSoFar = charactersSoFar + 1
        if currentPointer < stringLength: #checks why it exited the loop
            returnList.append(
            stringToDivide[endOfLastLinePointer:spacePointer])
            currentPointer = spacePointer + 1
            endOfLastLinePointer = currentPointer
        else:
            returnList.append(stringToDivide[endOfLastLinePointer:])
    return returnList

class Button:
    import pygame
    rect = pygame.Rect
    procCall = None
    spriteSheet = None
    neutralRect = pygame.Rect
    mouseOverRect = pygame.Rect
    clickedRect = pygame.Rect
    unclickableRect = pygame.Rect
    clickable = True

    def __init__(self,xPos,yPos,width,height,spriteImage,procCall = None,parameters = None):
        import pygame
        self.rect = pygame.Rect(xPos,yPos,width,height)
        self.clickable = True
        self.procCall = procCall
        self.spriteSheet = pygame.image.load(spriteImage)
        self.neutralRect = pygame.Rect(0,0,width,height)
        self.mouseOverRect = pygame.Rect(width,0,width,height)
        self.clickedRect = pygame.Rect(2*width,0,width,height)
        self.unclickableRect = pygame.Rect(3*width,0,width,height)
        self.parameters = parameters
    def proc(self):
        if self.procCall == None:
            print("No procedure specified")
        elif self.parameters == None:
            self.procCall()
        else:
            self.procCall(self.parameters)
class textDivision:
    import pygame
    import pygame.freetype
    rect = pygame.Rect
    textArray = []
    def __init__(self,xPos,yPos,width,height,fontToUse,fontSize,scrollable = False):
        import pygame, math
        import pygame.freetype
        self.xPos = xPos
        self.yPos = yPos
        self.width = width
        self.height = height
        self.rect = pygame.Rect(xPos,yPos,width,height)
        self.textArray = []
        self.font = fontToUse
        self.scrollAmount = 0
        self.scrollable = scrollable
        testCharacter = fontToUse.render('a',(255,255,255))
        self.fontSize = (testCharacter[0].get_width()
        + round(testCharacter[0].get_width() / 10)
        ,testCharacter[0].get_height())
        self.characterWidth = math.floor(self.width / (self.fontSize[0])) #rough height

buttonArray = []
reduceSpeedButton = (Button(750,437,62,63, #SLOWDOWN BUTTON
'assets/ui/reduceSpeed.png',reduceSpeed))
buttonArray.append(reduceSpeedButton)
increaseSpeedButton = (Button(812,437,63,63, #SPEEDUP BUTTON
'assets/ui/increaseSpeed.png',increaseSpeed))
buttonArray.append(increaseSpeedButton)
newFlowerButton = (Button(875,375,125,125, #NEW FLOWER BUTTON
'assets/ui/newFlower.png'))
buttonArray.append(newFlowerButton)

textDivisionArray = []

infoBoxDivision = (textDivision(750,0,250,300,infoFont,infoFontSize,True)) #INFOBOX
textDivisionArray.append(infoBoxDivision)
infoBoxDivision.textArray = divideStringIntoList(
testString,infoBoxDivision.characterWidth)

speedDivision = textDivision(750,375,125,62,speedFont,speedFontSize)
textDivisionArray.append(speedDivision)
speedDivision.textArray = ['speed: 1x']