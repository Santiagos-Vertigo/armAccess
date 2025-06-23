import time
from mfrc522 import SimpleMFRC522
from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
import RPi.GPIO as GPIO

from luma.core.interface.serial import spi, noop
from luma.led_matrix.device import max7219
from luma.core.render import canvas
from RPLCD.i2c import CharLCD

# --- GPIO Setup ---
TRIG_PIN = 23
ECHO_PIN = 24
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)
GPIO.output(TRIG_PIN, False)
GPIO.setwarnings(False)

# --- Servo Setup ---
factory = PiGPIOFactory()
servo = Servo(
    15,
    pin_factory=factory,
    min_pulse_width=0.5 / 1000,
    max_pulse_width=2.4 / 1000
)

# --- LCD Setup ---
lcd_ready = False
try:
    lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1,
                  cols=16, rows=2, charmap='A00', auto_linebreaks=True)
    lcd_ready = True
except Exception as e:
    print(f"LCD initialization failed: {e}")

# --- LED Matrix Setup ---
led_ready = False
try:
    serial_led = spi(port=0, device=1, gpio=noop())  # CE1 = GPIO7
    device_led = max7219(serial_led, cascaded=1, block_orientation=0, rotate=0)
    led_ready = True
except Exception as e:
    print(f"LED Matrix initialization failed: {e}")

# --- RFID Reader Setup ---
reader = SimpleMFRC522()

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

# --- LED Matrix Display Function ---
def led_char(symbol):
    if led_ready:
        with canvas(device_led) as draw:
            draw.text((0, 0), symbol[:1], fill="white")

# --- Distance Measurement Function ---
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

# --- Startup State ---
servo.mid()
lcd_message("System Ready", "Waiting...")
led_char("R")
time.sleep(2)

# --- Main Loop ---
try:
    while True:
        distance_cm = get_distance()
        print(f"Distance: {distance_cm} cm")

        if distance_cm < 30:
            lcd_message("User Detected", "Scan RFID...")
            led_char("U")

            try:
                id, text = reader.read()
                lcd_message("RFID Detected", f"ID: {id}")
                led_char("V")
                time.sleep(1)

                lcd_message("Access Granted", "Opening gate")
                led_char("O")
                servo.max()
                time.sleep(3)

                lcd_message("Returning arm", "to position")
                led_char("C")
                servo.mid()
                time.sleep(1)

            except Exception as e:
                lcd_message("RFID Error", str(e))
                led_char("E")
                time.sleep(1)

        else:
            lcd_message("System Ready", "Waiting presence")
            led_char("R")
            time.sleep(0.5)

except KeyboardInterrupt:
    lcd_message("Shutting down", "Goodbye")
    led_char("X")
    GPIO.cleanup()
