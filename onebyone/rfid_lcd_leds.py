import time
from mfrc522 import SimpleMFRC522
from RPLCD.i2c import CharLCD
import RPi.GPIO as GPIO

# --- Ultrasonic Sensor Pins ---
TRIG = 23
ECHO = 24

# --- LED Pins ---
RED = 21
GREEN = 20
YELLOW = 16

# --- GPIO Setup ---
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(RED, GPIO.OUT)
GPIO.setup(GREEN, GPIO.OUT)
GPIO.setup(YELLOW, GPIO.OUT)
GPIO.output(TRIG, False)

# --- LCD Setup ---
lcd_ready = False
try:
    lcd = CharLCD(
        i2c_expander='PCF8574',
        address=0x27,
        port=1,
        cols=16,
        rows=2,
        charmap='A00',
        auto_linebreaks=True
    )
    lcd_ready = True
except Exception as e:
    print("LCD init failed:", e)

# --- RFID Reader Setup ---
reader = SimpleMFRC522()

# --- Function: Display on LCD ---
def lcd_message(line1="", line2=""):
    if lcd_ready:
        lcd.clear()
        lcd.write_string(line1.ljust(16))
        lcd.crlf()
        lcd.write_string(line2.ljust(16))
    else:
        print(line1)
        print(line2)

# --- Function: Measure Distance ---
def get_distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    return round(distance, 2)

# --- Function: LED Control ---
def set_leds(red=False, green=False, yellow=False):
    GPIO.output(RED, red)
    GPIO.output(GREEN, green)
    GPIO.output(YELLOW, yellow)

# --- Main Loop ---
try:
    while True:
        distance = get_distance()
        print(f"Distance: {distance} cm")

        if distance < 30:
            lcd_message("User Detected", "Scan your card")
            set_leds(red=False, green=False, yellow=True)  # Yellow ON
            print("Waiting for RFID...")

            try:
                id, text = reader.read()
                print(f"Card scanned! ID: {id}")
                lcd_message("RFID Detected", f"ID: {id}")
                set_leds(red=False, green=True, yellow=False)  # Green ON
                time.sleep(3)
            except Exception as e:
                lcd_message("RFID Error", str(e))
                set_leds(red=True, green=False, yellow=False)  # Red ON
                time.sleep(3)
        else:
            lcd_message("Waiting for user", f"Dist: {distance} cm")
            set_leds(red=False, green=False, yellow=False)
            time.sleep(0.5)

except KeyboardInterrupt:
    lcd_message("Shutting down", "Goodbye")
    set_leds(False, False, False)
    GPIO.cleanup()
