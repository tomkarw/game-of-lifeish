#!/usr/bin/python3

import pygame
import numpy
import random
import operator # attrgetter
import namedlist # namedtuple

import multiprocessing
import queue

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)
YELLOW   = ( 255, 255,   0)
AQUA     = (   0, 255, 255)
BLUE     = (   0,   0, 255)
PURPLE   = ( 128,   0, 255)

COLORS = (GREEN, RED, PURPLE, BLUE, YELLOW, AQUA)

# VARIABLES

blobsPerTile = 5
nColonies = 1 + 5

life = 12		        # how many turns it takes for aggresive blob to die
span_chance = 0.15		# percentage chance of green blob spanning offspring

done = False
RUNNING, PAUSE = 0,1

state = RUNNING

# CLASSES

Blob = namedlist.namedlist('Blob','strength life age')
    
class TheMap:
    """Map stores screen size as well as 3D array of Blobs, also includes funtions for interaction of Blobs"""
    
    def __init__(self,pixWidth,pixHeight,pixel):
        """Initialises the map of given width and height with 1000 Blobs of each species"""
        
        self.pixWidth = pixWidth
        self.pixHeight = pixHeight
        self.pixel = pixel
        self.turn = 0
        
        self.count = [ 0 for i in range(nColonies) ]
        self.avgStr = [ 0 for i in range(nColonies) ]
        
        self.array = [ [ [ [] for z in range(nColonies) ] for y in range(pixHeight) ] for x in range(pixWidth) ]
        
        for n in range(1000):
                x = random.randrange(0,pixWidth)
                y = random.randrange(0,pixHeight)
                self.array[x][y][0].append(True)
        
        for i in range(1,nColonies):
            for n in range(round(2000/nColonies)):
                x = random.randrange(0,pixWidth)
                y = random.randrange(0,pixHeight)
                
                s = numpy.random.normal(50,1)                           # strength set as a normal distribution 
                l = numpy.random.normal(life,1) + pow(2,(x-50)/5)       # life span altered by plus/minus normal distribution
                a = random.random()*4
                self.array[x][y][i].append(Blob(s,l,a))
    
                  
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
                        # --- Count the blob that is beeing moved
                        self.count[i] += 1
                        # --- Sum strength of all colonies exept the vegetation
                        if(i!=0):
                            self.avgStr[i] += self.array[x][y][i][-1].strength
                        
                        # --- Move the blob in random direction
                        xx = x + random.choice([-1,0,1])
                        yy = y + random.choice([-1,0,1])
                        
                        # --- Check if blob is out of bounds (map loops N-S and W-E)
                        if xx >= self.pixWidth:
                            xx = 0
                        elif xx < 0:
                            xx = self.pixWidth - 1
                        if yy >= self.pixHeight:
                            yy = 0
                        elif yy < 0:
                            yy = self.pixHeight - 1
                        
                        # --- Delete if there are more than some set number (see VARIABLES) of blobs at a tile
                        
                        if len(tmp_array[xx][yy][i]) < blobsPerTile:
                            tmp_array[xx][yy][i].append(self.array[x][y][i].pop())
                        else:
                            break
                        
            if self.count[i] == 0:   
                a = 0
            else:                   
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
                        for blob in self.array[x][y][i]:
                            blob.age += 1
                            if blob.age > life:
                                self.array[x][y][i].remove(blob)
                    
                    # --- Resolve conflicts between aggressive Blobs
                    strength = [ 0 for _ in range(1,nColonies) ]
                    
                    for i in range(nColonies-1):
                        strength[i] = sum(blob.strength for blob in self.array[x][y][i+1])
                                    
                    winner = numpy.argmax(strength) + 1   
                    
                    for i in range(1,nColonies):
                        if i != winner:
                            del self.array[x][y][i][:] 
                    
                    
                    # --- Sort the agroBlobs by strenght (increasing)
                    for i in range(1,nColonies):
                        self.array[x][y][i].sort(key=operator.attrgetter('strength'),reverse=True) 
                    
                    # --- Let the winner eat green Blobs
                    while self.array[x][y][winner] and self.array[x][y][0]:
                        self.array[x][y][0].pop()
                        
                        # --- And a chance to reproduce
                        s = self.array[x][y][winner][-1].strength
                        a = self.array[x][y][winner][-1].age
                        if random.random() > s/100 * .3 + a/life * .1:
                            s = self.array[x][y][winner][-1].strength + numpy.random.normal(0,10)

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
                            
                            if len(tmp_array[xx][yy][winner]) < blobsPerTile:
                                tmp_array[xx][yy][winner].append(Blob(s,life,0))
                            else:
                                break
                                
                        tmp_array[x][y][winner].append(self.array[x][y][winner].pop())
                    
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
                            
                            if len(tmp_array[xx][yy][0]) < blobsPerTile:        
                                tmp_array[xx][yy][0].append(self.array[x][y][0][-1])
                            else:
                                break
                                
                        if len(tmp_array[x][y][0]) < blobsPerTile:    
                            tmp_array[x][y][0].append(self.array[x][y][0].pop())
                        else:
                            break    
                    
                    # --- Transfer the remaining agroBlobs to new array
                    for i in range(1,nColonies):
                        # self.array[x][y][i].reverse()
                                
                        while self.array[x][y][i]:
                            if len(tmp_array[x][y][i]) < blobsPerTile:
                                tmp_array[x][y][i].append(self.array[x][y][i].pop())
                            else:
                                break
        
        # --- Update the array
        self.array = tmp_array
        
        # --- Add to turn count
        self.turn += 1
                    
    def draw(self):
        """Draws the map with blobs"""
        
        image = pygame.Surface(size)
        
        for x in range(self.pixWidth):
            for y in range(self.pixHeight):
                xy = [x*self.pixel,y*self.pixel,self.pixel,self.pixel]
                
                for i in range(nColonies):
                    if self.array[x][y][i]:
                        pygame.draw.rect(image, COLORS[i], xy)
        
        pygame.draw.rect(image,BLACK,[0,0,200,25 + 20*nColonies])
        pygame.draw.rect(image,WHITE,[0,0,200,25 + 20*nColonies],2)
        
        label = myfont.render('Size', 1, WHITE)
        image.blit(label, (3,  1))
        label = myfont.render('avgStr', 1, WHITE)
        image.blit(label, (80,  1))
        
        for i in range(nColonies):
            label = myfont.render(str(self.count[i]), 1, COLORS[i])
            image.blit(label, (3, 21 + 20*i))
        
        for i in range(1,nColonies):
            label = myfont.render("{:.3f}".format(self.avgStr[i]), 1, COLORS[i])
            image.blit(label, (80, 21 + 20*i))
        
        return image

