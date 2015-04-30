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
import pygame
import pygame.freetype
pygame.freetype.init()
infoFontSize = 18
infoFont = pygame.freetype.SysFont('Consolas',infoFontSize)
selectionFontSize = 12
selectionFont = pygame.freetype.SysFont('Consolas',selectionFontSize)
speedFontSize = 20
speedFont = pygame.freetype.SysFont('Consolas',speedFontSize)
detailedFontSize = 20
detailedFont = pygame.freetype.SysFont('Consolas',detailedFontSize)
pollenRateFontSize = 16
pollenRateFont = pygame.freetype.SysFont('Consolas',pollenRateFontSize)