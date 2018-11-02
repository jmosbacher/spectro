# fw102c.py
#
# Thorlabs FW102C - Six-Position Motorized Filter Wheel - Python interface

# Gilles Simond <gilles.simond@unige.ch>	

# who       when        what
# --------  ----------  -------------------------------------------------
# gsimond   20140922    modified from Adrien.Deline version
#

import io,re,sys
import serial

class FW102C:
    """
       Class to control the ThorLabs FW102C filter wheel
       
          fwl = Thorlabs.FW102C(port='COM5')
          fwl.help()
          fwl.command('pos=5')
          fwl.query('pos?')
          fwl.disconnect()
          
       The following table describes all of the available commands and queries:
        *idn?     Get ID: Returns the model number and firmware version
        pos=n     Moves the wheel to filter position n
        pos?      Get current Position
        pcount=n  Set Position Count: Sets the wheel type where n is 6 or 12
        pcount?   Get Position Count: Returns the wheel type
        trig=0    Sets the external trigger to the input mode
        trig=1    Sets the external trigger to the output mode
        trig?     Get current Trigger Mode
        speed=0   Sets the move profile to slow speed
        speed=1   Sets the move profile to high speed
        speed?    Returns the move profile mode
        sensors=0 Sensors turn off when wheel is idle to eliminate stray light
        sensors=1 Sensors remain active
        sensors?  Get current Sensor Mode
        baud=0    Sets the baud rate to 9600
        baud=1    Sets the baud rate to 115200
        baud?     Returns the baud rate where 0 = 9600 and 1 = 115200
        save      This will save all the settings as default on power up
        
    """
    
    
    devInfo  = None

    def __init__(self, port='COM9'):
        self._port = port
        self.connect()
        if self.connectd:
            self._sio.write(u'*idn?\r')
            self.devInfo = self._sio.readlines(2048)[1][:-1]
            print( self.devInfo)
            self._sio.write(u'pos?\r')
            self.pos = self._sio.readlines(2048)[1][:-1]
            print(  'position=',self.pos,)
            self._sio.write(u'pcount?\r')
            self.pcount = self._sio.readlines(2048)[1][:-1]
            print(', pcount=',self.pcount,)
            self._sio.write(u'trig?\r')
            self.trig = self._sio.readlines(2048)[1][:-1]
            print(', trig=',self.trig,)
            self._sio.write(u'speed?\r')
            self.speed = self._sio.readlines(2048)[1][:-1]
            print(', speed=',self.speed,)
            self._sio.write(u'sensors?\r')
            self.sensors = self._sio.readlines(2048)[1][:-1]
            print(', sensors=',self.sensors,)
            self._sio.write(u'baud?\r')
            self.baud = self._sio.readlines(2048)[1][:-1]
            if self.baud: self.baud = 115200
            else: self.baud = 9600
            print(', baud=',self.baud)
            self._sio.flush()
        
    # end def __init__
    
    def help(self):
        print( self.__doc__)

    @property
    def port(self):
        return self._port
    
    @port.setter
    def set_port(self, value):
        self._port = value
        self.connect()

    @property
    def connected(self):
        if self._fw is not None:
            return self._fw.is_open()
        return False

    def connect(self):
        try:
            self._fw = serial.Serial(port=self.port, baudrate=115200,
                                  bytesize=8, parity='N', stopbits=1,
                                  timeout=1, xonxoff=0, rtscts=0)
        except  serial.SerialException as ex:
            print( 'Port {0} is unavailable: {1}'.format(self.port, ex))
            return
        except  OSError as ex:
            print( 'Port {0} is unavailable: {1}'.format(self.port, ex))
            return
        self._sio = io.TextIOWrapper(io.BufferedRWPair(self._fw, self._fw, 1),
                       newline=None, encoding='ascii')

    def disconnect(self):
        if not self.connected:
            print( "Disconnect error: Device not open")
            return "ERROR"
        #end if
        
        self._fw.close()
        return "OK"
    # end def disconnect

    def query(self, cmdstr):
        """
           Send query, get and return answer
        """
        if not self.connected:
            print( "Query error: Device not open")
            return "DEVICE NOT OPEN"
        #end if
        
        ans = 'ERROR'
        self._sio.flush()
        res = self._sio.write(cmdstr+u'\r')
        if res:
            ans = self._sio.readlines(2048)[1][:-1]
        #print 'queryans=',repr(ans)
        return ans
    # end def query

    def command(self, cmdstr):
        """
           Send command, check for error, send query to check and return answer
           If no error, answer value should be equal to command argument value
        """
        if not self.connected:
            print( "Command error: Device not open")
            return "DEVICE NOT OPEN"
        #end if
        
        ans = 'ERROR'
        self._sio.flush()
        cmd = cmdstr.split('=')[0]
        res = self._sio.write(cmdstr+u'\r')
        ans = self._sio.readlines(2048)
        regerr = re.compile("Command error.*")
        errors = [m.group(0) for l in ans for m in [regerr.search(l)] if m]
        #print 'res=',repr(res),'ans=',repr(ans),cmd
        if len(errors) > 0:
            return errors[0]
        ans = self.query(cmd+'?')
        #print 'ans=',repr(ans),cmd+'?'
        return ans
    # end def command

    def getinfo(self):
        if not self.connected:
            print( "Getinfo error: Device not open")
            return "DEVICE NOT OPEN"
        #end if
        
        return self.devInfo

    @property
    def position(self):
        return self.query("pos?")

    @position.setter
    def set_position(self, value):
        self.command(f'pos={value}')
        return self.position

    @property
    def sensors(self):
        return self.query("sensors?")

    @position.setter
    def set_sensors(self, value):
        if value in [0,1]:
            self.command(f'sensors={value}')
        return self.position

    @property
    def speed(self):
        return self.query("speed?")

    @speed.setter
    def set_speed(self, value):
        if value in [0,1]:
            self.command(f'speed={value}')
        return self.speed
    

# Class test, when called directly
if __name__ == "__main__":
    fwl = FW102C(port='COM9')
    if not fwl.connected:
        print( "FWL INIT FAILED")
        sys.exit(2)
    print( '**info',fwl.getinfo())
    print( '**idn?',fwl.query('*idn?'))

    print( '**pos=5',fwl.command('pos=5'))
    print( '**pos?',fwl.query('pos?'))
    print( '**pos=7',fwl.command('pos=7'))
    print( '**pos?',fwl.query('pos?'))
    print( '**pos=3',fwl.command('pos=3'))
    print( '**pos?',fwl.query('pos?'))
    print( '**pos=6',fwl.command('pos=6'))
    print( '**pos?',fwl.query('pos?'))
    print( '**qwzs=3',fwl.command('qwz=3'))
    print( '**pos?',fwl.query('pos?'))
    print(fwl.disconnect())

# oOo
