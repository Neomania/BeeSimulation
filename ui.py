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

def main():
    pass
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

    def __init__(self,xPos,yPos,width,height,spriteImage,procCall = None):
        import pygame
        self.rect = pygame.Rect(xPos,yPos,width,height)
        self.clickable = True
        self.procCall = procCall
        self.spriteSheet = pygame.image.load(spriteImage)
        self.neutralRect = pygame.Rect(0,0,width,height)
        self.mouseOverRect = pygame.Rect(width,0,width,height)
        self.clickedRect = pygame.Rect(2*width,0,width,height)
        self.unclickableRect = pygame.Rect(3*width,0,width,height)
    def proc(self):
        if self.procCall == None:
            print("No procedure specified")
        else:
            self.procCall()
class textDivision:
    import pygame
    import pygame.freetype
    rect = pygame.Rect
    def __init__(self,xPos,yPos,width,height,fontToUse,fontSize):
        import pygame, math
        import pygame.freetype
        self.xPos = xPos
        self.yPos = yPos
        self.width = width
        self.height = height
        self.textArray = []
        self.font = fontToUse
        testCharacter = fontToUse.render('a',(255,255,255))
        self.fontSize = (testCharacter[0].get_width()
        + round(testCharacter[0].get_width() / 10)
        ,testCharacter[0].get_height())
        self.characterWidth = math.floor(self.width / (self.fontSize[0])) #rough height



if __name__ == '__main__':
    main()
