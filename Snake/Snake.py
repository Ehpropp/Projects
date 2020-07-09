import pygame as py
import random as ran

py.init()
vertical = 600
horizontal = 810
screen = py.display.set_mode((horizontal,vertical))
clock = py.time.Clock()

#Initializing required variables
WHITE = (255,255,255)
BLUE = (0,0,255)
GREEN = (0,255,0)
RED = (255,0,0)
BLACK = (0,0,0)
food_list = []
colour_list = [(0,0,255)]
score = 0
bigger_font = py.font.SysFont('Arial', 75)
big_font = py.font.SysFont('Arial', 20)
med_font = py.font.SysFont('Arial', 15)
move_right = False
move_left = False
move_up = False
move_down = False
pause = 0

class PLAYER:     #Hold all player related functions
    def __init__(self):
        self.len, self.wid = 15, 15
        self.thick = 0
        self.x = 405
        self.y = 300
        self.store_position = [[self.x,self.y]]
        self.one_before_death = []

    def draw(self): #Draws the snake
        self.length = len(self.store_position)
        for i in range(0,len(self.store_position)):
            py.draw.rect(screen, colour_list[i], (self.store_position[i][0], self.store_position[i][1], self.len, self.wid), self.thick)

    def go(self, r, l, u, d): #Allows for movement and sets the boundaries to the walls
        self.r, self.l, self.u, self.d = r, l, u, d
        if self.r:
            self.x += self.len
        elif self.l:
            self.x -= self.len
        elif self.u:
            self.y -= self.len
        elif self.d:
            self.y += self.len
        self.one_before_death = self.store_position
        self.store_position.insert(0, [self.x, self.y])
        del self.store_position[len(self.store_position) - 1]
        print(self.store_position)

    def add_tail(self):
        # adds the first tail piece - will explain below why needs to be separate if statement (basically bc nothing to calculate delta with).
        # Can't do this method to add all tail pieces bc the snake will bend when it's longer and it's turning and head may be travelling right but it should add a tail
        # under to make it look smooth
        if self.length < 2:
            if self.r:
                snake.store_position.append([self.store_position[self.length - 1][0] - snake.len, self.store_position[self.length - 1][1]])
            elif self.l:
                snake.store_position.append([self.store_position[self.length - 1][0] + snake.len, self.store_position[self.length - 1][1]])
            elif self.u:
                snake.store_position.append([self.store_position[self.length - 1][0], self.store_position[self.length - 1][1] - snake.len])
            elif self.d:
                snake.store_position.append([self.store_position[self.length - 1][0], self.store_position[self.length - 1][1] + snake.len])
        #Gets the delta x and y of the the 2nd last and last peice of the snake. It will always be the length of the snake, but what makes it work is the +/- sign that comes from it
        #the plus or minus sign will have the new tail piece added in the right position relative to the snake
        elif self.length >= 2:
            delta_x = self.store_position[self.length-2][0] - self.store_position[self.length-1][0]
            delta_y = self.store_position[self.length-2][1] - self.store_position[self.length-1][1]
            snake.store_position.append([self.store_position[-1][0]-delta_x,self.store_position[-1][1]-delta_y])
            print(self.store_position)  # For debugging

    def check_death(self):
        for i in range(1,self.length):
            if self.store_position[0][0] == self.store_position[i][0] and self.store_position[0][1] == self.store_position[i][1]:
                # print(self.r, self.l, self.u, self.d)
                return True
        if self.store_position[0][0] >= horizontal or self.store_position[0][0] < 0:
            return True
        elif self.store_position[0][1] >= vertical or self.store_position[0][1] < 0:
            return True
        else:
            return False

    def dead(self):
        game_over = bigger_font.render("You Died", 1, (0, 0, 0))
        self.game_over_width = game_over.get_width()
        self.game_over_height = game_over.get_height()
        self.start_text = horizontal / 2 - snake.game_over_width / 2
        self.end_text = horizontal / 2 + snake.game_over_width / 2
        screen.blit(game_over,(horizontal / 2 - self.game_over_width / 2, vertical / 2 - self.game_over_height / 2))

        mX, mY = py.mouse.get_pos()
        clicked = py.mouse.get_pressed()
        #Following 4 if statements change the colour of the button so the player knows he's about to click
        if mX > self.start_text and mX < self.start_text + 80 and mY > 350 and mY < 390:
            thicc1 = 0
        else:
            thicc1 = 2
        if mX > self.end_text - 80 and mX < self.end_text and mY > 350 and mY < 390:
            thicc2 = 0
        else:
            thicc2 = 2
        death_buttons(thicc1,thicc2)

        if clicked[0] == True: #This block will have the end game buttons do stuff
            if mX > self.start_text and mX < self.start_text + 80 and mY > 350 and mY < 390: #quits the game
                exit()
            elif mX > self.end_text - 80 and mX < self.end_text and mY > 350 and mY < 390: #restarts the game by resetting initial varibales
                global food_list, colour_list, score, death, move_right, move_left, move_up, move_down
                self.x, self.y = 405, 300
                self.store_position = [[self.x, self.y]]
                food_list = []
                colour_list = [(0,0,255)]
                move_right, move_left, move_up, move_down = False, False, False, False
                death = False
                score = 0


