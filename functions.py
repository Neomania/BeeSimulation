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
import globalcfg
def reduceSpeed():
    if globalcfg.speedMultiplier > 0:
        globalcfg.speedMultiplier = globalcfg.speedMultiplier - 1
def increaseSpeed():
    globalcfg.speedMultiplier = globalcfg.speedMultiplier + 1

if __name__ == '__main__':
    main()
