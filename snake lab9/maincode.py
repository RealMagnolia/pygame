import os

import pygame, json
from game_objects import Player, Food, Wall

base_dir = os.path.dirname(os.path.abspath(__file__))
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
    # make a surface for saving text -> make it transparent -> blit it to main_surface(for getting the result of transparrent text)
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
    add_transparent_text(surface, f'Need: {balance}/{n_to_next_lvl}', 35, 150, 0)
    # Draw grid:
    for i in range(0, w, 20):
        pygame.draw.line(surface, color['black'], (0, max(i-1, 0)), (w, max(i-1, 0)), 2)
        pygame.draw.line(surface, color['black'], (max(i-1, 0), 0), (max(i-1, 0), h), 2)
fill_background(win, 1, 0, 5)

LEVEL = 1
# 1-easy, 2-normal, 3-hard, 4-god level/infinity game
wall = Wall(level = LEVEL)
player = Player(wall.points)
food = Food(player.points + wall.points)
speed = 5 #5 frames for second
BALANCE = 0 # number of apples eaten
N_to_next_lvl = 50 # apples neede to next level
add_speed_effect = timer_adding_speed = 0 # additional +speed effect for a short period of time
def null_effect_additional_speed():
    global add_speed_effect, timer_adding_speed, speed
    speed -= add_speed_effect
    add_speed_effect = timer_adding_speed = 0
clock = pygame.time.Clock()
run = True
losed = None # when snake will bump to wall/its body it'll change to 'bumping direction'
while run:
    k_down_events = []
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            k_down_events.append(event) # save each keydown event, after i'll determine snake's DIRECTION for moving 
            # RESTART game, press ENTER or RETURN buttons:
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER and losed!=None: 
                # Null balance, start with current level
                wall = Wall(level = LEVEL)
                player = Player(wall.points)
                food = Food(player.points+wall.points)
                BALANCE = 0 
                null_effect_additional_speed()
                losed = None
    if losed == None:
        # Game process:
        player.process_input(k_down_events) # check for direction
        fill_background(win, LEVEL, BALANCE, N_to_next_lvl)
        bumped_to_wall = wall.can_go(player.points[0], player.dx, player.dy) #if bumbed, then return direction of bumping, otherwise 'None'
        if bumped_to_wall:
            losed = bumped_to_wall
        if losed == None:
            losed = player.move(w, h)
        
        eat_food = food.can_eat(player.points[0], player.points + wall.points) 
        if eat_food[0]: # if we eat apple, then our balance+1
            player.add(player.points[0])
            BALANCE += eat_food[1]
            if BALANCE >= N_to_next_lvl:
                LEVEL += 1
                wall = Wall(LEVEL)
                player = Player(wall.points)
                null_effect_additional_speed()
                if LEVEL <= 3: speed += 1
                else: # if level==4 make a infinite game(99999)
                    speed += 8
                    N_to_next_lvl = 99999
                BALANCE = 0
            elif eat_food[2] != 0:
                null_effect_additional_speed()
                add_speed_effect = eat_food[2]
                timer_adding_speed = add_speed_effect * 10
                speed += eat_food[2]
        # draw game objects:
        player.draw(win)
        food.draw(win)
        wall.draw(win)
        if player.dx!=0 or player.dy!=0:
            food.change_timer(player.points + wall.points)
            if timer_adding_speed > 0:
                timer_adding_speed -= 1
                if timer_adding_speed == 0: 
                    null_effect_additional_speed()
    else: # if we lose the game, draw how we lose(direction of bump)
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

        #draw text: 'YOU LOSE'
        font = pygame.font.SysFont('comicsansms', 80)
        text = font.render('You Lose', True, color['red'])
        win.blit(text, (30, 120))

    pygame.display.update()
    clock.tick(speed)

pygame.quit()
print(losed)