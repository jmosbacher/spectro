from serial.rs485 import RS485
from helpers import find_instrument

class Energetiq:


    def power(self):
        self.conn.write(b'Q')
        res = self.conn.read(1024)

    def __init__(self, port=None):
        if port is None:
            port = find_instrument()
        self.port = port
        
    def __enter__(self):
        self.conn = RS485(self.port, baudrate=9600, timeout=1)

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()

