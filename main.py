import pygame, numpy, random

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
RED      = ( 255,   0,   0)
GREEN    = (   0, 255,   0)
BLUE     = (   0,   0, 255)
PURPLE   = ( 128,   0, 128)
# Set window parameters
pygame.init()
size = width, height = 680, 680
pixel = 5
pixWidth, pixHeight = width/pixel, height/pixel
pygame.display.set_caption("Game of Life")
screen = pygame.display.set_mode(size)
keys_down = set()
myfont = pygame.font.SysFont("monospace", 25)
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# Lay seed for random fuctions
random.seed

# Classes

class Blob:
    """Blob is a green or red block that moves around, repopulates, eats and dies"""
    
    def __init__(self, s, l, a=0):
        self.strength = s
        self.life = l
        self.age = a
    
    def strength(self):
        return self.strength
    
class TheMap:
    """Map stores screen size as well as 3D array of Blobs, also includes funtions for interaction of Blobs"""
    
    def __init__(self,pixWidth,pixHeight,pixel):
        """Initialises the map of given width and height with 500 Blobs of each species"""
        
        self.pixWidth = pixWidth
        self.pixHeight = pixHeight
        self.pixel = pixel
        self.turn = 0
        
        
        self.count = [ 0 for i in range(nColonies) ]
        self.avgStr = [ 0 for i in range(nColonies) ]
        
        self.array = [ [ [ [] for z in range(nColonies) ] for y in range(pixHeight) ] for x in range(pixWidth) ]
        for i in range(nColonies):
            for n in range(1000):
                x = random.randrange(0,pixWidth)
                y = random.randrange(0,pixHeight)
                
                s = numpy.random.normal(50,1)       # strength set as a normal distribution 
                l = numpy.random.normal(life,1)     # life span altered by plus/minus normal distribution
                
                self.array[x][y][i].append(Blob(s,l))
                                
                  
    def moveBlobs(self):
        """Moves blobs randomly within provided screen size, also counts each colony size"""
        
        # --- Create an arrray to store next turn
        tmp_array = [ [ [ [] for z in range(nColonies) ] for y in range(pixHeight) ] for x in range(pixWidth) ]
        
        # --- Set count to 0
        for i in range(nColonies):
            self.count[i] = 0
            self.avgStr[i] = 0
        
        # --- Go through each pixel of each layer of Map
        for i in range(nColonies):
            for x in range(self.pixWidth):
                for y in range(self.pixHeight):
                    
                    while self.array[x][y][i]:
                        self.count[i] += 1      # count the blob that is beeing moved
                        self.avgStr[i] += self.array[x][y][i][-1].strength
                        
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
                        
                        if len(tmp_array[xx][yy][i]) < 5:
                            tmp_array[xx][yy][i].append(self.array[x][y][i].pop())
                        else:
                            break
            
            self.avgStr[i] /= self.count[i]           
        self.array = tmp_array
                    
    def actBlobs(self):
        """Checks if aggresive blobs ate something and kills the old ones """
        
        # --- Create an arrray to store next turn
        tmp_array = [ [ [ [] for z in range(nColonies) ] for y in range(pixHeight) ] for x in range(pixWidth) ]
        
        # --- Go through each pixel in Map
        for x in range(self.pixWidth):
                for y in range(self.pixHeight):
                    
                    # --- Remove the old aggressive Blobs
                    for i in range(1,nColonies):
                        for dying in self.array[x][y][i]:
                            dying.age += 1
                            if dying.age > life:
                                self.array[x][y][i].remove(dying)
                    
                    # --- Resolve conflicts between aggressive Blobs
                    winner = 2
                    if self.array[x][y][1]:
                        winner = 1
                        if self.array[x][y][2]:
                            strength = [0,0]
                            for i in range(nColonies-1):
                                for blob in self.array[x][y][i+1]:
                                    strength[i] += blob.strength
                                strength[i] /= len(self.array[x][y][i+1])
                            if strength[1] == strength[0]:
                                winner = random.choice([1,2])
                            elif strength[1] > strength[0]:
                                winner = 2
                    
                    # --- Sort the agroBlobs by strenght (increasing)
                    for i in range(1,nColonies):
                        self.array[x][y][i].sort(key=lambda Blob: Blob.strength) # sorts list with strenght as a key
                    
                    # --- Let the winner eat green Blobs
                    while self.array[x][y][winner] and self.array[x][y][0]:
                        self.array[x][y][0].pop()
                        s = self.array[x][y][winner][-1].strength + numpy.random.normal(0,2)
                        tmp_array[x][y][winner].append(self.array[x][y][winner].pop())
                    
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
                        
                        if len(tmp_array[xx][yy][winner]) < 5:
                            tmp_array[xx][yy][winner].append(Blob(s,life))
                        else:
                            break
                    
                    # --- Surviving Greens get a chance to repopulate
                    while self.array[x][y][0]:
                        
                        if random.random() < span_chance:    
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
                            
                            if len(tmp_array[xx][yy][0]) < 5:        
                                tmp_array[xx][yy][0].append(self.array[x][y][0][-1])
                            else:
                                break
                                
                        if len(tmp_array[x][y][0]) < 5:    
                            tmp_array[x][y][0].append(self.array[x][y][0].pop())
                        else:
                            break    
                    
                    # --- Transfer the remaining agroBlobs to new array
                    for i in range(1,nColonies):        
                        while self.array[x][y][i]:
                            if len(tmp_array[x][y][i]) < 5:
                                tmp_array[x][y][i].append(self.array[x][y][i].pop())
                            else:
                                break
        
        # --- Update the array
        self.array = tmp_array
        self.turn += 1
                    
    def draw(self,screen):
        """Draws the map with blobs"""
        
        for x in range(self.pixWidth):
            for y in range(self.pixHeight):
                xy = [x*self.pixel,y*self.pixel,self.pixel,self.pixel]
                
                if self.array[x][y][1]:
                    pygame.draw.rect(screen,RED,xy)
                    if self.array[x][y][2]:
                        pygame.draw.polygon(screen,PURPLE,[[x*self.pixel,y*self.pixel],[(x+1)*self.pixel,y*self.pixel],[x*self.pixel,(y+1)*self.pixel]])
                elif self.array[x][y][2]:
                        pygame.draw.rect(screen,PURPLE,xy)
                elif self.array[x][y][0]:
                    pygame.draw.rect(screen,GREEN,xy)
        
        pygame.draw.rect(screen,BLACK,[0,0,200,85])
        pygame.draw.rect(screen,WHITE,[0,0,200,85],2)
        
        label = myfont.render('Size', 1, WHITE)
        screen.blit(label, (3,  1))
        label = myfont.render(str(self.count[0]), 1, GREEN)
        screen.blit(label, (3, 21))
        label = myfont.render(str(self.count[1]), 1, RED)
        screen.blit(label, (3, 41))
        label = myfont.render(str(self.count[2]), 1, PURPLE)
        screen.blit(label, (3, 61))
        
        label = myfont.render('avgStr', 1, WHITE)
        screen.blit(label, (80,  1))
        #label = myfont.render(str(self.avgStr[0]), 1, GREEN)
        #screen.blit(label, (80, 21))
        label = myfont.render("{:.3f}".format(self.avgStr[1]), 1, RED)
        screen.blit(label, (80, 41))
        label = myfont.render("{:.3f}".format(self.avgStr[2]), 1, PURPLE)
        screen.blit(label, (80, 61))
# Functions

# Variables
nColonies = 3

life = 12		        # how many turns it takes for aggresive blob to die
span_chance = 0.20		# percentage chance of green blob spanning offspring

done = False
RUNNING, PAUSE = 0,1
state = RUNNING

# Pre-start set up
theMap = TheMap(pixWidth,pixHeight,pixel)     # initalises theMap with blobs
theMap.draw(screen)

# -------- Main Program Loop -----------
while not done:
    
    # --- Event loop (not yet fully useful)
    
    for event in pygame.event.get():        # did user do something
        if event.type == pygame.KEYDOWN:    # if user pushed any key
            if event.key == pygame.K_SPACE: state = not state
            if event.key == pygame.K_ESCAPE:
                done = True
                state = PAUSE
            
    if state == RUNNING:
        # --- Game logic
        theMap.moveBlobs()  # moves the Blobs around in the array
        
        theMap.actBlobs()  # aggressive Blobs eat Green ones, they all reproduce
        
        # --- Clear the screen
        screen.fill(BLACK)
     
        # --- Drawing new screen
        theMap.draw(screen)
        
        # --- Update screen with what was drawn
        pygame.display.flip()
     
        # --- Limits frames per second
        clock.tick(10)
