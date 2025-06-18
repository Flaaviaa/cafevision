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
from API.ConsumoApi import gerarimagem
from API.analasyapi import enviar_para_api
from API.configapi import salvar_configuracao
import configparser
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
resultados = []
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
VERDE = (0,255,0)
VERMELHO = (255,0, 0)

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



    

def calcular_media_global():
    global resultados

    soma = {}
    contagem = {}

    for resultado in resultados:
        if not resultado:
            continue
        for classe, valor in resultado.items():
            soma[classe] = soma.get(classe, 0) + valor
            contagem[classe] = contagem.get(classe, 0) + 1

    medias = {}
    for classe in soma:
        medias[classe] = round(soma[classe] / contagem[classe], 2)

    return medias

def mostrar_resultados_final():
    global resultados

    image = Image.new("RGB", (320, 240), BRANCO)
    draw = ImageDraw.Draw(image)

    texto = "RESULTADO FINAL"
    w, h = medir_texto(draw, texto, font_media)
    y_inicio = 50
    x = (320 - w) // 2
    draw.text((x, y_inicio), texto, font=font_media, fill=PRETO)

    medias = calcular_media_global()
    espaco_linha = 30
    y_inicio = 80

    for i, (classe, valor) in enumerate(medias.items()):
        texto = f"{classe}: {valor:.2f}%"
        w, h = medir_texto(draw, texto, font_media)
        x = (320 - w) // 2
        y = y_inicio + i * espaco_linha
        draw.text((x, y), texto, font=font_media, fill=PRETO)

    display.image(image)
    sleep(10)



def status():

    # Usa a função que já calcula as médias globais
    medias = calcular_media_global()

    # Lê o config.ini
    config = configparser.ConfigParser()
    config.read("config.ini")

    if 'CONFIGURATION' not in config:
        return "⚠️ Configuração não encontrada."

    limites = {k: float(v) for k, v in config['CONFIGURATION'].items()}

    texto= "APROVADO"
    status_t=1
    # Verifica se todas as médias atingem os limites
    for classe, limite in limites.items():
        if classe in medias:
            media = medias[classe]
            if media < limite:
                print(f"Classe: {classe} | Média: {media:.2f}% | Limite: {limite:.2f}% ❌")
                texto= "REPROVADO"
                status_t=0

    image = Image.new("RGB", (320, 240), BRANCO)
    draw = ImageDraw.Draw(image)

    w, h = medir_texto(draw, texto, font_media)
    y_inicio = 50   
    x = (320 - w) // 2 
    cor = VERDE if status_t == 1 else VERMELHO
    draw.text((x, y_inicio), texto, font=font_media, fill=cor)

    display.image(image)
    sleep(10)
    return status_t

 



def mostrar_amostras(caminho,index):
    global resultados
    image = Image.new("RGB", (320, 240), BRANCO)
    draw = ImageDraw.Draw(image)


    texto = "AMOSTRA " + str(index)
    w, h = medir_texto(draw, texto, font_media)
    y_inicio = 50   
    x = (320 - w) // 2 
    draw.text((x, y_inicio), texto, font=font_media, fill=PRETO)

    resultado = gerarimagem(caminho)

    while len(resultados) <= index:
        resultados.append(None)

    resultados[index] = resultado
    print(f"{resultado}")
    y_inicio = 80
    espaco_linha = 30

    for i, (classe, valor) in enumerate(resultado.items()):
        texto = f"{classe}: {valor:.2f}%"
        w, h = medir_texto(draw, texto, font_media)
        x = (320 - w) // 2  # centralizado
        y = y_inicio + i * espaco_linha
        draw.text((x, y), texto, font=font_media, fill=PRETO)
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

    #sleep(10)
    print("Toque")
# ===============================
# Programa Principal
# ===============================

def processando():
    image = Image.new("RGB", (320, 240), BRANCO)
    draw = ImageDraw.Draw(image)


    texto = "PROCESSSANDO... "
    w, h = medir_texto(draw, texto, font_media)
    y_inicio = 50   
    x = (320 - w) // 2 
    draw.text((x, y_inicio), texto, font=font_media, fill=PRETO)
    display.image(image)
    
    
def handle_button_press():
    camera = Camera(0)

    for i in range(1, 4):
        filename = f"photo_{i}.png"
        processando()
        sleep(2)
        #camera.capture_photo(filename)
        mostrar_amostras(f'API/{i}.jpg', i)
        if i in (1,2):
            vibration()     
        #sleep(8)
        print(f"Photo {filename} initialized and ready.")

    
def main():
        try:
           mostrar_texto_inicial()
           while True: 
                time.sleep(3)
                
                mostrar_mensagem_toque()

                print("Aguardando toque na tela...")
                while not is_touching():
                    time.sleep(0.05)

                # Aguarda soltar para não repetir
                while is_touching():
                    time.sleep(0.05)
                    
                salvar_configuracao()
                mostrar_parametros()
                
                mostrar_resultados_final()
                status1=status()
                enviar_para_api(status1)
                # Mantém a tela ligada
                

        except KeyboardInterrupt:
            print("\nEncerrando...")

        finally:
            spi_touch.close()
            GPIO.cleanup()
