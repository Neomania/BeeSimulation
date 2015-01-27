#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Timothy
#
# Created:     22/1/2015
# Copyright:   (c) Timothy 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def main():
    import pygame, sys, os, random, ui, math
    import pygame.freetype
    clock = pygame.time.Clock()
    pygame.init()
    FPS = 60
    DEVPINK = (255,0,255)
    RED = (255,0,0)
    GREEN = (0,255,0)
    BLUE = (0,0,255)
    YELLOW = (0,255,255)
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    mousePos = (0,0)
    displaySurface = pygame.display.set_mode((1000,750))
    speedMultiplier = 1 #SPECIFIES HOW MANY TIMES THE PHYSICS LOOP RUNS

    #FONTS
    testString = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."

    pygame.freetype.init()
    infoFontSize = 12
    infoFont = pygame.freetype.SysFont('Consolas',infoFontSize)

    def reduceSpeed():
        if speedMultiplier > 0:
            speedMultiplier = speedMultiplier - 1
    def increaseSpeed():
        speedMultiplier = speedMultiplier + 1
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

    #DEFINING UI ELEMENTS
    buttonArray = []
    buttonArray.append(ui.Button(750,437,62,63, #SLOWDOWN BUTTON
    'assets/ui/reduceSpeed.png',reduceSpeed))
    buttonArray.append(ui.Button(812,437,63,63, #SPEEDUP BUTTON
    'assets/ui/increaseSpeed.png',increaseSpeed))
    buttonArray.append(ui.Button(875,375,125,125, #NEW FLOWER BUTTON
    'assets/ui/newFlower.png'))

    textDivisionArray = []
    infoBoxDivision = (ui.textDivision(750,0,250,300,infoFont,infoFontSize)) #INFOBOX
    textDivisionArray.append(infoBoxDivision)
    print(infoBoxDivision.characterWidth)
    infoBoxDivision.textArray = divideStringIntoList(
    testString,infoBoxDivision.characterWidth)


    while True: #MAIN GAME LOOP
        displaySurface.fill(BLACK)
        mousePos = pygame.mouse.get_pos()

        #PHYSICS, DECISION, ALL NON-UI ACTIONS
        for potato in range(0,speedMultiplier):
            pass
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        #DRAW SIMULATION

        #DRAW BASE UI

        #DRAW TEXT
        for div in textDivisionArray:
            lineNumber = 0
            for line in div.textArray:
                div.font.render_to(displaySurface,(div.xPos,div.yPos + (lineNumber * (div.fontSize[1] + 8))),line,WHITE)
                lineNumber = lineNumber + 1
        #DRAW BUTTONS
        for button in buttonArray:
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
        pygame.display.update()
        clock.tick(FPS)

if __name__ == '__main__':
    from pygame.locals import *
    main()
