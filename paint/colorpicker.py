import os

import pygame, button, json
base_dir = os.path.dirname(os.path.abspath(__file__))  # Get script's directory
file_path = os.path.join(base_dir, 'color.json')
with open(file_path) as f:
    color = json.loads(f.read())

surf_copy = pygame.Surface((256, 256))

def get_palette():
    surf = pygame.Surface((1, 2))
    surf.fill((255,255,255))
    surf.set_at((0, 1), (0,0,0))
    surf = pygame.transform.smoothscale(surf, surf_copy.get_size())
    
    surf2 = pygame.Surface((2,1))
    surf2.fill((255,255,255)) #replace color
    surf2.set_at((1,0), main_color)
    surf2 = pygame.transform.smoothscale(surf2, surf_copy.get_size())
    surf.blit(surf2, (0,0), special_flags=pygame.BLEND_MULT)
    return surf

pallete_rect = pygame.rect.Rect((3, 38), surf_copy.get_size())
main_color = (255,0,0)

def fill_surface(surf, current_color):
    global main_color
    font = pygame.font.SysFont('cambriamath', 20)
    # font = pygame.font.SysFont('bahnschrift', 20)
    text = font.render('Change color palette', True, color['black'])
    surf.blit(text, (5, 5))
    pygame.draw.rect(surf, color['l-gray'], (0, 35, surf.get_width(), surf.get_height()-35))
    palette = get_palette()
    surf.blit(palette, (3, 38))
    button.draw_border(surf, 1, 1, surf.get_width()-1, surf.get_height()-1, color['black'])
    pygame.draw.line(surf, color['black'], (0, 35), (surf.get_width(), 35))
    text_R = font.render(f'R: {current_color[0]}', True, color['black'])
    text_G = font.render(f'G: {current_color[1]}', True, color['black'])
    text_B = font.render(f'B: {current_color[2]}', True, color['black'])
    surf.blit(text_R, (265, 40))
    surf.blit(text_G, (265, 70))
    surf.blit(text_B, (265, 100))
    cp.update()
    if main_color != cp.get_color():
        main_color = cp.get_color()
    cp.draw(surf)

def cursor(surf, x, y):
    pygame.draw.circle(surf, color['white'], (x, y), 5, 1)


class Colorpick:
    def __init__(self, x, y, width, height, color):
        self.surface = pygame.Surface((width, height))
        self.surface.fill(color)
        self.rect = pygame.rect.Rect((x, y), (width, height))
        self.rad = height//2
        self.pwidth = width - self.rad//2
        self.bgcolor, self.x, self.y = color, x, y
        for i in range(self.pwidth):
            color = pygame.Color(0)
            color.hsla = (int(360*i/self.pwidth), 100,50,100)
            pygame.draw.rect(self.surface, color, (self.rad + i, 0, 1, int(height*0.5)))
        self.p = 0
    def get_color(self):
        color = pygame.Color(0)
        color.hsla = (int(self.p * 360), 100,50,100)
        return color
    def update(self):
        points = list(pygame.mouse.get_pos())
        points[0] -= 800
        points[1] -= 75
        if pygame.mouse.get_pressed()[0] and self.rect.collidepoint(points):
            self.p = (points[0] - self.x - self.rad)/self.pwidth
            self.p = max(0, min(self.p, 1))
        
    def draw(self, surf):
        surf.blit(self.surface, self.rect)
        center = (self.x + self.rad + self.pwidth * self.p, self.rect.centery)
        pygame.draw.rect(surf, (0,0,0), (center[0]-self.rad//2+10, center[1]-25, 5, self.rad+5), 1, border_radius = 2)

cp = Colorpick(5, 320, 300, 45, color['l-gray'])