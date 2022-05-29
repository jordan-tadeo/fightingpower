import pygame

W, H = 720, 480

GRAVITY = .45
JUMP_STRENGTH = 8
FRICTION = 0.5

class Character:
    def __init__(self, health, x, y):
        self.health = health
        self.x = x
        self.y = y

        self.velx, self.vely = 0, 0
        self.accx, self.accy = 0, 0

        self.max_speed = 5.5
        self.agility = 1.0

        self.width = 32
        self.height = 64

        self.color = (120, 130, 30)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.ground = False


    #   v   Methods   v

    # return health if character is alive, or 0 if not
    def is_alive(self):
        return max(0, self.get_health())
    
    # draw this character on 'win' pygame display obj
    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)
    
    # return if colliding with obj (only set up to work with stage rect rn)
    def colliding_with(self, obj):
        return self.rect.colliderect(obj.rects[0])

    # returns 1 if left side, 2 if right, 0 if within bounds
    def out_of_bounds(self):
        if self.x < 0:
            return 1
        elif self.x + self.width > W:
            return 2
        else:
            return 0

    # update player location with gravity, input, etc.
    def move(self):
        # apply gravity
        if not self.ground:
            jump_available = False
            self.accy += GRAVITY
        else:
            jump_available = True
            self.vely = 0

        # list of all keys, 0 if not pressed, 1 if pressed
        keys = pygame.key.get_pressed()
        
        # W, A, S, D
        # if keys[pygame.K_w]:
        #     self.vely -= self.movement_speed
        if keys[pygame.K_a] and self.velx > - self.max_speed:
            self.accx = - self.agility
        # if keys[pygame.K_s]:
        #     self.vely += self.movement_speed
        if keys[pygame.K_d] and self.velx < self.max_speed:
            self.accx = self.agility
        
        # SPACE
        if keys[pygame.K_SPACE] and jump_available:
            self.accy -= JUMP_STRENGTH
        
        # apply acceleration to velocity
        self.velx += self.accx
        self.vely += self.accy
        # apply velocity to position
        self.x += self.velx
        self.y += self.vely
        # update character's rectangle obj
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        # reset velocity for next frame
        self.accx, self.accy = 0, 0

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

        bounds_check = self.out_of_bounds()
        if bounds_check:
            self.velx *= -1
            if bounds_check == 1:
                self.x = 0
            else:
                self.x = W - self.width

    def update_pos(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    # inflict injury
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



    #   v   Getters/Setters   v

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