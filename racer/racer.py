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
SPEED = 5
SPEED_COIN = 5
SCORE = 0
Coin_score = 0

#Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)
base_dir = os.path.dirname(os.path.abspath(__file__))

file_path = os.path.join(base_dir, 'images', 'AnimatedStreet.png')
background = pygame.image.load(file_path)
 
#Create a white screen 
DISPLAYSURF = pygame.display.set_mode((400,600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")
 
class Enemy_and_Coin(pygame.sprite.Sprite):
    def __init__(self, coin = False, enemies = None):
        super().__init__() 
        self.coin = coin
        # setting image for enemy/coin:
        if not coin:
            file_path = os.path.join(base_dir, 'images', f"enemy{random.randint(1, 3)}.png")
            self.image = pygame.image.load(file_path)
        else:
            file_path = os.path.join(base_dir, 'images', f"coin.png")
            self.image = pygame.image.load(file_path)
        self.rect = self.image.get_rect()
        # give positions for enemy and coin:
        if not coin: self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)  
        else: self.coin_pos(enemies)
 
    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED if not self.coin else SPEED_COIN)
        if (self.rect.top > 600):
            if not self.coin: # set up new image for enemy:
                file_path = os.path.join(base_dir, 'images', f"enemy{random.randint(1, 3)}.png")
                self.image = pygame.image.load(file_path)
                SCORE += 1
                self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
            else:
                self.rect.center = (random.randint(50, SCREEN_WIDTH - 50), 0)
            self.rect.top = 0

    def coin_pos(self, enemies): # set up coin possition such that it isn't collide with enemies
        self.rect.center = (random.randint(50, SCREEN_WIDTH-50), 0) 
        while pygame.sprite.spritecollideany(self, enemies):
            self.rect.center = (random.randint(50, SCREEN_WIDTH-50), 0)
 
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        file_path = os.path.join(base_dir, 'images', 'player.png')
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
E1 = Enemy_and_Coin()

#Creating Sprites Groups
enemies = pygame.sprite.Group()
enemies.add(E1)
 
# Creatting coin
C1 = Enemy_and_Coin(True, enemies)
coins = pygame.sprite.Group()
coins.add(C1)


all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)

#Adding a new User event 
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

#Game Loop
while True:
       
    #Cycles through all events occurring  
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == INC_SPEED:
            SPEED += 0.5

    DISPLAYSURF.blit(background, (0,0))
    # show scores:
    scores = font_small.render(str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10,10))
    scores_coin = font_small.render(f'Coin: {Coin_score}', True, BLACK)
    DISPLAYSURF.blit(scores_coin, (310,10))

    #Moves and Re-draws all Sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()
 
    #To be run if collision occurs between Player and Enemy
    if pygame.sprite.spritecollideany(P1, enemies):
        file_path = os.path.join(base_dir, 'music', f"crash.wav")
        pygame.mixer.Sound(file_path).play()
        time.sleep(0.5)
                    
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30,250))
           
        pygame.display.update()
        for entity in all_sprites:
            entity.kill() 
        time.sleep(2)
        pygame.quit()
        sys.exit()        
    elif pygame.sprite.spritecollideany(P1, coins): # player is getting coin
        Coin_score += 1
        for coin in coins:
            coin.coin_pos(enemies)
    pygame.display.update()
    FramePerSec.tick(FPS)