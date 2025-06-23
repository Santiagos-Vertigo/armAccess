import spidev
import time

# --- SPI Setup ---
spi = spidev.SpiDev()
spi.open(0, 1)  # Use SPI bus 0, device 1 (CE1 = GPIO 7)
spi.max_speed_hz = 1000000  # Lowered to 1 MHz for stability

def write_register(register, data):
    print(f"Sending: register 0x{register:02X} → data 0x{data:02X}")
    spi.xfer([register, data])

# --- MAX7219 Initialization ---
print("Initializing MAX7219...")
init_sequence = [
    (0x09, 0x00),  # Decode mode: none
    (0x0A, 0x0F),  # Intensity: max
    (0x0B, 0x07),  # Scan limit: all 8 digits
    (0x0C, 0x01),  # Shutdown register: normal operation
    (0x0F, 0x01),  # Display test: all LEDs ON
]

for reg, val in init_sequence:
    write_register(reg, val)

# Wait 3 seconds to visually confirm all LEDs light up
time.sleep(3)

# Turn off display test
write_register(0x0F, 0x00)
print("Test complete. Display test turned off.")
