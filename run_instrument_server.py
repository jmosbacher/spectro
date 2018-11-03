import argparse
from filter_wheel import FW102C
from instrument_server import InstrumentServer
from instrument import EchoInstrument

devices = {'Echo':EchoInstrument,
}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Start an instrument webserver.')
    parser.add_argument('-DEVICE', '--DEVICE', dest='device', default='Echo',
                help='Device to control.')
    parser.add_argument('-NAME', '--NAME', dest='name', default='echo_chamber',
                help='Device name, must be unique.')
    parser.add_argument('-COM', '--COM', dest='com', default=1,type=int,
                help='Serial port.')
    parser.add_argument('-HOST','--HOST',dest='host',default='localhost',
                help='IP to serve on.')
    parser.add_argument('-PORT','--PORT',dest='port', type=int, default=5000,
            help='Port to open.')
    kwargs = vars(parser.parse_args())
    device = kwargs['device']
    name = kwargs['name']
    host = kwargs['host']
    port = kwargs['port']
    com = kwargs['com']
    instrument = devices[device](f'COM{com}')
    server = InstrumentServer(name, host, port, instrument)
    server.run()