from distutils.log import debug
import pygame


class ImageHandler(pygame.sprite.Sprite):
    # Takes an actual image (pygame surface), not a path to an image.
    def __init__(self, image=None, rows_cols=(0, 0), sprite_size=(0, 0)):
        self.image = image
        self.rows_cols = rows_cols
        self.sprite_size = sprite_size
        self.sprites = []
        
        if image and rows_cols and sprite_size:
            # Each row will be a list within our 'sprites' list.
            debug_col_count = 0
            for row in range(rows_cols[0]):
                curr_row = []
                for col in range(rows_cols[1]):
                    curr_row.append(self.image.subsurface(col * sprite_size[0], 
                        row * sprite_size[1], sprite_size[0], sprite_size[1]))
                    debug_col_count += 1
                self.sprites.append(curr_row)
    
    # This function will grab a specific sprite from the self.sprites list.
    # It will be given a tuple of the row and column of the sprite.
    def get_sprite(self, row_col):
        return self.sprites[row_col[0]][row_col[1]]
    
    # Returns a 1-D list of sprites from the sprites list already defined,
    # given a range. Sprites will be ordered from left to right, top to bottom.
    def get_sprites(self, start_coord=(0, 0), end_coord=(0, 0)):
        sprites = []
        for row in range(start_coord[0], end_coord[0]):
            curr_row = []
            for col in range(start_coord[1], end_coord[1]):
                curr_row.append(self.sprites[row][col])
            sprites.append(curr_row)
        return sprites

    def sprite_from_num(self, num):
        row, col = 0, 0
        for i in range(num):
            if col < len(self.sprites[0]) - 1:
                col += 1
            else:
                col = 0
                row += 1
                
        if not col == -1:
            return self.sprites[row][col]
        else:
            return self.sprites[0][0]
