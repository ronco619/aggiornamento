# rfid.py

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time

class RFIDReader:
    def __init__(self):
        self.reader = None

    def setup(self):
        """
        Inizializza il lettore RFID.
        Restituisce True se l'inizializzazione ha successo, False altrimenti.
        """
        try:
            GPIO.setwarnings(False)
            self.reader = SimpleMFRC522()
            print("Lettore RFID inizializzato con successo.")
            return True
        except Exception as e:
            print(f"Errore nell'inizializzazione del lettore RFID: {str(e)}")
            return False

    def read_card(self):
        """
        Legge una carta RFID.
        Restituisce l'UID della carta in formato stringa se la lettura ha successo, None altrimenti.
        """
        if self.reader is None:
            print("Errore: Lettore RFID non inizializzato.")
            return None

        try:
            id, text = self.reader.read_no_block()
            if id is not None:
                uid = format(id, '08X')[:8].upper()
                print(f"Carta letta. UID: {uid}")
                return uid
            else:
                return None
        except Exception as e:
            print(f"Errore durante la lettura della carta: {str(e)}")
            return None

    def cleanup(self):
        """
        Pulisce le risorse GPIO utilizzate dal lettore RFID.
        """
        GPIO.cleanup()
        print("Pulizia GPIO completata.")

def test_rfid_reader():
    """
    Funzione di test per il lettore RFID.
    """
    reader = RFIDReader()
    if reader.setup():
        print("Test del lettore RFID in corso...")
        try:
            for _ in range(10):  # Prova a leggere per 10 secondi
                uid = reader.read_card()
                if uid:
                    print(f"Carta rilevata con successo. UID: {uid}")
                    break
                time.sleep(1)
            else:
                print("Nessuna carta rilevata durante il test.")
        finally:
            reader.cleanup()
    else:
        print("Impossibile inizializzare il lettore RFID per il test.")

if __name__ == "__main__":
    test_rfid_reader()