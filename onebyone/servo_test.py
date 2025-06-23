from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
import time

# --- Setup ---
factory = PiGPIOFactory()
servo = Servo(
    15,  # GPIO 15 (Pin 10)
    pin_factory=factory,
    min_pulse_width=0.5 / 1000,
    max_pulse_width=2.4 / 1000
)

# --- Test Movements ---
try:
    print("Center (90°)")
    servo.mid()
    time.sleep(2)

    print("Open (180°)")
    servo.max()
    time.sleep(2)

    print("Closed (0°)")
    servo.min()
    time.sleep(2)

    print("Back to Center")
    servo.mid()
    time.sleep(2)

except KeyboardInterrupt:
    print("Stopped.")

