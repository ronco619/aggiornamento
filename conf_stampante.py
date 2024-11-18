import csv
import os
import usb.core # type: ignore
import usb.util # type: ignore
import logging
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk # type: ignore

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Stampante:
    def __init__(self):
        self.dev = None
        self.ep_out = None
        self.config_file = '/home/self/config_scontrino.csv'
        self.logo_path = '/home/self/logo.png'
        self.load_config()
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

            self.ep_out = None
            for ep in intf:
                if usb.util.endpoint_direction(ep.bEndpointAddress) == usb.util.ENDPOINT_OUT:
                    self.ep_out = ep
                    break

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
        default_config = {
            'indirizzo': ['', '', '', ''],
            'saluto': '',
            'spazi_prima': 0,
            'spazi_dopo': 0,
            'stampa_logo': False,
            'stampa_prelievi': False,
            'stampa_mensili': False,
            'stampa_ricevute': False
        }

        if not os.path.exists(self.config_file):
            self.config = default_config
            self.save_config()
        else:
            with open(self.config_file, 'r') as f:
                reader = csv.DictReader(f)
                try:
                    row = next(reader)
                    self.config = default_config.copy()  # Start with default values

                    # Update config with values from CSV, if they exist
                    if 'indirizzo' in row:
                        self.config['indirizzo'] = row['indirizzo'].split('|')
                    if 'saluto' in row:
                        self.config['saluto'] = row['saluto']
                    if 'spazi_prima' in row:
                        self.config['spazi_prima'] = int(row['spazi_prima'])
                    if 'spazi_dopo' in row:
                        self.config['spazi_dopo'] = int(row['spazi_dopo'])
                    if 'stampa_logo' in row:
                        self.config['stampa_logo'] = row['stampa_logo'].lower() == 'true'
                    if 'stampa_prelievi' in row:
                        self.config['stampa_prelievi'] = row['stampa_prelievi'].lower() == 'true'
                    if 'stampa_mensili' in row:
                        self.config['stampa_mensili'] = row['stampa_mensili'].lower() == 'true'
                    if 'stampa_ricevute' in row:
                        self.config['stampa_ricevute'] = row['stampa_ricevute'].lower() == 'true'

                except StopIteration:
                    self.config = default_config

    def save_config(self):
        with open(self.config_file, 'w', newline='') as f:
            fieldnames = ['indirizzo', 'saluto', 'spazi_prima', 'spazi_dopo', 'stampa_logo', 'stampa_prelievi', 'stampa_mensili', 'stampa_ricevute']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            row = self.config.copy()
            row['indirizzo'] = '|'.join(row['indirizzo'])
            row['stampa_logo'] = str(row['stampa_logo'])
            row['stampa_prelievi'] = str(row['stampa_prelievi'])
            row['stampa_mensili'] = str(row['stampa_mensili'])
            row['stampa_ricevute'] = str(row['stampa_ricevute'])
            writer.writerow(row)

    def print_receipt(self):
        if not self.dev or not self.ep_out:
            logger.error("Impossibile stampare: stampante non connessa.")
            return False

        try:
            logger.info("Inizio stampa scontrino")
            
            if self.config['stampa_logo'] and os.path.exists(self.logo_path):
                logger.info("Stampa logo")
                self.dev.write(self.ep_out, b'\x1B\x61\x01')
                self.dev.write(self.ep_out, b'\x1B\x61\x00')
            else:
                self.dev.write(self.ep_out, b'\x1B\x61\x00')

            for line in self.config['indirizzo']:
                if line:
                    self.dev.write(self.ep_out, (line + '\n').encode('ascii'))
            
            self.dev.write(self.ep_out, b'\n' * self.config['spazi_prima'])
            self.dev.write(self.ep_out, (self.config['saluto'] + '\n').encode('ascii'))
            self.dev.write(self.ep_out, b'\n' * self.config['spazi_dopo'])
            
            self.dev.write(self.ep_out, b'\x1D\x56\x41\x00')
            logger.info("Stampa scontrino completata con successo")
            return True
        except Exception as e:
            logger.error(f"Errore durante la stampa dello scontrino: {str(e)}")
            return False

    def test_print(self):
        if not self.dev or not self.ep_out:
            logger.error("Impossibile stampare: stampante non connessa.")
            return False

        try:
            logger.info("Inizio test di stampa")
            self.dev.write(self.ep_out, b"Test di stampa\n")
            self.dev.write(self.ep_out, b"\x1D\x56\x41\x00")
            logger.info("Test di stampa completato con successo")
            return True
        except Exception as e:
            logger.error(f"Errore durante il test di stampa: {str(e)}")
            logger.error(f"Dettagli errore: {type(e).__name__}, {str(e)}")
            return False

