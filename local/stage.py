import pygame
import csv
from local.imagehandler import ImageHandler

# we want to make 1 big pygame surface with all the tiles in their correct
# positions. we will use this surface to blit the tiles to the screen. 

SPRITE_SIZE = 8
STAGE_SIZE = (45, 30)
W, H = STAGE_SIZE[0] * SPRITE_SIZE, STAGE_SIZE[1] * SPRITE_SIZE
DEFAULT_SCALE = 2

class Stage:
    def __init__(self, screen, path='local/res/tiles.png'):
        self.screen = screen
        self.game_surface = pygame.Surface((W, H))
        self.image = pygame.image.load(path)
        self.img_handler = ImageHandler(self.image, (12, 8), (SPRITE_SIZE, SPRITE_SIZE), True)
        self.read_from_csv()
        
        self.game_surface.convert_alpha()
        self.game_surface.set_colorkey((0, 0, 0))

    def read_from_csv(self):
        with open('local/res/stage_1.csv', 'r') as csv_file:
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
        # print(f'this how many sprites we got on the sheet -> {len(self.img_handler.sprites)}')
        self.game_surface = pygame.transform.scale(self.game_surface, \
                                     (W * DEFAULT_SCALE, H * DEFAULT_SCALE))
        screen.blit(self.game_surface, (0, 0))
                