def computeProcess(Map,framesQueue):
    while True:
        Map.moveBlobs()  # moves the Blobs around in the array
        Map.actBlobs()   # aggressive Blobs eat Green ones, they all reproduce
        #print('new frame computed')
        image = pygame.image.tostring(Map.draw(),'RGB')
        framesQueue.put(image,block=True)

def outputProcess(framesQueue):
    
    def main_loop(state):
    # -------- Main Program Loop -----------
        
        # --- Event loop (not yet fully useful)
        for event in pygame.event.get():        # did user do something
            if event.type == pygame.KEYDOWN:    # if user pushed any key
                if event.key == pygame.K_SPACE:
                    state = not state
                if event.key == pygame.K_ESCAPE:
                    " NEED TO STOP THE OTHER PROCESS HERE "
                    exit()
                    state = PAUSE
        if state == RUNNING:
            # --- Game logic
            
            # --- Drawing new screen
            image = pygame.image.fromstring(framesQueue.get(block=True),size,'RGB')
            screen.blit(image,[0,0])
                
            # --- Update screen with what was drawn
            pygame.display.update()
             
            # --- Limits frames per second, taking into account time spent on computing
            clock.tick(3)
    
    
    state = RUNNING
    
    while True:
        print(framesQueue.qsize())
        main_loop(state)
        
        
if __name__ == "__main__":

    # Set window parameters
    pygame.init()
    size = width, height = 500, 500
    pixel = 5
    pixWidth, pixHeight = int(width/pixel), int(height/pixel)
    pygame.display.set_caption("Game of Life")
    screen = pygame.display.set_mode(size)
    keys_down = set()
    myfont = pygame.font.SysFont("monospace", 25)

    clock = pygame.time.Clock() # Used to manage how fast the screen updates

    framesQueue = multiprocessing.Queue(500)

    theMap = TheMap(pixWidth,pixHeight,pixel) # initalises theMap with blobs

    process1 = multiprocessing.Process(target=computeProcess, args=(theMap,framesQueue))
    process1.start()

    process2 = multiprocessing.Process(target=outputProcess, args=(framesQueue,))
    process2.start()
