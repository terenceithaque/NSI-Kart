# Script des circuits
import pygame
pygame.init()
import json
import os
from ligne_arrivee import *


# Cache d'images des portions
cache_images = {}

def charger_image_en_cache(chemin:str, rotation:int=0, taille:tuple=(1280, 720)) -> pygame.Surface:
    """Charge l'image demandée depuis le cache d'images. Si cette image n'y est pas présente, elle y est ajoutée."""
    cle = (chemin, rotation, taille)
    if cle not in cache_images:
        base = pygame.image.load(chemin).convert_alpha()
        if rotation:
            base = pygame.transform.rotate(base, rotation)

        if taille:
            base = pygame.transform.scale(base, taille)    

        cache_images[cle] = base

    return cache_images[cle]    


def trace_circuit(numero_circuit:int=1) -> list:
    """Ouvre le fichier circuits.json et renvoie le tracé du circuit correspondant au numéro donné sous forme de tableau en 2D."""
    fichier_circuits = "circuits.json" # Nom du fichier regroupant les données des circuits
    dossier_courant = os.path.abspath(os.path.dirname(__file__)) # Dossier courant du script
    chemin_fichier = os.path.join(dossier_courant, fichier_circuits) # Chemin complet du fichier de circuits


    # Ouvrir le fichier et en extraire les données
    with open(chemin_fichier, "r") as f:
        donnees = json.load(f)
    

    
    dict_circuits = dict(donnees["circuits"]) # On convertit les données de circuits sous forme de dictionnaire
    assert str(numero_circuit) in dict_circuits.keys(), "Numéro de circuit invalide" # Erreur si le numéro de circuit donné est invalide (absent des clés du dictionnaire)
    return dict_circuits[str(numero_circuit)] # Renvoyer le tableau de données correspondant au circuit désigné par le numéro



class Plateau:
    """Plateau de jeu représentant le circuit"""
    def __init__(self, fenetre:pygame.Surface):
        
        # Fenêtre pygame
        self.fenetre = fenetre
        self.dimensions_fenetre = self.fenetre.get_size()
        self.x_fenetre = self.dimensions_fenetre[0]
        self.y_fenetre = self.dimensions_fenetre[1]
        
    def affiche(self) -> None:
        pass


        
        