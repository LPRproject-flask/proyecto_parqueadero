import cv2
import numpy as np
from ultralytics import YOLO
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
import torch

# Ruta del modelo TrOCR
local_model_path = "C:\\Users\\kmilo\\Desktop\\proyecto_parqueadero\\trocr_model"

# Clase para extracción de texto con TrOCR
class TextExtraction:
    def __init__(self):
        self.processor = TrOCRProcessor.from_pretrained(local_model_path)
        self.model = VisionEncoderDecoderModel.from_pretrained(local_model_path)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)

    def extract_text(self, plate_image_crop: np.ndarray) -> str:
        # Convertir imagen a escala de grises y mejorar contraste
        gray = cv2.cvtColor(plate_image_crop, cv2.COLOR_BGR2GRAY)
        enhanced = cv2.equalizeHist(gray)
        image_pil = cv2.cvtColor(enhanced, cv2.COLOR_GRAY2RGB)

        pixel_values = self.processor(images=image_pil, return_tensors="pt").pixel_values.to(self.device)
        generated_ids = self.model.generate(pixel_values)
        text = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

        # Filtrar solo letras y números, y convertir a mayúsculas
        clean_text = "".join(filter(str.isalnum, text)).upper()
        return clean_text

# Clase principal de reconocimiento de placas
class PlateRecognition:
    def __init__(self):
        print("\U0001F4CC Cargando modelo YOLO...")
        self.model = YOLO("C:\\Users\\kmilo\\Desktop\\proyecto_parqueadero\\runs\\detect\\train\\weights\\best.pt")
        self.text_extraction = TextExtraction()
        print("✅ Modelo YOLO cargado correctamente.")

    def detect_plate(self, image):
        print("🔎 Procesando imagen para detección de placas...")
        results = self.model(image)
        plates = []

        for result in results:
            for box in result.boxes:
                conf = box.conf[0].item()
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                if conf > 0.3:
                    plates.append((x1, y1, x2, y2))

        return plates

    def process_frame(self, frame):
        plates = self.detect_plate(frame)
        
        for (x1, y1, x2, y2) in plates:
            plate_roi = frame[y1:y2, x1:x2]

            print("🔠 Extrayendo texto de la placa...")
            text = self.text_extraction.extract_text(plate_roi)
            print(f"📌 Placa detectada: {text}")

            # Dibujar la detección
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        return frame

    #### SE COMENTÓ EL CÓDIGO QUE PERMITE SELECCIONAR IMAGEN O VIDEO ####
    # def process_video(self, video_path):
    #     cap = cv2.VideoCapture(video_path)
    #
    #     if not cap.isOpened():
    #         print("❌ Error: No se pudo abrir el video.")
    #         return
    #
    #     while cap.isOpened():
    #         ret, frame = cap.read()
    #         if not ret:
    #             break  # Terminar si no hay más frames
    #
    #         processed_frame = self.process_frame(frame)
    #
    #         cv2.imshow("Deteccion en Video", processed_frame)
    #
    #         if cv2.waitKey(1) & 0xFF == ord('q'):  # Presiona 'q' para salir
    #             break
    #
    #     cap.release()
    #     cv2.destroyAllWindows()

#### INICIO DE CÁMARA WEB ####
plate_recognition = PlateRecognition()
cap = cv2.VideoCapture(0)  # 0 para la webcam principal

if not cap.isOpened():
    print("❌ Error: No se pudo acceder a la cámara.")
    exit()

print("🎥 Cámara en vivo iniciada. Presiona 'q' para salir.")

frame_count = 0
process_interval = 10 ##procesa cada 10 frames

while True:
    
    ret, frame = cap.read()
    if not ret:
        print("❌ Error: No se pudo capturar el frame de la cámara.")
        break

    if frame_count % process_interval == 0:
      print(f"🧠 Procesando frame {frame_count} con YOLO + TrOCR...")
      processed_frame = plate_recognition.process_frame(frame)
      
    else:
        print(f"🎞️ Mostrando frame {frame_count} sin procesamiento.")
        processed_frame = frame

    cv2.imshow("Detección en Vivo", processed_frame)
    frame_count += 1
    

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Presiona 'q' para salir
        break

cap.release()
cv2.destroyAllWindows()