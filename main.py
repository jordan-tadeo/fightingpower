import traceback
import pygame
from net.network import Network
from net.server import read_pos, make_pos
from local.stage import Stage
from local.character import Character


W, H = 720, 480


def draw_frame(win, objs):
    
    for o in objs:
        o.draw(win)
    pygame.display.update()
    # win.blit(bg, (0, 0))


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    clock = pygame.time.Clock()
    # n = Network()

    bg = pygame.image.load('local/res/mountains.png')
    bg = pygame.transform.scale(bg, (W, H))

    screen.fill((90, 90, 90))
    stage = Stage(screen)

    p = Character(100, 300, 200, screen, stage)
    # p2 = Character(100, 200, 200, True)

    world_objs = []
    world_objs.append(stage)
    world_objs.append(p)
    # world_objs.append(p2)


    running = True
    # Main loop
    while running:
        screen.blit(bg, (0, 0))
        p.move()
        p.draw(screen)
        stage.draw(screen)
        
        # receive p2 position from server
        """
        try:
            p2Pos = read_pos(n.send_and_recv(make_pos((p.get_x(), p.get_y()))))
            p2.set_x(p2Pos[0])
            p2.set_y(p2Pos[1])
            p2.update_pos()
        except:
            print("could not find player 2!")
        """
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
        
        clock.tick(60)
        pygame.display.update()