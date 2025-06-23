from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw

# Setup pigpio factory and calibrated servo
factory = PiGPIOFactory()
servo = Servo(
    15,
    pin_factory=factory,
    min_pulse_width=0.5/1000,   # 0.5ms
    max_pulse_width=2.4/1000    # 2.4ms
)

# Setup OLED via I2C
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, width=128, height=64)

def display_angle(label):
    image = Image.new("1", (device.width, device.height))
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), "Servo Position:", fill=255)
    draw.text((0, 16), f"{label}", fill=255)
    device.display(image)

# Sweep servo and update OLED display
try:
    while True:
        servo.min()
        display_angle("MIN (0°)")
        sleep(2)

        servo.mid()
        display_angle("MID (90°)")
        sleep(2)

        servo.max()
        display_angle("MAX (180°)")
        sleep(2)

except KeyboardInterrupt:
    print("Exiting...")
