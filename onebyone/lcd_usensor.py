import time
import RPi.GPIO as GPIO
from RPLCD.i2c import CharLCD

# --- Pin Setup ---
TRIG_PIN = 23
ECHO_PIN = 24
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)
GPIO.output(TRIG_PIN, False)
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
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)

    start_time = time.time()
    stop_time = time.time()

    while GPIO.input(ECHO_PIN) == 0:
        start_time = time.time()
    while GPIO.input(ECHO_PIN) == 1:
        stop_time = time.time()

    elapsed = stop_time - start_time
    distance = (elapsed * 34300) / 2
    return round(distance, 2)

# --- LCD Display Function ---
def lcd_message(line1="", line2=""):
    if lcd_ready:
        lcd.clear()
        lcd.write_string(line1.ljust(16))
        lcd.crlf()
        lcd.write_string(line2.ljust(16))
    else:
        print(line1)
        print(line2)

# --- Main Loop ---
try:
    while True:
        dist = get_distance()
        print(f"Distance: {dist} cm")
        lcd_message("Ultrasonic:", f"{dist} cm")
        time.sleep(1)

except KeyboardInterrupt:
    lcd.clear()
    lcd.write_string("Goodbye!")
    GPIO.cleanup()
