import pygame
import random
import sys
import math
import time
import binascii
import json
import os
from datetime import datetime

def elucidate():
# -- elucidate/main/pygame/initiation
	pygame.init()
	pygame.mixer.init()
# -- elucidate/main/pygame/screen
	screen_x, screen_y = 1275, 710
	screen = pygame.display.set_mode((screen_x, screen_y))
	pygame.display.set_caption("Elucidate RPG")
#[Loading]
	screen.fill((0, 0, 0))
	image = pygame.image.load("images/elucidate_title.png")
	resized_image = pygame.transform.scale(image, (int(1275/2), int(710/2)))
	screen.blit(resized_image, (int(1275/4), int(710/4)))
	image = pygame.image.load("images/elucidate_select_full.png")
	resized_image = pygame.transform.scale(image, (int(1275/2), 30))
	screen.blit(resized_image, (int(1275/4), int(710-115)))
	font = pygame.font.SysFont("Times New Roman", 25)
	text_surface = font.render("Processing Assets", True, (0, 0, 0))
	text_rect = text_surface.get_rect(center=(int(1275/2), int(710-100)))
	screen.blit(text_surface, text_rect)
	font = pygame.font.SysFont("Times New Roman", 20)
	text_surface = font.render("Loading...", True, (255, 255, 255))
	text_rect = text_surface.get_rect(center=(int(1275/2), int(710-20)))
	screen.blit(text_surface, text_rect)
	pygame.draw.rect(screen, (160, 0, 0), (0, 0, screen_x, screen_y), 1)
	pygame.display.flip()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
	pygame.time.delay(1 * 1000)
# -- elucidate/main/pygame/variables
	py_clock = pygame.time.Clock()
# -- elucidate/main/pygame/lists
	walls = []
