

class step:
    pass

class Measurement:
    requires = ()

    def __init__(self, devices):
        for dev in self.requires:
            if dev not in devices:
                raise ValueError('devices must include {}'.format(dev))
        self.devices = devices

    def protocol(self):
        pass

    def start(self):
        pass

    def stop(self):
        pass


class SpectralPowerScan(Measurement):

    requires = ('power_meter', 'monochromator', 'sp_filter_wheel', 'lp_filter_wheel')

    def protocol(self):
        pm = self.devices['power_meter']
        mono = self.devices['monochromator']
        spfw = self.devices['sp_filter_wheel']
