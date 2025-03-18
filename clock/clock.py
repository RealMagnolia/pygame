import pygame
import datetime

pygame.init()

screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()
FPS = 1
done = False
myClock = pygame.image.load('clock.png')
myClock = pygame.transform.scale(myClock, (600, 600))



minute_arrow = pygame.image.load('min_hand.png') 
minute_arrow = pygame.transform.scale(minute_arrow, (600, 600))
second_arrow = pygame.image.load('sec_hand.png')
second_arrow = pygame.transform.scale(second_arrow, (600, 600))


while not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True
        my_time = datetime.datetime.now()
        minuteINT = my_time.minute
        secondINT = my_time.second

        angleMINUTE = minuteINT * 6 * -1
        angleSECOND = secondINT * 6 * -1

        minute = pygame.transform.rotate(minute_arrow, angleMINUTE)
        second = pygame.transform.rotate(second_arrow, angleSECOND)
        

        screen.fill((255, 255, 255))
        screen.blit(myClock, (100, 100))
        screen.blit(second, (400 - int(second.get_width() / 2), 400 - int(second.get_height() / 2))) 
        screen.blit(minute, ((400 - int(minute.get_width() / 2), 400 - int(minute.get_height() / 2))))
        pygame.draw.circle(screen, (0, 0, 0), (400, 400), 22)
        pygame.display.flip()
        clock.tick(FPS)
pygame.quit()