# -- elucidate/main/pygame/dictionaries
	fonts = {
	15: pygame.font.SysFont("Times New Roman", 15),
	20: pygame.font.SysFont("Times New Roman", 20),
	25: pygame.font.SysFont("Times New Roman", 25),
	30: pygame.font.SysFont("Times New Roman", 30),
	35: pygame.font.SysFont("Times New Roman", 35),
	40: pygame.font.SysFont("Times New Roman", 40),
	45: pygame.font.SysFont("Times New Roman", 45),
	50: pygame.font.SysFont("Times New Roman", 50),
	}
	_hex_decode_cache = {}
	PLAYER_CLASSES = {
	"mercenary": 6,
	"cultist":   5,
	"priest":    4,
	"shaman":    4,
	"merchant":  3
	}
	_preloaded_images = {
	"elucidate_title":       pygame.image.load("images/elucidate_title.png").convert(),
	"elucidate_menu_bg_001": pygame.image.load("images/elucidate_menu_bg_001.png").convert(),
	"elucidate_menu_bg_002": pygame.image.load("images/elucidate_menu_bg_002.png").convert(),
	"elucidate_menu_bg_003": pygame.image.load("images/elucidate_menu_bg_003.png").convert(),
	"elucidate_menu_bg_004": pygame.image.load("images/elucidate_menu_bg_004.png").convert(),
	"elucidate_menu_bg_005": pygame.image.load("images/elucidate_menu_bg_005.png").convert(),
	"elucidate_menu_bg_006": pygame.image.load("images/elucidate_menu_bg_006.png").convert(),
	"elucidate_menu_bg_007": pygame.image.load("images/elucidate_menu_bg_007.png").convert(),
	"elucidate_menu_bg_008": pygame.image.load("images/elucidate_menu_bg_008.png").convert(),
	"elucidate_menu_bg_009": pygame.image.load("images/elucidate_menu_bg_009.png").convert(),
	"elucidate_select":      pygame.image.load("images/elucidate_select.png").convert(),
	"elucidate_select_full": pygame.image.load("images/elucidate_select_full.png").convert(),
	"elucidate_play_bg":     pygame.image.load("images/elucidate_play_bg.png").convert(),
	"elucidate_no_texture":  pygame.image.load("images/elucidate_no_texture.png").convert(),
	"elucidate_no_sprite_idle_1":  pygame.image.load("sprites/elucidate_player_sprite_idle_up.png").convert_alpha(),
	"elucidate_no_sprite_idle_2":  pygame.image.load("sprites/elucidate_player_sprite_idle_down.png").convert_alpha(),
	"elucidate_no_sprite_idle_3":  pygame.image.load("sprites/elucidate_player_sprite_idle_left.png").convert_alpha(),
	"elucidate_no_sprite_idle_4":  pygame.image.load("sprites/elucidate_player_sprite_idle_right.png").convert_alpha(),
	"elucidate_no_sprite_walk_1_1":  pygame.image.load("sprites/elucidate_player_sprite_walking_up_1.png").convert_alpha(),
	"elucidate_no_sprite_walk_1_2":  pygame.image.load("sprites/elucidate_player_sprite_walking_up_2.png").convert_alpha(),
	"elucidate_no_sprite_walk_2_1":  pygame.image.load("sprites/elucidate_player_sprite_walking_down_1.png").convert_alpha(),
	"elucidate_no_sprite_walk_2_2":  pygame.image.load("sprites/elucidate_player_sprite_walking_down_2.png").convert_alpha(),
	"elucidate_no_sprite_walk_3_1":  pygame.image.load("sprites/elucidate_player_sprite_walking_left_1.png").convert_alpha(),
	"elucidate_no_sprite_walk_3_2":  pygame.image.load("sprites/elucidate_player_sprite_walking_left_2.png").convert_alpha(),
	"elucidate_no_sprite_walk_4_1":  pygame.image.load("sprites/elucidate_player_sprite_walking_right_1.png").convert_alpha(),
	"elucidate_no_sprite_walk_4_2":  pygame.image.load("sprites/elucidate_player_sprite_walking_right_2.png").convert_alpha(),
	"elucidate_no_sprite_attack_1_1":  pygame.image.load("sprites/elucidate_player_sprite_attack_up_1.png").convert_alpha(),
	"elucidate_no_sprite_attack_1_2":  pygame.image.load("sprites/elucidate_player_sprite_attack_up_2.png").convert_alpha(),
	"elucidate_no_sprite_attack_2_1":  pygame.image.load("sprites/elucidate_player_sprite_attack_down_1.png").convert_alpha(),
	"elucidate_no_sprite_attack_2_2":  pygame.image.load("sprites/elucidate_player_sprite_attack_down_2.png").convert_alpha(),
	"elucidate_no_sprite_attack_3_1":  pygame.image.load("sprites/elucidate_player_sprite_attack_left_1.png").convert_alpha(),
	"elucidate_no_sprite_attack_3_2":  pygame.image.load("sprites/elucidate_player_sprite_attack_left_2.png").convert_alpha(),
	"elucidate_no_sprite_attack_4_1":  pygame.image.load("sprites/elucidate_player_sprite_attack_right_1.png").convert_alpha(),
	"elucidate_no_sprite_attack_4_2":  pygame.image.load("sprites/elucidate_player_sprite_attack_right_2.png").convert_alpha(),
	"elucidate_select_bg_001":     pygame.image.load("images/elucidate_select_background.png").convert(),
	"elucidate_select_bg_002":     pygame.image.load("images/elucidate_empty_bg_001.png").convert(),
	"elucidate_select_ui_001":     pygame.image.load("images/elucidate_show_selection_002.png").convert(),
	"elucidate_select_ui_002":     pygame.image.load("images/elucidate_show_selection_001.png").convert_alpha(),
	"elucidate_mcguy_001":     pygame.image.load("images/elucidate_mcguy_portrait_001.png").convert_alpha(),
	}
	_scaled_images = {
	"elucidate_title_full":  pygame.transform.scale(_preloaded_images["elucidate_title"], (1275, 710)),
	"elucidate_title_1":     pygame.transform.scale(_preloaded_images["elucidate_title"], (1275/2, 710/2)),
	"elucidate_select_load": pygame.transform.scale(_preloaded_images["elucidate_select_full"], (1275/2, 30)),
	"elucidate_select_home": pygame.transform.scale(_preloaded_images["elucidate_select"], (250, 35)),
	"elucidate_select_exit": pygame.transform.scale(_preloaded_images["elucidate_select_full"], (200, 30)),
	"elucidate_select_ui_002_play_select": pygame.transform.scale(_preloaded_images["elucidate_select_ui_002"], (500, 300)),
	"elucidate_mcguy_001_999": pygame.transform.scale(_preloaded_images["elucidate_mcguy_001"], (300, 500)),
	}
	_rotated_images = {
	"elucidate_title_1_r": pygame.transform.rotate(_scaled_images["elucidate_title_1"], 360),
	"elucidate_select_ui_002_play_select_r": pygame.transform.rotate(_scaled_images["elucidate_select_ui_002_play_select"], 90),
	}
	PLAYER_SPRITES = {
	"mercenary": "no",
	"cultist": "no",
	"priest": "no",
	"shaman": "no",
	"merchant": "no",
	}
	SPRITES = {
	"no": {
	"idle": {
	"up":    _preloaded_images["elucidate_no_sprite_idle_1"],
	"down":  _preloaded_images["elucidate_no_sprite_idle_2"],
	"left":  _preloaded_images["elucidate_no_sprite_idle_3"],
	"right": _preloaded_images["elucidate_no_sprite_idle_4"],
	},
	"walk": {
	"up": [ _preloaded_images["elucidate_no_sprite_walk_1_1"], _preloaded_images["elucidate_no_sprite_walk_1_2"]],
	"down": [ _preloaded_images["elucidate_no_sprite_walk_2_1"], _preloaded_images["elucidate_no_sprite_walk_2_2"]],
	"left": [ _preloaded_images["elucidate_no_sprite_walk_3_1"], _preloaded_images["elucidate_no_sprite_walk_3_2"]],
	"right": [ _preloaded_images["elucidate_no_sprite_walk_4_1"], _preloaded_images["elucidate_no_sprite_walk_4_2"]],
	},
	"attack": {
	"up": [ _preloaded_images["elucidate_no_sprite_attack_1_1"], _preloaded_images["elucidate_no_sprite_attack_1_2"]],
	"down": [ _preloaded_images["elucidate_no_sprite_attack_2_1"], _preloaded_images["elucidate_no_sprite_attack_2_2"]],
	"left": [ _preloaded_images["elucidate_no_sprite_attack_3_1"], _preloaded_images["elucidate_no_sprite_attack_3_2"]],
	"right": [ _preloaded_images["elucidate_no_sprite_attack_4_1"], _preloaded_images["elucidate_no_sprite_attack_4_2"]],
	},
	}
	}
