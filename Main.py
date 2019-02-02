import pygame, os, random, sys
from pygame.locals import *
from execution import *
from load_functions import *




def start_settings(screen):
    pass


def Start_level(screen, level_num):


    class Box(pygame.sprite.Sprite):
        image = pygame.transform.scale(load_image('box.png'),
                                              (int(screen.get_width() // 15), int(screen.get_height() // 7 )))
        tile_width = int(screen.get_width() // 9)
        tile_height = int(screen.get_height() // 6.5)
        def __init__(self, pos_x, pos_y):
            super().__init__(tiles_group, all_sprites)
            self.image = Box.image
            self.rect = self.image.get_rect().move(
                Box.tile_width * pos_x, Box.tile_height * pos_y)
            self.mask = pygame.mask.from_surface(self.image)

        def update(self):
            if pygame.sprite.collide_mask(self, player):
                player.speed = 0
                player.jump = False

    class Player(pygame.sprite.Sprite):
        image = pygame.transform.scale(load_image('player_1.png'),
                                       (int(screen.get_width() // 10), int(screen.get_height() // 3)))
        def __init__(self, pos_x, pos_y):
            super().__init__(player_group, all_sprites)
            self.image = Player.image
            self.rect = self.image.get_rect().move(pos_x, pos_y)
            self.mask = pygame.mask.from_surface(self.image)
            self.speed = screen.get_width()// 128
            self.jump = False
            self.jump_Count = screen.get_width()// 192

        def update(self):
            self.rect.x += self.speed

            if not (player.jump):
                if pygame.key.get_pressed()[pygame.K_SPACE]:
                    player.jump = True
            else:
                if player.jump_Count >= -(screen.get_width() // 192):
                    if player.jump_Count < 0:
                        player.rect.y += (player.jump_Count ** 2)
                    else:
                        player.rect.y -= (player.jump_Count ** 2)
                    player.jump_Count -= 1
                else:
                    player.jump_Count = (screen.get_width() // 192)
                    player.jump = False

    def generate_level(level):
        new_player, x, y = None, None, None
        for x in range(len(level)):
            if level[x] == '.':
                pass
            elif level[x] == '#':
                Box( x, 5)
        # вернем игрока, а также размер поля в клетках
        return x, y

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



    level = load_level('level_name1.txt')

    background_sprites = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()

    camera = Camera()
    background = BackGround('screen.jpg',[background_sprites, all_sprites], screen)
    player = Player(screen.get_width()//4,screen.get_height()//1.8)
    clock = pygame.time.Clock()
    generate_level(level)

    running = True
    fps = 120
    while running:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pass

        screen.fill((0,0,0))
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
    size = user_x, user_y = 1366, 768
    screen = pygame.display.set_mode((user_x, user_y), RESIZABLE)


    all_sprites = pygame.sprite.Group()
    menu = pygame.sprite.Group()
    button = pygame.sprite.Group()
    main_menu = BackGround("Комната.png", [menu,all_sprites], screen)
    play = Button('Play',(screen.get_rect().centerx, 100), [button,all_sprites])
    settings = Button('Settings', (screen.get_rect().centerx, 150), [button,all_sprites])
    quit = Button('Quit', (screen.get_rect().centerx, 200), [button,all_sprites])



    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                for i in button:
                    i.update(event.pos)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i in button:
                        if i.apply(event.pos) == 'Play':
                            Start_level(screen, 1)
                        elif i.apply(event.pos) == 'Settings':
                            start_settings(screen)
                        elif i.apply(event.pos) == 'Quit':
                            running = False
                            sys.exit()
        all_sprites.draw(screen)

        pygame.display.flip()
main()
