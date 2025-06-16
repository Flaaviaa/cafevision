from roboflow import Roboflow
import json
import os
from collections import Counter, defaultdict
from .shapes import draw_bounding_boxes_with_contours


def count_classes(data):
    classes = [prediction['class'] for prediction in data['predictions']]
    class_counts = dict(Counter(classes))
    return class_counts


def count_confidence_ranges(data):
    confidence_counts = {}
    for i in range(0, 100, 10):
        confidence_counts[f"{i}-{i + 9}"] = 0
    confidence_counts["100"] = 0

    for prediction in data['predictions']:
        confidence = round(prediction['confidence'] * 100)
        if confidence == 100:
            confidence_counts["100"] += 1
        else:
            for i in range(0, 100, 10):
                if i <= confidence <= i + 9:
                    confidence_counts[f"{i}-{i + 9}"] += 1
                    break
    return confidence_counts


def ler_resultado(nome_arquivo):
    try:
        with open(nome_arquivo, 'r') as f:
            dados = json.load(f)
        return dados
    except FileNotFoundError:
        print(f"❌ Arquivo {nome_arquivo} não encontrado.")
        return None
    except json.JSONDecodeError:
        print(f"❌ Erro ao decodificar JSON em {nome_arquivo}.")
        return None
    
def calcular_media_por_classe(data):
    classes = defaultdict(list)
    for pred in data.get("predictions", []):
        classe = pred["class"]
        confianca = pred["confidence"]
        classes[classe].append(confianca)

    medias = {}
    for classe, valores in classes.items():
        medias[classe] = round((sum(valores) / len(valores)) * 100, 2)
    return medias




def gerarimagem(filename):
    rf = Roboflow(api_key="sIfKQIjbxPJfJo1lu4Bc")
    project = rf.workspace().project("coffee-fruit-maturity-befkg")
    model = project.version(2).model

    print(f"Photo {filename} initialized and ready.")
    image_path = filename

    if image_path:
        result = model.predict(image_path).json()

        class_counts = count_classes(result)
        confidence_counts = count_confidence_ranges(result)
        media_por_classe = calcular_media_por_classe(result)

        result['class_counts'] = class_counts
        result['confidence_counts'] = confidence_counts
        print(f"media:{media_por_classe}")

        output_directory = "API"
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        image_name = os.path.splitext(os.path.basename(image_path))[0]

        # JSON completo com predições + contagens
        output_file_path = os.path.join(output_directory, f"resultado_{image_name}.json")
        with open(output_file_path, 'w') as json_file:
            json.dump(result, json_file, indent=4)

        # JSON só com médias
        output_media_path = os.path.join(output_directory, f"resultado_final_{image_name}.json")
        with open(output_media_path, 'w') as media_file:
            json.dump(media_por_classe, media_file, indent=4)

        draw_bounding_boxes_with_contours(image_path, output_file_path, image_name)

        return media_por_classe
        print(f"Resultado salvo em {output_file_path}")
        print(f"Resultado final salvo em {output_media_path}")
    else:
        print("Nenhuma imagem foi selecionada.")


if __name__ == '__main__':
    gerarimagem('API/2.jpg')