class AnteprimaStampa(tk.Canvas):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.text = []
        self.line_height = 20

    def set_text(self, text):
        self.text = text
        self.redraw()

    def redraw(self):
        self.delete("all")
        y = 10
        for line in self.text:
            if line.startswith("[LOGO:"):
                self.create_text(self.winfo_width() / 2, y, text=line, anchor="n", font=("Courier", 10))
            else:
                self.create_text(10, y, text=line, anchor="w", font=("Courier", 10))
            y += self.line_height

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.stampante = Stampante()
        self.logo_path = self.stampante.logo_path
        self.fullscreen = False
        self.init_ui()
        self.toggle_fullscreen()

    def init_ui(self):
        self.title('Configurazione Stampante')
        
        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Escape>", self.end_fullscreen)

        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)

        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        logo_frame = ttk.Frame(left_frame)
        logo_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(logo_frame, text="Logo:").pack(side=tk.LEFT)
        self.logo_path_var = tk.StringVar(value=self.logo_path)
        ttk.Entry(logo_frame, textvariable=self.logo_path_var, state='readonly').pack(side=tk.LEFT, expand=True, fill=tk.X)
        ttk.Button(logo_frame, text="Sfoglia", command=self.browse_logo).pack(side=tk.LEFT)

        logo_checkbox_frame = ttk.Frame(left_frame)
        logo_checkbox_frame.pack(fill=tk.X, padx=5, pady=5)
        self.stampa_logo_var = tk.BooleanVar(value=self.stampante.config['stampa_logo'])
        ttk.Checkbutton(logo_checkbox_frame, text="Stampa logo", variable=self.stampa_logo_var, command=self.update_preview).pack(side=tk.LEFT)

        stampa_prelievi_frame = ttk.Frame(left_frame)
        stampa_prelievi_frame.pack(fill=tk.X, padx=5, pady=5)
        self.stampa_prelievi_var = tk.BooleanVar(value=self.stampante.config['stampa_prelievi'])
        ttk.Checkbutton(stampa_prelievi_frame, text="Stampa prelievi", variable=self.stampa_prelievi_var, command=self.update_preview).pack(side=tk.LEFT)

        stampa_mensili_frame = ttk.Frame(left_frame)
        stampa_mensili_frame.pack(fill=tk.X, padx=5, pady=5)
        self.stampa_mensili_var = tk.BooleanVar(value=self.stampante.config['stampa_mensili'])
        ttk.Checkbutton(stampa_mensili_frame, text="Stampa mensili", variable=self.stampa_mensili_var, command=self.update_preview).pack(side=tk.LEFT)

        stampa_ricevute_frame = ttk.Frame(left_frame)
        stampa_ricevute_frame.pack(fill=tk.X, padx=5, pady=5)
        self.stampa_ricevute_var = tk.BooleanVar(value=self.stampante.config['stampa_ricevute'])
        ttk.Checkbutton(stampa_ricevute_frame, text="Stampa ricevute", variable=self.stampa_ricevute_var, command=self.update_preview).pack(side=tk.LEFT)

        self.address_inputs = []
        for i in range(4):
            frame = ttk.Frame(left_frame)
            frame.pack(fill=tk.X, padx=5, pady=5)
            ttk.Label(frame, text=f"Riga {i+1}:").pack(side=tk.LEFT)
            entry = ttk.Entry(frame)
            entry.insert(0, self.stampante.config['indirizzo'][i])
            entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
            self.address_inputs.append(entry)

        saluto_frame = ttk.Frame(left_frame)
        saluto_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(saluto_frame, text="Saluto:").pack(side=tk.LEFT)
        self.saluto_input = ttk.Entry(saluto_frame)
        self.saluto_input.insert(0, self.stampante.config['saluto'])
        self.saluto_input.pack(side=tk.LEFT, expand=True, fill=tk.X)

        spazi_prima_frame = ttk.Frame(left_frame)
        spazi_prima_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(spazi_prima_frame, text="Spazi prima del saluto:").pack(side=tk.LEFT)
        self.spazi_prima_input = ttk.Spinbox(spazi_prima_frame, from_=0, to=10, width=5)
        self.spazi_prima_input.set(self.stampante.config['spazi_prima'])
        self.spazi_prima_input.pack(side=tk.LEFT)

        spazi_dopo_frame = ttk.Frame(left_frame)
        spazi_dopo_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(spazi_dopo_frame, text="Spazi dopo il saluto:").pack(side=tk.LEFT)
        self.spazi_dopo_input = ttk.Spinbox(spazi_dopo_frame, from_=0, to=10, width=5)
        self.spazi_dopo_input.set(self.stampante.config['spazi_dopo'])
        self.spazi_dopo_input.pack(side=tk.LEFT)

        button_frame = ttk.Frame(left_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(button_frame, text="Aggiorna Anteprima", command=self.update_preview).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Stampa", command=self.print_receipt).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Test Stampante", command=self.test_print).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Salva", command=self.save_config).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Esci", command=self.quit).pack(side=tk.LEFT, padx=5)

        self.preview = AnteprimaStampa(main_frame, width=400, bg="white")
        self.preview.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.update_preview()

    def toggle_fullscreen(self, event=None):
        self.fullscreen = not self.fullscreen
        self.attributes("-fullscreen", self.fullscreen)
        return "break"

    def end_fullscreen(self, event=None):
        self.fullscreen = False
        self.attributes("-fullscreen", False)
        return "break"

    def browse_logo(self):
        filetypes = [('Image files', '*.png *.jpg *.jpeg *.bmp *.gif')]
        filename = filedialog.askopenfilename(title="Seleziona logo", filetypes=filetypes)
        if filename:
            self.logo_path = filename
            self.logo_path_var.set(filename)
            self.update_preview()

    def update_preview(self):
        preview_text = []

        if self.stampa_logo_var.get() and os.path.exists(self.logo_path):
            preview_text.append(f"[LOGO: {os.path.basename(self.logo_path)}]")
            preview_text.append("")

        for entry in self.address_inputs:
            if entry.get():
                preview_text.append(entry.get())
        
        try:
            spazi_prima = int(self.spazi_prima_input.get())
        except ValueError:
            spazi_prima = 0
        preview_text.extend([''] * spazi_prima)

        preview_text.append(self.saluto_input.get())

        try:
            spazi_dopo = int(self.spazi_dopo_input.get())
        except ValueError:
            spazi_dopo = 0
        preview_text.extend([''] * spazi_dopo)

        if self.stampa_prelievi_var.get():
            preview_text.append("Stampa prelievi: Attivo")
        else:
            preview_text.append("Stampa prelievi: Disattivo")

        if self.stampa_mensili_var.get():
            preview_text.append("Stampa mensili: Attivo")
        else:
            preview_text.append("Stampa mensili: Disattivo")

        if self.stampa_ricevute_var.get():
            preview_text.append("Stampa ricevute: Attivo")
        else:
            preview_text.append("Stampa ricevute: Disattivo")
        
        self.preview.set_text(preview_text)

    def save_config(self):
        for i, entry in enumerate(self.address_inputs):
            self.stampante.config['indirizzo'][i] = entry.get()
        self.stampante.config['saluto'] = self.saluto_input.get()
        self.stampante.config['spazi_prima'] = int(self.spazi_prima_input.get())
        self.stampante.config['spazi_dopo'] = int(self.spazi_dopo_input.get())
        self.stampante.config['stampa_logo'] = self.stampa_logo_var.get()
        self.stampante.config['stampa_prelievi'] = self.stampa_prelievi_var.get()
        self.stampante.config['stampa_mensili'] = self.stampa_mensili_var.get()
        self.stampante.config['stampa_ricevute'] = self.stampa_ricevute_var.get()
        self.stampante.logo_path = self.logo_path
        self.stampante.save_config()
        messagebox.showinfo("Successo", "Configurazione salvata con successo!")

    def print_receipt(self):
        self.save_config()  # Save config before printing
        if self.stampante.print_receipt():
            messagebox.showinfo("Successo", "Scontrino stampato con successo!")
        else:
            messagebox.showerror("Errore", "Si è verificato un errore durante la stampa.")

    def test_print(self):
        if self.stampante.test_print():
            messagebox.showinfo("Successo", "Test di stampa completato con successo!")
        else:
            messagebox.showerror("Errore", "Si è verificato un errore durante il test di stampa.")

if __name__ == '__main__':
    main_window = MainWindow()
    main_window.mainloop()