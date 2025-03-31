#Imports
import os

import pygame, sys
from pygame.locals import *
import random, time

#Initialzing 
pygame.init()

#Setting up FPS 
FPS = 120
FramePerSec = pygame.time.Clock()

#Creating colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#Other Variables for use in the program
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 6
SPEED_COIN = 4
# Increase the speed of Enemy when the player earns N coins
N = 50

SCORE = 0
SCORE_COIN = 0

#Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)
base_dir = os.path.dirname(os.path.abspath(__file__))  # Get script's directory
file_path = os.path.join(base_dir,"images" ,'AnimatedStreet.png')
background = pygame.image.load(file_path)

#Create a white screen 
DISPLAYSURF = pygame.display.set_mode((400,600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")


enemy_images = [pygame.image.load(os.path.join(base_dir, "images", f"enemy{i}.png")) for i in range(1, 4)]

class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemies = None):
        super().__init__() 
        self.image = enemy_images[random.randint(0, 2)]
        self.rect = self.image.get_rect()
        self.get_pos(enemies)

    def move(self):
        global SCORE
        self.rect.move_ip(0,SPEED)
        if (self.rect.top > 600): # if enemy leaves the window, he'll die
            SCORE += 1
            self.kill()

    def get_pos(self, enemies=None): # get random position
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0) 
        if enemies == None: return
        while pygame.sprite.spritecollideany(self, enemies): # not intersect with other enemies
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class Coin(pygame.sprite.Sprite):
    def __init__(self, coins = None):
        super().__init__()
        self.get_new_coin()

    def get_new_coin(self, coins = None):
        self.weight = random.randint(2, 6)
        self.size = 50 - (6 - self.weight) * 4 # set size by its cost
        file_path = os.path.join(base_dir, "images", 'coin.png')
        image = pygame.image.load(file_path)
        self.image = pygame.transform.scale(image, (self.size, self.size)).convert_alpha()
        self.rect = image.get_rect()
        self.Weight = font_small.render(str(self.weight), True, BLACK) # cost as text
        self.get_pos(coins)
    def draw(self, win):
        win.blit(self.image, self.rect)
        win.blit(self.Weight, (self.rect.x + self.size//2 - 6, self.rect.y + self.size//2 - 13))
    def move(self, coins = None):
        global SCORE_COIN
        self.rect.move_ip(0,SPEED_COIN)
        if (self.rect.top > 600):
            # self.get_new_coin(coins)
            self.kill()

    def get_pos(self, coins=None):
        self.rect.center = (random.randint(self.size, SCREEN_WIDTH-self.size), 0) 
        if coins == None: return
        while pygame.sprite.spritecollideany(self, coins):
            self.rect.center = (random.randint(self.size, SCREEN_WIDTH-self.size), 0)
    

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        file_path = os.path.join(base_dir, "images", 'player.png')
        self.image = pygame.image.load(file_path)
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
       
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(5, 0)
                  
#Setting up Sprites        
P1 = Player()
E1 = Enemy()
C1 = Coin()

#Creating Sprites Groups
enemies = pygame.sprite.Group()
enemies.add(E1)
coins = pygame.sprite.Group()
coins.add(C1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)

#Adding a new User event 
enemy_spawn_interval = 700 #700 ticks
last = 0
coin_spawn_interval = pygame.USEREVENT + 2
pygame.time.set_timer(coin_spawn_interval, 600)

losed = False
#Game Loop
while True:
    #Cycles through all events occurring  
    for event in pygame.event.get():
        if event.type == coin_spawn_interval and not losed:
            C_new = Coin(coins)
            coins.add(C_new)
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and losed:
                print("RESTART")
                SPEED, N, SCORE, SCORE_COIN, enemy_spawn_interval = 6, 50, 0, 0, 700
                losed = False
                P1, E1, C1 = Player(), Enemy(), Coin()
                enemies.add(E1)
                coins.add(C1)
                all_sprites.add(P1)
                all_sprites.add(E1)
                

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    if not losed:
        DISPLAYSURF.blit(background, (0,0))
        # show scores:
        scores = font_small.render(str(SCORE), True, BLACK)
        DISPLAYSURF.blit(scores, (10,10))
        scores_coin = font_small.render(f'Coin:{SCORE_COIN}', True, BLACK)
        DISPLAYSURF.blit(scores_coin, (300,10))

        #Moves and Re-draws all Sprites
        for entity in all_sprites:
            DISPLAYSURF.blit(entity.image, entity.rect)
            entity.move()
        for coin in coins:
            coin.draw(DISPLAYSURF)
            coin.move()
        #Collision occurs between Player and Enemy:
        if pygame.sprite.spritecollideany(P1, enemies):
            file_path = os.path.join(base_dir, "music", 'crash.wav')
            pygame.mixer.Sound(file_path).play()
            time.sleep(0.5)
                    
            DISPLAYSURF.fill(RED)
            DISPLAYSURF.blit(game_over, (30,250))
            DISPLAYSURF.blit(font_small.render(f'Score:{SCORE_COIN}', True, BLACK), (150, 325))
            
            pygame.display.update()
            for entity in all_sprites:
                entity.kill() 
            for coin in coins:
                coin.kill()
            losed = True
        # Collision between Player and Coin
        if pygame.sprite.spritecollideany(P1, coins) and not losed:
            for coin in coins: # find exact coin
                one_sprite = pygame.sprite.Group()
                one_sprite.add(coin)
                if pygame.sprite.spritecollideany(P1, one_sprite):
                    coins.remove(coin)
                    SCORE_COIN += coin.weight
                    coin.kill()
                    if SCORE_COIN >= N: # change speed of enemies
                        N += 50
                        SPEED += 2
                        enemy_spawn_interval = max(enemy_spawn_interval-50, 200)
                    break
        if pygame.time.get_ticks()-last >= enemy_spawn_interval: # new enemy
            last = pygame.time.get_ticks()
            E_new = Enemy(enemies)
            enemies.add(E_new)
            all_sprites.add(E_new)
        pygame.display.update()
        FramePerSec.tick(FPS)