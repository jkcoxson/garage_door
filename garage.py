# Jackson Coxson
from pins import PinClass
from time import sleep
import threading

from yeet import Yeeter

# 0 Open
# 1 Closed
# 2 Opening
# 3 Closing

class garage:
    def __init__(self, pins: PinClass, yeeter: Yeeter):
        self.pins = pins
        if pins.reed_switch():
            self.currentDoorState = 0
        else:
            self.currentDoorState = 1
        self.targetDoorState = 1
        self.obstructionDetected = 0
        self.yeeter = yeeter
        self.background_refresh()
        

    def open(self):
        self.yeeter.updateObstructionDetected(0)
        # Check to make sure the garage is closed
        if not self.pins.reed_switch():
            print("Garage closed, proceeding to open")
            self.currentDoorState = 2
            self.targetDoorState = 0

            self.pins.press()

            self.yeeter.updateTargetState(1)
            self.yeeter.updateCurrentState(2)
            self.open_timer()
        else:
            print("Garage is already open, aborting")
            self.yeeter.updateCurrentState(0)

    def close(self):
        self.yeeter.updateObstructionDetected(0)
        # Check to make sure the garage is open
        if self.pins.reed_switch():
            print("Garage open, proceeding to close")
            self.currentDoorState = 3
            self.targetDoorState = 1
            self.pins.press()
            self.yeeter.updateTargetState(0)
            self.yeeter.updateCurrentState(3)
            self.obstruction_detection()
        else:
            print("Garage is already closed, aborting")
            self.yeeter.updateCurrentState(1)

    def obstruction_detection(self):
        threading.Thread(target=self.__obstruction_detection).start()
        
    def __obstruction_detection(self):
        sleep(13)
        if self.pins.reed_switch():
            self.obstructionDetected = 1
            self.yeeter.updateObstructionDetected(1)
            self.yeeter.updateCurrentState(0)
            self.yeeter.updateTargetState(0)
            self.currentDoorState = 0
            self.targetDoorState = 0
            self.danger_timeout()

        else:
            self.obstructionDetected = 0
            self.currentDoorState = 1
            self.yeeter.updateObstructionDetected(0)
            self.yeeter.updateCurrentState(1)

    def danger_timeout(self):
        """Automatically remove the warning for obstruction detection after 120 seconds.
        There is no better way to do this because there is only one sensor on the top."""
        threading.Thread(target=self.__danger_timeout).start()
    
    def __danger_timeout(self):
        sleep(120)
        self.yeeter.updateObstructionDetected(0)

    def open_timer(self):
        threading.Thread(target=self.__open_timer).start()

    def __open_timer(self):
        while True:
            i = 0
            sleep(1)
            if self.pins.reed_switch():
                self.yeeter.updateCurrentState(0)
                break
            elif i == 30:
                self.yeeter.updateCurrentState(1)

    def background_refresh(self):
        threading.Thread(target=self.__background_refresh).start()

    def __background_refresh(self):
        while True:
            sleep(1)
            if self.currentDoorState == 1:
                if self.pins.reed_switch():
                    self.yeeter.updateCurrentState(0)
                    self.yeeter.updateTargetState(0)
                    self.currentDoorState = 0
            elif self.currentDoorState == 0:
                if not self.pins.reed_switch():
                    self.yeeter.updateCurrentState(1)
                    self.yeeter.updateTargetState(1)
                    self.currentDoorState = 1
