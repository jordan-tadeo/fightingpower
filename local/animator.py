from ntpath import join
import pygame
from os import *
from local.imagehandler import ImageHandler

DEFAULT_FRAMETIME = 64
DEFAULT_SPRITE_SCALE = 2
BLUE = (0, 0, 255)

class Animator:
    # Constructor: decide what directory we will be pulling sprites from,
    # get all those images loaded up and ready.
    def __init__(self, images_dir='local/sprites/', sprite_size=(200, 200), window=None):
        self.images_dir = images_dir
        self.images = {}
        self.sprite_size = sprite_size
        self.window = window
        self.imagehandler = ImageHandler()
        self.timer = pygame.time.get_ticks()

        for filename in listdir(self.images_dir):
            if filename.endswith('.png'):
                this_img = pygame.image.load(self.images_dir + filename)
                this_filename = filename.split('.')[0].lower()
                self.images.update({this_filename: this_img})
        
        self.curr_frame = 0
        self.curr_anim = 'idle'
        self.curr_anim_frames = self.get_num_frames(self.curr_anim)
        self.curr_anim_speed = DEFAULT_FRAMETIME


    def get_num_frames(self, name):
        return int(self.images[name].get_width() / self.sprite_size[0])
    
    # set up for 1-D animation spritesheet images only
    def animate(self, name=None, center=(0, 0), frame_time=DEFAULT_FRAMETIME):
        now = pygame.time.get_ticks()
        if now > self.timer + frame_time:
            self.timer = now
            self.curr_frame += 1

        # how many frames in this animation?
        if not name:
            name = self.curr_anim
        num_frames = self.get_num_frames(name)
        self.curr_anim = name

        if self.curr_frame > num_frames - 1:
                self.curr_frame = 0

        self.imagehandler = ImageHandler(self.images[name],
                                        (1, num_frames), self.sprite_size)
        
        # If we are facing left, reverse the order that we traverse the sprite
        # sheet.
        if name.endswith('f'):
            self.draw(self.imagehandler.get_sprite((0, num_frames - self.curr_frame - 1)), center)
        else:
            self.draw(self.imagehandler.get_sprite((0, self.curr_frame)), center)
    
    def draw(self, sprite, center):
        # Scale the sprite before we draw it
        sprite = pygame.transform.scale(sprite, (self.sprite_size[0] * DEFAULT_SPRITE_SCALE, 
                                        self.sprite_size[1] * DEFAULT_SPRITE_SCALE))
        # draw the sprite
        self.window.blit(sprite, (center[0] - (sprite.get_width() / 2),
                        center[1] - (sprite.get_height() / 2)))