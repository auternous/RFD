import pygame, os, sys
from pygame.locals import *


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    return level_map[0]


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        return pygame.image.load(fullname).convert_alpha()

    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)


def update_settings(info, size):
    if info['settings']['fullscreen']:
        screen = pygame.display.set_mode(size, FULLSCREEN)
    elif not info['settings']['fullscreen']:
        screen = pygame.display.set_mode(size, RESIZABLE)



    return screen

def load_sound_tap():
    sound_tap = pygame.mixer.Sound('data/sounds/sound_tap.wav')
    sound_tap.set_volume(0.2)
    return sound_tap


def Paper(screen):
    image = load_image("Мусорный бак.png")

    screen.blit(image, (0, 0))
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == 13:
                    running = False

        pygame.display.flip()