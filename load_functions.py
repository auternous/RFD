import pygame, os

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

