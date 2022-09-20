import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Runner")

# Clock (controlling the frametime)
clock = pygame.time.Clock()

# Event Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # draw all our elements
    # update everything
    pygame.display.update()
    clock.tick(60) # Frametime