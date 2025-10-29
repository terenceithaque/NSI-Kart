# Script des items
import pygame
import random


class Piece(pygame.sprite.Sprite):
    """Une pièce ramassable par le joueur et les adversaires.
    Elle augmente la vitesse maximale du kart qui la ramasse."""
    def __init__(self, fenetre:pygame.Surface, x=0, y=0) -> None:
        
        self.fenetre = fenetre
        self.image = pygame.image.load("assets/images/piece.png")
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def afficher(self) -> None:
        self.fenetre.blit(self.image, (self.rect.x, self.rect.y))    

