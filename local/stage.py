from cmath import rect
import pygame
import csv
from local.imagehandler import ImageHandler

# we want to make 1 big pygame surface with all the tiles in their correct
# positions. we will use this surface to blit the tiles to the screen. 


# then we will use one pixel's data from each tile in the big surface to
# determine the bounds of the rectangles we will use for collision.
# as we go tile by tile, row by row, we will keep an eye on the next
# tile, and see if it's empty or not. If its not empty, we can wait until
# later to decide on the right bound of the rectangle. Then we can
# go from top to bottom and combine rectangles that stack. Easy!


SPRITE_SIZE = 8
STAGE_SIZE = (45, 30)
W, H = STAGE_SIZE[0] * SPRITE_SIZE, STAGE_SIZE[1] * SPRITE_SIZE
DEFAULT_SCALE = 2

class Stage:
    def __init__(self, screen, path='local/res/tiles.png'):
        self.screen = screen
        self.game_surface = pygame.Surface((W, H))
        self.image = pygame.image.load(path)
        self.img_handler = ImageHandler(self.image, (12, 8), (SPRITE_SIZE, SPRITE_SIZE))
        self.read_from_csv()
        
        self.game_surface.convert_alpha()
        self.game_surface.set_colorkey((0, 0, 0))
        self.game_surface = pygame.transform.scale(self.game_surface, \
                                     (W * DEFAULT_SCALE, H * DEFAULT_SCALE))
        
        # a list of rectangles
        self.collision_map = []
        self.make_collision_map()
        print(self.collision_map)


    def read_from_csv(self):
        with open('local/res/stage_3.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            row, col = 0, 0

            for raw_row in csv_reader:
                for tile in raw_row:
                    tile = int(tile)

                    if tile == -1:
                        col += 1
                        continue

                    self.game_surface.blit(self.img_handler.sprite_from_num(int(tile)), \
                                             (col * SPRITE_SIZE, row * SPRITE_SIZE))
                    col += 1
                col = 0
                row += 1
    
    def draw(self, screen):
        screen.blit(self.game_surface, (0, 0))
        count = 0
        for rect in self.collision_map:
            # pygame.draw.rect(screen, (255, 0, 0), rect, 1)
            count += 1
    
    def make_collision_map(self):
        row = 0
        ds = DEFAULT_SCALE * SPRITE_SIZE
        for row in range(STAGE_SIZE[1]):
            col = 0
            rect_start_col = 0
            rect_count = 0
            in_a_rect = False
            for col in range(STAGE_SIZE[0]):
                # if this tile has something in it, we need to make a rectangle
                # for it, for collision detection.
                get_at_xy = (col * ds, row * ds)
                print("getting value at: ", get_at_xy)
                if not self.game_surface.get_at((col * ds, row * ds)) == (0, 0, 0, 255):
                    if not in_a_rect:
                        rect_start_col = col
                    in_a_rect = True
                    
                    # but, for efficiency, we can check the next tile to see
                    # if it has something in it. if it does, we can wait to make
                    # the rectangle until the upcoming tile is blank

                    if col < STAGE_SIZE[0] - 1:
                        if not self.game_surface.get_at(((col * ds) + \
                                    ds, row * ds)) == (0, 0, 0, 255):
                            # print(f'on row {row}, col {col}, we are in a rect, but the next tile is not empty')
                            col += 1
                            continue
                    # if the next tile is blank, we can end the rect here
                    # print(f'--> cutting off the rect here at col {col}, on row {row}')
                    in_a_rect = False
                    rect_count += 1
                    self.collision_map.append(pygame.Rect(rect_start_col * ds, \
                                            row * ds, (ds * (col - rect_start_col + 1)), ds))
                else:
                    col += 1
            # print(f'we made {rect_count} rectangles for row {row}')
            row += 1

        # Squash like-rectangles together on the Y-axis
        for x in range(3):
            for index, rect in enumerate(self.collision_map):
                mywidth, myheight = rect.width, rect.height
                my_x, my_y = rect.x, rect.y
                if index < len(self.collision_map) - 1:
                    if self.collision_map[index + 1].x == my_x and \
                        self.collision_map[index + 1].width == mywidth:
                        self.collision_map[index] = pygame.Rect(my_x, my_y, mywidth, \
                                        myheight + self.collision_map[index + 1].height)
                        self.collision_map.pop(index + 1)
                        continue
            