# ┌──────────────────────────────────────────────────────────────────────────────┐
# │                                Purpose:                                     │
# │  A resilient network client module that handles secure HTTP POST            │
# │  communication from the Pico microcontroller to the remote                  │
# │  env-monitor-server.                                                        │
# │                                                                              │
# │  It includes retry logic, error handling, and human-readable interpretation │
# │  of standard HTTP status codes.                                             │
# └──────────────────────────────────────────────────────────────────────────────┘
#
# ┌──────────────────────────────────────────────────────────────────────────────┐
# │                             Key Attributes:                                 │
# │  - `https_status`: A dictionary mapping HTTP status codes to their          │
# │                    explanations (used for debugging / logs).                │
# └──────────────────────────────────────────────────────────────────────────────┘
#
# ┌──────────────────────────────────────────────────────────────────────────────┐
# │                             Main Methods:                                   │
# │  - `safe_post_with_retry(url, headers, data, timeout, retries, backoff)`    │
# │      Makes a POST request with exponential backoff and exception safety.    │
# │      Ensures response is returned or fails clearly after retries.           │
# └──────────────────────────────────────────────────────────────────────────────┘
#
# ┌──────────────────────────────────────────────────────────────────────────────┐
# │                               Example:                                      │
# │  client = NetworkClient()                                                   │
# │  data = {"sensor": "dht22", "temp": 24.5}                                    │
# │  headers = {"Authorization": "Bearer abc123"}                               │
# │  resp = client.safe_post_with_retry("https://env-monitor-server/data",      │
# │                                     headers=headers, data=data)             │
# │  print(resp)                                                                │
# └──────────────────────────────────────────────────────────────────────────────┘


import requests
import urequests
import time
import ujson
import network

class NetworkClientError(Exception): pass

class NetworkClient:
    def __init__(self):
        """
                            # HTTP Status Codes:
                             - 200 OK
                             - 201 Created
                             - 202 Accepted
                             - 204 No Content

                             - 400 Bad Request
                             - 401 Unauthorized
                             - 403 Forbidden
                             - 404 Not Found
                             - 405 Method Not Allowed

                             - 500 Internal Server Error
                             - 502 Bad Gateway
                             - 503 Service Unavailable
                             - 504 Gateway Timeout -
                            """
        self.https_status = {200: "Request succeeded, data received or sent successfully",
                             201: "New resource created (used after POST success)",
                             202: "Request accepted for processing, but not completed",
                             204: "No Content. Request succeeded, but no data returned",
                             400: "Client sent invalid data",
                             401: "Authentication required (wrong/missing API key)",
                             403: "You are not allowed to access this resource",
                             404: "URL or endpoint does not exist",
                             405: "Used wrong HTTP method (e.g., POST to GET endpoint)",
                             500: "Problem on server side",
                             502: "Server acting as gateway received bad response",
                             503: "Server overloaded or down",
                             504: "Server didn't respond in time"}

    def safe_post_with_retry(self, url: str, headers: dict, data: dict,
                             timeout: int = 5, retries: int = 3, backoff: float = 2.0) -> str:

        for attempt in range(retries):
            try:
                response = requests.post(url, headers=headers, data=ujson.dumps(data))
                status = response.status_code

                if status not in self.https_status:
                    raise NetworkClientError(f"Error, wrong status: {status}")

                response_raw_data = response.text
                response.close()

                return response_raw_data # data will be jsonfiy at the server

            except Exception as e:
                if attempt == retries - 1:
                    raise NetworkClientError(f"POST failed after {retries} retries") from e
                wait = backoff ** attempt
                print(f"[Retry {attempt + 1} Error {e} - waiting {wait}s before retry...")
                time.sleep(wait)







