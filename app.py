from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import bcrypt  # Importar bcrypt
from flask import Flask, render_template, Response
import cv2
import numpy as np
from ultralytics import YOLO
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
import torch
from flask import Flask, request, jsonify
import os
from flask import Flask, redirect, url_for, session
import secrets
from models import Plate
from flask_sqlalchemy import SQLAlchemy
from models import db, Plate  
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
import base64
import io
from PIL import Image

app = Flask(__name__)

app.config['SECRET_KEY'] = 'e94b6a8f4b9e6c68c340de764c36e1c2'
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])

# Configuración de Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'poryectolpr@gmail.com'
app.config['MAIL_PASSWORD'] = 'jaau enfj rnij fhrj'  # NO tu contraseña normal
mail = Mail(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # 🔥 conectar db con la app.py

# Ruta del modelo TrOCR
##local_model_path = "C:\\Users\\kmilo\\Desktop\\proyecto_parqueadero\\trocr_model"
local_model_path = "trocr_model"

# Clase para extracción de texto con TrOCR
class TextExtraction:
    def __init__(self):
        model_name = "microsoft/trocr-base-stage1"
        self.processor = TrOCRProcessor.from_pretrained(model_name)
        self.model = VisionEncoderDecoderModel.from_pretrained(model_name)
        #self.processor = TrOCRProcessor.from_pretrained(local_model_path)
        #self.model = VisionEncoderDecoderModel.from_pretrained(local_model_path)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)

    def extract_text(self, plate_image_crop: np.ndarray) -> str:
        gray = cv2.cvtColor(plate_image_crop, cv2.COLOR_BGR2GRAY)
        enhanced = cv2.equalizeHist(gray)
        image_pil = cv2.cvtColor(enhanced, cv2.COLOR_GRAY2RGB)

        pixel_values = self.processor(images=image_pil, return_tensors="pt").pixel_values.to(self.device)
        generated_ids = self.model.generate(pixel_values)
        text = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

        clean_text = "".join(filter(str.isalnum, text)).upper()
        return clean_text
    


# Clase principal de reconocimiento de placas
class PlateRecognition:
    def __init__(self):
        print("📌 Cargando modelo YOLO...")
        ##self.model = YOLO("C:\\Users\\kmilo\\Desktop\\proyecto_parqueadero\\runs\\detect\\train\\weights\\best.pt")
        self.model = YOLO("model_weights/best.pt")
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
        
        for (x1, y1, x2, y2) in plates:
            plate_roi = frame[y1:y2, x1:x2]

            text = self.text_extraction.extract_text(plate_roi)
            print(f"📌 Placa detectada: {text}")

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        return frame

plate_recognition = PlateRecognition()


# Función para capturar video en vivo y enviarlo a la web
def generate_frames():
    cap = cv2.VideoCapture(0)

    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            frame = plate_recognition.process_frame(frame)

            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

# Ruta para la transmisión del video
@app.route('/video_feed')
def video_feed():
    return Response(plate_recognition.process_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Conectar a la base de datos
def get_db():
    conn = sqlite3.connect('db/data.db')
    conn.row_factory = sqlite3.Row  # Para acceder a las columnas como atributos
    return conn

# Ruta para la página de inicio de sesión
@app.route('/')
def login_page():
    return render_template('index.html')

# Ruta para manejar el inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user:
            stored_password = user['password']
            if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                return redirect(url_for('dashboard'))  
            else:
                return "Contraseña incorrecta", 400
        else:
            return "Usuario no encontrado", 400

    return render_template('index.html')  # Mostrar el formulario de login si el método es GET

# Ruta para el Dashboard
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# Ruta para registrar un usuario
@app.route('/register_user', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            return "Las contraseñas no coinciden", 400

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                           (username, email, hashed_password))
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            return "El usuario ya existe", 400
        conn.close()
        return redirect(url_for('login_user'))
    
    return render_template('register_user.html')

# Carpeta donde se guardarán las imágenes de los vehículos
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Asegurar que la carpeta existe
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Ruta para registrar placas
@app.route('/register_plate', methods=['POST'])
def register_plate():
    try:
        nombre = request.form.get('nombre')
        placa = request.form.get('placa')
        cedula = request.form.get('cedula')
        foto = request.files.get('foto')

        if not nombre or not placa or not cedula or not foto:
            return jsonify({"success": False, "error": "Todos los campos son obligatorios"}), 400
        
        # Guardar la imagen en la carpeta de uploads
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], foto.filename)
        foto.save(image_path)

        # Guardar en la base de datos
        conn = sqlite3.connect('db/data.db')
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO plates (nombre, placa, cedula, foto)
            VALUES (?, ?, ?, ?)
        """, (nombre, placa, cedula, foto.filename))
        conn.commit()
        conn.close()

        return jsonify({"success": True, "message": "Placa registrada con éxito"})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# Ruta para mostrar el formulario de registro de placa
@app.route('/register_plate')
def register_page():
    return render_template('register_plate.html')

#cierra sesion
@app.route('/logout')
def logout():
    # Elimina datos de sesión 
    session.clear()
    return redirect(url_for('login_page'))

#VERIFICA PLACA
@app.route('/check_plate', methods=['POST'])
def check_plate():
    data = request.get_json()
    plate = data.get('plates')

    if not plate:
        return jsonify({'error': 'No se proporcionó una placa'}), 400

    cleaned_plate = plate.strip().upper()

    conn = sqlite3.connect('db/data.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT nombre, placa, cedula, foto, email 
        FROM plates 
        WHERE placa = ?
    """, (cleaned_plate,))
    result = cursor.fetchone()
    conn.close()

    if result:
        nombre, placa, cedula, foto, email = result

        return jsonify({
            'registered': True,
            'owner_name': nombre,
            'plate_number': placa,
            'owner_id': cedula,
            'photo': foto,
            'email': email
        })
    else:
        return jsonify({'registered': False})

