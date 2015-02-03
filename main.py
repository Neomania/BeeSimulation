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
    import pygame, sys, os, random, ui, math, globalcfg
    import pygame.freetype
    from ui import buttonArray, textDivisionArray
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
    scrollSpeed = 5

    #FONTS
    testString = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."

    pygame.freetype.init()

    infoFontSize = 12
    infoFont = pygame.freetype.SysFont('Consolas',infoFontSize)

##    def reduceSpeed():
##        if globalcfg.speedMultiplier > 0:
##            globalcfg.speedMultiplier = globalcfg.speedMultiplier - 1
##    def increaseSpeed():
##        globalcfg.speedMultiplier = globalcfg.speedMultiplier + 1
    #DEFINING UI ELEMENTS
##    buttonArray = []
##    reduceSpeedButton = (ui.Button(750,437,62,63, #SLOWDOWN BUTTON
##    'assets/ui/reduceSpeed.png',reduceSpeed))
##    buttonArray.append(reduceSpeedButton)
##    increaseSpeedButton = (ui.Button(812,437,63,63, #SPEEDUP BUTTON
##    'assets/ui/increaseSpeed.png',increaseSpeed))
##    buttonArray.append(increaseSpeedButton)
##    newFlowerButton = (ui.Button(875,375,125,125, #NEW FLOWER BUTTON
##    'assets/ui/newFlower.png'))
##    buttonArray.append(newFlowerButton)

##    textDivisionArray = []
##    infoBoxDivision = (ui.textDivision(750,0,250,300,infoFont,infoFontSize)) #INFOBOX
##    textDivisionArray.append(infoBoxDivision)
##    infoBoxDivision.textArray = divideStringIntoList(
##    testString,infoBoxDivision.characterWidth)

    while True: #MAIN GAME LOOP
        displaySurface.fill(BLACK)
        mousePos = pygame.mouse.get_pos()

        #PHYSICS, DECISION, ALL NON-UI ACTIONS
        for potato in range(0,globalcfg.speedMultiplier):
            pass
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 4: #MOUSEWHEELUP, SCROLL DOWN
                    for div in textDivisionArray:
                        if div.rect.collidepoint(mousePos) and div.scrollable:
                            div.scrollAmount = div.scrollAmount - scrollSpeed
                elif event.button == 5:#MOUSEWHEELDOWN
                    for div in textDivisionArray:
                        if div.rect.collidepoint(mousePos) and div.scrollable and div.scrollAmount < 0:
                            div.scrollAmount = div.scrollAmount + scrollSpeed
                elif event.button == 1: #LEFT MOUSE CLICK
                    for button in buttonArray:
                        if button.rect.collidepoint(mousePos) and button.clickable:
                            button.proc()
                            ui.speedDivision.textArray = divideStringIntoList(
                            str("speed: " + str(globalcfg.speedMultiplier) + 'x'
                            ),
                            ui.speedDivision.characterWidth)
                            print(ui.speedDivision.textArray)

        #DRAW SIMULATION

        #DRAW BASE UI

        #DRAW TEXT
        for div in ui.textDivisionArray:
            lineNumber = 0
            if div.textArray != None:
                for line in div.textArray:
                    if (lineNumber * (div.fontSize[1] + 8)) + div.scrollAmount >= 0 and (lineNumber * (div.fontSize[1] + 8)) + div.scrollAmount <= div.height:
                        div.font.render_to(displaySurface,(div.xPos,div.yPos + div.scrollAmount + (lineNumber * (div.fontSize[1] + 8))),line,WHITE)
                    else:
                        #print(line)
                        pass
                    lineNumber = lineNumber + 1
            else:
                print("NONE AAA")
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
