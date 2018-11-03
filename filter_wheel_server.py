from flask import Flask, url_for
from flask_helpers import site_mapper, RestfulInstrument
from flask_restful import reqparse, abort, Api, Resource
from filter_wheel import FW102C
import argparse
import sys
import redis
app = Flask(__name__)
api = Api(app)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Start a webserver for a Thorlabs FW102C Filter Wheel.')
    parser.add_argument('-NAME', '--NAME', dest='name', default='filter_wheel',
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
    class RestfulFW102C(RestfulInstrument):
        name = kwargs['name']
        api = ['position', 'speed', 'sensors']
        inst = FW102C(f'COM{kwargs["com"]}')

    api.add_resource(RestfulFW102C, f'/{RestfulFW102C.name}/<ep>')

    @app.route(f'/{RestfulFW102C.name}/attributes')
    def attributes():
        return "\n".join(RestfulFW102C.api)
        
    rs = redis.Redis("localhost")
    try:
        app.run(host=kwargs['ip'], port=kwargs['port'])
        rs.set(name, f'{host}:{port}')
    except KeyboardInterrupt:
        pass
    finally:
        if RestfulFW102C.inst.connected:
            RestfulFW102C.inst.disconnect()