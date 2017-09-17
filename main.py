import sys, pygame
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
 
# Variables
a=0

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get(): # User did something
        if event.type == pygame.KEYDOWN: # If user pushed any key
			done = True # Then close the window
    
    # --- Game logic should go here

    
    # --- Drawing code should go here
    for y in range(0,height,10):
        for x in range(0,width,10):
            pygame.draw.rect(screen, COLORS[a], [x,y,10,10])
            a=a+1
            a=a%5
 
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    
    # screen.fill(BLACK)
 
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # --- Limit to 60 frames per second
    clock.tick(1)
