from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw, ImageFont

# Set up I2C interface and display
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, width=128, height=64)

# Create blank image for drawing
image = Image.new("1", (device.width, device.height))
draw = ImageDraw.Draw(image)

# Draw text
draw.text((0, 0), "Hello from Pi!", fill=255)
draw.text((0, 16), "OLED test OK", fill=255)

# Display the image on the OLED
device.display(image)

# Keep running to prevent script exit (optional)
while True:
    pass

