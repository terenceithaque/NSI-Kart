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



class PortionCircuit:
    """Une portion de route sur un circuit."""
    def __init__(self, fenetre:pygame.Surface, image:str="assets/images/route.png", orient_image=0, longueur=1280, largeur=720, numero=1):
        """Initialise la portion de route.
        - fenetre : fenêtre de jeu dans laquelle la portion de route est affichée
        - image : image représentant la portion de route
        - orient_image : degré de rotation de l'image représentant la portion de route
        - longueur : longueur de la portion en pixels
        - largeur : largeur de la portion en pixels
        - numero : numéro identifiant de la portion"""


        # Initialisation des attributs
        self.fenetre = fenetre
        self.image = pygame.image.load(image)
        self.image = pygame.transform.rotate(self.image, orient_image)
        self.image = pygame.transform.scale(self.image, (longueur, largeur))
        self.rect_image = self.image.get_rect()

        self.numero = numero

    def afficher(self) -> None:
        """Affiche la portion de route à l'écran"""
        self.fenetre.blit(self.image, self.rect_image)    



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


        self.portions = [] # Liste des différentes portions de circuit
        self.portions_numeros = {} # Dictionnaire liant les numéros (identifiants) de portions avec les objets PortionCircuit correspondants

        # Le circuit commence toujours par la ligne de départ / arrivée
        self.portion_depart = PortionCircuit(self.fenetre, "assets/images/ligne_arrivee.png",0, 1280, 720, numero=1)
        self.portions.append(self.portion_depart)
        self.portions_numeros[self.portion_depart.numero] = self.portion_depart

        self.portion_actuelle = self.portion_depart # Portion de circuit actuelle


    def nombre_portions(self) -> int:
        """Renvoie le nombre maximum de portions dont le circuit est composé."""


        n_portions = 0
        # On parcoure l'ensemble des données du circuit
        for ligne in range(len(self.donnees)):
            for col in range(len(self.donnees[ligne])):
                # On considère que chaque nombre 1 ou 2 correspond à une portion de circuit indépendante
                if self.donnees[ligne][col] == 1 or self.donnees[ligne][col] == 2:
                    n_portions += 1 # On incrémente le nombre total de portions

        return n_portions            


    def est_sur_la_route(self, coordonnees:tuple=(0,0)) -> bool:
        """Renvoie True si le point de coordonnées donné correspond à une partie de la route du circuit (valeur égale à 1 ou 2). Sinon, renvoie False."""
        x = coordonnees[0]
        y = coordonnees[1]        
        return self.donnees[x][y] > 0
    

    def coordonnees_ligne_arrivee(self, n=1) -> tuple[int, int]:
        """Renvoie les coordonnées de la n-ième ligne d'arrivée dans les données du circuit.
        -n : nombre entier, désigne le numéro de la ligne d'arrivée dont on cherche les coordonnées. Par exemple, pour n=1, cela renvoie les coordonnées de la première
        ligne d'arrivée trouvée."""

        l = 0 # Ligne dans les données
        col= 0 # Colonne dans les données
        n_lignes_arrivee = 0 # Nombre de lignes d'arrivée trouvées

        while n_lignes_arrivee < n:
            # Parcourir chaque ligne et chaque colonne dans le tableau de données
            for ligne in range(len(self.donnees)):
                for colonne in range(len(self.donnees[col])):
                    # Si la case actuelle représente une ligne d'arrivée
                    if self.donnees[ligne][colonne] == 2:
                        n_lignes_arrivee += 1 # Incrémenter le compteur de lignes d'arrivée trouvées
                        # Mettre à jour les coordonnées dans le tableau
                        l = ligne
                        col = colonne

        return (l, col)            


    def ajouter_portion(self, portion:PortionCircuit) -> None:
        """Intègre une portion de circuit (type PortionCircuit) au circuit de course."""
        self.portions.append(portion) # On ajoute la portion à la liste des portions
        if portion.numero < self.nombre_portions():
            self.portions_numeros[portion.numero] = portion


    def mettre_a_jour_portion_actuelle(self, portion:PortionCircuit) -> None:
        """Met à jour la portion de circuit actuelle en la remplaçant par la portion donnée en paramètre."""
        self.portion_actuelle = portion        


    def tourne_a_droite(self, coordonnees:tuple=(0, 0)) -> bool:
        """Renvoie True si la prochaine case représentant une portion de route est située à droite de celle désignée par les coordonnées indiquées."""

        x = coordonnees[0]
        y = coordonnees[1]

        assert self.est_sur_la_route(coordonnees), f"Impossible de vérifier si la route tourne à droite par rapport à un point qui n'est pas sur la route ({coordonnees[0]}, {coordonnees[1]})."

        for ligne in range(x, len(self.donnees)):
            print(ligne)
            for colonne in range(y -1):
                print(colonne)
                if self.donnees[ligne][colonne + 1] == 1 or self.donnees[ligne][colonne+1] == 2:
                    return True

        return False

    def est_tout_droit(self, coordonnees:tuple=(0, 0), direction:str="haut") -> bool:
        """Vérifie si la route du circuit continue tout droit dans la direction donnée."""

        # Assertions
        assert self.est_sur_la_route(coordonnees), f"Impossible de vérifier si la route tourne à droite par rapport à un point qui n'est pas sur la route ({coordonnees[0]}, {coordonnees[1]})."

        x = coordonnees[0] # Ligne actuelle
        y = coordonnees[1] # Colonne actuelle


        # Direction "haut"
        if direction == "haut":
            for ligne in range(x, 0, -1):
                if self.donnees[ligne][y] in [1, 2]:
                    return True
            
                
                

        # Direction "bas"
        elif direction == "bas":
            for ligne in range(x, len(self.donnees) -1):
                if self.donnees[ligne+1][y] in [1, 2]:
                    return True
                                
        # Direction "gauche"
        elif direction == "gauche":
            for colonne in range(y, 0, -1):
                if self.donnees[x][colonne] in [1, 2]:
                    return True
                

        # Direction "droite"
        elif direction == "droite":
            for colonne in range(y, len(self.donnees[x]) -1):
                if self.donnees[x][colonne+1] in [1, 2]:
                   return True
                

        return False
    

    def afficher(self) -> None:
        """Affiche la portion actuelle du circuit à l'écran."""
        self.portion_actuelle.afficher()
                



                   
