import numpy as np
from scipy.optimize import curve_fit
import datetime
import pandas as pd
import os
import time


class RamanScan:
    def __init__(self, system, working_folder):
        self.mono = system.mono
        self.spectro = system.spectro
        self.spf = system.spf
        self.lpf = system.lpf
        self.flipper = system.flipper
        self.working_folder = working_folder
        self.spectrum_file_format = '{date}_ID{ID}_ExWl_{wl}.asc'

    def scan(self, ID, mn, mx, stp, use_lpf=True, use_spf=True):
        now = datetime.datetime.now()
        date = str(now.day) + str(now.month) + str(now.year - 2000)

        # Defining intresting parameters
        self.mono.grating = 1
        wlrange = np.arange(mn, mx, stp)
        self.spf.position = 6
        self.lpf.position = 6
        self.flipper.position = 'down'
        pwr_avgs = []
        pwr_stds = []
        # Take measurments and save in ascii files
        for wl in wlrange:
            print("Excitation wl: ", wl, " Raman shift: ", self.ramanshift(wl, 3400))
            if use_spf:
                self.set_spf(wl)
            if use_lpf:
                self.set_lpf(wl)

            if (wl > 370):
                self.flipper.position = 'down'
            if (wl > 400):
                self.mono.grating = 2
            self.mono.wavelength = wl

            self.spectro.running = True
            power = []
            while self.spectro.running:
                power.append(self.pm.measure_power(wl))
            print(f'I measured {len(power)} power samples')

            path = os.path.join(self.working_folder, self.spectrum_file_template.format(date=date, ID=ID, wl=wl))
            self.spectro.save = path

            time.sleep(5.)
            pwr_avgs.append(np.mean(power))
            pwr_stds.append(np.std(power))

        data = {
            'ex_wl': wlrange,
            'em_wl': self.ramanshift(wlrange, 3400),
            'ex_pwr': pwr_avgs,
            'ex_pwr_std': pwr_stds,

        }
        return pd.DataFrame(data)

    def process(self, df, ID):

        df = df.copy()
        area = []
        now = datetime.datetime.now()
        date = str(now.day) + str(now.month) + str(now.year - 2000)
        for wl in df['ex_wl']:
            try:
                path = os.path.join(self.working_folder, self.spectrum_file_template.format(date=date, ID=ID, wl=wl))
                gassianArea = self.RamanGaussFit(path, wl)
            except RuntimeError:
                gassianArea = np.nan
            area.append(gassianArea)
        print(area)
        df['peak_area'] = area
        df['rel_eff'] = self.rel_eff(df["ex_wl"], df["ex_pwr"], df["peak_area"])
        return df

    def set_spf(self, wl):
        if (wl < 400):
            self.spf.position = 6
            print("self.spf is in posiotion 6 Empty")
        if (wl > 400) & (wl < 440):
            self.spf.position = 1
            print("self.spf is in posiotion 1 Wavlength 450")
        if (wl > 440) & (wl < 490):
            self.spf.position = 2
            print("self.spf is in posiotion 2 Wavlength 500")
        if (wl > 490) & (wl < 540):
            self.spf.position = 3
            print("self.spf is in posiotion 3 Wavlength 550")
        if (wl > 540) & (wl < 590):
            self.spf.position = 4
            print("self.spf is in posiotion 4 Wavlength 600")
        if (wl > 590) & (wl < 640):
            self.spf.position = 5
            print("self.spf is in posiotion 5 Wavlength 650")
        if (wl > 640):
            self.spf.position = 6
            print("self.spf is in posiotion 6 Empty")

    def set_lpf(self, wl):
        wlshift = self.ramanshift(wl, 3400)
        wlshift = 0  # In case you do not want any self.lpf
        if (wlshift < 420):
            self.lpf.position = 6
            print("self.lpf is in posiotion 6 Empty")
        if (wlshift > 420) & (wlshift < 470):
            self.lpf.position = 1
            print("self.lpf is in posiotion 1 Wavlength  400")
        if (wlshift > 470) & (wlshift < 520):
            self.lpf.position = 2
            print("self.lpf is in posiotion 2 Wavlength 450")
        if (wlshift > 520) & (wlshift < 570):
            self.lpf.position = 3
            print("self.lpf is in posiotion 3 Wavlength 500")
        if (wlshift > 570) & (wlshift < 620):
            self.lpf.position = 4
            print("self.lpf is in posiotion 4 Wavlength  550")
        if (wlshift > 620):
            self.lpf.position = 5
            print("self.lpf is in posiotion 4 Wavlength  600")

    @staticmethod
    def ramanshift(wl, shift):  # Expected position of peak
        wl = np.array(wl)
        shift = np.array(shift)
        return 1 / ((1 / wl - shift * 10 ** (-7)))  # shift is in cm^-1 units for water shift = 3400 cm^-1

    @staticmethod
    def gauss(x, a, x0, sigma, m, b):  # Gaussian to fit
        return a * np.exp(-(x - x0) ** 2 / (2 * sigma**2)) + m * x + b

    def RamanGaussFit(self, file, ex_wl):
        wl, count = np.genfromtxt(file, skip_footer=32, delimiter="\t").T
        wlmin, wlshift, wlmax = self.ramanshift(ex_wl, [2000., 3400, 4500]) # These are specific shifts for water
#        wlmin2, wlshift2, wlmax2 = self.ramanshift(ex_wl, [500., 3400, 7000]),  # These are specific shifts for water

        temp = wlmax > wl
        wl = wl[temp]
        count = count[temp]
        temp = wl > wlmin
        wl = wl[temp]
        count = count[temp]
        dwl = np.diff(wl).mean()
        std_est = np.sqrt(np.sum((count/np.sum(count)*(wl - wlshift)**2)))
        p0 = [np.max(count), wlshift, std_est , 0., np.min(count)]
        popt, pcov = curve_fit(self.gauss, wl, count, p0=p0)  # fit to gaussian
        return popt[0] * np.sqrt(popt[2]**2 * 2 * 3.14159)

    @staticmethod
    def raman_cs(wl):
        """
            Water Raman Cross Section
        """
        wl = wl * 10 ** (-7)  # Convert to cm
        vp = 1 / wl  # Frequency
        lams = 1 / ((1 / wl - 3400))  # Wl of Raman
        vs = 1 / lams  # Frequency of Raman
        vi = 88000
        res = vs ** 4 / ((vi ** 2 - vp ** 2) ** 2)  # number of expected photons
        return res

    def rel_eff(self, wl, p , area):
        photin = (p * wl * 10 ** (-9)) / (6.63 * 10 ** (-34) * 299792458)
        photout = area
        return photout / (photin * self.raman_cs(wl))