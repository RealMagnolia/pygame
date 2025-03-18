import pygame
from datetime import datetime

RES = WIDTH, HEIGHT = 800, 800

pygame.init()
surface = pygame.display.set_mode(RES)
clock = pygame.time.Clock()
FPS = 60
done = False
myClock = pygame.image.load('clock.png')
myClock = pygame.transform.scale(myClock, (600, 600))

minutes = pygame.image.load('minhand.png')
minutes = pygame.transform.scale(minutes, (550, 550))

seconds = pygame.image.load('sechand.png')
seconds = pygame.transform.scale(seconds, (550, 550))


while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    myTime = datetime.now()
    curMins = myTime.minute
    curSec = myTime.second

    angleM = curMins * 6 * -1
    angleS = curSec * 6 * -1

    Minute = pygame.transform.rotate(minutes, angleM)
    Second = pygame.transform.rotate(seconds, angleS)

    surface.fill((255, 255, 255))
    surface.blit(myClock, (100, 100))
    surface.blit(Minute, (400 - Minute.get_width() // 2, 400 - Minute.get_height() // 2))
    surface.blit(Second, (400 - Second.get_width() // 2, 400 - Second.get_height() // 2))
    
    pygame.draw.circle(surface, (0, 0, 0), (400, 400), 22)  
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
