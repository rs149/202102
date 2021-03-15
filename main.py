import pygame
from pygame.locals import *
from mod import Field

def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("sp")
    field = Field()
    field.draw(pygame, screen)
    keepRun = True
    while(keepRun):
        pygame.time.wait(10)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                keepRun = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                field.click(event.pos, pygame, screen)

if __name__ == "__main__":
    main()
