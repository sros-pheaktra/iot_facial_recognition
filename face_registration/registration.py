import cv2
from pathlib import Path
from datetime import datetime
from face_registration.excel import ExcelManager
excel = ExcelManager()

class Registration:

    def __init__(
        self,
        camera,
        detector,
        embedding_model,
        database
    ):

        self.camera = camera
        self.detector = detector
        self.embedding_model = embedding_model
        self.database = database

        self.current_embedding = None
        self.image_path = None


    def capture_face(self, gui):

        frame = self.camera.get_frame()


        if frame is None:
            return


        faces = self.detector.detect(
            frame
        )


        if len(faces) == 1:

            face = faces[0]


            self.current_embedding = (
                self.embedding_model
                .generate(face)
            )


            filename = (
                datetime.now()
                .strftime("%Y%m%d_%H%M%S")
                + ".jpg"
            )


            self.image_path = (
                "images/" + filename
            )


            cv2.imwrite(
                self.image_path,
                frame
            )


            gui.update_status(
                "Face captured successfully"
            )


        elif len(faces) == 0:

            gui.update_status(
                "No face detected"
            )


        else:

            gui.update_status(
                "Multiple faces detected"
            )

    def update_preview(self, gui):

        frame = self.camera.get_frame()


        if frame is not None:

            gui.update_camera(frame)


        gui.window.after(
            30,
            lambda:
            self.update_preview(gui)
        )
    def register_user(self, gui):

        if self.current_embedding is None:

            gui.update_status(
                "Please capture face first"
            )

            return



        user = gui.get_user_data()


        if not user["name"] or not user["student_id"]:

            gui.update_status(
                "Please fill all fields"
            )

            return



        embedding_bytes = (
            self.database
            .embedding_to_bytes(
                self.current_embedding
            )
        )


        success = self.database.insert_user(
            name=user["name"],
            student_id=user["student_id"],
            major=user["major"],
            role=user["role"],
            image_path=self.image_path,
            embedding=embedding_bytes
        )


        if success:

            gui.update_status(
                "Registration Successful"
            )
            excel.save_user(
            name=user["name"],
            student_id=user["student_id"],
            major=user["major"],
            role=user["role"],
            image_path=self.image_path
        )

        else:

            gui.update_status(
                "Student ID already exists"
            )