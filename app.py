import face_registration.cuda_config
from face_registration.camera import Camera
from face_registration.face_detector import FaceDetector
from face_registration.face_embedding import FaceEmbedding
from face_registration.database import Database
from face_registration.registration import Registration
from face_registration.gui import RegistrationGUI
from face_registration.excel import ExcelManager



camera = Camera()

detector = FaceDetector()

embedding_model = FaceEmbedding()

database = Database()

excel = ExcelManager()

registration = Registration(
    camera,
    detector,
    embedding_model,
    database
)



gui = RegistrationGUI()



# Connect buttons

gui.capture_button.configure(
    command=lambda:
    registration.capture_face(gui)
)


gui.register_button.configure(
    command=lambda:
    registration.register_user(gui)
)



gui.run()