# banknote_reader.py

import RPi.GPIO as GPIO
import time
import threading

INHIBIT_PIN = 20  # Pin per l'inibizione (output)
PULSE_PIN = 26    # Pin per la lettura degli impulsi (input)

class BanknoteReader:
    def __init__(self):
        self.setup_gpio()
        self.pulse_count = 0
        self.last_pulse_time = 0
        self.is_active = False
        self.callback = None

    def setup_gpio(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(INHIBIT_PIN, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(PULSE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def activate(self):
        GPIO.output(INHIBIT_PIN, GPIO.HIGH)
        self.is_active = True
        threading.Thread(target=self.check_pulses, daemon=True).start()

    def deactivate(self):
        GPIO.output(INHIBIT_PIN, GPIO.LOW)
        self.is_active = False

    def check_pulses(self):
        while self.is_active:
            current_state = GPIO.input(PULSE_PIN)
            current_time = time.time()

            if current_state == GPIO.LOW and (current_time - self.last_pulse_time) > 0.10:  # 100ms debounce
                self.pulse_count += 1
                self.last_pulse_time = current_time

            if (current_time - self.last_pulse_time) > 1 and self.pulse_count > 0:
                self.process_banknote()

            time.sleep(0.01)

    def process_banknote(self):
        amount = 0
        if self.pulse_count == 1:
            amount = 5
        elif self.pulse_count == 2:
            amount = 10
        elif self.pulse_count == 4:
            amount = 20
        elif self.pulse_count == 10:
            amount = 50


        if amount > 0 and self.callback:
            self.callback(amount)

        self.pulse_count = 0

    def set_callback(self, callback):
        self.callback = callback