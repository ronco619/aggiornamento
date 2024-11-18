#!/bin/bash

# Nome dello script: restart_self.sh

# Ferma l'applicazione esistente (se in esecuzione)
pkill -f "python /home/self/Desktop/SELF/main.py"

# Attiva l'ambiente virtuale
source /home/self/pi-rfid/env/bin/activate

# Lancia l'applicazione
python /home/self/Desktop/SELF/main.py