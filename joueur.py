# Script du joueur
import pygame
from kart import *
from circuits import *


class Joueur:
    """Une classe liant tous les éléments du joueur (position, kart, etc)."""
    def __init__(self, fenetre:pygame.Surface, kart:Kart, portion_depart:PortionCircuit, position_depart:int=12):
        """Initialise le joueur.
        - fenetre : fenêtre où les différentes informations concernant le joueur sont affichées
        - kart: le kart du joueur
        - portion_depart : portion de circuit dans laquelle le kart du joueur est au départ
        - position_depart : position de départ du joueur"""

        # Initialisation des attributs
        self.fenetre = fenetre
        self.kart = kart # Kart du joueur
        self.position_depart = position_depart # Position de départ du joueur

        self.position = self.position_depart # Position actuelle du joueur dans le classement
        self.portion_circuit = portion_depart

        self.tour = 1 # Numéro du tour actuel du joueur, au départ 1

    def incrementer_position(self, addition:int=1):
        """Incrémente la position du joueur dans le classement."""

        self.position += addition

    def actualiser_portion_actuelle(self, portion:PortionCircuit) -> None:
        """Actualise la portion de circuit dans laquelle le kart du joueur est en la remplaçant par celle donnée en paramètre."""
        self.portion_circuit = portion        
