# Script des adversaires du joueur
import pygame
from kart import *



class Adversaire:
    """Une classe liant tous les éléments d'un adversaire (position, kart, etc)."""
    def __init__(self, fenetre:pygame.Surface, kart:Kart, position_depart:int=1):
        """Initialise l'adversaire.
        - fenetre : fenêtre où les informations relatives à l'adversaire sont affichées
        - kart : le kart de l'adversaire,
        - position_depart : position de départ de l'adversaire."""


        # Initialisation des attributs
        self.fenetre = fenetre
        self.kart = kart # Kart de l'adversaire
        self.position_depart = position_depart # Position de départ de l'adversaire
        self.position = self.position_depart # Position actuelle de l'adversaire dans le classement


    def incrementer_position(self, addition:int=1):
        """Incrémente la position de l'adversaire dans le classement."""

        self.position += addition    