class FOOD: # Holds all food related functions
    def __init__(self): # Sets variables for the food - random location where they appear
        good = False
        while not good:
            x = ran.randrange(15, 685, snake.len)
            y = ran.randrange(15, 585, snake.wid)
            if [x,y] not in snake.store_position:
                good = True
        self.x = x
        self.y = y
        diff_colour = False
        while not diff_colour:
            self.colour = (ran.randint(0,255), ran.randint(0,255), ran.randint(0,255))
            for i in range(0, snake.length):
                if self.colour != colour_list[i]:
                    diff_colour = True
        colour_list.append(self.colour)
        self.thick = 0

    def draw(self): # Draws the food
        py.draw.rect(screen, self.colour, (self.x, self.y, snake.len, snake.wid), self.thick)

def fonts(): # Deals with different text sprites on the screens(creating and drawing) - makes it neater
    score_render = big_font.render("Score: " + str(score), 1, (0, 0, 0))
    score_width = score_render.get_width()
    screen.blit(score_render, (780 - score_width, 20))

def death_buttons(thick1, thick2):
    x_dim = 80
    y_dim = 40
    quit_render = big_font.render("Quit", 1, (0, 0, 0))
    quit_width = quit_render.get_width()
    screen.blit(quit_render, (snake.start_text + x_dim/2 - quit_width/2, 360))
    play_render = big_font.render("Restart", 1, (0, 0, 0))
    play_width = play_render.get_width()
    screen.blit(play_render, (snake.end_text - x_dim/2 - play_width/2, 360))
    py.draw.rect(screen, RED, (snake.start_text, 350, x_dim, y_dim), thick1)
    py.draw.rect(screen, BLUE, (snake.end_text - x_dim, 350, x_dim, y_dim), thick2)

snake = PLAYER()

running = True
while running:
    screen.fill(WHITE)
    frame_rate = clock.tick(15) # Sets the frame rate

    fonts()
    snake.draw()

    if food_list == []: # has a list with one item - food. Also created a new instance whenever the list is empty, which will make the new food appear in a new place
        food = FOOD()
        food_list.append(food)

    food_list[0].draw() #calls the functions food.draw() bc balls is the list value
    death = snake.check_death()
    if not death:
        snake.go(move_right, move_left, move_up, move_down)

    if snake.x == food.x and snake.y == food.y:
        del food_list[0]
        score += 1
        print("Eaten")
        snake.add_tail()

    if death:
        snake.dead()

    for event in py.event.get():
        if event.type == py.QUIT:
            running = False
        if event.type == py.KEYDOWN and death == False: # Control variables for movements which will get passed to snake.go() to control movement
            if event.key == py.K_RIGHT and not move_left:
                move_right = True
                move_left, move_up, move_down = False, False, False
            elif event.key == py.K_LEFT and not move_right:
                move_left = True
                move_right, move_up, move_down = False, False, False
            elif event.key == py.K_UP and not move_down:
                move_up = True
                move_right, move_left, move_down = False, False, False
            elif event.key == py.K_DOWN and not move_up:
                move_down = True
                move_right, move_left, move_up = False, False, False

    py.display.flip()

py.quit()
