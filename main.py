import time
from mfrc522 import SimpleMFRC522
from RPLCD.i2c import CharLCD
from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
import RPi.GPIO as GPIO

# --- GPIO Setup ---
TRIG = 23
ECHO = 24
RED = 21
GREEN = 20
YELLOW = 16
SERVO_PIN = 15

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(RED, GPIO.OUT)
GPIO.setup(GREEN, GPIO.OUT)
GPIO.setup(YELLOW, GPIO.OUT)
GPIO.output(TRIG, False)

# --- Servo Setup ---
factory = PiGPIOFactory()
servo = Servo(
    SERVO_PIN,
    pin_factory=factory,
    min_pulse_width=0.5 / 1000,
    max_pulse_width=2.4 / 1000
)

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

# --- RFID Reader ---
reader = SimpleMFRC522()

# --- Utility Functions ---
def lcd_message(line1="", line2=""):
    if lcd_ready:
        lcd.clear()
        lcd.write_string(line1.ljust(16))
        lcd.crlf()
        lcd.write_string(line2.ljust(16))
    else:
        print("[LCD]", line1)
        print("[LCD]", line2)

def get_distance():
    GPIO.output(TRIG, False)
    time.sleep(0.05)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    timeout_start = time.time()
    pulse_start = pulse_end = 0

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
        if pulse_start - timeout_start > 0.05:
            return 999

    timeout_start = time.time()
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()
        if pulse_end - timeout_start > 0.05:
            return 999

    pulse_duration = pulse_end - pulse_start
    distance_cm = pulse_duration * 17150
    return round(distance_cm, 2)

def set_leds(red=False, green=False, yellow=False):
    GPIO.output(RED, red)
    GPIO.output(GREEN, green)
    GPIO.output(YELLOW, yellow)

# --- Startup State ---
servo.mid()
set_leds(False, False, False)
lcd_message("System Ready", "No User Detected")

# --- Main Loop ---
try:
    last_state = None

    while True:
        distance = get_distance()
        print(f"Distance: {distance:.2f} cm")

        if 0 < distance <= 20:
            print("User detected! Starting RFID scan...")

            if last_state != "user_detected":
                lcd_message("User Detected", "Scan your card")
                last_state = "user_detected"

            set_leds(red=False, green=False, yellow=True)
            print("Waiting for RFID...")

            start_time = time.time()
            scanned = False

            while time.time() - start_time < 10:
                try:
                    card_id = reader.read_id()
                    print(f"Card scanned! ID: {card_id}")
                    lcd_message("RFID Detected", f"ID: {card_id}")
                    set_leds(red=False, green=True, yellow=False)

                    lcd_message("Access Granted", "Opening gate")
                    servo.max()
                    time.sleep(3)

                    lcd_message("Returning Arm", "to 90 deg")
                    servo.mid()
                    time.sleep(1)

                    scanned = True
                    break
                except Exception as e:
                    print("RFID read error:", e)

                time.sleep(0.3)

            if not scanned:
                print("RFID scan timeout.")
                lcd_message("Timeout", "Try again")
                set_leds(red=True, green=False, yellow=False)
                servo.mid()
                time.sleep(2)

            last_state = None

        else:
            if last_state != "no_user":
                lcd_message("System Ready", "No User Detected")
                last_state = "no_user"

            set_leds(False, False, False)
            servo.mid()
            time.sleep(0.5)

except KeyboardInterrupt:
    lcd_message("Shutting down", "Goodbye")
    set_leds(False, False, False)
    servo.mid()
    GPIO.cleanup()
