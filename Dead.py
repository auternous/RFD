def start_dead_scene(screen):
    images_dead_list = []
    for i in range(1, 11):
        images_dead_list.append(load_image('Dead_scene/Dead_{}.png'.format(i)))
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
