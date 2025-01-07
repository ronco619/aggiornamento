import pigpio
import time

# Configurazione dei pin
RX_PIN = 15  # GPIO 15 (RX)
TX_PIN = 14  # GPIO 14 (TX)

# Inizializzazione di pigpio
pi = pigpio.pi()
if not pi.connected:
    exit()

# Configurazione dei pin
pi.set_mode(RX_PIN, pigpio.INPUT)
pi.set_mode(TX_PIN, pigpio.OUTPUT)

def bit_bang_uart(pin, baud_rate):
    pi.wave_clear()
    
    # Calcolo della durata di un bit
    bit_time = 1000000 / baud_rate
    
    # Creazione dell'onda per il bit di start
    pi.wave_add_generic([pigpio.pulse(0, 1<<pin, int(bit_time))])
    
    # Creazione delle onde per i dati (8 bit)
    for i in range(8):
        pi.wave_add_generic([pigpio.pulse(1<<pin, 0, int(bit_time))])
    
    # Creazione dell'onda per il bit di stop
    pi.wave_add_generic([pigpio.pulse(1<<pin, 0, int(bit_time))])
    
    return pi.wave_create()

def read_sensor():
    wave_id = bit_bang_uart(TX_PIN, 115200)
    
    while True:
        pi.wave_send_once(wave_id)
        time.sleep(0.1)
        
        count = 0
        data = []
        while count < 9:
            if pi.wait_for_edge(RX_PIN, pigpio.RISING_EDGE, 1):
                bit = pi.read(RX_PIN)
                data.append(bit)
                count += 1
        
        if len(data) == 9 and data[0] == 1 and data[1] == 1:
            distance = (data[3] << 8) | data[2]
            motion = data[4]
            print(f"Distanza: {distance} cm, Movimento: {'Sì' if motion else 'No'}")

try:
    read_sensor()
except KeyboardInterrupt:
    print("Programma interrotto dall'utente")
finally:
    pi.stop()