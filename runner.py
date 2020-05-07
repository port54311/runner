import bisect
import itertools
import random
import sys
import time
import pygame

# Resources: images
img_youlose = pygame.image.load(r'game_images\lose.png')
img_start = pygame.image.load(r'game_images\start.png')
img_backgrounds = [pygame.image.load(r'game_images\background1.png'),
                   pygame.image.load(r'game_images\background2.png'),
                   pygame.image.load(r'game_images\background3.png')]
img_Lruncycle = [pygame.image.load(r'game_images\walk1.gif'),
                 pygame.image.load(r'game_images\walk2.gif'),#Lruncycle2.png'),
                 pygame.image.load(r'game_images\walk3.gif'),#Lruncycle3.png'),
                 pygame.image.load(r'game_images\walk4.gif'),#Lruncycle4.png'),
                 pygame.image.load(r'game_images\walk5.gif'),#Lruncycle5.png'),
                 pygame.image.load(r'game_images\walk6.gif'),#Lruncycle6.png'),
                 pygame.image.load(r'game_images\walk7.gif'),#Lruncycle7.png'),
                 pygame.image.load(r'game_images\walk8.gif'),#Lruncycle8.png'),
                 pygame.image.load(r'game_images\walk9.gif'),#Lruncycle9.png'),
                 pygame.image.load(r'game_images\walk10.gif'),#Lruncycle10.png'),
                 pygame.image.load(r'game_images\walk11.gif'),#Lruncycle11.png'),
                 pygame.image.load(r'game_images\walk12.gif'),#Lruncycle12.png'),
                 pygame.image.load(r'game_images\walk13.gif'),#Lruncycle13.png'),
                 pygame.image.load(r'game_images\walk14.gif')]#Lruncycle14.png')]
img_sliding = [pygame.image.load(r'game_images\slide1.gif'),#sliding1.png'),
               pygame.image.load(r'game_images\slide2.gif')]#sliding2.png')]
img_falling = pygame.image.load(r'game_images\walk1.gif')#falling.png')
img_mid = [pygame.image.load(r'game_images\intro1.png'),#mid1.png'),
           pygame.image.load(r'game_images\intro2.png')]#mid2.png')]
img_restart = pygame.image.load(r'game_images\restart.png')#restart.png')
img_Acycle = [pygame.image.load(r'game_images\walk7.gif'),#Acycle1.png'),
              pygame.image.load(r'game_images\walk8.gif'),#Acycle2.png'),
              pygame.image.load(r'game_images\walk9.gif'),#Acycle3.png'),
              pygame.image.load(r'game_images\walk10.gif')]#Acycle4.png'),

class Game():
    def __init__(self, character, game_display):
        pygame.init()
        pygame.display.set_caption('bootleg subway surfer')
        self.game_display = game_display
        self.game_width = game_display.get_width()
        self.speed = 10
        self.score = 0
        self.character = character
        self.obstacles = []
        self.clock = pygame.time.Clock()
        self.FPS = 30

    # Creates and returns an "Obstacle" object. Position is defaulted to slightly offscreen.
    def create_obstacle(self, position=False):
        defaults = [[0, 0, random.randint(20,80), 470], # top obstacle
                           [0, 275, random.randint(20,40), 200],# mid
                           [0, 400, random.randint(20,40), 500]] # bottom obstacle
        obstacle_number = random.randint(0,2)
        obstacle = defaults[obstacle_number]
        obstacle[0] = position if position else self.game_width + 100
        return Obstacle(self.game_display, *obstacle)
    
    # pygame event loop. Displays updates to screen. Returns "key" pressed (if any)
    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        #colors = [(255, 208, 168), (255, 177, 177), (255, 243, 170)] # orange, red, yellow
        self.message_to_screen(str(self.score), (255, 208, 168), 0, 0)
        pygame.display.update()
        self.clock.tick(self.FPS)
        return pygame.key.get_pressed()

    # What to display on the screen when the user has lost the game
    # Clears out any remaining obstacles, and makes a new obstacle when the user restarts
    def lost(self):
        while True:
            key = self.event_loop()
            self.game_display.blit(img_youlose, (120,100))
            self.game_display.blit(img_restart, (100, 470))
            if key[pygame.K_LEFT]:
                self.obstacles = []
                self.score = 0
                self.speed = 10
                self.character.reset()
                self.obstacles.append(self.create_obstacle())
                return

    # Advances the game. Difficulty curve is an index of how many obstacles exist at once.
    # All obstacles in the obstacle list are advanced "speed"-units on the x-axis
    def advance(self):
        difficulty = [0,10,20]
        for obstacle in self.obstacles:
            obstacle.position -= int(self.speed)
            if self.character.collision(obstacle):
                self.lost()
            if obstacle.position < 0:
                self.obstacles.remove(obstacle)
                self.score += 1
        obstacle_max = bisect.bisect(difficulty, self.score)
        for _ in range(obstacle_max):
            if len(self.obstacles) < obstacle_max:
                next_position = 0
                if len(self.obstacles):
                    next_position = max(map(lambda x: x.position, self.obstacles)) + 500
                self.obstacles.append(self.create_obstacle(next_position))
        self.character.advance()
    
    # Displays a message on the screen
    def message_to_screen(self, msg, color, xcor, ycor):
        font = pygame.font.SysFont(None, 40) # font size 25
        screen_text = font.render(msg, True, color)
        self.game_display.blit(screen_text, [xcor, ycor])
    
    # Displays the intro screen until the user hits "left"
    def intro(self):
        bounce_image = itertools.cycle([0]*5 + [1]*5)
        while True:
            key = self.event_loop()
            if key[pygame.K_LEFT]:
                break
            self.game_display.blit(img_backgrounds[0], (0, 0))
            self.game_display.blit(img_backgrounds[1], (0, 500))
            self.game_display.blit(img_start, (100, 450))
            self.game_display.blit(img_mid[next(bounce_image)], (self.character.x, self.character.reset_y))
    
    # Main game loop. Scrolls the background, increases speed, calls advance
    def main_loop(self):
        # scrolling background
        background_xcycle = itertools.cycle(range(0, self.game_width+1, 20))
        background = itertools.cycle([0,1,2])
        a = next(background)
        b = next(background)
        c = b # This is the background underneath "a"
        self.obstacles.append(self.create_obstacle())
        while True:
            background_x = next(background_xcycle)
            self.game_display.blit(img_backgrounds[a], (background_x, 0))
            self.game_display.blit(img_backgrounds[c], (background_x, 500))
            self.game_display.blit(img_backgrounds[b], (background_x-self.game_width, 0))
            self.game_display.blit(img_backgrounds[a], (background_x-self.game_width, 500))
            self.advance()

            if self.speed < 30:
                self.speed += 0.03
            
            if background_x >= self.game_width:
                c = a # Since "b" is updating, the new background underneath "a", is "b's" old background (a)
                a = b
                b = next(background)
            self.event_loop()

