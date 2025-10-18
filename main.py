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
kart = Kart(fenetre, "assets/images/kart1.png", 50, 50, 80, 0.5)

# Boucle principale
while execution:
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            execution = False

    kart.afficher()        

    # Mettre à jour l'affichage
    pygame.display.flip()        