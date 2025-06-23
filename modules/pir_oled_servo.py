import time
from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
import RPi.GPIO as GPIO
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw, ImageFont

# --- GPIO Setup ---
PIR_PIN = 17  # GPIO17 (Pin 11)
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)

# --- Servo Setup ---
factory = PiGPIOFactory()
servo = Servo(
    15,  # GPIO15 (Pin 10)
    pin_factory=factory,
    min_pulse_width=0.5/1000,
    max_pulse_width=2.4/1000
)

# --- OLED Setup ---
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, width=128, height=64)
font = ImageFont.load_default()

def display_message(line1="", line2=""):
    image = Image.new("1", (device.width, device.height))
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), line1, font=font, fill=255)
    draw.text((0, 20), line2, font=font, fill=255)
    device.display(image)

# --- Startup Position ---
servo.mid()  # Start at 90°
display_message("System Ready", "Gate at 90°")
time.sleep(2)

# --- Main Loop ---
try:
    while True:
        if GPIO.input(PIR_PIN):
            display_message("Motion Detected!", "Opening to 180°")
            servo.max()  # 180°
            time.sleep(3)

            display_message("Returning...", "Back to 90°")
            servo.mid()  # 90°
            time.sleep(1)
        else:
            display_message("No Motion", "Gate at 90°")
            servo.mid()  # Ensure it stays at 90°
            time.sleep(0.5)

except KeyboardInterrupt:
    display_message("Shutting down", "Goodbye!")
    GPIO.cleanup()
