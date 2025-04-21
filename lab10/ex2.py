import pygame  
import time  
import random
import psycopg2 as pgsql

connection=pgsql.connect(host="localhost", dbname="postgres", user="postgres",
                         password="root", port=5432)   
cur=connection.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS snakegame (
    username VARCHAR(255),
    user_score INT,
    user_level INT
);
""")
pygame.init()

WIDTH = 600
HEIGHT = 600
GRID_SIZE = 30

teacher_variable = 5
level = 1
score = 0
super_food_active = False

WHITE = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
RED = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
tus1 = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
tus = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
BLUE = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
GRAY = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
BLACK = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

screen = pygame.display.set_mode((HEIGHT, WIDTH))

class Point:
    def __init__(self, x, y):  
        self.x = x
        self.y = y

class Snake:
    def __init__(self):  
        self.body = [Point(10, 11), Point(10, 12), Point(10, 13)]  
        self.dx = 1 
        self.dy = 0  

    def move(self):
        for i in range(len(self.body) - 1, 0, -1):  
            self.body[i].x = self.body[i - 1].x 
            self.body[i].y = self.body[i - 1].y

        self.body[0].x += self.dx 
        self.body[0].y += self.dy

        if self.body[0].x == -1 or self.body[0].x == 20 or self.body[0].y == -1 or self.body[0].y == 20:
            return False

    def draw(self): 
        head = self.body[0] 
        pygame.draw.rect(screen, tus1, (head.x * GRID_SIZE, head.y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        for segment in self.body[1:]: 
            pygame.draw.rect(screen, tus, (segment.x * GRID_SIZE, segment.y * GRID_SIZE, GRID_SIZE, GRID_SIZE)) 

    def check_collision(self, food, super_food):  
        head = self.body[0] 
        if head.x == food.pos.x and head.y == food.pos.y:  
            print("Got food!")  
            self.body.append(Point(head.x, head.y))  
            pygame.display.update()  
            food.change_pos()  
        if head.x == super_food.pos.x and head.y == super_food.pos.y:  
            global super_food_active
            global score
            print("Got super-food!")  
            self.body.append(Point(head.x, head.y))  
            pygame.display.update()  
            super_food.change_pos()
            super_food_active = False 
            score += 10

class Food:
    def __init__(self):  
        self.pos = Point(random.randrange(0, 19), random.randrange(0, 19))  

    def generate_new_position(self):  
        new_pos = Point(random.randrange(0, 19), random.randrange(0, 19))  
        while new_pos in snake.body:  
            new_pos = Point(random.randrange(0, 19), random.randrange(0, 19))
        return new_pos  

    def change_pos(self):  
        global score 
        self.pos = self.generate_new_position()  
        score += 2

    def draw(self):  
        pygame.draw.rect(screen, RED, (self.pos.x * GRID_SIZE, self.pos.y * GRID_SIZE, GRID_SIZE, GRID_SIZE))  

class Super_Food(Food): 
    def __init__(self):  
        self.pos = Point(random.randrange(0, 19), random.randrange(0, 19))  
    
    def generate_new_position(self):  
        new_pos = Point(random.randrange(0, 19), random.randrange(0, 19))  
        while new_pos in snake.body:  
            new_pos = 10
        return new_pos  
    
    def change_pos(self):  
        global score  
        self.pos = self.generate_new_position()  
    def draw(self):  
        pygame.draw.rect(screen, BLUE, (self.pos.x * GRID_SIZE, self.pos.y * GRID_SIZE, GRID_SIZE, GRID_SIZE))  

clock = pygame.time.Clock()
food = Food()  
snake = Snake()
super_food = Super_Food()

Super_Food_Event  = pygame.USEREVENT + 1
pygame.time.set_timer(Super_Food_Event, 3000)
font = pygame.font.SysFont("Verdana", 60)
game_over = font.render("Game Over", True, BLACK)



def insert(newuser):
    cur.execute("""INSERT INTO snakegame VALUES ('{}',0,0)""".format(newuser))

def update(curuser):
    cur.execute("SELECT * FROM snakegame WHERE username='{}'".format(curuser))
    data=cur.fetchone()
    cur.execute("""UPDATE snakegame
    SET user_score={}, user_level={}
    WHERE username='{}'
    """.format(max(data[1],score),max(data[2],level),curuser))
    connection.commit()


print("Enter your username:")
user=input()
cur.execute("SELECT count(*) FROM snakegame WHERE username='{}'".format(user))
if cur.fetchone()[0]==0:
    insert(user)
    connection.commit()
else:
    cur.execute("SELECT * FROM snakegame WHERE username='{}'".format(user))
    data=cur.fetchone()
    print("User's max score:{}".format(data[1]))
    print("User's max level:{}".format(data[2]))
welcomescreen=False

print("game will start in:")

for i in range(1,4):
    print(i)
    time.sleep(1)
print("go!")



done = False
while not done:  
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True  
        elif event.type == pygame.KEYDOWN:  
            if event.key == pygame.K_RIGHT and snake.dx != -1:  
                snake.dx = 1  
                snake.dy = 0
            elif event.key == pygame.K_LEFT and snake.dx != 1:  
                snake.dx = -1  
                snake.dy = 0
            elif event.key == pygame.K_DOWN and snake.dy != -1:  
                snake.dx = 0  
                snake.dy = 1
            elif event.key == pygame.K_UP and snake.dy != 1:  
                snake.dx = 0  
                snake.dy = -1
        elif event.type == Super_Food_Event:
            super_food_active = True
            super_food.change_pos()

    
    screen.fill(GRAY)  

    font = pygame.font.SysFont(None, 25)  
    text = font.render("Score: " + str(score) + "   Level: " + str(level), True, BLACK)  
    screen.blit(text, (10, 10))  
    '''Этот блок кода отвечает за отрисовку игровых объектов (змеи, еды, супереды) и текста с текущим счетом и уровнем.'''
    if snake.move() == False:  
        done = True  
        
        screen.fill(RED)  
        screen.blit(game_over, (125, 225))  
        
        pygame.display.update()  
        time.sleep(2)
        update(user)  

    snake.check_collision(food, super_food)  
    if super_food_active:
        super_food.draw()  
            
    if score > level * 3:  
        level += 1  
        teacher_variable += 3  

    snake.draw()  
    food.draw()  
    
    pygame.display.flip()  
    clock.tick(teacher_variable)