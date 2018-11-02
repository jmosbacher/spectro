from flask import Flask
from spectral_products import CM112
import argparse
import sys
app = Flask(__name__)


@app.route('/wavelength/')
@app.route('/wavelength/<int:wl>')
def wavelength(wl=None):
    if wl is None:
        return mono.get_wavelength()
    return mono.set_wavelength(wl)

@app.route('/grating/')
@app.route('/grating/<int:gr>')
def grating(gr=None):
    if gr is None:
        return mono.get_grating()
    return mono.set_grating(gr)

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
        mono = CM112(f'COM{kwargs["com"]}')
        mono.connect()
        if not mono.isOpen():
            print( "MONOCHROMATOR INIT FAILED")
            sys.exit(2)
        app.run(host=kwargs['ip'], port=kwargs['port'])
    except KeyboardInterrupt:
        pass
    finally:
        if mono.isOpen:
            mono.disconnect()