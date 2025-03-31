import os

import pygame, json, random
base_dir = os.path.dirname(os.path.abspath(__file__))  # Get script's directory
file_path = os.path.join(base_dir, 'color.json')
with open(file_path) as f:
    color = json.loads(f.read())

class Point:
    def __init__(self, x, y, timer = 0, cost = 0, add_speed=0): # positions, timer and cost for Foods, also additional speed effect
        self.x = x
        self.y = y
        self.timer = timer
        self.cost = cost
        self.add_speed = add_speed
    def __str__(self):
        return f"point: x = {self.x}, y = {self.y}, timer = {self.timer}, cost = {self.cost})"

class GameObject:
    def __init__(self, points, color, tide_width):
        self.points = points
        self.color = color
        self.tide_width = tide_width
    def draw(self, surface):
        # Every point is the rectangle
        for point in self.points:
            pygame.draw.rect(surface, self.color, (point.x, point.y, self.tide_width, self.tide_width))
            pygame.draw.rect(surface, (0,0,0), (point.x, point.y, self.tide_width, self.tide_width), 1)
    # Take random point from free points(not occupied ones)
    def get_Random_point(self, occupied_points):
        all_possible = []
        for i in range(20):
            for j in range(20):
                possible_point = Point(j*20, i*20)
                # check if this point in occupied points
                for point in occupied_points:
                    if point.x == possible_point.x and point.y == possible_point.y:
                        possible_point = None
                        break
                if possible_point != None:
                    all_possible.append(possible_point)
                # second way:
                # check = [True for point in occupied_points if point.x == possible_point.x and point.y == possible_point.y]
                # if not any(check):
                #     all_possible.append(possible_point)
        return random.choice(all_possible)

class Player(GameObject):
    def __init__(self, occupied_points):
        random_point = self.get_Random_point(occupied_points) # get random point for player initial position
        GameObject.__init__(self, [random_point], color['blue'], 20)
        # game starts without any motion of snake
        self.dx = 0
        self.dy = 0
    def move(self, w, h):
        #temporary head
        temporary_x = self.points[0].x+self.dx*self.tide_width
        temporary_y = self.points[0].y+self.dy*self.tide_width
        # if bumped to window:
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
            # check if head is bumping with its body
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
        # draw head with another color:
        pygame.draw.rect(surface, color['head'], (self.points[0].x, self.points[0].y, self.tide_width, self.tide_width))
        pygame.draw.rect(surface, (0,0,0), (self.points[0].x, self.points[0].y, self.tide_width, self.tide_width), 1)

count = 0
class Food(GameObject):
    def __init__(self, occupied_points):
        GameObject.__init__(self,self.create_some_food(occupied_points), color['green'], 20)
    def create_some_food(self, occupied_points):
        self.points = []
        # Exactly n apples in window. Timer random: 30-50. Cost random: 2-7. Additional Speed: 4-6 or 0
        while len(self.points) <= 4:
            point = self.get_Random_point(occupied_points + self.points)
            point = Point(point.x, point.y, random.randint(30, 50), random.randint(2,7), random.randint(0, 1) * random.randint(4, 6))
            self.points += [point]
        return self.points

    def can_eat(self, point, occupied_points):
        # if head bumping with one of foods:
        for i in self.points:
            if i.x == point.x and i.y == point.y: 
                # remove current food, add new one
                self.points.append(self.create_one_more(occupied_points))
                self.points.remove(i)
                return [True, i.cost, i.add_speed] 
        return [False, 0, 0]
    def draw(self, surface):
        for point in self.points:
            # as timer lower, size of apple also lower
            narrow = (50 - point.timer)//5 
            x = point.x + narrow
            y = point.y + narrow
            food_color = self.color # different color to foods with additional speed effect
            if point.add_speed != 0:
                food_color = color['b-green']
            pygame.draw.rect(surface, food_color, (x, y, self.tide_width - 2*narrow, self.tide_width- 2*narrow))
            pygame.draw.rect(surface, (0,0,0), (x, y, self.tide_width-2*narrow, self.tide_width-2*narrow), 1)
            # add cost under rectangle
            font = pygame.font.SysFont('cambria', 20)
            text = font.render(f'{point.cost}', True, color['black'])
            surface.blit(text, text.get_rect(center = (point.x+9, point.y+10)))
    def change_timer(self, occupied_points):
        new_points = []
        for point in self.points:
            point.timer -= 1
            # add onlt points which timer>5, otherwise create new ones
            if point.timer > 5:
                new_points.append(point)
            else:
                new_points.append(self.create_one_more(occupied_points))
        self.points = new_points
    def create_one_more(self, occupied_points):
        # 
        point = self.get_Random_point(occupied_points + self.points)
        point.timer = random.randint(30, 50)
        point.cost = random.randint(2, 7)
        point.add_speed = random.randint(0, 1) * random.randint(1, 7)
        return point
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
            file_path = os.path.join(base_dir, 'levels',f'level{self.level}.txt')
            with open(file_path, 'r') as f:
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