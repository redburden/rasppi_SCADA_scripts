# Run motor on GPIO 26
import RPi.GPIO as GPI

GPIO.setup(26, GPIO.OUT) 

for i in range(10000):
	GPIO.output(26,GPIO.HIGH)
        time.sleep(0.007)
        GPIO.output(26,GPIO.LOW)
