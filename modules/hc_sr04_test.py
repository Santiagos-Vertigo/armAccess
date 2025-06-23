import RPi.GPIO as GPIO
import time

# Pin Definitions
TRIG = 23  # GPIO23
ECHO = 24  # GPIO24

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.output(TRIG, False)
print("Waiting for sensor to settle...")
time.sleep(2)

def get_distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    start_time = time.time()
    stop_time = time.time()

    while GPIO.input(ECHO) == 0:
        start_time = time.time()

    while GPIO.input(ECHO) == 1:
        stop_time = time.time()

    elapsed = stop_time - start_time
    distance = (elapsed * 34300) / 2  # speed of sound = 34300 cm/s
    return round(distance, 2)

try:
    while True:
        dist = get_distance()
        print(f"Distance: {dist} cm")
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nMeasurement stopped by User")
    GPIO.cleanup()

