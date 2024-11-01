#!/usr/bin/env python3

from multiprocessing import Process, Value
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)

from pyModbusTCP.client import ModbusClient


def read_regs():    
    # main read loop
    while True:
        coils_l = c.read_coils(0, 15)
        # if success display registers
        if coils_l:
            if coils_l[0] == True:
                # red light on
                GPIO.output(17,GPIO.HIGH)
            else:
                GPIO.output(17,GPIO.LOW)
            if coils_l[1] == True:
                # yellow light on
                GPIO.output(27,GPIO.HIGH)
            else:
                GPIO.output(27,GPIO.LOW)
            if coils_l[2] == True:
                # green light on
                GPIO.output(22,GPIO.HIGH)
            else:
                GPIO.output(22,GPIO.LOW)
        else:
            print('unable to read coils')

        # sleep 2s before next polling
        time.sleep(0.1)


if __name__ == "__main__":
    # init modbus client
    c = ModbusClient(host='100.71.6.22', port=502, auto_open=True)
    read_regs()
    
