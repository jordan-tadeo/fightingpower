import pygame


class SpriteSheet():
	# width and height of each frame of spritesheet --> w, h
	def __init__(self):
		self.w = 200
		self.h = 200

		self.anim_speed = 64
		self.last_frame_time = pygame.time.get_ticks()

		self.sheets = {		# spritesheet surface, number of frames, flipped or not
						0: [pygame.image.load('local/sprites/Idle.png'), 4, 0],
						1: [pygame.image.load('local/sprites/Idlef.png'), 4, 1],
						2: [pygame.image.load('local/sprites/Run.png'), 8, 0],	
						3: [pygame.image.load('local/sprites/Runf.png'), 8, 1],
						4: [pygame.image.load('local/sprites/Jump.png'), 2, 0],
						5: [pygame.image.load('local/sprites/Jumpf.png'), 2, 1],
						6: [pygame.image.load('local/sprites/Atk1.png'), 4, 0],
						7: [pygame.image.load('local/sprites/Atk1f.png'), 4, 1],
						8: [pygame.image.load('local/sprites/Atk2.png'), 4, 0],
						9: [pygame.image.load('local/sprites/Atk2f.png'), 4, 1]
		}
						# image, number of frames, flipped or not
		self.curr_anim = [self.sheets[0][0], self.sheets[0][1], self.sheets[0][2]]
		self.curr_frame = [0, self.curr_anim[0]]
		self.curr_frame = [0, self.get_frame(0)]

		self.frame_center = 0

	def select_anim(self, sheet_id):
		self.curr_anim = [self.sheets[sheet_id][0], self.sheets[sheet_id][1], self.sheets[sheet_id][2]]
		
	def get_frame(self, frame, scale=2):
		image = pygame.Surface((self.w, self.h)).convert_alpha()
		image.blit(self.curr_anim[0], (0, 0), ((frame * self.w), 0, self.w, self.h))
		image = pygame.transform.scale(image, (self.w * scale, self.h * scale))
		image.set_colorkey((0,0,0))
		self.frame_center = image.get_rect().center
		return image

	def step_frame(self):
		if pygame.time.get_ticks() > self.last_frame_time + self.anim_speed:
			self.last_frame_time = pygame.time.get_ticks()
			framenumber = 0
			if self.curr_anim[2]:
				self.curr_frame[0] %= self.curr_anim[1]
				framenumber =  self.curr_anim[1] - self.curr_frame[0] - 1
			else:
				self.curr_frame[0] %= self.curr_anim[1]
				framenumber = self.curr_frame[0]
			self.curr_frame[0] += 1
			self.curr_frame[1] = self.get_frame(framenumber)
		else:
			pass

	def draw(self, hold_frame=False):
		if not hold_frame:
			self.step_frame()
		return self.curr_frame[1]