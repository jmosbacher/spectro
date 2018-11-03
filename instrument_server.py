from flask import Flask, url_for
from flask_helpers import site_mapper
from flask_restful import reqparse, abort, Api, Resource
import argparse
import sys
import redis
rparser = reqparse.RequestParser()
rparser.add_argument('value')

class InstrumentServer:

    def __init__(self, name, host, port, instrument):
        self.name = name
        self.host = host
        self.port = port
        self.instrument = instrument

    def run(self):
        app = Flask(__name__)
        api = Api(app)
        class RestfulInstrument(Resource):
            
            inst = self.instrument
            
            
            def get(self, ep):
                if ep in self.inst.public:
                    resp = getattr(self.inst, ep)
                else:
                    resp = f'No attribute named {ep}'
                return {ep: resp}
                
            def put(self, ep):
                if ep in self.inst.public:
                    args = rparser.parse_args()
                    val = args['value']
                    try:
                        setattr(self.inst, ep, val)
                        resp = f'{ep} is now {getattr(self.inst, ep)}'
                    except:
                        resp = f'{ep} is not writable.'
                else:
                    resp = f'No attribute named {ep}'        
                return {ep: resp}, 201

        api.add_resource(RestfulInstrument, f'/{self.name}/<ep>')

        @app.route(f'/{self.name}/attributes')
        def attributes():
            return "\n".join(RestfulInstrument.inst.public)
        rs = redis.Redis("localhost")
        try:
            app.run(host=self.host, port=self.port, debug=True)
            rs.set(self.name, f'{self.host}:{self.port}')
        except KeyboardInterrupt:
            pass
        finally:
            if RestfulInstrument.inst.connected:
                RestfulInstrument.inst.disconnect()
            rs.delete(self.name)
