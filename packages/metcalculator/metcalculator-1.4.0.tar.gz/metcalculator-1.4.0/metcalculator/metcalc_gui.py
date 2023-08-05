#!/usr/bin/env python
import sys

if sys.version_info[0] < 3:
    import Tkinter as tk
    import ttk
else:
    import tkinter as tk
    from tkinter import ttk as ttk

__author__ = 'Mark Baker  email: mark2182@mac.com'


class MainView:
    """Main GUI class responsible for initiating separate window frames for the various calculation tools."""

    def __init__(self, master):
        self.frame = ttk.Frame(master)
        self.frame.grid(row=0, column=0, padx=5, pady=5)

        # s = ttk.Style()
        # s.theme_use('aqua')

        """self.menubar = tk.Menu(master)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label='Quit', command=sys.exit)
        self.menubar.add_cascade(label='MetCalculator', menu=self.filemenu)
        master.config(menu=self.menubar)"""

        self.qnh_view = QNHview(master)
        self.dewpt_hum_view = DewpointFromHumidityView(master)
        self.dewpt_wetbulb_view = DewpointFromWetbulbView(master)
        self.middlewallop_view = MiddleWallop(master)
        self.windgust_view = WindGust(master)
        self.stratus_view = StratusBase(master)



class QNHview:
    """Label window frame containing the widgets for calculating QNH/QFE/QFF. """

    def __init__(self, root):
        validcmd_positive = (root.register(validate_float_positive), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        validcmd = (root.register(validate_float_negative), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.frame_qnh = tk.LabelFrame(root, text='QNH QFE QFF')
        self.frame_qnh.grid(row=0, column=0, columnspan=2, sticky=tk.NSEW, padx=5, pady=5)

        self.obs_press_label = ttk.Label(self.frame_qnh, text="Observed Pressure (hPa):")
        self.obs_press_label.grid(sticky=tk.E, row=0, column=0, padx=5, pady=5)

        self.obs_press = tk.DoubleVar()
        self.obs_press_entry = ttk.Entry(self.frame_qnh, textvariable=self.obs_press, width=8, validate='key',
                                         validatecommand=validcmd_positive)
        self.obs_press_entry.grid(row=0, column=2, pady=5)
        self.obs_press.set(1013.25)

        self.temp_label = ttk.Label(self.frame_qnh, text="Temperature (deg C):")
        self.temp_label.grid(sticky=tk.E, row=1, column=0, padx=5, pady=5)

        self.temp = tk.DoubleVar()
        self.temp_entry = ttk.Entry(self.frame_qnh, textvariable=self.temp, width=8, validate='key',
                                    validatecommand=validcmd)
        self.temp_entry.grid(row=1, column=2, pady=5)
        self.temp.set(15.0)

        self.baro_ht_label = ttk.Label(self.frame_qnh, text="Barometer height above ground (metres):")
        self.baro_ht_label.grid(sticky=tk.E, row=2, column=0, padx=5, pady=5)

        self.baro_ht = tk.DoubleVar()
        self.baro_ht_entry = ttk.Entry(self.frame_qnh, textvariable=self.baro_ht, width=8, validate='key',
                                       validatecommand=validcmd)
        self.baro_ht_entry.grid(row=2, column=2, pady=5)
        self.baro_ht.set(4.65)

        self.elevation_label = ttk.Label(self.frame_qnh, text="Station Elevation AMSL (metres):")
        self.elevation_label.grid(sticky=tk.E, row=3, column=0, padx=5, pady=5)

        self.elevation = tk.DoubleVar()
        self.elevation_entry = ttk.Entry(self.frame_qnh, textvariable=self.elevation, width=8, validate='key',
                                         validatecommand=validcmd)
        self.elevation_entry.grid(row=3, column=2, pady=5)
        self.elevation.set(86.35)

        self.latitude_label = ttk.Label(self.frame_qnh, text="Station Latitude (only affects QFF):")
        self.latitude_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.E)

        self.latitude = tk.DoubleVar()
        self.latitude_entry = ttk.Entry(self.frame_qnh, textvariable=self.latitude, width=8, validate='key',
                                        validatecommand=validcmd_positive)
        self.latitude_entry.grid(row=4, column=2, pady=5)

        self.calc_qnh_button = ttk.Button(self.frame_qnh, text='Calculate')
        self.calc_qnh_button.grid(row=3, column=5, sticky=tk.W, padx=10)

        self.calc_inhg_button = ttk.Button(self.frame_qnh, text='>> inHg')
        self.calc_inhg_button.grid(row=3, column=6, sticky=tk.W, padx=10)

        self.qnhlabel = tk.StringVar()
        self.qnhlabel.set('QNH (hPa) :')
        self.qnh = tk.StringVar()
        self.qnh_result_label = ttk.Label(self.frame_qnh, textvariable=self.qnhlabel)
        self.qnh_result_label.grid(row=0, column=5, sticky=tk.E, padx=5)
        self.qnh_result = ttk.Label(self.frame_qnh, textvariable=self.qnh, width=7)
        self.qnh_result.grid(sticky=tk.W, row=0, column=6, padx=5)

        self.qfelabel = tk.StringVar()
        self.qfelabel.set('QFE (hPa) :')
        self.qfe = tk.StringVar()
        self.qfe_result_label = ttk.Label(self.frame_qnh, textvariable=self.qfelabel)
        self.qfe_result_label.grid(row=1, column=5, sticky=tk.E, padx=5)
        self.qfe_result = ttk.Label(self.frame_qnh, textvariable=self.qfe, width=7)
        self.qfe_result.grid(sticky=tk.W, row=1, column=6, padx=5)

        self.qfflabel = tk.StringVar()
        self.qfflabel.set('QFF (hPa) :')
        self.qff = tk.StringVar()
        self.qff_result_label = ttk.Label(self.frame_qnh, textvariable=self.qfflabel)
        self.qff_result_label.grid(row=2, column=5, sticky=tk.E, padx=5)
        self.qff_result = ttk.Label(self.frame_qnh, textvariable=self.qff, width=7)
        self.qff_result.grid(sticky=tk.W, row=2, column=6, padx=5)


class DewpointFromHumidityView:
    """Label window frame containing the widgets for calculating dew point from humidity. """

    def __init__(self, root):
        validcmd = (root.register(validate_float_negative), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        validcmd_positive = (root.register(validate_float_positive), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.frame_dewpt_humi = tk.LabelFrame(root, text='Dew Point from Humidity')
        self.frame_dewpt_humi.grid(row=1, column=0, sticky=tk.NSEW, padx=5, pady=5)

        self.temp_label = ttk.Label(self.frame_dewpt_humi, text="Temperature (deg C):")
        self.temp_label.grid(sticky=tk.E, row=0, column=0, padx=5, pady=5)
        self.temp = tk.DoubleVar()
        self.temp_entry = ttk.Entry(self.frame_dewpt_humi, textvariable=self.temp, width=6, validate='key',
                                    validatecommand=validcmd)
        self.temp_entry.grid(row=0, column=1, pady=5)
        self.temp.set(15.0)

        self.humi_label = ttk.Label(self.frame_dewpt_humi, text="Humidity (%):")
        self.humi_label.grid(sticky=tk.E, row=1, column=0, padx=5, pady=5)
        self.humidity = tk.DoubleVar()
        self.humi_entry = ttk.Entry(self.frame_dewpt_humi, textvariable=self.humidity, width=6, validate='key',
                                    validatecommand=validcmd_positive)
        self.humi_entry.grid(row=1, column=1, pady=5)
        self.humidity.set(75)

        self.dewpt_label = ttk.Label(self.frame_dewpt_humi, text="Dew Pt (deg C):")
        self.dewpt_label.grid(sticky=tk.E, row=3, column=0, padx=5, pady=5)
        self.result_dewpt = tk.StringVar()
        self.result_label = ttk.Label(self.frame_dewpt_humi, textvariable=self.result_dewpt, width=7)
        self.result_label.grid(row=3, column=1, sticky=tk.E, padx=5, pady=5)

        self.calc_dewpt_button = ttk.Button(self.frame_dewpt_humi, text='Calculate')
        self.calc_dewpt_button.grid(row=2, column=0, columnspan=1, sticky=tk.E, )


class DewpointFromWetbulbView:
    """Label window frame containing the widgets for calculating dew point from wet bulb."""

    def __init__(self, root):
        validcmd = (root.register(validate_float_negative), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.frame_dewpt_wetb = tk.LabelFrame(root, text='Dew Point from Wet Bulb')
        self.frame_dewpt_wetb.grid(row=1, column=1, sticky=tk.NSEW, padx=5, pady=5)

        self.temp_label = ttk.Label(self.frame_dewpt_wetb, text="Temperature (deg C):")
        self.temp_label.grid(sticky=tk.E, row=0, column=0, padx=5, pady=5)
        self.temp = tk.DoubleVar()
        self.temp_entry = ttk.Entry(self.frame_dewpt_wetb, textvariable=self.temp, width=7, validate='key',
                                    validatecommand=validcmd)
        self.temp_entry.grid(row=0, column=1, pady=5)
        self.temp.set(15.0)

        self.wetb_label = ttk.Label(self.frame_dewpt_wetb, text="Wet Bulb (deg C):")
        self.wetb_label.grid(sticky=tk.E, row=1, column=0, padx=5, pady=5)
        self.wetbulb = tk.DoubleVar()
        self.wetb_entry = ttk.Entry(self.frame_dewpt_wetb, textvariable=self.wetbulb, width=7, validate='key',
                                    validatecommand=validcmd)
        self.wetb_entry.grid(row=1, column=1, pady=5)
        self.wetbulb.set(12.5)

        self.pressure_label = ttk.Label(self.frame_dewpt_wetb, text="Pressure (hPa):")
        self.pressure_label.grid(sticky=tk.E, row=2, column=0, padx=5, pady=5)
        self.pressure = tk.DoubleVar()
        self.pressure_entry = ttk.Entry(self.frame_dewpt_wetb, textvariable=self.pressure, width=7, validate='key',
                                    validatecommand=validcmd)
        self.pressure_entry.grid(row=2, column=1, pady=5)
        self.pressure.set(1013.25)

        self.dewpt_label = ttk.Label(self.frame_dewpt_wetb, text="Dew Pt (deg C):")
        self.dewpt_label.grid(sticky=tk.E, row=4, column=0, padx=5, pady=5)
        self.result_dewpt = tk.StringVar()
        self.result_dewpt_label = ttk.Label(self.frame_dewpt_wetb, textvariable=self.result_dewpt,
                                            width=7)
        self.result_dewpt_label.grid(row=4, column=1, sticky=tk.E, padx=5, pady=5)

        self.humi_label = ttk.Label(self.frame_dewpt_wetb, text="Humidity (%):")
        self.humi_label.grid(sticky=tk.E, row=5, column=0, padx=5, pady=5)
        self.result_humi = tk.StringVar()
        self.result_humi_label = ttk.Label(self.frame_dewpt_wetb, textvariable=self.result_humi,
                                           width=7)
        self.result_humi_label.grid(row=5, column=1, sticky=tk.E, padx=5, pady=5)

        self.calc_dewpt_button = ttk.Button(self.frame_dewpt_wetb, text='Calculate')
        self.calc_dewpt_button.grid(row=3, column=0, columnspan=1, sticky=tk.E, )


class MiddleWallop:
    """Label window frame containing the widgets for calculating fog and visibility parameters
        via Middle Wallop method."""

    def __init__(self, root):
        self.frame_middlewallop = tk.LabelFrame(root, text='Middle Wallop Method (Vis/Fog)')
        self.frame_middlewallop.grid(row=0, column=2, rowspan=2, sticky=tk.NSEW, padx=5, pady=5)

        self.fogpt_label = ttk.Label(self.frame_middlewallop, text="Fog Pt (C):")
        self.fogpt_label.grid(sticky=tk.W, row=0, column=0, padx=10, pady=5)
        self.result_fogpt = tk.StringVar()
        self.result_fogpt_label = ttk.Label(self.frame_middlewallop, textvariable=self.result_fogpt,
                                            width=7)
        self.result_fogpt_label.grid(row=0, column=1, sticky=tk.E, padx=10, pady=5)

        self.minvis_label = ttk.Label(self.frame_middlewallop, text='Min VIS (M):')
        self.minvis_label.grid(sticky=tk.W, row=1, column=0, padx=10, pady=5)
        self.result_minvis = tk.StringVar()
        self.result_minvis_label = ttk.Label(self.frame_middlewallop, textvariable=self.result_minvis,
                                             width=7)
        self.result_minvis_label.grid(row=1, column=1, sticky=tk.E, padx=10, pady=5)

        self.duskvis_label = ttk.Label(self.frame_middlewallop, text='Dusk VIS (M):')
        self.duskvis_label.grid(sticky=tk.W, row=2, column=0, padx=10)
        self.result_duskvis = tk.StringVar()
        self.result_duskvis_label = ttk.Label(self.frame_middlewallop, textvariable=self.result_duskvis,
                                              width=7)
        self.result_duskvis_label.grid(row=2, column=1, sticky=tk.E, padx=10, pady=5)

        self.wind = tk.IntVar()
        self.wind5 = tk.Radiobutton(self.frame_middlewallop, text="0-5 kt", variable=self.wind, value=1)
        self.wind5.grid(row=5, column=0, padx=15, pady=15, sticky=tk.W)
        self.wind9 = tk.Radiobutton(self.frame_middlewallop, text="6-9 kt", variable=self.wind, value=2)
        self.wind9.grid(row=5, column=1, pady=15, sticky=tk.W)
        self.wind10 = tk.Radiobutton(self.frame_middlewallop, text=">9 kt", variable=self.wind, value=3)
        self.wind10.grid(row=5, column=2, pady=15, sticky=tk.W)
        self.wind5.select()

        self.maxvis_label = ttk.Label(self.frame_middlewallop, text="Daytime Maximum Vis (M)")
        self.maxvis_label.grid(sticky=tk.W, row=7, column=0, columnspan=4, padx=10, pady=5)
        self.maxvis_scale = tk.Scale(self.frame_middlewallop, from_=1000, to=50000, orient=tk.HORIZONTAL,
                                     length=220, resolution=1000)
        self.maxvis_scale.grid(row=6, column=0, columnspan=4, padx=10)
        self.maxvis_scale.set(25000)

        self.mintemp_label = ttk.Label(self.frame_middlewallop, text="Min Overnight Temp. (deg C)")
        self.mintemp_label.grid(sticky=tk.W, row=9, column=0, columnspan=4, padx=10, pady=5)
        self.mintemp_scale = tk.Scale(self.frame_middlewallop, from_=-20, to=25, orient=tk.HORIZONTAL, length=220)
        self.mintemp_scale.grid(row=8, column=0, columnspan=4, padx=10)

        self.dewpt_label = ttk.Label(self.frame_middlewallop, text="Dew Point at Max Vis (deg C)")
        self.dewpt_label.grid(sticky=tk.W, row=11, column=0, columnspan=4, padx=10, pady=5)
        self.dewpt_scale = tk.Scale(self.frame_middlewallop, from_=-20, to=25, orient=tk.HORIZONTAL, length=220)
        self.dewpt_scale.grid(row=10, column=0, columnspan=4, padx=10)


class WindGust:
    """Label window frame containing the widgets for calculating surface wind speed & gusts for various stability
        profiles."""

    def __init__(self, root):
        validcmd_int = (root.register(validate_int), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.frame_windgust = tk.LabelFrame(root, text='Wind Gust')
        self.frame_windgust.grid(row=2, column=0, columnspan=2, sticky=tk.NSEW, padx=5, pady=5)

        self.gradwind_label = ttk.Label(self.frame_windgust, text="Gradient Wind (kts):")
        self.gradwind_label.grid(sticky=tk.N, row=0, column=0, padx=5, pady=10)
        self.gradwind = tk.IntVar()
        self.gradwind_entry = ttk.Entry(self.frame_windgust, textvariable=self.gradwind, width=5, validate='key',
                                        validatecommand=validcmd_int)
        self.gradwind_entry.grid(row=0, column=1, pady=10, padx=5, sticky=tk.NW)
        self.gradwind.set(25)

        self.wind1200_label = ttk.Label(self.frame_windgust, text="1200ft Wind (kts) :")
        self.wind1200_label.grid(sticky=tk.S, row=2, column=0)
        self.result_wind1200 = tk.StringVar()
        self.result_wind1200_label = ttk.Label(self.frame_windgust, textvariable=self.result_wind1200, width=7)
        self.result_wind1200_label.grid(row=2, column=1, sticky=tk.S)

        self.calc_wind_button = ttk.Button(self.frame_windgust, text='Calculate')
        self.calc_wind_button.grid(row=1, column=0, sticky=tk.NE, columnspan=1)

        self.treeview = ttk.Treeview(self.frame_windgust, height=8)
        self.treeview.grid(row=0, column=2, rowspan=8, columnspan=1, padx=5, pady=5)

        self.treeview["columns"] = ("mean", "gust")
        self.treeview.column("mean", width=50)
        self.treeview.column("gust", width=50)
        self.treeview.heading("mean", text="Mean")
        self.treeview.heading("gust", text="Gust")

        self.treeview.insert("", 0, text="Steep inversion", values=())
        self.treeview.insert("", 1, text="Shallow inversion", values=())
        self.treeview.insert("", 2, text="SALR from surface", values=())
        self.treeview.insert("", 3, text="1-2 deg C / 1000ft", values=())
        self.treeview.insert("", 4, text="DALR from surface", values=())
        self.treeview.insert("", 5, text="DALR to 6000ft", values=())
        self.treeview.insert("", 6, text="Large CU / Steep LR", values=())

        self.author_label = ttk.Label(self.frame_windgust, text='v1.4 - mark.baker@metoffice.gov.uk')
        self.author_label.grid(row=14, column=0, columnspan=5, sticky=tk.W)


class StratusBase:
    """Label window frame containing the widgets for calculating stratus cloud base."""
    def __init__(self, root):
        validcmd_float = (root.register(validate_float_negative), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        validcmd_int = (root.register(validate_int), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.frame_stratus = tk.LabelFrame(root, text='Stratus Base')
        self.frame_stratus.grid(row=2, column=2, sticky=tk.NSEW, padx=5, pady=5)

        self.temp_label = ttk.Label(self.frame_stratus, text="Temp(C):")
        self.temp_label.grid(sticky=tk.W, row=0, column=0, padx=5, pady=5)
        self.temp = tk.DoubleVar()
        self.temp_entry = ttk.Entry(self.frame_stratus, textvariable=self.temp, width=5, validate='key',
                                    validatecommand=validcmd_float)
        self.temp_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        self.temp.set(8.0)

        self.dewpt_label = ttk.Label(self.frame_stratus, text="DewPt.(C):")
        self.dewpt_label.grid(sticky=tk.W, row=0, column=2, padx=5, pady=5)
        self.dewpt = tk.DoubleVar()
        self.dewpt_entry = ttk.Entry(self.frame_stratus, textvariable=self.dewpt, width=5, validate='key',
                                     validatecommand=validcmd_float)
        self.dewpt_entry.grid(row=0, column=3, sticky=tk.W, padx=5, pady=5)
        self.dewpt.set(6.0)

        self.land_state = tk.IntVar()
        self.land_warming = tk.Radiobutton(self.frame_stratus, text="Land warming", variable=self.land_state, value=1)
        self.land_warming.grid(row=2, column=0, sticky=tk.W, columnspan=3, padx=5, pady=5)
        self.land_cooling = tk.Radiobutton(self.frame_stratus, text="Land cooling", variable=self.land_state, value=0)
        self.land_cooling.grid(row=2, column=2, sticky=tk.W, columnspan=3, padx=5, pady=5)
        self.land_cooling.select()

        self.calc_stratus_button = ttk.Button(self.frame_stratus, text='Calculate')
        self.calc_stratus_button.grid(row=3, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)

        self.stratusbase_label = ttk.Label(self.frame_stratus, text='BASE (ft):')
        self.stratusbase_label.grid(sticky=tk.E, row=3, column=2, padx=5, pady=5)
        self.result_stratusbase = tk.StringVar()
        self.result_stratusbase_label = ttk.Label(self.frame_stratus, textvariable=self.result_stratusbase, width=6)
        self.result_stratusbase_label.grid(row=3, column=3, sticky=tk.W, padx=5, pady=5)

        self.wind_label = ttk.Label(self.frame_stratus, text="Surface wind (V) (kts):")
        self.wind_label.grid(sticky=tk.E, row=4, column=0, columnspan=3, padx=5, pady=5)
        self.wind = tk.IntVar()
        self.wind_entry = ttk.Entry(self.frame_stratus, textvariable=self.wind, width=5, validate='key',
                                    validatecommand=validcmd_int)
        self.wind_entry.grid(row=4, column=3, sticky=tk.W, padx=5, pady=5)
        self.wind.set(10)

        self.air_state = tk.IntVar()
        self.dry_air = tk.Radiobutton(self.frame_stratus, text="Dry air (V*200)", variable=self.air_state, value=0)
        self.dry_air.grid(row=5, column=0, sticky=tk.W, columnspan=3, padx=5, pady=5)
        self.moist_air = tk.Radiobutton(self.frame_stratus, text="Moist air (V*75)", variable=self.air_state, value=1)
        self.moist_air.grid(row=5, column=2, sticky=tk.W, columnspan=3, padx=5, pady=5)
        self.moist_air.select()

        self.calc_stratus_button2 = ttk.Button(self.frame_stratus, text='Calculate')
        self.calc_stratus_button2.grid(row=6, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)

        self.stratusbase_label2 = ttk.Label(self.frame_stratus, text='BASE (ft):')
        self.stratusbase_label2.grid(sticky=tk.E, row=6, column=2, padx=5, pady=5)
        self.result_stratusbase2 = tk.StringVar()
        self.result_stratusbase2_label = ttk.Label(self.frame_stratus, textvariable=self.result_stratusbase2, width=6)
        self.result_stratusbase2_label.grid(row=6, column=3, sticky=tk.W, padx=5, pady=5)


def validate_float_negative(action, index, value_if_allowed,
                   prior_value, text, validation_type, trigger_type, widget_name):
    if not value_if_allowed:
        return True

    if text in '-1234567890':
        return True

    if text in '0123456789.-+':
        try:
            float(value_if_allowed)
            return True
        except ValueError:
            return False
    else:
        return False


def validate_float_positive(action, index, value_if_allowed,
                   prior_value, text, validation_type, trigger_type, widget_name):
    if not value_if_allowed:
        return True

    if text in '0123456789.+':
        try:
            float(value_if_allowed)
            return True
        except ValueError:
            return False
    else:
        return False


def validate_int(action, index, value_if_allowed,
                 prior_value, text, validation_type, trigger_type, widget_name):
    if not value_if_allowed:
        return True

    if text in '0123456789':
        try:
            int(value_if_allowed)
            return True
        except ValueError:
            return False
    else:
        return False
