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

# DHT22 Environmental Features (for dashboard):
# - Temperature: Shows how hot or cold the air is (in °C)
# - Humidity: Shows how much moisture is in the air (in %)

# Sources:
#        - https://randomnerdtutorials.com/esp32-esp8266-dht11-dht22-micropython-temperature-humidity-sensor/


import adafruit_dht
# import Adafruit_DHT # this libray will be used for now. When deployed will uses -> import dht


import os
# from machine import Pin
import board
from time import time, sleep


class DHT22:
    def __init__(self):

        self.sensor = dht.DHT22(Pin())

        # fahrenheit = (Celsius * 9/5) + 32
        # Temperature
        # Range: -40°C to +80°C
        # Accuracy: ±0.5°C
        # Resolution: 0.1°C
        self.temperature = 14

        # Humidity
        # Range: 0 % to
        # 100 % RH
        # Accuracy: ±2–5 % RH
        # Resolution: 0.1 % RH
        self.humidity = 33
        self.average_reading = None
        self.sensor_status = False # False is OFF, True is ON
        self.min_max_temperature = 0
        self.max_min_history = []

    # Check to see if the sensor is reading data
    def sensor_status(self):
        pass

    def data_timestamp(self):
        pass

    @property
    def average_readings(self):
        return self.average_readings

    @property
    def read_temperature(self):
        return self.temperature
    @property
    def read_humidity(self):
        return self.humidity

    def max_min_history(self):
        pass

    def heat_ndex(self):
        pass


dhtDevice = MockDHT()

print("Hello World")

