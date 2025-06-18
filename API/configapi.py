import requests
import configparser

def salvar_configuracao(api_url='http://172.20.10.2:8000/api/config', caminho_arquivo='config.ini'):
    try:
        response = requests.get(api_url)
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

        with open(caminho_arquivo, 'w') as configfile:
            config.write(configfile)

        print(f"✅ Configuração salva em {caminho_arquivo}")
    
    except requests.exceptions.RequestException as e:
        print("❌ Erro ao obter a configuração da API:")
        print(e)
