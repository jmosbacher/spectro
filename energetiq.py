from serial.rs485 import RS485

class Energetiq:
    def query(self, q):
        self.conn.write(q.encode())
        res = self.conn.read(2048).strip()
        return res.split(b' = ')[-1].decode()

    def get_power(self):
        return self.query('Q')

    def set_power(self, pwr):
        pwr = int(pwr)
        if pwr>100 or pwr<15:
            return 'Requested power out of range 15-100%'
        
        while True:
            p = self.get_power()
            if p==pwr:
                return f'Power now at {pwr}%'
            elif p>pwr:
                self.query('D')
            elif p<pwr:
                self.query('U')
        

    def __init__(self, port='COM1'):
        self.port = port
        
    def __enter__(self):
        self.conn = RS485(self.port, baudrate=9600, timeout=1)

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()

if __name__ == '__main__':
    with Energetiq('COM8') as en:
        print(en.get_power())