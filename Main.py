import pygame, os, random, sys, json
from pygame.locals import *
from pygame import mixer
from execution import *
from load_functions import *


def start_settings(screen, size, info):
    all_sprites = pygame.sprite.Group()
    button = pygame.sprite.Group()
    button_list = []
    num_button = 0
    full_screen_flag = info['settings']['fullscreen']
    sound_tap = mixer.Sound('data/sounds/sound_tap.wav')
    settings_menu = BackGround("Settings/pause_settings.png", [all_sprites], screen)

    ok = Button('settings/ok', (1920 // 3, 780), [button, all_sprites], 1)
    back = Button('settings/back', (1920 // 1.8, 780), [button, all_sprites], 2)

    if full_screen_flag:
        full_screen = Button_Fullscreen('settings/full_screen_1', (1920 // 3.7, 270), [button, all_sprites], 3, info)
    else:
        full_screen = Button_Fullscreen('settings/full_screen_0', (1920 // 3.7, 270), [button, all_sprites], 3, info)
    print(info['settings']['volume'])
    if info['settings']['volume'] == 0:
        volume = Button_Volume('settings/volume_0', (1920 // 2.9, 500), [button, all_sprites], 5, info)
    elif info['settings']['volume'] == 0.25:
        volume = Button_Volume('settings/volume_1', (1920 // 2.9, 500), [button, all_sprites], 5, info)
    elif info['settings']['volume'] == 0.50:
        volume = Button_Volume('settings/volume_2', (1920 // 2.9, 500), [button, all_sprites], 5, info)
    elif info['settings']['volume'] == 0.75:
        volume = Button_Volume('settings/volume_3', (1920 // 2.9, 500), [button, all_sprites], 5, info)
    elif info['settings']['volume'] == 1:
        volume = Button_Volume('settings/volume_4', (1920 // 2.9, 500), [button, all_sprites], 5, info)
    screen_resolution = Button('settings/screen_resolution_1920', (1920 // 4.3, 20), [button, all_sprites], 4, True)

    for i in [screen_resolution, full_screen, volume, ok, back]:
        button_list.append(i)

    running = True

    while running:
        screen2 = pygame.Surface((1920, 1080))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()

            if event.type == pygame.KEYDOWN:
                sound_tap.play()
                if event.key == pygame.K_UP:
                    button_list[num_button % 5].apply()
                    num_button -= 1
                    button_list[num_button % 5].apply()
                elif event.key == pygame.K_DOWN:
                    button_list[num_button % 5].apply()
                    num_button += 1
                    button_list[num_button % 5].apply()
                elif event.key == 13:
                    for i in button_list:
                        if i.num == 1 and i.flag:
                            info['settings']['fullscreen'] = full_screen_flag
                            info['settings']['volume'] = volume.dict_key[volume.filename]
                            mixer.music.set_volume(info['settings']['volume'])
                            screen = update_settings(info, size)
                        elif i.num == 2 and i.flag:
                            running = False
                        elif i.num == 3 and i.flag:
                            if full_screen_flag:
                                i.filename = 'settings/full_screen_0'
                                i.image_change()
                                full_screen_flag = False
                            elif not full_screen_flag:
                                i.filename = 'settings/full_screen_1'
                                i.image_change()
                                full_screen_flag = True

                        elif i.num == 4 and i.flag:
                            pass
                        elif i.num == 5 and i.flag:
                            i.change()
        for i in button_list:
            i.update()
        all_sprites.draw(screen2)
        screen2 = pygame.transform.scale(screen2, (int(screen.get_width()), int(screen.get_height())))
        screen.blit(screen2, (0, 0))

        pygame.display.flip()


def start_level(screen, level_num):
    class Box(pygame.sprite.Sprite):
        image = pygame.transform.scale(load_image('Мусорный бак.png'),
                                       (int(screen.get_width() // 15), int(screen.get_height() // 7)))
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
                player.run_mode = False
                player.jump = False

    class Player(pygame.sprite.Sprite):
        image = load_image('person/player_stop.png')
        images_run = [load_image('person/run_animation/run_1.png'), load_image('person/run_animation/run_2.png'),
                      load_image('person/run_animation/run_3.png'),
                      load_image('person/run_animation/run_4.png')]


        def __init__(self, pos_x, pos_y):
            super().__init__(player_group, all_sprites)
            self.animCount = 0
            self.image = Player.image
            self.rect = self.image.get_rect().move(pos_x, pos_y)
            self.mask = pygame.mask.from_surface(self.image)
            self.walk_mode = True
            self.run_mode = False
            self.speed = screen.get_width() // 128
            self.jump = False
            self.jump_Count = screen.get_width() // 192

        def update(self):
            if self.run_mode:
                self.rect.x += self.speed
            if self.animCount + 1>= 60:
                self.animCount = 0
            if self.run_mode and not self.jump:
                self.image = Player.images_run[int(self.animCount % 4)]
                self.animCount += 1
            if player.walk_mode:
                if pygame.key.get_pressed()[pygame.K_LEFT]:
                    player.rect.x -= 5
                if pygame.key.get_pressed()[pygame.K_RIGHT]:
                    player.rect.x += 5
            if not self.jump:
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
                Box(x, 5)
        # вернем игрока, а также размер поля в клетках
        return x, y

    class Camera:
        def __init__(self):
            self.dx = 0
            self.dy = 0

        def apply(self, obj):
            if obj.rect.x < -obj.rect[2] and obj in tiles_group:
                all_sprites.remove(obj)
            elif obj in background_sprites and player.run_mode:
                obj.rect.x += self.dx + 10

            else:
                obj.rect.x += self.dx
                obj.rect.y += self.dy

        def update(self, target):

            self.dx = -(target.rect.x - target.rect.w)

    level = load_level('levels/level_name{}.txt'.format(str(level_num)))

    background_sprites = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()

    camera = Camera()
    background = BackGround('screen.jpg', [background_sprites, all_sprites], screen)
    player = Player(screen.get_width() // 4, screen.get_height() // 1.8)
    clock = pygame.time.Clock()
    generate_level(level)

    running = True
    fps = 60
    while running:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pass


        screen.fill((255, 255, 255))
        player.update()
        camera.update(player)
        for i in all_sprites:
            camera.apply(i)
            if i in tiles_group:
                i.update()

        all_sprites.draw(screen)

        pygame.display.flip()


def main():
    with open('Settings.json', 'r', encoding='utf-8') as f_obj:
        info = json.load(f_obj)

    pygame.init()
    mixer.pre_init(44100, -16, 1, 512)
    mixer.init()

    mixer.music.load('data/sounds/music.mp3')
    mixer.music.set_volume(info['settings']['volume'])
    mixer.music.play(-1)
    sound_tap = mixer.Sound('data/sounds/sound_tap.wav')
    sound_tap.set_volume(0.2)


    size = user_x, user_y = info['settings']["scr_res"]
    screen = pygame.display.set_mode((user_x, user_y), RESIZABLE)

    all_sprites = pygame.sprite.Group()
    menu = pygame.sprite.Group()
    button = pygame.sprite.Group()
    button_list = []

    backgroung = BackGround("main_menu/Комната.png", [menu, all_sprites], screen)
    play = Button('main_menu/play', (1920 // 2.8, 90), [button, all_sprites], 1, True)
    settings = Button('main_menu/settings', (1920 // 3.4, 360), [button, all_sprites], 2)
    quit = Button('main_menu/quit', (1920 // 2.9, 590), [button, all_sprites], 3)
    backgroung_dark = BackGround("main_menu/Затемнение.png", [menu, all_sprites], screen)

    num_button = 0

    for i in [play, settings, quit]:
        button_list.append(i)
    running = True
    while running:
        screen2 = pygame.Surface((1920, 1080))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                sound_tap.play()
                if event.key == pygame.K_UP:
                    button_list[num_button % 3].apply()
                    num_button -= 1
                    button_list[num_button % 3].apply()
                elif event.key == pygame.K_DOWN:
                    button_list[num_button % 3].apply()
                    num_button += 1
                    button_list[num_button % 3].apply()
                elif event.key == 13:
                    for i in button_list:
                        if i.num == 1 and i.flag:
                            start_level(screen, 1)
                        elif i.num == 2 and i.flag:
                            start_settings(screen, size, info)
                            with open('Settings.json', 'w', encoding='utf-8') as f_obj:
                                json.dump(info, f_obj, ensure_ascii=False)
                        elif i.num == 3 and i.flag:
                            running = False
                            sys.exit()
        for i in button_list:
            i.update()
        all_sprites.draw(screen2)
        screen2 = pygame.transform.scale(screen2, (user_x, user_y))
        screen.blit(screen2, (0, 0))
        pygame.display.flip()


main()
