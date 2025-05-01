import cv2
import json
import matplotlib.pyplot as plt
import numpy as np

def draw_bounding_boxes_with_contours(image_path, json_path):
    # Carregar a imagem
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Converte a imagem para RGB

    # Carregar os dados do JSON
    with open(json_path, 'r') as file:
        data = json.load(file)

    # Configurar o gráfico do matplotlib
    fig, ax = plt.subplots(1, figsize=(12, 8))
    ax.imshow(image_rgb)

    class_translation = {
        "ripe": "maduro",
        "unripe": "imaduro",
        "semi_ripe": "semi-maduro"
    }

    # Iterar sobre as previsões e desenhar os contornos
    for prediction in data['predictions']:
        if 'points' in prediction:
            points = prediction['points']
            points_array = np.array([(point['x'], point['y']) for point in points], np.int32)
            points_array = points_array.reshape((-1, 1, 2))

            # Desenhar o contorno (polígono fechado)
            color = (255, 255, 0)  # Cor do contorno (amarelo)
            thickness = 2  # Espessura do contorno
            cv2.polylines(image, [points_array], isClosed=True, color=color, thickness=thickness)

            # Adicionar rótulo com o nome da classe e a confiança diretamente na imagem
            class_name = prediction['class']
            confidence = prediction['confidence']
            translated_class_name = class_translation.get(class_name, class_name)

            label = f"{translated_class_name} {confidence * 100:.2f}%"

            # Coordenadas corretas para o texto
            org = (int(prediction['x'] - 50), int(prediction['y']))  # Ajuste a posição do texto

            # Adicionar fundo sobre o texto
            (text_width, text_height), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_DUPLEX, 0.6, 2)
            cv2.rectangle(image, (org[0]-15, org[1]-15 ), (org[0] + text_width , org[1] + text_height), (0, 0, 0), -1)

            # Colocar o texto sobre o fundo
            cv2.putText(image, label, org, cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 2)

    plt.axis('off')  # Desligar os eixos do gráfico

    # Salvar a imagem com os contornos no formato RGB
    output_image = image  # Converter para BGR antes de salvar
    cv2.imwrite('api/imagem_com_contornos.png', output_image)  # Salvar a imagem no formato BGR


