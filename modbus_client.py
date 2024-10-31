#!/usr/bin/env python3

""" Read 10 coils and print result on stdout. """

import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(3, GPIO.OUT)

from pyModbusTCP.client import ModbusClient

# init modbus client
c = ModbusClient(host='100.71.6.22', port=12345, auto_open=True)

# main read loop
while True:
    # read 10 bits (= coils) at address 0, store result in coils list
    coils_l = c.read_coils(0, 10)

    # if success display registers
    if coils_l:
        if coils_l[0] == True:
            GPIO.output(3,GPIO.HIGH)
        else:
            GPIO.output(3,GPIO.LOW)
        print('coil ad #0 to 9: %s' % coils_l)
    else:
        print('unable to read coils')

    # sleep 2s before next polling
    time.sleep(2)
