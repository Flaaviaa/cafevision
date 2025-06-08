import board
import busio
import adafruit_ahtx0
from time import sleep

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_ahtx0.AHTx0(i2c)

def get_temperature():
	temperature = sensor.temperature
	print(f"Temperatura: {temperature:.2f}")
	sleep(2)
	return temperature

def get_humidity():
	humidity = sensor.relative_humidity
	print(f"Umidade: {humidity:.2f}")
	sleep(2)
	return humidity
