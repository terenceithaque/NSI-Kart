# Script des circuits
import pygame
pygame.init()
import json
import os


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


class Circuit:
    "Un circuit de course."
    def __init__(self, fenetre:pygame.Surface, numero:int=1) -> None:
        """Initialise le circuit.
        -fenetre : fenêtre de jeu dans laquelle le circuit s'affiche
        -numero : numéro du circuit permettant de l'identifier et d'en charger les données. Doit être compris entre 1 et le nombre total de circuits dans le jeu."""

        # Initialisation des attributs
        self.fenetre = fenetre
        self.numero = numero # Numéro du circuit

        # Charger les données JSON du circuit
        self.donnees = trace_circuit(self.numero)

        # Dans les données du circuit, on considère que les "1" représentent la route devant être suivie par les karts
        # Les "2" représentent la ligne de la / les ligne(s) de départ / arrivée.
        # Les "0" quant à eux, désignent tout ce qui est en dehors de la route.
        self.localisations = {
            0:"hors_route",
            1:"route",
            2:"ligne_arrivee"
        }