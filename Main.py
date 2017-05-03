#Author : Tanguy PELADO
import time
import simpleaudio 
import RPi.GPIO as GPIO
import MFRC522
from sons import * #ici on importe les sons 

def lecture():
    MIFAREReader = MFRC522.MFRC522()
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    if status == MIFAREReader.MI_OK:
        print("Card detected")
    (status,uid) = MIFAREReader.MFRC522_Anticoll()
    if status == MIFAREReader.MI_OK:
        return uid

class carte:
    def __init__(self,nom,uid,elimine):
        self.nom = nom
        self.uid = uid
        self.em = elimine # false si en jeu, True si hors jeu
        
### initialisation des cartes

#12 cartes pour chaque joueurs dans 2 liste respectives : 0xA0 : j1[0], 0xA1 : j1_[0]
def initialisation():
    noms = ["Michel","jean","pierre","paul","salut"] #noms des cartes, en supposant que les 2 joueurs on les memes noms de cartes
    uids = [[136,4,11,75,204],2,3,4,5,6,7] #liste des uids
    j1,j2 = [],[]
    for i in range(len(noms)):
        j1.append(carte(noms[i],uids[i],False))
        j2.append(carte(noms[i],uids[i],False))
    print(j1[0].uid)
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
        for i in range(nbr_cartes):
            if select == j1[i].uid:
                select_j1 = j1[i]
                reussi = True
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
        for i in range(nbr_cartes):
            if select == j2[i].uid:
                select_j2 = j2[i]
                reussi = True
    reussite.play()
    
    return select_j1,select_j2
    
    
def condi_victoire_j1(j1):#prend la liste des cartes en argu <a>
    j = 0
    for i in j1:
        if i.em = False:
            j =+1
    if j == 1: #si il ne reste qu'une carte dans le jeu du j1 -> il gagne car il a decouvert la carte du j2
        gagne = True
        return gagne
        
def condi_victoire_j2(j2):#idem </a>
    j = 0
    for i in j2:
        if i.em = False:
            j =+1
    if j == 1: #si il ne reste qu'une carte dans le jeu du j2 -> il gagne car il a decouvert la carte du j1
        gagne = True
        return gagne
    
    
###Main Game
###MG init
nbr_cartes,j1,j2 = initialisation()
select_j1, select_j2 = selection()
gagne = False
tour_j1 = True
delete = False
j = 0
###MG Main
while(not gagne):
    #tour j1 #faudra juste écrire le tour du j1 et c/c pour le j2 en modifiant
    while(tour_j1): ##comment gere t on le passage de tour
        if(delete): ## delete -> bouton pour supr les cartes
            dele = lecture()
            for i in range(nbr_cartes):
                if select == j1[i].uid:
                    if(j1[i].em): # remise de la carte
                        j1[i].em = False
                    else:
                        j1[i].em = True
        else: #mode lecture
            lect = lecture()
            for i in range(nbr_cartes):
                if lect == j1[i].uid:
                    print(i)
                    carte[i].play() #carte_i correspond au nom de la carte dans sons.py
            time.sleep(1)
    #condition de victoire
    if(not condi_victoire_j1(j1):
        while(tour_j2):
            ###c/c le tour du j1 quand il marche
    else:
        print("j1 gagne")
        #jouer le son ici
            
            
        
    









