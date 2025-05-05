#  Purpose:
#
#
#  Key Attributes:
#
#
#  Main Methods:
#
#
#  Example:

# ENS160 Air Quality Sensor Features:
# - eCO2: Equivalent CO₂ level estimation (in ppm), useful for indoor air quality
# - TVOC: Total Volatile Organic Compounds (in ppb), indicates chemical pollutants
# - AQI: Air Quality Index (scale 1–5), gives a general air quality score
# - Status: Sensor health or validity of measurements (e.g., NORMAL, WARMUP)

'''
in	Control digital I/O pins (e.g., turn LEDs on/off, read buttons)
I2C	Communicate with I²C devices like sensor_manager (ENS160, LCDs, etc.)
ADC	Read analog signals (e.g., from potentiometers, light sensor_manager)
PWM	Create pulse-width signals (for dimming LEDs, driving servos, etc.)
'''

"""
     Sources: 
           - https://github.com/sparkfun/qwiic_ens160_py
           - https://docs.sparkfun.com/qwiic_ens160_py/classqwiic__ens160_1_1_qwiic_e_n_s160.html#a3aae69c3519a68f347308d4514a2b2a7

"""

# from machine import I2C
import time
import ujson  # lighhtwegiht json
import gc  # Garbage collection
import sys
import qwiic_ens160


class ENS160:
    def __init__(self):
        self.__ENS160 = qwiic_ens160.QwiicENS160()
        self.ON = True
        self.OFF = False
        self.air_quality = None
        self.sensor_status = False # False is OFF, True is ON
        '''
        eCO₂ (Equivalent Carbon Dioxide) Levels in ppm:
        - 400–1000 ppm     → Good (typical fresh indoor air)
        - 1001–2000 ppm    → Moderate (drowsiness, stale air)
        - 2001–5000 ppm    → Poor (headaches, reduced focus)
        - 5001+ ppm        → Unhealthy (requires ventilation)
         Lower is better. Keep below 1000 ppm for comfort and focus.
        '''
        self.eCO2_level = 0

        '''
        TVOC (Total Volatile Organic Compounds) Levels in ppb:
        - 0–150 ppb     → Good
        - 151–500 ppb   → Moderate
        - 501–1000 ppb  → Poor
        - 1001+ ppb     → Unhealthy
        Lower is better. Aim for under 150 ppb indoors.
        '''
        self.total_TVOC = 0

    @property
    def is_connected(self):
        if self.__ENS160.is_connected() == self.OFF:
            print(f"The device isn't connected to the system.", file=sys.stderr)

    @property
    def air_quality(self):
        return self.air_quality

    @air_quality.setter
    def air_quality(self, value):
        self._air_quality = value

    @property
    def eCO2_level(self):
        return self.eCO2_level

    @eCO2_level.setter
    def eCO2_level(self, value):
        self._eCO2_level = value

    def thresholds(self):
        # Normal
        # Warning
        # Critical
        pass

    def data_timestamp(self):
        pass

    def max_min_history(self):
        pass

