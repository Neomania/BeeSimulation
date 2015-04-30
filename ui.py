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
class ExpandingCircle:
    def __init__(self,colour,xPos,yPos,timeToLive=20,lineWidth=1):
        self.colour = colour
        self.timeToLive = timeToLive
        self.timeLived = 3
        self.xPos = xPos
        self.yPos = yPos
        self.lineWidth = 1
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
    def __init__(self,xPos,yPos,width,height,fontToUse,fontSize,scrollable = False,colour = (255,255,255)):
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
        self.colour = colour
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
        preElementString,detailTextDiv.characterWidth)

def updateDetail(): #[expletive] past timothy comment on your code more
    if globalcfg.selectedItem == None:
        pass
    else:
        prepareDetail(globalcfg.selectedItem.detailString)

expandingCircleArray = []

baseUI = pygame.image.load('assets/ui/baseui.png')

buttonArray = []
reduceSpeedButton = (Button(750,437,62,63, #SLOWDOWN BUTTON
'assets/ui/reduceSpeed.png',reduceSpeed))
buttonArray.append(reduceSpeedButton)
increaseSpeedButton = (Button(812,437,63,63, #SPEEDUP BUTTON
'assets/ui/increaseSpeed.png',increaseSpeed))
buttonArray.append(increaseSpeedButton)
newFlowerButton = (Button(875,375,125,125, #NEW FLOWER BUTTON
'assets/ui/newFlower.png',toggleFlower))
buttonArray.append(newFlowerButton)
showDetailButton = (Button(975,275,25,25,
'assets/ui/showDetail.png',showDetail))
buttonArray.append(showDetailButton)
selectNextButton = (Button(950,275,25,25,
'assets/ui/rightArrow.png',selectNext))
buttonArray.append(selectNextButton)
selectPrevButton = (Button(750,275,25,25,
'assets/ui/leftArrow.png',selectPrev))
buttonArray.append(selectPrevButton)
increasePollenRateButton = Button(750,550,50,25,
'assets/ui/increasePollenRate.png',increaseFlowerRate)
buttonArray.append(increasePollenRateButton)
decreasePollenRateButton = Button(750,575,50,25,
'assets/ui/decreasePollenRate.png',decreaseFlowerRate)
buttonArray.append(decreasePollenRateButton)
addBeeButton = Button(750,700,50,25,'assets/ui/addBee.png',addBee)
buttonArray.append(addBeeButton)
removeBeeButton = Button(750,725,50,25,'assets/ui/removeBee.png',removeBee)
buttonArray.append(removeBeeButton)

#Flower colour buttons
redButton = Button(750,600,50,50,'assets/ui/redButton.png',changeFlowerColour,
(242,87,70))
orangeButton = Button(800,600,50,50,'assets/ui/orangeButton.png',changeFlowerColour,
(242,173,70))
yellowButton = Button(850,600,50,50,'assets/ui/yellowButton.png',changeFlowerColour,
(242,239,70))
greenButton = Button(900,600,50,50,'assets/ui/greenButton.png',changeFlowerColour,
(179,242,70))
blueButton = Button(950,600,50,50,'assets/ui/blueButton.png',changeFlowerColour,
(70,173,242))
purpleButton = Button(750,650,50,50,'assets/ui/purpleButton.png',changeFlowerColour,
(171,70,242))
pinkButton = Button(800,650,50,50,'assets/ui/pinkButton.png',changeFlowerColour,
(255,128,255))
brownButton = Button(850,650,50,50,'assets/ui/brownButton.png',changeFlowerColour,
(179,80,15))
whiteButton = Button(900,650,50,50,'assets/ui/whiteButton.png',changeFlowerColour,
(255,255,255))
greyButton = Button(950,650,50,50,'assets/ui/greyButton.png',changeFlowerColour,
(125,125,125))

buttonArray.append(redButton)
buttonArray.append(orangeButton)
buttonArray.append(yellowButton)
buttonArray.append(greenButton)
buttonArray.append(blueButton)
buttonArray.append(purpleButton)
buttonArray.append(pinkButton)
buttonArray.append(brownButton)
buttonArray.append(whiteButton)
buttonArray.append(greyButton)


textDivisionArray = []

infoBoxDivision = (textDivision(760,5,230,295,infoFont,infoFontSize,False)) #INFOBOX
textDivisionArray.append(infoBoxDivision)
infoBoxDivision.textArray = divideStringIntoList(
testString,infoBoxDivision.characterWidth)

selectionInfoDivision = textDivision(760,310,240,70,selectionFont,
selectionFontSize,False)
textDivisionArray.append(selectionInfoDivision)

