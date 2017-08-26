"""
Implementation of BREAKOUT in Python with Pygame.
More about this code here:
Katie Amazing, August 2017
"""

import sys
import pygame
import math
import random


class Collision(object):
    def __init__(self, ball):
        self.ball = ball
        self.bodies = []

    def add(self, body):
        self.bodies.append(body)

    def remove(self, body):
        self.bodies.remove(body)

    def update(self):
        for body in self.bodies:
            if self.ball.x > body.x \
            and self.ball.x < body.x + body.width \
            and self.ball.y < body.y + body.height \
            and self.ball.y > body.y:
                body.on_collide()
                self.ball.on_collide()

    def draw(self):
        pass


class Ball(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velx = 0
        self.vely = 0
        self.r = 6
        self.launched = False
        self.speed = 6

    def launch(self, pos):
         if self.launched:
             pass
         mx = pos[0] - 300
         my = pos[1] - 400
         dist = math.sqrt(mx ** 2 + my ** 2)
         self.velx = mx/(dist)
         self.vely = my/(dist)
         self.launched = True

    def on_collide(self):
         self.vely *= -1

    def reset(self):
         self.x = width/2
         self.y = height-6
         self.velx = 0
         self.vely = 0
         self.launched = False

    def update(self):
         self.x += self.velx
         self.y += self.vely

         if self.x < 0 or self.x > width:
             self.velx *= -1
         if self.y < 0:
             self.vely *= -1
         if self.y > height:
             self.reset()

    def draw(self):
         pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), self.r)


class Paddle(object):
    def __init__(self, x, velx):
        self.x = x
        self.y = height - 4
        self.width = 80
        self.height = 4
        self.velx = velx
        self.speed = 4

    def keypress(self, key):
        if key == pygame.K_LEFT and self.velx > -self.speed:
            self.velx -= 1
        elif key == pygame.K_RIGHT and self.velx < self.speed:
            self.velx += 1

    def on_collide(self):
        pass

    def update(self):
        self.velx *= 0.95               # Apply friction
        self.x += self.velx

        if self.x < 0:                   # Lock paddle to screen
            self.x = 0
        elif self.x > width - 80:
            self.x = width - 80

    def draw(self):
        pygame.draw.rect(screen, (255,255,255), [self.x, self.y, self.width, self.height])


class Brick(object):
    def __init__(self, x, y, sprite, collision_handler, bubbles):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 25
        self.sprite = sprite
        self.hit = False
        self.collision_handler = collision_handler
        self.bubbles = bubbles

    def on_collide(self):
        self.bubbles.create(self.x, self.y) # TODO feels weird
        self.hit = True
        self.collision_handler.remove(self)

    def draw(self):
        if not self.hit:
            screen.blit(self.sprite, pygame.Rect(self.x, self.y, self.width, self.height))


class Bricks(object):
    def __init__(self, rows, cols, sprite_name, collision_handler, bubbles):
        self.sprite = pygame.image.load(sprite_name)
        self.grid = self.initlist(rows, cols, collision_handler, bubbles)

    def initlist(self, rows, cols, collision_handler, bubbles):
        """Returns a list of lists of bricks."""
        bricklist = []
        for row in range(0,rows):
            bricklist.append([])
            bricky = 25 * row + 50
            for col in range (0,cols):
                brickx = col * 50 + (.5 * (600-(50*cols)))
                bricklist[row].append(Brick(brickx, bricky, self.sprite, collision_handler, bubbles))
                collision_handler.add(bricklist[row][col])
        return bricklist

    def done(self):
        for row in self.grid:
            for brick in row:
                if not brick.hit:
                    return False
        else:
            return True

    def update(self):
        pass

    def draw(self):
        for row in self.grid:
            for brick in row:
                brick.draw()


class Particles(object):
    def __init__(self):
        self.particles = []

    def create(self, x, y):
        for bubble in range(0, random.randint(1, 5)):
            self.particles.append(Particle(x + 25, y + 13))

    def update(self):
        live_particles = []
        for bubble in self.particles:
            if bubble.alive:
                live_particles.append(bubble)
                bubble.update()
        self.particles = live_particles

    def draw(self):
        for bubble in self.particles:
            bubble.draw()


class Particle(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velx = (random.randint(-3, 3) + 0.5) / 2
        self.vely = (random.randint(1, 4) * -1) / 5
        self.scale = random.randint(7, 15)
        self.sprite = pygame.image.load("bubble15.png")
        self.alive = True

    def update(self):
        if self.velx < 0:
            self.velx += 0.1
        elif self.velx > 0:
            self.velx -= 0.1

        if self.vely > 1:
            self.vely -= 0.1

        self.x += self.velx
        self.y += self.vely

        if self.y < - 1 or self.x < -1 or self.x > width + 2:
            self.alive = False

    def draw(self):
        screen.blit(self.sprite, pygame.Rect(self.x, self.y, self.scale, self.scale))


class Level(object):
    def __init__(self, rows, cols, bricksprite):
        self.rows = rows
        self.cols = cols
        self.bricksprite = bricksprite
        self.components = []

    def add(self, component):
        self.components.append(component)

    def update(self):
        for component in self.components:
            component.update()

    def draw(self):
        for component in self.components:
            component.draw()

    def play(self):
        ball = Ball(width/2, height-6)
        collision_handler = Collision(ball)
        bubbles = Particles()
        bricks = Bricks(self.rows, self.cols, self.bricksprite, collision_handler, bubbles)
        paddle = Paddle(width/2, 0)
        collision_handler.add(paddle)
        self.add(collision_handler)
        self.add(bricks)
        self.add(paddle)
        self.add(ball)
        self.add(bubbles)
        bgimg = pygame.image.load("gradientbg.png")
        bg = pygame.Surface((width, height))
        bg.blit(bgimg, (0, 0))
        pygame.key.set_repeat(30, 30)
        while not bricks.done():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    paddle.keypress(event.key)
                if event.type == pygame.MOUSEBUTTONUP:
                    position = pygame.mouse.get_pos()
                    ball.launch(position)
            screen.blit(bg, (0,0))
            self.update()
            self.draw()
            pygame.display.flip()


class WinScreen(object):
    def __init__(self):
        self.sprite = pygame.image.load("wintext.png")
        self.done = False

    def play(self):
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    self.done = True
            screen.blit(self.sprite, pygame.Rect(width/2 - 272/2, height/2 - 112/2, 272, 112))
            pygame.display.flip()


class SplashScreen(object):
    def __init__(self):
        self.sprite = pygame.image.load("splashtext.png")
        self.done = False

    def play(self):
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    self.done = True
            screen.blit(self.sprite, pygame.Rect(0, 0, 600, 400))
            pygame.display.flip()


class Game(object):
    def __init__(self):
        self.levels = [
            SplashScreen(),
            Level(3, 12, "waterbrick.png"),
            Level(5, 8, "waterbrick2.png"),
            Level(4, 10, "waterbrick3.png"),
            WinScreen(),
        ]
        bgimg = pygame.image.load("gradientbg.png")
        self.bg = pygame.Surface((width, height))
        self.bg.blit(bgimg, (0, 0))

    def play(self):
        for level in self.levels:
            screen.blit(self.bg, (0,0))
            level.play()


pygame.init()
size = width, height = 600, 400
screen = pygame.display.set_mode(size)
while 1:
    game = Game()
    game.play()
