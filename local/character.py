import pygame
from local.animator import Animator
from local.animator import DEFAULT_FRAMETIME


W, H = 720, 480
BOX_COLOR = (120, 130, 30)
GRAVITY = .45
JUMP_STRENGTH = 8.0
FRICTION = 0.5


class Character:
    def __init__(self, health, x, y, screen=None, stage=None, npc=False):
        self.color = BOX_COLOR
        self.health = health
        self.x = x
        self.y = y
        self.width, self.height = 32, 92
        self.animator = Animator(window=screen)
        self.curr_anim = 'idle'

        self.velx, self.vely = 0, 0
        self.accx, self.accy = 0, 0
        self.max_speed, self.agility = 7.5, 3.0

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.center = self.rect.center

        self.ground = True
        self.facing = 'right'
        self.attacking = False
        self.atk_start_time = pygame.time.get_ticks()

        self.stage_rect = stage.rect
        self.npc = npc
    
    # draw this character on 'win' pygame display obj
    def draw(self, win):
        # pygame.draw.rect(win, self.color, self.rect)
        self.animator.curr_anim = self.curr_anim
        self.animator.animate(self.curr_anim, self.center)
    
    # return if colliding with obj (only set up to work with stage rect rn)
    def colliding_with(self):
        return self.rect.colliderect(self.stage_rect)

    def hit_ground(self):
        # Check if p is hitting the ground
        if self.colliding_with():
            self.ground = True
            self.vely = 0
            # Set player y value to be on the ground
            self.set_y(self.stage_rect[1] - self.height + 1)
        else:
            self.ground = False

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
                self.x = 0
            else:
                self.x = W - self.width

    def apply_physics(self):
        # apply acceleration to velocity
        self.velx += self.accx
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

        #this is ugly
        

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

    def injure(self, body_part):
        match body_part:
            case "head":
                self.set_health(self.get_health-20)
            case "body":
                self.set_health(self.get_health-10)
            case "arm":
                self.set_health(self.get_health-5)
            case "leg":
                self.set_health(self.get_health-5)

    def is_alive(self):
        return max(0, self.get_health())

    def get_health(self):
        return self.health
    def set_health(self, health):
        self.health = health

    def get_x(self):
        return self.x
    def set_x(self, x):
        self.x = x

    def get_y(self):
        return self.y
    def set_y(self, y):
        self.y = y