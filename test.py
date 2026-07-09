from machine import Pin, SPI, SoftI2C, PWM
from mfrc522 import MFRC522
from machine_i2c_lcd import I2cLcd
import neopixel
import time

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

while True:
    (stat, tag_type) = rdr.request(rdr.REQIDL)

    if stat == rdr.OK:
        (stat, uid) = rdr.anticoll()

        if stat == rdr.OK:
            uid_str = "".join([str(i) for i in uid])
            print("UID:", uid_str)
            if uid_str in students:

                student = students[uid_str]

                print("Valid Student")
                
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
                
                time.sleep(3)
                lcd.clear()
                led[1] = (0,0,0)
                # Lock
                servo.duty(26)
                led.write()
                
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
            
