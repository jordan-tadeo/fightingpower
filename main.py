import pygame
from net.network import Network
from net.server import read_pos, make_pos
from local.stage import Stage
from local.character import Character


clock = pygame.time.Clock()

W, H = 720, 480

BG_COLOR = (0, 30, 20)
RED_BROWN = (200, 90, 85)
BLUE = (28, 98, 128)
STAGE_COLOR = (190, 210, 255)

bg = pygame.image.load('local/mountains.png')
bg = pygame.transform.scale(bg, (W, H))

world_objs = []


def draw_frame(win, objs):
    win.fill(BG_COLOR)
    win.blit(bg, (0, 0))
    for o in objs:
        try:
            o.draw(win)
        except:
            pygame.draw.rect(win, STAGE_COLOR, o)
    pygame.display.update()


if __name__ == '__main__':
    pygame.init()

    n = Network()
    screen = pygame.display.set_mode((W, H))

    stage = Stage()
    facade = (0, H - 84, W, 84)
    p = Character(100, 300, 300)
    p2 = Character(100, 200, 200)

    world_objs.append(stage)
    world_objs.append(facade)
    world_objs.append(p)
    world_objs.append(p2)

    running = True
    # Main loop
    while running:
        clock.tick(60)
        draw_frame(screen, world_objs)
        p.move()

        # Check if p is hitting the ground
        if p.colliding_with(stage):
            p.ground = True
            # Set p height to be 1 pixel into the ground
            p.set_y(stage.rects[0][1] - p.height + 1)
        else:
            p.ground = False
        
        # receive p2 position from server
        try:
            p2Pos = read_pos(n.send_and_recv(make_pos((p.get_x(), p.get_y()))))
            p2.set_x(p2Pos[0])
            p2.set_y(p2Pos[1])
            p2.update_pos()
        except:
            print("could not find player 2!")

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