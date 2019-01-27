import pygame, os, random, sys

pygame.init()
tile_width = 130
tile_height = 150

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        return pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x , tile_height * pos_y)
        self.mask = pygame.mask.from_surface(self.image)

    def apply(self):
        self.rect.x -= player.speed

    def update(self):
        if pygame.sprite.collide_mask(self, player):
            player.speed = 0


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(pos_x, pos_y)
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 20
        self.jump = False
        self.jump_Count = 10
    def update(self):
        self.rect.x += self.speed

def generate_level(level):
    new_player, x, y = None, None, None
    for x in range(len(level)):
        if level[x] == '.':
            pass
        elif level[x] == '#':

            Tile('wall', x, 5)
    # вернем игрока, а также размер поля в клетках
    return x, y


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    return level_map[0]



level = load_level('level_name1.txt')

tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
size = width, height = 1920, 1080
screen = pygame.display.set_mode(size)
fon = load_image('screen_2.png')
f = fon.get_rect()
player_image = load_image('player_1.png')
all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player = Player(300, 600)
running = True
fps = 60
clock = pygame.time.Clock()
x, y = generate_level(level)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if not (player.jump):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump = True
    else:
        if player.jump_Count >= -10:
            if player.jump_Count < 0:
                player.rect.y += (player.jump_Count ** 2)
            else:
                player.rect.y -= (player.jump_Count ** 2)
            player.jump_Count -= 1
        else:
            player.jump_Count = 10
            player.jump = False
    for i in tiles_group:
        i.update()
        i.apply()
    if player.speed!=0:
        f[0]-= player.speed - 14
    screen.blit(fon, f)
    all_sprites.draw(screen)

    pygame.display.flip()

pygame.quit()
