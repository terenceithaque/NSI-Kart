# Script de la ligne d'arrivée
import pygame


class LigneArrivee(pygame.sprite.Sprite):
    "Une ligne d'arrivée du circuit."
    def __init__(self, fenetre:pygame.Surface, orient:int=0, longueur:int=500, largeur:int=1280, x:int=0, y:int=0):
        """Initialise la ligne d'arrivée.
        - fenetre : fenêtre dans laquelle la ligne d'arrivée est affuchée
        - orient : degré d'orientation de l'image de la ligne d'arrivée
        - longueur : longueur de la ligne d'arrivée
        - largeur : largeur de la ligne d'arrivée
        - x : position x de la ligne d'arrivée
        - y : position y de la ligne d'arrivée"""

        # Initialisation des attributs
        super().__init__()
        
        self.fenetre = fenetre
        self.orient = orient
        self.image = pygame.image.load("assets/images/ligne_arrivee.png")
        self.image = pygame.transform.rotate(self.image, self.orient)
        self.image = pygame.transform.scale(self.image, (longueur, largeur))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.longueur = longueur
        self.largeur = largeur


    def est_passee(self, objet) -> bool:
        """Renvoie True si la ligne est passée par un objet actuellement, False sinon."""
        return pygame.Rect.colliderect(self, objet.rect)    


    def afficher(self) -> None:
        """Affiche la ligne d'arrivée à l'écran."""
        self.fenetre.blit(self.image, (self.rect.x, self.rect.y))    