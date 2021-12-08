# --- Imports
import pygame
import json
from typing import List, Union
from collections import defaultdict
from constants import *
from classes import *
from pygame import font

from pygame import constants


# --- Game Setup
with open("square game 2\\rooms.json") as f:
    rooms = json.load(f)

walls: List[List[Wall]] = []
enemy_positions: List[List[Tuple[int, int]]] = []
enemy_shoot_dirs: List[List[Tuple[int, int]]] = []
spawns: List[Tuple[int, int]] = []
exits: List[Tuple[int, int]] = []
shoot_seps: List[Union[float, int]] = []
for room in rooms:
    room_walls = []
    for wall_raw in room["walls"]:
        room_walls.append(Wall(*wall_raw))
    walls.append(room_walls[:])

    enemy_positions.append(list(map(tuple, room["enemies"])))
    enemy_shoot_dirs.append(list(map(tuple, room["shoot dirs"])))
    spawns.append(tuple(room["spawn"]))
    exits.append(tuple(room["exit"]))
    shoot_seps.append(room["shoot sep"])

current_room = 0
player = Player(spawns[current_room])
projectiles: List[Projectile] = []

# --- Pygame Setup
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()

pygame.font.init()
font20 = pygame.font.SysFont("JetBrains Mono", 20)
font30 = pygame.font.SysFont("JetBrains Mono", 30)
font150 = pygame.font.SysFont("JetBrains Mono", 150)
win_text = font150.render("You Win!", True, "white")
lose_text = font150.render("You Lose!", True, "white")
controls_text = font20.render("Controls: WASD (shift to sprint)", True, "white")
note_text = font20.render("Note: Collisions cancel all movement (I cba to fix it)", True, "white")

# --- Other Variables
run = True
new_room = False
win = False
lose = False
key_states = defaultdict(lambda: False)
run_time = 0

# --- Main Loop
while run:
    # -- Event Checking
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            run = False
        elif ev.type == pygame.KEYDOWN:
            key_states[ev.key] = True
        elif ev.type == pygame.KEYUP:
            key_states[ev.key] = False

    # -- Sort Past Round
    if new_room:
        new_room = False
        player.rect.x, player.rect.y = spawns[current_room]
        projectiles = []
    
    if not player.alive:
        lose = True

    # -- Main Game Code
    if not lose and not win:
        # Sort Keys/Movements
        pos = (player.rect.x, player.rect.y)
        shift = key_states[pygame.K_LSHIFT]
        for k in key_states:
            if k in MOVEMENTS and key_states[k]:
                if shift:
                    player.move(map(lambda x: x*2, MOVEMENTS[k]))
                else:
                    player.move(MOVEMENTS[k])

        # Move Projectiles
        for p in projectiles:
            p.move()

        # Shoot New Projectiles
        if not round(run_time, 5) % shoot_seps[current_room]:
            for e, d in zip(enemy_positions[current_room], enemy_shoot_dirs[current_room]):
                projectiles.append(
                    Projectile(e, d)
                )

        # Check Collisions With Walls & Enemies
        for w in walls[current_room]:
            if player.collides_with(w):
                player.rect.x, player.rect.y = pos
                break

        for e in enemy_positions[current_room]:
            if player.collides_with(*e, 10, 10):
                player.rect.x, player.rect.y = pos
                break
        
        # Check Collisions With Projectiles & (Projectiles and Walls)
        for i, p in enumerate(projectiles):
            if player.collides_with(p.rect.x, p.rect.y, 5, 5):
                player.hurt()
                del projectiles[i]
            for w in walls[current_room]:
                if p.collides_with(w):
                    del projectiles[i]
                    break

        # Check If Hit Exit
        if player.collides_with(*exits[current_room], 10, 40):
            current_room += 1
            if current_room > len(walls) - 1:
                win = True
                end_time = run_time
            else:
                new_room = True

    screen.fill("black")

    if win:
        # Draw Win Text
        score_text = font30.render(f"Time: {end_time}", True, "white")
        text_pos = (
            500 - (win_text.get_width() // 2),
            300 - (win_text.get_height() // 2)
        )
        screen.blit(win_text, text_pos)
        screen.blit(score_text, (text_pos[0], text_pos[1] + win_text.get_height() + 10))
    elif lose:
        # Draw Lose Text
        text_pos = (
            500 - (win_text.get_width() // 2),
            300 - (win_text.get_height() // 2)
        )
        screen.blit(lose_text, text_pos)
    else:
        # Draw All Entities
        pygame.draw.rect(screen, player.colour, player.rect)
        pygame.draw.rect(
                screen,
                "green",
                pygame.rect.Rect(*exits[current_room], 10, 40)
            )
        for e in enemy_positions[current_room]:
            pygame.draw.rect(
                screen,
                (227, 157, 18),
                pygame.rect.Rect(*e, 10, 10)
            )
        for w in walls[current_room]:
            pygame.draw.rect(screen, "white", w.rect)
        for p in projectiles:
            pygame.draw.rect(screen, "red", p.rect)

        # Draw Text
        stats_text_1 = font30.render(f"Time: {round(run_time)}", True, "white")
        stats_text_2 = font30.render(f"Lives: {player.lives}", True, "white")
        stats_text_3 = font30.render(f"Room: {current_room}", True, "white")
        screen.blit(stats_text_1, (20, 20))
        screen.blit(stats_text_2, (20, 20 + stats_text_1.get_height()))
        screen.blit(stats_text_3, (20, 20 + stats_text_1.get_height() + stats_text_2.get_height()))
        screen.blit(controls_text, (980 - controls_text.get_width(), 20))
        screen.blit(note_text, (980 - note_text.get_width(), 20 + controls_text.get_height()))

    # -- Update Display & Clock
    pygame.display.update()
    run_time += 1 / FPS
    clock.tick(FPS)
