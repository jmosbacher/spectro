import serial
import struct

class CM112:
    @staticmethod
    def wl_to_bytes(wl):
        a = wl*10.
        high = int(a/256)
        low = int(a - high*256)
        return high, low

    @staticmethod
    def encode(*args):
        return b''.join([struct.pack('B',arg) for arg in args])

    def query(self, *args):
        msg = self.encode(*args)
        self.conn.write(msg)
        return self.conn.read(1024)
        
    def get_wavelength(self):
        h,l = self.query(56,0)
        return (h*256+l)/10
        

    def set_wavelength(self, wl):
        high, low = self.wl_to_bytes(wl)     #Set monochromator to wl
        self.conn.write(self.encode(16, high, low))

    def __init__(self, port):
        self.port = port
        
    def __enter__(self):
        self.conn = serial.Serial(self.port, baudrate=9600, timeout=1)

    def __exit__(self, exc_type, exc_value, traceback):
        pass