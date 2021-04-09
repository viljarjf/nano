import sys, pygame
import numpy as np
from numba import jit
import time

pygame.init()

size = width, height = 1000, 1000
black = 0
white = 2**24 -1 # (255, 255, 255)

radius = 10


@jit(nopython = True)
def calc(arr):
    iter1 = np.arange(1, height-1)
    iter2 = np.arange(1, width-1)
    np.random.shuffle(iter1)
    np.random.shuffle(iter2)
    for i in iter1:
        for j in iter2:
            if arr[i,j] == white:
                n = np.random.randint(4)
                if n == 0:
                    if arr[i-1, j] == black:
                        arr[i-1, j] = white
                        arr[i, j] = black
                if n == 1:
                    if arr[i+1, j] == black:
                        arr[i+1, j] = white
                        arr[i, j] = black
                if n == 2:
                    if arr[i, j-1] == black:
                        arr[i, j-1] = white
                        arr[i, j] = black
                if n == 3:
                    if arr[i, j+1] == black:
                        arr[i, j+1] = white
                        arr[i, j] = black
    return arr

# compile
a = calc(np.zeros(size))
del a

screen = pygame.display.set_mode(size)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()       

    if pygame.mouse.get_pressed()[0]:
        pygame.draw.circle(screen, white, (pygame.mouse.get_pos()), radius)

    
    arr = pygame.surfarray.array2d(screen)
    
    arr = calc(arr)

    pygame.surfarray.blit_array(screen, arr)
    pygame.display.flip()
    