# -- elucidate/main/pygame/ints
	sys_bg_color         = (0  , 0  , 0  )
	sys_bd_color_sc_area = (180, 180, 180)
	sys_audio_volume     = 1.0
	ui_white = (245, 245, 245)
	ui_crimson = (160, 0, 0)
	ui_dark_crimson = (120, 0, 0)
	ui_gray = (180, 180, 180)
# -- elucidate/main/pygame/bools
	sys_audio_muted = False
# -- elucidate/main/pygame/strings
	sys_controls_mode = "keyboard"
	controls = {
	"move_left": pygame.K_a,
	"move_right": pygame.K_d,
	"move_up": pygame.K_w,
	"move_down": pygame.K_s,
	"attack": pygame.K_SPACE,
	}
	SAVE_DIR          = "saves"
	CONTROLS_FILE = os.path.join(SAVE_DIR, "controls.json")
	text_home_001 = "PLAY"
	text_home_002 = "SETTINGS"
	text_home_003 = "EXIT"
# -- elucidate/main/functions/save/directory
	if not os.path.exists(SAVE_DIR):
		os.makedirs(SAVE_DIR)
# -- elucidate/main/functions/system
	def sys_tick(n):
		py_clock.tick(n)
	def elucidate_sys_exit():
		pygame.quit()
		sys.exit()
	def display():
		pygame.display.flip()
		sys_tick(999)
	def sys_font(size):
		return fonts[size]
	def sys_main_hex(text):
		if text in _hex_decode_cache:
			return _hex_decode_cache[text]
		try:
			text_clean = text.replace(" ", "")
			bytes_object = bytes.fromhex(text_clean)
			result = bytes_object.decode('utf-8')
		except ValueError:
			result = "there was an error while generating this text."
		_hex_decode_cache[text] = result
		return result
	def load_controls():
		if os.path.exists(CONTROLS_FILE):
			with open(CONTROLS_FILE, "r") as f:
				data = json.load(f)
				for k in controls:
					if k in data:
						controls[k] = data[k]
# -- elucidate/main/functions/general
	def save_controls():
		with open(CONTROLS_FILE, "w") as f:
			json.dump(controls, f)
	def static_text(text, color, position, size):
		text = sys_main_hex(text)
		font = sys_font(size)
		text_surface = font.render(text, True, color)
		screen.blit(text_surface, position)
	def static_text_center(text, color, position, size):
		text = sys_main_hex(text)
		font = sys_font(size)
		text_surface = font.render(text, True, color)
		text_rect = text_surface.get_rect(center=position)
		screen.blit(text_surface, text_rect)
	def static_text_raw(text, color, position, size):
		font = sys_font(size)
		text_surface = font.render(text, True, color)
		screen.blit(text_surface, position)
	def static_text_raw_center(text, color, position, size):
		font = sys_font(size)
		text_surface = font.render(text, True, color)
		text_rect = text_surface.get_rect(center=position)
		screen.blit(text_surface, text_rect)
	def tuple_static_text(*t, color, position, size):
		font = sys_font(size)
		text_surface = font.render(" ".join(map(str, t)), True, color)
		screen.blit(text_surface, position)
	def ambient(file, loop):
		pygame.mixer.music.load(file)
		pygame.mixer.music.play(loop)
		sys_apply_audio_settings()
	def sys_apply_audio_settings():
		if sys_audio_muted:
			pygame.mixer.music.set_volume(0.0)
		else:
			pygame.mixer.music.set_volume(sys_audio_volume)
	def mouse():
		pygame.draw.rect(screen, (160, 0, 0), (0, 0, screen_x, screen_y), 1)
		mouse_782d61786973, mouse_792d61786973 = pygame.mouse.get_pos()
		pygame.draw.rect(screen, (0, 255, 0), (mouse_782d61786973 - 10, mouse_792d61786973, 20, 1))
		pygame.draw.rect(screen, (0, 255, 0), (mouse_782d61786973, mouse_792d61786973 - 10, 1, 20))
		tuple_static_text((mouse_782d61786973, mouse_792d61786973), color=(0, 255, 0), position=(mouse_782d61786973 + 10, mouse_792d61786973), size=15)
		tuple_static_text((py_clock), color=(0, 255, 0), position=(mouse_782d61786973 + 10, mouse_792d61786973 + 15), size=15)
	def sys_gen_loading(n):
		ambient("music/elucidate_the_wait.wav", -1)
		screen.fill(sys_bg_color)
		screen.blit(_scaled_images["elucidate_title_1"], (int(1275/4), int(710/4)))
		screen.blit(_scaled_images["elucidate_select_load"], (int(1275/4), int(710-115)))
		static_text_raw_center("Welcome to Elucidate RPG", color=(0, 0, 0), position=(int(1275/2), int(710-100)), size=25)
		static_text_raw_center("Loading...", color=(255, 255, 255), position=(int(1275/2), int(710-20)), size=20)
		pygame.draw.rect(screen, (160, 0, 0), (0, 0, screen_x, screen_y), 1)
		display()
		pygame.time.delay(n * 1000)
		screen.fill(sys_bg_color)
		screen.blit(_scaled_images["elucidate_title_1"], (int(1275/4), int(710/4)))
		screen.blit(_scaled_images["elucidate_select_load"], (int(1275/4), int(710-115)))
		static_text_raw_center("Welcome to Elucidate RPG", color=(0, 0, 0), position=(int(1275/2), int(710-100)), size=25)
		static_text_raw_center("Done", color=(255, 255, 255), position=(int(1275/2), int(710-20)), size=20)
		pygame.draw.rect(screen, (160, 0, 0), (0, 0, screen_x, screen_y), 1)
		display()
		pygame.time.delay(1 * 1000)
	def sys_gen_update_error():
		loop_cytsuwjw = True
		colide_yes = pygame.Rect((screen_x/2)-100, (screen_y/2)+134, 200, 30)
		colide_no = pygame.Rect((screen_x/2)-100, (screen_y/2)+174, 200, 30)
		while loop_cytsuwjw:
			events = pygame.event.get()
			for event in events:
				if event.type == pygame.QUIT:
					elucidate_sys_exit()
			mouse_x, mouse_y = pygame.mouse.get_pos()
			screen.fill(sys_bg_color)
			screen.blit(_preloaded_images["elucidate_select_bg_002"], (0, 0))
			static_text_raw_center("Built for future update.", color=(255, 255, 255), position=(screen_x/2, (screen_y/2)-40), size=(40))
			static_text_raw_center("Unavailable state.", color=(255, 255, 255), position=(screen_x/2, (screen_y/2)), size=(40))
			static_text_raw_center("BACK", color=(255, 255, 255), position=(screen_x/2, (screen_y/2)+150), size=(30))
			static_text_raw_center("CLOSE GAME", color=(255, 255, 255), position=(screen_x/2, (screen_y/2)+190), size=(30))
			if colide_yes.collidepoint(mouse_x, mouse_y):
				screen.blit(_scaled_images["elucidate_select_exit"], ((screen_x/2)-100, (screen_y/2)+134))
				static_text_raw_center("BACK", color=(0, 0, 0), position=(screen_x/2, (screen_y/2)+150), size=(30))
				for event in events:
					if event.type == pygame.MOUSEBUTTONDOWN:
						loop_cytsuwjw = False
			elif colide_no.collidepoint(mouse_x, mouse_y):
				screen.blit(_scaled_images["elucidate_select_exit"], ((screen_x/2)-100, (screen_y/2)+174))
				static_text_raw_center("CLOSE GAME", color=(0, 0, 0), position=(screen_x/2, (screen_y/2)+190), size=(30))
				for event in events:
					if event.type == pygame.MOUSEBUTTONDOWN:
						elucidate_sys_exit()
			mouse()
			display()
