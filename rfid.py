import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import requests
import time

reader = SimpleMFRC522()

try:
    while True:
        print("Scan your RFID tag...")
        id, text = reader.read()
        uid_str = str(id)
        print("UID Scanned:", uid_str)

        # Send UID to Flask server
        response = requests.post('http://localhost:5000/scan', json={'uid': uid_str})
        print("Server Response:", response.json())

        time.sleep(2)  # wait before next scan

except KeyboardInterrupt:
    print("Exiting...")
finally:
    GPIO.cleanup()
