import requests
import configparser

API_URL = 'http://10.0.0.106:8000/api/config'

response = requests.get(API_URL)
response.raise_for_status()

config_data = response.json()

config = configparser.ConfigParser()

config['CONFIGURATION'] = {
    'unripe': str(config_data.get('unripe', 0)),
    'semi_ripe': str(config_data.get('semi_ripe', 0)),
    'ripe': str(config_data.get('ripe', 0)),
    'overripe': str(config_data.get('overripe', 0)),
    'dry': str(config_data.get('dry', 0))
}

config['CONFIGURATION_DEFAULT'] = {
    'unripe': '10',
    'semi_ripe': '4',
    'ripe': '45',
    'overripe': '15',
    'dry': '4'
}

with open('config.ini', 'w') as configfile:
    config.write(configfile)

print("✅ Configuração salva em config.ini")
