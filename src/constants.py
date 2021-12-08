import pygame

SCREEN_SIZE = (1000, 600)
FPS = 60
MOVEMENTS = {
    pygame.K_w: (0, -1),
    pygame.K_s: (0, 1),
    pygame.K_d: (1, 0),
    pygame.K_a: (-1, 0)
}