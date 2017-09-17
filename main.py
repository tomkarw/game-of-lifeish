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
pixel = 10
pixWidth, pixHeight = width/pixel, height/pixel
pygame.display.set_caption("Game of Life")
screen = pygame.display.set_mode(size)
keys_down = set()


 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# Lay seed for random fuctions
random.seed

# Kind-of inlines


# Classes

class Blob:
	"""Blob is a green or red block that moves around, repopulates, eats and dies"""
    
	def __init__(self, c, s, a=0):
		self.colony = c
		self.span = s
		self.age = a
        
    
class TheMap:
    """Map stores screen size as well as 3D array of Blobs lists, also includes funtions for interaction of Blobs"""
    
    def __init__(self,pixWidth,pixHeight,pixel):
        """Initialises the map of given width and height"""
        
        self.pixWidth = pixWidth
        self.pixHeight = pixHeight
        self.pixel = pixel
        self.turn = 0
        
        self.array = [ [ [ [] for z in range(0,2) ] for y in range(0,pixHeight) ] for x in range(0,pixWidth) ]
        for i in range(0,500):
            x = random.randrange(0,pixWidth)
            y = random.randrange(0,pixHeight)
            self.array[x][y][0].append(Blob(0,life))

        for i in range(0,500):
            x = random.randrange(0,pixWidth)
            y = random.randrange(0,pixHeight)
            self.array[x][y][1].append(Blob(1,life))
                
        print 'init successful'
                  
    def moveBlobs(self):
        """Moves blobs randomly within provided screen size"""
        
        tmp_array = [ [ [ [] for z in range(0,2) ] for y in range(0,pixHeight) ] for x in range(0,pixWidth) ]
        
        for i in range(0,2):
            for x in range(0,self.pixWidth):
                for y in range(0,self.pixHeight):
                    
                    while len(self.array[x][y][i]) > 0:
                        
                        xx = x + random.choice([-1,0,1])
                        yy = y + random.choice([-1,0,1])
 
                        if xx >= self.pixWidth:
                            xx = 0
                        elif xx < 0:
                            xx = self.pixWidth - 1
                        if yy >= self.pixHeight:
                            yy = 0
                        elif yy < 0:
                            yy = self.pixHeight - 1
                        tmp_array[xx][yy][i].append(self.array[x][y][i].pop())
                        
        self.array = tmp_array
        print 'move successful'
                    
    def actBlobs(self):
        """Checks if aggresive blobs ate something and kills the old ones """
        
        tmp_array = [ [ [ [] for z in range(0,2) ] for y in range(0,pixHeight) ] for x in range(0,pixWidth) ]
        
        for x in range(0,self.pixWidth):
                for y in range(0,self.pixHeight):
                    for dying in self.array[x][y][0]:
                        dying.age += 1
                        if dying.age > 12:
                            self.array[x][y][0].remove(dying)
                        
                    while len(self.array[x][y][0]) > 0 and len(self.array[x][y][1]) > 0:
                        self.array[x][y][1].pop()
                        tmp_array[x][y][0].append(self.array[x][y][0].pop())
                    
                        xx = x + random.choice([-1,0,1])
                        yy = y + random.choice([-1,0,1])
                        
                        if xx >= self.pixWidth:
                            xx = 0
                        elif xx < 0:
                            xx = self.pixWidth - 1
                        if yy >= self.pixHeight:
                            yy = 0
                        elif yy < 0:
                            yy = self.pixHeight - 1
                        
                        tmp_array[xx][yy][0].append(Blob(0,life))
                    
                    
                        
                    while len(self.array[x][y][1]) > 0:
                        
                        if self.turn % 5 == 0:    
                            xx = x + random.choice([-1,0,1])
                            yy = y + random.choice([-1,0,1])
                                
                            if xx >= self.pixWidth:
                                xx = 0
                            elif xx < 0:
                                xx = self.pixWidth - 1
                            if yy >= self.pixHeight:
                                yy = 0
                            elif yy < 0:
                                yy = self.pixHeight - 1
                                    
                            tmp_array[xx][yy][1].append(self.array[x][y][1][-1])
                            
                        tmp_array[x][y][1].append(self.array[x][y][1].pop())
                            
                            
                    while len(self.array[x][y][0]) > 0:
                            tmp_array[x][y][0].append(self.array[x][y][0].pop())
                            
        self.array = tmp_array
        self.turn += 1
                    
    def draw(self,screen):
        """Draws the map with blobs"""
        for x in range(0,self.pixWidth):
            for y in range(0,self.pixHeight):
                if len(self.array[x][y][0]) > 0:
                    pygame.draw.rect(screen,[255,0,0],[x*self.pixel,y*self.pixel,self.pixel,self.pixel])
                elif len(self.array[x][y][1]) > 0:
                    pygame.draw.rect(screen,[0,255,0],[x*self.pixel,y*self.pixel,self.pixel,self.pixel])
        
        print 'draw successful'
            
# Functions

# Variables
done = False    # loop until the user clicks the close button.
t = 1			# turn count
life = 12		# how many turns it takes for aggresive blob to die
span = 5		# how many turns it takes for passive blob to reproduce

# Pre-start set up
theMap = TheMap(pixWidth,pixHeight,pixel)     # initalises theMap with blobs
theMap.draw(screen)
# -------- Main Program Loop -----------
while not done:
    
    # --- Event loop (not yet fully useful)
    for event in pygame.event.get():        # did user do something
        if event.type == pygame.KEYDOWN:    # if user pushed any key
            while event.type in pygame.event.get() is not pygame.KEYDOWN:                     # then close the window
                clock.tick(1)
    # --- Game logic
    theMap.moveBlobs()  # moves the Blobs around in the array
    
    theMap.actBlobs()   # aggressive Blobs eat Green ones, they all reproduce
    
    # --- Clear the screen
    screen.fill(BLACK)
 
    # --- Drawing new screen
    
    theMap.draw(screen)
    # --- Update screen with what was drawn
    pygame.display.flip()
 
    # --- Limits frames per second
    clock.tick(30)
    t+=1
