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
    import pygame
    pygame.init()
    import sys, os, random, ui, math, globalcfg, fonts
    import pygame.freetype
    from ui import buttonArray, textDivisionArray, baseUI#, detailSurface, ui.detailTextDiv,ui.detailElements
    clock = pygame.time.Clock()
    FPS = 60
    DEVPINK = (255,0,255)
    RED = (255,0,0)
    GREEN = (0,255,0)
    BLUE = (0,0,255)
    YELLOW = (0,255,255)
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    mousePos = (0,0)
    displaySurface = pygame.display.set_mode(
    (globalcfg.windowWidth,globalcfg.windowHeight))
    scrollSpeed = 5
    globalcfg.displayingDetail = True #DENOTES IF GAME IS DISPLAYING DETAIL PANEL

    #PHYSICS
    simHeight = 750
    simWidth = 750
    simSurface = pygame.Surface((simWidth,simHeight))
    beeArray = []
    flowerArray = []
    danceFloorArray = []

    danceFloorArray.append(DanceFloor(40,0))
    danceFloorArray.append(DanceFloor(-40,0))

    hiveArray = [] #in the odd case that we eventually add more hives

    home = Hive(0.0,0.0)
    hiveArray.append(home)

    #FONTS
    testString = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."

    pygame.freetype.init()

    infoFontSize = 12
    infoFont = pygame.freetype.SysFont('Consolas',infoFontSize)
    beeArray.append(Bee(home))

    def flipBoolean():
        globalcfg.displayingDetail = False
    selectedItem = None
    detailOverlay = pygame.image.load('assets/ui/detailoverlay.png')
    detailButtons = [ui.Button(725,0,25,25,'assets/ui/closeDetail.png',flipBoolean),
                    ui.Button(700,0,25,25,'assets/ui/refreshDetail.png',ui.prepareDetail,open("testdetail.txt").read())]
    for button in detailButtons:
        button.clickable = globalcfg.displayingDetail

    while True: #MAIN GAME LOOP
        displaySurface.fill(BLACK)
        ui.detailSurface.fill(BLACK)
        mousePos = pygame.mouse.get_pos()

        #PHYSICS, DECISION, ALL NON-UI ACTIONS
        if globalcfg.displayingDetail == False:
            for potato in range(0,globalcfg.speedMultiplier):
                for bee in beeArray:
                    bee.updatePosition()

        #USER INPUT HANDLING
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 5: #MOUSEWHEELDOWN
                    for div in textDivisionArray:
                        if div.rect.collidepoint(mousePos) and div.scrollable:
                            div.scrollAmount = div.scrollAmount - scrollSpeed
                elif event.button == 4:#MOUSEWHEELUP
                    for div in textDivisionArray:
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
                    for button in buttonArray + detailButtons:
                        if button.rect.collidepoint(mousePos) and button.clickable:
                            button.proc()
                            ui.speedDivision.textArray = ui.divideStringIntoList(
                            str("speed: " + str(globalcfg.speedMultiplier) + 'x'
                            ),ui.speedDivision.characterWidth)
                            print(ui.speedDivision.textArray)

        #DRAW SIMULATION
        simSurface.fill(BLACK)
        for hive in hiveArray:
            #DRAW HIVE
            pygame.draw.circle(simSurface,(125,125,0),
            (round(hive.xPos + (simWidth / 2)),
            round(hive.yPos + (simHeight/2))),hive.radius)
        for danceFloor in danceFloorArray:
            #DRAW DANCE FLOORS
            pygame.draw.circle(simSurface,(200,200,0),
            (round(danceFloor.xPos + (simWidth/2)),
            round(danceFloor.yPos + (simHeight/2))),danceFloor.radius)
            #DRAW BEES
        for bee in beeArray:
            pygame.draw.circle(simSurface,(255,255,0),
            (round(bee.xPos + (simWidth/2)),round(bee.yPos + (simHeight/2))
            ),2)
        #APPLY SIMSURFACE TO DISPLAY SURFACE
        displaySurface.blit(simSurface,(0,0))
        #DRAW BASE UI
        displaySurface.blit(baseUI,(0,0))
        #DETAIL BITS
        if globalcfg.displayingDetail == True:
            #DRAW DETAIL BASE
            ui.detailSurface.fill(BLACK)
            lineNumber = 0
            for element in ui.detailElements:
                if type(element) is str:
                    if 25 + (lineNumber * (ui.detailTextDiv.fontSize[1] +
                    ui.detailTextDiv.lineSpace)) + ui.detailTextDiv.scrollAmount >= 0:
                        fonts.detailedFont.render_to(
                        ui.detailSurface,
                        (0,25 + (lineNumber * (ui.detailTextDiv.fontSize[1] +
                         ui.detailTextDiv.lineSpace)) + ui.detailTextDiv.scrollAmount)
                         ,element,WHITE)
                    lineNumber = lineNumber + 1
                elif type(element) is ui.Video:
                    ui.detailSurface.blit(element.movieSurface,(element.rect.left,25 + (lineNumber * (ui.detailTextDiv.fontSize[1] +
                     ui.detailTextDiv.lineSpace)) + ui.detailTextDiv.scrollAmount))
                elif type(element) is ui.Image:
                    ui.detailSurface.blit(element.imageSurface,(0,25 + (lineNumber * (ui.detailTextDiv.fontSize[1] +
                     ui.detailTextDiv.lineSpace)) + ui.detailTextDiv.scrollAmount))
            displaySurface.blit(ui.detailSurface,(25,0))
            displaySurface.blit(detailOverlay,(0,0))
            for button in detailButtons:
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
    from physics import *
    main()