import tkinter as tk
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, CommandHandler

# Configura il tuo bot Telegram
TELEGRAM_TOKEN = "7751515790:AAHZvl0MXgyYZFWb9R-WO0soVsN5_MQr650"
CHAT_ID = "YOUR_CHAT_ID"  # Sostituisci con l'ID del chat o gruppo Telegram

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
        "c) Portale bloccata",
        "d) Manca acqua"
    ]

    def send_response(response):
        send_telegram_message(response)
        help_screen.destroy()

    for option in options:
        button = tk.Button(help_screen, text=option, command=lambda opt=option: send_response(opt))
        button.pack(pady=5)

# Funzione per ottenere l'ID della chat
async def get_chat_id(update: Update, context):
    chat_id = update.message.chat_id
    await update.message.reply_text(f"Your chat ID is: {chat_id}")

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", get_chat_id))

# Avvia il bot
app.run_polling()

# Configurazione della finestra principale
root = tk.Tk()
root.title("Help Interface")
root.geometry("1024x800")
root.attributes('-fullscreen', True)

help_button = tk.Button(root, text="AIUTO", command=show_help_screen, height=2, width=20)
help_button.pack(pady=20)

root.mainloop()
