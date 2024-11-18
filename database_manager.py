import csv
import os
import logging
from datetime import datetime

logging.basicConfig(filename='database.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

class DatabaseManager:
    def __init__(self, clients_file='clienti.csv', transactions_file='transactions.csv'):
        self.clients_file = clients_file
        self.transactions_file = transactions_file
        if not os.path.exists(self.clients_file):
            self.create_empty_db(self.clients_file, ['nome', 'cognome', 'uid', 'euro', 'data'])
        if not os.path.exists(self.transactions_file):
            self.create_empty_db(self.transactions_file, ['Data', 'Ora', 'Valore', 'Cliente', 'Tipo'])
        logging.info(f"Database manager inizializzato con {self.clients_file} e {self.transactions_file}")
        self.test_file_access()
        self.preview_transactions()

    def create_empty_db(self, file_name, fieldnames):
        with open(file_name, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
        logging.info(f"Nuovo file creato: {file_name}")

    def test_file_access(self):
        for file_path in [self.clients_file, self.transactions_file]:
            try:
                with open(file_path, 'r') as file:
                    logging.info(f"Accesso al file {file_path} riuscito")
            except IOError as e:
                logging.error(f"Impossibile accedere al file {file_path}: {str(e)}")

    def preview_transactions(self, n=5):
        try:
            with open(self.transactions_file, 'r') as file:
                reader = csv.DictReader(file)
                for i, row in enumerate(reader):
                    if i >= n:
                        break
                    logging.info(f"Riga {i}: {row}")
            logging.info(f"Anteprima delle prime {n} righe del file transazioni completata")
        except Exception as e:
            logging.error(f"Errore nella visualizzazione dell'anteprima delle transazioni: {str(e)}")

    def load_clients(self):
        clients = []
        try:
            with open(self.clients_file, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    clients.append(row)
            logging.info(f"Caricati {len(clients)} clienti dal database")
        except Exception as e:
            logging.error(f"Errore nel caricamento dei clienti: {str(e)}")
        return clients

    def save_clients(self, clients):
        try:
            with open(self.clients_file, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=['nome', 'cognome', 'uid', 'euro', 'data'])
                writer.writeheader()
                for client in clients:
                    writer.writerow(client)
            logging.info(f"Salvati {len(clients)} clienti nel database")
        except Exception as e:
            logging.error(f"Errore nel salvataggio dei clienti: {str(e)}")

    def add_client(self, nome, cognome, uid, euro, data):
        clients = self.load_clients()
        new_client = {
            'nome': nome,
            'cognome': cognome,
            'uid': uid,
            'euro': self.format_amount(euro),
            'data': data
        }
        clients.append(new_client)
        self.save_clients(clients)
        logging.info(f"Aggiunto nuovo cliente: {nome} {cognome}")

    def get_client_by_uid(self, uid):
        clients = self.load_clients()
        for client in clients:
            if client['uid'] == uid:
                return client
        logging.warning(f"Cliente con UID {uid} non trovato")
        return None

    def update_client_balance(self, uid, new_balance):
        clients = self.load_clients()
        for client in clients:
            if client['uid'] == uid:
                old_balance = float(client['euro'])
                new_balance = float(new_balance)
                formatted_new_balance = self.format_amount(new_balance)
                client['euro'] = formatted_new_balance
                self.save_clients(clients)
                logging.info(f"Aggiornato il saldo del cliente con UID {uid} da {old_balance} a {formatted_new_balance}")

                # Calcola la differenza, ma non aggiunge la transazione
                transaction_amount = new_balance - old_balance
                if transaction_amount > 0:
                    logging.info(f"Aumento del saldo rilevato: {self.format_amount(transaction_amount)}")

                # Restituisce le informazioni sulla transazione senza registrarla
                return {
                    'cliente': f"{client['nome']} {client['cognome']}",
                    'importo': self.format_amount(transaction_amount),
                    'vecchio_saldo': self.format_amount(old_balance),
                    'nuovo_saldo': formatted_new_balance
                }

        logging.warning(f"Tentativo di aggiornare il saldo di un cliente non esistente con UID {uid}")
        return None

    def delete_client(self, uid):
        clients = self.load_clients()
        original_count = len(clients)
        clients = [client for client in clients if client['uid'] != uid]
        if len(clients) < original_count:
            self.save_clients(clients)
            logging.info(f"Cliente con UID {uid} eliminato")
        else:
            logging.warning(f"Tentativo di eliminare un cliente non esistente con UID {uid}")

    def get_all_clients(self):
        return self.load_clients()

    def add_transaction(self, data, ora, valore, cliente, tipo):
        try:
            valore_float = float(valore)
            existing_transactions = self.get_all_transactions()
            for transaction in existing_transactions:
                if (transaction['Data'] == data and
                    transaction['Ora'] == ora and
                    abs(float(transaction['Valore']) - valore_float) < 0.01 and
                    transaction['Cliente'] == cliente and
                    transaction['Tipo'] == tipo):
                    logging.warning(f"Transazione simile già esistente, non aggiunta: {data}, {ora}, {valore}, {cliente}, {tipo}")
                    return

            # Se non esiste una transazione simile, aggiungi la nuova transazione
            with open(self.transactions_file, 'a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=['Data', 'Ora', 'Valore', 'Cliente', 'Tipo'])
                writer.writerow({
                    'Data': data,
                    'Ora': ora,
                    'Valore': self.format_amount(valore_float),
                    'Cliente': cliente,
                    'Tipo': tipo
                })
            logging.info(f"Nuova transazione aggiunta per {cliente}: {valore} ({tipo})")
        except Exception as e:
            logging.error(f"Errore nell'aggiunta della transazione: {str(e)}")

    def get_all_transactions(self):
        transactions = []
        try:
            with open(self.transactions_file, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    transactions.append(row)
            logging.info(f"Caricate {len(transactions)} transazioni")
        except Exception as e:
            logging.error(f"Errore nel caricamento delle transazioni: {str(e)}")
        return transactions

    def get_total_transactions(self):
        total = 0
        try:
            logging.info("Inizio calcolo del totale delle transazioni")
            
            if not os.path.exists(self.transactions_file):
                logging.error(f"Il file delle transazioni {self.transactions_file} non esiste")
                return 0

            transactions = self.get_all_transactions()
            logging.info(f"Numero di transazioni recuperate: {len(transactions)}")
            
            for index, transaction in enumerate(transactions):
                logging.debug(f"Elaborazione transazione {index}: {transaction}")
                try:
                    if "Banconote inserite per ricarica" in transaction.get('Tipo', ''):
                        amount = float(transaction.get('Valore', 0))
                        total += amount
                        logging.debug(f"Transazione {index}: Aggiunto {amount} al totale. Nuovo totale: {total}")
                    else:
                        logging.debug(f"Transazione {index}: Ignorata (tipo non corrispondente)")
                except ValueError as ve:
                    logging.warning(f"Transazione {index}: Valore non valido per 'Valore' - {ve}")
                except Exception as e:
                    logging.error(f"Errore imprevisto nell'elaborazione della transazione {index}: {str(e)}")

            logging.info(f"Totale transazioni di ricarica calcolato: {total}")
            return total
        except Exception as e:
            logging.error(f"Errore nel calcolo del totale delle transazioni: {str(e)}", exc_info=True)
            return 0

    def get_transactions_by_uid(self, cliente):
        transactions = []
        try:
            all_transactions = self.get_all_transactions()
            transactions = [t for t in all_transactions if t['Cliente'] == cliente]
            logging.info(f"Recuperate {len(transactions)} transazioni per il cliente {cliente}")
        except Exception as e:
            logging.error(f"Errore nel recupero delle transazioni per il cliente {cliente}: {str(e)}")
        return transactions

    def get_total_transactions_for_period(self, start_datetime, end_datetime):
        total = 0
        try:
            transactions = self.get_all_transactions()
            for transaction in transactions:
                try:
                    transaction_datetime = datetime.strptime(f"{transaction['Data']} {transaction['Ora']}", "%d/%m/%y %H:%M:%S")
                    if start_datetime <= transaction_datetime <= end_datetime and "" in transaction['Tipo']:
                        total += float(transaction['Valore'])
                except ValueError:
                    logging.warning(f"Valore non valido nella transazione: {transaction}")
            logging.info(f"Totale transazioni di ricarica calcolato per il periodo {start_datetime} - {end_datetime}: {total}")
            return total
        except Exception as e:
            logging.error(f"Errore nel calcolo del totale delle transazioni per periodo: {str(e)}")
            return 0

    def get_total_transactions_by_period(self, start_date, end_date):
        total = 0
        try:
            transactions = self.get_all_transactions()
            for transaction in transactions:
                try:
                    transaction_date = datetime.strptime(transaction['Data'], "%d/%m/%y")
                    if start_date <= transaction_date <= end_date and "Banconote inserite per ricarica" in transaction['Tipo']:
                        total += float(transaction['Valore'])
                except ValueError:
                    logging.warning(f"Valore non valido nella transazione: {transaction}")
            logging.info(f"Totale transazioni di ricarica calcolato per il periodo {start_date} - {end_date}: {total}")
            return total
        except Exception as e:
            logging.error(f"Errore nel calcolo del totale delle transazioni per periodo: {str(e)}")
            return 0

    @staticmethod
    def format_amount(amount):
        return f"{float(amount):.2f}"

# Script di test
if __name__ == "__main__":
    db_manager = DatabaseManager('clienti.csv', 'transactions.csv')
    # Aggiungi qui il codice per testare le funzionalità
    print("Test completato")