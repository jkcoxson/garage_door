# Jackson Coxson

import requests

class Yeeter:
    def __init__(self, endpoint):
        self.endpoint = endpoint
    
    def updateCurrentState(self, value):
        """Updates Homebridge's door state. Values 0 - 3 are valid."""
        requests.get(self.endpoint + "/currentDoorState?value=" + str(value))

    def updateTargetState(self, value):
        """Updates Homebridge's target state. Values 0 - 1 are valid."""
        requests.get(self.endpoint + "/targetDoorState?value=" + str(value))

    def updateObstructionDetected(self, value):
        """Updates Homebridge's obstruction detected state. 1 means obstruction detected."""
        requests.get(self.endpoint + "/obstructionDetected?value=" + str(value))