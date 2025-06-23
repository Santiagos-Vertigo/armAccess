import time
from mfrc522 import SimpleMFRC522
from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
import RPi.GPIO as GPIO
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw, ImageFont
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
    15,  # GPIO15
    pin_factory=factory,
    min_pulse_width=0.5 / 1000,
    max_pulse_width=2.4 / 1000
)

# --- OLED Setup ---
oled_ready = False
try:
    serial = i2c(port=1, address=0x3C)
    device = ssd1306(serial, width=128, height=64)
    font = ImageFont.load_default()
    oled_ready = True
except Exception as e:
    print(f"OLED initialization failed: {e}")

# --- LCD Setup ---
lcd_ready = False
try:
    lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1,
                  cols=16, rows=2, charmap='A00', auto_linebreaks=True)
    lcd_ready = True
except Exception as e:
    print(f"LCD initialization failed: {e}")

# --- RFID Reader Setup ---
reader = SimpleMFRC522()

# --- Unified Display Function ---
def display_message(line1="", line2=""):
    if oled_ready:
        image = Image.new("1", (device.width, device.height))
        draw = ImageDraw.Draw(image)
        draw.text((0, 0), line1, font=font, fill=255)
        draw.text((0, 20), line2, font=font, fill=255)
        device.display(image)
    if lcd_ready:
        lcd.clear()
        lcd.write_string(line1.ljust(16))
        lcd.crlf()
        lcd.write_string(line2.ljust(16))
    if not oled_ready and not lcd_ready:
        print(line1)
        print(line2)

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
display_message("System Ready", "Waiting presence")
time.sleep(2)

# --- Main Loop ---
try:
    while True:
        distance_cm = get_distance()
        if distance_cm < 30:  # Presence detected
            display_message("User Detected", "Scan RFID...")
            timeout = time.time() + 5

            while time.time() < timeout:
                id, text = reader.read_no_block()
                if id:
                    display_message("RFID Detected", f"ID: {id}")
                    time.sleep(1)

                    display_message("Access Granted", "Opening gate")
                    servo.max()
                    time.sleep(3)

                    display_message("Returning gate", "to 90 degrees")
                    servo.mid()
                    time.sleep(1)
                    break

                time.sleep(0.2)

            else:
                display_message("No RFID Found", "Timeout...")
                time.sleep(1)

        else:
            display_message("System Ready", "Waiting presence")
            time.sleep(0.5)

except KeyboardInterrupt:
    display_message("Shutting down", "Goodbye")
    GPIO.cleanup()
