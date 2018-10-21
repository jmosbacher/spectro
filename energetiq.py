from serial.rs485 import RS485

class Energetiq:

    def __init__(self, port):
        self.port = port
        
    def __enter__(self):
        self.conn = RS485(self.port, baudrate=115200, timeout=1)

    def __exit__(self, exc_type, exc_value, traceback):
        pass

