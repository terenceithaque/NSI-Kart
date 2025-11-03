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



class PortionCircuit:
    """Une portion de route sur un circuit."""
    def __init__(self, fenetre:pygame.Surface, image:str="assets/images/route.png", orient_image=0, longueur=1280, largeur=720, numero=1, direction:str="haut",
                 adversaires=None):
        """Initialise la portion de route.
        - fenetre : fenêtre de jeu dans laquelle la portion de route est affichée
        - image : image représentant la portion de route
        - orient_image : degré de rotation de l'image représentant la portion de route
        - longueur : longueur de la portion en pixels
        - largeur : largeur de la portion en pixels
        - numero : numéro identifiant de la portion
        - direction : direction vers laquelle la portion de circuit est orientée
        - adversaires : liste des adversaires présents dans la portion."""


        # Initialisation des attributs
        self.fenetre = fenetre
        self.image = charger_image_en_cache(image, orient_image, (longueur, largeur))
        self.rect_image = self.image.get_rect()

        self.numero = numero
        self.direction = direction
        self.ligne_arrivee_placee = False
        self.ligne_arrivee = None
        self.orient = orient_image
        self.longueur = longueur
        self.largeur = largeur
        if adversaires is None:
            self.adversaires = []

        else:    
            self.adversaires = adversaires
    

    def placer_ligne_arrivee(self) -> None:
        """Place une ligne d'arrivée sur la portion de circuit."""
        if not self.ligne_arrivee_placee:
            epaisseur_ligne = 20
            self.ligne_arrivee = LigneArrivee(self.fenetre, self.orient, self.longueur, epaisseur_ligne, 0, self.largeur // 2 - epaisseur_ligne // 2)
            self.ligne_arrivee_placee = True


    def est_ligne_arrivee_passee(self, objet) -> bool:
        """Si la portion de circuit possède est une ligne d'arrivée et qu'elle est passée, renvoie True, et False sinon. Si la portion ne possède aucune ligne d'arrivée, renvoie False."""        
        
        if self.ligne_arrivee_placee:
            if self.ligne_arrivee.est_passee(objet):
                return True
            
            return False
        
        return False

    def afficher(self) -> None:
        """Affiche la portion de route à l'écran"""
        self.fenetre.blit(self.image, self.rect_image)
        if self.ligne_arrivee_placee:
            self.ligne_arrivee.afficher()    



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
        self.portion_depart = PortionCircuit(self.fenetre, "assets/images/route.png",0, 1280, 720, numero=1)
        self.portion_depart.placer_ligne_arrivee()
        self.coordonnees_depart = self.coordonnees_ligne_arrivee(1) # On récupère les coordonnées de la première ligne de départ / arrivée
        self.coordonnees_portion_actuelle = self.coordonnees_depart # Coordonnées de la portion actuellement chargée

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
    

    def prochaine_direction(self, x:int=0, y:int=0, direction_actuelle:str="haut") -> str:
        """Renvoie la direction vers laquelle continue la route à partir de la case (x, y)."""

        directions = {
            "haut":(-1, 0),
            "bas":(1, 0),
            "gauche":(0, -1),
            "droite":(0, 1)
        }


        # On vérifie les 4 cases voisines
        for direction, (dx, dy) in directions.items():
            x_case, y_case = x + dx, y + dy
            if 0 <= x_case < len(self.donnees) and 0 <= y_case < len(self.donnees[0]):
                # Ignorer la case d'où l'on vient
                if direction_actuelle == "haut" and direction == "bas": continue
                if direction_actuelle == "bas" and direction == "haut": continue
                if direction_actuelle == "gauche" and direction == "droite": continue
                if direction_actuelle == "droite" and direction == "gauche": continue


                if self.donnees[x_case][y_case] in (1, 2):
                    return direction
            
        return None    


    def mettre_a_jour_coords_portion_actuelle(self, direction="haut") -> None:
        """Met à jour les coordonnées de la portion de circuit actuelle en fonction de la direction."""

        # Direction "haut"
        if direction == "haut":
            if self.coordonnees_portion_actuelle[0] > 0:
                self.coordonnees_portion_actuelle[0] -= 1

        # Direction "bas"
        elif direction == "bas":
            if self.coordonnees_portion_actuelle[0] < (len(self.donnees)-1):  
                self.coordonnees_portion_actuelle[0] += 1

        # Direction "gauche"
        elif direction == "gauche":
            if self.coordonnees_portion_actuelle[1] > 0:
                self.coordonnees_portion_actuelle[1] -=1

        # Direction "droite"
        elif direction == "droite":
            if self.coordonnees_portion_actuelle[1] < (len(self.donnees[0]) -1):
                self.coordonnees_portion_actuelle[1] += 1



    def est_sur_la_route(self, coordonnees:tuple=(0,0)) -> bool:
        """Renvoie True si le point de coordonnées donné correspond à une partie de la route du circuit (valeur égale à 1 ou 2). Sinon, renvoie False."""
        x = coordonnees[0]
        y = coordonnees[1]        
        return self.donnees[x][y] > 0
    

    def coordonnees_ligne_arrivee(self, n=1) -> list[int, int]:
        """Renvoie les coordonnées de la n-ième ligne d'arrivée dans les données du circuit.
        -n : nombre entier, désigne le numéro de la ligne d'arrivée dont on cherche les coordonnées. Par exemple, pour n=1, cela renvoie les coordonnées de la première
        ligne d'arrivée trouvée.
        Note: donner la valeur 'all' à n modifie le comportement de cette méthode en renvoyant une liste contenant lezs coordonnées de chaque ligne d'arrivée trouvée."""

        l = 0 # Ligne dans les données
        col= 0 # Colonne dans les données
        n_lignes_arrivee = 0 # Nombre de lignes d'arrivée trouvées
        
        if isinstance(n, int):
            while n_lignes_arrivee < n:
                # Parcourir chaque ligne et chaque colonne dans le tableau de données
                for ligne in range(len(self.donnees)):
                    for colonne in range(len(self.donnees[ligne])):
                        # Si la case actuelle représente une ligne d'arrivée
                        if self.donnees[ligne][colonne] == 2:
                            n_lignes_arrivee += 1 # Incrémenter le compteur de lignes d'arrivée trouvées
                            # Mettre à jour les coordonnées dans le tableau
                            l = ligne
                            col = colonne

            return [l, col]

        elif n == "all":
            liste_coordonnees = []
            for ligne in range(len(self.donnees)):
                for colonne in range(len(self.donnees[col])):
                    if self.donnees[ligne][colonne] == 2:
                        n_lignes_arrivee += 1
                        l = ligne
                        col = colonne
                        liste_coordonnees.append((l, col))           


    def ajouter_portion(self, portion:PortionCircuit) -> None:
        """Intègre une portion de circuit (type PortionCircuit) au circuit de course."""
        self.portions.append(portion) # On ajoute la portion à la liste des portions
        if portion.numero < self.nombre_portions():
            self.portions_numeros[portion.numero] = portion


    def rotation_virage(self, ancienne_direction:str, nouvelle_direction:str) -> int:
        """Renvoie la rotation de l'image du virage nécessaire selon l'ancienne et la nouvelle direction."""

        table = {
            # Virages vers la droite
            ("haut", "droite"): 0,
            ("droite", "bas"): 90,
            ("bas", "gauche"):180,
            ("gauche", "haut"): 270,

            # Virages vers la gauche
            ("haut", "gauche"): 270,
            ("gauche", "bas"): 0,
            ("bas", "droite"): 270,
            ("droite", "haut"): 180,
        }

        return table.get((ancienne_direction, nouvelle_direction), 0)
    
    def portions_autour(self,n_portion) -> list:
        "Renvoie une liste contenant les deux portions situées autour de celle dont le numéro est donné en paramètre, étant la précédente et la suivante."
        # Assertions
        assert n_portion >= 1 and n_portion <= self.nombre_portions()
        
        portions = [] # Liste des deux portions autour
        
        # Récupérer la portion correspondant au numéro
        portion = self.portions_numeros[n_portion]
        
        # Récupérer la portion suivante
        if n_portion < self.nombre_portions():
            portion_suivante = self.portions_numeros[n_portion + 1]
            portions.append(portion_suivante)
        
        elif n_portion == self.nombre_portions():
            portion_suivante = self.portions_numeros[1]
            portions.append(portion_suivante)
        
        # Récupérer la portion précédente
        if n_portion > 1:
            portion_precedente = self.portions_numeros[n_portion - 1]
            portions.append(portion_precedente)
        
        elif n_portion == 1:
            portion_precedente = self.portions_numeros[self.nombre_portions()]
            portions.append(portion_precedente)
        
        return portions
            
        
        


    def mettre_a_jour_portion_actuelle(self, portion:PortionCircuit) -> None:
        """Met à jour la portion de circuit actuelle en la remplaçant par la portion donnée en paramètre."""
        self.portion_actuelle = portion


    def case_adjacente(self, x=0, y=0, direction="haut") -> int:
        """Renvoie le contenu de la case adjacente à celle de coordonnées (x, y) dans la direction donnée. Si la case de coordonnées (x, y) est à l'extrémité de la direction donnée, son contenu est renvoyé."""
        # Direction "haut"
        if direction == "haut":
            if x == 0:
                return self.donnees[x][y]

            else:
                return self.donnees[x-1][y]

        # Direction "bas"
        elif direction == "bas":
            if x == len(self.donnees) -1:
                return self.donnees[x][y]

            else:
                return self.donnees[x+1][y]

        # Direction "gauche"
        elif direction == "gauche":
            if y == 0:
                return self.donnees[x][y]

            else:
                return self.donnees[x][y-1]

        # Direction "droite"
        elif direction == "droite":
            if y == len(self.donnees[0]) -1:
                return self.donnees[x][y]

            else:
                return self.donnees[x][y+1]

        # Renvoyer des données valides au cas où dans tous les cas
        return self.donnees[x][y]            




    def charger_prochaine_portion(self, update=True, adversaires=[]) -> None:
        """Charge la prochaine portion du circuit.
        - update : booléen, met à jour directement la portion actuelle si sa valeur est True. Sinon, charge la prochaine portion mais ne met pas à jour l'actuelle."""
        

        #self.portion_actuelle.adversaires = []

        # Retrouver les portions déjà chargées
        if self.portion_actuelle.numero < self.nombre_portions() and self.portion_actuelle.numero + 1 in self.portions_numeros:
            #print("Chargement d'une portion existante")
            portion_suivante = self.portions_numeros[self.portion_actuelle.numero + 1]
            if len(adversaires) > 0:
    
                portion_suivante.adversaires.extend(adversaires)
                #print(portion_suivante.adversaires)
            
            if update:
                self.mettre_a_jour_portion_actuelle(portion_suivante)
                self.mettre_a_jour_coords_portion_actuelle(portion_suivante.direction)


        # Si toutes les portions ont été utilisées, revenir à celle de départ
        elif self.portion_actuelle.numero == self.nombre_portions():
            print("Retour à la portion initiale !")
            portion_suivante = self.portions_numeros[1]
            portion_suivante.placer_ligne_arrivee()
            if len(adversaires) > 0:
                
                portion_suivante.adversaires.extend(adversaires)
            
            if update:
                self.mettre_a_jour_portion_actuelle(portion_suivante)
                self.mettre_a_jour_coords_portion_actuelle(portion_suivante.direction)    

        else:
            x, y = self.coordonnees_portion_actuelle
            #print(f"Coordonnées de l'ancienne portion : ({x}, {y})")
            direction_suivante = self.prochaine_direction(x, y, self.portion_actuelle.direction)

            directions_route = {
                "haut":{
                    "gauche":["assets/images/virage_gauche.png", self.rotation_virage("haut", "gauche")],
                    "droite":["assets/images/virage_droite.png", self.rotation_virage("haut", "droite")],
                    "haut":["assets/images/route.png", 0]
                },
                "bas":{
                    "gauche":["assets/images/virage_gauche.png", self.rotation_virage("bas", "gauche")],
                    "droite":["assets/images/virage_droite.png", self.rotation_virage("bas", "droite")],
                    "bas":["assets/images/route.png", 0]
                },
                "gauche":{
                    "haut":["assets/images/virage_gauche.png", self.rotation_virage("gauche", "haut")],
                    "bas":["assets/images/virage_droite.png", self.rotation_virage("gauche", "bas")],
                    "gauche":["assets/images/route.png", 90]
                },
                "droite":{
                    "haut":["assets/images/virage_droite.png", self.rotation_virage("droite", "haut")],
                    "bas":["assets/images/virage_gauche.png", self.rotation_virage("droite", "bas")],
                    "droite":["assets/images/route.png", 90]
                }
                
            }

            directions = directions_route[self.portion_actuelle.direction]
            #print(directions)
            for direction in directions.keys():
                if direction == direction_suivante:
                    portion_suivante = PortionCircuit(self.fenetre, directions[direction][0], directions[direction][1], numero=len(self.portions)+1, direction=direction, adversaires=adversaires)
                    # Si la portion suivante a une ligne d'arrivée, la placer
                    if self.case_adjacente(x, y, direction_suivante) == 2:
                        portion_suivante.placer_ligne_arrivee()
                        
                    self.ajouter_portion(portion_suivante)
                    if update:
                        self.mettre_a_jour_portion_actuelle(portion_suivante)
                        self.mettre_a_jour_coords_portion_actuelle(direction)


        """x, y = self.coordonnees_portion_actuelle
        #print(f"Coordonnées de l'ancienne portion : ({x}, {y})")
        direction_suivante = self.prochaine_direction(x, y, self.portion_actuelle.direction)

        print("Direction suivante :", direction_suivante)
        if not direction_suivante:
            print("Fin du circuit ou erreur de tracé.")
            return
        
        # Mise à jour des coordonnéees
        if direction_suivante == "haut": 
            x -= 1

        elif direction_suivante == "bas":   
            x += 1

        elif direction_suivante == "gauche": 
            y -= 1

        elif direction_suivante == "droite": 
            y += 1

        self.coordonnees_portion_actuelle = [x, y]

        # Choix de l'image selon la direction
        if direction_suivante in ["haut", "bas"]:
            image = "assets/images/route.png"
            rotation = 0

        else:
            image = "assets/images/route.png"
            rotation = 90

        # Gestion des virages
        if direction_suivante == "gauche" and self.portion_actuelle.direction != "gauche":
            image = "assets/images/virage_gauche.png"
            rotation = self.rotation_virage(self.portion_actuelle.direction, direction_suivante)

        elif direction_suivante == "droite" and self.portion_actuelle.direction != "droite":
            image = "assets/images/virage_droite.png"
            rotation = self.rotation_virage(self.portion_actuelle.direction, direction_suivante)    

        portion_suivante = PortionCircuit(self.fenetre, image=image, orient_image=rotation, numero=len(self.portions)+1, direction=direction_suivante)
        self.ajouter_portion(portion_suivante)
        self.mettre_a_jour_portion_actuelle(portion_suivante)"""            




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
                



                   
