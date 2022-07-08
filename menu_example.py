import pygame
import sys
from pygame.locals import *

width, height = 500, 700

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

screen.fill((100, 100, 100))

def place_text(str, color, center):
    text = pygame.font.SysFont('impact', 20)
    text_surf = text.render(str, True, color)
    text_rect = text_surf.get_rect()
    text_rect.center = center
    screen.blit(text_surf, text_rect)
    return text_rect

def click_button():
    if place_text('example shit', (255, 0, 0), (200, 200)).collidepoint((mx, my)):
        if click:
            print('i hope this workjed')
    if place_text('example shit', (0, 0, 250), (width / 3, height / 4)).collidepoint((mx, my)):
        if click:
            print('i hope this example works')

while 1:
    pygame.init()
    mx, my = pygame.mouse.get_pos()
    click = False

    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            click = True

    str = 'Testing this shit'
    text = pygame.font.SysFont('impact', 20)
    text_surf = text.render(str, True, (255, 255, 255))
    text_rect = text_surf.get_rect()
    text_rect.center = (100, 100)
    screen.blit(text_surf, text_rect)

    if text_rect.collidepoint((mx, my)):
        if click:
            print('is this thing working')

    # if place_text('example shit', (255, 0, 0), (200, 200)).collidepoint((mx, my)):
    #     if click:
    #         print('i hope this workjed')
    click_button()

    pygame.display.update()
    clock.tick(30)