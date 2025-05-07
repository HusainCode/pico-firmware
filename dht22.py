# Purpose:
#   Interface for DHT22 sensor to monitor temperature and humidity in real-time.
#   Designed for MicroPython environments like ESP32, ESP8266, or Raspberry Pi Pico.
#
# Key Attributes:
#   - temperature: Current temperature in Celsius
#   - humidity: Current relative humidity (%)
#   - average_reading: Running average of last N readings
#   - sensor_status: Health status of last sensor read
#
# Main Methods:
#   - update(): Reads temperature and humidity from the DHT22
#   - max_min_history(): Returns min/max temperature and humidity seen
#   - data_timestamp(): Timestamp of last successful read
#   - heat_index(): Calculates "feels like" temperature
#
# Example:
#   dht = DHT22(pin=4)
#   dht.update()
#   print(dht.read_temperature, dht.read_humidity)

from machine import Pin
import dht
import time


class DHT22:
    def __init__(self, pin):
        self.sensor = dht.DHT22(Pin(pin))
        self.temperature = None
        self.humidity = None
        self._timestamp = None
        self.sensor_status = False

        self._temp_max = float('-inf')
        self._temp_min = float('inf')
        self._hum_max = float('-inf')
        self._hum_min = float('inf')

        self._readings = []

    def update(self):
        try:
            self.sensor.measure()
            self.temperature = self.sensor.temperature()
            self.humidity = self.sensor.humidity()
            self._timestamp = time.ticks_ms()
            self.sensor_status = True

            self._temp_max = max(self._temp_max, self.temperature)
            self._temp_min = min(self._temp_min, self.temperature)
            self._hum_max = max(self._hum_max, self.humidity)
            self._hum_min = min(self._hum_min, self.humidity)

            self._readings.append((self.temperature, self.humidity))
            if len(self._readings) > 10:
                self._readings.pop(0)

        except Exception as e:
            self.sensor_status = False
            print(f"DHT22 read error: {e}")

    def data_timestamp(self):
        return self._timestamp

    def max_min_history(self):
        return {
            "temperature": {"min": self._temp_min, "max": self._temp_max},
            "humidity": {"min": self._hum_min, "max": self._hum_max}
        }

    @property
    def average_readings(self):
        if not self._readings:
            return None
        temps = [t for t, _ in self._readings]
        hums = [h for _, h in self._readings]
        return {
            "temperature": sum(temps) / len(temps),
            "humidity": sum(hums) / len(hums)
        }

    @property
    def read_temperature(self):
        return self.temperature

    @property
    def read_humidity(self):
        return self.humidity

    def heat_index(self):
        # Compute "feels like" temp using simplified Rothfusz formula
        if self.temperature is None or self.humidity is None:
            return None
        T = self.temperature
        R = self.humidity
        # valid only for T > 26°C, R > 40%
        HI = -8.784695 + 1.61139411 * T + 2.338549 * R \
             - 0.14611605 * T * R - 0.012308094 * (T**2) \
             - 0.016424828 * (R**2) + 0.002211732 * (T**2) * R \
             + 0.00072546 * T * (R**2) - 0.000003582 * (T**2) * (R**2)
        return round(HI, 2)


# Minimal test block
if __name__ == "__main__":
    dht22 = DHT22(pin=4)
    dht22.update()
    print(f"Temp: {dht22.read_temperature}°C, Humidity: {dht22.read_humidity}%")
    print(f"Heat Index: {dht22.heat_index()}°C")
    print("Avg:", dht22.average_readings)
