import pygame
from random import randint, choice

pygame.init()

# Dimensions de la fenêtre
WIDTH = 800
HEIGHT = 600

# Initialisation de la fenêtre
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pong')

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
PINK = (255, 192, 203)
CYAN = (0, 255, 255)
BROWN = (165, 42, 42)
GRAY = (128, 128, 128)

# Liste de couleurs pour la raquette
PADDLE_COLORS = [RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, PINK, CYAN, BROWN, GRAY, WHITE, BLACK]

# Police de caractères
font = pygame.font.SysFont('Arial', 36)
big_font = pygame.font.SysFont('Arial', 72)

# Définition de la raquette
paddle_width = 100
paddle_height = 20
paddle_x = (WIDTH - paddle_width) // 2
paddle_y = HEIGHT - 2 * paddle_height
paddle_speed = 10

# Définition de la balle
ball_radius = 10
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_speed_x = choice([-5, 5])
ball_speed_y = randint(-5, 5)

# Score
score = 0

# Liste des scores
high_scores = []

# Fonction pour afficher le score
def display_score():
    score_text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, (10, 10))

# Fonction pour afficher les 3 meilleurs scores
def display_top_scores():
    sorted_scores = sorted(high_scores, reverse=True)[:3]
    scores_text = font.render("Top Scores:", True, WHITE)
    screen.blit(scores_text, (WIDTH - 200, 10))
    for i, high_score in enumerate(sorted_scores):
        score_text = font.render(str(i+1) + ": " + str(high_score), True, WHITE)
        screen.blit(score_text, (WIDTH - 200, 50 + i * 30))

# Fonction pour afficher la raquette
def draw_paddle(color):
    pygame.draw.rect(screen, color, (paddle_x, paddle_y, paddle_width, paddle_height))

# Fonction pour afficher la balle
def draw_ball():
    pygame.draw.circle(screen, WHITE, (ball_x, ball_y), ball_radius)

# Fonction pour réinitialiser le jeu
def reset_game():
    global paddle_x, ball_x, ball_y, ball_speed_x, ball_speed_y, score
    paddle_x = (WIDTH - paddle_width) // 2
    ball_x = WIDTH // 2
    ball_y = HEIGHT // 2
    ball_speed_x = choice([-5, 5])
    ball_speed_y = randint(-5, 5)
    score = 0

# Boucle principale du jeu
running = True
clock = pygame.time.Clock()

while running:
    game_over = False
    reset_game()  # Réinitialise le jeu au début de chaque boucle

    # Minuteur de 3 secondes
    start_ticks = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_ticks < 3000:
        screen.fill(BLACK)
        timer_text = font.render("Starting in: " + str((3000 - (pygame.time.get_ticks() - start_ticks)) // 1000 + 1), True, WHITE)
        screen.blit(timer_text, (WIDTH // 2 - timer_text.get_width() // 2, HEIGHT // 2 - timer_text.get_height() // 2))
        pygame.display.flip()
        clock.tick(60)

    # Couleur initiale de la raquette
    paddle_color_index = 0

    while not game_over:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    game_over = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle_x > 0:
            paddle_x -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle_x < WIDTH - paddle_width:
            paddle_x += paddle_speed

        # Mouvement de la balle
        ball_x += ball_speed_x
        ball_y += ball_speed_y

        # Collision avec les bords de l'écran
        if ball_x <= 0 or ball_x >= WIDTH:
            ball_speed_x = -ball_speed_x
        if ball_y <= 0:
            ball_speed_y = -ball_speed_y

        # Collision avec la raquette
        if ball_y >= paddle_y - ball_radius and paddle_x <= ball_x <= paddle_x + paddle_width:
            ball_speed_y = -ball_speed_y
            score += 1

            # Changer la couleur de la raquette
            paddle_color_index = (paddle_color_index + 1) % len(PADDLE_COLORS)

        # Si la balle atteint le bas de l'écran, c'est la fin du jeu
        if ball_y >= HEIGHT:
            # Ajouter le score à la liste des scores
            high_scores.append(score)
            game_over = True

        # Affichage des éléments du jeu
        draw_paddle(PADDLE_COLORS[paddle_color_index])
        draw_ball()
        display_score()
        display_top_scores()

        pygame.display.flip()
        clock.tick(60)

    # Fin du jeu
    screen.fill(BLACK)

    game_over_text = big_font.render("Game Over", True, RED)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 4 - game_over_text.get_height() // 2))

    restart_text = font.render("Appuyer sur Entrer pour rejouer", True, WHITE)
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 - restart_text.get_height() // 2))

    quit_text = font.render("Appuyer sur Échap pour quitter le jeu", True, WHITE)
    screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + restart_text.get_height() + 10))

    pygame.display.flip()

    # Attend que le joueur appuie sur la barre d'espace pour relancer le jeu
    waiting_for_restart = True
    while waiting_for_restart:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting_for_restart = False
                elif event.key == pygame.K_ESCAPE:
                    running = False
                    waiting_for_restart = False

pygame.quit()
