import os

import pygame, json
base_dir = os.path.dirname(os.path.abspath(__file__))  # Get script's directory
file_path = os.path.join(base_dir, 'color.json')
with open(file_path) as f:
    color = json.loads(f.read())

def draw_border(surf, x1, y1, x2, y2, color):
    pygame.draw.line(surf, color, (x1-1, y1-1), (x1-1, y2), 1)
    pygame.draw.line(surf, color, (x1-1, y1-1), (x2, y1-1), 1)
    pygame.draw.line(surf, color, (x2, y1-1), (x2, y2), 1)
    pygame.draw.line(surf, color, (x1-1, y2), (x2, y2), 1)

def fill_button(button, border=False, bgcolor = color['white'], border_color = color['l-black']):
    button.surf.fill(bgcolor)
    if border:
        x2, y2 = button.surf.get_size()
        draw_border(button.surf, 1, 1, x2-1, y2-1, border_color)

class BUTTON:
    def __init__(self, width, height, x, y):
        self.w = width
        self.h = height
        self.surf = pygame.Surface((self.w, self.h))
        self.x = x
        self.y = y
        self.rect = self.surf.get_rect(topleft = (self.x, self.y))
    def update(self, dx, dy):
        self.x = dx
        self.y = dy
        self.rect.topleft = (self.x, self.y)
    def update_size_coord_to_center(self, dx, dy, size):
        self.w = self.h = size
        self.x, self.y = dx, dy
        self.surf = pygame.Surface((self.w, self.h))
        self.rect = self.surf.get_rect(center = (self.x, self.y))
    def check_colision(self, point):
        return self.rect.collidepoint(point)
    def draw_button(self, surf):
        surf.blit(self.surf, self.rect)
        


# Buttons for controling width:
buttons_changing_size = []

def change_for_figures():
    global buttons_changing_size
    button_1px = BUTTON(196, 50, 2, 2)
    button_3px = BUTTON(196, 50, 2, 54)
    button_5px = BUTTON(196, 50, 2, 106)
    button_8px = BUTTON(196, 50, 2, 158)
    buttons_changing_size = [button_1px, button_3px, button_5px, button_8px]
def change_for_pen():
    global buttons_changing_size
    button_1px = BUTTON(196, 50, 2, 2)
    button_2px = BUTTON(196, 50, 2, 54)
    button_3px = BUTTON(196, 50, 2, 106)
    button_4px = BUTTON(196, 50, 2, 158)
    buttons_changing_size = [button_1px, button_2px, button_3px, button_4px]
def change_for_eraser():
    global buttons_changing_size
    button_4px = BUTTON(196, 50, 2, 2)
    button_6px = BUTTON(196, 50, 2, 54)
    button_8px = BUTTON(196, 50, 2, 106)
    button_10px = BUTTON(196, 50, 2, 158)
    buttons_changing_size = [button_4px, button_6px, button_8px, button_10px]

change_for_figures()

def update_size_buttons(surf_for_draw, active_size_order, changing_size_order, ACTIVE_TOOL):
    [fill_button(but, False, color['bg_size_picker']) for but in buttons_changing_size]
    if active_size_order != changing_size_order:
        fill_button(buttons_changing_size[active_size_order], True, color['picked_button'], color['picked_button_border'])
    if changing_size_order != -1:
        fill_button(buttons_changing_size[changing_size_order], True, color['in_button'], color['in_button_border'])
    def draw_line_to_button_changing_size(ord, size): 
        pygame.draw.line(buttons_changing_size[ord].surf, color['black'], (15, 24), (180, 24), size)
    if ACTIVE_TOOL != 'eraser':
        draw_line_to_button_changing_size(0, 1)
    else:
        draw_line_to_button_changing_size(0, 4)
    if ACTIVE_TOOL == 'pen':
        draw_line_to_button_changing_size(1, 2)
        draw_line_to_button_changing_size(2, 3)
        draw_line_to_button_changing_size(3, 4)
    elif ACTIVE_TOOL == 'eraser':
        draw_line_to_button_changing_size(1, 6)
        draw_line_to_button_changing_size(2, 8)
        draw_line_to_button_changing_size(3, 10)
    else:
        draw_line_to_button_changing_size(1, 3)
        draw_line_to_button_changing_size(2, 5)
        draw_line_to_button_changing_size(3, 8)
    [but.draw_button(surf_for_draw[3].surface) for but in buttons_changing_size]


def determine_size_by_order(ord, ACTIVE_TOOL):
    if ACTIVE_TOOL == 'pen':
        return ord + 1
    elif ACTIVE_TOOL == 'eraser':
        return 4 + ord * 2

    if ord == 0:
        return 1
    elif ord == 1:
        return 3
    elif ord == 2:
        return 5
    elif ord == 3:
        return 8

    return None
