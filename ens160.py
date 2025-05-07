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

import time
import ujson
import gc
import sys
import qwiic_ens160


class ENS160:
    def __init__(self):
        self.__ENS160 = qwiic_ens160.QwiicENS160()
        self.ON = True
        self.OFF = False
        self.sensor_status = False

        self._eCO2_level = 0
        self._total_TVOC = 0
        self._air_quality = 0
        self._timestamp = None

        self._eCO2_max = 0
        self._eCO2_min = float('inf')
        self._TVOC_max = 0
        self._TVOC_min = float('inf')

    @property
    def is_connected(self):
        connected = self.__ENS160.is_connected()
        if not connected:
            print("ENS160 not connected.", file=sys.stderr)
        return connected

    @property
    def eCO2_level(self):
        return self._eCO2_level

    @eCO2_level.setter
    def eCO2_level(self, value):
        self._eCO2_level = value

    @property
    def total_TVOC(self):
        return self._total_TVOC

    @total_TVOC.setter
    def total_TVOC(self, value):
        self._total_TVOC = value

    @property
    def air_quality(self):
        return self._air_quality

    @air_quality.setter
    def air_quality(self, value):
        self._air_quality = value

    def update(self):
        if not self.is_connected:
            return False

        try:
            self.__ENS160.begin()
            self.__ENS160.set_operating_mode(2)  # standard mode

            time.sleep(0.1)
            self._eCO2_level = self.__ENS160.get_eco2()
            self._total_TVOC = self.__ENS160.get_tvoc()
            self._air_quality = self.__ENS160.get_air_quality_index()
            self._timestamp = time.time()
            self.sensor_status = True

            self._update_min_max()

            return True
        except Exception as e:
            print(f"ENS160 update failed: {e}", file=sys.stderr)
            self.sensor_status = False
            return False

    def _update_min_max(self):
        self._eCO2_max = max(self._eCO2_max, self._eCO2_level)
        self._eCO2_min = min(self._eCO2_min, self._eCO2_level)
        self._TVOC_max = max(self._TVOC_max, self._total_TVOC)
        self._TVOC_min = min(self._TVOC_min, self._total_TVOC)

    def thresholds(self):
        def classify(val, bounds):
            for threshold, label in bounds:
                if val <= threshold:
                    return label
            return bounds[-1][1]

        co2_quality = classify(self._eCO2_level, [
            (1000, "Good"),
            (2000, "Moderate"),
            (5000, "Poor"),
            (float("inf"), "Unhealthy"),
        ])

        tvoc_quality = classify(self._total_TVOC, [
            (150, "Good"),
            (500, "Moderate"),
            (1000, "Poor"),
            (float("inf"), "Unhealthy"),
        ])

        return {
            "eCO2": co2_quality,
            "TVOC": tvoc_quality,
            "AQI": f"Level {self._air_quality}/5"
        }

    def data_timestamp(self):
        return self._timestamp

    def max_min_history(self):
        return {
            "eCO2": {"min": self._eCO2_min, "max": self._eCO2_max},
            "TVOC": {"min": self._TVOC_min, "max": self._TVOC_max}
        }



# Optional: Minimal test scaffold
if __name__ == "__main__":
    ens = ENS160()
    if ens.update():
        print(ens.thresholds())