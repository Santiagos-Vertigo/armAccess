from RPLCD.i2c import CharLCD

lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1,
              cols=16, rows=2, charmap='A00', auto_linebreaks=True)

lcd.write_string("Hello Diego!")
