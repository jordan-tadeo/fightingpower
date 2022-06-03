import pygame
from local.animator import Animator
from local.animator import DEFAULT_FRAMETIME


W, H = 720, 480
BOX_COLOR = (120, 130, 30)
GRAVITY = .35
JUMP_STRENGTH = 7.0
FRICTION = 0.2


class Character:
    def __init__(self, health, x, y, screen=None, stage=None, npc=False):
        self.color = BOX_COLOR
        self.health = health
        self.x = x
        self.y = y
        self.width, self.height = 16, 46
        self.animator = Animator(window=screen)
        self.curr_anim = 'idle'

        self.velx, self.vely = 0, 0
        self.accx, self.accy = 0, 0
        self.max_speed, self.agility = 5.5, 1.0

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.center = self.rect.center

        self.ground = True
        self.ground_y = 0
        self.ground_rect = None
        self.facing = 'right'
        self.attacking = False
        self.atk_start_time = pygame.time.get_ticks()

        self.stage = stage
        self.collision_map = self.stage.collision_map
        self.npc = npc
    
    # draw this character on 'win' pygame display obj
    def draw(self, win):
        # pygame.draw.rect(win, self.color, self.rect)
        self.animator.curr_anim = self.curr_anim
        self.animator.animate(self.curr_anim, self.center)
    
    # return list of stage rects that we are colliding with
    def colliding_with(self):
        colliding_with = []
        for rect in self.collision_map:
            if self.rect.colliderect(rect):
                colliding_with.append(rect)
        return colliding_with

    def hit_ground(self):
        # Check to see if we are still on any kind of platform.
        # this is also where i prevent jittering when on the ground
        
        if (self.ground_rect and not (self.x + self.width / 2 > self.ground_rect.x \
            and self.x + self.width / 2 < self.ground_rect.x + self.ground_rect.width)):
            self.ground = False
            
        if not abs((self.y + self.height) - self.ground_y) < 2:
            self.ground = False

        # Check if p is hitting the ground
        # if the pixels under the player are not black/trasparent,
        # then the player is on the ground
        # print(f'heres the culprit {self.colliding_with()}')
        for rect in self.colliding_with():
            # if we are on top of this rect and inside it at least a bit
            if self.y + self.height >= rect.top and self.y + self.height <= \
                rect.top + 8 and self.x + self.width > rect.x and self.x < rect.x + rect.width:
                self.vely = 0
                self.ground = True
                self.ground_y = rect.top
                self.ground_rect = rect
                self.y = rect.top - self.height - 1
            # if we are not within the X-bounds of this rect, we are hitting
            # it from the side
            elif not (self.x > rect.x and self.x + self.width < rect.x + rect.width):
                dist_to_right = abs((self.x + self.width) - (rect.x + rect.width))
                dist_to_left = abs(self.x - rect.x)

                if dist_to_right < dist_to_left:
                    self.x = rect.x + rect.width + 2
                else:
                    self.x = rect.x - self.width - 2
                self.velx *= -.50
                
        
    # returns 1 if left side, 2 if right, 0 if within bounds
    def is_out_of_bounds(self):
        if self.x < 0:
            return 1
        elif self.x + self.width > W:
            return 2
        else:
            return 0

    def attack(self):
        type = 0
        # check for a mouse press
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
               type = event.button
        
        if pygame.time.get_ticks() > self.atk_start_time + \
            (DEFAULT_FRAMETIME * self.animator.curr_anim_frames):
            # attack animation is over
            self.attacking = False

         # attack # 1
        if type == 1:
            match self.facing:
                case 'right':
                    self.curr_anim = 'atk1'
                case 'left':
                    self.curr_anim = 'atk1f'
            self.attacking = True
            self.atk_start_time = pygame.time.get_ticks()
            # attack # 2
        if type == 3:
            match self.facing:
                case 'right':
                    self.curr_anim = 'atk2'
                case 'left':
                    self.curr_anim = 'atk2f'
            self.attacking = True
            self.atk_start_time = pygame.time.get_ticks()

    def idle(self):
        # select idle animation, right or left
        if abs(self.velx) <= 0.2 and self.ground and not self.attacking:
            if self.facing == 'right':
                self.curr_anim = 'idle'
            else:
                self.curr_anim = 'idlef'

    def jump(self):
        if not self.attacking:
            keys = pygame.key.get_pressed()
            # jump

            if keys[pygame.K_SPACE] and self.ground:
                self.accy -= JUMP_STRENGTH
                self.ground = False
                self.airtime_start = pygame.time.get_ticks()


    def run(self):
        # list of all keys, 0 if not pressed, 1 if pressed
        keys = pygame.key.get_pressed()
        if not self.attacking:
            # move left
            if keys[pygame.K_a] and self.velx > - self.max_speed:
                self.accx = - self.agility
                self.facing = 'left'
                if self.ground:
                    self.curr_anim = 'runf'
            # move right
            if keys[pygame.K_d] and self.velx < self.max_speed:
                self.accx = self.agility
                self.facing = 'right'
                if self.ground:
                    self.curr_anim = 'run'

    def midair(self):
        # not on ground? apply gravity
        if not self.ground:
            self.accy += GRAVITY
            # in-air animation
            if self.facing == 'right' and not self.attacking:
                self.curr_anim = 'jump'
            elif not self.attacking:
                self.curr_anim = 'jumpf'

    def x_friction(self):
        # add friction to X movement
        if not abs(self.velx) < FRICTION:
            # if moving right...
            if max(0, self.velx):
                self.velx -= FRICTION
            # if moving left...
            elif min(0, self.velx) < 0:
                self.velx += FRICTION
        else:
            self.velx = 0

    def bounds(self):
        # keep player on screen (x-axis)
        bounds_check = self.is_out_of_bounds()
        if bounds_check:
            self.velx *= -1
            if bounds_check == 1:
                self.x = 2
            else:
                self.x = W - self.width - 2

    def apply_physics(self):
        # apply acceleration to velocity
        self.velx += self.accx
        if self.vely < self.max_speed:
            self.vely += self.accy

        # apply velocity to position
        self.x += self.velx
        self.y += self.vely

        # reset accel for next frame
        self.accx, self.accy = 0, 0

    def update_pos(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.center = self.rect.center

    # root function. calls all movement functions
    def move(self):    
        self.colliding_with()
        self.jump()
        self.run()
        self.apply_physics()
        self.x_friction()
        self.bounds()
        self.update_pos()
        self.attack()
        self.midair()
        self.hit_ground()
        self.idle()
            

        # this is ugly
        

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

    def get_x(self):
        return self.x
    def set_x(self, x):
        self.x = x

    def get_y(self):
        return self.y
    def set_y(self, y):
        self.y = y