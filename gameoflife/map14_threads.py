#!/usr/bin/python3

import threading
import queue

from map14 import *

QUEUE_SIZE = 500
FRAMES_PER_SEC = 6

class ComputeThread(threading.Thread):
    def __init__(self,mapObject,storeQueue):
        super().__init__()
        self.myQueue = storeQueue
        self.counter = 0
        self.Map = mapObject
        
    def run(self):
        while True:
            self.Map.moveBlobs()  # moves the Blobs around in the array
            self.Map.actBlobs()   # aggressive Blobs eat Green ones, they all reproduce
            self.myQueue.put(self.Map.draw(),block=True)
        
class OutputThread(threading.Thread):
    def __init__(self, storeQueue):
        super().__init__()
        self.myQueue = storeQueue
        self.state = RUNNING
        
    def run(self):
        while True:
            self.main_loop()
            print(self.myQueue.qsize())
                
    def main_loop(self):
        # -------- Main Program Loop -----------
        if True:
            # --- Event loop (not yet fully useful)
            for event in pygame.event.get():        # did user do something
                if event.type == pygame.KEYDOWN:    # if user pushed any key
                    if event.key == pygame.K_SPACE:
                        self.state = not self.state
                    if event.key == pygame.K_ESCAPE:
                        """ NEED TO STOP THE OTHER THREAD HERE """
                        exit()
                        self.state = PAUSE
                    
            if self.state == RUNNING:
                # --- Game logic
                
                # --- Drawing new screen
                image = self.myQueue.get(block=True)
                screen.blit(image,[0,0])
                
                # --- Update screen with what was drawn
                pygame.display.update()
             
                # --- Limits frames per second, taking into account time spent on computing
                clock.tick(FRAMES_PER_SEC - clock.get_rawtime())

         
framesQueue = queue.Queue(QUEUE_SIZE)

theMap = TheMap(pixWidth,pixHeight,pixel) # initalises theMap with blobs

thread1 = ComputeThread(theMap,framesQueue)
thread1.start()

thread2 = OutputThread(framesQueue)
thread2.start()
