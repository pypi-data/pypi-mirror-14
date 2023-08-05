#!/usr/bin/env python

import metcalcs as met_calcs
import metcalc_gui as gui
import sys

if sys.version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk

__author__ = 'Mark Baker  email: mark.baker@metoffice.gov.uk'


class Model:
    """Perform meteorological calculations calling methods contained within the 'metcalcs' module."""
    def __init__(self):
        self.qnh = ''
        self.qfe = ''
        self.qff = ''
        self.dewpoint_fm_humi = 0.0
        self.dewpoint_fm_wetb = 0.0
        self.humi_fm_wetb = 0.0
        self.fogpt = 0.0
        self.minvis = 0
        self.duskvis = 0
        self.wind1200 = 0
        self.steep_inv = 0
        self.steep_inv_gust = 0
        self.shall_inv = 0
        self.shall_inv_gust = 0
        self.salr = 0
        self.salr_gust = 0
        self.one_c = 0
        self.one_c_gust = 0
        self.dalr_sfc = 0
        self.dalr_sfc_gust = 0
        self.dalr_6000 = 0
        self.dalr_6000_gust = 0
        self.large_cu = 0
        self.large_cu_gust = 0
        self.base = 0
        self.base_alt = 0

    def get_qnh(self, obs_press, temp, baro_ht, elevation, latitude):
        """Get the QNH pressure from observed pressure.
        :param obs_press: The sensor pressure reading in hPa.
        :param temp: The air temperature in degrees C.
        :param baro_ht: The barometer height above site level in metres.
        :param elevation: The altitude of the site above mean sea level in metres.
        :param latitude: The latitude of the site e.g. 52 degrees.
        """
        self.qnh = '{:.2f}'.format(round(met_calcs.calc_qnh_alt(obs_press, temp, elevation, baro_ht), 2))
        self.qfe = '{:.2f}'.format(round(met_calcs.calc_qfe(temp, obs_press, baro_ht), 2))
        self.qff = '{:.2f}'.format(round(met_calcs.calc_qff(temp, float(self.qfe), elevation, latitude), 2))
        self.inhg_flag = True

    def convert_to_inhg(self, qnh_hpa, qfe_hpa, qff_hpa):
        """Convert QNH, QFE, QFF values in hectopascals to inches of mercury
        :param qfe_hpa:
        :param qff_hpa:
        :param qnh_hpa: """
        qnh_inhg = '{:.2f}'.format(round(float(qnh_hpa) * 0.0295299830714, 2))
        qfe_inhg = '{:.2f}'.format(round(float(qfe_hpa) * 0.0295299830714, 2))
        qff_inhg = '{:.2f}'.format(round(float(qff_hpa) * 0.0295299830714, 2))

        return qnh_inhg, qfe_inhg, qff_inhg

    def get_dewpt_fm_humi(self, temp, humidity):
        """Get Dew Point temperature in degrees C from the air temperature and humidity.
        :param temp: Air temperature in degrees C.
        :param humidity: Air humidity %
        """
        self.dewpoint_fm_humi = '{:.1f}'.format(round(met_calcs.calc_dewpoint(humidity, temp), 2))

    def get_dewpt_fm_wetb(self, temp, wetb, pressure):
        """Get Dew Point from the air temperature and wet bulb temperature.
        :param pressure:
        :param temp: Air temperature in degrees C.
        :param wetb: Wet Bulb temperature in degrees C.
        """
        self.dewpoint_fm_wetb = '{:.1f}'.format(round(met_calcs.calc_dewpoint_fm_wetbulb(temp, wetb, pressure), 2))

    def get_humi_fm_wetb(self, temp, wetb, pressure):
        """Get the humidity for a given air temperature and wet bulb temperature.
        :param pressure:
        :param temp: Air temperature in degrees C.
        :param wetb: Wet Bulb temperature in degrees C.
        """
        self.humi_fm_wetb = '{:.0f}'.format(round(met_calcs.calc_humid_fm_wetbulb(temp, wetb, pressure), 0))

    def get_fog(self, mintemp, dewpt, windpsd, maxvis):
        """Get the minimum overnight visibility(M), dusk visibility(M) and fog point as calculated by the modified
            Middle Wallop method.
        :param mintemp: Minimum overnight temperature in degrees C.
        :param dewpt: The dew point temperature in degrees C at time of maximum visibility.
        :param windpsd: Overnight wind speed factor (1 = 0-5kts, 2 = 6-9kts, 3 = >9 kts).
        :param maxvis: Maximum daytime visibility in metres.
        """
        middle_wallop_results = met_calcs.middle_wallop(mintemp, dewpt, windpsd, maxvis)
        self.fogpt = '{:.1f}'.format(round(middle_wallop_results[2], 2))
        self.minvis = '{:.0f}'.format(round(middle_wallop_results[0], -2))
        self.duskvis = '{:.0f}'.format(round(middle_wallop_results[1], -2))

    def get_winds(self, grad_wind):
        """Get the wind speed and max gust expected for given gradient wind speed and pre-set atmospheric stability
            profiles.
        :param grad_wind: Gradient wind speed in kts.
        """
        wind_results = met_calcs.calc_winds(grad_wind)
        self.wind1200 = '{:.0f}'.format(wind_results[0])
        self.steep_inv = wind_results[1]
        self.steep_inv_gust = wind_results[2]
        self.shall_inv = wind_results[3]
        self.shall_inv_gust = wind_results[4]
        self.salr = wind_results[5]
        self.salr_gust = wind_results[6]
        self.one_c = wind_results[7]
        self.one_c_gust = wind_results[8]
        self.dalr_sfc = wind_results[9]
        self.dalr_sfc_gust = wind_results[10]
        self.dalr_6000 = wind_results[11]
        self.dalr_6000_gust = wind_results[12]
        self.large_cu = wind_results[13]
        self.large_cu_gust = wind_results[14]

    def get_base(self, temp, dewpt, land_state):
        """Get the calculated stratus base for a given air temperature, dew point and land warming/colling state.
        :param temp: Air temperature in degrees C.
        :param dewpt: Dew point in degrees C.
        :param land_state: Either 1 = warming land or other integer to indicate cooling land.
        """
        self.base = '{:.0f}'.format(round(met_calcs.calc_stratus_base(temp, dewpt, land_state), 0))

    def get_base_alt(self, sfc_wind, air_state):
        """Get the calculated stratus base for a given surface wind speed in knots and moist or dry air.
        :param air_state: 0 = dry air, 1 - moist air.
        :param sfc_wind: Surface wind speed in knots.
        """
        self.base_alt = '{:.0f}'.format(round(met_calcs.calc_stratus_base_alt(sfc_wind, air_state), 0))


