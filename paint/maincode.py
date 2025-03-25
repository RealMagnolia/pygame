import os

import pygame, button, figure, colorpicker ,json
pygame.init()

base_dir = os.path.dirname(os.path.abspath(__file__))  # Get script's directory
file_path = os.path.join(base_dir, 'color.json')
with open(file_path) as f:
    color = json.loads(f.read())

w = 1200
h = 666
win = pygame.display.set_mode((w, h))
pygame.display.set_caption('Paint')

def not_dots(): 
    if ACTIVE_TOOL == 'rectangle' and current_figure != None: return current_figure.w > 1 and current_figure.h > 1
    elif ACTIVE_TOOL == 'circle' and current_figure != None: return current_figure.r > 2
    else: return False
def draw_working_surface():
    if stage_of_figure>=1 and not_dots():
        current_figure.draw_figure(surf_for_draw[1].surface, current_color)
        if stage_of_figure >= 2:
            current_figure.draw_buttons(surf_for_draw[1].surface)
    surf_for_draw[2].draw_to_surface(win)

    if ACTIVE_TOOL == 'eraser':
        figure.eraser_button.draw_button(surf_for_draw[1].surface)
    surf_for_draw[1].draw_to_surface(win)
    for i in buttons['change_size'].values():
        win.blit(i.surf, i.rect)



