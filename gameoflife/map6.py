### Made it so that child blocks span near parents, it got the game to run more smoothly

import sys, pygame, random
from pygame.locals import *
# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
BLUE     = (   0,   0, 255)
COLORS = BLACK,WHITE,GREEN,RED,BLUE

# Set window parameters
pygame.init()
size = width, height = 680, 680
pygame.display.set_caption("Game of Life")
screen = pygame.display.set_mode(size)
keys_down = set()

# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# Lay seed for random fuctions
random.seed

# Functions
def move(rect,size,r):
    if r==1:
        rect[1] -= 10
    elif r==2:
        rect[0] += 10
        rect[1] -= 10
    elif r==3:
        rect[0] += 10
    elif r==4:
        rect[0] += 10
        rect[1] += 10
    elif r==5:
        rect[1] += 10
    elif r==6:
        rect[0] -= 10
        rect[1] += 10
    elif r==7:
        rect[0] -= 10
    elif r==8:
        rect[0] -= 10
        rect[1] -= 10
    
    for i in (0,1):
        if rect[i] < 0:
            rect[i] = size[0]-10
        elif rect[i] >= size[i]:
            rect[i] = 0
            
# Variables
t = 1
life = 16
span = 4
RectsR = []
RectsG = []

# Pre-start set-up
for i in range(0,500):
    x = random.randrange(0,width,10)
    y = random.randrange(0,height,10)
    RectsR.append([x,y,life])
    pygame.draw.rect(screen,RED,[RectsR[i][0],RectsR[i][1],10,10])
    
for i in range(0,500):
    x = random.randrange(0,width,10)
    y = random.randrange(0,height,10)
    RectsG.append([x,y,10,10])
    pygame.draw.rect(screen,GREEN,[RectsR[i][0],RectsR[i][1],10,10])
    
# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get(): # User did something
        if event.type == pygame.KEYDOWN: # If user pushed any key
            done = True # Then close the window
    
    # --- Game logic should go here
    for rect in RectsR: # moves all red rects
        r = random.randint(0,8)
        move(rect,size,r) 
    
    for rect in RectsG: # moves all green rects
        r = random.randint(0,8)
        move(rect,size,r) 
        
    for rectR in RectsR:
        for rectG in RectsG:            
            if rectR[0]==rectG[0]:
                if rectR[1]==rectG[1]:
                    RectsG.remove(rectG) # 'eats' green rects, spans red ones
                    x = random.randint(-1,1)
                    y = random.randint(-1,1)
                    RectsR.append([rectR[0]+x*10,rectR[1]+y*10,life])
        rectR[2]-=1
        if rectR[2] == 0:
            RectsR.remove(rectR) # red ones die after thier life-span
            
    tmp = []
    for rectG in RectsG:
        if t % span == 0:
			x = random.randint(-1,1)
			y = random.randint(-1,1)
			tmp.append([rectG[0]+x*10,rectG[1]+y*10,life])
    RectsG.extend(tmp)
    
    
    
    
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(BLACK)
 
    # --- Drawing code should go here
    for rect in RectsR:
        pygame.draw.rect(screen,RED,[rect[0],rect[1],10,10])
    for rect in RectsG:
        pygame.draw.rect(screen,GREEN,[rect[0],rect[1],10,10])
        
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # --- Limit to 60 frames per second
    clock.tick(20)
    t+=1
