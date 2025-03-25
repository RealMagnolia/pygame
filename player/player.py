import pygame
import os

pygame.init()

screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Music Player")

music_directory = 'C:/Users/Руслан/Desktop/pygame/pygame/player/music_files'
os.chdir(music_directory)

music_files = [file for file in os.listdir() if file.endswith(".mp3")]

current_track = 1
paused = False

pygame.mixer.music.load(music_files[current_track])

font = pygame.font.Font(None, 24)
button_font = pygame.font.Font(None, 30)

ya = pygame.image.load("../ya.jpg")
ya = pygame.transform.scale(ya, (200, 200))

playPause = pygame.Rect(200, 350, 100, 40)
next = pygame.Rect(350, 350, 100, 40)
prev = pygame.Rect(50, 350, 100, 40)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                if paused:
                    pygame.mixer.music.unpause()
                    paused = False
                else:
                    pygame.mixer.music.pause()
                    paused = True
            elif event.key == pygame.K_RIGHT:
                current_track = (current_track + 1) % len(music_files)
                pygame.mixer.music.load(music_files[current_track])
                pygame.mixer.music.play()
            elif event.key == pygame.K_LEFT:
                current_track = (current_track - 1) % len(music_files)
                pygame.mixer.music.load(music_files[current_track])
                pygame.mixer.music.play()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if playPause.collidepoint(event.pos):  # Кнопка Play/Pause
                if paused:
                    pygame.mixer.music.unpause()
                    paused = False
                else:
                    pygame.mixer.music.pause()
                    paused = True
            elif next.collidepoint(event.pos):  # Кнопка Next
                current_track = (current_track + 1) % len(music_files)
                pygame.mixer.music.load(music_files[current_track])
                pygame.mixer.music.play()
            elif prev.collidepoint(event.pos):  # Кнопка Prev
                current_track = (current_track - 1) % len(music_files)
                pygame.mixer.music.load(music_files[current_track])
                pygame.mixer.music.play()

    screen.fill((255, 255, 255))
    screen.blit(ya, (150, 100))
    
    pygame.draw.rect(screen, (200, 200, 200), playPause)
    pygame.draw.rect(screen, (200, 200, 200), next)
    pygame.draw.rect(screen, (200, 200, 200), prev)
    
    screen.blit(button_font.render("||", True, (0, 0, 0)), (210, 360))
    screen.blit(button_font.render("->", True, (0, 0, 0)), (375, 360))
    screen.blit(button_font.render("<-", True, (0, 0, 0)), (75, 360))
    
    screen.blit(ya, (150, 100))
    pygame.display.update() 


pygame.quit()