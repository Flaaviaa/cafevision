import requests
import os
import json

def enviar_para_api(status):
    API_URL = "http://172.20.10.2:8000/api/analasy"

    IMAGE_FILES = {
        'image_1': 'API/1-analisada.png',
        'image_2': 'API/2-analisada.png',
        'image_3': 'API/3-analisada.png'
    }

    JSON_FILES = {
        'j_imagem1': 'API/resultado_photo_1.json',
        'j_imagem2': 'API/resultado_photo_2.json',
        'j_imagem3': 'API/resultado_photo_3.json'
    }

    payload = {
        'status': status,
    }

    for key, filename in JSON_FILES.items():
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
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
            print(f"📸 Arquivo '{file_name}' preparado para envio.")
        else:
            print(f"⚠️ Arquivo '{file_name}' não encontrado.")

    if not files_to_upload and not payload:
        print("🚫 Nenhum dado ou arquivo para enviar. Abortando.")
        return

    try:
        response = requests.post(API_URL, data=payload, files=files_to_upload)

        if response.status_code == 201:
            print("✅ Sucesso! Resposta da API:")
            print(response.json())
        else:
            print(f"\n❌ Erro: Status inesperado {response.status_code}")
            try:
                print(response.json())
            except requests.exceptions.JSONDecodeError:
                print(response.text)

    except requests.exceptions.RequestException as e:
        print(f"\n❌ Erro de conexão com a API:")
        print(e)

    finally:
        for _, file_tuple in files_to_upload:
            file_tuple[1].close()
