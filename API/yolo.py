import os
from ultralytics import YOLO

def train_yolov8(dataset_path, epochs=50, img_size=640):
    model = YOLO('yolov8n.pt')
    model.train(data=dataset_path, epochs=epochs, imgsz=img_size)
    return model

def predict_image(model, image_path):
    results = model.predict(image_path)
    results.show()
    return results

def save_model(model, save_path):
    model.save(save_path)
    print(f"Modelo salvo em: {save_path}")

def main():
    dataset_path = 'G:/Meu Drive/UTFPR/OFICINAS 2/Coffee Fruit Maturity ---.v1i.yolov8/data.yaml'
    print("Iniciando o treinamento do modelo YOLOv8...")
    model = train_yolov8(dataset_path)
   
    image_path = 'api/i.png'
    print(f"Realizando a inferência na imagem: {image_path}")
    predict_image(model, image_path)
    
    model_save_path = 'yolov8_trained_model.pt'
    save_model(model, model_save_path)

if __name__ == "__main__":
    main()
