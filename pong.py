import pygame
from random import randint, random, choice

pygame.init()

WIDTH = 800  # Example width
HEIGHT = 600  # Example height
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('My Game')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 255)
GOLD = (255, 215, 0)  # Valeur RVB pour la couleur gold
ORANGE = (255, 165, 0)  # Valeur RVB pour la couleur orange
VIOLET = (148, 0, 211)  # Valeur RVB pour la couleur violet
CYAN = (0, 255, 255)  # Valeur RVB pour la couleur cyan
MARRON = (139, 69, 19)  # Valeur RVB pour la couleur marron
VERT = (0, 128, 0)  # Valeur RVB pour la couleur vert
POMME = (0, 255, 0)  # Valeur RVB pour la couleur pomme

screen.fill(BLACK)
pygame.display.update()

radius = 10
x = WIDTH // 2
y = radius+10

pygame.draw.circle(screen, WHITE, (x, y), radius)

paddle = {"width": 2000,
          "height": 20,
          "color": POMME,  # Utiliser la couleur pomme pour le paddle
          "x": (WIDTH - 100) // 2,  # Centrer le paddle horizontalement
          "y": HEIGHT - 40}  # Positionner le paddle près du bas

pygame.draw.rect(screen, paddle["color"], (paddle["x"], paddle["y"], paddle["width"], paddle["height"]))

speed = 5
x_sens = choice([-1, 1])
y_sens = choice([-1, 1])
pause = False

end = False
while not end:
    screen.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end = True

    key = pygame.key.get_pressed()

    if key[pygame.K_SPACE]:
        pause = not pause

    if key[pygame.K_RETURN]:
        pause = False

    if key[pygame.K_m]:
        auto = False

    if not pause:

        if key[pygame.K_LEFT]:
            paddle["x"] -= speed

        if key[pygame.K_RIGHT]:
            paddle["x"] += speed

        # Prevent paddle from going out of bounds
        paddle["x"] = max(0, min(paddle["x"], WIDTH - paddle["width"]))

        # Change x direction if the ball hits the left or right edge
        if x <= radius or x >= WIDTH - radius:
            while 1<(abs(int(y_sens * speed)))<6:
                x_sens = abs(x_sens*choice([-0.45,-1.45,-0.55,-0.65,-1.65,-0.75,-0.85,]))
            x_sens *=-1
            print("xsens=",x_sens,"x=",x)



        # Change y direction if the ball hits the top or bottom edge
        if y <= radius :
            while 1<(abs(int(x_sens * speed)))<6:
                y_sens = abs(y_sens*([-0.45,-1.45,-0.55,-0.65,-1.65,-0.75,-0.85,]))
            y_sens *=-1
            print("ysens=",y_sens,"y=",y)



        # If the ball hits the paddle top
        if y + radius >= paddle["y"]:
            # If the ball is between the x paddle begin and the x paddle end
            if paddle["x"] <= x <= paddle["x"] + paddle["width"]:
                # Change y direction
                y_sens *= -1

        # If the ball comes out of the screen from below, end the game
        if y >= HEIGHT - radius:
            end = True

        # Compute the new ball coordinates
        x += int(x_sens * speed)
        y += int(y_sens * speed)

    # Redraw ball and paddle
    pygame.draw.circle(screen, WHITE, (x, y), radius)
    pygame.draw.rect(screen, paddle["color"], (paddle["x"], paddle["y"], paddle["width"], paddle["height"]))

    # Update screen
    pygame.display.update()
    pygame.time.delay(10)

pygame.quit()