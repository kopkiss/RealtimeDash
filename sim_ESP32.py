import requests
import random
import time

SERVER_URL = "http://127.0.0.1:8000/receive"

while True:
    random_value = random.randint(1, 20)
    data = {"value": random_value}

    try:
        response = requests.post(SERVER_URL, json=data)
        print(f"Sent: {data}, Response: {response.status_code}, {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

    time.sleep(2)  # ส่งข้อมูลทุก 5 วินาที