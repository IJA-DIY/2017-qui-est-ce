#Author : Tanguy PELADO
#Help : Daniel Sanchez, Alois Lacassagne


##ToDo List
#ajouter une fonction de reset
#ajouter les sons
#fixer les bugs
#verifier les noms
##fin Todo List


##Import 

import time #pratique pour les delais entre les lectures
#import simpleaudio #pour lire les fichier *.wav
import RPi.GPIO as GPIO #permet l'interaction avec les Pins sur la carte
import MFRC522 #biblio pour les lecteurs NFCs
#from sons import * #ici on importe les sons 

##Declaration des variables
etat = False # defini le mode lecture ou delete (mode lecture par defaut)
gagne = False #defini si le jeu est gagne ou pas (faux par defaut)
tour_j1 = True # fonctionne en paire avec tour_j2, est utilise pour changer de personne
tour_j2 = False
#j = 0 # je sais pas a quoi celui ci sert, si ca plante c'est que c'etait utile

##GPIO Config
GPIO.setmode(GPIO.BOARD) #mode BCM non dispo a cause de MFRC
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #declaration du bouton de tour    
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)#declaration du bouton changement de mode (lecture // delete)
#inserer ici le bouton reset
GPIO.setup(40, GPIO.OUT)
GPIO.output(40,GPIO.LOW)


def lecture(): #lit une carte NFC et renvoie son UID si disponible, sinon renvoie None
    print("lecture")
    MIFAREReader = MFRC522.MFRC522()
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    if status == MIFAREReader.MI_OK:
        print("carte detecte")
    (status,uid) = MIFAREReader.MFRC522_Anticoll()
    if status == MIFAREReader.MI_OK:
        return uid[:4]

class carte: # la classe carte, la base du jeu
    def __init__(self,nom,uid,elimine):
        self.nom = nom # nom de la carte
        self.uid = uid # uid de la carte
        self.em = elimine # false si en jeu, True si hors jeu
        
## initialisation des cartes

#12 cartes pour chaque joueurs dans 2 liste respectives  j1 et j2
def initialisation():#initialise la liste de carte et revoie le nombre de carte par joeur ainsi que les listes de cartes
    noms = ["Delphine","Anna","Joseline","Alice","Vero","Cathy","Olivier","jacques","Mathieu","Daniel","Enrique","Henri"] #noms des cartes, en supposant que les 2 joueurs on les memes noms de cartes
    uids_j1 = [[136,4,123,218],[136,4,123,211],[136,4,122,208],[136,4,122,98],[136,4,122,104
],[136,4,122,110],[136,4,122,117],[136,4,122,124],[136,4,125,254],[136,4,125,1],[136,4,126,6],[136,4,124,4]] #liste des uids pour les cartes du j1
    uids_j2 = [[136,4,123,254],[136,4,123,215],[136,4,122,204],[136,4,122,101],[136,4,122,107],[136,4,122,113],[136,4,122,120],[136,4,122,127],[136,4,124,251],[136,4,126,3],[136,4,124,8],[136,4,124,0]] #liste des uids pour les cartes du j2
    j1,j2 = [],[]
    for i in range(len(noms)):
        j1.append(carte(noms[i],uids_j1[i],False))
        j2.append(carte(noms[i],uids_j2[i],False))
    return len(noms),j1,j2

## Selection de la carte a faire deviner
    
def selection():#j1 puis j2, ne valide que si les 2 cartes existent
    reussi = False
    while(not reussi):#tant que la selection pour le j1 n'est pas valide
        select = lecture()
        if(select != None):# si la carte scannee possede un uid, on regarde si elle est dans notre jeu de carte
            print(select) #pour le debug
            for i in range(nbr_cartes):
                if select == j1[i].uid:# si la carte est bien dans le jeu du j1 alors on la selectionne
                    select_j1 = j1[i]
                    reussi = True
                    print(j1[i].nom)#pour le debug
    reussi = False
    print("j1 ok")#pour le debug
    while(not reussi):#tant que la selection pour le j2 n'est pas valide
        select = lecture()        
        if(select != None):
            print(select)#pour le debug
            for i in range(nbr_cartes):
                if select == j2[i].uid:
                    select_j2 = j2[i]
                    reussi = True
                    print(j2[i].nom)#pour le debug
    return select_j1,select_j2
    
def condi_victoire_j1(j1):#prend la liste des cartes en argument et revoie True si il ne reste que la carte du j2 dans le jeu du j1
    global gagne
    j = 0
    for i in j1:
        if i.em == False:
            j +=1
    if j == 1: #si il ne reste qu'une carte dans le jeu du j1 -> il gagne car il a decouvert la carte du j2
        gagne = True # fin du jeu
    return gagne
        
