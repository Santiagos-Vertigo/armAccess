import RPi.GPIO as GPIO
import time

LED_PIN = 21  # Use GPIO 21 (physical pin 40)

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setwarnings(False)

# Blink loop
try:
    while True:
        GPIO.output(LED_PIN, GPIO.HIGH)
        print("LED ON")
        time.sleep(1)

        GPIO.output(LED_PIN, GPIO.LOW)
        print("LED OFF")
        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()
    print("Clean exit.")
