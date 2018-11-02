import serial
import struct
import time


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
        return self.conn.read(2048)
    
    def home(self):
        self.query(255,255,255)

    def get_wavelength(self):
        h,l = self.query(56,0)
        return (h*256+l)/10
        
    def set_wavelength(self, wl):
        high, low = self.wl_to_bytes(wl)  #Set monochromator to wl
        while True:
            cwl = self.get_wavelength()
            if abs(wl - cwl)<1:
                return 
            else:
                self.query(16, high, low)
                time.sleep(0.5)

    def get_grating(self):
        h,l = self.query(56,4)
        return l

    def set_grating(self,gr):
        if gr not in [1,2]:
            return 'Invalid grating number (must be 1 or 2)'
        while True:
            if self.get_grating()==gr:
                break
            else:
                self.query(26,gr)
                time.sleep(4)

    def connect(self):
        self.conn  = serial.Serial(self.port, baudrate=9600, timeout=1)

    def isOpen(self):
        if self.conn:
            return self.conn.is_open()
        return False

    def disconnect(self):
        if self.conn and self.conn.is_open():
            self.conn.close()

    def __init__(self, port):
        self.port = port
        
    def __enter__(self):
        self.connect()

    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()