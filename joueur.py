# Script du joueur
import pygame
from kart import *


class Joueur:
    """Une classe liant tous les éléments du joueur (position, kart, etc)."""
    def __init__(self, fenetre:pygame.Surface, kart:Kart, position_depart:int=12):
        """Initialise le joueur.
        - fenetre : fenêtre où les différentes informations concernant le joueur sont affichées
        - kart: le kart du joueur
        - position_depart : position de départ du joueur"""

        # Initialisation des attributs
        self.fenetre = fenetre
        self.kart = kart # Kart du joueur
        self.position_depart = position_depart # Position de départ du joueur

        self.position = self.position_depart # Position actuelle du joueur dans le classement

        self.tours = 1 # Numéro du tour actuel du joueur, au départ 1
