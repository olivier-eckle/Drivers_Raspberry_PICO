from machine import Pin
import time

# Exemple de code :

# from Encoder_lib import Encoder
# 
# rotactor = Encoder(27,26)
# 
# rotactor.start_IT()
# 
# nb_mouv = 0
# 
# while nb_mouv < 100:
#     liste_mouv = rotactor.readEncoder()
#     if len(liste_mouv) > 0:
#         if liste_mouv[0] == rotactor.cw:
#             print('Mouvement', nb_mouv,': Sens Horaire', end=' ')
#         elif liste_mouv[0] == rotactor.ccw:
#             print('Mouvement', nb_mouv,': Sens Anti-Horaire', end=' ')
#         print(liste_mouv, end=' -> ')
#         liste_mouv.pop(0)
#         print(liste_mouv)
#         nb_mouv += 1
#         
# rotactor.stop_IT()

class Encoder:        
    def __init__(self, pin_clk, pin_data):
        ''' Instanciation de l'encodeur GROVE 111020001.
            Lors de l'appel du constructeur (déclaration) il est nécessaire de fournir
            en argument le numéro des 2 entrées sur lesquelles est connecté l'encodeur...

            A utiliser :
            - directement sur deux GPIO de la PICO mais avec une alimentation 3v3.
            - avec le shield GROVE PICO (103100142) sur les connecteurs A1 ou A2.
            
            Methodes disponibles dans cette CLASS :
            -  .start_IT() 
            -  .stop_IT()
            -  .readEncoder()  --> Retourne une liste des derniers différents mouvements (100 maxi) 
        '''
        self.__pin_clk = Pin(pin_clk, Pin.IN, None)
        self.__pin_data = Pin(pin_data, Pin.IN, None)
        self.__debounce = 0
        self.list_IT = []
        self.cw = 1
        self.ccw = -1

    def start_IT(self):
        ''' Active l'IT associé au GPIO de l'encodeur...'''
        self.__pin_clk.irq(trigger = Pin.IRQ_FALLING, handler = self.__encoderISR)
        
    def stop_IT(self):
        ''' Désactive l'IT associé au GPIO de l'encodeur...'''
        self.__pin_clk.irq(handler = None)


    def __encoderISR(self, pin_number):
        ''' Permet de récupérer la liste des 100 derniers mouvements...'''
        if pin_number == self.__pin_clk:
            if len(self.list_IT) == 100:
                self.list_IT.pop(0)
            else:
                if time.ticks_ms() - self.__debounce > 50:
                    self.__debounce = time.ticks_ms()
                    time.sleep_us(100)
                    if self.__pin_data.value():
                        self.list_IT.append(self.ccw)
                    else:
                        self.list_IT.append(self.cw)
                
    def readEncoder(self):
        return self.list_IT

