# report_menu.py

import csv
from datetime import datetime, timedelta

class ReportMenu:
    def __init__(self, file_path='/home/self/transactions.csv'):
        self.file_path = file_path

    def read_transactions(self):
        transactions = []
        try:
            with open(self.file_path, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    transactions.append(row)
        except FileNotFoundError:
            raise Exception(f"File {self.file_path} non trovato.")
        except csv.Error as e:
            raise Exception(f"Errore durante la lettura del file CSV: {str(e)}")
        return transactions

    def parse_date(self, date_string):
        try:
            return datetime.strptime(date_string, '%d/%m/%y')
        except ValueError:
            return datetime.strptime(date_string, '%d/%m/%Y')

    def calculate_absolute_total(self):
        total = 0
        try:
            transactions = self.read_transactions()
            for transaction in transactions:
                total += float(transaction['Valore'])
        except KeyError:
            raise Exception("Il campo 'Valore' non è presente nel file CSV")
        except ValueError as e:
            raise Exception(f"Errore nella conversione del valore a numero: {str(e)}")
        return total

    def calculate_monthly_total(self, year, month):
        total = 0
        try:
            transactions = self.read_transactions()
            for transaction in transactions:
                date = self.parse_date(transaction['Data'])
                if date.year == year and date.month == month:
                    total += float(transaction['Valore'])
        except KeyError as e:
            raise Exception(f"Campo mancante nel file CSV: {str(e)}")
        except ValueError as e:
            raise Exception(f"Errore nella conversione della data o del valore: {str(e)}")
        return total

    def calculate_daily_total(self, date):
        total = 0
        try:
            transactions = self.read_transactions()
            for transaction in transactions:
                trans_date = self.parse_date(transaction['Data']).date()
                if trans_date == date:
                    total += float(transaction['Valore'])
        except KeyError as e:
            raise Exception(f"Campo mancante nel file CSV: {str(e)}")
        except ValueError as e:
            raise Exception(f"Errore nella conversione della data o del valore: {str(e)}")
        return total

    def calculate_custom_period_total(self, start_date, end_date):
        total = 0
        try:
            transactions = self.read_transactions()
            for transaction in transactions:
                trans_date = self.parse_date(transaction['Data']).date()
                if start_date <= trans_date <= end_date:
                    total += float(transaction['Valore'])
        except KeyError as e:
            raise Exception(f"Campo mancante nel file CSV: {str(e)}")
        except ValueError as e:
            raise Exception(f"Errore nella conversione della data o del valore: {str(e)}")
        return total

# Esempio di utilizzo:
if __name__ == "__main__":
    report = ReportMenu()
    try:
        print(f"Totale assoluto: €{report.calculate_absolute_total():.2f}")
        print(f"Totale mensile (Ottobre 2024): €{report.calculate_monthly_total(2024, 10):.2f}")
        print(f"Totale giornaliero (21/10/2024): €{report.calculate_daily_total(datetime(2024, 10, 21).date()):.2f}")
        print(f"Totale periodo personalizzato (1-31 Ottobre 2024): €{report.calculate_custom_period_total(datetime(2024, 10, 1).date(), datetime(2024, 10, 31).date()):.2f}")
    except Exception as e:
        print(f"Si è verificato un errore: {str(e)}")