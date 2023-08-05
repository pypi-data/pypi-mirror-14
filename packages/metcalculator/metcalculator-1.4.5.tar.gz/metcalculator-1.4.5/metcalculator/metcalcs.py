#!/usr/bin/env python

import math

__author__ = 'Mark Baker - mark2182@mac.com'

""" Python code for calculating various meteorological parameters
by Mark Baker (c)2015 - Mark Baker mark2182@mac.com')"""


def celsius_to_kelvin(temp_c):
    """Convert celsius temperature to Kelvin by adding 273.15.
    :param temp_c: Temperature in degrees C.
    :return temperature in Kelvin
    """
    return temp_c + 273.15


def kelvin_to_celsius(temp_k):
    """Convert Kelvin temperature to Celsius by subtracting 273.15.
    :param temp_k: Temperature in Kelvin.
    :return Temperature in degrees Celsius.
    """
    return temp_k - 273.15


def celsius_to_farenh(temp_c):
    """Convert Celsius temperature to Fahrenheit.
    :param temp_c: Temperature in degees C
    :return Temperature in degrees Fahrenheit.
    """
    return ((temp_c * 9.0) / 5.0) + 32.0


def farenh_to_celsius(temp_f):
    """Convert Fahrenheit temperature to Celsius.
    :param temp_f: Temperature in Fahrenheit.
    :return Temperature in Celsius.
    """
    return ((temp_f - 32.0) * 5.0) / 9.0


def calc_dewpoint(rel_humi, temp_c):
    """Calculate the air mass dewpoint for a given relative humidity (%) and temperature (C)
       using Vaisala's method.

        pws= Saturation vapour pressure (hPa)   A, m, Tn= constants   T= temp (C)
        A = 6.116441  m = 7.591386  Tn = 240.7263
        :param temp_c: Temperature in degrees C.
        :param rel_humi: Percentage relative humidity
        """
    if rel_humi > 0:
        x = (7.591386 * temp_c) / (temp_c + 240.7263)
        pws = 6.116441 * math.pow(10, x)
        pw = pws * (rel_humi / 100.0)
        y = math.log10(pw / 6.116441)
        z = (7.591386 / y) - 1
        dewpoint = 240.7263 / z
        return dewpoint


def calc_dewpoint_fm_wetbulb(temp_c, wetbulb_c, pressure):
    """Calculate the air mass dewpoint for a given dry bulb and wet bulb temperature (C) using
       Vaisala's method.
       :param pressure:
       :param wetbulb_c: Wet bulb temperature in degrees C.
       :param temp_c: Dry bulb temperature in degrees C.
       """

    xdry = (7.591386 * temp_c) / (temp_c + 240.7263)
    xwet = (7.591386 * wetbulb_c) / (wetbulb_c + 240.7263)

    pwswet = 6.116441 * math.pow(10, xwet)

    pw = pwswet - pressure * 0.0008 * (temp_c - wetbulb_c)

    y = math.log10(pw / 6.116441)

    z = (7.591386 / y) - 1

    dewpoint = 240.7263 / z
    return dewpoint


def calc_humid_fm_wetbulb(temp_c, wetbulb_c, pressure):
    """Calculate the air mass humidity (%) for a given dry bulb and wet bulb temperature (C) using
       Vaisala's method.
       :param pressure:
       :param wetbulb_c: Wet bulb temperature in degrees C.
       :param temp_c: Dry bulb temperature in degrees C.
       """
    xdry = (7.591386 * temp_c) / (temp_c + 240.7263)
    xwet = (7.591386 * wetbulb_c) / (wetbulb_c + 240.7263)

    pwsdry = 6.116441 * math.pow(10, xdry)
    pwswet = 6.116441 * math.pow(10, xwet)

    pw = pwswet - pressure * 0.0008 * (temp_c - wetbulb_c)

    rh = (pw / pwsdry) * 100
    return rh


def calc_qfe(temp_c, sensor_pressure, sensor_height):
    """Calculate pressure at site ground level given observed pressure, temperature and height
       above ground of the sensor.

        Applies the 'hypsometric equation':
        QFE = p x (1+ (hQFE x g) / (R x T))
        p = sensor pressure, hQFE = barometer height above station elevation, R = gas const.
        T = temperature in deg C.
        :param sensor_height: Height of barometer above ground level in metres.
        :param sensor_pressure: Pressure reading from sensor in hPa.
        :param temp_c: Temperature in degrees C.
        """

    qfe = sensor_pressure * (1 + ((sensor_height * 9.80665) / (287.04 * (temp_c + 273.15))))
    return qfe


def calc_qnh(qfe, site_elevation):
    """Calculate the mean sea level pressure given QFE pressure, temperature and height
       above sea level (altitude) - ICAO recommended calculation of QNH from QFE see ICAO doc 9837.

        heightISA = 44330.77 - 11880.32 x QFE^0.190263
        QNH = 1013.25 x ((1 - (0.0065 x (heightISA-height)/288.15))^5.25588)
        :param site_elevation: Elevation of the site above mean sea level (MSL).
        :param qfe: QFE pressure reading in hPa."""

    qnh = 1013.23 * (math.pow((1 - ((((44330.77 - (11880.32 * (math.pow(qfe, 0.190263)))) -
                                      site_elevation) / 288.15) * 0.0065)), 5.25588))
    return qnh


