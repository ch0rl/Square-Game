import pygame
import random
import json
from classes import *
from constants import *
from map_maker._input import Keyboard_Handler
from typing import List


print("[*] Provide inputs in form: `key` `value(s)`")
print("[*] Type `help` for help and `quit` to finish")

HELP = """
***
Inputs in form: key value(s)

Possible keys: `wall`, `enemy`, `spawn`, `exit`
Corresponding value(s) form(s):
    `wall`: x, y, width, height
    `enemy`: x, y, shoot-x, shoot-y
    `spawn`: x, y
    `exit`: x, y

All `x`s and `y`s are top-left, all values are integers
Example: wall 0 0 10 600
***
"""

kb = Keyboard_Handler()
kb.start_thread()
map_ = {
    "walls": [
        [0, 0, 1000, 10],
        [0, 590, 1000, 10],
        [0, 0, 10, 600],
        [990, 0, 10, 600]
        ],
    "enemies": [],
    "shoot dirs": [],
    "spawn": [],
    "exit": []
}

walls: List[Wall] = []
for w in [[0, 0, 1000, 10], [0, 590, 1000, 10], [0, 0, 10, 600], [990, 0, 10, 600]]: walls.append(Wall(*w))

enemy_positions: List[Tuple[int, int]] = []
enemy_shoot_dirs: List[Tuple[int, int]] = []
spawn: Tuple[int, int] = ()
exit_: Tuple[int, int] = ()
projectiles: List[Projectile] = []

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()

run = True
run_time = 0
while run:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            run = False
    
    if kb.newline:
        text = kb.access_text()
        if text == "help":
            print(HELP)
        elif text == "quit":
            run = False
        else:
            key, *values = text.split()
            values = list(map(int, values))
            if key == "wall":
                map_["walls"].append(values)
                walls.append(Wall(*values))
            elif key == "enemy":
                map_["enemies"].append([values[0], values[1]])
                map_["shoot dirs"].append([values[2], values[3]])
                enemy_positions.append((values[0], values[1]))
                enemy_shoot_dirs.append((values[2], values[3]))
            elif key == "spawn":
                map_["spawn"] = values
                spawn = tuple(values)
            elif key == "exit":
                map_["exit"] = values
                exit_ = tuple(values)

    # Move Projectiles
    for p in projectiles:
        p.move()

    # Shoot New Projectiles
    if not round(run_time, 5) % 1:
        for e, d in zip(enemy_positions, enemy_shoot_dirs):
            projectiles.append(
                Projectile(e, d)
            )

    # Check Collisions With Projectiles & (Projectiles and Walls)
    for i, p in enumerate(projectiles):
        for w in walls:
            if p.collides_with(w):
                del projectiles[i]
                break
    
    screen.fill("black")
    for w in walls:
        pygame.draw.rect(screen, "white", w.rect)
    for e in enemy_positions:
        pygame.draw.rect(
            screen,
            (227, 157, 18),
            pygame.rect.Rect(*e, 10, 10)
        )
    for p in projectiles:
        pygame.draw.rect(screen, "red", p.rect)

    if spawn:
        pygame.draw.rect(
            screen,
            (25, 93, 242),
            pygame.rect.Rect(*spawn, 10, 10)
        )
    
    if exit_:
        pygame.draw.rect(
            screen,
            "green",
            pygame.rect.Rect(*exit_, 10, 40)
        )

    pygame.display.update()
    run_time += 1 / FPS
    clock.tick(FPS)

else:
    kb.kill()
    pygame.quit()
    fname = f"map_maker_output{random.randint(1000, 9999)}.json"
    with open(fname, "w") as f:
        json.dump(map_, f, indent=4)
    print(f"Outputted to: {fname}")
