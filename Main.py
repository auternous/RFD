import json
import random
from pygame import mixer
from execution import *
from load_functions import *


def start_pause(screen):
    sound_tap = load_sound('data/sounds/sound_tap.wav')  # включение фоновой музыки
    all_sprites_pause = pygame.sprite.Group()
    background_sprites_pause = pygame.sprite.Group()
    button = pygame.sprite.Group()
    button_list = []  # список кнопок
    num_button = 0  # номер кнопки

    background = BackGround('Pause/pause_settings.png',
                            [background_sprites_pause, all_sprites_pause], screen)
    continue_ = Button('Pause/continue', (1920 // 2.8, 150), [button, all_sprites_pause], 1, True)
    main_menu = Button('Pause/main_menu', (1920 // 3.4, 500), [button, all_sprites_pause], 2)
    # определяем кнопки и фон

    for i in [continue_, main_menu]:
        button_list.append(i)  # добавляем кнопки в список

    running_pause = True

    while running_pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()  # выход
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    sound_tap.play()
                    button_list[num_button % 2].apply()
                    num_button -= 1
                    button_list[num_button % 2].apply()  # обрабатываем нажатие кнопки "up"
                elif event.key == pygame.K_DOWN:
                    sound_tap.play()
                    button_list[num_button % 2].apply()
                    num_button += 1
                    button_list[num_button % 2].apply()  # обрабатываем нажатие кнопки "down"
                elif event.key == 13:
                    sound_tap.play()
                    for i in button_list:
                        if i.num == 1 and i.flag:  # обрабатываем нажатие кнопки "enter"
                            return True
                        if i.num == 2 and i.flag:
                            running_pause = False
                            return False

        for i in button_list:
            i.update()
        all_sprites_pause.draw(screen)
        pygame.display.flip()


def start_settings(screen, size, info):
    all_sprites = pygame.sprite.Group()
    button = pygame.sprite.Group()
    button_list = []
    num_button = 0
    full_screen_flag = info['settings']['fullscreen']

    sound_tap = load_sound('data/sounds/sound_tap.wav')

    settings_menu = BackGround("Settings/pause_settings.png", [all_sprites], screen)
    ok = Button('settings/ok', (1920 // 3, 780), [button, all_sprites], 1)
    back = Button('settings/back', (1920 // 1.8, 780), [button, all_sprites], 2)

    if full_screen_flag:
        full_screen = Button_Fullscreen('settings/full_screen_1', (1920 // 3.7, 270), [button, all_sprites], 3, info)
    else:
        full_screen = Button_Fullscreen('settings/full_screen_0', (1920 // 3.7, 270), [button, all_sprites], 3, info)
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
    screen_resolution = Button('settings/screen_resolution_1920', (1920 // 4.3, 20), [button, all_sprites], 4,
                               True)  # эта кнопка ждёт фикса
    # определяем нужные кнопки
    for i in [screen_resolution, full_screen, volume, ok, back]:
        button_list.append(i)

    running = True

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP:  # обрабатываем нажатие кнопок
                    sound_tap.play()
                    button_list[num_button % 5].apply()
                    num_button -= 1
                    button_list[num_button % 5].apply()
                elif event.key == pygame.K_DOWN:
                    sound_tap.play()
                    button_list[num_button % 5].apply()
                    num_button += 1
                    button_list[num_button % 5].apply()
                elif event.key == 13:
                    sound_tap.play()
                    for i in button_list:
                        if i.num == 1 and i.flag:
                            info['settings']['fullscreen'] = full_screen_flag
                            info['settings']['volume'] = volume.dict_key[volume.filename]
                            mixer.music.set_volume(info['settings']['volume'])
                            screen = update_settings(info, size)  # меняем настройки и сохраняем в переменной
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
        all_sprites.draw(screen)

        pygame.display.flip()


def start_level(screen, level_num, info):
    class Box(pygame.sprite.Sprite):
        image_list = [load_image('Level_1/Block_1.png'),
                      load_image('Level_1/Block_2.png'),
                      load_image('Level_1/Block_3.png'),
                      load_image('Level_1/Block_4.png')]

        tile_width = int(screen.get_width() // 9)
        tile_height = int(screen.get_height() // 6.5)

        def __init__(self, pos_x, pos_y):
            super().__init__(tiles_group, all_sprites)
            self.image = random.choice(Box.image_list)

            self.rect = self.image.get_rect().move(
                Box.tile_width * pos_x, Box.tile_height * pos_y + 8)
            self.mask = pygame.mask.from_surface(self.image)

        def update(self):
            if pygame.sprite.collide_mask(self, player):
                player.run_mode = False
                player.jump = False
                player.walk_mode = False

    class Player(pygame.sprite.Sprite):
        image = load_image('person/player_stop.png')
        images_run = []
        images_walk = [load_image('person/run_animation/run_1.png'), load_image('person/run_animation/run_3.png')]
        for i in range(1, 9):
            images_run.append(load_image('person/run_animation/run_{}.png'.format(i)))

        def __init__(self, pos_x, pos_y):
            super().__init__(player_group, all_sprites)
            self.animCount = 0
            self.image = Player.image
            self.rect = self.image.get_rect().move(pos_x, pos_y)
            self.mask = pygame.mask.from_surface(self.image)
            self.walk_mode = True  # ходьба
            self.run_mode = False  # бег
            self.speed = 17
            self.jump = False  # прыжок
            self.jump_Count = screen.get_width() // 192  # граница прыжка
            self.jump_mode = False  # можно ли осуществить прыжок
            self.n = 0
            self.finish = False  # конец уровня

        def update(self):

            if self.animCount + 1 >= 60:
                self.animCount = 0

            if self.run_mode and not self.jump:
                self.image = Player.images_run[int(self.animCount % 8)]
                self.animCount += 1

            if self.walk_mode:
                self.rect.x += self.speed - 10
                self.animCount += 1
                if self.animCount % 5 == 0:
                    self.image = Player.images_walk[int(self.animCount % 2)]

            if self.run_mode:
                self.rect.x += self.speed

            if self.jump_mode and not player.jump:

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        player.jump = True
                        print(1)

            elif self.jump:
                if player.jump_Count >= -(screen.get_width() // 192):
                    if player.jump_Count < 0:
                        player.rect.y += (player.jump_Count ** 2)
                    else:
                        player.rect.y -= (player.jump_Count ** 2)
                    player.jump_Count -= 1
                else:
                    player.jump_Count = (screen.get_width() // 192)
                    player.jump = False

    class Enemy(pygame.sprite.Sprite):
        image_list = [load_image('Dog/Dog_1.png'), load_image('Dog/Dog_2.png'), load_image('Dog/Dog_3.png')]

        def __init__(self, pos_x, pos_y):
            super().__init__(enemy_group, all_sprites)
            self.animCount = 0
            self.speed_k = 0
            self.image = Enemy.image_list[int(self.animCount % 3)]
            self.rect = self.image.get_rect().move(pos_x, pos_y)
            self.mask = pygame.mask.from_surface(self.image)
            self.run_mode = False

        def update(self):
            if self.run_mode:
                self.animCount += 1
                self.image = Enemy.image_list[int(self.animCount % 3)]

            if pygame.sprite.collide_mask(self, player):
                self.run_mode = False
                player.run_mode = False

    def generate_level(level):
        new_player, x, y = None, None, None
        for x in range(len(level)):
            if level[x] == '.':
                pass
            elif level[x] == '#':
                Box(x, 4.6)
        return x, y

    class Camera:
        def __init__(self):
            self.dx = 0
            self.dy = 0

        def apply(self, obj):
            if obj.rect.x < -obj.rect[2] and obj in tiles_group:
                all_sprites.remove(obj)

            elif obj in enemy_group and enemy.run_mode:
                if player.run_mode:
                    if obj.rect.x + 6 > 0:
                        obj.rect.x += random.randint(-6, 0)
                    else:
                        obj.rect.x += random.randint(0, 6)

                    if obj.rect.y - 30 > screen.get_height() // 3.5:
                        obj.rect.y += random.randint(-6, 0)
                    else:
                        obj.rect.y += random.randint(0, 6)

                else:
                    obj.rect.x += 10

            elif obj in background_sprites:
                if player.run_mode and obj.rect.x >= -13000:
                    obj.rect.x += self.dx + 13
                if obj.rect.x <= -12700:
                    player.jump_mode = False
                if obj.rect.x < -13000:
                    player.finish = True

                elif player.walk_mode:
                    obj.rect.x += self.dx + 5


            else:
                obj.rect.x += self.dx

        def update(self, target):
            self.dx = -(target.rect.x - target.rect.w - 400)

    Paper(screen)  # заставка с газетой
    load_music(info, 'data/sounds/music_game.mp3')
    level = load_level('levels/level_name{}.txt'.format(str(level_num)))

    background_sprites = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()

    camera = Camera()
    background = BackGround('Level_1/Map2.png', [background_sprites, all_sprites], screen)
    player = Player(700, screen.get_height() // 1.8)
    enemy = Enemy(screen.get_width(), screen.get_height() // 3.2)
    clock = pygame.time.Clock()
    generate_level(level)

    running = True
    fps = 60
    start_run_flag = True

    while running:

        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mixer.music.pause()
                    running = start_pause(screen)
                    mixer.music.unpause()

        if background.rect.x < -400 and start_run_flag:

            def start_run(screen):

                enemy.rect.x = -enemy.rect.w
                screen3 = pygame.Surface(screen.get_size())
                screen3.blit(screen, (0, 0))
                while True:
                    screen2 = pygame.Surface(screen.get_size())
                    screen2.blit(screen3, (0, 0))
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            sys.exit()

                    enemy.rect.x += 130
                    screen.blit(screen2, (0, 0))
                    enemy_group.draw(screen)
                    time.sleep(1)
                    pygame.display.flip()
                    if enemy.rect.x >= 0:
                        return False

            start_run_flag = start_run(screen)

            player.run_mode = True
            player.walk_mode = False
            enemy.rect.x = 0
            enemy.run_mode = True
            player.jump_mode = True

        if player.finish:
            def start_end(screen):
                background_sprites.draw(screen)
                screen3 = pygame.Surface(screen.get_size())
                screen3.blit(screen, (0, 0))
                while True:

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            sys.exit()

                    player.rect.x += 6
                    player.update()
                    screen.blit(screen3, (0, 0))
                    player_group.draw(screen)
                    enemy_group.draw(screen)
                    pygame.display.flip()
                    if player.rect.x > 1920:
                        return False

            start_end(screen)
            mixer.music.stop()
            running = start_dead_win_scene(screen, False)  # мужик выйграл

        screen.fill((255, 255, 255))
        player.update()
        camera.update(player)
        for i in all_sprites:
            camera.apply(i)
            if i in tiles_group or i in enemy_group:
                i.update()
        if running:
            background_sprites.draw(screen)
            player_group.draw(screen)
            tiles_group.draw(screen)
        if enemy.run_mode:
            enemy_group.draw(screen)
        if not player.run_mode and not player.walk_mode:
            mixer.music.stop()
            running = start_dead_win_scene(screen)  # умер Мужык фамилия таджик

        pygame.display.flip()
    mixer.music.stop()


def main():
    with open('Settings.json', 'r', encoding='utf-8') as f_obj:
        info = json.load(f_obj)  # считываем настройки с json

    pygame.init()
    mixer.pre_init(44100, -16, 1, 512)
    mixer.init()  # инициализируем всякую дичь

    load_music(info, 'data/sounds/Menu.mp3')  # включаем фонувую музыку
    sound_tap = load_sound('data/sounds/sound_tap.wav')  # записываем в переменную звук нажатия

    size = user_x, user_y = info['settings']["scr_res"]  # считываем разрешение экрана

    if info['settings']["fullscreen"]:  # проверяем не включен ли режим полного экрана
        screen = pygame.display.set_mode((user_x, user_y), FULLSCREEN)
    else:
        screen = pygame.display.set_mode((user_x, user_y), RESIZABLE)

    all_sprites = pygame.sprite.Group()
    menu = pygame.sprite.Group()
    button = pygame.sprite.Group()
    button_list = []
    num_button = 0

    backgroung = BackGround("main_menu/Комната.png", [menu, all_sprites], screen)
    play = Button('main_menu/play', (1920 // 2.8, 90), [button, all_sprites], 1, True)
    settings = Button('main_menu/settings', (1920 // 3.4, 360), [button, all_sprites], 2)
    quit = Button('main_menu/quit', (1920 // 2.9, 590), [button, all_sprites], 3)
    backgroung_dark = BackGround("main_menu/Затемнение.png", [menu, all_sprites], screen)
    # определяем кнопки и фон

    for i in [play, settings, quit]:
        button_list.append(i)
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP:  # обрабатывам нажатие кнопок
                    sound_tap.play()
                    button_list[num_button % 3].apply()
                    num_button -= 1
                    button_list[num_button % 3].apply()
                elif event.key == pygame.K_DOWN:
                    sound_tap.play()
                    button_list[num_button % 3].apply()
                    num_button += 1
                    button_list[num_button % 3].apply()
                elif event.key == 13:
                    sound_tap.play()
                    for i in button_list:
                        if i.num == 1 and i.flag:
                            mixer.music.stop()
                            start_level(screen, 1, info)  # cтартуем
                            load_music(info, 'data/sounds/Menu.mp3')
                        elif i.num == 2 and i.flag:
                            start_settings(screen, size, info)  # включаем настройки
                            with open('Settings.json', 'w', encoding='utf-8') as f_obj:
                                json.dump(info, f_obj, ensure_ascii=False)  # записываем изменения в json
                        elif i.num == 3 and i.flag:
                            running = False
                            sys.exit()
        for i in button_list:
            i.update()
        all_sprites.draw(screen)

        pygame.display.flip()


if __name__ == "__main__":
    main()
