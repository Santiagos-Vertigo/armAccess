import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

try:
    print("Hold a tag near the RFID reader...")
    id, text = reader.read()
    print(f"ID: {id}")
    print(f"Text: {text}")
finally:
    print("Cleaning up...")
    GPIO.cleanup()
