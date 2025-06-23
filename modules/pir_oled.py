# inland_pir_oled.py

import RPi.GPIO as GPIO
import time
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw, ImageFont

# GPIO pin where PIR output is connected
PIR_PIN = 17  # GPIO15 (Physical pin 10)

# --- GPIO Setup ---
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)

# --- OLED Setup ---
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, width=128, height=64)
font = ImageFont.load_default()

# --- Function to show message on OLED ---
def show_message(msg):
    image = Image.new("1", (device.width, device.height))
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), "Inland Motion Sensor", font=font, fill=255)
    draw.text((0, 20), msg, font=font, fill=255)
    device.display(image)

# --- Startup Message ---
show_message("Initializing...")
time.sleep(2)

# --- Main Loop ---
try:
    while True:
        if GPIO.input(PIR_PIN):
            show_message("Motion Detected!")
        else:
            show_message("No Motion")
        time.sleep(1)

except KeyboardInterrupt:
    show_message("Exiting...")
    GPIO.cleanup()

