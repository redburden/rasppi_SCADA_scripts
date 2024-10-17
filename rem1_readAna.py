import time
import board
from digitalio import DigitalInOut, Direction
from collections import deque

RCpin = board.D18
samples = deque([0]*1000)

while True:
    with DigitalInOut(RCpin) as rc:
        reading = 0

        # setup pin as output and direction low value
        rc.direction = Direction.OUTPUT
        rc.value = False

        # setup pin as input and wait for low value
        rc.direction = Direction.INPUT

        # This takes about 1 millisecond per loop cycle
        while rc.value is False:
            reading += 1
        # Keep a moving average based on the last 10 readings
        # Write that moving average to ana_value.txt
        samples.pop()
        samples.appendleft(reading)

        reading = sum(samples) / len(samples)
        reading /= 430
        reading = round(reading, 2)
        reading *= 100

        if reading > 100:
            reading = 100
        else:
            reading = int(reading)
        print(reading)
        f = open("ana_value.txt", "w")
        f.write(str(reading))
        f.close()