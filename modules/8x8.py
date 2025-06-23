from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from time import sleep

# Configure SPI connection for CE1 (GPIO7 / Pin 26)
serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=1, block_orientation=0, rotate=0)

# Display Test Sequence
try:
    print("Displaying characters on the 8x8 matrix...")

    chars = ["A", "B", "C", "✓", "R", "U", "O", "C", "E", "X"]

    while True:
        for symbol in chars:
            print(f"Showing: {symbol}")
            with canvas(device) as draw:
                draw.text((0, 0), symbol, fill="white")
            sleep(1)

except KeyboardInterrupt:
    print("Exiting LED test.")

