import os

import pygame, json
from game_objects import Player, Food, Wall
base_dir = os.path.dirname(os.path.abspath(__file__))  # Get script's directory
file_path = os.path.join(base_dir, 'color.json')
with open(file_path) as f:
    color = json.loads(f.read())

pygame.init()

h = w = 400
win = pygame.display.set_mode((w, h))
pygame.display.set_caption('Snake')

def add_transparent_text(main_surface, text, size, x, y):
    font = pygame.font.SysFont('comicsansms', size)
    text = font.render(text, True, color['text'])
    surface = pygame.Surface((w,h))
    surface.fill(color['bg_color'])
    surface.blit(text, (0,0))
    surface.set_alpha(150)
    main_surface.blit(surface, (x, y))
def fill_background(surface, level, balance, n_to_next_lvl):
    surface.fill(color['bg_color'])
    # Draw our level in right bottom corner:
    add_transparent_text(surface, f'LVL: {level}', 35, 0, 0)
    # Draw balance:
    add_transparent_text(surface, f'Need: {balance}/{n_to_next_lvl}', 35, 200, 0)
    # Draw grid:
    for i in range(0, w, 20):
        pygame.draw.line(surface, color['black'], (0, max(i-1, 0)), (w, max(i-1, 0)), 2)
        pygame.draw.line(surface, color['black'], (max(i-1, 0), 0), (max(i-1, 0), h), 2)
fill_background(win, 1, 0, 5)

LEVEL = 1
wall = Wall(level = LEVEL)
player = Player(wall.points)
food = Food(player.points + wall.points)
speed = 5 #5 frames for second
BALANCE = 0 # number of apples eaten
N_to_next_lvl = 5 # apples neede to next level
clock = pygame.time.Clock()
run = True
losed = None # when snake will bump to wall/its body, losed = 'bumping direction'
while run:
    k_down_events = []
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            k_down_events.append(event)
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER and losed!=None:
                # Return initial characteristics
                wall = Wall(level = LEVEL)
                player = Player(wall.points)
                food = Food(player.points+wall.points)
                BALANCE = 0 
                losed = None
    if losed == None:
        player.process_input(k_down_events)
        fill_background(win, LEVEL, BALANCE, N_to_next_lvl)
        bumped_to_wall = wall.can_go(player.points[0], player.dx, player.dy) #if bumbed, then return direction of bumping, otherwise 'None'
        if bumped_to_wall:
            losed = bumped_to_wall
        if losed == None:
            losed = player.move(w, h)
        eat_food = food.can_eat(player.points[0]) 
        if eat_food: # if we eat apple, then apple change its position, and out balance+1
            player.add(player.points[0])
            BALANCE += 1
            if BALANCE == N_to_next_lvl:
                LEVEL += 1
                wall = Wall(LEVEL)
                player = Player(wall.points)
                if LEVEL <= 3: speed += 2
                else: 
                    speed += 8
                    N_to_next_lvl = 999
                BALANCE = 0
            food.change_pos(food.points + player.points + wall.points)
        # draw game objects:
        player.draw(win)
        food.draw(win)
        wall.draw(win)
    else: # if we lose game, draw how we lose(direction of bump)
        start = [player.points[0].x, player.points[0].y]
        end = list(start)
        if losed == 'down_collide':
            end[0] += 20
            end[1] += 18
            start[1] += 18
        elif losed == 'up_collide':
            end[0] += 20
        elif losed == 'left_collide':
            end[1] += 20
        elif losed == 'right_collide':
            start[0] += 18
            end[0] += 18
            end[1] += 20
        pygame.draw.line(win, color['red'], start, end, 2)

        #draw text: 'YOU LOSED'
        font = pygame.font.SysFont('comicsansms', 80)
        text = font.render('You Lose', True, color['red'])
        win.blit(text, (30, 120))

    pygame.display.update()
    clock.tick(speed)

pygame.quit()
print(losed)