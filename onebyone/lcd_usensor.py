import time
import RPi.GPIO as GPIO
from RPLCD.i2c import CharLCD

# --- GPIO Pins for Ultrasonic ---
TRIG = 23
ECHO = 24
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.output(TRIG, False)
GPIO.setwarnings(False)

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

# --- Distance Function ---
def get_distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    duration = pulse_end - pulse_start
    distance_cm = (duration * 34300) / 2
    return round(distance_cm, 2)

# --- LCD Display Helper ---
def show_distance_on_lcd(dist):
    if lcd_ready:
        lcd.clear()
        lcd.write_string("Distance:")
        lcd.crlf()
        lcd.write_string(f"{dist:.2f} cm")
    else:
        print(f"Distance: {dist:.2f} cm")

# --- Main Loop ---
try:
    while True:
        distance = get_distance()
        show_distance_on_lcd(distance)
        time.sleep(1)

except KeyboardInterrupt:
    if lcd_ready:
        lcd.clear()
        lcd.write_string("Shutting down...")
    GPIO.cleanup()