def draw_upper_block():
    button.update_size_buttons(surf_for_draw, active_size_order, changing_size_order, ACTIVE_TOOL)
    pygame.draw.rect(win, color['upper_block'], (0, 0, win.get_width(), win.get_height()//9))
    main_size_picker.draw_button(win)
    if size_picker_stage == 2:
        surf_for_draw[3].draw_to_surface(win)
    
    current_color_button.draw_button(win)
    
    [tool.draw_button(win) for tool in figure.TOOL_BUTTONS.values()]

    if CHANGE_COLOR:
        surf_for_draw[4].draw_to_surface(win)

def draw_dashed_border(x1, y1, x2, y2, color):
    for i in range(y1+1, y2, 3):
        pygame.draw.line(win, color, (x1, i), (x1, i+1), 1)
        pygame.draw.line(win, color, (x2, i), (x2, i+1), 1)
    for i in range(x1+1, x2, 3): 
        pygame.draw.line(win, color, (i, y1), (i+1, y1), 1)
        pygame.draw.line(win, color, (i, y2), (i+1, y2), 1)


class SURFACE:
    def __init__(self, width, height, x, y, color, alpha = -1):
        self.w, self.h, self.x, self.y, self.color, self.alpha = width, height, x, y, color, alpha
        self.surface = pygame.Surface((self.w, self.h))
        self.surface = SURFACE.set_alpha(self, self.surface)
        self.surface.fill(color)
        self.rect = self.surface.get_rect(topleft=(self.x, self.y))
        
    def set_alpha(self, surf):
        if self.alpha>=0:
            surf.set_alpha(self.alpha)
        return surf
    def update_by_new_coord(self, dx, dy):
        self.w += dx - (self.w+self.x)
        self.h += dy - (self.h+self.y)
        self.w, self.h = max(1, self.w), max(1, self.h)

        new_surf = pygame.Surface((self.w, self.h))
        new_surf = SURFACE.set_alpha(self, new_surf)
        new_surf.fill(self.color)
        new_surf.blit(self.surface, (0,0))
        self.surface = new_surf
    
    def draw_to_surface(self, bg_surface):
        bg_surface.blit(self.surface, (self.x, self.y))


main_surface = SURFACE(int(w/1.4), int(h/1.5), 5, h//9+5, color['white'])
temporary_surface = SURFACE(int(w/1.4), int(h/1.5), 5, h//9+5, color['white'])
shadow_surface = SURFACE(int(w/1.4), int(h/1.5), 5+5, h//9+5+5, color['black'], 20)
border_size_choose_surface = SURFACE(200, 220, 700, 75, color['bg_size_picker'])
color_picker = SURFACE(330, 370, 800, 75, color['white'])
surf_for_draw = [main_surface, temporary_surface, shadow_surface, border_size_choose_surface, color_picker]

#prepare border_size_picker:
main_size_picker = button.BUTTON(70, 65, 700, 3)
def fill_size_picker(bg_color, border=False, border_color=None):
    button.fill_button(main_size_picker, border, bg_color, border_color)
    def size_picker_draw_line(x1, x2, y, width): pygame.draw.line(main_size_picker.surf, color['black'], (x1, y), (x2, y), width)
    size_picker_draw_line(13, 53, 5, 1) 
    size_picker_draw_line(13, 53, 12, 2)
    size_picker_draw_line(13, 53, 20, 3)
    size_picker_draw_line(13, 53, 29, 8)
    font = pygame.font.SysFont('cambriamath', 22)
    text = font.render('Width', True, color['black'])
    main_size_picker.surf.blit(text, (5, 40))

fill_size_picker(color['upper_block'])
size_picker_stage = 0
# 0 - nothing
# 1 - cursor on button
# 2 - open surface for choosing/clicked

active_size_order = 0
changing_size_order = -1
ACTIVE_SIZE = 1

# initial coord for working surface:
def get_sz_button_changing_size():
    return [surf_for_draw[1].x + surf_for_draw[1].w, surf_for_draw[1].y + surf_for_draw[1].h] #get bottom right corner

sz = get_sz_button_changing_size()

buttons = {
    'change_size' : {
        'diagonal' : button.BUTTON(5,5, sz[0], sz[1]),
        'right' : button.BUTTON(5,5, sz[0], sz[1]-surf_for_draw[1].h//2),
        'bottom' : button.BUTTON(5,5, sz[0]-surf_for_draw[1].w//2, sz[1])
    }
}
[button.fill_button(i, True) for i in buttons['change_size'].values()]

#FIGURE:
current_figure = None
change_figure_bottom = figure.change_figure_bottom
ACTIVE_TOOL = None

border_size = 1
stage_of_figure = -1
# stage -1 nit drawing figure
# stage = 0: none any figure chosed
# stage = 1: drawing figure
# stage = 2: figure drawed, waiting changing figure size by buttons
# stage = 3: changing size by buttons
# stage = 4: shift figure
# stage = 5: end, save the figure in main_surface
stage_4 = {
    'start_coord_figure':[],
    'start_coord_mine':[]
}

def accident_draw():
    global current_figure, stage_of_figure
    if current_figure != None: 
        current_figure.draw_figure(surf_for_draw[0].surface, current_color)
    current_figure = None
    stage_of_figure = 0

# PEN/ERASER:
x1 = y1 = x2 = y2 = 0
drawing_pen = drawing_eraser = False
def change_eraser_cursor(event):
    points = figure.from_win_to_working_surf_position(event, h)
    figure.eraser_button.update_size_coord_to_center(points[0], points[1], ACTIVE_SIZE)
    button.fill_button(figure.eraser_button, True)

def bfs_fill(origin_color, fill_color, x, y):
    if origin_color == fill_color: return
    queue = [(x, y)]
    surf_for_draw[0].surface.set_at((x, y), fill_color)
    def step(x, y):
        if x>=0 and y>=0 and x < surf_for_draw[0].w and y < surf_for_draw[0].h and surf_for_draw[0].surface.get_at((x, y)) == origin_color:
            surf_for_draw[0].surface.set_at((x, y), fill_color)
            queue.append((x, y))
    while len(queue) > 0:
        start = queue[0]
        queue.pop(0)
        step(start[0]+1, start[1])
        step(start[0]-1, start[1])
        step(start[0], start[1]+1)
        step(start[0], start[1]-1)
        

current_color = color['black']
current_color_button = button.BUTTON(70, 65, 800, 3)
def change_current_color_button(bg_color=color['upper_block'], border=False, border_color=color['black']):
    button.fill_button(current_color_button, border, bg_color, border_color)
    font = pygame.font.SysFont('cambriamath', 22)
    text = font.render('Color', True, color['black'])
    current_color_button.surf.blit(text, (8, 40))
    pygame.draw.rect(current_color_button.surf, current_color, (19, 5, 30, 30))
change_current_color_button()
CHANGE_COLOR = False
colorpicker.fill_surface(surf_for_draw[4].surface, current_color)



clock = pygame.time.Clock()
surf_change_by_diagonal = surf_change_by_right = surf_change_by_bottom = False
change_dx, change_dy = get_sz_button_changing_size()
run = True
# pygam  e.draw.rect(surf_for_draw[1].surface, (255,0,0), (800, 50, 60,60))
while run:
    win.fill(color['background'])
    surf_for_draw[1].surface.blit(surf_for_draw[0].surface, (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and buttons['change_size']['diagonal'].rect.collidepoint(event.pos):
                surf_change_by_diagonal = True
                accident_draw()
            elif event.button == 1 and buttons['change_size']['right'].rect.collidepoint(event.pos):
                surf_change_by_right = True
                accident_draw()
            elif event.button == 1 and buttons['change_size']['bottom'].rect.collidepoint(event.pos):
                surf_change_by_bottom = True
                accident_draw()
            if event.button == 1 and surf_for_draw[1].rect.collidepoint(event.pos) and stage_of_figure == 2:
                figure.null()
                figure.check_for_figure_button(event, current_figure, h)
                change_figure_bottom = figure.change_figure_bottom
                points = figure.from_win_to_working_surf_position(event, h)
                if not any([i for i in change_figure_bottom.values()]):
                    if current_figure != None and current_figure.rect.collidepoint(points): #points
                        stage_of_figure = 4
                        stage_4['start_coord_figure'] = [current_figure.x, current_figure.y]
                        stage_4['start_coord_mine'] = list(event.pos)
                    else:
                        stage_of_figure = 5
                else:
                    if current_figure != None: #points
                        stage_of_figure = 3
                        if ACTIVE_TOOL == 'rectangle':
                            current_figure.startx = current_figure.x
                            current_figure.starty = current_figure.y
                        if ACTIVE_TOOL == 'circle':
                            current_figure.startx = current_figure.x - current_figure.r
                            current_figure.starty = current_figure.y - current_figure.r
                            current_figure.endx = current_figure.x + current_figure.r
                            current_figure.endy = current_figure.y + current_figure.r
                        current_figure.points_tl_tr_bl_br()
            if event.button == 1 and surf_for_draw[1].rect.collidepoint(event.pos) and stage_of_figure%5 == 0 and not (surf_change_by_diagonal or surf_change_by_right or surf_change_by_bottom or CHANGE_COLOR):
                if current_figure != None: accident_draw()
                stage_of_figure = 1
                start_x, start_y = figure.from_win_to_working_surf_position(event, h)
                if ACTIVE_TOOL == 'rectangle': 
                    current_figure = figure.FIGURE(ACTIVE_TOOL, 1, 1, start_x, start_y, 0, ACTIVE_SIZE)
                elif ACTIVE_TOOL == 'circle':
                    current_figure = figure.FIGURE(ACTIVE_TOOL, 0, 0, start_x, start_y, 1, ACTIVE_SIZE)
            if event.button == 1 and main_size_picker.rect.collidepoint(event.pos) and size_picker_stage!=2:
                size_picker_stage = 2
                fill_size_picker(color['picked_button'], True, color['picked_button_border'])
            elif event.button == 1 and size_picker_stage==2:
                if main_size_picker.rect.collidepoint(event.pos):
                    fill_size_picker(color['in_button'], True, color['in_button_border'])
                    size_picker_stage = 1
                elif surf_for_draw[3].rect.collidepoint(event.pos):
                    
                    fill_size_picker(color['upper_block'])
                    size_picker_stage = 0

                    # active = changing / change size of width:
                    points = list(event.pos)
                    points[0] -= surf_for_draw[3].x
                    points[1] -= surf_for_draw[3].y
                    if button.buttons_changing_size[0].rect.collidepoint(points):
                        active_size_order = changing_size_order
                    elif button.buttons_changing_size[1].rect.collidepoint(points):
                        active_size_order = changing_size_order
                    elif button.buttons_changing_size[2].rect.collidepoint(points):
                        active_size_order = changing_size_order
                    elif button.buttons_changing_size[3].rect.collidepoint(points):
                        active_size_order = changing_size_order
                    changing_size_order = -1
                    ACTIVE_SIZE = button.determine_size_by_order(active_size_order, ACTIVE_TOOL)
                    if current_figure!= None and current_figure.border_size != ACTIVE_SIZE and ACTIVE_SIZE != None:
                        current_figure.border_size = ACTIVE_SIZE
                else:
                    fill_size_picker(color['upper_block'])
                    size_picker_stage = 0

            # TOOL CHOOSE:
            check_type = figure.check_for_collision(event.pos)
            if check_type != None:
                figure.update_all()
                if check_type == ACTIVE_TOOL:
                    ACTIVE_TOOL = None
                else:
                    ACTIVE_TOOL = check_type
                    if ACTIVE_TOOL == 'pen': 
                        button.change_for_pen()
                    elif ACTIVE_TOOL == 'eraser': 
                        button.change_for_eraser()
                    else: 
                        button.change_for_figures()
                    ACTIVE_SIZE = button.determine_size_by_order(active_size_order , ACTIVE_TOOL)
                    button.fill_button(figure.TOOL_BUTTONS[ACTIVE_TOOL], True, color['picked_button'], color['picked_button_border'])
                    figure.update_by_Active_tool(ACTIVE_TOOL)
                    accident_draw()
                #Or: ACTIVE_TOOL = check_type
                    # figure.update_all()
                    # button.fill_button(figure.TOOL_BUTTONS[ACTIVE_TOOL], True, color['picked_button'], color['picked_button_border'])
                    # figure.update_by_Active_tool(ACTIVE_TOOL)
                    # accident_draw()
            # Start drawig with pen or eraser
            if event.button == 1 and (ACTIVE_TOOL == 'pen' or ACTIVE_TOOL == 'eraser') and not (surf_change_by_diagonal or surf_change_by_right or surf_change_by_bottom):
                if ACTIVE_TOOL == 'pen': drawing_pen = True
                elif ACTIVE_TOOL == 'eraser': drawing_eraser = True
                x1, y1 = figure.from_win_to_working_surf_position(event, h)
                x2 = x1
                y2 = y1
            
            # DRAW FIGURE TO MAIN SURFACE:
            if stage_of_figure == 5 and not size_picker_stage==2 and not CHANGE_COLOR:
                if not_dots(): 
                    current_figure.draw_figure(surf_for_draw[0].surface, current_color)
                current_figure = None
                stage_of_figure = 0
            #Fill:
            if event.button == 1 and ACTIVE_TOOL == 'fill' and not CHANGE_COLOR:
                if surf_for_draw[0].rect.collidepoint(event.pos):
                    points = figure.from_win_to_working_surf_position(event, h)
                    origin_color = surf_for_draw[0].surface.get_at(points)
                    bfs_fill(origin_color, current_color, points[0], points[1])
            # COLOR change:
            if event.button == 1 and current_color_button.check_colision(event.pos):
                if not CHANGE_COLOR:
                    change_current_color_button(color['picked_button'], True, color['picked_button_border'])
                else:
                    change_current_color_button(color['in_button'], True, color['in_button_border'])
                CHANGE_COLOR = not CHANGE_COLOR
            if event.button == 1 and CHANGE_COLOR and not (surf_for_draw[4].rect.collidepoint(event.pos) or current_color_button.check_colision(event.pos)):
                CHANGE_COLOR = False
        if event.type == pygame.MOUSEMOTION:
            # NOT CHANGE, please
            if surf_change_by_diagonal:
                change_dx = event.pos[0]
                change_dy = event.pos[1]
                buttons['change_size']['diagonal'].update(change_dx, change_dy)
            elif surf_change_by_right:
                change_dx = event.pos[0]
                buttons['change_size']['right'].update(change_dx, buttons['change_size']['right'].y)
            elif surf_change_by_bottom:
                change_dy = event.pos[1]
                buttons['change_size']['bottom'].update(buttons['change_size']['bottom'].x, change_dy)
            elif stage_of_figure == 1 and current_figure != None:
                surf_for_draw[1].surface.blit(surf_for_draw[0].surface, (0, 0))
                position = figure.from_win_to_working_surf_position(event, h)
                current_figure.update_by_start(position[0], position[1])
                current_figure.update_surf_rect()
            elif stage_of_figure == 3:
                surf_for_draw[1].surface.blit(surf_for_draw[0].surface, (0, 0))
                points = figure.from_win_to_working_surf_position(event, h)
                current_figure = figure.change_figure_by_buttom(current_figure, points)
            elif stage_of_figure == 4:
                surf_for_draw[1].surface.blit(surf_for_draw[0].surface, (0, 0))
                dx, dy = event.pos[0] - stage_4['start_coord_mine'][0], event.pos[1] - stage_4['start_coord_mine'][1]
                if ACTIVE_TOOL == 'rectangle':
                    current_figure.startx = current_figure.x = stage_4['start_coord_figure'][0] + dx
                    current_figure.starty = current_figure.y = stage_4['start_coord_figure'][1] + dy
                if ACTIVE_TOOL == 'circle':
                    current_figure.x = stage_4['start_coord_figure'][0] + dx
                    current_figure.y = stage_4['start_coord_figure'][1] + dy
                    current_figure.startx = current_figure.x - current_figure.r
                    current_figure.starty = current_figure.y - current_figure.r
                    current_figure.endx = current_figure.x + current_figure.r
                    current_figure.endy = current_figure.y + current_figure.r
                current_figure.update_surf_rect()
            # SIZE PICKER:
            if size_picker_stage == 0 and main_size_picker.check_colision(event.pos):
                fill_size_picker(color['in_button'], True, color['in_button_border'])
                size_picker_stage = 1
            elif size_picker_stage == 1 and not main_size_picker.check_colision(event.pos):
                fill_size_picker(color['upper_block'])
                size_picker_stage = 0
            elif size_picker_stage == 2:
                points = list(event.pos)
                points[0] -= surf_for_draw[3].x
                points[1] -= surf_for_draw[3].y
                if button.buttons_changing_size[0].rect.collidepoint(points):
                    changing_size_order = 0
                elif button.buttons_changing_size[1].rect.collidepoint(points):
                    changing_size_order = 1
                elif button.buttons_changing_size[2].rect.collidepoint(points):
                    changing_size_order = 2
                elif button.buttons_changing_size[3].rect.collidepoint(points):
                    changing_size_order = 3
                else:
                    changing_size_order = -1
                if changing_size_order != -1 and ACTIVE_TOOL != 'pen' and ACTIVE_TOOL != 'eraser':
                    ACTIVE_SIZE = button.determine_size_by_order(changing_size_order , ACTIVE_TOOL)
                
                if current_figure!= None and current_figure.border_size != ACTIVE_SIZE and ACTIVE_SIZE != None:
                    current_figure.border_size = ACTIVE_SIZE
            # DRAWING PEN:
            if drawing_pen or drawing_eraser:
                x1, y1 = x2, y2
                x2, y2 = figure.from_win_to_working_surf_position(event, h)
                if drawing_pen: pygame.draw.line(surf_for_draw[0].surface, current_color, (x1, y1), (x2, y2), ACTIVE_SIZE)
                if drawing_eraser: pygame.draw.line(surf_for_draw[0].surface, color['white'], (x1, y1), (x2, y2), ACTIVE_SIZE)
            if ACTIVE_TOOL == 'eraser':
                change_eraser_cursor(event)
            # TOOL, LOOKING FOR:
            figure.change_by_collision(event.pos, ACTIVE_TOOL)
            # COLOR, For looking:
            if not CHANGE_COLOR and current_color_button.check_colision(event.pos):
                change_current_color_button(color['in_button'], True, color['in_button_border'])
            elif not CHANGE_COLOR:
                change_current_color_button()
            if CHANGE_COLOR and surf_for_draw[4].rect.collidepoint(event.pos):
                # colorpicker.cp.update()
                # colorpicker.cp.draw(surf_for_draw[4].surface)
                colorpicker.fill_surface(surf_for_draw[4].surface, current_color)
                colorpicker.cp.draw(surf_for_draw[4].surface)
                points = list(event.pos)
                points[0] -= surf_for_draw[4].x
                points[1] -= surf_for_draw[4].y
                if colorpicker.pallete_rect.collidepoint(points) and pygame.mouse.get_pressed()[0]:
                    colorpicker.fill_surface(surf_for_draw[4].surface, current_color) # avoid contact with cursor
                    current_color = surf_for_draw[4].surface.get_at(points)
                    change_current_color_button(color['picked_button'], True, color['picked_button_border'])
                    colorpicker.fill_surface(surf_for_draw[4].surface, current_color)
                    colorpicker.cursor(surf_for_draw[4].surface, points[0], points[1])
                
        if event.type == pygame.MOUSEBUTTONUP:
            if surf_change_by_diagonal or surf_change_by_right or surf_change_by_bottom:
                [surf_for_draw[i].update_by_new_coord(change_dx, change_dy) for i in range(2)]
                surf_for_draw[2].update_by_new_coord(change_dx+5, change_dy+5) 
                sz = get_sz_button_changing_size()
                buttons['change_size']['diagonal'].update(sz[0], sz[1])
                buttons['change_size']['right'].update(sz[0], sz[1]-surf_for_draw[1].h//2) # DON't CHANGE
                buttons['change_size']['bottom'].update(sz[0]-surf_for_draw[1].w//2, sz[1])
                surf_change_by_diagonal = surf_change_by_right = surf_change_by_bottom = False
            if stage_of_figure == 1 or stage_of_figure == 3:
                stage_of_figure = 2
            if stage_of_figure == 4:
                stage_of_figure = 2
            if drawing_pen:
                drawing_pen = False
            if drawing_eraser:
                drawing_eraser = False

    draw_working_surface()
    if surf_change_by_diagonal or surf_change_by_right or surf_change_by_bottom: #draw buttons for changing size of working window
        draw_dashed_border(surf_for_draw[1].x, surf_for_draw[1].y, change_dx, change_dy, color['l-black'])
    draw_upper_block()
    pygame.display.update()
    clock.tick(60)
pygame.quit()