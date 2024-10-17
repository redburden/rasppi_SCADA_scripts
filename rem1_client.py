#!/usr/bin/env python3

""" Read 10 coils and print result on stdout. """
from multiprocessing import Process, Value, Array
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(3, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)

from pyModbusTCP.client import ModbusClient

# init modbus client
c = ModbusClient(host='100.107.143.47', port=502, auto_open=True)
m1_speed = 0
m1_hand_speed = 0
pulse_time = 0


def run_M1(pulse_time):
    while True:
        GPIO.output(26,GPIO.HIGH)
        time.sleep(pulse_time)
        GPIO.output(26,GPIO.LOW)

def m1_proc():
    if p.is_alive() == True:
        p.terminate()
        p.start()
        p.join()
    else:
        p.start()
        p.join()

# main read loop
while True:
    # read 10 bits (= coils) at address 0, store result in coils list
    coils_l = c.read_coils(0, 15)
    c.write_single_register(3, m1_speed)
    m1_remote_speed = c.read_holding_registers(0, 1)
    p = Process(target=run_M1, args=(pulse_time,))

    try:
        # Read an analog value written to ana_val.txt
        with open('ana_val.txt', 'r') as f:
            m1_speed = int(f.read())
    except:
        m1_speed = 0
    else:
        f.close()

    # if success display registers
    if coils_l:
        if coils_l[0] == True:
            GPIO.output(3,GPIO.HIGH)
        else:
            GPIO.output(3,GPIO.LOW)
        if coils_l[1] == True:
            GPIO.output(17,GPIO.HIGH)
        else:
            GPIO.output(17,GPIO.LOW)
        if coils_l[2] == True:
            GPIO.output(27,GPIO.HIGH)
        else:
            GPIO.output(27,GPIO.LOW)
        if coils_l[10] == True:
            if coils_l[11] == False:
                # Test if m1_remote_speed is different from m1_speed by more than 5
                if m1_remote_speed == 0:
                    if p.is_alive() == True:
                        p.terminate()
                elif abs(m1_remote_speed - m1_speed) > 1:
                    m1_speed = m1_remote_speed
                    pulse_time = 0.004 + (100/m1_speed) * 0.001
                    m1_proc()
            else:
                if m1_hand_speed == 0:
                    if p.is_alive() == True:
                        p.terminate()
                elif abs(m1_hand_speed - m1_speed) > 1:
                    m1_speed = m1_hand_speed
                    0.004 + (100/m1_speed) * 0.001
                    m1_proc()
        else:
            if p.is_alive() == True:
                p.terminate()            
        
    else:
        print('unable to read coils')

    # sleep 2s before next polling
    time.sleep(0.1)