def calc_qnh_alt(pressure, temperature, afht, barht):
    """Alternative method for calculating QNH base on Ross Provans (Met Office) spreadsheet
    :param barht: Barometer height above ground level.
    :param afht: Airfield height above mean sea level.
    :param temperature: Observed temperature (deg C).
    :param pressure: Observed pressure (hPa - read from sensor).
    """

    const = (1 + (9.6 * ((math.pow(10, -5)) * afht) + (6 * (math.pow(10, -9)) * (math.pow(afht, 2)))))
    qnh = pressure + ((0.022857 * afht) + ((const - 1) * pressure) + (const * (pressure * ((math.pow(10,
        (barht / (18429.1 + 67.53 * temperature + (0.003 * barht)))))) - pressure)))

    return qnh


def calc_qff(temp_c, qfe, site_elevation, latitude):
    """Calculate the sea level pressure using the Swedish HMI method for automatic stations.

        QFF = QFE x e^(stationElev x (0.034163(1-0.0026373 cos(2w)/t)
        if temp < -7degC  t = 0.5 x temp + 275
                   -7degC <= temp < +2degC   t = 0.54 x temp + 275.6
                     temp > +2degC  t = 1.07 x temp + 274.5
              t is a way of describing the winter inversions.
              :param latitude: Latitude of site (e.g. 52.0).
              :param site_elevation: Site elevation above mean sea level in metres.
              :param qfe: Calculated QFE pressure in hPa.
              :param temp_c: Temperature in degrees C.
              """

    if temp_c < -7:
        t = 0.5 * temp_c + 275
    elif -7 <= temp_c <= 2:
        t = 0.533 * temp_c + 275.6
    else:
        t = 1.07 * temp_c + 274.5

    qff = qfe * (math.pow(2.71828182, ((site_elevation * (0.034163 *
                                (1 - (0.0026373 * (math.cos(2 * latitude)))))) / t)))
    return qff


def middle_wallop(temp_min, dewpt, windfactor, maxvis):
    """Calculate fog point, minimum overnight visibility and dusk visibility using the Middle Wallop
        method as modified by matt.woods@metoffice.gov.uk, fog point calculated using method developed by
        dan.harris@metoffice.gov.uk . This empirical technique takes account of overnight wind, daytime maximum
        visibility and daytime dew point. For further details refer to the Forecasters Reference book visibility
        section.
    :param temp_min: Minimum temperature overnight in degrees C.
    :param dewpt: Dew point at maximum daytime visibility in degrees C.
    :param windfactor: 1 = 0-5kts, 2 = 6-9kts, 3 = >9kts.
    :param maxvis: Maximum daytime visibility in metres.
    :return: A tuple containing minimum visibility(M), dusk visibility(M) and fog point(deg C).
    """
    duskvis = maxvis * 0.8

    if windfactor == 1:
        fogpt = round(dewpt - (math.log(maxvis / 3000) / math.log(2)), 1)
        minvis = int(maxvis * 0.33)

    elif windfactor == 2:
        fogpt = round(dewpt - (math.log(maxvis / 2000) / math.log(2)), 1)
        minvis = int(maxvis * 0.5)

    else:
        fogpt = round(dewpt - (math.log((3 * maxvis) / 4000) / math.log(2)), 1)
        minvis = int(maxvis * 0.75)

    if temp_min - dewpt == 0:
        minvis = minvis
    if temp_min - dewpt < 0:
        minvis /= 2
    if temp_min - dewpt < -1:
        minvis /= 2
    if temp_min - dewpt < -2:
        minvis /= 2
    if temp_min - dewpt < -3:
        minvis /= 2
    if temp_min - dewpt < -4:
        minvis /= 2
    if temp_min - dewpt < -5:
        minvis /= 2
    if temp_min - dewpt < -6:
        minvis /= 2
    if temp_min - dewpt < -7:
        minvis /= 2
    elif temp_min - dewpt > 0:
        minvis = duskvis

    return minvis, duskvis, fogpt


