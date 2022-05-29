import pygame

from stage import Stage
from character import Character


clock = pygame.time.Clock()

W, H = 720, 480

BG_COLOR = (0, 30, 20)
RED_BROWN = (200, 90, 85)
BLUE = (28, 98, 128)
STAGE_COLOR = (190, 210, 255)

world_objs = []

def draw_frame(win, objs):
    win.fill(BG_COLOR)
    for o in objs:
        try:
            o.draw(win)
        except:
            pygame.draw.rect(win, STAGE_COLOR, o)
    pygame.display.update()


if __name__ == '__main__':
    pygame.init()
    
    screen = pygame.display.set_mode((W, H))

    stage = Stage()
    facade = (0, H - 84, W, 84)
    player = Character(100, 300, 300)

    world_objs.append(stage)
    world_objs.append(facade)
    world_objs.append(player)

    # Variable to keep the main loop running
    running = True
    # Main loop
    while running:
        clock.tick(60)
        draw_frame(screen, world_objs)
        player.move()

        # Check if player is hitting the ground
        if player.colliding_with(stage):
            player.ground = True
            # Set player height to be 1 pixel into the ground
            player.set_y(stage.rects[0][1] - player.height + 1)
        else:
            player.ground = False

        # Look at every event in the queue
        for event in pygame.event.get():
            # Did the user hit a key?
            if event.type == pygame.KEYDOWN:
                # Was it the Escape key? If so, stop the loop.
                if event.key == pygame.K_ESCAPE:
                    running = False
            # Did the user click the window close button? If so, stop the loop.
            elif event.type == pygame.QUIT:
                running = False