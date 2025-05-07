# Purpose:
#  - Read sensor data from DHT22 and ENS160
#  - Serialize the data into JSON
#  - Send it securely to a Flask server running on Raspberry Pi 5
#
# Key Attributes:
#  - wifi_ssid: WiFi network name to connect the Pico to
#  - wifi_password: Password for WiFi network
#  - server_url: Flask server endpoint to POST data to
#  - api_key: Simple shared secret for basic security
#
# Main Methods:
#  - connect_wifi(): Connects Pico to WiFi
#  - read_sensor_data(): Read sensor data
#  - send_data(): Sends JSON payload to server with API Key in header

import time
import network
import urequests
import ujson
from machine import Pin
from dht22 import DHT22
from ens160 import ENS160


class WifiConnectionError(Exception): pass
class PicoError(Exception): pass


class WifiManager:
    def __init__(self, ssid: str, password: str, timeout: int = 10):
        self.ssid = ssid
        self.password = password
        self.timeout = timeout
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)

    def connect_wifi(self) -> None:
        try:
            self.wlan.connect(self.ssid, self.password)
            while not self.wlan.isconnected() and self.timeout > 0:
                time.sleep(1)
                self.timeout -= 1

            if not self.wlan.isconnected():
                raise WifiConnectionError("WiFi connection timed out")
        except Exception as e:
            raise WifiConnectionError(f"WiFi connection failed: {e}")


class Pico:
    def __init__(self, api_key: str, server_url: str, dht_pin: int = 4):
        self.api_key = api_key
        self.server_url = server_url
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        self.dht22 = DHT22(pin=dht_pin)
        self.ens160 = ENS160()

    def read_sensor_data(self) -> dict:
        self.dht22.update()
        self.ens160.update()

        return {
            "timestamp": time.ticks_ms(),
            "temperature": self.dht22.read_temperature,
            "humidity": self.dht22.read_humidity,
            "heat_index": self.dht22.heat_index(),
            "eco2": self.ens160.eCO2_level,
            "tvoc": self.ens160.total_TVOC,
            "aqi": self.ens160.air_quality,
            "status": {
                "dht22": self.dht22.sensor_status,
                "ens160": self.ens160.sensor_status
            }
        }

    def send_data(self) -> None:
        self.dht22.update()
        self.ens160.update()

        # Format: temp,humidity,heat_index,eCO2,TVOC,AQI,dht_status,ens_status
        payload = ",".join([
            f"{self.dht22.read_temperature:.2f}",
            f"{self.dht22.read_humidity:.2f}",
            f"{self.dht22.heat_index():.2f}" if self.dht22.heat_index() else "0.00",
            f"{self.ens160.eCO2_level:.2f}",
            f"{self.ens160.total_TVOC:.2f}",
            f"{self.ens160.air_quality}",
            str(int(self.dht22.sensor_status)),
            str(int(self.ens160.sensor_status))
        ])

        try:
            response = urequests.post(self.server_url,
                                      headers=self.headers,
                                      data=payload)
            response.close()
        except Exception as e:
            raise PicoError(f"Failed to send raw data: {e}")


if __name__ == "__main__":
    ssid = ""
    password = ""
    api_key = ""
    server_url = "http://raspberrypi.local:5000/api/sensor"

    wifi = WifiManager(ssid, password)
    try:
        wifi.connect_wifi()
    except WifiConnectionError as e:
        print(f"WiFi Error: {e}")
        raise SystemExit

    pico = Pico(api_key=api_key, server_url=server_url)
    pico.send_data()
