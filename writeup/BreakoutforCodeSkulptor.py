# Implementation of BREAKOUT
# To run on CodeSkulptor Web App
# Holy Global Variables, Batman

import simplegui
import random
import math

WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 80
PAD_HEIGHT = 396
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
paddle_pos = WIDTH/2
paddle_vel = 0
launched = False
level = 0
posx = WIDTH/2
posy = HEIGHT
velx = 0
vely = 0
broken_count = 0
lives = 3
ball_radius = 6
particles = []
img_bbubble = simplegui.load_image("https://raw.githubusercontent.com/katieamazing/breakout/master/bbubble.png")
img_bbrick = simplegui.load_image("https://raw.githubusercontent.com/katieamazing/breakout/master/waterbrick.png")
img_cbrick = simplegui.load_image("https://raw.githubusercontent.com/katieamazing/breakout/master/waterbrick2.png")
img_pbrick = simplegui.load_image("https://raw.githubusercontent.com/katieamazing/breakout/master/waterbrick3.png")
img_bubble = simplegui.load_image("https://raw.githubusercontent.com/katieamazing/breakout/master/bubble15.png")
img_gbg = simplegui.load_image("https://raw.githubusercontent.com/katieamazing/breakout/master/gradientbg.png")
img_splash = simplegui.load_image("https://raw.githubusercontent.com/katieamazing/breakout/master/splashtext.png")
img_win = simplegui.load_image("https://raw.githubusercontent.com/katieamazing/breakout/master/wintext.png")
sfx_pop = simplegui.load_sound("https://raw.githubusercontent.com/katieamazing/breakout/master/pop.wav")
sfx_pop.set_volume(0.7)
sfx_level = simplegui.load_sound("https://raw.githubusercontent.com/katieamazing/breakout/master/transition.wav")
sfx_level.set_volume(0.7)
levels = [
    {'rows': 0, 'cols': 0, 'brickgoals': 0, 'bricktype': img_bbrick, 'bg': '#FFFFFF'},
    {'rows': 3, 'cols': 12, 'brickgoals': 3*12, 'bricktype': img_bbrick, 'bg': '#8BE8FF'},
    {'rows': 5, 'cols': 8, 'brickgoals': 5*8, 'bricktype': img_cbrick, 'bg': '#94FFFC'},
    {'rows': 4, 'cols': 10, 'brickgoals': 4*10, 'bricktype': img_pbrick, 'bg': '#7978F8'},
    {'rows': 0, 'cols': 0, 'brickgoals': 0, 'bricktype': img_bbrick, 'bg': '#FFFFFF'},
]

def initlist():
    global bricklist
    bricklist = []
    for row in range(0,levels[level]['rows']):
        bricklist.append([])
        for i in range (0,levels[level]['cols']):
            bricklist[row].append(False)
            
def newgame():
    global posx, posy, velx, vely, paddle_pos, paddle_vel, lives, launched, bricklist
    global sfx_level, level
    posx = WIDTH/2
    posy = HEIGHT
    velx = 0
    vely = 0
    paddle_pos = WIDTH/2
    paddle_vel = 0
    broken_count = 0
    level = 0
    lives = 3
    label2.set_text("Lives Remaining: %r" % lives)
    initlist()

def reset():
    global posx, posy, velx, vely, paddle_pos, paddle_vel, lives, launched, brickhit, level
    posx = WIDTH/2
    posy = HEIGHT
    velx = 0
    vely = 0
    paddle_vel = 0
    launched = False
    if level == 0:
        level = 1
        initlist()
    frame.set_canvas_background(levels[level]['bg'])

def over(cols):
    return (.5 * (600-(50*cols)))

def draw_bricks(canvas, bricklist):
    global posx, posy, velx, vely, broken_count, level, ball_radius
    done = False    
    for row in range (0,levels[level]['rows']):
        if done:
            break
        brickheight = 25 * row+50
        cols = levels[level]['cols']
        for col in range(0,cols):
            if done:
                break
            brickorigin = col * 50 + over(cols)
            if bricklist[row][col] == False:  
                canvas.draw_image(levels[level]['bricktype'], (25,12), (50,25), (brickorigin+25, brickheight+25), (50,25))
                #canvas.draw_polygon([(brickorigin, brickheight), (brickorigin+50, brickheight), (brickorigin+50, brickheight + 25), (brickorigin, brickheight + 25)], 3, "Black", "White")
                if posx > brickorigin and posx < brickorigin + 50 and posy < brickheight + 25 and posy > brickheight:
                    bricklist[row][col] = True 
                    vely = vely * -1
                    ball_radius = 12
                    make_particles(brickorigin, brickheight)
                    sfx_pop.rewind()
                    sfx_pop.play()
                    broken_count += 1
                    if broken_count >= levels[level]['brickgoals']:
                        level += 1
                        broken_count = 0
                        initlist()
                        reset()
                        sfx_level.rewind()
                        sfx_level.play()
                        done = True  
                        
