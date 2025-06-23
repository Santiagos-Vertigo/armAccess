from mfrc522 import SimpleMFRC522
import time

reader = SimpleMFRC522()

try:
    print("📶 Scan an RFID tag/card...")
    while True:
        id, text = reader.read()
        print(f"🆔 ID: {id}")
        print(f"📝 Text: {text}")
        time.sleep(2)

except KeyboardInterrupt:
    print("\n🛑 Exiting...")
finally:
    reader.cleanup()
