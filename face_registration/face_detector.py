import insightface
import cv2

class FaceDetector:

    def __init__(self):

        self.model = insightface.app.FaceAnalysis(
            name="buffalo_l"
        )

        self.model.prepare(
            ctx_id=0,
            det_size=(640, 640)
        )


    def detect(self, frame):

        faces = self.model.get(frame)

        return faces


    def draw_faces(self, frame, faces):

        for face in faces:

            box = face.bbox.astype(int)

            x1, y1, x2, y2 = box


            # Draw bounding box
            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0,255,0),
                2
            )


        return frame