def calc_winds(grad_wind):
    """Calculate the surface mean wind speed and maximum gust expected for a given gradient wind speed. These
     figures are calculated using the figures supplied in the revised forecaster reference book, originally determined
     at RAF Honnington.

    :param grad_wind: The gradient wind in knots.
    :return: A tuple containing the wind speed and gust results for different stability profiles:
    0 - 1200ft wind
    2 - Steep inversion - mean
    2 - Steep inversion - gust
    3 - Shallow inversion - mean
    4 - Shallow inversion - gust
    5 - SALR from surface - mean
    6 - SALR from surface - gust
    7 - 1-2 deg C / 1000ft - mean
    8 - 1-2 deg C / 1000ft - gust
    9 - DALR from surface - mean
    10 - DALR from surface - gust
    11 - DALR to 6000ft - mean
    12 - DALR to 6000ft - gust
    13 - Large CU / Steep LR - mean
    14 - Large CU / Steep LR - gust
    """
    wind1200 = round(grad_wind * 0.9, 0)
    steep_inv = round(grad_wind * (1.0 / 6.0), 0)
    steep_inv_gust = steep_inv
    shallow_inv = round(grad_wind * (3.0 / 10.0), 0)
    shallow_inv_gust = round(shallow_inv * (30.0 / 25.0), 0)
    salr_sfc = round(grad_wind * (2.0 / 5.0), 0)
    salr_sfc_gust = round(salr_sfc * (35.0 / 25.0), 0)
    one_c1000 = round(grad_wind * (25.0 / 49.0), 0)
    one_c1000_gust = round(one_c1000 * (35.0 / 25.0), 0)
    dalr_sfc = round(grad_wind * (25.0 / 45.0), 0)
    dalr_sfc_gust = round(dalr_sfc * (24.5 / 15.0), 0)
    dalr_6000 = round(grad_wind * (30.0 / 49.5), 0)
    dalr_6000_gust = round(dalr_6000 * (24.5 / 15.0), 0)
    large_cu = round(grad_wind * (27.5 / 40.0), 0)
    large_cu_gust = round(large_cu * (24.5 / 15.0), 0)

    return wind1200, steep_inv, steep_inv_gust, shallow_inv, shallow_inv_gust, salr_sfc, salr_sfc_gust, one_c1000, \
           one_c1000_gust, dalr_sfc, dalr_sfc_gust, dalr_6000, dalr_6000_gust, large_cu, large_cu_gust


def calc_stratus_base(temp, dewpt, land_state):
    """Calculate the height of the base of stratus clouds base on the dewpoint and temperature of the air. The
    Base height in feet = z(T-Td) where z is a constant dependant on the land state: 350 = land warming
    450 = land cooling.
    :param temp: Air temperature in degrees C.
    :param dewpt: Dew point in degrees C.
    :param land_state: Land state where 1 = land warming otherwise land assumed to be cooling.
    :return: The height of the base of stratus cloud in feet.
    """
    if land_state is 1:
        factor = 350.0  # land warming
    else:
        factor = 450.0

    base = factor * (temp - dewpt)
    return base


def calc_stratus_base_alt(sfc_wind, air_state):
    """Calculate the height of the base of stratus clouds base on the surface wind and moisture of the air. The
    Base height in feet = surface wind * z where z is a constant dependant on the air state: 75 = moist air
    200 = dry air.
    :param sfc_wind: Surface wind speed in knots.
    :param air_state: 0 = dry air, 1 = moist air.
    :return: The height of the base of stratus cloud in feet.
    """
    if air_state is 1:
        factor = 75.0  # moist air
    else:
        factor = 200.0  # dry air

    base = factor * sfc_wind
    return base


def tests():
    """Perform tests of this modules functions."""

    print('Humid=50%, TempC=20.0 Dewpoint = ', calc_dewpoint(50, 20.0), 'C')
    print('WetbulbC=38.5, TempC=40.0, Pressure=1013: Dewpoint from wetbulb = ', calc_dewpoint_fm_wetbulb(40.0, 38.5, 1013), 'C')
    print('WetbulbC=38.5, TempC=40.0, Pressure=1013 Humidity from wetbulb = ', calc_humid_fm_wetbulb(40.0, 38.5, 1013), '%')
    print('0 deg C = ', celsius_to_kelvin(0), 'K')
    print('0 K = ', kelvin_to_celsius(0), 'C')
    print('0 deg C  = ', celsius_to_farenh(0), 'F')
    print('32 deg F  = ', farenh_to_celsius(32), 'C')
    print('1008.5 hPa, temp=25 C, sensor ht=3 M : QFE= ', calc_qfe(25, 1008.5, 3.0))
    print('QFE=1008.85 hPa, Site elevation=150 M : QNH= ', calc_qnh(1008.85, 150))
    print('QFE=1008.85 hPa, Site elevation=150 M, Temp=25 C : QFF= ', calc_qff(25, 1008.85, 150, 52))
    print('1008.5 hPa, temp=25 C, Site elevation=150 M, Sensor ht=3 M : (alt) QNH= ', calc_qnh_alt(1008.5, 25, 150, 3))
    print('Middle Wallop (Tmin=1C DewPt=4C Windfactor=1 Vismax=15000m - Min vis, Dusk vis, Fog point: '
          , middle_wallop(1, 4, 1, 15000))
    print('Surface wind / gust(kts) - gradient wind 25kts: ', calc_winds(25))
    print('Stratus base(ft) - Temp 8C, Dewpt 7C, Land warming - ', calc_stratus_base(8, 7.5, 1))


if __name__ == '__main__':
    tests()
