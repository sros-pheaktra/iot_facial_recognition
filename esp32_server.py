from machine import Pin, SoftI2C, PWM
from machine_i2c_lcd import I2cLcd
import neopixel
import network
import socket
import time

# --------------------------
# Hardware
# --------------------------

servo = PWM(Pin(4), freq=50)
servo.duty(26)

led = neopixel.NeoPixel(Pin(32), 16)


i2c = SoftI2C(
    sda=Pin(25),
    scl=Pin(26),
    freq=400000
)

lcd = I2cLcd(i2c, 0x27, 2, 16)

# --------------------------
# WiFi
# --------------------------

SSID = "Robotic WIFI"
PASSWORD = "rbtWIFI@2025"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

if not wlan.isconnected():

    wlan.connect(SSID, PASSWORD)

    while not wlan.isconnected():
        time.sleep(1)

print(wlan.ifconfig())

# --------------------------
# Web Server
# --------------------------

addr = socket.getaddrinfo(
    "0.0.0.0",
    80
)[0][-1]

server = socket.socket()

server.bind(addr)

server.listen(1)

print("Server Started")

# --------------------------
# Door State
# --------------------------

door_open = False
unlock_time = 0

# --------------------------
# Functions
# --------------------------

def lock():

    global door_open

    servo.duty(26)

    led[1] = (0,0,0)
    led.write()

    lcd.clear()
    lcd.putstr("Scan Face")

    door_open = False


def unlock(name):

    global door_open
    global unlock_time

    lcd.clear()

    lcd.move_to(0,0)
    lcd.putstr("Welcome")

    lcd.move_to(0,1)
    lcd.putstr(name[:16])

    servo.duty(77)

    led[1]=(0,255,0)
    led.write()

    time.sleep(0.2)

    door_open = True
    unlock_time = time.ticks_ms()


def denied():

    lcd.clear()

    lcd.putstr("Access Denied")

    led[1]=(255,0,0)
    led.write()

    time.sleep(1)

    led[1]=(0,0,0)
    led.write()


lock()

# --------------------------
# Main Loop
# --------------------------

while True:

    # Auto lock after 3 seconds

    if door_open:

        if time.ticks_diff(
            time.ticks_ms(),
            unlock_time
        ) > 3000:

            lock()

    server.settimeout(0.1)

    try:

        client, addr = server.accept()

        request = client.recv(1024).decode()

        line = request.split("\r\n")[0]

        if "/access" in line:

            name = "User"

            if "name=" in line:

                start = line.find("name=")+5

                end = line.find(" HTTP")

                name = line[start:end]

                name = name.replace("%20"," ")

            client.send(
                "HTTP/1.1 200 OK\r\n"
                "Content-Type:text/plain\r\n\r\n"
                "OK"
            )

            client.close()

            unlock(name)

        elif "/denied" in line:

            client.send(
                "HTTP/1.1 200 OK\r\n"
                "Content-Type:text/plain\r\n\r\n"
                "OK"
            )

            client.close()

            denied()

        else:

            client.send(
                "HTTP/1.1 404 Not Found\r\n\r\n"
            )

            client.close()

    except OSError:

        pass
