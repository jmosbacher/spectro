from itertools import product
import time
from typing import Iterable, Dict


class Measurement:
    name = 'measurement'

    def execute(self, cfg):
        raise NotImplementedError


class Andor(Measurement):
    #name = 'Andor'

    def __init__(self, andor):
        self.andor  = andor

    def execute(self, cfg: dict):
        path = cfg.pop("save_path", f"andor_data_file_{int(time.time())}.asc")
        for k, v in cfg.items():
            setattr(self.andor, k, v)
        self.andor.running = True
        while self.andor.running:
            time.sleep(1)
        self.andor.save_path = path


class Experiment:

    def __init__(self, system, working_dir,
                 states: Iterable[Dict[str, Dict]],
                 configs: Iterable[Dict[str, Dict]],
                 measurements: Iterable[Measurement]):
        self.sys = system
        self.wd = working_dir
        self.states = states
        self.configs = configs
        self.measurements = measurements

    @classmethod
    def from_protocol_file(cls, system, path: str):
        pass

    def run(self, repeats=1):
        state_nums = range(len(self.states))
        for exp_idx, (state_idx, state, measurement), config in product(range(repeats),
                                                         zip(state_nums, self.states, self.configs),
                                                         self.measurements):
            self.sys.set_state(state)
            cfg = {k: v.format(exp_idx=exp_idx, state_idx=state_idx, working_dir=self.wd)
                   for k, v in config[measurement.__class__.__name__].items()}

            measurement.execute(cfg)

