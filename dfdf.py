import pygame, os, random, sys
from pygame.locals import *


def start_level_1(screen):
    tile_width = 130
    tile_height = 150

    def load_image(name, colorkey=None):
        fullname = os.path.join('data', name)
        try:
            image = pygame.image.load(fullname).convert_alpha()



            return image
        except pygame.error as message:
            print('Cannot load image:', name)
            raise SystemExit(message)

    class Tile(pygame.sprite.Sprite):
        def __init__(self, tile_type, pos_x, pos_y):
            super().__init__(tiles_group, all_sprites)
            self.image = tile_images[tile_type]
            self.rect = self.image.get_rect().move(
                tile_width * pos_x, tile_height * pos_y)
            self.mask = pygame.mask.from_surface(self.image)

        def update(self):
            if pygame.sprite.collide_mask(self, player):
                player.speed = 0
                player.jump = False

    class Player(pygame.sprite.Sprite):
        player_image = load_image('player_1.png')

        def __init__(self, pos_x, pos_y):
            super().__init__(player_group, all_sprites)
            self.image = Player.player_image
            self.rect = self.image.get_rect().move(pos_x, pos_y)
            self.mask = pygame.mask.from_surface(self.image)
            self.speed = 10
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

    class BackGround(pygame.sprite.Sprite):
        backgrounds = load_image('screen_2.jpg')

        def __init__(self):
            super().__init__(background_sprites, all_sprites)
            self.image = BackGround.backgrounds
            self.rect = self.image.get_rect()

    class Camera:
        def __init__(self):
            self.dx = 0
            self.dy = 0

        def apply(self, obj):
            if obj.rect.x < -obj.rect[2] and obj in tiles_group:
                all_sprites.remove(obj)
            elif obj in background_sprites and player.speed != 0:
                obj.rect.x += self.dx

            else:
                obj.rect.x += self.dx
                obj.rect.y += self.dy

        def update(self, target):
            self.dx = -(target.rect.x - target.rect.w)
            pass
    def load_level(filename):
        filename = "data/" + filename
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]
        return level_map[0]

    level = load_level('level_name1.txt')

    tile_images = {
        'wall': load_image('box.png'),
    }

    background_sprites = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    camera = Camera()
    background = BackGround()
    player = Player(screen.get_width()//4,screen.get_height()//1.8)
    running = True
    fps = 120
    clock = pygame.time.Clock()
    x, y = generate_level(level)
    while running:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if not (player.jump):
            if pygame.key.get_pressed()[pygame.K_SPACE]:
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

        player.update()
        camera.update(player)
        for i in all_sprites:
            camera.apply(i)
            if i in tiles_group:
                i.update()

        all_sprites.draw(screen)

        pygame.display.flip()


def main():
    pygame.init()
    size = user_x, user_y = 1920, 1080

    screen = pygame.display.set_mode((user_x, user_y), RESIZABLE)
    start_level_1(screen)


main()
