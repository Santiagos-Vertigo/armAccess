import RPi.GPIO as GPIO
import time

# --- Pin Assignments ---
RED = 21     # GPIO21 → Physical Pin 40
GREEN = 20   # GPIO20 → Physical Pin 38
YELLOW = 16  # GPIO16 → Physical Pin 36

# --- GPIO Setup ---
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(RED, GPIO.OUT)
GPIO.setup(GREEN, GPIO.OUT)
GPIO.setup(YELLOW, GPIO.OUT)

# --- Loop: Cycle LEDs ---
try:
    while True:
        # RED
        GPIO.output(RED, GPIO.HIGH)
        GPIO.output(GREEN, GPIO.LOW)
        GPIO.output(YELLOW, GPIO.LOW)
        print("RED ON")
        time.sleep(1)

        # YELLOW
        GPIO.output(RED, GPIO.LOW)
        GPIO.output(GREEN, GPIO.LOW)
        GPIO.output(YELLOW, GPIO.HIGH)
        print("YELLOW ON")
        time.sleep(1)

        # GREEN
        GPIO.output(RED, GPIO.LOW)
        GPIO.output(GREEN, GPIO.HIGH)
        GPIO.output(YELLOW, GPIO.LOW)
        print("GREEN ON")
        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()
    print("Clean exit.")

