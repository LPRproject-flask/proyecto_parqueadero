import cv2

# Abre la cámara (prueba con 0, 1, 2 si tienes varias)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ No se pudo abrir la cámara")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ No se pudo capturar el frame")
        break

    cv2.imshow('Prueba de Cámara', frame)  # Muestra la imagen en una ventana

    # Cierra la ventana con la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()