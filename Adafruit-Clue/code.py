# SPDX-FileCopyrightText: 2019 Kattni Rembor, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
from adafruit_clue import clue
import board
import displayio
from adafruit_display_shapes.circle import Circle
import supervisor


clue.sea_level_pressure = 1020

display = board.DISPLAY
clue_group = displayio.Group(max_size=4)

outer_circle = Circle(120, 120, 119, outline=clue.WHITE)
middle_circle = Circle(120, 120, 75, outline=clue.YELLOW)
inner_circle = Circle(120, 120, 35, outline=clue.GREEN)
clue_group.append(outer_circle)
clue_group.append(middle_circle)
clue_group.append(inner_circle)

x, y, _ = clue.acceleration
bubble_group = displayio.Group(max_size=1)
level_bubble = Circle(int(x + 120), int(y + 120), 20, fill=clue.RED, outline=clue.RED)
bubble_group.append(level_bubble)

clue_group.append(bubble_group)
display.show(clue_group)

lastProx = clue.proximity


while True:

    x, y, _ = clue.acceleration
    bubble_group.x = int(x * -10)
    bubble_group.y = int(y * -10)

    # Check for proximity conditions
    prox = clue.proximity
    if prox > lastProx:
        print("!P: {}".format(prox))
        if prox > 5:
            clue.start_tone(800)
    lastProx = prox
    if prox == 0:
        clue.stop_tone()

    # Check for queries from serial
    if supervisor.runtime.serial_bytes_available:
        value = input().strip()

        # Sometimes Windows sends an extra (or missing) newline - ignore them
        if value == "":
            continue

        # This is a bit brute force, but it's simple to follow, so we've left it like that.
        if value == 'a':
            print("a: {:.2f} {:.2f} {:.2f}".format(*clue.acceleration))
        elif value == 'aX':
            print("aX: {:.2f}".format(clue.acceleration[0]))
        elif value == 'aY':
            print("aY: {:.2f}".format(clue.acceleration[1]))
        elif value == 'aZ':
            print("aZ: {:.2f}".format(clue.acceleration[2]))
        elif value == 'g':
            print("G: {:.2f} {:.2f} {:.2f}".format(*clue.gyro))
        elif value == 'gX':
            print("gX: {:.2f}".format(clue.gyro[0]))
        elif value == 'gY':
            print("gY: {:.2f}".format(clue.gyro[1]))
        elif value == 'gZ':
            print("gZ: {:.2f}".format(clue.gyro[2]))
        elif value == 'm':
            print("M: {:.3f} {:.3f} {:.3f}".format(*clue.magnetic))
        elif value == 'mX':
            print("mX: {:.2f}".format(clue.magnetic[0]))
        elif value == 'mY':
            print("mY: {:.2f}".format(clue.magnetic[1]))
        elif value == 'mZ':
            print("mZ: {:.2f}".format(clue.magnetic[2]))
        elif value == 'p':
            print("P: {}".format(clue.proximity))
        elif value == 'l1':
            clue.white_leds = True
        elif value == 'l0':
            clue.white_leds = False