speedDivision = textDivision(755,400,125,62,speedFont,speedFontSize)
textDivisionArray.append(speedDivision)
speedDivision.textArray = ['speed: 1x']

flowerPlacingDivision = textDivision(950,515,50,50,pollenRateFont,
pollenRateFontSize)
textDivisionArray.append(flowerPlacingDivision)
flowerPlacingDivision.textArray = ["No"]

pollenRateDivision = textDivision(950,573,50,50,pollenRateFont,
pollenRateFontSize) #displays pollen rate for created flowers
textDivisionArray.append(pollenRateDivision)
pollenRateDivision.textArray = [str(round(globalcfg.createdFlowerRate,1))]

beeCountDivision = textDivision(920,720,80,25,speedFont,speedFontSize)
textDivisionArray.append(beeCountDivision)
beeCountDivision.textArray = [str(globalcfg.beeCount)]

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

def updateSummary():
    if globalcfg.selectedItem == None and globalcfg.flowerPlacing == False:
        infoBoxDivision.textArray = divideStringIntoList("Click and drag to select bees, or click once to select other objects!",
        infoBoxDivision.characterWidth)
        showDetailButton.clickable = False
    elif globalcfg.flowerPlacing:
        infoBoxDivision.textArray = divideStringIntoList("Now placing a flower, selection disabled",
        infoBoxDivision.characterWidth)
        showDetailButton.clickable = False
    else:
        infoBoxDivision.textArray = divideStringIntoList(
        globalcfg.selectedItem.summaryText,infoBoxDivision.characterWidth)
        showDetailButton.clickable = True
def updateSelection():#called each frame, gives technical info on selected item
    import physics
    if globalcfg.selectedItem == None:
        selectionInfoDivision.textArray = []
    else:
        selectionInfoDivision.textArray = []
        selectionType = type(globalcfg.selectedItem)
        if selectionType == physics.Bee:
            if globalcfg.selectedItem.state == "Foraging randomly":
                selectionInfoDivision.textArray.append("Just looking around.")
            elif globalcfg.selectedItem.state == "Searching local area":
                selectionInfoDivision.textArray.append("Looking near the hive.")
            elif globalcfg.selectedItem.state == "Attending dance" or (
            globalcfg.selectedItem.state == "Moving to dance floor"):
                selectionInfoDivision.textArray.append("Watching a dance!")
            elif globalcfg.selectedItem.state == "Moving to known food source":
                selectionInfoDivision.textArray.append(
                "Going to a known food source")
            elif globalcfg.selectedItem.state == "Harvesting pollen":
                selectionInfoDivision.textArray.append("Harvesting from a flower")
            elif globalcfg.selectedItem.state == "Preparing to dance":
                selectionInfoDivision.textArray.append("Getting her dance on")
            elif globalcfg.selectedItem.state == "Performing round dance":
                selectionInfoDivision.textArray.append("Food source nearby!")
            elif globalcfg.selectedItem.state == "Performing waggle dance":
                selectionInfoDivision.textArray.append("Food source over there!")
            elif globalcfg.selectedItem.state == "Returning to hive":
                selectionInfoDivision.textArray.append("Going home")
            elif globalcfg.selectedItem.state == "Idle":
                selectionInfoDivision.textArray.append("Lazing around")
            elif globalcfg.selectedItem.state == "Moving to flower":
                selectionInfoDivision.textArray.append("Landing on a flower")
            selectionInfoDivision.textArray.append("Memories: " + str(len(
            globalcfg.selectedItem.memoryStore)))
            selectionInfoDivision.textArray.append(
            "Flowers visited this flight: " + str(
            len(globalcfg.selectedItem.visitedFlowers)))
        elif selectionType == physics.Flower:
            if globalcfg.selectedItem.occupied:
                selectionInfoDivision.textArray.append("Catering to a bee")
            else:
                selectionInfoDivision.textArray.append("Not being bugged")
            selectionInfoDivision.textArray.append("Pollen rate: " + str(
            globalcfg.selectedItem.pollenRate))
        elif selectionType == physics.DanceFloor:
            if globalcfg.selectedItem.occupied:
                selectionInfoDivision.textArray.append("Someone's dancing here!")
                selectionInfoDivision.textArray.append("Number of attending bees: "
                + str(len(globalcfg.selectedItem.beesOnFloor)))
            else:
                selectionInfoDivision.textArray.append("Nothing happening here.")
        elif selectionType == physics.Hive:
            selectionInfoDivision.textArray.append("The hive!")
