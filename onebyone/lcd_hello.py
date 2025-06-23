import time
from RPLCD.i2c import CharLCD

# --- LCD Setup ---
try:
    lcd = CharLCD(
        i2c_expander='PCF8574',
        address=0x27,
        port=1,
        cols=16,
        rows=2,
        charmap='A00',
        auto_linebreaks=True
    )
    lcd.clear()
    lcd.write_string("Hello, World!")
    lcd.crlf()
    lcd.write_string("LCD is working :)")
    time.sleep(5)
    lcd.clear()

except Exception as e:
    print("LCD initialization failed:", e)
