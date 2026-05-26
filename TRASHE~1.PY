import pygame

PLAYER_CLASSES = {
"mercenary": 6,
"cultist":   5,
"priest":    4,
"shaman":    4,
"merchant":  3
}

ANIM_WALK_INTERVAL   = 0.15
ANIM_ATTACK_INTERVAL = 0.12

# -- elucidate/main/class/player
class Player:
# -- elucidate/main/class/player/self
	def __init__(self, class_name, x, y, pw, ph, PLAYER_SPRITES, SPRITES):
		self.class_name = class_name
		self.x = float(x)
		self.y = float(y)
		self.pw = pw
		self.ph = ph
		self.size = 48
		self.dx = 0
		self.dy = 0
		self.speed = PLAYER_CLASSES.get(class_name, 5)
		self.facing = "down"
		self.state = "idle"
		self.is_attacking = False
		self.sprite_type = PLAYER_SPRITES.get(class_name, "no")
		self.anim_frame = 0
		self.anim_timer = 0.0
		self._SPRITES = SPRITES
# -- elucidate/main/class/player/self/input
	def update_input(self, controls):
		keys = pygame.key.get_pressed()
		self.dx = 0
		self.dy = 0
		if keys[controls["move_left"]]:
			self.dx = -self.speed
			self.facing = "left"
		if keys[controls["move_right"]]:
			self.dx = self.speed
			self.facing = "right"
		if keys[controls["move_up"]]:
			self.dy = -self.speed
			self.facing = "up"
		if keys[controls["move_down"]]:
			self.dy = self.speed
			self.facing = "down"
		if self.dx or self.dy:
			self.state = "walk"
		else:
			self.state = "idle"
# -- elucidate/main/class/player/self/move
	def move(self, walls):
		self.x += self.dx
		rect = self.get_rect()
		for wall in walls:
			if rect.colliderect(wall):
				if self.dx > 0:
					self.x = wall.left - self.size
				elif self.dx < 0:
					self.x = wall.right
		self.y += self.dy
		rect = self.get_rect()
		for wall in walls:
			if rect.colliderect(wall):
				if self.dy > 0:
					self.y = wall.top - self.size
				elif self.dy < 0:
					self.y = wall.bottom
	def border(self):
		if self.x < 0:
			self.x = self.pw - self.size
		if self.x > self.pw - self.size:
			self.x = 0
		if self.y < 0:
			self.y = self.ph - self.size
		if self.y > self.ph - self.size:
			self.y = 0
# -- elucidate/main/class/player/self/attack
	def attack(self):
		self.is_attacking = True
		self.state = "attack"
# -- elucidate/main/class/player/self/collisionbox
	def get_rect(self):
		return pygame.Rect(int(self.x), int(self.y), self.size, self.size)
# -- elucidate/main/class/player/self/draw
	def draw(self, screen, dt):
		sprite_set = self._SPRITES[self.sprite_type]
		if self.state == "idle":
			sprite = sprite_set["idle"][self.facing]
		elif self.state == "walk":
			frames = sprite_set["walk"][self.facing]
			self.anim_timer += dt
			if self.anim_timer >= ANIM_WALK_INTERVAL:
				self.anim_timer = 0.0
				self.anim_frame = (self.anim_frame + 1) % len(frames)
			sprite = frames[self.anim_frame]
		elif self.state == "attack":
			frames = sprite_set["attack"][self.facing]
			self.anim_timer += dt
			if self.anim_timer >= ANIM_ATTACK_INTERVAL:
				self.anim_timer = 0.0
				self.anim_frame = (self.anim_frame + 1) % len(frames)
			sprite = frames[self.anim_frame]
		else:
			sprite = sprite_set["idle"][self.facing]
		screen.blit(sprite, (int(self.x), int(self.y)))

# -- elucidate/main/functions/player
def player(class_name, x, y, pw, ph, PLAYER_SPRITES, SPRITES):
	return Player(class_name, x, y, pw, ph, PLAYER_SPRITES, SPRITES)
	# to call : p = player("mercenary", 100, 200, 1275, 710)
