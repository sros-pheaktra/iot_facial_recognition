import customtkinter as ctk
from PIL import Image, ImageTk
import cv2


class RegistrationGUI:

    def __init__(self):

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.window = ctk.CTk()

        self.window.title(
            "Face Registration System"
        )

        self.window.geometry(
            "500x700"
        )

        self.create_widgets()


    def create_widgets(self):

        # Camera Preview
        self.camera_label = ctk.CTkLabel(
            self.window,
            text=""
        )

        self.camera_label.pack(
            pady=10
        )


        # Name
        self.name_label = ctk.CTkLabel(
            self.window,
            text="Name"
        )

        self.name_label.pack()


        self.name_entry = ctk.CTkEntry(
            self.window,
            width=300
        )

        self.name_entry.pack(
            pady=5
        )


        # Student ID
        self.id_label = ctk.CTkLabel(
            self.window,
            text="Student ID"
        )

        self.id_label.pack()


        self.id_entry = ctk.CTkEntry(
            self.window,
            width=300
        )

        self.id_entry.pack(
            pady=5
        )


        # Major
        self.major_label = ctk.CTkLabel(
            self.window,
            text="Major"
        )

        self.major_label.pack()


        self.major_entry = ctk.CTkEntry(
            self.window,
            width=300
        )

        self.major_entry.pack(
            pady=5
        )


        # Role
        self.role_label = ctk.CTkLabel(
            self.window,
            text="Role"
        )

        self.role_label.pack()


        self.role_menu = ctk.CTkOptionMenu(
            self.window,
            values=[
                "Student",
                "Teacher",
                "Staff"
            ]
        )

        self.role_menu.pack(
            pady=10
        )


        # Capture Button
        self.capture_button = ctk.CTkButton(
            self.window,
            text="Capture Face"
        )

        self.capture_button.pack(
            pady=10
        )


        # Register Button
        self.register_button = ctk.CTkButton(
            self.window,
            text="Register"
        )

        self.register_button.pack(
            pady=10
        )


        # Status
        self.status = ctk.CTkLabel(
            self.window,
            text="Waiting..."
        )

        self.status.pack(
            pady=20
        )


    def get_user_data(self):

        return {
            "name": self.name_entry.get(),
            "student_id": self.id_entry.get(),
            "major": self.major_entry.get(),
            "role": self.role_menu.get()
        }


    def update_status(self, message):

        self.status.configure(
            text=message
        )


    def update_camera(self, frame):

        # Convert OpenCV BGR -> RGB

        frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )


        image = Image.fromarray(frame)


        image = image.resize(
            (400, 300)
        )


        photo = ImageTk.PhotoImage(
            image
        )


        self.camera_label.configure(
            image=photo
        )


        # Prevent garbage collection
        self.camera_label.image = photo



    def run(self):

        self.window.mainloop()