from flask import url_for

from flask_restful import reqparse, abort, Api, Resource

class RestfulInstrument(Resource):
        name = 'instrument'
        api = []
        inst = None

        def get(self, ep):
            if ep in self.api:
                resp = getattr(self.inst, ep)
            else:
                f'No attribute named {ep}'
            return {ep: resp}
            
        def put(self, ep):
            if ep in self.api:
                args = rparser.parse_args()
                setattr(self.inst, ep, args['value'])
                resp = getattr(self.inst, ep)
            else:
                f'No attribute named {ep}'        
            return {ep: resp}

def site_mapper(app, path):
    def has_no_empty_params(rule):
        defaults = rule.defaults if rule.defaults is not None else ()
        arguments = rule.arguments if rule.arguments is not None else ()
        return len(defaults) >= len(arguments)
    @app.route(path)
    def site_map():
        links = []
        for rule in app.url_map.iter_rules():

            # Filter out rules we can't navigate to in a browser
                # and rules that require parameters
            if "GET" in rule.methods and has_no_empty_params(rule):
                url = url_for(rule.endpoint, **(rule.defaults or {}))
                links.append((url, rule.endpoint))
        return  "\n".join([f"{l}" for l in links])
    

        # links is now a list of url, endpoint tuples