#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Timothy
#
# Created:     26/04/2015
# Copyright:   (c) Timothy 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from physics import *

testHive = Hive(0,0)
testBee = Bee(testHive)

testFlower1 = Flower(0,0,(0,0,0),1.0)
testFlower2 = Flower(0,0,(0,0,0),2.0)
testFlower3 = Flower(0,0,(0,0,0),3.0)
testFlower4 = Flower(0,0,(0,0,0),4.0)
testFlower5 = Flower(0,0,(0,0,0),5.0)
testBee.createMemoryAbout(testFlower4)
testBee.createMemoryAbout(testFlower2)
testBee.createMemoryAbout(testFlower3)
testBee.createMemoryAbout(testFlower5)
testBee.createMemoryAbout(testFlower1)
for memory in testBee.memoryStore:
    print(memory.flower.pollenRate)

print("Sorting!")
testBee.sortMemory()

for memory in testBee.memoryStore:
    print(memory.flower.pollenRate)