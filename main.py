# Jackson Coxson
# Howard Crawford

from http.server import BaseHTTPRequestHandler, HTTPServer
from pins import PinClass
import garage as grg
from yeet import Yeeter


PORT = 3030
pins = PinClass(27, 17)
yeeter = Yeeter('http://192.168.1.37:2000')
garage = grg.garage(pins, yeeter)

class handler(BaseHTTPRequestHandler):
    def do_GET(self):

        # Check if the request is from Homebridge
        print("Recieved request from {}".format(self.client_address[0]))
        if not self.client_address[0] == "192.168.1.37":
            return
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Close the door
        if self.path == '/setTargetDoorState?value=1':
            print("Received request to close the garage")
            garage.close()
            self.wfile.write(bytes("Closing", "utf-8"))
            return
        
        # Open the door
        elif self.path == '/setTargetDoorState?value=0':
            print("Received request to open the garage")
            garage.open()
            self.wfile.write(bytes("Opening", "utf-8"))
            return

        elif self.path == '/status':
            message = '{"currentDoorState":' + str(garage.currentDoorState) + ',"targetDoorState":' + str(garage.targetDoorState) + '}'
            self.wfile.write(bytes(message, "utf8"))



# Start the server, listening for Homebridge requests
with HTTPServer(('0.0.0.0', 3030), handler) as server:
    server.serve_forever()
