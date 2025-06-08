import time
import RPi.GPIO as GPIO
from hx711 import HX711

# Modo de numeração usado = BCM
GPIO.setmode(GPIO.BCM)

# Desativa warnings no terminal
GPIO.setwarnings(False)

PIN_DAT = 5   # DOUT (DT) (GPIO5 - Pino físico 29)
PIN_CLK = 6   # SCK (GPIO6 - Pino físico 31)

# Inicializa o HX711
hx = HX711(dout_pin=PIN_DAT, pd_sck_pin=PIN_CLK)

# Configura a leitura (canal A, ganho 128)
hx.set_gain_A(128)

# Fator de calibração conhecido
# -185000 vem de testes realizados com peso conhecido
# A balança não deve conter amostra no inicio
CALIBRATION_FACTOR = -2000000

# Zera a balança
hx.zero()


def get_weight():
    """Lê o peso em gramas usando o fator de calibração definido."""
    raw_val = hx.get_raw_data_mean()
    if raw_val is None:
        print("Erro na leitura do sensor.")
        return None
    weight_kg = raw_val / CALIBRATION_FACTOR  # peso em kg
    weight_g = weight_kg * 1000               # converte para gramas
    return (weight_g - 39.5)

def get_peso():
    try:
        print("Iniciando leituras. Pressione Ctrl+C para sair.")
        weight = get_weight()
        while weight < 100:
            weight = get_weight()
            if weight is not None:
                print(f"Peso: {weight:.1f} g")
            time.sleep(1)

        
    except KeyboardInterrupt:
        print("\nLeitura encerrada pelo usuário.")

    finally:
        # Libera os recursos dos GPIOs
        return weight