# -- elucidate/main/functions/logic
	def resolve_collision(mover, obstacle):
		if not mover.colliderect(obstacle):
			return mover.x, mover.y
		overlap_left = mover.right - obstacle.left
		overlap_right = obstacle.right - mover.left
		overlap_top = mover.bottom - obstacle.top
		overlap_bot = obstacle.bottom - mover.top
		min_x = overlap_left if overlap_left < overlap_right else -overlap_right
		min_y = overlap_top if overlap_top < overlap_bot else -overlap_bot
		if abs(min_x) < abs(min_y):
			return mover.x - min_x, mover.y
		else:
			return mover.x, mover.y - min_y
# -- elucidate/main/class/player
	class Player:
# -- elucidate/main/class/player/self
		def __init__(self, class_name, x, y, pw, ph):
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
			self.anim_timer = 0
# -- elucidate/main/class/player/self/input
		def update_input(self):
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
		def draw(self, screen):
			sprite_set = SPRITES[self.sprite_type]
			if self.state == "idle":
				sprite = sprite_set["idle"][self.facing]
			elif self.state == "walk":
				frames = sprite_set["walk"][self.facing]
				self.anim_timer += 1
				if self.anim_timer > 10:
					self.anim_timer = 0
					self.anim_frame = (self.anim_frame + 1) % len(frames)
				sprite = frames[self.anim_frame]
			elif self.state == "attack":
				frames = sprite_set["attack"][self.facing]
				self.anim_timer += 1
				if self.anim_timer > 8:
					self.anim_timer = 0
					self.anim_frame = (self.anim_frame + 1) % len(frames)
				sprite = frames[self.anim_frame]
			else:
				sprite = sprite_set["idle"][self.facing]
			screen.blit(sprite, (int(self.x), int(self.y)))
# -- elucidate/main/functions/player
	def player(class_name, x, y, pw, ph):
		return Player(class_name, x, y, pw, ph)
		# to call : p = player("mercenary", 100, 200, 1275, 710)
