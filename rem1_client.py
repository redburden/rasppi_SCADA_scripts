#!/usr/bin/env python3

""" Read 10 coils and print result on stdout. """
from multiprocessing import Process, Queue
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(3, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)

from pyModbusTCP.client import ModbusClient

<<<<<<< HEAD

def run_M1(pulse_time, m1_command):
    while True:
        # print(str(m1_command.value))
        while m1_command.value > 0:
            GPIO.output(26,GPIO.HIGH)
            time.sleep(pulse_time.value)
            GPIO.output(26,GPIO.LOW)

def read_regs(m1_speed, m1_command, pulse_time):
    # main read loop
    m1_hand_speed = 0
=======
# init modbus client
c = ModbusClient(host='100.107.143.47', port=502, auto_open=True)
m1_speed = 0
m1_hand_speed = 0
m1_run_cmd = False
m1_q = Queue()

def run_M1(q):
    while m1_run_cmd:
        # if there is something in the queue, pull it
        if not q.empty():
            m1_run_data = q.get()
            m1_run_cmd = m1_run_data[0]
        GPIO.output(26,GPIO.HIGH)
        time.sleep(m1_run_data[1])
        GPIO.output(26,GPIO.LOW)
    GPIO.output(26,GPIO.LOW)
    return 0

if __name__ == '__main__':    
    # main read loop
    p = Process(target=run_M1, args=(m1_q,))
>>>>>>> a3f31f4ba54c1d1d467732321875177fa64318d8
    while True:
        # read 10 bits (= coils) at address 0, store result in coils list
        coils_l = c.read_coils(0, 15)
        c.write_single_register(3, m1_speed)
        m1_remote_speed = c.read_holding_registers(0, 1)[0]
<<<<<<< HEAD

        try:
            # Read an analog value written to ana_val.txt
            with open('ana_value.txt', 'r') as f:
                m1_hand_speed = int(f.read())
        except:
            pass
        else:
            f.close()
        
        print(m1_hand_speed)

=======
        try:
            # Read an analog value written to ana_val.txt
            with open('ana_val.txt', 'r') as f:
                m1_hand_speed = int(f.read())
        except:
            m1_hand_speed = 0
        else:
            f.close()
>>>>>>> a3f31f4ba54c1d1d467732321875177fa64318d8
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
<<<<<<< HEAD
                if coils_l[11] == False:
                    # Test if m1_remote_speed is different from m1_speed by more than 5
                    if m1_remote_speed == 0:
                        m1_command.value = 0
                        
                    elif abs(m1_remote_speed - m1_speed) > 1:
                        m1_speed = m1_remote_speed
                        pulse_time.value = 0.004 + (100/m1_speed) * 0.001
                        m1_command.value = 1
                    
                    else:
                        m1_command.value = 1
                else:
                    if m1_hand_speed == 0:
                        m1_command.value = 0

                    elif abs(m1_hand_speed - m1_speed) > 1:
                        m1_speed = m1_hand_speed
                        pulse_time.value = 0.004 + (100/m1_speed) * 0.001
                        m1_command.value = 1
                        
                    else:
                        m1_command.value = 1
            else:
                # print("Motor is being told to stop.")
                m1_command.value = 0            
                GPIO.output(26,GPIO.LOW)
        else:
            print('unable to read coils')

        # sleep 2s before next polling
        time.sleep(0.1)


if __name__ == "__main__":
    pulse_time = Value('d',0)
    m1_command = Value('i',0)
    # init modbus client
    c = ModbusClient(host='100.107.143.47', port=502, auto_open=True)
    m1_speed = 0
    p = Process(target=run_M1, args=(pulse_time, m1_command,))
    p2 = Process(target=read_regs, args=(m1_speed, m1_command, pulse_time,))
    
    
    
    p.start()
    p2.start()
=======
                print(coils_l[10], coils_l[11], m1_speed, m1_remote_speed, m1_hand_speed)
                if coils_l[11] == False:
                    if m1_remote_speed == 0:
                        GPIO.output(26,GPIO.LOW)
                        while not m1_q.empty():
                            m1_q.get()
                        m1_q.put([False, 0])                           
                    elif abs(m1_remote_speed - m1_speed) > 1:
                        m1_speed = m1_remote_speed
                        pulse_time = 0.004 + (100/m1_speed) * 0.001
                        m1_q.put([True, pulse_time])
                        if not p.is_alive():
                            p.start()
                            p.join()
                else:
                    if m1_hand_speed == 0:
                        GPIO.output(26,GPIO.LOW)
                        while not m1_q.empty():
                            m1_q.get()
                        m1_q.put([False, 0])   
                    elif abs(m1_hand_speed - m1_speed) > 1:
                        m1_speed = m1_hand_speed
                        0.004 + (100/m1_speed) * 0.001
                        m1_q.put([True, pulse_time])
                        if not p.is_alive():
                            p.start()
                            p.join()
            else:
                m1_speed = 0
                print("Motor is being told to stop.")                
                GPIO.output(26,GPIO.LOW)
                while not m1_q.empty():
                    m1_q.get()
                m1_q.put([False, 0])
        else:
            print('unable to read coils')
        time.sleep(0.1)
>>>>>>> a3f31f4ba54c1d1d467732321875177fa64318d8
