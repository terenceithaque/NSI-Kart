# Script du joueur
import pygame
from kart import *
from circuits import *


class Joueur:
    """Une classe liant tous les éléments du joueur (position, kart, etc)."""
    def __init__(self, fenetre:pygame.Surface, kart:Kart, portion_depart:PortionCircuit, position_depart:int=12, nom:str="Vous"):
        """Initialise le joueur.
        - fenetre : fenêtre où les différentes informations concernant le joueur sont affichées
        - kart: le kart du joueur
        - portion_depart : portion de circuit dans laquelle le kart du joueur est au départ
        - position_depart : position de départ du joueur
        - nom : nom du joueur."""

        # Initialisation des attributs
        self.fenetre = fenetre
        self.kart = kart # Kart du joueur
        self.position_depart = position_depart # Position de départ du joueur

        self.position = self.position_depart # Position actuelle du joueur dans le classement
        self.portion_circuit = portion_depart
        self.police_position = pygame.font.Font(None, 36)

        self.tour = 1 # Numéro du tour actuel du joueur, au départ 1
        self.nom = nom
        self.police_nom = pygame.font.Font(None, 36)

    def incrementer_position(self, addition:int=1):
        """Incrémente la position du joueur dans le classement."""

        self.position += addition
        # La position du joueur ne peut jamais être inférieure à 1
        if self.position < 1:
            self.position = 1

    def afficher_position(self) -> None:
        """Affiche la position du joueur à l'écran."""
        # Dictionnaire liant les différentes positions à des couleurs d'affichage en RGB
        positions_couleurs = {
            1: (255, 255, 0),
            2: (128, 128, 128),
            3: (128, 0, 0),
            4: (255, 165, 0),
            5: (237, 158, 11),
            6: (244, 164, 15),
            7: (213, 145, 19),
            8: (187, 129, 22),
            9: (175, 121, 21),
            10: (139, 100, 27),
            11: (119, 85, 25),
            12: (107, 78, 24)
        }

        affichage_position = self.police_position.render(str(self.position), False, positions_couleurs[self.position])
        self.fenetre.blit(affichage_position, (1196, 561))

    def afficher_nom(self):
        """Affiche le nom du joueur à l'écran, près du kart."""
        affichage_nom = self.police_nom.render(self.nom, False, (255, 255, 255))
        self.fenetre.blit(affichage_nom, (self.kart.rect.x, self.kart.rect.y + 5))        

    def actualiser_portion_actuelle(self, portion:PortionCircuit) -> None:
        """Actualise la portion de circuit dans laquelle le kart du joueur est en la remplaçant par celle donnée en paramètre."""
        self.portion_circuit = portion

    def afficher(self):
        """Affiche les informations relatives au joueur (kart, nom, position, etc.) à l'écran."""
        self.kart.afficher()
        self.afficher_nom()
        self.afficher_position()            
