import time
import digitalio
import board
import busio
import spidev
import RPi.GPIO as GPIO
from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import st7789
from componentes.carga import get_peso
from componentes.camera import Camera
from componentes.motor import vibration
from time import sleep
from componentes.aht21 import get_temperature, get_humidity
# ===============================
# Configuração do DISPLAY
# ===============================

# Pinos do display
cs_pin = digitalio.DigitalInOut(board.CE0)      # GPIO8
dc_pin = digitalio.DigitalInOut(board.D25)      # GPIO25
reset_pin = digitalio.DigitalInOut(board.D24)   # GPIO24

# SPI do display
spi_display = busio.SPI(clock=board.SCK, MOSI=board.MOSI)

# Inicialização do display
display = st7789.ST7789(
    spi_display,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    width=240,
    height=320,
    rotation=90,
    baudrate=64000000,
)

# ===============================
# Configuração do TOUCHSCREEN
# ===============================

# Pinos do touchscreen
T_CS = 7       # Chip Select
T_IRQ = 15     # Interrupção de toque (LOW quando pressionado)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(T_CS, GPIO.OUT)
GPIO.setup(T_IRQ, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Inicialização do SPI do touchscreen
spi_touch = spidev.SpiDev()
spi_touch.open(0, 0)  # SPI0, CS0 (compartilhado com display)
spi_touch.max_speed_hz = 1000000
spi_touch.mode = 0b00

# ===============================
# Cores e Fontes
# ===============================

MARROM = (19, 69, 139)
PRETO = (255, 255, 255)
BRANCO = (0, 0, 0)

font_grande = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 32)
font_media = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)

# ===============================
# Funções Auxiliares
# ===============================

def medir_texto(draw, texto, fonte):
    bbox = draw.textbbox((0, 0), texto, font=fonte)
    largura = bbox[2] - bbox[0]
    altura = bbox[3] - bbox[1]
    return largura, altura

def is_touching():
    return GPIO.input(T_IRQ) == GPIO.LOW  # Pressionado quando LOW

# ===============================
# Funções de Tela
# ===============================

def mostrar_texto_inicial():
    image = Image.new("RGB", (320, 240), BRANCO)
    draw = ImageDraw.Draw(image)

    texto1 = "CafeVision"
    w1, h1 = medir_texto(draw, texto1, font_grande)
    draw.text(((320 - w1) // 2, 20), texto1, font=font_grande, fill=PRETO)

    texto2 = "Carregando"
    w2, h2 = medir_texto(draw, texto2, font_media)
    draw.text(((320 - w2) // 2, 240 - h2 - 20), texto2, font=font_media, fill=PRETO)

    display.image(image)

def mostrar_mensagem_toque():
    image = Image.new("RGB", (320, 240), BRANCO)
    draw = ImageDraw.Draw(image)

    texto = "Toque na tela para iniciar"
    w, h = medir_texto(draw, texto, font_media)
    draw.text(((320 - w) // 2, (240 - h) // 2), texto, font=font_media, fill=PRETO)

    display.image(image)

def mostrar_parametros():
    image = Image.new("RGB", (320, 240), BRANCO)
    draw = ImageDraw.Draw(image)
    peso_g=get_peso()
    peso = f"Peso {peso_g:.1f}"
    w1, h1 = medir_texto(draw, peso, font_media)
    temperatura = get_temperature()
    temperature = f"Temperatura {temperatura:.2f}"
    w2, h2 = medir_texto(draw, temperature, font_media)
    umidade = get_humidity()
    humidity = f"Umidade {umidade:.2f}"
    w3, h3 = medir_texto(draw, humidity, font_media)

    y_inicio = 80
    draw.text(((320 - w1) // 2, y_inicio), peso, font=font_media, fill=PRETO)
    draw.text(((320 - w2) // 2, y_inicio + h1 + 10), temperature, font=font_media, fill=PRETO)
    draw.text(((320 - w3) // 2, y_inicio + h3 + 50), humidity, font=font_media, fill=PRETO)
    display.image(image)
    
    if peso_g > 100 :
        handle_button_press()

   
    print("Toque")
# ===============================
# Programa Principal
# ===============================

def handle_button_press():
    camera = Camera(0)

    for i in range(1, 4):
        filename = f"photo_{i}.png"
        camera.capture_photo(filename)
        vibration()
        sleep(8)
        print(f"Photo {filename} initialized and ready.")

    
def main():
        try:
           while True: 
                mostrar_texto_inicial()
                time.sleep(3)

                mostrar_mensagem_toque()

                print("Aguardando toque na tela...")
                while not is_touching():
                    time.sleep(0.05)

                # Aguarda soltar para não repetir
                while is_touching():
                    time.sleep(0.05)

                mostrar_parametros()

                # Mantém a tela ligada
                

        except KeyboardInterrupt:
            print("\nEncerrando...")

        finally:
            spi_touch.close()
            GPIO.cleanup()
