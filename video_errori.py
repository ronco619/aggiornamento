import tkinter as tk
from telegram import Bot

# Configura il tuo bot Telegram
TELEGRAM_TOKEN = "7751515790:AAHZvIOMXgyYZFWb9R-WO0soVsN%_MQr650"
CHAT_ID = "WB wash RCC"  # ID del chat o gruppo Telegram dove inviare i messaggi
bot = Bot(token=TELEGRAM_TOKEN)

# Funzione per inviare messaggi Telegram
def send_telegram_message(message):
    try:
        bot.send_message(chat_id=CHAT_ID, text=message)
        print("Message sent successfully")
    except Exception as e:
        print(f"Failed to send message: {e}")

# Funzione chiamata quando si preme il tasto AIUTO
def show_help_screen():
    help_screen = tk.Toplevel(root)
    help_screen.title("AIUTO")

    label = tk.Label(help_screen, text="Qual è il tuo problema?")
    label.pack(pady=10)

    # Opzioni per le risposte
    options = [
        "a) Mangiato un gettone",
        "b) Pista bloccata",
        "c) Portale bloccato",
        "d) Manca acqua"
    ]

    def send_response(response):
        send_telegram_message(response)
        help_screen.destroy()

    for option in options:
        button = tk.Button(help_screen, text=option, command=lambda opt=option: send_response(opt))
        button.pack(pady=5)

# Configurazione della finestra principale
root = tk.Tk()
root.title("Help Interface")
root.geometry("1024x800")
root.attributes('-fullscreen', True)

help_button = tk.Button(root, text="AIUTO", command=show_help_screen, height=2, width=20)
help_button.pack(pady=20)

root.mainloop()
