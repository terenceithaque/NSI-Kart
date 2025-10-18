# Script des karts
import pygame


class Kart(pygame.sprite.Sprite):
    "Classe représentant un kart en course."

    def __init__(self, fenetre:pygame.Surface, image:str="assets/images/kart1.png", x:int=0, y:int=0, vitesse_max=50, acceleration=0.5) -> None:
        """Initialise le kart
        - fenetre : fenêtre de jeu dans laquelle le kart est affiché
        - image : chemin de l'image représentannt le kart
        - x : position x de départ du kart
        - y : position y de départ du kart
        - vitesse_max : vitesse maximale du kart
        - acceleration : taux d'accélération du kart par secondes, par défaut 0.5"""

        # Initialisation des attributs
        self.fenetre = fenetre
        self.chemin_image = image
        self.image = pygame.image.load(self.chemin_image)
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


    def afficher(self) -> None:
        """Affiche le kart à l'écran."""
        self.fenetre.blit(self.image, (self.rect.x, self.rect.y))    

