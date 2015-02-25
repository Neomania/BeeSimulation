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

DEVPINK = (255,0,255)
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
        testCharacter = fontToUse.render('abcdefghijklmnopqrstuvwxyz',(255,255,255))
        self.fontSize = (round((testCharacter[0].get_width()/26))
        ,testCharacter[0].get_height())
        self.characterWidth = math.floor(self.width / (self.fontSize[0])) #rough height
        self.lineSpace = 0 #round(self.fontSize[1]/1.2) #no longer needed
class Image:
    def __init__(self,filepath,width,height,fontHeightAndSpacing):
        import pygame,math
        self.imageSurface = pygame.image.load(filepath)
        self.width = width
        self.height = height
        self.characterHeight = math.ceil(self.height / fontHeightAndSpacing)
class Video:
    import pygame
    def __init__(self,filepath,width,height,fontHeightAndSpacing,lineNumber):
        import pygame, math
        pygame.mixer.quit() #TEMPORARY: NEEDED FOR AUDIO TO WORK ON TEST
        self.rect = pygame.Rect(round((700-width)/2)
        ,lineNumber * fontHeightAndSpacing,width,height)
        self.fontHeightAndSpacing = fontHeightAndSpacing
        self.lineNumber = lineNumber
        self.filepath = filepath
        self.movie = pygame.movie.Movie(filepath)
        self.movieSurface = pygame.Surface((width,height))
        self.movie.set_display(self.movieSurface)
        self.width = width
        self.height = height
        self.characterHeight = math.ceil(self.height / fontHeightAndSpacing)
    def play(self):
        import pygame
        #pygame.mixer.init()
        self.movie = pygame.movie.Movie(self.filepath)
        self.movie.set_display(self.movieSurface)
        self.movie.play()
def prepareDetail(detailString): #parses detail string into elements
    global detailElements
    detailElements = []
    preElementString = ""
    imageString = ""
    videoString = ""
    filePath = ""
    workingString = ""
    mode = "normal"
    eleWidth = 0
    eleHeight = 0
    for i in range(0,len(detailString)):
        if detailString[i] == "#":
            if mode == "image":
                #PROCESS IMAGE STRING
                mode = "normal"
                workingChar = 0
                workingString = ""
                filePath = ""
                while imageString[workingChar] != ",":
                    filePath = filePath + imageString[workingChar]
                    workingChar = workingChar + 1
                workingChar = workingChar + 1
                while imageString[workingChar] != ",":
                    workingString = workingString + imageString[workingChar]
                    workingChar = workingChar + 1
                eleWidth = int(workingString)
                workingChar = workingChar + 1
                eleHeight = int(imageString[workingChar:])
                detailElements.append(Image(filePath,eleWidth,eleHeight,
                detailTextDiv.fontSize[1] + detailTextDiv.lineSpace))
                for k in range(0,detailElements[len(detailElements) - 1].characterHeight):
                    preElementString = preElementString + "@"
            elif mode == "normal":
                detailElements = detailElements + divideStringIntoList(
                preElementString,detailTextDiv.characterWidth)
                preElementString = ""
                mode = "image"
                imageString = ""
        elif detailString[i] == "^":
            if mode == "video":
                #PROCESS VIDEO STRING
                mode = "normal"
                workingChar = 0
                workingString = ""
                filePath = ""
                while videoString[workingChar] != ",":
                    filePath = filePath + videoString[workingChar]
                    workingChar = workingChar + 1
                workingChar = workingChar + 1
                while videoString[workingChar] != ",":
                    workingString = workingString + videoString[workingChar]
                    workingChar = workingChar + 1
                eleWidth = int(workingString)
                workingChar = workingChar + 1
                eleHeight = int(videoString[workingChar:])
                detailElements.append(Video(filePath,eleWidth,eleHeight,
                detailTextDiv.fontSize[1] + detailTextDiv.lineSpace,len(detailElements))) #len(detailElements) passes line number
                for k in range(0,detailElements[len(detailElements) - 1].characterHeight):
                    preElementString = preElementString + "@"
            elif mode == "normal":
                detailElements = detailElements + divideStringIntoList(
                preElementString,detailTextDiv.characterWidth)
                preElementString = ""
                mode = "video"
                videoString = ""
        else:
            if mode == "image":
                imageString = imageString + detailString[i]
            elif mode == "video":
                videoString = videoString + detailString[i]
            else:
                preElementString = preElementString + detailString[i]
    if mode == "normal":
        detailElements = detailElements + divideStringIntoList(
        preElementString,700)

def updateDetail(): #dammit past timothy comment on your code more
    if globalcfg.selectedItem == None:
        pass
    else:
        prepareDetail(globalcfg.selectedItem.detailString)
    print(textDivisionArray)

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
showDetailButton = (Button(975,275,25,25,
'assets/ui/showDetail.png',showDetail))
buttonArray.append(showDetailButton)

textDivisionArray = []

infoBoxDivision = (textDivision(760,0,240,300,infoFont,infoFontSize,True)) #INFOBOX
textDivisionArray.append(infoBoxDivision)
infoBoxDivision.textArray = divideStringIntoList(
testString,infoBoxDivision.characterWidth)

speedDivision = textDivision(750,375,125,62,speedFont,speedFontSize)
textDivisionArray.append(speedDivision)
speedDivision.textArray = ['speed: 1x']

#DETAILS
detailSurface = pygame.Surface((700,750))
detailTextDiv = textDivision(25,0,700,750,detailedFont,detailedFontSize,True)
detailElements = []
detailSurface.set_colorkey((1,1,1))
detailButtons = [Button(725,0,25,25,'assets/ui/closeDetail.png',closeDetail),
                Button(700,0,25,25,'assets/ui/refreshDetail.png',updateDetail)]


#DEBUG
textDivisionArray.append(detailTextDiv)
prepareDetail(open("assets/summary/bee.txt","r").read())
print(detailElements)

def updateSummary():
    if globalcfg.selectedItem == None:
        infoBoxDivision.textArray = divideStringIntoList("Select something!",
        infoBoxDivision.characterWidth)
        showDetailButton.clickable = False
    else:
        infoBoxDivision.textArray = divideStringIntoList(
        globalcfg.selectedItem.summaryText,infoBoxDivision.characterWidth)
        showDetailButton.clickable = True