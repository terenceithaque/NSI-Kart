# Programme principal du jeu
import pygame
pygame.init()
from kart import *
from circuits import *
from joueur import *



# Créer la fenêtre de jeu
fenetre = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("NSI-Kart")



# Joueur et kart du joueur
kart_joueur = Kart(fenetre, choisir_image_kart(1, 6), 120, 600, 2.0, 0.25, "haut")
joueur = Joueur(fenetre, kart_joueur, 12)



acceleration = pygame.USEREVENT + 1
pygame.time.set_timer(acceleration, 500)


circuit = Circuit(fenetre, 1)
print(circuit.donnees)
print(circuit.tourne_a_droite((0, 3)))
print(circuit.est_tout_droit((0, 4), "bas"))


portion_depart = PortionCircuit(fenetre, "assets/images/route.png")

execution = True


# Boucle principale
while execution:

    #pygame.time.wait(1000)

    fenetre.fill((0, 0, 0))

    touches = pygame.key.get_pressed()


    print(kart_joueur.rect.x, kart_joueur.rect.y)

    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            execution = False

        if evenement.type == acceleration: 
            kart_joueur.accelerer()

        if evenement.type == pygame.MOUSEMOTION:
            print(pygame.mouse.get_pos())       

    if touches[pygame.K_RIGHT]:
        kart_joueur.changer_direction("droite")
        kart_joueur.mettre_a_jour_rotation()

    if touches[pygame.K_LEFT]:
        kart_joueur.changer_direction("gauche")
        kart_joueur.mettre_a_jour_rotation()

    if touches[pygame.K_UP]:
        kart_joueur.changer_direction("haut")
        kart_joueur.mettre_a_jour_rotation()

    if touches[pygame.K_DOWN]:
        kart_joueur.changer_direction("bas")
        kart_joueur.mettre_a_jour_rotation()


    kart_joueur.mettre_a_jour_direction()
    kart_joueur.deplacer()


    if kart_joueur.est_hors_ecran():
        print("Le kart du joueur est hors de l'écran !")

    if kart_joueur.est_hors_circuit(1280, 720):
        print("Le kart du joueur est hors du circuit !")                
    

    portion_depart.afficher()
    
    kart_joueur.afficher() 

           

    # Mettre à jour l'affichage
    pygame.display.flip()        