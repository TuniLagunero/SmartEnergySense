import requests
import time
import random

SERVER = "http://127.0.0.1:5000/upload"  # local server

while True:
    current = round(random.uniform(0.2, 2.0), 2)  # Amperes
    voltage = 220
    power = round(current * voltage, 2)

    data = {"current": current, "voltage": voltage, "power": power}
    try:
        res = requests.post(SERVER, json=data)
        print(f"Sent: {data} | Status: {res.status_code}")
    except Exception as e:
        print("Error:", e)

    time.sleep(2)