# -- elucidate/main/run
	load_controls()
	home_random_bg = random.randint(1,9)
	home_bg_ran = _preloaded_images[f"elucidate_menu_bg_{home_random_bg:03d}"]
	colide_play = pygame.Rect(5, 561, 250, 35)
	colide_settings = pygame.Rect(5, 596, 250, 35)
	colide_exit = pygame.Rect(5, 631, 250, 35)
	colide_yes = pygame.Rect((screen_x/2)-100, (screen_y/2)+134, 200, 30)
	colide_no = pygame.Rect((screen_x/2)-100, (screen_y/2)+174, 200, 30)
	colide_graphics = pygame.Rect((screen_x/2)-100, 185, 200, 30)
	colide_audio = pygame.Rect((screen_x/2)-100, 220, 200, 30)
	colide_controls = pygame.Rect((screen_x/2)-100, 255, 200, 30)
	colide_authors = pygame.Rect((screen_x/2)-100, 290, 200, 30)
	colide_back = pygame.Rect((screen_x/2)-100, 635, 200, 30)
	colide_up = pygame.Rect((screen_x/2)-150, 185, 300, 30)
	colide_down = pygame.Rect((screen_x/2)-150, 225, 300, 30)
	colide_left = pygame.Rect((screen_x/2)-150, 265, 300, 30)
	colide_right = pygame.Rect((screen_x/2)-150, 305, 300, 30)
	colide_attack = pygame.Rect((screen_x/2)-150, 345, 300, 30)
	elucidate_main_run_home_play_newgame = pygame.Rect(5, 202, 250, 35)
	elucidate_main_run_home_play_more = pygame.Rect(5, 237, 250, 35)
	elucidate_main_run_home_play_back = pygame.Rect(5, 272, 250, 35)
	elucidate_main_run_home_play_back_select = pygame.Rect((screen_x/2)-100, 665, 200, 30)
	slider_x = (screen_x/2) - 200
	slider_y = 300
	slider_w = 400
	slider_h = 10
	knob_r = 12
	dragging_slider = False
	mute_rect = pygame.Rect((screen_x/2)-60, 360, 120, 35)
	waiting_for_key = None
	credits_player = None
	main_game_loop = True
	state = "version_check"
	sys_gen_loading(1)
	ambient("music/elucidate_calm.wav", -1)
	while main_game_loop:
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				elucidate_sys_exit()
		mouse_x, mouse_y = pygame.mouse.get_pos()
		if state == "version_check":
			screen.fill(sys_bg_color)
			screen.blit(_preloaded_images["elucidate_select_bg_002"], (0, 0))
			static_text_raw_center("The version you currently have is an outdated test version,", color=(255, 255, 255), position=(screen_x/2, (screen_y/2)-40), size=(40))
			static_text_raw_center("would you like to continue?", color=(255, 255, 255), position=(screen_x/2, (screen_y/2)), size=(40))
			static_text_raw_center("YES", color=(255, 255, 255), position=(screen_x/2, (screen_y/2)+150), size=(30))
			static_text_raw_center("NO", color=(255, 255, 255), position=(screen_x/2, (screen_y/2)+190), size=(30))
			if colide_yes.collidepoint(mouse_x, mouse_y):
				screen.blit(_scaled_images["elucidate_select_exit"], ((screen_x/2)-100, (screen_y/2)+134))
				static_text_raw_center("YES", color=(0, 0, 0), position=(screen_x/2, (screen_y/2)+150), size=(30))
				for event in events:
					if event.type == pygame.MOUSEBUTTONDOWN:
						state = "home"
			elif colide_no.collidepoint(mouse_x, mouse_y):
				screen.blit(_scaled_images["elucidate_select_exit"], ((screen_x/2)-100, (screen_y/2)+174))
				static_text_raw_center("NO", color=(0, 0, 0), position=(screen_x/2, (screen_y/2)+190), size=(30))
				for event in events:
					if event.type == pygame.MOUSEBUTTONDOWN:
						elucidate_sys_exit()
# -- elucidate/main/run/home/play/select
		elif state == "play_select":
			screen.fill(sys_bg_color)
			screen.blit(_preloaded_images["elucidate_select_bg_002"], (0, 0))
			static_text_raw_center("BACK", color=(255, 255, 255), position=(screen_x/2, 670), size=(30))
			static_text_raw_center("SELECT CHARACTER", color=(255, 255, 255), position=(screen_x/2, 80), size=(40))
			screen.blit(_scaled_images["elucidate_mcguy_001_999"], ((screen_x/2)-125, 100))
			screen.blit(_scaled_images["elucidate_mcguy_001_999"], ((screen_x/2)-325, 100))
			screen.blit(_scaled_images["elucidate_mcguy_001_999"], ((screen_x/2)-529, 100))
			screen.blit(_scaled_images["elucidate_mcguy_001_999"], ((screen_x/2)+78, 100))
			screen.blit(_scaled_images["elucidate_mcguy_001_999"], ((screen_x/2)+280, 100))
			screen.blit(_rotated_images["elucidate_select_ui_002_play_select_r"], ((screen_x/2)-125, 100))
			screen.blit(_rotated_images["elucidate_select_ui_002_play_select_r"], ((screen_x/2)-325, 100))
			screen.blit(_rotated_images["elucidate_select_ui_002_play_select_r"], ((screen_x/2)-529, 100))
			screen.blit(_rotated_images["elucidate_select_ui_002_play_select_r"], ((screen_x/2)+78, 100))
			screen.blit(_rotated_images["elucidate_select_ui_002_play_select_r"], ((screen_x/2)+280, 100))
			if elucidate_main_run_home_play_back_select.collidepoint(mouse_x, mouse_y):
				screen.blit(_scaled_images["elucidate_select_exit"], ((screen_x/2)-100, 665))
				static_text_raw_center("BACK", color=(0, 0, 0), position=(screen_x/2, 670), size=(30))
				for event in events:
					if event.type == pygame.MOUSEBUTTONDOWN:
						state = "play"
