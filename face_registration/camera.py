import cv2


class Camera:

    def __init__(self):
        self.url = "http://10.30.0.55:81/stream"

        self.cap = cv2.VideoCapture(0)


        if not self.cap.isOpened():
            raise Exception(
                "Camera not found"
            )


    def get_frame(self):

        ret, frame = self.cap.read()

        if ret:
            frame = cv2.resize(frame, (840, 840))
            return frame

        return None



    def release(self):

        self.cap.release()