import cv2
import json
import matplotlib.pyplot as plt
import numpy as np

def draw_bounding_boxes_with_contours(image_path, json_path):
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    with open(json_path, 'r') as file:
        data = json.load(file)

    fig, ax = plt.subplots(1, figsize=(12, 8))
    ax.imshow(image_rgb)

    class_translation = {
    "ripe": "maduro",
    "unripe": "imaduro",
    "semi_ripe": "semi-maduro",
    "overripe": "muito maduro",
    "dry": "seco"
}


    for prediction in data['predictions']:
        
           
       class_name = prediction['class']
       confidence = prediction['confidence']
       translated_class_name = class_translation.get(class_name, class_name)
            
       label = f"{translated_class_name} {confidence * 100:.2f}%"
       ax.text(prediction['x']-50, prediction['y'], label, color='yellow', fontsize=12, fontweight='bold', 
                    bbox=dict(facecolor='black', alpha=0.5, edgecolor='none', boxstyle='round,pad=0.5'))

    plt.axis('off')

    # Salvar a imagem com textos
    plt.savefig('API/imagem.png', bbox_inches='tight', pad_inches=0, transparent=True)  # Salvar a imagem 

  


