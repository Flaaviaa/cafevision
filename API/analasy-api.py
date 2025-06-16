import requests
import os
import json


API_URL = "http://10.0.0.106:8000/api/analasy" # URL corrigida para o endpoint que funciona

IMAGE_FILES = {
    'image_1': 'API/photo_1-analisada.png',
    'image_2': 'API/photo_2-analisada.png',
    'image_3': 'API/photo_3-analisada.png'
}

JSON_FILES = {
    'j_imagem1': 'API/resultado_photo_1.json',
    'j_imagem2': 'API/resultado_photo_2.json',
    'j_imagem3': 'API/resultado_photo_3.json'
}

# 3. Adicione TODOS os novos campos ao payload
payload = {
    'status': 1,
}


for key, filename in JSON_FILES.items():
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            # Lê o arquivo e o transforma em um dicionário Python
            data = json.load(f)
            # Converte o dicionário de volta para uma string JSON e adiciona ao payload
            payload[key] = json.dumps(data)
            print(f"✅ Dados para '{key}' lidos de '{filename}'.")
    else:
        print(f"⚠️ Aviso: Arquivo de dados '{filename}' não encontrado.")


files_to_upload = []
for field_name, file_name in IMAGE_FILES.items():
    if os.path.exists(file_name):
        files_to_upload.append(
            (field_name, (file_name, open(file_name, 'rb'), 'image/png'))
        )
        print(f"Arquivo '{file_name}' encontrado e preparado para envio no campo '{field_name}'.")
    else:
        print(f"Aviso: Arquivo '{file_name}' não encontrado. O campo '{field_name}' será ignorado.")

if not files_to_upload and not payload:
    print("Nenhum dado ou arquivo para enviar. Abortando.")
    exit()
    
# Envio da Requisição
try:
    response = requests.post(API_URL, data=payload, files=files_to_upload)

    if response.status_code == 201:
        print("Resposta da API:")
        print(response.json())
    else:
        print(f"\n Erro! A API retornou um status inesperado: {response.status_code}")
        print("Resposta da API:")
        try:
            print(response.json())
        except requests.exceptions.JSONDecodeError:
            print(response.text)

except requests.exceptions.RequestException as e:
    print(f"\n❌ Erro de Conexão: Não foi possível conectar à API.")
    print(e)

finally:
    for _, file_tuple in files_to_upload:
        file_tuple[1].close()