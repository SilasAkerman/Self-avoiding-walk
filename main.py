import pygame
import sys

from walker import Walker

def main():
    pygame.init()
    sys.setrecursionlimit(10**6)

    WIN = pygame.display.set_mode((1400, 700))
    FPS = 0
    SPACING = 5

    while True:
        Entity = Walker()
        result = Entity.run(WIN, FPS, SPACING)
        if result:
            break



if __name__ == "__main__":
    main()