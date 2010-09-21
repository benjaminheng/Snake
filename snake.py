#! /usr/bin/env python

import pygame
import random
import sys


def startGame(width, height, wTitle):
    pygame.init()
    pygame.font.init()
    random.seed()
    global screen
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(wTitle)
    global clock
    clock = pygame.time.Clock()

def text(intext, size, inx, iny, color):
    font = pygame.font.Font(None, size)
    text = font.render((intext), 0, color)
    if inx == -1:
        x = width/2
    else:
        x = inx
    if iny == -1:
        y = height/2
    else:
        y = iny
    textpos = text.get_rect(centerx = x, centery = y)
    screen.blit(text, textpos)

class snake:
    def __init__(self, x, y, color=(0, 255, 0), pixels=None):
        self.x = x
        self.y = y
        self.hdir = 0
        self.vdir = -10
        if pixels == None:
            self.pixels = [(x, y)]
        else:
            self.pixels = pixels
        self.color = color
        self.crash = False
        self.length = 7

    def events(self, event):
        if (event.key == pygame.K_UP or event.key == pygame.K_w) and self.vdir != 10:
            self.hdir = 0
            self.vdir = -10
        elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and self.vdir != -10:
            self.hdir = 0
            self.vdir = 10
        elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and self.hdir != 10:
            self.hdir = -10
            self.vdir = 0
        elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and self.hdir != -10:
            self.hdir = 10
            self.vdir = 0

    def move(self, otherSnake=None):
        self.x += self.hdir
        self.y += self.vdir

        if (self.x, self.y) in self.pixels:
            self.crash = True
        # Checks if another snake exists.
        elif otherSnake and (self.x, self.y) in otherSnake.pixels:
            self.crash = True
        
        # Wraps the snake
        if self.x < 0:
            self.x = width-10
        elif self.x >= width:
            self.x = 0
        elif self.y <= 0:
            self.y = height-20
        elif self.y >= height-10:
            self.y = 10
            
        self.pixels.insert(0, (self.x, self.y))

        if len(self.pixels) > self.length:
            del self.pixels[self.length]
        
    def draw(self):
        for x, y in self.pixels:
            pygame.draw.rect(screen, self.color, (x, y+10, 10, 10), 1)

class food():
    def __init__(self):
        self.x = random.randrange(20, width - 20, 10)
        self.y = random.randrange(20, height - 20, 10)

    def hitCheck(self, snakePixels):
        if snakePixels[0][0] == self.x and snakePixels[0][1] == self.y:
            return True

    def relocate(self):
        self.x = random.randrange(20, width - 20, 10)
        self.y = random.randrange(20, height - 20, 10)

    def draw(self):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y+10, 10, 10), 0)
        
        
def pause():
    loop = True
    while loop:
        text("Paused", 30, -1, height/2+30, (255, 255, 255))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                loop = False
    del loop
            
# Allows user to select singleplayer or multiplayer modes
def playerSelect():
    loop = True
    while loop:
        text("1-player: Press 1", 30, -1, height/2+30, (255, 255, 255))
        text("2-players: Press 2", 30, -1, height/2+10, (255, 255, 255))
        pygame.display.flip()
        clock.tick(50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                snake.crash = False
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_2:
                    return True
                    loop = False
                if event.key == pygame.K_1:
                    return False
                    loop = False
    del loop


running = True
wTitle = "Snake!"
score = 0
highscore = 0 # Will eventually use a local file to log highscores
newHighscore = False
twoPlayers = False
arrowKeys = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]
wasdKeys = [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]
p1Color = (210, 130, 197) # Pink - WASD
p2Color = (0, 255, 0) # Green - Arrow Keys
width = 600
height = 600
speed = 25 # lower = slower

startGame(width, height, wTitle)
    
twoPlayers = playerSelect()

if twoPlayers:
    snake1 = snake(0+130, height/2, p1Color)
    snake2 = snake(width-140, height/2, p2Color)
else:
    snake1 = snake(width/2, height/2)
    
food = food()

while running:
    screen.fill((0, 0, 0))

    if twoPlayers:
        snake1.move(snake2)
        snake2.move(snake1)
        snake2.draw()
    else:
        snake1.move()
    snake1.draw()
    food.draw()
    
    if food.hitCheck(snake1.pixels):
        food.relocate()
        if not twoPlayers:
            score = score + 10
        snake1.length = snake1.length + 7
    elif twoPlayers and food.hitCheck(snake2.pixels):
        food.relocate()
        snake2.length = snake2.length + 7
        
    if not twoPlayers:
        text("Score: " + str(score), 16, width/2-50, 10, (255, 255, 255))
        if score > highscore:
            highscore = score
            newHighscore = True
        text("Highscore: " + str(highscore), 16, width/2+50, 10, (255, 255, 255))
    else:
        text("Player 1: Pink", 16, width/2-50, 10, p1Color)
        text("Player 2: Green", 16, width/2+50, 10, p2Color)
    
    
    
    # Checks for user input and perform the relevant actions.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if twoPlayers and event.key in arrowKeys:
                snake2.events(event)
            elif not twoPlayers and event.key in arrowKeys:
                snake1.events(event)
            elif event.key in wasdKeys:
                snake1.events(event)
            elif event.key == pygame.K_ESCAPE:
                pause()
            clock.tick(speed)
                
                
                
    # Updates the display at the end.
    pygame.display.flip()
    clock.tick(speed)
    
    while snake1.crash or (twoPlayers and snake2.crash):
        if not twoPlayers:
            if newHighscore:
                text("New Highscore", 30, -1, height/2-30, (30, 255, 30))
            text("Game Over, Score: " + str(score), 40, -1, -1, (255, 255, 255))
        else:
            if snake1.crash:
                text("Winner: Player 2! ", 40, -1, -1, p2Color)
            elif snake2.crash:
                text("Winner: Player 1! ", 40, -1, -1, p1Color)
        text("Press R to restart", 30, -1, height/2+30, (255, 255, 255))
        text("ESC to return to main menu", 20, -1, height/2+50, (255, 255, 255))
        pygame.display.flip()
        clock.tick(50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                snake.crash = False
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    score = 0
                    newHighscore = False
                    food.__init__()
                    if twoPlayers:
                        snake1.__init__(0+130, height/2, p1Color)
                        snake2.__init__(width-140, height/2, p2Color)
                    else:
                        snake1.__init__(height/2, width/2)
                elif event.key == pygame.K_ESCAPE:
                    screen.fill((0, 0, 0))
                    score = 0
                    newHighscore = False
                    food.__init__()
                    twoPlayers = playerSelect()
                    if twoPlayers:
                        snake1 = snake(0+130, height/2, p1Color)
                        snake2 = snake(width-140, height/2, p2Color)
                    else:
                        snake1 = snake(width/2, height/2)
                
                