import pygame

from character import Character


W, H = 720, 480

RED_BROWN = (200, 90, 85)
BLUE = (28, 98, 128)


if __name__ == '__main__':
    pygame.init()
    
    screen = pygame.display.set_mode((W, H))

    floor = pygame.Surface((W, 32))
    floor.fill(RED_BROWN)
    floor_coord = (0, H - 32)

    player = Character(100, 200, 200)
    player.rect.fill(BLUE)

    # Variable to keep the main loop running
    running = True
    # Main loop
    while running:
        screen.fill((0,0,0))
        screen.blit(floor, floor_coord)
        screen.blit(player.rect, (player.get_xpos(), player.get_ypos()))
        pygame.display.flip()

        # Look at every event in the queue
        for event in pygame.event.get():
            # Did the user hit a key?
            if event.type == pygame.KEYDOWN:
                # Was it the Escape key? If so, stop the loop.
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_d:
                    player.set_xpos(player.get_xpos() + 8)

            # Did the user click the window close button? If so, stop the loop.
            elif event.type == pygame.QUIT:
                running = False