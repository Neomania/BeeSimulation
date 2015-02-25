#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Timothy
#
# Created:     02/02/2015
# Copyright:   (c) Timothy 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import globalcfg, ui
def reduceSpeed():
    if globalcfg.speedMultiplier > 0:
        globalcfg.speedMultiplier = globalcfg.speedMultiplier - 1
def increaseSpeed():
    globalcfg.speedMultiplier = globalcfg.speedMultiplier + 1
def showDetail():
    print("alksdnmlfks")
    for button in ui.buttonArray:
        button.clickable = False
    ui.detailTextDiv.scrollAmount = 0
    ui.prepareDetail(globalcfg.selectedItem.detailString)
    globalcfg.displayingDetail = True
    for button in ui.detailButtons:
        button.clickable = True
    print("blalh")
def closeDetail():
    print("closed")
    globalcfg.displayingDetail = False
    for button in ui.buttonArray:
        button.clickable = True
    for button in ui.detailButtons:
        button.clickable = False
    for vid in ui.detailElements:
        if type(vid) is ui.Video:
            vid.movie.stop()
    print("dun")
def updateSummary():
    if globalcfg.selectedItem == None:
        ui.infoBoxDivision.textArray = divideStringIntoList("Select something!",
        ui.infoBoxDivision.characterWidth)
    else:
        ui.infoBoxDivision.textArray = divideStringIntoList(
        globalcfg.selectedItem.summaryText,ui.infoBoxDivision.characterWidth)

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

