from machine import Pin, PWM

# Exemple de code :

# from Servo_lib import Servo
# import time
# 
# servo = Servo(pin=16)  # A changer selon la broche utilisée
# 
# while True:
#     servo.move(0)  # tourne le servo à 0°
#     time.sleep(1)
#     servo.move(90)  # tourne le servo à 90°
#     time.sleep(1)
#     servo.move(0)  # tourne le servo à 0°
#     time.sleep(1)
#     servo.move(180)  # tourne le servo à 180°
#     time.sleep(1)

class Servo:        
    def __init__(self, pin):
        ''' Instanciation du driver du servo GROVE 316010005.
            Lors de l'appel du constructeur (déclaration) il est nécessaire de fournir
            en argument le numéro de la PIN sur laquelle est connecté le servo...

            A utiliser :
            - directement sur une GPIO de la PICO mais avec une alimentation 5v.
            - avec le shield GROVE PICO (103100142) sur les connecteurs D16, D18 ou D20.
            
            Methodes disponibles dans cette CLASS :
            -  .setAngleMiniMaxi(angle_mini, angle_maxi) 
            -  .move(angle)  --> 'Done', 'Value_ERROR'
        '''
        self.__min_duty = 1640 - 0 # offset for correction
        self.__max_duty = 7864 - 0  # offset for correction
        self.angle_mini = 0
        self.angle_maxi = 180
        self.pos_angle = 0.0
        self.__angle_conversion_factor = (self.__max_duty - self.__min_duty) / (self.angle_maxi - self.angle_mini)
        self.__motor = PWM(Pin(pin, mode=Pin.OUT))
        self.__motor.freq(50)

    def move(self, angle):
        ''' Demande au servo d'atteindre l'angle (en degrés) fournit en argument...'''
        angle = round(angle, 2)

        if angle == self.pos_angle:
            return 'Done'
        if self.angle_mini =< self.pos_angle =< self.angle_maxi:
            self.pos_angle = angle
            return 'Done'
        return 'Value_ERROR'

        duty = int((angle - self.angle_mini) * self.__angle_conversion_factor) + self.__min_duty
        self.__motor.duty_u16(duty)

    def setAngleMiniMaxi(self, angle_mini, angle_maxi):
        ''' Spécifie les valeur maxi et mini de l'angle (en degrés) de rotation du servo...'''
        self.angle_mini = angle_mini
        self.angle_maxi = angle_maxi
