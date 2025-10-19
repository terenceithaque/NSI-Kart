# Programme principal du jeu
import pygame
pygame.init()
from kart import *
from circuits import *

print(trace_circuit(1))

# Créer la fenêtre de jeu
fenetre = pygame.display.set_mode((800, 600))
pygame.display.set_caption("NSI-Kart")

execution = True
kart_joueur = Kart(fenetre, "assets/images/kart1.png", 120, 600, 10.0, 0.05, "haut")
acceleration = pygame.USEREVENT + 1
pygame.time.set_timer(acceleration, 500)

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

    if touches[pygame.K_LEFT]:
        kart_joueur.changer_direction("gauche")

    if touches[pygame.K_UP]:
        kart_joueur.changer_direction("haut")

    if touches[pygame.K_DOWN]:
        kart_joueur.changer_direction("bas")


    kart_joueur.mettre_a_jour_rotation()
    kart_joueur.deplacer()                
    
    
    kart_joueur.afficher()        

    # Mettre à jour l'affichage
    pygame.display.flip()        