import pygame


sheet_idle = [pygame.image.load('local/sprites/Idle.png'), 4]		# 0
sheet_idlef = [pygame.image.load('local/sprites/Idlef.png'), 4]		# 1
sheet_run = [pygame.image.load('local/sprites/Run.png'), 8]			# 2
sheet_runf = [pygame.image.load('local/sprites/Runf.png'), 8]		# 3
sheet_jump = [pygame.image.load('local/sprites/Jump.png'), 2]		# 4
sheet_jumpf = [pygame.image.load('local/sprites/Jumpf.png'), 2]		# 5


class SpriteSheet():
	# width and height of each frame of spritesheet --> w, h
	def __init__(self):
		self.w = 200
		self.h = 200

		self.curr_anim = [sheet_idle[0], sheet_idle[1]]
		self.curr_frame = [0, self.curr_anim[0]]
		self.curr_frame = [0, self.get_frame(0)]

		self.anim_speed = 64
		self.last_frame_time = pygame.time.get_ticks()

		self.sheets = [sheet_idle, sheet_idlef, sheet_run, sheet_runf, sheet_jump, sheet_jumpf]


	def select_anim(self, sheet_id):
		self.curr_anim = [self.sheets[sheet_id][0], self.sheets[sheet_id][1]]
		

	def get_frame(self, frame, scale=2):
		image = pygame.Surface((self.w, self.h)).convert_alpha()
		image.blit(self.curr_anim[0], (0, 0), ((frame * self.w) + 29, 18, self.w - 32, self.h - 32))
		image = pygame.transform.scale(image, (self.w * scale, self.h * scale))
		image.set_colorkey((0,0,0))

		return image

	def step_frame(self):
		if pygame.time.get_ticks() > self.last_frame_time + self.anim_speed:
			self.last_frame_time = pygame.time.get_ticks()

			self.curr_frame[0] += 1
			self.curr_frame[0] %= self.curr_anim[1]
			self.curr_frame[1] = self.get_frame(self.curr_frame[0])
		else:
			pass

	def draw(self, hold_frame=False):
		if not hold_frame:
			self.step_frame()
		return self.curr_frame[1]