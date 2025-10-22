# Programme principal du jeu
import pygame
pygame.init()
from kart import *
from circuits import *
from joueur import *
from course import *



# Créer la fenêtre de jeu
fenetre = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("NSI-Kart")


course = Course(fenetre, 12, 12, 1)
course.courir()