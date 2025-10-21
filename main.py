# Programme principal du jeu
import pygame
pygame.init()
from kart import *
from circuits import *



# Créer la fenêtre de jeu
fenetre = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("NSI-Kart")

execution = True
kart_joueur = Kart(fenetre, "assets/images/kart1.png", 120, 600, 2.0, 0.25, "haut")
acceleration = pygame.USEREVENT + 1
pygame.time.set_timer(acceleration, 500)


circuit = Circuit(fenetre, 1)
print(circuit.donnees)
print(circuit.tourne_a_droite((0, 3)))


portion_depart = PortionCircuit(fenetre, "assets/images/route.png")

# Boucle principale
while execution:

    fenetre.fill((0, 0, 0))

    touches = pygame.key.get_pressed()

    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            execution = False

        if evenement.type == acceleration: 
            kart_joueur.accelerer()   

    if touches[pygame.K_RIGHT]:
        kart_joueur.changer_direction("droite")
        kart_joueur.mettre_a_jour_rotation()

    if touches[pygame.K_LEFT]:
        kart_joueur.changer_direction("gauche")
        kart_joueur.mettre_a_jour_rotation()

    if touches[pygame.K_UP]:
        kart_joueur.changer_direction("haut")
        kart_joueur.mettre_a_jour_rotation()

    if touches[pygame.K_DOWN]:
        kart_joueur.changer_direction("bas")
        kart_joueur.mettre_a_jour_rotation()


    kart_joueur.mettre_a_jour_direction()
    kart_joueur.deplacer()                
    

    portion_depart.afficher()
    
    kart_joueur.afficher() 

           

    # Mettre à jour l'affichage
    pygame.display.flip()        