# -- elucidate/main/run/home
		elif state == "home":
			screen.fill(sys_bg_color)
			screen.blit(home_bg_ran, (0, 0))
			static_text_raw(text_home_001, color=(255, 255, 255), position=(5, 560), size=(35))
			static_text_raw(text_home_002, color=(255, 255, 255), position=(5, 595), size=(35))
			static_text_raw(text_home_003, color=(255, 255, 255), position=(5, 630), size=(35))
			if colide_play.collidepoint(mouse_x, mouse_y):
				screen.blit(_scaled_images["elucidate_select_home"], (5, 561))
				static_text_raw(text_home_001, color=(0, 0, 0), position=(25, 560), size=(35))
				for event in events:
					if event.type == pygame.MOUSEBUTTONDOWN:
						state = "play"
			elif colide_settings.collidepoint(mouse_x, mouse_y):
				screen.blit(_scaled_images["elucidate_select_home"], (5, 596))
				static_text_raw(text_home_002, color=(0, 0, 0), position=(25, 595), size=(35))
				for event in events:
					if event.type == pygame.MOUSEBUTTONDOWN:
						state = "settings"
			elif colide_exit.collidepoint(mouse_x, mouse_y):
				screen.blit(_scaled_images["elucidate_select_home"], (5, 631))
				static_text_raw(text_home_003, color=(0, 0, 0), position=(25, 630), size=(35))
				for event in events:
					if event.type == pygame.MOUSEBUTTONDOWN:
						state = "exit_confirm"
		elif state == "settings":
# -- elucidate/main/run/home/settings
			screen.fill(sys_bg_color)
			screen.blit(_preloaded_images["elucidate_select_bg_002"], (0, 0))
			static_text_raw_center(text_home_002, color=(255, 255, 255), position=(screen_x/2, 80), size=(50))
			static_text_raw_center("GRAPHICS", color=(255, 255, 255), position=(screen_x/2, 200), size=(30))
			static_text_raw_center("AUDIO", color=(255, 255, 255), position=(screen_x/2, 235), size=(30))
			static_text_raw_center("CONTROLS", color=(255, 255, 255), position=(screen_x/2, 270), size=(30))
			static_text_raw_center("CREDITS", color=(255, 255, 255), position=(screen_x/2, 305), size=(30))
			static_text_raw_center("BACK", color=(255, 255, 255), position=(screen_x/2, 650), size=(30))
			if colide_back.collidepoint(mouse_x, mouse_y):
				screen.blit(_scaled_images["elucidate_select_exit"], ((screen_x/2)-100, 635))
				static_text_raw_center("BACK", color=(0, 0, 0), position=(screen_x/2, 650), size=(30))
				for event in events:
					if event.type == pygame.MOUSEBUTTONDOWN:
						state = "home"
			elif colide_authors.collidepoint(mouse_x, mouse_y):
				screen.blit(_scaled_images["elucidate_select_exit"], ((screen_x/2)-100, 290))
				static_text_raw_center("CREDITS", color=(0, 0, 0), position=(screen_x/2, 305), size=(30))
				for event in events:
					if event.type == pygame.MOUSEBUTTONDOWN:
						credits_player = player("mercenary", (screen_x/2)-24, 560, 1275, 710)
						state = "settings_credits"
			elif colide_controls.collidepoint(mouse_x, mouse_y):
				screen.blit(_scaled_images["elucidate_select_exit"], ((screen_x/2)-100, 255))
				static_text_raw_center("CONTROLS", color=(0, 0, 0), position=(screen_x/2, 270), size=(30))
				for event in events:
					if event.type == pygame.MOUSEBUTTONDOWN:
						waiting_for_key = None
						state = "settings_controls"
			elif colide_audio.collidepoint(mouse_x, mouse_y):
				screen.blit(_scaled_images["elucidate_select_exit"], ((screen_x/2)-100, 220))
				static_text_raw_center("AUDIO", color=(0, 0, 0), position=(screen_x/2, 235), size=(30))
				for event in events:
					if event.type == pygame.MOUSEBUTTONDOWN:
						dragging_slider = False
						state = "settings_audio"
			elif colide_graphics.collidepoint(mouse_x, mouse_y):
				screen.blit(_scaled_images["elucidate_select_exit"], ((screen_x/2)-100, 185))
				static_text_raw_center("GRAPHICS", color=(0, 0, 0), position=(screen_x/2, 200), size=(30))
				for event in events:
					if event.type == pygame.MOUSEBUTTONDOWN:
						state = "settings_graphics"
		elif state == "settings_credits":
