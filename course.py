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

        self.circuit = Circuit(self.fenetre, numero_circuit)
        print(self.circuit.donnees)
        print(self.circuit.tourne_a_droite((0, 3)))
        print(self.circuit.est_tout_droit((0, 4), "bas"))
        self.adversaires = []
        self.cloche = pygame.time.Clock()
        self.intervalle_timer_depart = 1000 # Intervalle de mise à jour du timer de départ
        self.textes_timer_depart = ["3", "2", "1", "Partez !"] # Textes affichés lors du timer de départ
        self.police_timer_depart = pygame.font.Font(None, 36)
        self.polices_scores = [] # Liste des polices de scores




        # Générer 11 adversaires avec un décalage entre les karts ainsi qu'un joueur
        x_coureur = 574
        y_coureur = 359
        for i in range(n_participants):
            if i < n_participants - 1:
                accelerations = [0.25, 0.35, 0.50, 0.75]
                vitesse_kart = float(random.randint(2, 6))
                acceleration_kart = random.choice(accelerations)
                print(f"Vitesse du kart adverse : {vitesse_kart}, accélération du kart adverse : {acceleration_kart}")
                kart_adversaire = Kart(self.fenetre, choisir_image_kart(1, 6), x_coureur, y_coureur, vitesse_kart, acceleration_kart, "haut")
                adversaire = Adversaire(self.fenetre, kart_adversaire, i+1, self.circuit.portion_depart)
                self.adversaires.append(adversaire)
                x_coureur += 30
                y_coureur += 10
                adversaire.kart.moteur_allume = True
                police_score_adv = pygame.font.Font(None, 36)
                self.polices_scores.append(police_score_adv)

            else:
                self.kart_joueur = Kart(self.fenetre, choisir_image_kart(1, 6), x_coureur, y_coureur, 6.0, 0.25, "haut") # Kart du joueur
                self.joueur = Joueur(self.fenetre, self.kart_joueur, self.circuit.portion_depart, position_joueur, nom_joueur) # Joueur
                police_score_joueur = pygame.font.Font(None, 36)
                self.polices_scores.append(police_score_joueur)


        self.circuit.portion_actuelle.adversaires = self.adversaires.copy()
        self.positions_scores = positions_scores

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
                
                portions_autour = self.circuit.portions_autour(self.circuit.portion_actuelle.numero)
                if len(portions_autour)> 0:
                    print(f"Portion actuelle : {self.circuit.portion_actuelle.numero}, portions autour :{list(portion.numero for portion in portions_autour)}")
                #print("Portions autour :", self.circuit.portions_autour(self.circuit.portion_actuelle.numero))
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

                            for adversaire in self.adversaires:
                                if adversaire.kart.moteur_allume:
                                    adversaire.kart.accelerer()    

                        if evenement.type == deceleration:
                            if not self.kart_joueur.moteur_allume:
                                self.kart_joueur.decelerer()

                        """"if evenement.type == increment_position_joueur:
                            self.joueur.incrementer_position(-1)""" 

                        if evenement.type == depasse:
                            for adversaire, adversaire2 in zip(self.adversaires, self.adversaires[::-1]):
                                if adversaire.est_actif and adversaire.portion == self.joueur.portion_circuit:
                                    if self.joueur.depasse(adversaire.kart, self.circuit.portion_actuelle.direction):
                                        #print("Le joueur dépasse le kart de", adversaire.nom)
                                        self.joueur.incrementer_position(-1)
                                        adversaire.incrementer_position(1)
                                        depasse_1.play()

                                    elif adversaire.depasse(self.kart_joueur, self.circuit.portion_actuelle.direction):
                                        self.joueur.incrementer_position(1)
                                        adversaire.incrementer_position(-1)
                                        depasse_2.play()

                                    if adversaire2.est_actif and adversaire2.portion == adversaire.portion:
                                        if adversaire.depasse(adversaire2.kart):
                                            adversaire2.incrementer_position(1)
                                            adversaire.incrementer_position(-1)

        

                                if adversaire2.est_actif and adversaire2.portion == adversaire.portion or adversaire2.portion == self.circuit.portion_actuelle:
                                    if self.joueur.depasse(adversaire2.kart, self.circuit.portion_actuelle.direction):
                                        #print("Le joueur dépasse le kart de", adversaire2.nom)
                                        self.joueur.incrementer_position(-1)
                                        adversaire2.incrementer_position(1)
                                        depasse_1.play()

                                    elif adversaire2.depasse(self.kart_joueur, self.circuit.portion_actuelle.direction):
                                        self.joueur.incrementer_position(1)
                                        adversaire2.incrementer_position(-1)
                                        depasse_2.play()

                                    if adversaire.est_actif and adversaire.portion == adversaire2.portion:
                                        if adversaire2.depasse(adversaire.kart):
                                            adversaire.incrementer_position(1)
                                            adversaire2.incrementer_position(-1)    

                        if evenement.type == passage_ligne:
                            if self.circuit.portion_actuelle.est_ligne_arrivee_passee(self.kart_joueur):
                                print("La ligne d'arrivée a été passée !")
                                # Fin de la course si le joueur a terminé le troisième tour
                                if self.joueur.tour == 3:
                                    print("Le joueur a terminé la course !")
                                    self.fin_course()
                                    pygame.display.flip()
                                    pygame.time.wait(10000)
                                    return
                                
                                # Si le joueur a visité toutes les portions de circuit pendant le tour
                                elif len(self.joueur.portions_visitees) == self.circuit.nombre_portions():
                                    print("Passage au tour suivant.")
                                    self.joueur.tour += 1 # Incrémenter de 1 le nombre de tours effectués par le joueur
                                    self.joueur.portions_visitees = [] # Réinitialise la liste des portions visitées

                                else:
                                    print("Toutes les portions n'ont pas été visitées, tour actuel maintenu.")

                            for adversaire in self.adversaires:
                                if self.circuit.portion_actuelle.est_ligne_arrivee_passee(adversaire.kart):
                                    # Si un adversaire a terminé la course, le détruire
                                    if adversaire.tour == 3:
                                        print(f"{adversaire.nom} a terminé la course !")
                                        self.adversaires.remove(adversaire)
                                        del adversaire

                                    # Si l'adversaire a visité toutes les portions de circuit pendant le tour
                                    elif len(adversaire.portions_visitees) >= self.circuit.nombre_portions():
                                        print(f"Passage de {adversaire.nom} au tour suivant.")
                                        adversaire.tour += 1
                                        adversaire.portions_visitees = []

                                    else:
                                        print(f"Toutes les portions n'ont pas été visitées par {adversaire.nom}, tour actuel maintenu.")        



                                    
        

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


                    # Si au moins un kart adverse est sorti de l'écran
                    for adversaire in self.adversaires:
                        if adversaire.kart.est_hors_ecran():
                            print(f"Longueur de self.adversaires : {len(self.adversaires)}")
                            print(f"{len(list([adversaire] for adversaire in self.adversaires if adversaire.est_actif))} adversaires sont actifs.")
                            # Charger la portion de circuit suivante, mais sans mettre à jour l'actuelle immédiatement
                            if adversaire.portion.numero >= self.circuit.portion_actuelle.numero:
                                self.circuit.charger_prochaine_portion(update=False, adversaires=[adversaire])
                                adversaire.est_actif = False
                                adversaire.portions_visitees.append(self.circuit.portion_actuelle)

                            else:
                                adversaire.portion = self.circuit.portions_numeros.get(self.circuit.portion_actuelle.numero - 1, self.circuit.portion_actuelle)
                                adversaire.est_actif = False
                                adversaire.portions_visitees.append(adversaire.portion)    

                            if adversaire.kart.direction == "haut":
                                adversaire.kart.changer_position((adversaire.kart.rect.x, 716))

                            if adversaire.kart.direction == "bas":
                                adversaire.kart.changer_position((adversaire.kart.rect.x, 0))

                            if adversaire.kart.direction == "gauche":
                                adversaire.kart.changer_position((1279, adversaire.kart.rect.y))

                            if adversaire.kart.direction == "droite":
                                adversaire.kart.changer_position((0, adversaire.kart.rect.y))

                        else:
                            adversaire.est_actif = True
                            if self.circuit.portion_actuelle.direction == "haut":
                                if adversaire.kart.direction != "haut":
                                    adversaire.kart.changer_direction("haut")
                                    


                            elif self.circuit.portion_actuelle.direction == "bas":
                                if adversaire.kart.direction != "bas":
                                    adversaire.kart.changer_direction("bas")


                            elif self.circuit.portion_actuelle.direction == "gauche":
                                if adversaire.kart.direction != "gauche":
                                    adversaire.kart.changer_direction("gauche")

                            elif self.circuit.portion_actuelle.direction == "droite":
                                if adversaire.kart.direction != "droite":
                                    adversaire.kart.changer_direction("droite")

                            adversaire.kart.mettre_a_jour_rotation()


                    if self.kart_joueur.est_hors_ecran():
                        print(self.circuit.portions_numeros)
                        print("Le kart du joueur est hors de l'écran !")
                        print("Coordonnées de la portion de circuit :", self.circuit.coordonnees_portion_actuelle)

                        # Charger la prochaine portion de circuit selon la direction du kart du joueur
                        # A ajouter : gestion des transitions (virages vers la droite, la gauche, etc. selon la direction)


                        # Replacer le kart du joueur
                        if self.kart_joueur.direction == "haut":
                            self.kart_joueur.changer_position((self.kart_joueur.rect.x, 716))

                        if self.kart_joueur.direction == "bas":
                            self.kart_joueur.changer_position((self.kart_joueur.rect.x, 0))

                        if self.kart_joueur.direction == "gauche":
                            self.kart_joueur.changer_position((1279, self.kart_joueur.rect.y))

                        if self.kart_joueur.direction == "droite":
                            self.kart_joueur.changer_position((0, self.kart_joueur.rect.y))            

                        self.circuit.charger_prochaine_portion(update=True)
                        self.joueur.portion_circuit = self.circuit.portion_actuelle
                        print("N° de la portion de circuit du joueur :",self.joueur.portion_circuit.numero)
                        print("N° de la portion actuelle :", self.circuit.portion_actuelle.numero)
                        if len(self.joueur.portions_visitees) < self.circuit.nombre_portions():
                            self.joueur.portions_visitees.append(self.circuit.portion_actuelle)


                        """for adversaire in self.circuit.portion_actuelle.adversaires:
                            adversaire.est_actif = True"""
                        
                        """"if self.kart_joueur.direction_suivante == "haut":
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
                                self.circuit.mettre_a_jour_portion_actuelle(portion_suivante)"""                

                    if self.kart_joueur.est_hors_circuit(1280, 720):
                        print("Le kart du joueur est hors du circuit !")                
                    
                
                self.joueur.afficher()

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
