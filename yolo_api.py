from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import cv2
import os
import sys

# 🔥 IMPORTAR TU DETECTOR REAL
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, "dataset"))

from dataset.detector_fisico_enfermeria import DetectorFisicoEnfermeria

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# INICIALIZAR DETECTOR
# -------------------------
print("🚀 Iniciando detector de enfermería...")
detector = DetectorFisicoEnfermeria()

# Estado global
yolo_activo = False


# -------------------------
# STREAM DE VIDEO
# -------------------------
def generar_frames():
    global yolo_activo

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ No se pudo abrir la cámara")
        return

    while True:
        try:
            success, frame = cap.read()
            if not success:
                print("❌ No se pudo leer frame")
                break

            # 🔥 USAR TU LÓGICA REAL
            if yolo_activo:
                try:
                    print("🧠 Entrando a análisis...")
                    frame, dets = detector.analizar_frame(frame)
                except Exception as e:
                    print("❌ ERROR DETECTOR:", e)

            # Codificar imagen
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                continue

            frame_bytes = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

        except Exception as e:
            print("💥 Error en stream:", e)
            break

    cap.release()


@app.get("/yolo/video")
def video():
    return StreamingResponse(
        generar_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )


# -------------------------
# CONTROL YOLO
# -------------------------
@app.post("/yolo/iniciar")
def iniciar_yolo():
    global yolo_activo
    yolo_activo = True
    print("🟢 YOLO ACTIVADO")
    return {"resultado": "YOLO activado"}


@app.post("/yolo/detener")
def detener_yolo():
    global yolo_activo
    yolo_activo = False
    print("🔴 YOLO DESACTIVADO")
    return {"resultado": "YOLO desactivado"}


@app.get("/yolo/estado")
def estado_yolo():
    return {"corriendo": yolo_activo}