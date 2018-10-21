import serial

class CM112:
    def __init__(self, port):
        self.port = port
        
    def __enter__(self):
        self.conn = serial.Serial(self.port, baudrate=115200, timeout=1)

    def __exit__(self, exc_type, exc_value, traceback):
        pass