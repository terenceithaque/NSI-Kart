# Script des adversaires du joueur
import pygame
from kart import *
import random

# Noms disponibles pour les adversaires
noms = ["Jean-Louis", "Daniel", "Marie", "Bernard", "Mario", "Luigi", "Judith", "Nicolas"]



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
        self.tour = 1  # Numéro du tour actuel de l'adversaire, au départ 1
        self.nom = random.choice(noms)
        self.police_nom = pygame.font.Font(None, 36)


    def afficher_nom(self):
        """Affiche le nom de l'adversaire à l'écran."""
        affichage_nom = self.police_nom.render(self.nom, False, (255, 255, 255))
        self.fenetre.blit(affichage_nom, (self.kart.rect.x, self.kart.rect.y - 5))


    def incrementer_position(self, addition:int=1):
        """Incrémente la position de l'adversaire dans le classement."""

        self.position += addition 

    def afficher(self):
        """Affiche le kart et le nom de l'adversaire."""
        self.kart.afficher()
        self.afficher_nom()       