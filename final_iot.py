import face_registration.cuda_config as cuda_config
from machine import Pin, SPI, SoftI2C, PWM
from mfrc522 import MFRC522
from machine_i2c_lcd import I2cLcd
import neopixel
import time
import cv2
from face_registration.camera import Camera
from face_registration.face_detector import FaceDetector
from face_registration.face_embedding import FaceEmbedding
from face_registration.database import Database
from face_recognition import FaceRecognition

#Face detection 
camera = Camera()
detector = FaceDetector()
embedding_model = FaceEmbedding()
db = Database()

recognizer = FaceRecognition(db)
#Inital Servo Motor
servo = PWM(Pin(4), freq=50)
servo.duty(26)   # Lock the door at startup

#Initial nexopixel
led = neopixel.NeoPixel(Pin(32), 16)

#Initial lcd
I2C_ADDR = 0x27
i2c = SoftI2C(sda=Pin(25), scl=Pin(26), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)

#Student data
students = {
    "1791731572129": {
        "name": "Sros Pheaktra",
        "student_id": "2024542",
        "role": "student",
        "major": "software development"
        }
    }
spi = SPI(1, baudrate=1000000, polarity=0, phase=0,
          sck=Pin(18), mosi=Pin(23), miso=Pin(19))

rdr = MFRC522(spi=spi, gpioRst=Pin(22), gpioCs=Pin(16))

print("Scan RFID...")

def unlock():
    #Lcd control
    lcd.clear()
    lcd.move_to(0, 0)         # first row
    lcd.putstr("Welcome")
    lcd.move_to(0, 1)         # second row
    lcd.putstr(student["name"])
    
    #Servo control
    # Unlock
    servo.duty(77)
    
    #LED control
    led[1] = (0,255,0)
    led.write()
def lock():
    lcd.clear()
    led[1] = (0,0,0)
    # Lock
    servo.duty(26)
    led.write()

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
            cv2.FONT_HERSHEY_SIMPLEX, 0.8,
            color,2
        )
    cv2.imshow(
        "Face Recognition",
        frame
    )
    if cv2.waitKey(1) == ord("q"):
        break

    (stat, tag_type) = rdr.request(rdr.REQIDL)
    if stat == rdr.OK:
        (stat, uid) = rdr.anticoll()
        if stat == rdr.OK:
            uid_str = "".join([str(i) for i in uid])
            print("UID:", uid_str)
            if uid_str in students:
                student = students[uid_str]
                print("Valid Student")
                unlock()
                time.sleep(3)
                lock()
                
            else:
                #Lcd control
                lcd.clear()
                lcd.move_to(0, 0)         # first row
                lcd.putstr("Unknow Card")
                #LED control
                led[1] = (255,0,0)  # Red
                led.write()
                print("Unknown Card")
            time.sleep(1)
            

camera.release()
cv2.destroyAllWindows()