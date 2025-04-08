from ultralytics import YOLO

# Ruta del dataset
dataset_path = "C:\\Users\\kmilo\\Desktop\\proyecto_parqueadero\\dataset\\data.yaml"

# Cargar el modelo preentrenado
model = YOLO("yolov8s.pt")  

# Entrenar con hiperparámetros ajustados
model.train(
    data=dataset_path,  
    epochs=60,        
    imgsz=608,   # Ajuste del tamaño de la imagen
    batch=8,          
    workers=2,        
    device="cpu",     
    lr0=0.001,        
    lrf=0.01,         
    momentum=0.937,   
    weight_decay=0.0005,  
    hsv_h=0.015,      
    hsv_s=0.7,        
    hsv_v=0.4,        
    scale=0.5,        
    translate=0.2,    
    fliplr=0.5,       
    mixup=0.2         
)

# Evaluar el modelo después del entrenamiento
results = model.val()
print(results)