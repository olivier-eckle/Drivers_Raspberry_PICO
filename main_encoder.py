from Encoder_lib import Encoder

rotactor = Encoder(27,26)

rotactor.start_IT()

nb_mouv = 0

while nb_mouv < 100:
    liste_mouv = rotactor.readEncoder()
    if len(liste_mouv) > 0:
        if liste_mouv[0] == rotactor.cw:
            print('Mouvement', nb_mouv,': Sens Horaire', end=' ')
        elif liste_mouv[0] == rotactor.ccw:
            print('Mouvement', nb_mouv,': Sens Anti-Horaire', end=' ')
        print(liste_mouv, end=' -> ')
        liste_mouv.pop(0)
        print(liste_mouv)
        nb_mouv += 1
        
rotactor.stop_IT()
