import time
import threading
import cv2
import requests

import face_registration.cuda_config as cuda_config
from face_registration.camera import Camera
from face_registration.face_detector import FaceDetector
from face_registration.face_embedding import FaceEmbedding
from face_registration.database import Database
from face_registration.face_recognition import FaceRecognition


# =====================================
# Configuration
# =====================================

ESP32_IP = "10.30.0.173"

CONFIDENCE_THRESHOLD = 70
COOLDOWN = 5          # seconds

last_user = None
last_time = 0

# Optional: cooldown for unknown requests
last_denied = 0
DENIED_COOLDOWN = 3


# =====================================
# Initialize
# =====================================

camera = Camera()

detector = FaceDetector()

embedding_model = FaceEmbedding()

db = Database()

recognizer = FaceRecognition(db)


# =====================================
# HTTP Functions
# =====================================

def send_access(name):

    try:

        response = requests.get(
            f"http://{ESP32_IP}/access",
            params={
                "name": name
            },
            timeout=2
        )

        print("ESP32:", response.text)

    except Exception as e:

        print("ESP32 Error:", e)


def send_denied():

    try:

        requests.get(
            f"http://{ESP32_IP}/denied",
            timeout=2
        )

    except Exception as e:

        print("ESP32 Error:", e)


# =====================================
# Main Loop
# =====================================

while True:

    frame = camera.get_frame()

    if frame is None:
        break

    faces = detector.detect(frame)

    for face in faces:

        box = face.bbox.astype(int)

        x1, y1, x2, y2 = box

        embedding = embedding_model.generate(face)

        result = recognizer.recognize(embedding)

        if result:

            name = result["name"]

            confidence = result["score"] * 100

            label = f"{name} {confidence:.2f}%"

            color = (0, 255, 0)

            current_time = time.time()

            if confidence >= CONFIDENCE_THRESHOLD:

                if (
                    last_user != name or
                    current_time - last_time > COOLDOWN
                ):

                    user = db.get_user_by_name(name)

                    if user:

                        db.insert_attendance(
                            user_id=user[0],
                            name=user[1],
                            student_id=user[2],
                            major=user[3],
                            role=user[4],
                            confidence=confidence
                        )

                    threading.Thread(
                        target=send_access,
                        args=(name,),
                        daemon=True
                    ).start()

                    last_user = name
                    last_time = current_time
        else:

            label = "Unknown"

            color = (0, 0, 255)

            current_time = time.time()

            if current_time - last_denied > DENIED_COOLDOWN:

                threading.Thread(
                    target=send_denied,
                    daemon=True
                ).start()

                last_denied = current_time
        
        # Draw rectangle
        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            color,
            2
        )

        # Draw label
        cv2.putText(
            frame,
            label,
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            color,
            2
        )

    cv2.imshow(
        "Face Recognition",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


camera.release()

cv2.destroyAllWindows()