class Controller:
    """Main GUI controller, handles mouse, keyboard and data change events."""

    def __init__(self):
        self.root = tk.Tk()
        self.model = Model()
        self.main_view = gui.MainView(self.root)
        self.inhg_flag = True

        self.main_view.qnh_view.calc_qnh_button.bind('<Button>', self.get_qnh)
        self.main_view.qnh_view.calc_qnh_button.bind('<Return>', self.get_qnh)
        self.main_view.qnh_view.calc_inhg_button.bind('<Button>', self.convert_inhg)
        self.main_view.qnh_view.calc_inhg_button.bind('<Return>', self.convert_inhg)
        self.main_view.dewpt_hum_view.calc_dewpt_button.bind('<Button>', self.get_dewpt_fm_humi)
        self.main_view.dewpt_hum_view.calc_dewpt_button.bind('<Return>', self.get_dewpt_fm_humi)
        self.main_view.dewpt_wetbulb_view.calc_dewpt_button.bind('<Button>', self.get_dewpt_fm_wetb)
        self.main_view.dewpt_wetbulb_view.calc_dewpt_button.bind('<Return>', self.get_dewpt_fm_wetb)

        self.main_view.middlewallop_view.mintemp_scale.bind('<ButtonRelease>', self.get_fog)
        self.main_view.middlewallop_view.dewpt_scale.bind('<ButtonRelease>', self.get_fog)
        self.main_view.middlewallop_view.maxvis_scale.bind('<ButtonRelease>', self.get_fog)

        self.main_view.middlewallop_view.wind5.bind('<ButtonRelease>', self.get_fog1)
        self.main_view.middlewallop_view.wind9.bind('<ButtonRelease>', self.get_fog2)
        self.main_view.middlewallop_view.wind10.bind('<ButtonRelease>', self.get_fog3)

        self.main_view.windgust_view.calc_wind_button.bind('<Button>', self.get_winds)
        self.main_view.windgust_view.calc_wind_button.bind('<Return>', self.get_winds)

        self.main_view.stratus_view.calc_stratus_button.bind('<Button>', self.get_stratus_base)
        self.main_view.stratus_view.calc_stratus_button.bind('<Return>', self.get_stratus_base)

        self.main_view.stratus_view.calc_stratus_button2.bind('<Button>', self.get_stratus_base_alt)
        self.main_view.stratus_view.calc_stratus_button2.bind('<Return>', self.get_stratus_base_alt)

    def run(self):
        """Start the application"""
        self.root.title('Met Calculator')
        self.root.deiconify()
        self.root.mainloop()

    def get_qnh(self, event):
        """Handle response to QNH/QFE/QFF calculate request.
        :param event: QNH/QFE/QFF calculate button or enter.
        """
        self.main_view.qnh_view.qnh.set('ERROR')
        self.main_view.qnh_view.qff.set('ERROR')
        self.main_view.qnh_view.qfe.set('ERROR')

        self.model.get_qnh(self.main_view.qnh_view.obs_press.get(), self.main_view.qnh_view.temp.get(),
                           self.main_view.qnh_view.baro_ht.get(), self.main_view.qnh_view.elevation.get(),
                           self.main_view.qnh_view.latitude.get())

        self.main_view.qnh_view.qnh.set(self.model.qnh)
        self.main_view.qnh_view.qfe.set(self.model.qfe)
        self.main_view.qnh_view.qff.set(self.model.qff)
        self.main_view.qnh_view.qnhlabel.set('QNH (hPa) :')
        self.main_view.qnh_view.qfelabel.set('QFE (hPa) :')
        self.main_view.qnh_view.qfflabel.set('QFF (hPa) :')
        self.inhg_flag = True

    def convert_inhg(self, event):
        if self.inhg_flag:
            pressures_inhg = self.model.convert_to_inhg(self.main_view.qnh_view.qnh.get(),
                                                        self.main_view.qnh_view.qfe.get(),
                                                        self.main_view.qnh_view.qff.get())
            self.main_view.qnh_view.qnh.set(pressures_inhg[0])
            self.main_view.qnh_view.qfe.set(pressures_inhg[1])
            self.main_view.qnh_view.qff.set(pressures_inhg[2])
            self.main_view.qnh_view.qnhlabel.set('QNH (inHg):')
            self.main_view.qnh_view.qfelabel.set('QFE (inHg):')
            self.main_view.qnh_view.qfflabel.set('QFF (inHg):')
            self.inhg_flag = False

    def get_dewpt_fm_humi(self, event):
        """Handle response to dew point from humidity calculate request.
        :param event: Mouse button or enter pressed on calculate button.
        """
        self.main_view.dewpt_hum_view.result_dewpt.set('ERROR')
        self.model.get_dewpt_fm_humi(self.main_view.dewpt_hum_view.temp.get(),
                                     self.main_view.dewpt_hum_view.humidity.get())

        self.main_view.dewpt_hum_view.result_dewpt.set(self.model.dewpoint_fm_humi)

    def get_dewpt_fm_wetb(self, event):
        """Handle response to dew point from wet bulb calculate request.
        :param event: Mouse button or enter pressed on calculate button.
        """
        self.main_view.dewpt_wetbulb_view.result_dewpt.set('ERROR')
        self.main_view.dewpt_wetbulb_view.result_humi.set('ERROR')

        self.model.get_dewpt_fm_wetb(self.main_view.dewpt_wetbulb_view.temp.get(),
                                     self.main_view.dewpt_wetbulb_view.wetbulb.get(),
                                     self.main_view.dewpt_wetbulb_view.pressure.get())

        self.model.get_humi_fm_wetb(self.main_view.dewpt_wetbulb_view.temp.get(),
                                    self.main_view.dewpt_wetbulb_view.wetbulb.get(),
                                    self.main_view.dewpt_wetbulb_view.pressure.get())

        self.main_view.dewpt_wetbulb_view.result_dewpt.set(self.model.dewpoint_fm_wetb)
        self.main_view.dewpt_wetbulb_view.result_humi.set(self.model.humi_fm_wetb)

    def get_fog(self, event):
        """Handle response to fog/vis slider change recalculate request.
        :param event: Fog/Vis method slider changed.
        """
        self.model.get_fog(self.main_view.middlewallop_view.mintemp_scale.get(),
                           self.main_view.middlewallop_view.dewpt_scale.get(),
                           self.main_view.middlewallop_view.wind.get(),
                           self.main_view.middlewallop_view.maxvis_scale.get())

        self.main_view.middlewallop_view.result_fogpt.set(self.model.fogpt)
        self.main_view.middlewallop_view.result_minvis.set(self.model.minvis)
        self.main_view.middlewallop_view.result_duskvis.set(self.model.duskvis)

    def get_fog1(self, event):  # Must be an easier way to do this? Tk variables events?
        """Handle response to wind 0-5kts selected calculate request.
        :param event: 0-5 kts radio button selected.
        """
        self.model.get_fog(self.main_view.middlewallop_view.mintemp_scale.get(),
                           self.main_view.middlewallop_view.dewpt_scale.get(),
                           1,
                           self.main_view.middlewallop_view.maxvis_scale.get())

        self.main_view.middlewallop_view.result_fogpt.set(self.model.fogpt)
        self.main_view.middlewallop_view.result_minvis.set(self.model.minvis)
        self.main_view.middlewallop_view.result_duskvis.set(self.model.duskvis)

    def get_fog2(self, event):
        """Handle response to wind 6-9kts selected calculate request.
        :param event: 6-9 kts radio button selected."""
        self.model.get_fog(self.main_view.middlewallop_view.mintemp_scale.get(),
                           self.main_view.middlewallop_view.dewpt_scale.get(),
                           2,
                           self.main_view.middlewallop_view.maxvis_scale.get())

        self.main_view.middlewallop_view.result_fogpt.set(self.model.fogpt)
        self.main_view.middlewallop_view.result_minvis.set(self.model.minvis)
        self.main_view.middlewallop_view.result_duskvis.set(self.model.duskvis)

    def get_fog3(self, event):
        """Handle response to wind 6-9kts selected calculate request.
        :param event: 6-9 kts radio button selected."""
        self.model.get_fog(self.main_view.middlewallop_view.mintemp_scale.get(),
                           self.main_view.middlewallop_view.dewpt_scale.get(),
                           3,
                           self.main_view.middlewallop_view.maxvis_scale.get())

        self.main_view.middlewallop_view.result_fogpt.set(self.model.fogpt)
        self.main_view.middlewallop_view.result_minvis.set(self.model.minvis)
        self.main_view.middlewallop_view.result_duskvis.set(self.model.duskvis)

    def get_winds(self, event):
        """Handle response to mouse button or enter key on winds calculate
        :param event: Mouse button or enter button pressed on calculate winds.
        """
        self.model.get_winds(self.main_view.windgust_view.gradwind.get())
        self.main_view.windgust_view.result_wind1200.set(self.model.wind1200)

        for i in self.main_view.windgust_view.treeview.get_children():
            self.main_view.windgust_view.treeview.delete(i)

        self.main_view.windgust_view.treeview.insert("", 0, text="Steep inversion",
                                                     values=(int(self.model.steep_inv), int(self.model.steep_inv_gust)))
        self.main_view.windgust_view.treeview.insert("", 1, text="Shallow inversion",
                                                     values=(int(self.model.shall_inv), int(self.model.shall_inv_gust)))
        self.main_view.windgust_view.treeview.insert("", 2, text="SALR from surface",
                                                     values=(int(self.model.salr), int(self.model.salr_gust)))
        self.main_view.windgust_view.treeview.insert("", 3, text="1-2 deg C / 1000ft",
                                                     values=(int(self.model.one_c), int(self.model.one_c_gust)))
        self.main_view.windgust_view.treeview.insert("", 4, text="DALR from surface",
                                                     values=(int(self.model.dalr_sfc), int(self.model.dalr_sfc_gust)))
        self.main_view.windgust_view.treeview.insert("", 5, text="DALR to 6000ft",
                                                     values=(int(self.model.dalr_6000), int(self.model.dalr_6000_gust)))
        self.main_view.windgust_view.treeview.insert("", 6, text="Large CU / Steep LR",
                                                     values=(int(self.model.large_cu), int(self.model.large_cu_gust)))

    def get_stratus_base(self, event):
        """Handle events for stratus base calculator.
        :param event: Mouse button or enter pressed on stratus base calculate.
        """
        self.main_view.stratus_view.result_stratusbase.set('ERROR')
        self.model.get_base(self.main_view.stratus_view.temp.get(), self.main_view.stratus_view.dewpt.get(),
                            self.main_view.stratus_view.land_state.get())

        self.main_view.stratus_view.result_stratusbase.set(self.model.base)

    def get_stratus_base_alt(self, event):
        """Handle events for the alternative stratus base calculator.
        :param event: Mouse button or enter pressed on alternative stratus base calculate.
        """
        self.main_view.stratus_view.result_stratusbase2.set('ERROR')
        self.model.get_base_alt(self.main_view.stratus_view.wind.get(), self.main_view.stratus_view.air_state.get())

        self.main_view.stratus_view.result_stratusbase2.set(self.model.base_alt)


if __name__ == '__main__':
    controller = Controller()
    controller.run()
