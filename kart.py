# Script des karts
import pygame


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

        self.direction = direction


    def changer_direction(self, nouvelle_direction:str) -> None:
        "Modifie la direction du kart"
        self.direction = nouvelle_direction


    def mettre_a_jour_rotation(self):
        """Met à jour l'angle de rotation du kart."""
        angles = {
            "haut":0,
            "droite":-90,
            "bas":180,
            "gauche":90
        }

        angle = angles.get(self.direction, 0)
        self.image = pygame.transform.rotate(self.image, angle)

        # Conserver le centre après rotation
        centre = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = centre        

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