# -- elucidate/main/run/home/settings/credits
			screen.fill(sys_bg_color)
			screen.blit(_preloaded_images["elucidate_select_bg_002"], (0, 0))
			credits_player.update_input()
			credits_player.move(walls)
			credits_player.border()
			credits_player.draw(screen)
			static_text_raw_center("CREDITS", color=(255, 255, 255), position=(screen_x/2, 80), size=(50))
			static_text_raw_center("Baterbonia, Jose Gabriel", color=(255, 255, 255), position=(screen_x/2, 200), size=(30))
			static_text_raw_center("Capulong, Ivan Rafael", color=(255, 255, 255), position=(screen_x/2, 235), size=(30))
			static_text_raw_center("De Leon, Maximilian Kurt", color=(255, 255, 255), position=(screen_x/2, 270), size=(30))
			static_text_raw_center("Famero, Marc Roden", color=(255, 255, 255), position=(screen_x/2, 305), size=(30))
			static_text_raw_center("Tinoko, Gabrielle Keira", color=(255, 255, 255), position=(screen_x/2, 340), size=(30))
			static_text_raw_center("Vallite, John Alwyn", color=(255, 255, 255), position=(screen_x/2, 375), size=(30))
			static_text_raw_center("BACK", color=(255, 255, 255), position=(screen_x/2, 650), size=(30))
			if colide_back.collidepoint(mouse_x, mouse_y):
				screen.blit(_scaled_images["elucidate_select_exit"], ((screen_x/2)-100, 635))
				static_text_raw_center("BACK", color=(0, 0, 0), position=(screen_x/2, 650), size=(30))
				for event in events:
					if event.type == pygame.MOUSEBUTTONDOWN:
						state = "settings"
		elif state == "settings_controls":
# -- elucidate/main/run/home/settings/controls
			for event in events:
				if event.type == pygame.KEYDOWN and waiting_for_key:
					controls[waiting_for_key] = event.key
					save_controls()
					waiting_for_key = None
				if event.type == pygame.MOUSEBUTTONDOWN:
					if colide_up.collidepoint(event.pos):
						waiting_for_key = "move_up"
					elif colide_down.collidepoint(event.pos):
						waiting_for_key = "move_down"
					elif colide_left.collidepoint(event.pos):
						waiting_for_key = "move_left"
					elif colide_right.collidepoint(event.pos):
						waiting_for_key = "move_right"
					elif colide_attack.collidepoint(event.pos):
						waiting_for_key = "attack"
					elif colide_back.collidepoint(event.pos):
						state = "settings"
			screen.fill(sys_bg_color)
			screen.blit(_preloaded_images["elucidate_select_bg_002"], (0, 0))
			static_text_raw_center("CONTROLS", color=(255, 255, 255), position=(screen_x/2, 80), size=(50))
			static_text_raw_center(f"MOVE UP : {pygame.key.name(controls['move_up'])}", (255,255,255),(screen_x/2,200),30)
			static_text_raw_center(f"MOVE DOWN : {pygame.key.name(controls['move_down'])}", (255,255,255),(screen_x/2,240),30)
			static_text_raw_center(f"MOVE LEFT : {pygame.key.name(controls['move_left'])}", (255,255,255),(screen_x/2,280),30)
			static_text_raw_center(f"MOVE RIGHT : {pygame.key.name(controls['move_right'])}", (255,255,255),(screen_x/2,320),30)
			static_text_raw_center(f"ATTACK : {pygame.key.name(controls['attack'])}", (255,255,255),(screen_x/2,360),30)
			static_text_raw_center("BACK", color=(255, 255, 255), position=(screen_x/2, 650), size=(30))
			if colide_back.collidepoint(mouse_x, mouse_y):
				screen.blit(_scaled_images["elucidate_select_exit"], ((screen_x/2)-100, 635))
				static_text_raw_center("BACK", color=(0, 0, 0), position=(screen_x/2, 650), size=(30))
# -- elucidate/main/run/home/settings/audio
		elif state == "settings_audio":
			for event in events:
				if event.type == pygame.MOUSEBUTTONDOWN:
					if mute_rect.collidepoint(event.pos):
						sys_audio_muted = not sys_audio_muted
						sys_apply_audio_settings()
					if pygame.Rect(slider_x, slider_y-10, slider_w, 20).collidepoint(event.pos):
						dragging_slider = True
				if event.type == pygame.MOUSEBUTTONUP:
					dragging_slider = False
				if dragging_slider and event.type == pygame.MOUSEMOTION:
					value = max(0, min(1, (event.pos[0] - slider_x) / slider_w))
					sys_audio_volume = value
					sys_apply_audio_settings()
			if dragging_slider:
				value = max(0, min(1, (mouse_x - slider_x) / slider_w))
				sys_audio_volume = value
				sys_apply_audio_settings()
			screen.fill(sys_bg_color)
			screen.blit(_preloaded_images["elucidate_select_bg_002"], (0, 0))
			static_text_raw_center("AUDIO", color=(255, 255, 255), position=(screen_x/2, 80), size=(50))
			static_text_raw_center("BACK", color=(255, 255, 255), position=(screen_x/2, 650), size=(30))
			pygame.draw.rect(screen, ui_gray, (slider_x, slider_y, slider_w, slider_h))
			knob_x = slider_x + (sys_audio_volume * slider_w)
			pygame.draw.circle(screen, ui_crimson, (int(knob_x), slider_y + 5), knob_r)
			static_text_raw_center(f"VOLUME : {int(sys_audio_volume*100)}%", ui_white, (screen_x/2, 260), 30)
			pygame.draw.rect(screen, ui_crimson, mute_rect)
			if sys_audio_muted:
				static_text_raw_center("UNMUTE", ui_white, mute_rect.center, 25)
			else:
				static_text_raw_center("MUTE", ui_white, mute_rect.center, 25)
			if colide_back.collidepoint(mouse_x, mouse_y):
				screen.blit(_scaled_images["elucidate_select_exit"], ((screen_x/2)-100, 635))
				static_text_raw_center("BACK", color=(0, 0, 0), position=(screen_x/2, 650), size=(30))
				for event in events:
					if event.type == pygame.MOUSEBUTTONDOWN:
						state = "settings"
