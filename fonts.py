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
infoFontSize = 12
infoFont = pygame.freetype.SysFont('Consolas',infoFontSize)
speedFontSize = 26
speedFont = pygame.freetype.SysFont('Helvetica',speedFontSize)
detailedFontSize = 12
detailedFont = pygame.freetype.SysFont('Consolas',detailedFontSize)
pollenRateFontSize = 16
pollenRateFont = pygame.freetype.SysFont('Consolas',pollenRateFontSize)