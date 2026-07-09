import face_registration.cuda_config as cuda_config
import cv2

from face_registration.camera import Camera
from face_registration.face_detector import FaceDetector
from face_registration.face_embedding import FaceEmbedding
from face_registration.database import Database
from face_recognition import FaceRecognition


camera = Camera()

detector = FaceDetector()

embedding_model = FaceEmbedding()

db = Database()

recognizer = FaceRecognition(db)


while True:

    frame = camera.get_frame()

    if frame is None:
        break


    faces = detector.detect(frame)


    for face in faces:

        # Get face box

        box = face.bbox.astype(int)

        x1, y1, x2, y2 = box


        # Generate embedding

        embedding = (
            embedding_model
            .generate(face)
        )


        result = recognizer.recognize(
            embedding
        )


        if result:

            name = result["name"]

            confidence = (
                result["score"] * 100
            )


            label = (
                f"{name} "
                f"{confidence:.2f}%"
            )


            color = (
                0,
                255,
                0
            )


        else:

            label = (
                "Unknown"
            )

            color = (
                0,
                0,
                255
            )


        # Draw face rectangle

        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            color,
            2
        )


        # Draw name + confidence

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


    if cv2.waitKey(1) == ord("q"):
        break



camera.release()

cv2.destroyAllWindows()