#Author : Tanguy PELADO
import time
import simpleaudio 
import RPi.GPIO as GPIO
import MFRC522
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(40, GPIO.OUT)
GPIO.output(40,GPIO.LOW)



etat = False # mode lecture par défaut
from sons import * #ici on importe les sons 

def lecture():
    MIFAREReader = MFRC522.MFRC522()
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    if status == MIFAREReader.MI_OK:
        print("Card detected")
    (status,uid) = MIFAREReader.MFRC522_Anticoll()
    if status == MIFAREReader.MI_OK:
        return uid[:4]

class carte:
    def __init__(self,nom,uid,elimine):
        self.nom = nom
        self.uid = uid
        self.em = elimine # false si en jeu, True si hors jeu
        
### initialisation des cartes

#12 cartes pour chaque joueurs dans 2 liste respectives : 0xA0 : j1[0], 0xA1 : j1_[0]
def initialisation():
    noms = ["Benoit","Jean-Luc","Manuel","Francois","Donald","Jacques","Marine","Nathalie","Segolene","Martine","Bernadette","Elisabeth"] #noms des cartes, en supposant que les 2 joueurs on les memes noms de cartes
    uids_j1 = [[136,4,123,218],[136,4,123,211],[136,4,122,208],[136,4,122,98],[136,4,122,104
],[136,4,122,110],[136,4,122,117],[136,4,122,124],[136,4,125,254],[136,4,125,1],[136,4,126,6],[136,4,124,4]] #liste des uids
    uids_j2 = [[136,4,123,254],[136,4,123,215],[136,4,122,204],[136,4,122,101],[136,4,122,107],[136,4,122,113],[136,4,122,120],[136,4,122,127],[136,4,124,251],[136,4,126,3],[136,4,124,8],[136,4,124,0]] #liste des uids
    j1,j2 = [],[]
    for i in range(len(noms)):
        j1.append(carte(noms[i],uids_j1[i],False))
        j2.append(carte(noms[i],uids_j2[i],False))
    return len(noms),j1,j2

### Selection de la carte a faire deviner
    
#voir quand j'aurais la lib de lecture qui marche comme il faut
def selection():
    reussi = False
    test = choix_j1.play()
    time.sleep(1)
    simpleaudio.stop_all()
    while(not reussi):
        select = lecture()
        if(select != None):
            print(select)
            for i in range(nbr_cartes):
                if select == j1[i].uid:
                    select_j1 = j1[i]
                    reussi = True
                    print(j1[i].nom)
    if(reussi):
        test = reussite.play()
    time.sleep(1)
    simpleaudio.stop_all()
    reussi = False
    print("j1 ok")
    time.sleep(2)
    choix_j2.play()
    while(not reussi):
        select = lecture()        
        if(select != None):
            print(select)
            for i in range(nbr_cartes):
                if select == j2[i].uid:
                    select_j2 = j2[i]
                    reussi = True
                    print(j2[i].nom)
    reussite.play()
    
    return select_j1,select_j2

gagne = False
    
def condi_victoire_j1(j1):#prend la liste des cartes en argu <a>
    global gagne
    j = 0
    for i in j1:
        if i.em == False:
            j +=1
    if j == 1: #si il ne reste qu'une carte dans le jeu du j1 -> il gagne car il a decouvert la carte du j2
        gagne = True
    return gagne
        
def condi_victoire_j2(j2):#idem </a>
    global gagne
    j = 0
    for i in j2:
        if i.em == False:
            j +=1
    if j == 1: #si il ne reste qu'une carte dans le jeu du j2 -> il gagne car il a decouvert la carte du j1
        gagne = True
    return gagne
        

        
def relais(channel):
    global etat
    if(etat):
        print("mode lecture")
        GPIO.output(40,GPIO.LOW)
    else:
        GPIO.output(40,GPIO.HIGH)
        print("mode delete")
    etat = not etat
    
tour_j1 = True
tour_j2 = False
    
def tour(channel):
    global tour_j1
    global tour_j2
    tour_j1 = not tour_j1
    tour_j2 = not tour_j2
        
    
GPIO.add_event_detect(12, GPIO.RISING, callback=tour, bouncetime=300)   
GPIO.add_event_detect(11, GPIO.FALLING, callback=relais, bouncetime=300) 
    
###Main Game
###MG init
nbr_cartes,j1,j2 = initialisation()
select_j1, select_j2 = selection()


j = 0
###MG Main
while(not gagne):
    print("tour j1")
    #tour j1 #faudra juste ecrire le tour du j1 et c/c pour le j2 en modifiant
    while(tour_j1 and not condi_victoire_j2(j2)): ##bouton
        if(etat): ## delete -> bouton pour supr les cartes
            dele = lecture()
            if(dele != None):
                for i in range(nbr_cartes):
                    if dele == j1[i].uid:
                        if(j1[i].em): # remise de la carte
                            j1[i].em = False
                            print("remis")
                            print(j1[i].nom)
                        else:
                            j1[i].em = True                               
                            print("delete")
                            print(j1[i].nom)
                        time.sleep(2)
        else: #mode lecture
            lect = lecture()
            if(lect != None):
                for i in range(nbr_cartes):
                    if lect == j1[i].uid:
                        print("lecture")
                        print(j1[i].nom)
                        time.sleep(1)
                     #   carte[i].play() #carte_i correspond au nom de la carte dans sons.py
            time.sleep(1)
    #condition de victoire
    print("tour j2")
    if(etat):
        relais(12)
    if(not condi_victoire_j1(j1)):
        while(tour_j2):
            if(etat): ## delete -> bouton pour supr les cartes
                dele = lecture()
                if(dele != None):
                    for i in range(nbr_cartes):
                        if dele == j2[i].uid:
                            if(j2[i].em): # remise de la carte
                                j2[i].em = False
                                print("remis")
                                print(j2[i].nom)
                            else:
                                j2[i].em = True
                                print("delete")
                                print(j2[i].nom)
                            time.sleep(2)
            else: #mode lecture
                lect = lecture()
                if(lect != None):
                    for i in range(nbr_cartes):
                        if lect == j2[i].uid:
                            print("lecture")
                            print(j2[i].nom)
                            time.sleep(1)
                           # carte[i].play() #carte_i correspond au nom de la carte dans sons.py
                time.sleep(1)
        if(condi_victoire_j2(j2)):
            print("j2 gagne")
        
    else:
        print("j1 gagne")
        #jouer le son ici
            
if KeyboardInterrupt:
    GPIO.cleanup()
GPIO.cleanup() 
    









