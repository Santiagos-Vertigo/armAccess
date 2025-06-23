import time
from mfrc522 import SimpleMFRC522
from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
import RPi.GPIO as GPIO
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw, ImageFont

# --- GPIO Setup ---
PIR_PIN = 17  # PIR motion sensor
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)
GPIO.setwarnings(False)  # Optional: suppress reuse warnings

# --- Servo Setup ---
factory = PiGPIOFactory()
servo = Servo(
    15,  # Servo signal on GPIO15
    pin_factory=factory,
    min_pulse_width=0.5 / 1000,
    max_pulse_width=2.4 / 1000
)

# --- OLED Setup with error handling ---
oled_ready = False
try:
    serial = i2c(port=1, address=0x3C)
    device = ssd1306(serial, width=128, height=64)
    font = ImageFont.load_default()
    oled_ready = True
except Exception as e:
    print(f"OLED initialization failed: {e}")
    print("Continuing without OLED display...")

# --- RFID Reader Setup ---
reader = SimpleMFRC522()

def display_message(line1="", line2=""):
    if oled_ready:
        image = Image.new("1", (device.width, device.height))
        draw = ImageDraw.Draw(image)
        draw.text((0, 0), line1, font=font, fill=255)
        draw.text((0, 20), line2, font=font, fill=255)
        device.display(image)
    else:
        print(line1)
        print(line2)

# --- Startup State ---
servo.mid()  # Set servo to 90°
display_message("System Ready", "Waiting for motion...")
time.sleep(2)

# --- Main Loop ---
try:
    while True:
        if GPIO.input(PIR_PIN):  # Motion detected
            display_message("Motion Detected", "Scan RFID...")
            timeout = time.time() + 5  # Allow 5 seconds to scan

            while time.time() < timeout:
                id, text = reader.read_no_block()
                if id:
                    display_message("RFID Detected", f"ID: {id}")
                    time.sleep(1)

                    display_message("Access Granted", "Opening gate")
                    servo.max()  # Move to 180°
                    time.sleep(3)

                    display_message("Returning gate", "to 90 degrees")
                    servo.mid()
                    time.sleep(1)
                    break  # Exit RFID scan loop

                time.sleep(0.2)  # Avoid CPU hogging

            else:
                display_message("No RFID Found", "Timeout...")
                time.sleep(1)

        else:
            display_message("System Ready", "Waiting for motion...")
            time.sleep(0.5)

except KeyboardInterrupt:
    display_message("Shutting down", "Goodbye")
    GPIO.cleanup()
