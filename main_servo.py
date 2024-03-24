from Servo_lib import Servo
import time

servo = Servo(pin=16)  # A changer selon la broche utilisée

while True:
    servo.move(0)  # tourne le servo à 0°
    time.sleep(1)
    servo.move(90)  # tourne le servo à 90°
    time.sleep(1)
    servo.move(0)  # tourne le servo à 0°
    time.sleep(1)
    servo.move(180)  # tourne le servo à 180°
    time.sleep(1)
   

