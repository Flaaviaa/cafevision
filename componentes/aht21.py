import board
import busio
import adafruit_ahtx0
from time import sleep

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_ahtx0.AHTx0(i2c)

def get_temperature():
	tempemperature = sensor.temperature
	sleep(2)
	print(f"cheguei")
	return temperature

def get_humidity():
	humidity = sensor.relative_humidity
	sleep(2)
	return humidity
