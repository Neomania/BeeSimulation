#-------------------------------------------------------------------------------
# Name:        main
# Purpose:
#
# Author:      Timothy
#
# Created:     20/01/2015
# Copyright:   (c) Timothy 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def main():
    import pygame, sys, os, random, ui
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
    mainSurface = pygame.display.set_mode((1366,768))
    def pause():
        print("paws")
    pause()
    playButton = ui.Button(50,50,50,50,'playbutton.png')

    while True:
        mainSurface.fill(BLACK)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONUP:
                if playButton.rect.collidepoint(pygame.mouse.get_pos()):
                    playButton.proc()
        if playButton.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                mainSurface.blit(playButton.spriteSheet,playButton.rect,playButton.clickedRect)
            else:
                mainSurface.blit(playButton.spriteSheet,playButton.rect,playButton.mouseOverRect)
        else:
            mainSurface.blit(playButton.spriteSheet,playButton.rect,playButton.neutralRect)

        pygame.display.update()
        clock.tick(FPS)

if __name__ == '__main__':
    from pygame.locals import *
    main()
