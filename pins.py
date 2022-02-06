# Jackson Coxson

import RPi.GPIO as GPIO
from time import sleep
import threading


class PinClass:
    def __init__(self, in_pin, out_pin):
        # Initialize the GPIO pins
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(out_pin, GPIO.OUT, initial=GPIO.HIGH)
        self.in_pin = in_pin
        self.out_pin = out_pin
    
    def press(self):
        threading.Thread(target=self.__press).start()

    def __press(self):
        print("Press thread started")
        GPIO.output(self.out_pin, GPIO.LOW)
        sleep(0.3)
        GPIO.output(self.out_pin, GPIO.HIGH)

    def reed_switch(self) -> bool:
        return GPIO.input(self.in_pin) == GPIO.HIGH
