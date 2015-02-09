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

testString = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In efficitur malesuada felis, in pharetra tellus vehicula gravida. Fusce sed interdum lorem. Nam facilisis ex nunc, vitae suscipit libero faucibus nec. Pellentesque mollis laoreet elit, eu pulvinar mauris mattis vitae. Quisque sapien diam, pretium ut posuere non, elementum a ante. Cras a feugiat mauris. Vestibulum ornare nibh sit amet magna accumsan ullamcorper. Donec faucibus ex non viverra suscipit. Sed ut turpis id arcu convallis elementum. Praesent non hendrerit metus, consectetur placerat leo. Duis elementum enim eu nisi porttitor, in rutrum diam finibus. Suspendisse et mi vitae lacus molestie vulputate. Nam id turpis aliquam, porttitor sapien sed, dictum augue. Sed placerat ante leo, quis vulputate metus scelerisque quis. Quisque urna massa, blandit eget lobortis et, fermentum quis augue. Etiam eget nunc efficitur, pretium elit nec, consectetur diam. Praesent risus urna, venenatis id orci at, scelerisque pharetra elit. Donec consequat tellus quis lacus varius, vel cursus nisi porttitor. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae"

def divideStringIntoList(stringToDivide,lineLength): #@ is a line break
    stringLength = len(stringToDivide) - 1
    spacePointer = 0
    endOfLastLinePointer = 0
    currentPointer = 0
    charactersSoFar = 0
    returnList = []

    while currentPointer < stringLength:
        charactersSoFar = 0
        while charactersSoFar < lineLength and currentPointer < stringLength and stringToDivide[currentPointer] != '@':
            if stringToDivide[currentPointer] == ' ':
                spacePointer = currentPointer
            currentPointer = currentPointer + 1
            charactersSoFar = charactersSoFar + 1
        if currentPointer < stringLength and stringToDivide[currentPointer] != '@': #checks why it exited the loop
            returnList.append(
            stringToDivide[endOfLastLinePointer:spacePointer])
            currentPointer = spacePointer + 1
            endOfLastLinePointer = currentPointer
        elif stringToDivide[currentPointer] == '@':
            returnList.append(
            stringToDivide[endOfLastLinePointer:currentPointer])
            currentPointer = currentPointer + 1
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
        self.lineSpace = round(self.fontSize[1]/1.2)
class Video:
    import pygame
    def __init__(self,filepath,width,height,fontHeightAndSpacing):
        import pygame, math
        self.movie = pygame.movie.Movie(filepath)
        self.movieSurface = pygame.Surface((width,height))
        self.movie.set_display(self.movieSurface)
        self.width = width
        self.height = height
        self.characterHeight = math.ceil(self.height / fontHeightAndSpacing)

def prepareDetail(detailString): #parses detail string into elements
    global detailElements
    detailElements = []
    for i in range(0,len(detailString)):
        pass


baseUI = pygame.image.load('assets/ui/baseui.png')

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

#DETAILS
detailSurface = pygame.Surface((750,750))
detailTextDiv = ui.textDivision(25,0,700,700,detailedFont,detailedFontSize,True)
detailElements = []