from luma.core.interface.serial import spi, noop
from luma.led_matrix.device import max7219
from luma.core.render import canvas
import time

serial = spi(port=0, device=1, gpio=noop())  # CS on CE1 = GPIO7
device = max7219(serial, width=8, height=8, block_orientation=90)
device.contrast(5)

while True:
    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="white", fill="black")
        draw.text((1, 0), "✓", fill="white")  # Unicode checkmark
    time.sleep(1)
