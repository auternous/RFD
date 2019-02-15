import pygame
from load_functions import load_image


class Button(pygame.sprite.Sprite):  # класс обычной кнопки
    def __init__(self, filename, pos, groups, num, flag=False):
        super().__init__(groups)
        self.filename = filename
        self.num = num
        self.button = load_image(self.filename + ".png")
        self.button_true = load_image(self.filename + "_True.png")

        self.image = self.button
        self.rect = self.image.get_rect().move(pos)
        self.flag = flag

    def update(self):
        if self.flag:
            self.image = self.button_true
        else:
            self.image = self.button  # меняем изображение

    def apply(self):
        if self.flag:
            self.flag = False
        else:
            self.flag = True  # меняем значение переменной

    def image_change(self):
        self.button = load_image(self.filename + ".png")
        self.button_true = load_image(self.filename + "_True.png")  # изменение кнопки при нажатии


class BackGround(pygame.sprite.Sprite):

    def __init__(self, filename, groups, screen):
        super().__init__(groups)
        self.image = load_image(filename)
        self.rect = self.image.get_rect()


class Button_Fullscreen(Button):
    def __init__(self, filename, pos, groups, num, info, flag=False):
        super().__init__(filename, pos, groups, num, flag)
        self.filename = filename
        self.num = num
        self.condition = False
        if info['settings']['fullscreen']:
            self.button_true = load_image(self.filename[:-1] + '1' + "_True.png")
        else:
            self.button = load_image(self.filename + ".png")
            self.button_true = load_image(self.filename + "_True.png")

        self.image = self.button
        self.rect = self.image.get_rect().move(pos)
        self.flag = flag  # включен или выключен режим полного экрана


class Button_Volume(Button):
    def __init__(self, filename, pos, groups, num, info, flag=False):
        super().__init__(filename, pos, groups, num, flag)
        self.filename = filename
        self.num = num
        self.condition = False

        self.button = load_image(self.filename + ".png")
        self.button_true = load_image(self.filename + "_True.png")
        self.image = self.button
        self.rect = self.image.get_rect().move(pos)
        self.flag = flag
        self.list_vol = ['settings/volume_0', 'settings/volume_1', 'settings/volume_2',
                         'settings/volume_3', 'settings/volume_4']
        self.dict_key = {'settings/volume_0': 0, 'settings/volume_1': 0.25, 'settings/volume_2': 0.5,
                         'settings/volume_3': 0.75, 'settings/volume_4': 1}

    def change(self):
        self.filename = self.list_vol[(self.list_vol.index(self.filename) + 1) % 5]
        self.button = load_image(self.filename + ".png")
        self.button_true = load_image(self.filename + "_True.png")  # изменение кнопки при нажатии
