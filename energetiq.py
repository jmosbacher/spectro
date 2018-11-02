from serial.rs485 import RS485
import time
class Energetiq:
    def query(self, q):
        self.conn.write(q.encode())
        res = self.conn.readlines(2048)[-1].strip()
        return res.split(b' = ')[-1].decode()

    def get_power(self):
        return self.query('Q')

    def set_power(self, pwr):
        pwr = int(pwr)
        if pwr>100 or pwr<15:
            return 'Requested power out of range 15-100'
        
        while True:
            p = self.get_power()
            if p==pwr:
                return f'Power now at {pwr}%'
            elif p>pwr:
                self.query('D')
            elif p<pwr:
                self.query('U')
            time.sleep(0.2)
        
    def connect(self):
        self.conn = RS485(self.port, baudrate=9600, timeout=1)

    def isOpen(self):
        if self.conn:
            return self.conn.is_open()
        return False

    def disconnect(self):
        if self.conn and self.conn.is_open():
            self.conn.close()

    def __init__(self, port='COM1'):
        self.port = port
        
    def __enter__(self):
        self.connect()

    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()

if __name__ == '__main__':
    with Energetiq('COM8') as en:
        print(en.get_power())