# -- elucidate/main/run/home/settings/graphics
		elif state == "settings_graphics":
			screen.fill(sys_bg_color)
			screen.blit(_preloaded_images["elucidate_select_bg_002"], (0, 0))
			static_text_raw_center("GRAPHICS", color=(255, 255, 255), position=(screen_x/2, 80), size=(50))
			static_text_raw_center("BACK", color=(255, 255, 255), position=(screen_x/2, 650), size=(30))
			static_text_raw_center("Current version doesn't support this settings.", color=(255, 255, 255), position=(screen_x/2, 200), size=(30))
			static_text_raw_center("[You are currently playing on a stable pre-released version]", color=(255, 255, 255), position=(screen_x/2, 230), size=(15))
			static_text_raw_center("[ver : Alpha 1.0.185]", color=(255, 255, 255), position=(screen_x/2, 245), size=(15))
			if colide_back.collidepoint(mouse_x, mouse_y):
				screen.blit(_scaled_images["elucidate_select_exit"], ((screen_x/2)-100, 635))
				static_text_raw_center("BACK", color=(0, 0, 0), position=(screen_x/2, 650), size=(30))
				for event in events:
					if event.type == pygame.MOUSEBUTTONDOWN:
						state = "settings"
# -- elucidate/main/run/home/exit
		elif state == "exit_confirm":
			screen.fill(sys_bg_color)
			screen.blit(_preloaded_images["elucidate_select_bg_002"], (0, 0))
			static_text_raw_center("ARE YOU SURE YOU WANT TO EXIT THE GAME?", color=(255, 255, 255), position=(screen_x/2, (screen_y/2)-40), size=(40))
			static_text_raw_center("YES", color=(255, 255, 255), position=(screen_x/2, (screen_y/2)+150), size=(30))
			static_text_raw_center("NO", color=(255, 255, 255), position=(screen_x/2, (screen_y/2)+190), size=(30))
			if colide_yes.collidepoint(mouse_x, mouse_y):
				screen.blit(_scaled_images["elucidate_select_exit"], ((screen_x/2)-100, (screen_y/2)+134))
				static_text_raw_center("YES", color=(0, 0, 0), position=(screen_x/2, (screen_y/2)+150), size=(30))
				for event in events:
					if event.type == pygame.MOUSEBUTTONDOWN:
						elucidate_sys_exit()
			elif colide_no.collidepoint(mouse_x, mouse_y):
				screen.blit(_scaled_images["elucidate_select_exit"], ((screen_x/2)-100, (screen_y/2)+174))
				static_text_raw_center("NO", color=(0, 0, 0), position=(screen_x/2, (screen_y/2)+190), size=(30))
				for event in events:
					if event.type == pygame.MOUSEBUTTONDOWN:
						state = "home"
# -- elucidate/main/run/home/play
		elif state == "play":
			screen.fill(sys_bg_color)
			screen.blit(_preloaded_images["elucidate_select_bg_001"], (0, 0))
			static_text_raw("NEW GAME", color=(255, 255, 255), position=(5, 200), size=(35))
			static_text_raw("MORE", color=(255, 255, 255), position=(5, 235), size=(35))
			static_text_raw("BACK", color=(255, 255, 255), position=(5, 270), size=(35))
			if elucidate_main_run_home_play_newgame.collidepoint(mouse_x, mouse_y):
				screen.blit(_scaled_images["elucidate_select_home"], (5, 202))
				static_text_raw("NEW GAME", color=(0, 0, 0), position=(5, 200), size=(35))
				for event in events:
					if event.type == pygame.MOUSEBUTTONDOWN:
						state = "play_select"
			if elucidate_main_run_home_play_more.collidepoint(mouse_x, mouse_y):
				screen.blit(_scaled_images["elucidate_select_home"], (5, 237))
				static_text_raw("MORE", color=(0, 0, 0), position=(5, 235), size=(35))
				for event in events:
					if event.type == pygame.MOUSEBUTTONDOWN:
						sys_gen_update_error()
			if elucidate_main_run_home_play_back.collidepoint(mouse_x, mouse_y):
				screen.blit(_scaled_images["elucidate_select_home"], (5, 272))
				static_text_raw("BACK", color=(0, 0, 0), position=(5, 270), size=(35))
				for event in events:
					if event.type == pygame.MOUSEBUTTONDOWN:
						state = "home"

# -- elucidate/main/run/else_state
		else:
			state = "home"
		mouse()
		display()
elucidate()