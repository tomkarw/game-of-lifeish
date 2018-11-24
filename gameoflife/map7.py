### TO-DO LIST:
### Make two distinct predator species
### Make some optimistaions for colision checking

import sys, pygame, random
# from pygame.locals import *

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
RED      = ( 255,   0,   0)
GREEN    = (   0, 255,   0)
BLUE     = (   0,   0, 255)

# Set window parameters
pygame.init()
size = width, height = 680, 680
pixel = 1
pixWidth, pixHeight = width/pixel, height/pixel
pygame.display.set_caption("Game of Life")
screen = pygame.display.set_mode(size)
keys_down = set()


 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# Lay seed for random fuctions
random.seed

# Classes

class Blob:
	"""Blob is a green or red block that moves around, repopulates, eats and dies"""
    
	def __init__(self, c, s, a=0):
		self.colony = c
		self.span = s
		self.age = a
        
    
class TheMap:
    """Map stores screen size as well as 3D array of Blobs, also includes funtions for interaction of Blobs"""
    
    def __init__(self,pixWidth,pixHeight):
        """Initialises the map of given width and height"""
        """SOMETHING WRONG HERE"""
        self.pixWidth = pixWidth
        self.pixHeight = pixHeight
        
        self.array = [ [ [ [] for z in range(0,2) ] for y in range(0,pixHeight) ] for x in range(0,pixWidth) ]
        for i in range(0,500):
            x = random.randrange(0,pixWidth)
            y = random.randrange(0,pixHeight)
            if self.array[x][y][0] is 0:
                self.array[x][y][0] = Blob(0,life)
            else:
                i-=1

        for i in range(0,500):
            x = random.randrange(0,pixWidth)
            y = random.randrange(0,pixHeight)
            if self.array[x][y][0] is 0:
                self.array[x][y][1] = Blob(1,life)
            else:
                i-=1
        
                  
    def moveBlobs(self):
        """Moves blobs randomly within provided screen size"""
        
        for i in range(0,2):
            for x in range(0,self.pixWidth):
                for y in range(0,self.pixHeight):
                    if self.array[x][y][i] is not 0:
						xx = x
						yy = y
						
						while self.array[xx][yy][i] is not 0:
							while True:
								xx += random.choice([-1,0,1])
								yy += random.choice([-1,0,1])
								if not (xx is 0 and yy is 0):
									break
 
							if xx >= self.pixWidth:
								xx = 0
							elif xx < 0:
								xx = self.pixWidth - 1
							if yy >= self.pixHeight:
								yy = 0
							elif yy < 0:
								yy = self.pixHeight - 1
							print 'stuck in move'
							
						self.array[xx][yy][i] = self.array[x][y][i]
						self.array[x][y][i] = 0
						
                        
                    
    def actBlobs(self):
        """Checks if aggresive blobs ate something and kills the old ones """
        for x in range(0,self.pixWidth):
                for y in range(0,self.pixHeight):
                    if self.array[x][y][0] is not 0 and self.array[x][y][1] is not 0:
                        self.array[x][y][1] = 0
                        self.array[x][y][0] = Blob(0,life)
                    xx = x
                    yy = y
                   
                    while self.array[xx][yy][0] is not 0:    
                        while True:
                            xx = random.choice([-1,0,1])
                            yy = random.choice([-1,0,1])
                            if not xx and yy is 0:
                                break
 
                        if xx > self.pixWidth:
                            xx = 0
                        elif xx < 0:
                            xx = self.pixWidth - 1
                        if yy > self.pixHeight:
                            yy = 0
                        elif yy < 0:
                            yy = self.pixHeight - 1
                        print 'stuck in act'
                        
                    self.array[xx][yy][0] = Blob(0,life)
                    
    def draw(self):
        """Draws the map with blobs"""
        for x in range(0,pixWidth):
            for y in range(0,pixHeight):
                if self.array[x][y][0] is not 0:
                    pygame.draw.rect(screen,RED,[x*pixel,y*pixel,pixel,pixel])
                elif self.array[x][y][1] is not 0:
                    pygame.draw.rect(screen,GREEN,[x*pixel,y*pixel,pixel,pixel])
            
# Functions

# Variables
done = False    # loop until the user clicks the close button.
t = 1			# turn count
life = 12		# how many turns it takes for aggresive blob to die
span = 5		# how many turns it takes for passive blob to reproduce

# Pre-start set up
theMap = TheMap(pixWidth,pixHeight)     # initalises theMap with blobs
theMap.draw()
# -------- Main Program Loop -----------
while not done:
    
    # --- Event loop (not yet fully useful)
    for event in pygame.event.get():        # did user do something
        if event.type == pygame.KEYDOWN:    # if user pushed any key
            done = True                     # then close the window
    
    # --- Game logic
    theMap.moveBlobs()  # moves the Blobs around in the array
    
    theMap.actBlobs()   # aggressive Blobs eat Green ones, they all reproduce
    
    # --- Clear the screen
    screen.fill(BLACK)
 
    # --- Drawing new screen
    theMap.draw()
    
    # --- Update screen with what was drawn
    pygame.display.flip()
 
    # --- Limits frames per second
    clock.tick(30)
    t+=1
