from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from time import sleep

def test_spi(device_num):
    print(f"Trying /dev/spidev0.{device_num}...")
    try:
        serial = spi(port=0, device=device_num, gpio=noop())
        matrix = max7219(serial, cascaded=1, block_orientation=0, rotate=0)
        with canvas(matrix) as draw:
            draw.text((0, 0), "✓", fill="white")
        print(f"Success on /dev/spidev0.{device_num}")
    except Exception as e:
        print(f"Failed on /dev/spidev0.{device_num}: {e}")

print("\n--- SPI CE Line Test ---")
test_spi(0)
sleep(2)
test_spi(1)