# Ruta para solicitar recuperación    
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']

        conn = sqlite3.connect('db/data.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        conn.close()

        if user:
            token = s.dumps(email, salt='recuperar-contrasena')
            link = url_for('reset_password', token=token, _external=True)

            msg = Message("Restablece tu contraseña",
                          sender=app.config['MAIL_USERNAME'],
                          recipients=[email])
            msg.body = f"Hola! Haz clic en este enlace para restablecer tu contraseña: {link}\n\nEste enlace expirará en 10 minutos."
            mail.send(msg)

        return render_template('mensaje_confirmacion.html')  # Muestra mensaje genérico
    return render_template('forgot_password.html')  # Tu plantilla HTML actual

    
# Ruta para restablecer contraseña

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        email = s.loads(token, salt='recuperar-contrasena', max_age=600)  # 600 segundos = 10 minutos
    except Exception:
        return "El enlace ha expirado o no es válido", 400

    if request.method == 'POST':
        nueva_contra = request.form['password']

        # Hasheamos la contraseña antes de guardarla
        hashed_password = bcrypt.hashpw(nueva_contra.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        conn = sqlite3.connect('db/data.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET password = ? WHERE email = ?", (hashed_password, email))
        conn.commit()
        conn.close()

        return redirect(url_for('login_page'))

    return render_template('nueva_contrasena.html') 

#al dar al boton capturar placa se envia la imagen y la procesa 
@app.route('/process_plate', methods=['POST'])
def process_plate():
    data = request.get_json()
    if not data or 'image' not in data:
        return jsonify({'error': 'No se proporcionó ninguna imagen'}), 400

    image_data = data['image'].split(",")[1]
    image_bytes = base64.b64decode(image_data)

    image_pil = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image_np = np.array(image_pil)
    image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    plates = plate_recognition.detect_plate(image_bgr)

    if not plates:
        return jsonify({'plate_text': 'No detectada'})

    # Suponemos que solo interesa la primera placa detectada
    x1, y1, x2, y2 = plates[0]
    plate_crop = image_bgr[y1:y2, x1:x2]
    plate_text = plate_recognition.text_extraction.extract_text(plate_crop)

    return jsonify({'plate_text': plate_text})

# Ejecutar la app
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Render asigna el puerto por la variable de entorno PORT
    app.run(host='0.0.0.0', port=port)                                                                                                                                       