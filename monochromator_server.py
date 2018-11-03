from flask import Flask, url_for
from flask_helpers import site_mapper, RestfulInstrument
from flask_restful import reqparse, abort, Api, Resource
from spectral_products import CM112
import argparse
import sys
import redis
app = Flask(__name__)
api = Api(app)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Start a webserver for a Spectral Products Monochromator.')
    parser.add_argument('-NAME', '--NAME', dest='name', default='monochromator',
                help='Serial port for filter wheel.')
    parser.add_argument('-COM', '--COM', dest='com', default=1,
                help='Serial port for filter wheel.')
    parser.add_argument('-IP','--IP',dest='ip',default='localhost',
                help='IP to serve on.')
    parser.add_argument('-PORT','--PORT',dest='port', type=int, default=5000,
            help='Port to open.')
    kwargs = vars(parser.parse_args())
    name = kwargs['name']
    host = kwargs['ip']
    port = kwargs['port']
    class RestfulCM112(RestfulInstrument):
        api = ['wavelength', 'grating', 'port']
        inst = CM112(f'COM{kwargs["com"]}')

    api.add_resource(RestfulCM112, f'/{name}/<ep>')
    @app.route(f'/{name}/attributes')
    def attributes():
        return "\n".join(RestfulCM112.api)
    rs = redis.Redis("localhost")
    try:
        app.run(host=host, port=port)
        rs.set(name, f'{host}:{port}')
    except KeyboardInterrupt:
        pass
    finally:
        if RestfulCM112.inst.connected:
            RestfulCM112.inst.disconnect()
        rs.set(name, '')