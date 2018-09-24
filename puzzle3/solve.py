#!/usr/bin/env python3

from pyautogui import *
from time import sleep
from itertools import product

color = (0x27, 0xae, 0x60)

sleep(5)

res = (800, 600)
samplePitch = 20
greyTolerance = 10

overview = screenshot()

xStart = 99999
xEnd = 0
yStart = 99999
yEnd = 0

for y in range(0, res[1], samplePitch):
    for x in range(0, res[0], samplePitch):
        if overview.getpixel((x, y)) == color:
            xStart = min(x, xStart)
            xEnd = max(x, xEnd)
            yStart = min(y, yStart)
            yEnd = max(y, yEnd)

xEnd += 1
yEnd += 1

print("Found:", xStart, yStart, xEnd, yEnd)

for _ in range(1100):
    print("shot")
    shot = screenshot()
    print("search")
    for y, x in product(range(yStart, yEnd, samplePitch), range(xStart, xEnd, samplePitch)):
            r, g, b = shot.getpixel((x, y))
            if abs(r - g) <= greyTolerance and \
               abs(r - g) <= greyTolerance and \
               abs(r - g) <= greyTolerance:
                print("click")
                click(x, y)
                break