def condi_victoire_j2(j2):#idem que pour le j1
    global gagne
    j = 0
    for i in j2:
        if i.em == False:
            j +=1
    if j == 1: #si il ne reste qu'une carte dans le jeu du j2 -> il gagne car il a decouvert la carte du j1
        gagne = True # fin du jeu
    return gagne
        

        
def relais(channel): #controle le relais pour changer entre le mode lecture et mode delete
    global etat 
    if(etat):
        print("mode lecture")#pour le debug
        GPIO.output(40,GPIO.LOW) #eteint le relais
    else:
        GPIO.output(40,GPIO.HIGH) # allume le relais
        print("mode delete")#pour le debug
    etat = not etat
    
def tour(channel): # est utilise pour changer de tour
    global tour_j1
    global tour_j2
    tour_j1 = not tour_j1
    tour_j2 = not tour_j2
        
##GPIO interupt
#ajoute les interuptions de changement de mode et de fin de tour
GPIO.add_event_detect(12, GPIO.RISING, callback=tour, bouncetime=300)  
GPIO.add_event_detect(11, GPIO.RISING, callback=relais, bouncetime=300) 
#ajouter le bouton de reset ici aussi
    
##Main Game
##
nbr_cartes,j1,j2 = initialisation() # initialisation du nombre de carte, et du jeu de chaque joeur
select_j1, select_j2 = selection() # selection des cartes a faire deviner

##MG Main
#sachant que le tour du j2 est exactement le meme que celui du j1, le tour du j2
while(not gagne): # tant que le jeu n'est pas fini
    if(etat):#si jamais on etait en mode delete, on repasse en mode lecture
        relais(12)
    print("tour j1")#pour le debug
    while(tour_j1 and not condi_victoire_j2(j2)): #tant que je tour n'est pas fini. on regarde aussi si le j2 n'a pas gagne
        if(etat): ## mode delete -> bouton pour supr les cartes
            dele = lecture()
            if(dele != None):# si la carte est valide, alors on regarde si elle est dans notre jeu, cela evite de faire des boucles inutiles si la carte n'est pas valide
                for i in range(nbr_cartes):
                    if dele == j1[i].uid:#si notre carte est bien dans le jeu du j1
                        if(j1[i].em): # elle est deja elimine, on la remet en jeu
                            j1[i].em = False
                            print("remis")#pour le debug
                            print(j1[i].nom)#pour le debug
                        else:#elle n'est pas elimine, donc on l'elimine
                            j1[i].em = True                               
                            print("delete")#pour le debug
                            print(j1[i].nom)#pour le debug
                        time.sleep(2)# on pause 2 secondes afin de ne pas supprimer et remettre la meme carte 1545 fois en une lecture
            else:
                time.sleep(0.5)
        else: #mode lecture : on lit la carte et on joue son nom
            lect = lecture()
            if(lect != None):
                for i in range(nbr_cartes):
                    if lect == j1[i].uid:
                        print("lecture")
                        print(j1[i].nom)
                        time.sleep(1)#pour eviter de lire 556684 fois la meme carte
            else:
                time.sleep(0.5)
    #condition de victoire
    print("tour j2")#pour le debug
    if(etat):#si jamais on etait en mode delete, on repasse en mode lecture
        relais(12)
    if(not condi_victoire_j1(j1)):#on verifie que le j1 n'ait pas gagne
        while(tour_j2):#voir j1 pour l'explication du code
            if(etat): ## delete -> bouton pour supr les cartes
                dele = lecture()
                if(dele != None):
                    for i in range(nbr_cartes):
                        if dele == j2[i].uid:
                            if(j2[i].em): # remise de la carte
                                j2[i].em = False
                                print("remis")#pour le debug
                                print(j2[i].nom)#pour le debug
                            else:
                                j2[i].em = True
                                print("delete")#pour le debug
                                print(j2[i].nom)#pour le debug
                            time.sleep(2)
                else:
                    time.sleep(0.5)
            else: #mode lecture
                lect = lecture()
                if(lect != None):
                    for i in range(nbr_cartes):
                        if lect == j2[i].uid:
                            print("lecture")#pour le debug
                            print(j2[i].nom)#pour le debug
                            time.sleep(1)
                else:
                    time.sleep(0.5)
        if(condi_victoire_j2(j2)):
            print("j2 gagne")#pour le debug
        
    else:
        print("j1 gagne")#pour le debug
        #jouer le son ici
            
if KeyboardInterrupt: # ca cest pour bien finir le programme et ne plus mobiliser les ports GPIO
    GPIO.cleanup()
GPIO.cleanup() 
    
    









