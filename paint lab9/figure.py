import os

import pygame, json, button
base_dir = os.path.dirname(os.path.abspath(__file__))  # Get script's directory
file_path = os.path.join(base_dir, 'color.json')
with open(file_path) as f:
    color = json.loads(f.read())

class FIGURE:
    def __init__(self, type, width=0, height=0, x=0, y=0, radius=0, border_size = 5):
        self.type = type
        self.x, self.y, self.border_size = x, y, border_size
        self.startx, self.starty = self.x, self.y
        self.w = self.h = self.r = 0
        if type != 'circle':
            self.w, self.h = width, height
            self.surf = pygame.Surface((self.w, self.h))
        elif type == 'circle':
            self.r = radius
            self.x += self.r 
            self.y += self.r
            self.const_stx = self.startx = self.x - self.r
            self.const_sty = self.starty = self.y - self.r
            self.endx = self.x + self.r
            self.endy = self.y + self.r
            self.surf = pygame.Surface((self.r*2, self.r*2))
        if type == 'square' or type == 'r-triangle' or type == 'e-triangle' or type == 'romb': 
            self.startx, self.endx, self.starty, self.endy = self.x, self.x+self.w, self.y, self.y+self.h
            self.const_stx = self.startx
            self.const_sty = self.starty
        if type == 'rectangle' or type == 'square' or type == 'r-triangle' or type == 'e-triangle' or type == 'romb': 
            self.rect = pygame.rect.Rect((self.x, self.y), (self.w, self.h))
        if type == 'circle': 
            self.rect = self.surf.get_rect(topleft = (self.x-self.r, self.y-self.r))
        if type == 'r-triangle' or type == 'e-triangle' or type == 'romb':
            self.border_size = 1
        self.buttons = {}
        FIGURE.update_buttons(self)

    def update_surf_rect(self):
        if self.type != 'circle':
            self.surf = pygame.Surface((self.w, self.h))
            self.rect = self.surf.get_rect(topleft = (self.x, self.y)) # check for/determine collides 
        elif self.type == 'circle': 
            self.surf = pygame.Surface((self.r*2, self.r*2))
            self.rect = self.surf.get_rect(topleft = (self.x-self.r, self.y-self.r))
    def update_surf_rect_by_start_end(self):
        if self.type == 'rectangle' or self.type == 'r-triangle' or self.type == 'romb': 
            self.surf = pygame.Surface((self.w, self.h))
            self.rect = self.surf.get_rect(topleft = (self.x, self.y)) # check for/determine collides 
        elif self.type == 'circle' or self.type == 'square' or self.type == 'e-triangle': 
            self.rect = pygame.rect.Rect((self.startx, self.starty), (abs(self.endx-self.startx), abs(self.endy-self.starty)))
            self.rect.topleft = (self.startx, self.starty)
        
    def update_buttons(self):
        #PLEASE DON'T CHANGE
        if self.type == 'rectangle' or self.type == 'r-triangle' or self.type == 'romb':
            self.buttons['top_left'] = button.BUTTON(5, 5, self.x + self.border_size//2 - 5//2, self.y + self.border_size//2 - 5//2)
            self.buttons['top'] = button.BUTTON(5, 5, self.x + self.w//2 - 5//2, self.y + self.border_size//2 - 5//2)
            self.buttons['top_right'] = button.BUTTON(5, 5, self.x + self.w - 3 - self.border_size//2, self.y + self.border_size//2 - 5//2)
            self.buttons['left'] = button.BUTTON(5, 5, self.x + self.border_size//2 - 5//2, self.y + self.h//2 - 5//2)
            self.buttons['bottom_left'] = button.BUTTON(5, 5, self.x + self.border_size//2 - 5//2, self.y + self.h - 3 - self.border_size//2)
            self.buttons['bottom'] = button.BUTTON(5, 5, self.x + self.w//2 - 5//2, self.y + self.h - 3 - self.border_size//2)
            self.buttons['bottom_right'] = button.BUTTON(5, 5, self.x + self.w - 3 - self.border_size//2, self.y + self.h - 3 - self.border_size//2)
            self.buttons['right'] = button.BUTTON(5, 5, self.x + self.w - 3 - self.border_size//2, self.y + self.h//2 - 5//2)
        elif self.type == 'circle':
            self.buttons['top_left'] = button.BUTTON(5, 5, self.startx, self.starty)
            self.buttons['top_right'] = button.BUTTON(5, 5, self.endx - 5, self.starty)
            self.buttons['bottom_left'] = button.BUTTON(5, 5, self.startx, self.endy - 5)
            self.buttons['bottom_right'] = button.BUTTON(5, 5, self.endx - 5, self.endy - 5)
        elif self.type == 'square' or self.type == 'e-triangle':
            self.buttons['top_left'] = button.BUTTON(5, 5, self.startx + self.border_size//2 - 5//2, self.starty + self.border_size//2 - 5//2)
            self.buttons['top_right'] = button.BUTTON(5, 5, self.endx - 3 - self.border_size//2, self.starty + self.border_size//2 - 5//2)
            self.buttons['bottom_left'] = button.BUTTON(5, 5, self.startx + self.border_size//2 - 5//2, self.endy - 3 - self.border_size//2)
            self.buttons['bottom_right'] = button.BUTTON(5, 5, self.endx - 3 - self.border_size//2, self.endy - 3 - self.border_size//2)
        [button.fill_button(i, True) for i in self.buttons.values()]
    
    def draw_buttons(self, surf):
        FIGURE.update_buttons(self)
        if self.type == 'rectangle' or self.type == 'r-triangle' or self.type == 'romb':
            x1 = self.x + self.border_size//2
            x2 = self.x + self.w - self.border_size//2  - 1 
            y1 = self.y + self.border_size//2
            y2 = self.y + self.h - self.border_size//2 - 1
        if self.type == 'circle':
            x1 = self.startx + 2
            x2 = self.endx - 3 
            y1 = self.starty + 2
            y2 = self.endy - 3 
        if self.type == 'square' or self.type == 'e-triangle':
            x1 = int(self.startx + self.border_size//2)
            x2 = int(self.endx - self.border_size//2  - 1) 
            y1 = int(self.starty + self.border_size//2)
            y2 = int(self.endy - self.border_size//2 - 1)
        self.rect = pygame.rect.Rect((x1, y1), (x2-x1, y2-y1))
        
        for i in range(x1+1, x2, 6): 
            pygame.draw.line(surf, color['blue'], (min(i, x2), y1), (min(i+3, x2), y1), 1)
            pygame.draw.line(surf, color['white'], (min(i+3, x2), y1), (min(i+6, x2), y1), 1)
            pygame.draw.line(surf, color['blue'], (i, y2), (i+3, y2), 1)
            pygame.draw.line(surf, color['white'], (min(i+3, x2), y2), (min(i+6, x2), y2), 1)
        for i in range(y1+1, y2, 6):
            pygame.draw.line(surf, color['blue'], (x1, i), (x1, i+3), 1)
            pygame.draw.line(surf, color['white'], (x1, min(i+3, y2)), (x1, min(i+6, y2)), 1)
            pygame.draw.line(surf, color['blue'], (x2, i), (x2, i+3), 1)
            pygame.draw.line(surf, color['white'], (x2, min(i+3, y2)), (x2, min(i+6, y2)), 1)
        for but in self.buttons.values():
            if self.type == 'rectangle': FIGURE.update_surf_rect(self)
            else: FIGURE.update_surf_rect_by_start_end(self)
            but.draw_button(surf)
    
    def draw_figure(self, surf, color):
        if self.type == 'rectangle' or self.type == 'square':
            pygame.draw.rect(surf, color, (self.x, self.y, self.w, self.h), self.border_size)
        elif self.type == 'circle':
            pygame.draw.circle(surf, color, (self.x, self.y), self.r, self.border_size)
        elif self.type == 'r-triangle':
            # pygame.draw.polygon(surf, color, ((self.x, self.y), (self.x, self.y+self.h-self.border_size), (self.x+self.w-self.border_size, self.y+self.h-self.border_size)), self.border_size)
            pygame.draw.aalines(surf, color, True, ((self.x, self.y), (self.x, self.y+self.h), (self.x+self.w, self.y+self.h)))
        elif self.type == 'e-triangle':
            pygame.draw.aalines(surf, color, True, ((self.x, self.y+self.h), (self.x+self.w//2, self.y), (self.x+self.w, self.y+self.h)))
        elif self.type == 'romb':
            pygame.draw.aalines(surf, color, True, ((self.x, self.y + self.h//2), (self.x+self.w//2, self.y), (self.x+self.w, self.y+self.h//2), (self.x + self.w//2, self.y+self.h)))
    def update_by_start(self, x2, y2): # x2, y2
        if self.type == 'rectangle' or self.type == 'r-triangle' or self.type == 'romb':
            self.w = abs(self.startx-x2)
            self.h = abs(self.starty-y2)
            self.x = min(self.startx, x2)
            self.y = min(self.starty, y2)
        elif self.type == 'square' or self.type == 'e-triangle':
            self.x = min(self.const_stx, x2)
            self.y = min(self.const_sty, y2)
            self.w = abs(x2-self.const_stx)
            self.h = abs(y2-self.const_sty)
            if self.type == 'square':
                self.w = min(self.w, self.h)
                self.h = self.w
            elif self.type == 'e-triangle':
                self.w = min(self.w, int(self.h*2/(3**0.5)))
                self.h = (self.w * (3**0.5))//2
            if self.x != self.const_stx:
                self.x = self.const_stx - self.w
                self.startx = self.x
            else:
                self.startx = self.const_stx
            if self.y != self.const_sty:
                self.y = self.const_sty - self.h
                self.starty = self.y
            else:
                self.starty = self.const_sty
            self.endx = int(self.x + self.w)
            self.endy = int(self.y + self.h)
        elif self.type == 'circle':
            self.r = min(abs(x2-self.const_stx)//2, abs(y2-self.const_sty)//2)
            if x2 > self.const_stx and y2 < self.const_sty:
                self.starty = self.const_sty - self.r*2
            elif x2 < self.const_stx and y2 > self.const_sty:
                self.startx = self.const_stx - self.r*2
            elif x2 < self.const_stx and y2 < self.const_sty:
                self.startx = self.const_stx - self.r*2
                self.starty = self.const_sty - self.r*2
            self.x = self.startx + self.r
            self.y = self.starty + self.r
            self.endx = self.x + self.r
            self.endy = self.y + self.r
            
        if self.type == 'rectangle' or self.type == 'r-triangle' or self.type == 'romb': FIGURE.update_surf_rect(self)
        elif self.type == 'circle' or self.type == 'square' or self.type == 'e-triangle': FIGURE.update_surf_rect_by_start_end(self)
    def points_tl_tr_bl_br(self):
        if self.type == 'rectangle' or self.type == 'r-triangle' or self.type == 'romb':
            self.tl = (self.x, self.y)
            self.tr = (self.x+self.w, self.y)
            self.bl = (self.x, self.y + self.h)
            self.br = (self.x+self.w, self.y+self.h)
        if self.type == 'circle' or self.type == 'square' or self.type == 'e-triangle':
            self.tl = (self.startx, self.starty)
            self.tr = (self.endx, self.starty)
            self.bl = (self.startx, self.endy)
            self.br = (self.endx, self.endy)
        



change_figure_bottom = {
    'top_left' : False,
    'top_right' : False,
    'top' : False,
    'bottom_left' : False,
    'bottom_right' : False,
    'bottom' : False,
    'left' : False,
    'right' : False
}
def null():
    for i in change_figure_bottom.keys(): change_figure_bottom[i] = False

def from_win_to_working_surf_position(event, h):
    point_in_working_surf = list(event.pos)
    point_in_working_surf[0] -= 5
    point_in_working_surf[1] -=  h//9+5
    return point_in_working_surf
def check_for_figure_button(event, current_figure, h):
    if current_figure == None: return 
    point_in_working_surf = from_win_to_working_surf_position(event, h)
    if current_figure.buttons['top_left'].rect.collidepoint(point_in_working_surf):
        change_figure_bottom['top_left'] = True
    if 'top' in current_figure.buttons.keys() and current_figure.buttons['top'].rect.collidepoint(point_in_working_surf):
        change_figure_bottom['top'] = True
    if current_figure.buttons['top_right'].rect.collidepoint(point_in_working_surf):
        change_figure_bottom['top_right'] = True
    if current_figure.buttons['bottom_left'].rect.collidepoint(point_in_working_surf):
        change_figure_bottom['bottom_left'] = True
    if 'bottom' in current_figure.buttons.keys() and current_figure.buttons['bottom'].rect.collidepoint(point_in_working_surf):
        change_figure_bottom['bottom'] = True
    if current_figure.buttons['bottom_right'].rect.collidepoint(point_in_working_surf):
        change_figure_bottom['bottom_right'] = True
    if 'left' in current_figure.buttons.keys() and current_figure.buttons['left'].rect.collidepoint(point_in_working_surf):
        change_figure_bottom['left'] = True
    if 'right' in current_figure.buttons.keys() and current_figure.buttons['right'].rect.collidepoint(point_in_working_surf):
        change_figure_bottom['right'] = True

def change_figure_by_buttom(current_figure, points):
    current_figure.points_tl_tr_bl_br()
    if current_figure.type == 'rectangle' or current_figure.type == 'r-triangle' or current_figure.type == 'romb':
        if change_figure_bottom['top_left']:
            current_figure.x = min(points[0], current_figure.br[0] - int(current_figure.border_size*1.5) - 5)
            current_figure.w = current_figure.br[0] - current_figure.x
            current_figure.y = min(points[1], current_figure.br[1] - int(current_figure.border_size*1.5) - 5) 
            current_figure.h = current_figure.br[1] - current_figure.y
        elif change_figure_bottom['top']:
            current_figure.y = min(points[1], current_figure.br[1] - int(current_figure.border_size*1.5) - 5)
            current_figure.h = current_figure.br[1] - current_figure.y
        elif change_figure_bottom['top_right']:
            current_figure.w = max(points[0]-current_figure.x, int(current_figure.border_size*1.5) + 5)
            current_figure.y = min(points[1], current_figure.bl[1] - int(current_figure.border_size*1.5) - 5) 
            current_figure.h = current_figure.bl[1] - current_figure.y
        elif change_figure_bottom['right']:
            current_figure.w = max(points[0]-current_figure.x, int(current_figure.border_size*1.5) + 5)
        elif change_figure_bottom['bottom_right']:
            current_figure.w = max(points[0]-current_figure.x, int(current_figure.border_size*1.5) + 5)
            current_figure.h = max(points[1]-current_figure.y, int(current_figure.border_size*1.5) + 5)
        elif change_figure_bottom['bottom']:
            current_figure.h = max(points[1]-current_figure.y, int(current_figure.border_size*1.5) + 5)
        elif change_figure_bottom['bottom_left']:
            current_figure.x = min(points[0], current_figure.br[0] - int(current_figure.border_size*1.5) - 5)
            current_figure.w = current_figure.br[0] - current_figure.x
            current_figure.h = max(points[1]-current_figure.y, int(current_figure.border_size*1.5) + 5)
        elif change_figure_bottom['left']:
            current_figure.x = min(points[0], current_figure.br[0] - int(current_figure.border_size*1.5) - 5)
            current_figure.w = current_figure.br[0] - current_figure.x
    if current_figure.type == 'circle':
        if change_figure_bottom['top_left']:
            current_figure.startx = min(points[0], current_figure.br[0] - int(current_figure.border_size*1.5))
            current_figure.starty = min(points[1], current_figure.br[1] - int(current_figure.border_size*1.5))
            current_figure.r = min(abs(current_figure.br[0] - current_figure.startx)//2, abs(current_figure.br[1] - current_figure.starty)//2)
            current_figure.x = current_figure.br[0] - current_figure.r  
            current_figure.y = current_figure.br[1] - current_figure.r
        if change_figure_bottom['top_right']:
            current_figure.endx = max(points[0], current_figure.startx + int(current_figure.border_size*1.5))
            current_figure.starty = min(points[1], current_figure.bl[1] - int(current_figure.border_size*1.5))
            current_figure.r = min(abs(current_figure.startx-current_figure.endx)//2, abs(current_figure.starty-current_figure.endy)//2)
            current_figure.x = current_figure.bl[0] + current_figure.r  
            current_figure.y = current_figure.bl[1] - current_figure.r
        if change_figure_bottom['bottom_right']:
            current_figure.endx = max(points[0], current_figure.startx + int(current_figure.border_size*1.5))
            current_figure.endy = max(points[1], current_figure.starty + int(current_figure.border_size*1.5))
            current_figure.r = min(abs(current_figure.startx-current_figure.endx)//2, abs(current_figure.starty-current_figure.endy)//2)
            current_figure.x = current_figure.tl[0] + current_figure.r  
            current_figure.y = current_figure.tl[1] + current_figure.r
        if change_figure_bottom['bottom_left']:
            current_figure.startx = min(points[0], current_figure.br[0] - int(current_figure.border_size*1.5))
            current_figure.endy = max(points[1], current_figure.starty + int(current_figure.border_size*1.5))
            current_figure.r = min(abs(current_figure.startx-current_figure.endx)//2, abs(current_figure.starty-current_figure.endy)//2)
            current_figure.x = current_figure.tr[0] - current_figure.r  
            current_figure.y = current_figure.tr[1] + current_figure.r
    
    if current_figure.type == 'square' or current_figure.type == 'e-triangle':
        if change_figure_bottom['top_left']:
            current_figure.x = min(points[0], current_figure.br[0] - int(current_figure.border_size*1.5) - 5)
            current_figure.w = current_figure.br[0] - current_figure.x
            current_figure.y = min(points[1], current_figure.br[1] - int(current_figure.border_size*1.5) - 5) 
            current_figure.h = current_figure.br[1] - current_figure.y
            if current_figure.type == 'square':
                current_figure.w = min(current_figure.w, current_figure.h)
                current_figure.h = current_figure.w
            elif current_figure.type == 'e-triangle':
                current_figure.w = min(current_figure.w, int(current_figure.h*2/(3**0.5)))
                current_figure.h = (current_figure.w * (3**0.5))//2
            current_figure.x = current_figure.br[0] - current_figure.w
            current_figure.y = current_figure.br[1] - current_figure.h
            current_figure.startx, current_figure.starty = current_figure.x, current_figure.y
            current_figure.endx, current_figure.endy = current_figure.x+current_figure.w, current_figure.y+current_figure.h
        elif change_figure_bottom['top_right']:
            current_figure.w = max(points[0]-current_figure.x, int(current_figure.border_size*1.5) + 5)
            current_figure.y = min(points[1], current_figure.bl[1] - int(current_figure.border_size*1.5) - 5) 
            current_figure.h = current_figure.bl[1] - current_figure.y
            if current_figure.type == 'square':
                current_figure.w = min(current_figure.w, current_figure.h)
                current_figure.h = current_figure.w
            elif current_figure.type == 'e-triangle':
                current_figure.w = min(current_figure.w, int(current_figure.h*2/(3**0.5)))
                current_figure.h = (current_figure.w * (3**0.5))//2
            current_figure.y = current_figure.bl[1] - current_figure.h
            current_figure.startx, current_figure.starty = current_figure.x, current_figure.y
            current_figure.endx, current_figure.endy = current_figure.x+current_figure.w, current_figure.y+current_figure.h
        elif change_figure_bottom['bottom_right']:
            current_figure.w = max(points[0]-current_figure.x, int(current_figure.border_size*1.5) + 5)
            current_figure.h = max(points[1]-current_figure.y, int(current_figure.border_size*1.5) + 5)
            if current_figure.type == 'square':
                current_figure.w = min(current_figure.w, current_figure.h)
                current_figure.h = current_figure.w
            elif current_figure.type == 'e-triangle':
                current_figure.w = min(current_figure.w, int(current_figure.h*2/(3**0.5)))
                current_figure.h = (current_figure.w * (3**0.5))//2
            current_figure.startx, current_figure.starty = current_figure.x, current_figure.y
            current_figure.endx, current_figure.endy = current_figure.x+current_figure.w, current_figure.y+current_figure.h
        elif change_figure_bottom['bottom_left']:
            current_figure.x = min(points[0], current_figure.br[0] - int(current_figure.border_size*1.5) - 5)
            current_figure.w = current_figure.br[0] - current_figure.x
            current_figure.h = max(points[1]-current_figure.y, int(current_figure.border_size*1.5) + 5)
            if current_figure.type == 'square':
                current_figure.w = min(current_figure.w, current_figure.h)
                current_figure.h = current_figure.w
            elif current_figure.type == 'e-triangle':
                current_figure.w = min(current_figure.w, int(current_figure.h*2/(3**0.5)))
                current_figure.h = (current_figure.w * (3**0.5))//2
            current_figure.x = current_figure.br[0] - current_figure.w
            current_figure.startx, current_figure.starty = current_figure.x, current_figure.y
            current_figure.endx, current_figure.endy = current_figure.x+current_figure.w, current_figure.y+current_figure.h
        
    return current_figure

# MAKING CHOICE OF TOOLS:
pen = button.BUTTON(55, 55, 10, 10)
rectangle = button.BUTTON(55, 55, 80, 10)
circle = button.BUTTON(55, 55, 150, 10)
square = button.BUTTON(55, 55, 220, 10)
r_triangle = button.BUTTON(55, 55, 290, 10)
e_triangle = button.BUTTON(55, 55, 360, 10)
romb = button.BUTTON(55, 55, 430, 10)
eraser = button.BUTTON(55, 55, 500, 10)
fill = button.BUTTON(55, 55, 570, 10)
TOOL_BUTTONS = {
    'pen' : pen,
    'rectangle' : rectangle,
    'circle' : circle,
    'square' : square,
    'r-triangle' : r_triangle,
    'e-triangle' : e_triangle,
    'romb' : romb,
    'eraser' : eraser,
    'fill' : fill
}

# FILL BACKGROUND OF TOOL BUTTONS:
def fill_bg_tools(except_type=None):
    [button.fill_button(tool, True, color['upper_block'], color['border_tools']) for type, tool in TOOL_BUTTONS.items() if type!=except_type]
fill_bg_tools()
# PEN:
def update_pen():
    file_path = os.path.join(base_dir, 'pencil.png')
    pen_image = pygame.image.load(file_path)
    TOOL_BUTTONS['pen'].surf.blit(pen_image, (3, 3))

# RECTANGLE:
def update_rectangle():
    pygame.draw.rect(TOOL_BUTTONS['rectangle'].surf, color['dark_blue'], (6, 15, 43,25), 1)
    pygame.draw.rect(TOOL_BUTTONS['rectangle'].surf, color['bg_figure'], (7, 16, 41, 23))

# CIRCLE:
def update_circle():
    pygame.draw.circle(TOOL_BUTTONS['circle'].surf, color['dark_blue'], (55//2, 55//2), 18, 1)
    pygame.draw.circle(TOOL_BUTTONS['circle'].surf, color['bg_figure'], (55//2, 55//2), 17)

# SQUARE:
def update_square():
    pygame.draw.rect(TOOL_BUTTONS['square'].surf, color['dark_blue'], (12, 12, 30,30), 1)
    pygame.draw.rect(TOOL_BUTTONS['square'].surf, color['bg_figure'], (13, 13, 28, 28))

# RIGHT TRIANGLE:
def update_r_triangle():
    pygame.draw.polygon(TOOL_BUTTONS['r-triangle'].surf, color['bg_figure'], ((11, 11), (11, 44), (44, 44)))
    pygame.draw.polygon(TOOL_BUTTONS['r-triangle'].surf, color['dark_blue'], ((11, 11), (11, 44), (44, 44)), 1)

# EQUILATERAL TRIANGLE:
def update_e_triangle():
    pygame.draw.polygon(TOOL_BUTTONS['e-triangle'].surf, color['bg_figure'], ((9,42), (27, 10), (45, 42)))
    pygame.draw.aalines(TOOL_BUTTONS['e-triangle'].surf, color['dark_blue'],True, ((9,42), (27, 10), (45, 42)))
    # pygame.draw.polygon(TOOL_BUTTONS['e-triangle'].surf, color['dark_blue'], ((9,42), (27, 10), (45, 42)), 1)

# ROMB:
def update_romb():
    pygame.draw.polygon(TOOL_BUTTONS['romb'].surf, color['bg_figure'], ((10, 28), (27, 11), (44, 28), (27, 45)))
    pygame.draw.aalines(TOOL_BUTTONS['romb'].surf, color['dark_blue'], True, ((10, 28), (27, 11), (44, 28), (27, 45)))

# ERASER:
def update_eraser():
    file_path = os.path.join(base_dir, 'eraser.png')
    eraser_image = pygame.image.load(file_path)
    TOOL_BUTTONS['eraser'].surf.blit(eraser_image, (10, 10))

# FILL:
def update_fill():
    file_path = os.path.join(base_dir, 'fill.png')
    fill_image = pygame.image.load(file_path)
    TOOL_BUTTONS['fill'].surf.blit(fill_image, (12, 10))

# First update, to draw all content to TOOLS
def update_all(except_type = None):
    fill_bg_tools(except_type)
    update_pen()
    update_rectangle()
    update_circle()
    update_square()
    update_r_triangle()
    update_e_triangle()
    update_romb()
    update_eraser()
    update_fill()
update_all()



def change_by_collision(points, ACTIVE_TOOL = None):
    if TOOL_BUTTONS['pen'].rect.collidepoint(points):
        update_all(except_type = 'pen')
        button.fill_button(TOOL_BUTTONS['pen'], True, color['in_button'], color['in_button_border'])
        update_pen()
    elif TOOL_BUTTONS['rectangle'].rect.collidepoint(points):
        update_all(except_type = 'rectangle')
        button.fill_button(TOOL_BUTTONS['rectangle'], True, color['in_button'], color['in_button_border'])
        update_rectangle()
    elif TOOL_BUTTONS['circle'].rect.collidepoint(points):
        update_all(except_type = 'circle')
        button.fill_button(TOOL_BUTTONS['circle'], True, color['in_button'], color['in_button_border'])
        update_circle()
    elif TOOL_BUTTONS['square'].rect.collidepoint(points):
        update_all(except_type = 'square')
        button.fill_button(TOOL_BUTTONS['square'], True, color['in_button'], color['in_button_border'])
        update_square()
    elif TOOL_BUTTONS['r-triangle'].rect.collidepoint(points):
        update_all(except_type = 'r-triangle')
        button.fill_button(TOOL_BUTTONS['r-triangle'], True, color['in_button'], color['in_button_border'])
        update_r_triangle()
    elif TOOL_BUTTONS['e-triangle'].rect.collidepoint(points):
        update_all(except_type = 'e-triangle')
        button.fill_button(TOOL_BUTTONS['e-triangle'], True, color['in_button'], color['in_button_border'])
        update_e_triangle()
    elif TOOL_BUTTONS['romb'].rect.collidepoint(points):
        update_all(except_type = 'romb')
        button.fill_button(TOOL_BUTTONS['romb'], True, color['in_button'], color['in_button_border'])
        update_romb()
    elif TOOL_BUTTONS['eraser'].rect.collidepoint(points):
        update_all(except_type = 'eraser')
        button.fill_button(TOOL_BUTTONS['eraser'], True, color['in_button'], color['in_button_border'])
        update_eraser()
    elif TOOL_BUTTONS['fill'].rect.collidepoint(points):
        update_all(except_type = 'fill')
        button.fill_button(TOOL_BUTTONS['fill'], True, color['in_button'], color['in_button_border'])
        update_fill()
    else:
        update_all()

    if ACTIVE_TOOL != None:
        button.fill_button(TOOL_BUTTONS[ACTIVE_TOOL], True, color['picked_button'], color['picked_button_border'])
        update_by_Active_tool(ACTIVE_TOOL)

def check_for_collision(points):
    if TOOL_BUTTONS['pen'].rect.collidepoint(points): return 'pen'
    elif TOOL_BUTTONS['rectangle'].rect.collidepoint(points): return 'rectangle'
    elif TOOL_BUTTONS['circle'].rect.collidepoint(points): return 'circle'
    elif TOOL_BUTTONS['square'].rect.collidepoint(points): return 'square'
    elif TOOL_BUTTONS['r-triangle'].rect.collidepoint(points): return 'r-triangle'
    elif TOOL_BUTTONS['e-triangle'].rect.collidepoint(points): return 'e-triangle'
    elif TOOL_BUTTONS['romb'].rect.collidepoint(points): return 'romb'
    elif TOOL_BUTTONS['eraser'].rect.collidepoint(points): return 'eraser'
    elif TOOL_BUTTONS['fill'].rect.collidepoint(points): return 'fill'
    else: return None

def update_by_Active_tool(active_tool):
    if active_tool == 'pen': update_pen()
    if active_tool == 'rectangle': update_rectangle()
    if active_tool == 'circle': update_circle()
    if active_tool == 'square': update_square()
    if active_tool == 'r-triangle': update_r_triangle()
    if active_tool == 'e-triangle': update_e_triangle()
    if active_tool == 'romb': update_romb()
    if active_tool == 'eraser': update_eraser()
    if active_tool == 'fill': update_fill()


eraser_button = button.BUTTON(4, 4, 0, 0)
button.fill_button(eraser_button, True)