# Script d'une course
import pygame
pygame.init()
pygame.mixer.init()
from kart import *
from circuits import *
from joueur import *
from adversaires import *
import random


class Course:
    """Classe représentant une course indépendante."""
    def __init__(self, fenetre:pygame.Surface, n_participants:int=12, position_joueur=12, numero_circuit=1, nom_joueur:str="Vous", positions_scores:dict={}):
        """Initialise la course.
        - fenetre : fenêtre de jeu dans laquelle les éléments de la course sont affichés
        - n_participants : nombre de participants à la course (adversaires + joueur),
        - position_joueur : position de départ du joueur
        - numero_circuit : numéro du circuit de course
        - nom_joueur : chaîne de caractères, nom du joueur
        - positions_scores : dictionnaire contenant les scores attribués aux participants selon leur position à la fin de la course."""

        # Initialisation des attributs
        self.fenetre = fenetre
        assert 0 < position_joueur <= n_participants, f"La position de départ du joueur doit être comprise entre 1 et {n_participants}."
        assert len(positions_scores) == n_participants, f"Le dictionnaire de scores selon les positions doit avoir la même taille que le nombre de participants ({n_participants} participants contre une taille de {len(positions_scores)})."

        self.n_participants = n_participants

        
        self.adversaires = []
        self.cloche = pygame.time.Clock()
        self.intervalle_timer_depart = 1000 # Intervalle de mise à jour du timer de départ
        self.textes_timer_depart = ["3", "2", "1", "Partez !"] # Textes affichés lors du timer de départ
        self.police_timer_depart = pygame.font.Font(None, 36)
        self.polices_scores = [] # Liste des polices de scores




        self.dernier_temps = pygame.time.get_ticks()

    def afficher_timer_depart(self, n=0, x=700, y=500):
        """Affiche le timer de départ""" 
        texte = self.textes_timer_depart[n]
        affichage_timer = self.police_timer_depart.render(texte, False, (255, 255, 255))
        self.fenetre.blit(affichage_timer, (x, y))

    def mettre_a_jour_etat_adversaires(self) -> None:
        """Active uniquement les adversaires de la portion visible."""
        for adversaire in self.adversaires:
            adversaire.est_actif = bool(adversaire.portion.numero == self.circuit.portion_actuelle)    


    def fin_course(self) -> None:
        """Affiche les scores finaux et termine la course."""
        # Déterminer les scores
        for position in self.positions_scores:
            if self.joueur.position == position:
                self.joueur.score += self.positions_scores[position]

            else:
                for adversaire in self.adversaires:
                    if adversaire.position == position:
                        adversaire.score += self.positions_scores[position]

        # Afficher les scores
        x = 500
        y = 300
        for pos in range(1, self.n_participants + 1):
            if pos == self.joueur.position:
                police = self.polices_scores[pos - 1]
                affichage_score_joueur = police.render(f"{self.joueur.nom} : {self.joueur.score}", False, (255, 255, 255))
                self.fenetre.blit(affichage_score_joueur, (x, y))
                y += 20

            else:
                for adversaire in self.adversaires:
                    if pos == adversaire.position:
                        police = self.polices_scores[pos - 1]
                        affichage_score_adv = police.render(f"{adversaire.nom} : {adversaire.score}", False, (255, 255, 255))
                        self.fenetre.blit(affichage_score_adv, (x, y))
                        y += 20    

        

    def courir(self) -> None:
        """Démarre la course."""

        

        course_demarree = False
        acceleration = pygame.USEREVENT + 1
        deceleration = pygame.USEREVENT + 2
        #increment_position_joueur = pygame.USEREVENT + 3
        depasse = pygame.USEREVENT + 4
        passage_ligne = pygame.USEREVENT + 5

        pygame.time.set_timer(acceleration, 500)
        #pygame.time.set_timer(increment_position_joueur, 1000)
        pygame.time.set_timer(depasse, 500)
        pygame.time.set_timer(passage_ligne, 100)


        execution = True
        n_texte_timer = 0

        x_timer_depart = 500
        y_timer_depart = 500
        son_timer_depart = pygame.mixer.Sound("assets/audio/timer.mp3")
        depasse_1 = pygame.mixer.Sound("assets/audio/depasse_1.mp3") # Son joué quand le joueur dépasse un adversaire
        depasse_2 = pygame.mixer.Sound("assets/audio/depasse_2.mp3") # Son joué quand un adversaire dépasse le joueur
        musique = pygame.mixer.music.load("assets/audio/musique.mp3")
        pygame.mixer.music.play(-1)


        # Boucle principale
        while execution:
             
                #pygame.time.wait(1000)
                maintenant = pygame.time.get_ticks()
                if not course_demarree:
                    #son_timer_depart.stop()
                    if maintenant - self.dernier_temps >= self.intervalle_timer_depart:
                        self.afficher_timer_depart(n_texte_timer, x_timer_depart, y_timer_depart)
                        son_timer_depart.play()
                        y_timer_depart += 15
                        self.dernier_temps = pygame.time.get_ticks()
                        n_texte_timer += 1
                        if n_texte_timer == 4:
                            course_demarree = True

                elif course_demarree:

                    """for adversaire in self.adversaires:
                        if adversaire.est_actif:
                            if self.joueur.depasse(adversaire.kart):
                                print(f"Le joueur a dépassé le kart de {adversaire.nom}")"""


                    

                    """
                    if not self.kart_joueur.moteur_allume:
                        self.kart_joueur.decelerer()"""

                    self.fenetre.fill((255, 255, 255))



                    touches = pygame.key.get_pressed()


                    #print(self.kart_joueur.rect.x, self.kart_joueur.rect.y)

                    for evenement in pygame.event.get():
                        if evenement.type == pygame.QUIT:
                            pygame.quit()

                        if evenement.type == acceleration:
                            """if self.kart_joueur.moteur_allume: 
                                self.kart_joueur.accelerer()"""

                            for adversaire in self.adversaires:
                                if adversaire.kart.moteur_allume:
                                    adversaire.kart.accelerer()    

                        if evenement.type == deceleration:
                            """if not self.kart_joueur.moteur_allume:
                                self.kart_joueur.decelerer()"""

                        """"if evenement.type == increment_position_joueur:
                            self.joueur.incrementer_position(-1)""" 

                        if evenement.type == depasse:
                            pass

                        if evenement.type == passage_ligne:
                            pass

                                    
        

                        if evenement.type == pygame.KEYUP:
                            if evenement.key == pygame.K_SPACE:
                                """"self.kart_joueur.moteur_allume = not self.kart_joueur.moteur_allume
                                if self.kart_joueur.moteur_allume == False:
                                    pygame.time.set_timer(acceleration, 0)
                                    pygame.time.set_timer(deceleration, 1000)

                                else:
                                    pygame.time.set_timer(deceleration, 0)
                                    pygame.time.set_timer(acceleration, 500)"""


                        if evenement.type == pygame.MOUSEMOTION:
                            print(pygame.mouse.get_pos())


                    """if not self.kart_joueur.moteur_allume:
                        self.kart_joueur.decelerer()   """            

                    if touches[pygame.K_RIGHT]:
                        pass

                    if touches[pygame.K_LEFT]:
                        pass

                    if touches[pygame.K_UP]:
                        pass

                    if touches[pygame.K_DOWN]:
                        pass


                    """self.kart_joueur.mettre_a_jour_direction()
                    self.kart_joueur.deplacer()"""


                    # Si au moins un kart adverse est sorti de l'écran
                    for adversaire in self.adversaires:
                        if adversaire.kart.est_hors_ecran():
                           pass


                                   
                
                #self.circuit.portion_actuelle.mettre_a_jour_longueur_affichee(self.joueur.vitesse_haut)

                for adversaire in self.adversaires:
                    """if adversaire.portion != self.joueur.portion_circuit:
                        print(f"La portion de {adversaire.nom} n'est pas la même que celle du joueur.")"""
                        

                    adversaire.kart.deplacer()
                    adversaire.kart.mettre_a_jour_direction()
                    if adversaire.est_actif:
                        adversaire.afficher()

                #print("Coordonnées de la ligne d'arrivée :", self.circuit.coordonnees_ligne_arrivee(1))

                

                    

                # Mettre à jour l'affichage
                pygame.display.flip()      
