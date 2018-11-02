from flask import Flask
from energetiq import Energetiq
import argparse
import sys
app = Flask(__name__)


@app.route('/power/')
@app.route('/power/<int:pwr>')
def position(pwr=None):
    if pwr is None:
        return en.get_power()
    return en.set_power(pwr)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Start a webserver for a Thorlabs FW102C Filter Wheel.')
    parser.add_argument('-COM', '--COM', dest='com', default='',
                help='Serial port for filter wheel.')
    parser.add_argument('-IP','--IP',dest='ip',default='localhost',
                help='IP to serve on.')
    parser.add_argument('-PORT','--PORT',dest='port', type=int, default=5000,
            help='Port to open.')
    kwargs = vars(parser.parse_args())
    try:
        en = Energetiq(f'COM{kwargs["com"]}')
        en.connect()
        if not en.isOpen:
            print( "SOURCE INIT FAILED")
            sys.exit(2)
        app.run(host=kwargs['ip'], port=kwargs['port'])
    except KeyboardInterrupt:
        pass
    finally:
        if en.isOpen:
            en.disconnect()