class Rectangle():
    "A rectangle object. y is inverse (lower is higher)"
    def __init__(self, x, y, height, width):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    # Detects if two rectangle objects are intersecting
    def collision(self, obstacle):
        return (obstacle.right  > self.left   and
                obstacle.left   < self.right  and
                obstacle.top    < self.bottom and
                obstacle.bottom > self.top)
    
    # Make nice/dynamic names for x/y coordinates
    @property
    def top(self):
        return self.y
    
    @property
    def bottom(self):
        return self.y + self.height
    
    @property
    def left(self):
        return self.x
    
    @property
    def right(self):
        return self.x + self.width

class Character(Rectangle):
    def __init__(self, game_display, x, y, jumpCount=10):
        # Height and width indicate hitbox proportions
        super().__init__(x,y, height=100, width=90)
        self.game_display = game_display
        self.game_height = game_display.get_height()
        self.jumpCount = jumpCount
        self.running = True
        self.jumping = False
        self.sliding = False
        self.falling = False
        self.reset_y = y
        # This makes a cycle that iterates smoothly no matter how many sliding animations you have
        self.slide_img = itertools.cycle([i for i,img in enumerate(range(2)) for repetition in range(5)])
        self.run_img = itertools.cycle(range(len(img_Lruncycle)))
        self.jump_img = itertools.cycle(range(len(img_Acycle)))
    
    def reset(self):
        self.__init__(self.game_display, self.x, self.reset_y, jumpCount=10)
    
    @property
    def top(self):
        if self.sliding:
            return self.y + self.height//2
        else:
            return self.y
    
    # Make the hitbox only the front of the character
    @property
    def left(self):
        return self.x + self.width//2
    
    def move(self):
        k = pygame.key.get_pressed()
        if k[pygame.K_UP] and not (self.falling or self.sliding):
            self.jumping = True
        if k[pygame.K_DOWN]:
            if self.jumping:
                self.falling = True
                self.jumping = False
                self.running = False
                self.sliding = False
            elif self.falling:
                self.y += 70
                if self.y + 10 > self.game_height - 150:
                    self.y = self.game_height - 150
                    self.falling = False
                    self.jumpCount = 10
            else:
                self.running = False
                self.jumping = False
                self.jumpCount = 10
                self.sliding = True
        else:
            if not self.falling:
                self.running = True
                self.sliding = False
        if self.jumping:
            if self.jumpCount >= -10:
                neg = -1 if self.jumpCount < 0 else 1
                self.y -= int((self.jumpCount **2) * 0.9 * neg)
                self.jumpCount -= 1
            else:
                self.jumping = False
                self.jumpCount = 10
    
    def draw(self):
        if self.falling:
            self.game_display.blit(img_falling, (self.x, self.y))
        elif self.sliding:
            self.game_display.blit(img_sliding[next(self.slide_img)], (self.x, self.y))
        elif self.jumping:
            self.game_display.blit(img_Acycle[next(self.jump_img)], (self.x, self.y))
        else: # Running
            self.game_display.blit(img_Lruncycle[next(self.run_img)], (self.x, self.y))

    def advance(self):
        self.move()
        self.draw()
 
class Obstacle(Rectangle):
    def __init__(self, game_display, x, y, width, height, color = (255,255,255)):
        super().__init__(x, y, height, width)
        self.game_display = game_display
        self.color = color
    
    @property
    def position(self):
        return self.x
    
    @position.setter
    def position(self, value):
        self.x = value
        pygame.draw.rect(self.game_display, self.color, (self.x, self.y, self.width, self.height))
 
if __name__ == '__main__':
    # Game Constants
    display_width = 800
    display_height = 600
    player_start = {"x": 80, "y": display_height - 150}

    # Initialize
    game_display = pygame.display.set_mode((display_width, display_height))
    runner = Character(game_display, player_start["x"], player_start["y"])
    game = Game(runner, game_display)
    game.intro()
    game.main_loop()
