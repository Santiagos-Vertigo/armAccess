import RPi.GPIO as GPIO
import time

# --- Pin Definitions ---
RED_LED = 21     # GPIO21 → Physical Pin 40
GREEN_LED = 20   # GPIO20 → Physical Pin 38

# --- Setup ---
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(RED_LED, GPIO.OUT)
GPIO.setup(GREEN_LED, GPIO.OUT)

# --- Blink Loop ---
try:
    while True:
        # RED ON, GREEN OFF
        GPIO.output(RED_LED, GPIO.HIGH)
        GPIO.output(GREEN_LED, GPIO.LOW)
        print("RED ON, GREEN OFF")
        time.sleep(1)

        # RED OFF, GREEN ON
        GPIO.output(RED_LED, GPIO.LOW)
        GPIO.output(GREEN_LED, GPIO.HIGH)
        print("RED OFF, GREEN ON")
        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()
    print("GPIO cleaned up.")
