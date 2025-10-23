# Script d'une course
import pygame
pygame.init()
from kart import *
from circuits import *
from joueur import *


class Course:
    """Classe représentant une course indépendante."""
    def __init__(self, fenetre:pygame.Surface, n_participants:int=12, position_joueur=12, numero_circuit=1):
        """Initialise la course.
        - fenetre : fenêtre de jeu dans laquelle les éléments de la course sont affichés
        - n_participants : nombre de participants à la course (adversaires + joueur),
        - position_joueur : position de départ du joueur
        - numero_circuit : numéro du circuit de course."""

        # Initialisation des attributs
        self.fenetre = fenetre
        assert 0 < position_joueur <= n_participants, f"La position de départ du joueur doit être comprise entre 1 et {n_participants}."

        self.kart_joueur = Kart(self.fenetre, choisir_image_kart(1, 6), 120, 600, 6.0, 0.25, "haut") # Kart du joueur
        self.joueur = Joueur(self.fenetre, self.kart_joueur, None, position_joueur) # Joueur

        self.circuit = Circuit(self.fenetre, numero_circuit)
        print(self.circuit.donnees)
        print(self.circuit.tourne_a_droite((0, 3)))
        print(self.circuit.est_tout_droit((0, 4), "bas"))


    def courir(self) -> None:
        """Démarre la course."""


        acceleration = pygame.USEREVENT + 1
        deceleration = pygame.USEREVENT + 2
        pygame.time.set_timer(acceleration, 500)


        execution = True


        # Boucle principale
        while execution:
                #pygame.time.wait(1000)


                if not self.kart_joueur.moteur_allume:
                    self.kart_joueur.decelerer()

                self.fenetre.fill((255, 255, 255))


                self.circuit.afficher()

                touches = pygame.key.get_pressed()


                #print(self.kart_joueur.rect.x, self.kart_joueur.rect.y)

                for evenement in pygame.event.get():
                    if evenement.type == pygame.QUIT:
                        pygame.quit()

                    if evenement.type == acceleration:
                        if self.kart_joueur.moteur_allume: 
                            self.kart_joueur.accelerer()

                    if evenement.type == deceleration:
                        if not self.kart_joueur.moteur_allume:
                            self.kart_joueur.decelerer()        

                    if evenement.type == pygame.KEYUP:
                        if evenement.key == pygame.K_SPACE:
                            self.kart_joueur.moteur_allume = not self.kart_joueur.moteur_allume
                            if self.kart_joueur.moteur_allume == False:
                                pygame.time.set_timer(acceleration, 0)
                                pygame.time.set_timer(deceleration, 1000)

                            else:
                                pygame.time.set_timer(deceleration, 0)
                                pygame.time.set_timer(acceleration, 500)    


                    if evenement.type == pygame.MOUSEMOTION:
                        print(pygame.mouse.get_pos())


                if not self.kart_joueur.moteur_allume:
                    self.kart_joueur.decelerer()               

                if touches[pygame.K_RIGHT]:
                    self.kart_joueur.changer_direction("droite")
                    self.kart_joueur.mettre_a_jour_rotation()

                if touches[pygame.K_LEFT]:
                    self.kart_joueur.changer_direction("gauche")
                    self.kart_joueur.mettre_a_jour_rotation()

                if touches[pygame.K_UP]:
                    self.kart_joueur.changer_direction("haut")
                    self.kart_joueur.mettre_a_jour_rotation()

                if touches[pygame.K_DOWN]:
                    self.kart_joueur.changer_direction("bas")
                    self.kart_joueur.mettre_a_jour_rotation()


                self.kart_joueur.mettre_a_jour_direction()
                self.kart_joueur.deplacer()


                if self.kart_joueur.est_hors_ecran():
                    print("Le kart du joueur est hors de l'écran !")
                    print("Coordonnées de la portion de circuit :", self.circuit.coordonnees_portion_actuelle)

                    # Charger la prochaine portion de circuit selon la direction du kart du joueur
                    # A ajouter : gestion des transitions (virages vers la droite, la gauche, etc. selon la direction)
                    
                    if self.kart_joueur.direction_suivante == "haut":
                        if self.circuit.est_tout_droit(self.circuit.coordonnees_portion_actuelle, self.kart_joueur.direction_suivante):
                            self.circuit.mettre_a_jour_coords_portion_actuelle(self.kart_joueur.direction_suivante)
                            portion_suivante = PortionCircuit(self.fenetre, "assets/images/route.png", 0, 1280, 720, len(self.circuit.portions) + 1)
                            self.circuit.ajouter_portion(portion_suivante)
                            self.circuit.mettre_a_jour_portion_actuelle(portion_suivante)

                    elif self.kart_joueur.direction_suivante == "bas":
                        if self.circuit.est_tout_droit(self.circuit.coordonnees_portion_actuelle, self.kart_joueur.direction_suivante):
                            self.circuit.mettre_a_jour_coords_portion_actuelle(self.kart_joueur.direction_suivante)
                            portion_suivante = PortionCircuit(self.fenetre, "assets/images/route.png", 0, 1280, 720, len(self.circuit.portions) + 1)
                            self.circuit.ajouter_portion(portion_suivante)
                            self.circuit.mettre_a_jour_portion_actuelle(portion_suivante)

                    elif self.kart_joueur.direction_suivante == "gauche":
                        if self.circuit.est_tout_droit(self.circuit.coordonnees_portion_actuelle, self.kart_joueur.direction_suivante):
                            self.circuit.mettre_a_jour_coords_portion_actuelle(self.kart_joueur.direction_suivante)
                            portion_suivante = PortionCircuit(self.fenetre, "assets/images/route.png", 90, 1280, 720, len(self.circuit.portions) + 1)
                            self.circuit.ajouter_portion(portion_suivante)
                            self.circuit.mettre_a_jour_portion_actuelle(portion_suivante)

                    elif self.kart_joueur.direction_suivante == "droite":
                        if self.circuit.est_tout_droit(self.circuit.coordonnees_portion_actuelle, self.kart_joueur.direction_suivante):
                            self.circuit.mettre_a_jour_coords_portion_actuelle(self.kart_joueur.direction_suivante)
                            portion_suivante = PortionCircuit(self.fenetre, "assets/images/route.png", 90, 1280, 720, len(self.circuit.portions) + 1)
                            self.circuit.ajouter_portion(portion_suivante)
                            self.circuit.mettre_a_jour_portion_actuelle(portion_suivante)                

                if self.kart_joueur.est_hors_circuit(1280, 720):
                    print("Le kart du joueur est hors du circuit !")                
                    
                self.kart_joueur.afficher() 


                #print("Coordonnées de la ligne d'arrivée :", self.circuit.coordonnees_ligne_arrivee(1))

                

                    

                # Mettre à jour l'affichage
                pygame.display.flip()      
