from flask import Flask
from filter_wheel import FW102C
import argparse
import sys
app = Flask(__name__)


@app.route('/position/')
@app.route('/position/<int:pos>')
def position(pos=None):
    if pos is None:
        return fwl.query('pos?')
    return fwl.command(f'pos={pos}')

@app.route('/sensors/')
@app.route('/sensors/<int:val>')
def sensors(val=None):
    if val in [0,1]:
        return fwl.command(f'sensors={val}')
    else:
        return fwl.query('sensors?')
        
@app.route('/speed/')
@app.route('/speed/<int:val>')
def speed(val=None):
    if val in [0,1]:
        return fwl.command(f'speed={val}')
    else:
        return fwl.query('speed?')
        

@app.route('/info')
def info():
    return fwl.getinfo()


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
        fwl = FW102C(f'COM{kwargs["com"]}')
        if not fwl.isOpen:
            print( "FWL INIT FAILED")
            sys.exit(2)
        app.run(host=kwargs['ip'], port=kwargs['port'])
    except KeyboardInterrupt:
        pass
    finally:
        if fwl.isOpen:
            fwl.close()