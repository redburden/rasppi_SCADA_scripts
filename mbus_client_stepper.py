#!/usr/bin/env python3

""" Read 10 coils and print result on stdout. """

import time
import board
from adafruit_motorkit import MotorKit
from pyModbusTCP.client import ModbusClient

# init modbus client
c = ModbusClient(host='100.71.6.22', port=12345, auto_open=True)

MOTOR_ON = False

# main read loop
while True:
    # read 10 bits (= coils) at address 0, store result in coils list
    coils_l = c.read_coils(0, 10)
    # read 16 holding registers
    motor_h_regs = c.read_h_regs(0,15)

    # if success display registers
    if coils_l:
        if coils_l[0] == True:
            MOTOR_ON = True
        else:
            MOTOR_ON = False
    else:
        print('unable to read coils')

    # sleep 2s before next polling
    time.sleep(2)

# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""Simple test for using adafruit_motorkit with a stepper motor"""


kit = MotorKit(i2c=board.I2C())

while MOTOR_ON == True:
    kit.stepper1.onestep()
    time.sleep(0.01)


