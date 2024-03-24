from machine import I2C, Pin

# Exemple de code :

# import time
# from Four_Channel_Relay_I2C_lib import Four_Channel_Relay_I2C
# 
# pont_H = Four_Channel_Relay_I2C(0)
# pont_H.initI2C()
# print(pont_H.scanI2C())
# 
# pont_H.setAddrI2C(0x11)
# 
# pont_H.turnOnAllSwitch()
# time.sleep(1)
# pont_H.turnOffAllSwitch()
# time.sleep(1)
# pont_H.turnOnAllSwitch()
# time.sleep(1)
# pont_H.turnOffAllSwitch()
# time.sleep(1)
# pont_H.controlSwitch([True, False, True, False])
# print(pont_H.getState())
# time.sleep(1)
# pont_H.controlSwitch([False, True, False, True])
# print(pont_H.getState())
# time.sleep(1)
# pont_H.controlSwitch([True, False, False, False])
# print(pont_H.getState())
# time.sleep(1)
# pont_H.turnOffAllSwitch()
# print(pont_H.getState())


class Four_Channel_Relay_I2C:
    def __init__(self,val_id_hardware_I2C):
        ''' Instanciation du driver du pont en H 4 relais GROVE 103020133.
            Lors de l'appel du constructeur (déclaration) il est nécessaire de fournir
            le numéro de l'I2C (hardware) 0 ou 1 sur laquelle est connecté la carte GROVE...

            ATTENTION : Pour être compatible avec les niveaux logiques de la PICO (3v3),
            il faut dessouder les 2 résistances de PULL-UP à 5v qui se trouve sur la carte
            GROVE. Ces 2 résistances (R49 et R50) se trouvent juste à gauche du connecteur GROVE.
            
            A utiliser :
            - directement sur le bus I2C hardware (0 ou 1) de la PICO mais avec une alimentation 5v.
            - avec le shield GROVE PICO (103100142) sur les connecteurs I2C0 ou I2C1.
            
            Methodes disponibles dans cette CLASS :
            -  .initI2C()
            -  .scanI2C()  --> liste des adresses des périphériques qui "répondent"...
            -  .setAddrI2C(addr_I2C)
            -  .changeAddrI2C(new_addr_I2C)  --> Résultat du changement d'adresse I2C...
            -  .getFirmwareVersion() --> numéro du Firmware
            -  .turnOnAllSwitch()
            -  .turnOFFAllSwitch()
            -  .controlSwitch([bool, bool, bool, bool])
            -  .getState()  --> liste de 4 booléens qui représentent (dans l'ordre) les état de SW1, SW2, SW3 et SW4
        '''
        self.__id_hardware_I2C = val_id_hardware_I2C
        self.__addr_I2C = 17
        if val_id_hardware_I2C == 0:
            self.__pin_scl = 9
            self.__pin_sda = 8
        elif val_id_hardware_I2C == 1:
            self.__pin_scl = 7
            self.__pin_sda = 6
        else:
            return none
        self.__freq_I2C = 400000
        self.__cmd_Channel_Ctrl = 16
        self.__cmd_read_I2C_addr = 18
        self.__cmd_save_I2C_addr = 17
        self.__cmd_read_firmware_ver = 19
        self.state = [False, False, False, False]
        self.__i2c = None
        
        
    def initI2C(self):
        ''' Initialisatiopn de la liaison I2C...'''
        self.__i2c = I2C(self.__id_hardware_I2C, scl=Pin(self.__pin_scl), sda=Pin(self.__pin_sda), freq=self.__freq_I2C)
        
        
    def scanI2C(self):
        ''' Scan de toutres les adresses I2C entre 0x08 et 0x77
            et retourne dans une liste les adresses qui "répondent"...'''
        l_addr = self.__i2c.scan()
        if len(l_addr) == 0:
            return '\nAucun périphérique I2C trouvé... Vérifiez la connection du périphérique à la PICO...'
        elif len(l_addr) == 1:
            return '\nUn seul périphérique I2C trouvé. Son adresse est :  ' + hex(l_addr[0])
        else:
            message = '\nPlusieurs périquériques I2C trouvés. A vous de déterminer lequel...\nLeurs adresses sont :  '
            for i in range(len(l_addr)):
                message = message + hex(l_addr[i])
                if i < len(l_addr)-1:
                    message = message + '  /  '
            return message
            
            
    def setAddrI2C(self, addr):
        ''' Specifie l'adresse I2C de la carte GROVE 103020133.'''
        self.__addr_I2C = addr
    
    
    def changeAddrI2C(self, new_addr):
        ''' Change l'adresse I2C de la carte GROVE 103020133.
            La valeur de la nouvelle adresse doit être : 0x08 =< @I2C =< 0x77 ...'''
        if 7 < new_addr < 120:
            self.__i2c.writeto(self.__addr_I2C, chr(self.__cmd_save_I2C_addr) + chr(new_addr))
            self.__addr_I2C = new_addr
            return '\nLa nouvelle adresse I2C de la carte GROVE 103020133 est :  ' + hex(new_addr) + '\nUn reboot de la carte GROVE est nécessaire !!!'
        else:
            return "\nL'adresse I2C de la carte GROVE 103020133 doit être comprise entre 0x08 et 0x77...\nL'adresse I2C valide est toujours :  " + hex(self.addr_I2C)
            
    
    def getFirmwareVersion(self):
        ''' Lecture du Firmware de le la carte GROVE 103020133...'''
        self.__i2c.writeto(self.__addr_I2C, chr(self.__cmd_read_firmware_ver))
        val = self.i2c.readfrom(self.addr_I2C, 1)
        return val


    def turnOnAllSwitch(self):
        ''' Force à ON tous les SWITCHs de la carte GROVE 103020133...'''
        self.state = [True, True, True, True]
        self.__i2c.writeto(self.__addr_I2C, chr(self.__cmd_Channel_Ctrl)+chr(15))
    
    
    def turnOffAllSwitch(self):
        ''' Force à OFF tous les SWITCHs de la carte GROVE 103020133...'''
        self.state = [False, False, False, False]
        self.__i2c.writeto(self.__addr_I2C, chr(self.__cmd_Channel_Ctrl)+chr(0))


    def controlSwitch(self, switch_state):
        ''' Force à ON / OFF tous les SWITCHs de la carte GROVE 103020133
            en fonction de la liste donnée en argument.
            Ex : [True, True, False, True] => SW1:ON, SW2:ON, SW3:OFF et SW4:ON'''
        self.state = switch_state
        self.__i2c.writeto(self.__addr_I2C, chr(self.__cmd_Channel_Ctrl)+chr(self.__calculChrState()))
        

    def getState(self):
        ''' Retourne l'état des SWITCHs de la carte GROVE 103020133 dans une liste de 4 booléens...
            Ex : SW1:ON, SW2:ON, SW3:OFF et SW4:ON => [True, True, False, True]'''
        return self.state
    
    
    def __calculChrState(self):
        val_state = 0
        if self.state[3]:
            val_state += 8
        if self.state[2]:
            val_state += 4
        if self.state[1]:
            val_state += 2
        if self.state[0]:
            val_state += 1
        return val_state
