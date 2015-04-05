#-------------------------------------------------------------------------------
# Name:        sharedfunctions
# Purpose:     Functions which are independent of other modules
#
# Author:      Timothy
#
# Created:     04/04/2015
# Copyright:   (c) Timothy 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
def pointAround(target,radius):
    import random, math
    direction = random.random() * 360
    if type(target) == tuple:
        return(target[0] + (radius * math.cos(direction)),
        target[1] + (radius * math.sin(direction)))
    else:
        return(target.xPos + (radius * math.cos(direction)),
        target.yPos + (radius * math.sin(direction)))