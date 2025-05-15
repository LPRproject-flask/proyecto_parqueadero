from ultralytics import YOLO

# Ruta del dataset
dataset_path = "C:\\Users\\kmilo\\Desktop\\proyecto_parqueadero\\dataset\\data.yaml"

# Cargar el modelo YOLO preentrenado
# Version de YOLO -> yolov8s.pt
model = YOLO("yolov8s.pt")  

# Entrenamiento del modelo con hiperparámetros ajustados
model.train(
    data=dataset_path,   # Ruta al archivo .yaml que contiene las configuraciones del dataset
    epochs=60,           # 60 epocas de entrenamiento
    imgsz=608,           # tamaño de las imagenes de entrada 608px
    batch=8,             # Tamaño del batch o lote (8 imágenes por lote)
    workers=2,           # (procesos paralelos) para cargar las imágenes del disco
    device="cpu",        # Se entrenará en la CPU 
    lr0=0.001,           # Tasa de aprendizaje
    lrf=0.01,            # Factor de reducción de la tasa de aprendizaje
    momentum=0.937,      # Momentum para el optimizador (mejora la convergencia)
    weight_decay=0.0005, # regularizacion de pesos para evitar sobreajuste
    hsv_h=0.015,         # Ajuste de hue en el espacio HSV (modificación aleatoria de colores para mejorar la generalización)
    hsv_s=0.7,           # Ajuste de saturación en el espacio HSV
    hsv_v=0.4,           # Ajuste de brillo en el espacio HSV
    scale=0.5,           # Factor de escala para aumentar la variedad de las imágenes
    translate=0.2,       # Factor de traslación (desplazamiento aleatorio) de las imágenes
    fliplr=0.5,          # Probabilidad de voltear horizontalmente las imágenes durante el entrenamiento
    mixup=0.2            # Técnica de "mixup" para crear imágenes compuestas mezclando dos imágenes
)

# Evaluar el modelo después de entrenar
results = model.val()

# Mostrar los resultados de la evaluación
print(results)
