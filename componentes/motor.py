import RPi.GPIO as GPIO
import time

# Configuração
GPIO.setmode(GPIO.BCM)       # Usa a numeração BCM
GPIO.setwarnings(False)

# Defina o pino GPIO que você quer usar
pino_mosfet = 17             # GPIO17 (pino físico 11)

# Configura o pino como saída
GPIO.setup(pino_mosfet, GPIO.OUT)

def vibration():
    try:
        
            # Liga o módulo IRF520
            print("Ligado")
            GPIO.output(pino_mosfet, GPIO.HIGH)
            time.sleep(5)  # Mantém ligado por 5 segundos

            # Desliga o módulo IRF520
            print("Desligado")
            GPIO.output(pino_mosfet, GPIO.LOW)
           

    except KeyboardInterrupt:
        print("\nEncerrando o programa")

    finally:
         print("vibrou")
