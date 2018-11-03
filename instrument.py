
class Instrument:
    public = ['connected']
    def __init__(self, *args, **kwargs):
        pass

    def connect(self):
        raise NotImplementedError

    def disconnect(self):
        raise NotImplementedError

class EchoInstrument(Instrument):
    public = ['echo','connected']
    connected = True
    _echo = ''
    
    @property
    def echo(self):
        return self._echo

    @echo.setter
    def echo(self, value):
        self._echo = value

    def connect(self):
        pass

    def disconnect(self):
        pass

    
