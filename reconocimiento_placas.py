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
        print("📌 Cargando modelo YOLO...")
        self.model = YOLO("C:\\Users\\kmilo\\Desktop\\proyecto_parqueadero\\runs\\detect\\train\\weights\\best.pt")
        self.text_extraction = TextExtraction()
        print("✅ Modelo YOLO cargado correctamente.")

    def detect_plate(self, image):
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
        resultados = []

        for (x1, y1, x2, y2) in plates:
            plate_roi = frame[y1:y2, x1:x2]
            text = self.text_extraction.extract_text(plate_roi)
            resultados.append({
                "text": text,
                "bbox": (x1, y1, x2, y2)
            })

        return resultados