class Particle:
    def __init__(self, x, y):
        self.pos_x = x
        self.pos_y = y
        self.vel_y = random.randint(1, 4)*-1
        self.vel_x = random.randint(-3,3)+.5
        self.scale = random.randint(7,15)
        self.alive = True
    def update(self):
        if self.vel_x < 0:
            self.vel_x += 0.1
        elif self.vel_x > 0:
            self.vel_x -= 0.1
        if self.vel_y > 1:
            self.vel_y -= 0.1
        self.pos_x += self.vel_x
        self.pos_y += self.vel_y
        if self.pos_y > HEIGHT +2 or self.pos_y < -1 or self.pos_x < -1 or self.pos_x > WIDTH +2:
            self.alive = False
    def draw(self, canvas):
        canvas.draw_image(img_bubble, (7,7), (15,15),(self.pos_x, self.pos_y), (self.scale, self.scale))

def make_particles(x, y):
    numparticles = random.randint(1,5)
    for things in range (0, numparticles):
        particles.append(Particle(x + 25, y + 13))
        
def draw(canvas):
    global posx, posy, velx, vely, paddle_pos, paddle_vel, lives, launched, bricklist
    global level, ball_radius, broken_count
    if posy<1:
        vely = vely * -1
    if posx<1:
        velx = velx * -1
    if posx>599:
        velx = velx * -1
    # update ball
    posx += velx*1.5 #debug
    posy += vely*1.5
    if ball_radius > 6:
        ball_radius -= 0.5
    # update paddle's vertical position, keep paddle on the screen
    if paddle_pos < (HALF_PAD_WIDTH) and paddle_vel < 0:
        paddle_vel = 0
    if paddle_pos > (WIDTH - (HALF_PAD_WIDTH)) and paddle_vel > 0:
        paddle_vel = 0  
    paddle_pos += paddle_vel*2
    # draw paddle, bricks, particles, ball
    canvas.draw_polygon([(paddle_pos-HALF_PAD_WIDTH, HEIGHT), (paddle_pos+HALF_PAD_WIDTH, HEIGHT), (paddle_pos+HALF_PAD_WIDTH, PAD_HEIGHT),(paddle_pos-HALF_PAD_WIDTH, PAD_HEIGHT)], 1, "White","White")
    draw_bricks(canvas, bricklist)
    for particle in particles:
        particle.update()
        particle.draw(canvas)
    for i in range(len(particles)-1, 0, -1):
        particle = particles[i]
        if particle.alive == False:
            particles.pop(i)
    canvas.draw_circle([posx, posy], ball_radius, 1, "white", "white")
    if level == 0:
        canvas.draw_image(img_gbg, (300,200), (600,400), (300,200), (600,400))
        canvas.draw_image(img_splash, (300,200), (600,400), (300,200), (600,400))
    elif level == 4:
        canvas.draw_image(img_gbg, (300,200), (600,400), (300,200), (600,400))
        canvas.draw_image(img_win, (272/2,56), (272,112), (300,200), (272,112))
    # determine whether paddle and ball collide  
    if vely > 0 and posy > 394 and launched == True:
        if posx < (paddle_pos - HALF_PAD_WIDTH) or posx > (paddle_pos + HALF_PAD_WIDTH):
            launched = False
            lives -= 1
            label2.set_text("Lives Remaining: %r" % lives)
            if lives <= 0:
                broken_count = 0
                newgame()
            else:
                reset()
        else:
            vely = vely * -1
    
    if posy > 420 and launched == True:
        launched = False
        reset()    
        
def mouse_handler(position):
    global velx, vely, launched, level
    if launched:
        pass
    elif level == 0:
        reset()
    elif level == 4:
        newgame()
    else:
        x = position[0] - 300
        y = position[1] - 400
        dist = math.sqrt(x ** 2 + y ** 2)
        velx = x/(dist/4)
        vely = y/(dist/4)
        launched = True
    
def keydown(key):
    global paddle_vel
    if key == simplegui.KEY_MAP['left']:
        paddle_vel = -4
    elif key == simplegui.KEY_MAP['right']:
        paddle_vel = 4
    elif key == simplegui.KEY_MAP['space']:
        particles.pop()
   
def keyup(key):
    global paddle_vel
    if key == simplegui.KEY_MAP['left']:
        paddle_vel = 0
    elif key == simplegui.KEY_MAP['right']:
        paddle_vel = 0

# create frame
frame = simplegui.create_frame("Bubble Bricks", WIDTH, HEIGHT)
label2 = frame.add_label("Lives Remaining: %r" % lives, 200)
frame.set_draw_handler(draw)
frame.set_mouseclick_handler(mouse_handler)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

# start frame
newgame()
frame.start()
