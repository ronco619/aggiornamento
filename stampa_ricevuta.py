import csv
import os
import usb.core
import usb.util
import logging
import time

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Stampante:
    def __init__(self):
        self.dev = None
        self.ep_out = None
        self.config_scontrino_file = '/home/self/config_scontrino.csv'
        self.config_stampante_file = '/home/self/config_stampante.csv'
        self.transactions_file = '/home/self/transactions.csv'
        self.connect_printer()

    def connect_printer(self):
        try:
            logger.info("Tentativo di connessione alla stampante")
            self.dev = usb.core.find(idVendor=0x0dd4, product="TG02-H")
            if self.dev is None:
                logger.error("Stampante non trovata")
                return
            logger.info(f"Stampante trovata: {self.dev}")
            if self.dev.is_kernel_driver_active(0):
                self.dev.detach_kernel_driver(0)
            self.dev.set_configuration()
            cfg = self.dev.get_active_configuration()
            intf = cfg[(0,0)]
            self.ep_out = usb.util.find_descriptor(
                intf,
                custom_match = \
                lambda e: \
                    usb.util.endpoint_direction(e.bEndpointAddress) == \
                    usb.util.ENDPOINT_OUT
            )
            if self.ep_out is None:
                logger.error("Endpoint OUT non trovato")
                return
            logger.info(f"Endpoint OUT trovato: {self.ep_out.bEndpointAddress}")
            logger.info("Connessione alla stampante riuscita")
        except Exception as e:
            logger.error(f"Errore durante la connessione alla stampante: {str(e)}")
            self.dev = None
            self.ep_out = None

    def load_config(self):
        config = {
            'indirizzo': [],
            'saluto': '',
            'spazi_prima': 0,
            'spazi_dopo': 0,
            'stampa_logo': False
        }
        try:
            with open(self.config_scontrino_file, 'r') as f:
                reader = csv.DictReader(f)
                row = next(reader)
                logger.debug(f"Riga letta dal file di configurazione: {row}")
                
                config['indirizzo'] = [line.strip() for line in row['indirizzo'].strip('"').split('|')]
                config['saluto'] = row['saluto'].strip()
                config['spazi_prima'] = int(row['spazi_prima'])
                config['spazi_dopo'] = int(row['spazi_dopo'])
                config['stampa_logo'] = row['stampa_logo'].lower() == 'true'
                
            logger.debug(f"Configurazione caricata: {config}")
        except Exception as e:
            logger.error(f"Errore durante la lettura del file di configurazione scontrino: {str(e)}")
        return config

    def should_print_receipt(self):
        try:
            with open(self.config_stampante_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['Opzione'] == 'stampa_ricevute':
                        return row['Valore'].lower() == 'true'
        except Exception as e:
            logger.error(f"Errore durante la lettura del file di configurazione stampante: {str(e)}")
        return False

    def get_last_transaction(self):
        try:
            with open(self.transactions_file, 'r') as f:
                reader = csv.DictReader(f)
                transactions = list(reader)
                if transactions:
                    return transactions[-1]
        except Exception as e:
            logger.error(f"Errore durante la lettura del file delle transazioni: {str(e)}")
        return None

    def print_receipt(self):
        if not self.dev or not self.ep_out:
            logger.error("Impossibile stampare: stampante non connessa.")
            return False

        config = self.load_config()
        last_transaction = self.get_last_transaction()

        try:
            logger.info("Inizio stampa scontrino")

            # Larghezza dello scontrino (in caratteri)
            receipt_width = 32

            # Stampa indirizzo
            for line in config['indirizzo']:
                if line:
                    centered_line = line.strip().center(receipt_width)
                    self.safe_write(self.ep_out, (centered_line + '\n').encode('cp437'))

            # Aggiunge uno spazio vuoto
            self.safe_write(self.ep_out, b'\n')

            if last_transaction:
                # Stampa data e ora
                date_time = f"{last_transaction['Data']},{last_transaction['Ora']}"
                centered_date_time = date_time.center(receipt_width)
                self.safe_write(self.ep_out, (centered_date_time + '\n'+ '\n'+ '\n').encode('cp437'))

                # Stampa il valore in un carattere più grande
                self.safe_write(self.ep_out, b'\x1B\x21\x20')  # Seleziona carattere più grande
                valore = last_transaction[   'Valore'].replace('€', '')  # Rimuove il simbolo dell'euro se presente
                centered_value = f"{valore} Euro".center(receipt_width)  
                self.safe_write(self.ep_out, (centered_value + '\n').encode('cp437'))
                self.safe_write(self.ep_out, b'\x1B\x21\x00')  # Ripristina carattere normale

            # Aggiunge gli spazi prima del saluto
            self.safe_write(self.ep_out, b'\n' * config['spazi_prima'])

            # Stampa il saluto
            centered_saluto = config['saluto'].center(receipt_width)
            self.safe_write(self.ep_out, (centered_saluto + '\n').encode('cp437'))

            # Stampa "ricevuta non fiscale"
            centered_ricevuta = "ricevuta non fiscale".center(receipt_width)
            self.safe_write(self.ep_out, (centered_ricevuta + '\n').encode('cp437'))

            # Aggiunge gli spazi dopo il saluto
            self.safe_write(self.ep_out, b'\n' * config['spazi_dopo'])

            # Taglia lo scontrino
            self.safe_write(self.ep_out, b'\x1D\x56\x41\x00')

            logger.info("Stampa scontrino completata con successo")
            return True
        except Exception as e:
            logger.error(f"Errore durante la stampa dello scontrino: {str(e)}")
        return False

    def safe_write(self, endpoint, data, retries=3, delay=1):
        for attempt in range(retries):
            try:
                endpoint.write(data, timeout=5000)
                return
            except usb.core.USBError as e:
                if e.errno == 110:  # Operation timed out
                    logger.warning(f"Tentativo {attempt + 1} fallito. Riprovo tra {delay} secondi.")
                    time.sleep(delay)
                else:
                    raise
        raise Exception("Impossibile scrivere sulla stampante dopo multipli tentativi")

def main():
    stampante = Stampante()
    if stampante.should_print_receipt():
        success = stampante.print_receipt()
        if success:
            logger.info("Scontrino stampato con successo")
        else:
            logger.error("Errore durante la stampa dello scontrino")
    else:
        logger.info("La stampa delle ricevute non è abilitata.")

if __name__ == '__main__':
    main()