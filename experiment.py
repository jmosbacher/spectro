from itertools import product
import time
from typing import Iterable, Dict
import json
from collections import defaultdict


class Measurement:
    name = 'measurement'

    def __init__(self, sys_state: dict):
        self.system_state = sys_state

    def perform(self, idx, system, state):
        raise NotImplementedError


class AndorSignal(Measurement):
    #name = 'Andor'

    def perform(self, idx, system, state):
        andor = system.andor
        andor.shutter = 'open'
        andor.running = True
        while andor.running:
            time.sleep(0.5)
        andor.saved = True

class AndorBackground(Measurement):
    #name = 'Andor'

    def perform(self, idx, system, state):
        andor = system.andor
        andor.shutter = 'closed'
        andor.running = True
        while andor.running:
            time.sleep(0.5)
        andor.saved = True

class MeasurementSet(Measurement):

    def __init__(self, sys_state: dict, measurements: Iterable[Measurement]):
        super().__init__(sys_state)
        self.measurements = measurements

    def perform(self, idx, system, state):
        for meas in self.measurements:
            meas.perform(system)
            time.sleep(0.5)

class Protocol:
    def __init__(self, config: dict, changed_only=False):
        self.config = config
        self.changed_only = changed_only

    @classmethod
    def from_config_file(cls, path, changed_only=False):
        import configparser
        config = configparser.ConfigParser()
        config.read(path)
        configs = defaultdict(list)

        for name in config.sections():
            params = dict(config[name])
            name = tuple(name.split('.'))
            t = params.pop('type', 'constant')

            params['values'] = eval(params.pop('values', '[]'))
            configs[t].append((name, params))
        cfg = cls.flatten_configs(configs)
        return cls(cfg, changed_only)

    @staticmethod
    def flatten_configs(configs):
        lists = []
        for (dev, attr), cfg in configs['list']:
            alias = cfg.get("alias", f"{dev}_{attr}")
            l = [(dev, attr, alias, val) for val in cfg['values']]
            lists.append(l)

        mappings = []
        for (dev, attr), cfg in configs['mapping']:
            mapping = {val: cfg[f"{val}"] for val in cfg["values"]}
            alias = cfg.get("alias", f"{dev}_{attr}")
            mappings.append((dev, attr, alias, mapping))

        constants = []
        for (dev,), cfg in configs['constant']:
            cs = [(dev, attr, f"{dev}_{attr}", cfg[f"{attr}"]) for attr in cfg["values"]]
            constants.extend(cs)

        derivations = []
        for (dev,), cfg in configs['derivation']:
            cs = [(dev, attr, f"{dev}_{attr}", cfg[f"{attr}"]) for attr in cfg["values"]]
            derivations.extend(cs)

        config = {"lists": lists, "mappings": mappings,
                  "constants": constants, "derivations": derivations}
        return config

    def __iter__(self):
        state = defaultdict(dict)

        local = {}

        for dev, attr, alias, val in self.config["constants"]:
            state[dev][attr] = val
            # local[alias] = val

        for idx, lparams in enumerate(product(*self.config["lists"])):
            new_state = defaultdict(dict)
            local['state_idx'] = idx
            for (dev, attr, alias, val) in lparams:
                local[alias] = val
                if state[dev].get(attr, None) != val:
                    new_state[dev][attr] = val
                state[dev][attr] = val
            for dev, attr, alias, mapping in self.config['mappings']:
                for val, condition in mapping.items():
                    if eval(condition.format(**local)):
                        if state[dev].get(attr, None) != val:
                            new_state[dev][attr] = val
                        state[dev][attr] = val
                        break
            for dev, attr, alias, expression in self.config['derivations']:
                val = expression.format(**local)
                if state[dev].get(attr, None) != val:
                    new_state[dev][attr] = val
                state[dev][attr] = val
            # state.update(new_state)
            if self.changed_only and idx:
                yield idx, new_state
            else:
                yield idx, state


class Experiment:

    def __init__(self, system, working_dir, protocol,
                 measurements: Iterable[Measurement]):
        self.system = system
        self.wd = working_dir
        self.protocol = protocol
        self.measurements = measurements

    def run(self):
        for idx, state in self.protocol:
            self.system.set_state(state)
            for measurement in self.measurements:
                measurement.perform(idx, self.system, state)





