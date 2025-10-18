# Programme principal du jeu
import pygame
pygame.init()


# Créer la fenêtre de jeu
fenetre = pygame.display.set_mode((800, 600))
pygame.display.set_caption("NSI-Kart")

execution = True

# Boucle principale
while execution:
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            execution = False

    # Mettre à jour l'affichage
    pygame.display.flip()        