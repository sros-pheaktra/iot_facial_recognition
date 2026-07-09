import cv2


class Camera:

    def __init__(self):

        self.cap = cv2.VideoCapture(0)


        if not self.cap.isOpened():
            raise Exception(
                "Camera not found"
            )


    def get_frame(self):

        ret, frame = self.cap.read()

        if ret:
            return frame

        return None



    def release(self):

        self.cap.release()