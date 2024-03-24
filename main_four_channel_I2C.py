import time
from Four_Channel_Relay_I2C_lib import Four_Channel_Relay_I2C

pont_H = Four_Channel_Relay_I2C(0)
pont_H.initI2C()
print(pont_H.scanI2C())

pont_H.setAddrI2C(0x11)

pont_H.turnOnAllSwitch()
time.sleep(1)
pont_H.turnOffAllSwitch()
time.sleep(1)
pont_H.turnOnAllSwitch()
time.sleep(1)
pont_H.turnOffAllSwitch()
time.sleep(1)
pont_H.controlSwitch([True, False, True, False])
print(pont_H.getState())
time.sleep(1)
pont_H.controlSwitch([False, True, False, True])
print(pont_H.getState())
time.sleep(1)
pont_H.controlSwitch([True, False, False, False])
print(pont_H.getState())
time.sleep(1)
pont_H.turnOffAllSwitch()
print(pont_H.getState())


