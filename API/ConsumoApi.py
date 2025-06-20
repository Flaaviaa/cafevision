from roboflow import Roboflow
import json
import os
from collections import Counter
from .shapes import draw_bounding_boxes_with_contours



def count_classes(data):
    classes = [prediction['class'] for prediction in data['predictions']]
    class_counts = dict(Counter(classes))
    return class_counts


# Agrupamento por Confidence
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

        result['class_counts'] = class_counts
        result['confidence_counts'] = confidence_counts

        output_directory = "API"
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        image_name = os.path.splitext(os.path.basename(image_path))[0]

        output_file_path = os.path.join(output_directory, f"resultado_{image_name}.json")
        with open(output_file_path, 'w') as json_file:
            json.dump(result, json_file, indent=4)

        draw_bounding_boxes_with_contours(image_path, output_file_path,image_name)

        print(f"Resultado salvo em {output_file_path}")
    else:
        print("Nenhuma imagem foi selecionada.")
