# Programme principal du jeu
import pygame
pygame.init()
from course import *
from tkinter import simpledialog

# Demander le nom du joueur
nom_joueur = simpledialog.askstring("Votre nom:", "Saisissez votre nom de joueur:", initialvalue="Vous")
if not nom_joueur:
    nom_joueur = "Vous"



# Créer la fenêtre de jeu
fenetre = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("NSI-Kart")


course = Course(fenetre, 12, 12, 1, nom_joueur, positions_scores = {
            1:15,
            2:12,
            3:10,
            4:9,
            5:8,
            6:7,
            7:6,
            8:5,
            9:4,
            10:3,
            11:2,
            12:1
        })

course.courir() 