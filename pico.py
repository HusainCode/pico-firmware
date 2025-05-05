#  Purpose:
#  - Read sensor data from DHT22 and ESN160
#  - Serialize the data into JSON
#  - Send it securely to a Flask server running on Raspberry Pi 5
#
#  Key Attributes:
#  - wifi_ssid: WiFi network name to connect the Pico to
#  - wifi_password: Password for WiFi network
#  - server_url: Flask server endpoint to POST data to
#  - api_key: Simple shared secret for basic security
#
#  Main Methods:
#  - connect_wifi(): Connects Pico to WiFi
#  - read_sensor_data(): Read sensor data
#  - send_data(): Sends JSON payload to server with API Key in header

"""
Sources:
   - https://docs.micropython.org/en/latest/library/json.html
   - https://docs.micropython.org/en/latest/library/urequests.html
   - https://docs.micropython.org/en/latest/library/network.WLAN.html
   - https://randomnerdtutorials.com/raspberry-pi-pico-dht11-dht22-micropython/
"""

import time
import network
import dht
import requests
# from machine import Pin
import urequests
import ujson
from dht22 import DHT22
from ens160 import ENS160

class WifiConnectionError(Exception): pass
class PicoError(Exception): pass

class WifiManger:
    UP = True
    DOWN = False
    wifi_ssid = None
    wifi_password = None
    timeout = 10

    def __init__(self):
        self.wlan = network.Wlan(network.STA_IF)  # create Wi-Fi connection with station mode
        self.wlan_is_active = self.wlan.active(WifiManger.UP)

    def connect_wifi(self) -> None:
        try:
            self.wlan.connect(WifiManger.wifi_ssid, WifiManger.wifi_password)
            while not self.wlan.isconnected() and WifiManger.timeout > 0:
                time.sleep(1)
                WifiManger.timeout -= 1
            if not self.wlan.isconnected():
                raise WifiConnectionError(f"Failed to connect to WiFi after timeout of {WifiManger.timeout} seconds")
        except Exception as e:
            raise WifiConnectionError(f"Failed to connect to WiFi!{e}")


class Pico:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Pico, cls).__new__(cls)
        return cls._instance

    def __init__(self, api_key=None, server_url=None):
        if not hasattr(self, 'initialized'):
            self.api_key = api_key
            self.server_url = server_url

            self.headers = {
                "Content-Type": "text/plain",
                "Authorization": f"Bearer {self.api_key}"
            }



            self.dht22 = DHT22()
            self.ens160 = ENS160()

            self.temperature = round(self.dht22.temperature, 2)
            self.humidity = round(self.dht22.humidity, 2)
            self.co2 = round(self.ens160.co2, 2)

            self.initialized = True


    def send_dht22_data(self) -> None:
        # ADD MORE DATA
        payload = f"{self.dht22.temperature},{self.dht22.humidity},{self.dht22.average_reading},{self.dht22.sensor_status}"

        try:
            self.send_request(Pico.server_url, headers=Pico.headers, data=payload)
        except PicoError as e:
            raise PicoError("Falied to send DHT22 data to server")

    def send_ens160_data(self):
      # ADD MORE DATA
      payload = f"{self.ens160.eCO2_level}, {self.ens160.total_TVOC},{self.ens160.air_quality},{self.ens160.sensor_status}"

      try:
          self.send_request(Pico.server_url, headers=Pico.headers, data=payload)
      except PicoError as e:
         raise PicoError(f"Failed to send ENS160 data to server")
