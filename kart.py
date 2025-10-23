# Script des karts
import pygame
import random


def choisir_image_kart(n_min:int=1, n_max:int=6) -> str:
    """Choisit une image de kart au hasard parmi les numéros de karts allant de n_min à n_max."""

    n = random.randint(n_min, n_max)

    return f"assets/images/kart{n}.png"


class Kart(pygame.sprite.Sprite):
    "Classe représentant un kart en course."

    def __init__(self, fenetre:pygame.Surface, image:str="assets/images/kart1.png", x:int=0, y:int=0, vitesse_max=50.0, acceleration=0.5, direction="haut") -> None:
        """Initialise le kart
        - fenetre : fenêtre de jeu dans laquelle le kart est affiché
        - image : chemin de l'image représentannt le kart
        - x : position x de départ du kart
        - y : position y de départ du kart
        - vitesse_max : vitesse maximale du kart
        - acceleration : taux d'accélération du kart par secondes, par défaut 0.5
        - direction : direction dans laquelle le kart se dirige, par défaut vers le haut"""

        # Initialisation des attributs
        self.fenetre = fenetre
        self.chemin_image = image
        # Image originale du kart
        self.image = pygame.image.load(self.chemin_image)
        self.image = pygame.transform.scale(self.image, (100, 100))
    

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.vitesse_haut = 0.0
        self.vitesse_bas = 0.0
        self.vitesse_gauche = 0.0
        self.vitesse_droite = 0.0
        self.acceleration = acceleration
        self.vitesse_max = vitesse_max
        self.moteur_allume = False # Le moteur du kart est-il allumé ?

        self.direction = direction # Direction actuelle du kart
        self.direction_suivante = self.direction # Direction suivante


    def changer_direction(self, nouvelle_direction:str) -> None:
        "Modifie la direction du kart"
        self.direction_suivante = nouvelle_direction


    def est_hors_ecran(self) -> bool:
        "Renvoie True si le kart est sorti de l'écran, False sinon."

        dimensions = self.fenetre.get_size()
        x = dimensions[0]
        y = dimensions[1]

        return any([self.rect.x < 0, self.rect.x > x,
                   self.rect.y < 0, self.rect.y > y])


    def est_hors_circuit(self, longueur_portion:int, largeur_portion:int) -> bool:
        "Renvoie True si le kart est en dehors de la portion du circuit actuelle, False sinon."
        return any([self.rect.x > longueur_portion, self.rect.y > largeur_portion])

    def changer_position(self, coordonnes:tuple[int, int]) -> None:
        """Remplace la position actuelle du kart par celle donnée en paramètre."""

        self.rect.x = coordonnes[0]
        self.rect.y = coordonnes[1] 


    def mettre_a_jour_rotation(self):
        """Met à jour l'angle de rotation du kart."""

        # Il faudra gérer les différences d'angles selon la direction actuelle
        
        angles_haut = {
            "haut":0,
            "bas":180,
            "droite":-90,
            "gauche":90
        }

        angles_bas = {
            "haut":180,
            "bas":0,
            "droite":90,
            "gauche":-90
        }

        angles_gauche = {
            "haut":-90,
            "bas":90,
            "droite":180,
            "gauche":0,
            
        }

        angles_droite = {
            "haut":90,
            "bas":-90,
            "droite":0,
            "gauche":180
        }

        if self.direction == "haut": # Si le kart se déplace actuellement vers le haut
            # Appliquer la rotation de l'image du kart selon l'angle nécessaire pour la direction suivante
            angle = angles_haut.get(self.direction_suivante, 0)
            self.image = pygame.transform.rotate(self.image, angle)

        # Idem pour les autres directions
        elif self.direction == "bas":
            angle = angles_bas.get(self.direction_suivante, 0)
            self.image = pygame.transform.rotate(self.image, angle)

        elif self.direction == "gauche":
            angle = angles_gauche.get(self.direction_suivante, 0)
            self.image = pygame.transform.rotate(self.image, angle)

        elif self.direction == "droite":
            angle = angles_droite.get(self.direction_suivante, 0)
            self.image = pygame.transform.rotate(self.image, angle)            

        # Conserver le centre après rotation
        centre = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = centre


    def mettre_a_jour_direction(self) -> None:
        """Met à jour la direction actuelle du kart par rapport à la suivante."""
        self.direction = self.direction_suivante            

    def accelerer(self) -> None:
        """Accélère le kart si sa vitesse est inférieure à la vitesse maximale."""
        if self.direction == "haut":
            if self.vitesse_haut < self.vitesse_max:
                self.vitesse_haut += (self.acceleration * self.vitesse_max)
                print("Vitesse du kart (haut) :", self.vitesse_haut)

        elif self.direction == "bas":
            if self.vitesse_bas < self.vitesse_max:
                self.vitesse_bas += (self.acceleration * self.vitesse_max)
                print("Vitesse du kart (bas) :", self.vitesse_bas)

        elif self.direction == "gauche":
            if self.vitesse_gauche < self.vitesse_max:
                self.vitesse_gauche += (self.acceleration * self.vitesse_max)
                print("Vitesse du kart (gauche) :", self.vitesse_gauche)

        elif self.direction == "droite":
            if self.vitesse_droite < self.vitesse_max:
                self.vitesse_droite += (self.acceleration * self.vitesse_max)
                print("Vitesse du kart (droite) :", self.vitesse_droite)


    def decelerer(self) -> None:
        """Le kart ralentit."""
        if self.vitesse_haut > 0:
            self.vitesse_haut *= 0.95
            print("Vitesse du kart (haut) :", self.vitesse_haut) 

        if self.vitesse_bas > 0:    
            self.vitesse_bas *= 0.95
            print("Vitesse du kart (bas) :", self.vitesse_bas)

        if self.vitesse_gauche > 0:    
            self.vitesse_gauche *= 0.95
            print("Vitesse du kart (gauche) :", self.vitesse_gauche)

        if self.vitesse_droite > 0:    
            self.vitesse_droite *= 0.95
            print("Vitesse du kart (droite) :", self.vitesse_droite)           


    def deplacer(self) -> None:
        """Déplace le kart dans sa direction actuelle."""
        if self.direction == "haut":
            self.rect.y -= self.vitesse_haut

        elif self.direction == "bas":
            self.rect.y += self.vitesse_bas

        elif self.direction == "gauche":
            self.rect.x -= self.vitesse_gauche

        elif self.direction == "droite":
            self.rect.x += self.vitesse_droite                                                


    def afficher(self) -> None:
        """Affiche le kart à l'écran."""
        self.fenetre.blit(self.image, (self.rect.x, self.rect.y))    

