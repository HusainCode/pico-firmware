# pico-firmware

**Pico Firmware for Environmental Monitoring**

This firmware runs on a Raspberry Pi Pico (or compatible board) and collects sensor data from environmental sensors. It transmits this data securely to a remote server (`env-monitor-server`) over HTTPS.

---

## 🧩 System Overview

![Firmware Architecture](https://github.com/<your-username>/pico-firmware/blob/main/diagram.png) <!-- update this with real path if hosted -->

- **DHT22 Sensor** — Temperature & Humidity
- **ENS160 Sensor** — eCO2 & TVOC
- **WiFi STA_IF** — Connects to WLAN using `WifiManager`
- **Data Formatter** — Converts to JSON/CSV
- **HTTP Client** — Sends data via `urequests` POST to:



---

## 📦 Project Structure

| File             | Description                                 |
|------------------|---------------------------------------------|
| `pico.py`        | Main loop handling sensor read & transmit   |
| `network_client.py` | WiFi setup and connection logic         |
| `dht22.py`       | Driver for DHT22 sensor                     |
| `ens160.py`      | Driver for ENS160 sensor                    |
| `_init__.py`     | Module init                                 |
| `README.md`      | This file                                   |

---

## 🚀 Getting Started

1. Flash MicroPython to your Pico.
2. Clone this repo and upload files using `Thonny` or `rshell`.
3. Ensure the following hardware is connected:
 - DHT22 (GPIO pin as configured)
 - ENS160 (I²C)
4. Configure your WiFi credentials in `network_client.py`.

---

## 📡 API Endpoint

**POST** `/api/sensor`  
Payload Example (JSON):

```json
{
"temperature": 24.5,
"humidity": 48.2,
"eco2": 680,
"tvoc": 123
}
