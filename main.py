import pygame
import random

# Initialisation de Pygame
pygame.init()

LARGEUR, HAUTEUR = 800, 600
ECRAN = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Jeu du Cube")

# Couleurs
NOIR = (0, 0, 0)
ROUGE = (255, 0, 0)
BLEU = (0, 0, 255)
BLANC = (255, 255, 255)

# Cube
cube_taille = 50
position_initiale = (LARGEUR // 2 - cube_taille // 2, HAUTEUR // 2 - cube_taille // 2)
cube_x, cube_y = position_initiale
animation_distance = 100  # Distance totale de l'animation du cube
animation_step = 2  # Incrément pour chaque étape de l'animation

# Bordures
bordures = ['haut', 'bas', 'gauche', 'droite']
bordure_cible = random.choice(bordures)
derniere_bordure = None

# Score
score = 0
font = pygame.font.Font(None, 36)

# Animation
en_animation = False
direction_animation = None
distance_parcourue = 0
retour_animation = False

# Fonction pour choisir une nouvelle bordure cible
def choisir_nouvelle_bordure():
    global derniere_bordure, bordure_cible
    choix = bordures[:]
    if derniere_bordure in choix:
        choix.remove(derniere_bordure)
    bordure_cible = random.choice(choix)
    derniere_bordure = bordure_cible

# Fonction pour redémarrer le jeu
def redemarrer():
    global cube_x, cube_y, score, en_animation, direction_animation, distance_parcourue, retour_animation
    cube_x, cube_y = position_initiale
    score = 0
    en_animation = False
    direction_animation = None
    distance_parcourue = 0
    retour_animation = False
    choisir_nouvelle_bordure()

# Boucle de jeu
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and not en_animation:
            if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                direction_animation = {
                    pygame.K_UP: 'haut',
                    pygame.K_DOWN: 'bas',
                    pygame.K_LEFT: 'gauche',
                    pygame.K_RIGHT: 'droite'
                }[event.key]
                en_animation = True
                distance_parcourue = 0
                retour_animation = False

    # Gérer l'animation
    if en_animation:
        if direction_animation == 'haut':
            cube_y -= animation_step if not retour_animation else animation_step / 2
        elif direction_animation == 'bas':
            cube_y += animation_step if not retour_animation else animation_step / 2
        elif direction_animation == 'gauche':
            cube_x -= animation_step if not retour_animation else animation_step / 2
        elif direction_animation == 'droite':
            cube_x += animation_step if not retour_animation else animation_step / 2

        distance_parcourue += animation_step

        # Gérer le retour du cube à sa position initiale
        if distance_parcourue >= animation_distance:
            if not retour_animation:
                retour_animation = True
                distance_parcourue = 0
            else:
                # Vérifier si la direction est correcte
                if direction_animation == bordure_cible:
                    score += 1
                    choisir_nouvelle_bordure()
                else:
                    print(f"Perdu! Score final : {score}")
                    redemarrer()  # Redémarrer le jeu

                # Réinitialiser pour la prochaine animation
                en_animation = False
                direction_animation = None

        # Réinitialiser la position du cube après le retour
        if retour_animation and distance_parcourue >= animation_distance / 2:
            cube_x, cube_y = position_initiale

    # Dessiner le cube, la bordure cible et le score
    ECRAN.fill(NOIR)
    pygame.draw.rect(ECRAN, BLEU, (cube_x, cube_y, cube_taille, cube_taille))

    # Changer la couleur de la bordure cible
    bordure_rects = {
        'haut': pygame.Rect(0, 0, LARGEUR, 10),
        'bas': pygame.Rect(0, HAUTEUR - 10, LARGEUR, 10),
        'gauche': pygame.Rect(0, 0, 10, HAUTEUR),
        'droite': pygame.Rect(LARGEUR - 10, 0, 10, HAUTEUR)
    }
    pygame.draw.rect(ECRAN, ROUGE, bordure_rects[bordure_cible])

    # Afficher le score
    score_text = font.render(f"Score: {score}", True, BLANC)
    ECRAN.blit(score_text, (10, 10))

    pygame.display.update()

pygame.quit()
