from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from time import sleep

serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=1, block_orientation=90, rotate=0)

while True:
    with canvas(device) as draw:
        draw.text((0, 0), "D", fill="white")  # Only shows 1 char
    sleep(1)

