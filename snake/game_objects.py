import os

import pygame, json, random
base_dir = os.path.dirname(os.path.abspath(__file__))  # Get script's directory
file_path = os.path.join(base_dir, 'color.json')
with open(file_path) as f:
    color = json.loads(f.read())

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __str__(self):
        return f'({self.x}, {self.y})'

class GameObject:
    def __init__(self, points, color, tide_width):
        self.points = points
        self.color = color
        self.tide_width = tide_width
    def draw(self, surface):
        for point in self.points:
            pygame.draw.rect(surface, self.color, (point.x, point.y, self.tide_width, self.tide_width))
            pygame.draw.rect(surface, (0,0,0), (point.x, point.y, self.tide_width, self.tide_width), 1)
    def get_Random_point(self, occupied_points):
        all_possible = []
        for i in range(20):
            for j in range(20):
                possible_point = Point(j*20, i*20)
                for point in occupied_points:
                    if point.x == possible_point.x and point.y == possible_point.y:
                        possible_point = None
                        break
                if possible_point != None:
                    all_possible.append(possible_point)
        return random.choice(all_possible)

class Player(GameObject):
    def __init__(self, occupied_points):
        print('oc:', occupied_points)
        random_point = self.get_Random_point(occupied_points)
        GameObject.__init__(self, [random_point], color['blue'], 20)
        self.dx = 0
        self.dy = 0
    def move(self, w, h):
        temporary_x = self.points[0].x+self.dx*self.tide_width
        temporary_y = self.points[0].y+self.dy*self.tide_width
        if temporary_x < 0:
            return 'left_collide'
        if temporary_y < 0:
            return 'up_collide'
        if temporary_x >= w:
            return 'right_collide'
        if temporary_y >= h: 
            return 'down_collide'
        temporary_points_list = self.points.copy()
        for i in range(len(self.points)-1, 0, -1):
            temporary_points_list[i].x = self.points[i-1].x
            temporary_points_list[i].y = self.points[i-1].y
            if temporary_x == temporary_points_list[i].x and temporary_y == temporary_points_list[i].y:
                if self.dx == 1:
                    return 'right_collide'
                elif self.dx == -1:
                    return 'left_collide'
                if self.dy == 1:
                    return 'down_collide'
                elif self.dy == -1:
                    return 'up_collide'
        self.points = temporary_points_list.copy()
        self.points[0].x = temporary_x
        self.points[0].y = temporary_y
        return None
    def add(self, point):
        self.points.append(Point(point.x, point.y))
    def process_input(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.dy = -1
                    self.dx = 0
                elif event.key == pygame.K_DOWN:
                    self.dy = 1
                    self.dx = 0
                elif event.key == pygame.K_RIGHT:
                    self.dx = 1
                    self.dy = 0
                elif event.key == pygame.K_LEFT:
                    self.dx = -1
                    self.dy = 0

    def draw(self, surface):
        GameObject.draw(self, surface)
        pygame.draw.rect(surface, color['head'], (self.points[0].x, self.points[0].y, self.tide_width, self.tide_width))
        pygame.draw.rect(surface, (0,0,0), (self.points[0].x, self.points[0].y, self.tide_width, self.tide_width), 1)


class Food(GameObject):
    def __init__(self, occupied_points):
        initial_point = self.get_Random_point(occupied_points)
        GameObject.__init__(self, [initial_point], color['green'], 20)
    def can_eat(self, point):
        for i in self.points:
            if i.x == point.x and i.y == point.y: return True
        return False
    def change_pos(self, occupied_points):
        occupied_points.append(self.points[0])
        self.points[0] = self.get_Random_point(occupied_points)

    
class Wall(GameObject):
    def __init__(self, level=1):
        self.level = level
        self.points = self.take_level()
        GameObject.__init__(self, self.points, color['wall'], 20)
    def take_level(self):
        level_txt = []
        points = []
        if self.level == 4:
            while len(points) < 6:
                points.append(self.get_Random_point(points))
        else:

            file_path = os.path.join(base_dir,"levels", f'level{self.level}.txt')
            with open(file_path) as f:
                for i in f.readlines(): level_txt.append(i)
            for i in range(20):
                for j in range(20):
                    if level_txt[i][j] == '#':
                        points.append(Point(j*20, i*20))
        return points
    def can_go(self, point, dx, dy):
        temporaty_point = Point(point.x, point.y)
        temporaty_point.x += dx*self.tide_width
        temporaty_point.y += dy*self.tide_width
        for i in self.points:
            if i.x == temporaty_point.x and i.y == temporaty_point.y:
                if dx == 1:
                    return 'right_collide'
                elif dx == -1:
                    return 'left_collide'
                if dy == 1:
                    return 'down_collide'
                elif dy == -1:
                    return 'up_collide'

        return None