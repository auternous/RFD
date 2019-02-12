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


def load_music(info):
    pygame.mixer.music.load('data/sounds/Menu.mp3')
    pygame.mixer.music.set_volume(info['settings']['volume'])
    pygame.mixer.music.play(-1)


def Paper(screen):
    image = load_image("Level_1/Starting.png")

    screen.blit(image, (0, 0))
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            if event.type == pygame.KEYDOWN:
                running = False

        pygame.display.flip()


def start_dead_win_scene(screen, dead=True):
    images_dead_list = []
    for i in range(1, 10):
        images_dead_list.append(load_image('Dead_Win/Dark_{}.png'.format(i)))
    if dead:
        images_dead_list.append(load_image('Dead_Win/Dead.png'))
    else:
        images_dead_list.append(load_image('Dead_Win/Level_passed.png'))
    animCount = 0
    fps = 5
    clock = pygame.time.Clock()
    screen3 = pygame.Surface(screen.get_size())
    screen3.blit(screen, (0, 0))
    while True:
        clock.tick(fps)
        screen2 = pygame.Surface(screen.get_size())
        screen2.blit(screen3, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return False
        if animCount < 10:
            screen2 = pygame.Surface(screen.get_size())
            screen2.blit(screen3, (0, 0))
            screen2.blit(images_dead_list[animCount % 10], (0, 0))
            screen.blit(screen2, (0, 0))
            animCount += 1

        pygame.display.flip()
