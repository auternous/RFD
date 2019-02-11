class Camera:
        def __init__(self):
            self.dx = 0
            self.dy = 0

        def apply(self, obj):
            if obj.rect.x < -obj.rect[2] and obj in tiles_group:
                all_sprites.remove(obj)


            elif obj in background_sprites and player.run_mode:
                obj.rect.x += self.dx + 13

            elif obj in enemy_group and enemy.run_mode:
                if player.run_mode:
                    if obj.rect.x + 6 > 0:
                        obj.rect.x += random.randint(-6, 0)
                    else:
                        obj.rect.x += random.randint(0, 6)

                    if obj.rect.y - 30> screen.get_height() // 3.5:
                        obj.rect.y += random.randint(-6, 0)
                    else:
                        obj.rect.y += random.randint(0, 6)

                else:
                    obj.rect.x += 10

            else:
                obj.rect.x += self.dx
                obj.rect.y += self.dy

        def update(self, target):
            self.dx = -(target.rect.x - target.rect.w - 400)