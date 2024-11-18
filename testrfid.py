from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO

reader = SimpleMFRC522()

try:
    print("Avvicina una carta al lettore...")
    id, text = reader.read()
    print(f"ID: {id}")
    print(f"Testo: {text}")
finally:
    GPIO.cleanup()