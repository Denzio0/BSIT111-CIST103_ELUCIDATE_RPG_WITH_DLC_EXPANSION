import importlib, subprocess, sys
libs = ["pygame", "requests", "gdown", "psutil"]
for lib in libs:
	try:
		globals()[lib] = importlib.import_module(lib)
	except ImportError:
		subprocess.check_call([sys.executable, "-m", "pip", "install", lib])
		globals()[lib] = importlib.import_module(lib)
import pygame
import sys
import os
import requests
import zipfile
import gdown
import shutil
import time
import random
import json
import math
import threading
pygame.init()
screen_x, screen_y = 1275, 710
screen = pygame.display.set_mode((screen_x, screen_y), pygame.RESIZABLE)
pygame.display.set_caption("Elucidate RPG Launcher")
font = pygame.font.SysFont("Times New Roman", 20)
THEME_CONFIG_FILE = "theme_config.json"
THEME_COUNT = 5
THEME_BLUE_STARS = 0
THEME_NEON       = 1
THEME_RED        = 2
THEME_GRAY       = 3
THEME_WHITE      = 4
def _load_theme():
	if os.path.exists(THEME_CONFIG_FILE):
		try:
			with open(THEME_CONFIG_FILE, "r") as f:
				data = json.load(f)
			idx = int(data.get("theme", THEME_GRAY))
			if 0 <= idx < THEME_COUNT:
				return idx
		except Exception:
			pass
	return THEME_GRAY
def _save_theme(idx):
	try:
		with open(THEME_CONFIG_FILE, "w") as f:
			json.dump({"theme": idx}, f)
	except Exception:
		pass
_current_theme = _load_theme()
_stars = [
	{
		"x": random.randint(0, 1275),
		"y": random.randint(0, 710),
		"r": random.randint(1, 2),
		"phase": random.uniform(0, 6.28),
		"speed": random.uniform(0.5, 2.5),
	}
	for _ in range(160)
]
_neon_time = 0.0
_red_particles = [
	{
		"x": random.uniform(0, 1275),
		"y": random.uniform(0, 710),
		"vy": random.uniform(-0.4, -1.6),
		"vx": random.uniform(-0.3, 0.3),
		"r":  random.randint(2, 5),
		"alpha": random.randint(80, 220),
		"life": random.uniform(0, 1.0),
	}
	for _ in range(120)
]
_red_last_t = time.time()
def _update_stars():
	t = time.time()
	for s in _stars:
		s["phase"] += s["speed"] * 0.016
def _draw_stars_bg():
	screen.fill((5, 8, 22))
	t = time.time()
	for s in _stars:
		bri = int(120 + 120 * (0.5 + 0.5 * math.sin(s["phase"])))
		bri = max(30, min(255, bri))
		col = (bri // 3, bri // 2, bri)
		pygame.draw.circle(screen, col, (int(s["x"]), int(s["y"])), s["r"])
	_update_stars()
def _update_red_particles(dt):
	for p in _red_particles:
		p["x"] += p["vx"]
		p["y"] += p["vy"]
		p["life"] += dt * 0.3
		if p["life"] >= 1.0 or p["y"] < -10:
			p["x"]     = random.uniform(0, screen_x)
			p["y"]     = screen_y + 5
			p["vy"]    = random.uniform(-0.4, -1.6)
			p["vx"]    = random.uniform(-0.3, 0.3)
			p["r"]     = random.randint(2, 5)
			p["alpha"] = random.randint(80, 220)
			p["life"]  = 0.0
def _draw_red_bg():
	global _red_last_t
	now = time.time()
	dt  = now - _red_last_t
	_red_last_t = now
	screen.fill((12, 0, 0))
	_update_red_particles(dt)
	psurf = pygame.Surface((screen_x, screen_y), pygame.SRCALPHA)
	for p in _red_particles:
		alpha = int(p["alpha"] * (1.0 - p["life"]))
		alpha = max(0, min(255, alpha))
		rb    = int(180 + 60 * (1.0 - p["life"]))
		pygame.draw.circle(psurf, (rb, 0, 0, alpha), (int(p["x"]), int(p["y"])), p["r"])
	screen.blit(psurf, (0, 0))
def _draw_neon_bg():
	global _neon_time
	_neon_time += 0.018
	screen.fill((4, 0, 14))
	for i in range(6):
		t   = _neon_time + i * 1.05
		x1  = int(screen_x * (0.5 + 0.5 * math.sin(t * 0.31 + i)))
		y1  = int(screen_y * (0.5 + 0.5 * math.cos(t * 0.27 + i * 0.7)))
		x2  = int(screen_x * (0.5 + 0.5 * math.cos(t * 0.19 + i * 1.3)))
		y2  = int(screen_y * (0.5 + 0.5 * math.sin(t * 0.23 + i * 0.4)))
		cols = [
			(0, 255, 200),
			(255, 0, 180),
			(0, 150, 255),
			(200, 0, 255),
			(0, 255, 100),
			(255, 80, 0),
		]
		c = cols[i % len(cols)]
		lsurf = pygame.Surface((screen_x, screen_y), pygame.SRCALPHA)
		pygame.draw.line(lsurf, (*c, 18), (x1, y1), (x2, y2), 2)
		screen.blit(lsurf, (0, 0))
def _theme_bg():
	if _current_theme == THEME_BLUE_STARS:
		_draw_stars_bg()
	elif _current_theme == THEME_NEON:
		_draw_neon_bg()
	elif _current_theme == THEME_RED:
		_draw_red_bg()
	elif _current_theme == THEME_WHITE:
		screen.fill((240, 240, 240))
	else:
		screen.fill((10, 10, 10))
def _theme_panel_bg():
	if _current_theme == THEME_BLUE_STARS:
		return (12, 18, 45)
	elif _current_theme == THEME_NEON:
		return (8, 0, 22)
	elif _current_theme == THEME_RED:
		return (22, 4, 4)
	elif _current_theme == THEME_WHITE:
		return (255, 255, 255)
	else:
		return (38, 38, 38)
def _theme_panel_border():
	if _current_theme == THEME_BLUE_STARS:
		return (40, 80, 160)
	elif _current_theme == THEME_NEON:
		return (0, 220, 180)
	elif _current_theme == THEME_RED:
		return (180, 30, 30)
	elif _current_theme == THEME_WHITE:
		return (160, 160, 160)
	else:
		return (80, 80, 75)
def _theme_sub_bg():
	if _current_theme == THEME_BLUE_STARS:
		return (8, 14, 38)
	elif _current_theme == THEME_NEON:
		return (4, 0, 16)
	elif _current_theme == THEME_RED:
		return (16, 2, 2)
	elif _current_theme == THEME_WHITE:
		return (230, 230, 230)
	else:
		return (28, 28, 28)
def _theme_sub_border():
	if _current_theme == THEME_BLUE_STARS:
		return (30, 60, 130)
	elif _current_theme == THEME_NEON:
		return (0, 180, 140)
	elif _current_theme == THEME_RED:
		return (140, 20, 20)
	elif _current_theme == THEME_WHITE:
		return (180, 180, 180)
	else:
		return (60, 60, 58)
def _theme_bar_fill():
	if _current_theme == THEME_BLUE_STARS:
		return (40, 100, 220)
	elif _current_theme == THEME_NEON:
		return (0, 255, 190)
	elif _current_theme == THEME_RED:
		return (210, 30, 30)
	elif _current_theme == THEME_WHITE:
		return (80, 80, 200)
	else:
		return (180, 180, 160)
def _theme_bar_shine():
	if _current_theme == THEME_BLUE_STARS:
		return (80, 160, 255)
	elif _current_theme == THEME_NEON:
		return (180, 255, 240)
	elif _current_theme == THEME_RED:
		return (255, 80, 80)
	elif _current_theme == THEME_WHITE:
		return (140, 140, 255)
	else:
		return (230, 230, 210)
def _theme_text_main():
	if _current_theme == THEME_WHITE:
		return (20, 20, 20)
	elif _current_theme == THEME_NEON:
		return (0, 255, 200)
	elif _current_theme == THEME_RED:
		return (255, 180, 180)
	elif _current_theme == THEME_BLUE_STARS:
		return (160, 200, 255)
	else:
		return (210, 205, 195)
def _theme_text_dim():
	if _current_theme == THEME_WHITE:
		return (60, 60, 60)
	elif _current_theme == THEME_NEON:
		return (0, 200, 160)
	elif _current_theme == THEME_RED:
		return (200, 80, 80)
	elif _current_theme == THEME_BLUE_STARS:
		return (80, 130, 220)
	else:
		return (140, 135, 125)
def _theme_text_label():
	if _current_theme == THEME_WHITE:
		return (90, 90, 90)
	elif _current_theme == THEME_NEON:
		return (0, 160, 130)
	elif _current_theme == THEME_RED:
		return (160, 50, 50)
	elif _current_theme == THEME_BLUE_STARS:
		return (60, 100, 180)
	else:
		return (120, 115, 105)
def _theme_outer_border():
	if _current_theme == THEME_BLUE_STARS:
		return (40, 80, 160)
	elif _current_theme == THEME_NEON:
		return (0, 255, 190)
	elif _current_theme == THEME_RED:
		return (180, 30, 30)
	elif _current_theme == THEME_WHITE:
		return (140, 140, 140)
	else:
		return (70, 70, 65)
def _theme_footer_text():
	if _current_theme == THEME_WHITE:
		return (100, 100, 100)
	elif _current_theme == THEME_NEON:
		return (0, 180, 140)
	elif _current_theme == THEME_RED:
		return (160, 60, 60)
	elif _current_theme == THEME_BLUE_STARS:
		return (60, 100, 180)
	else:
		return (90, 88, 84)
def _theme_footer_bg():
	if _current_theme == THEME_BLUE_STARS:
		return (6, 10, 28)
	elif _current_theme == THEME_NEON:
		return (4, 0, 16)
	elif _current_theme == THEME_RED:
		return (14, 2, 2)
	elif _current_theme == THEME_WHITE:
		return (210, 210, 210)
	else:
		return (25, 25, 25)
def _theme_bar_empty_bg():
	if _current_theme == THEME_BLUE_STARS:
		return (10, 16, 40)
	elif _current_theme == THEME_NEON:
		return (4, 0, 18)
	elif _current_theme == THEME_RED:
		return (18, 2, 2)
	elif _current_theme == THEME_WHITE:
		return (200, 200, 200)
	else:
		return (30, 30, 30)
def draw_text(text, x, y):
	surf = font.render(text, True, (255, 255, 255))
	screen.blit(surf, (x, y))
def draw_text_ui(text, x, y, color=(220, 220, 220)):
	surf = font.render(text, True, color)
	screen.blit(surf, (x, y))
def draw_verify_bg():
	_theme_bg()
	pygame.draw.rect(screen, _theme_footer_bg(), (0, screen_y - 40, screen_x, 40))
	draw_text_ui("ELUCIDATE  ·  ASSET VERIFICATION SYSTEM", screen_x // 2 - 200, screen_y - 28, _theme_footer_text())
mini_game_active = False
_si_lock = threading.Lock()
_si = {
	"player_x": 0.0,
	"player_y": 0.0,
	"player_w": 40,
	"player_h": 22,
	"player_speed": 320.0,
	"bullets": [],
	"enemy_bullets": [],
	"enemies": [],
	"score": 0,
	"lives": 3,
	"game_over": False,
	"won": False,
	"shoot_cooldown": 0.0,
	"enemy_dir": 1,
	"enemy_speed": 60.0,
	"enemy_drop": 18,
	"enemy_shoot_timer": 0.0,
	"enemy_shoot_interval": 1.4,
	"last_time": 0.0,
	"explosions": [],
	"stars": [],
	"wave": 1,
	"flash_timer": 0.0,
	"hi_score": 0,
	"scroll_y": 0.0,
}

_si_font_large  = None
_si_font_medium = None
_si_font_small  = None

_SI_GX  = 80
_SI_GY  = 60
_SI_GW  = 1115
_SI_GH  = 590

def _si_make_fonts():
	global _si_font_large, _si_font_medium, _si_font_small
	_si_font_large  = pygame.font.SysFont("Courier New", 32, bold=True)
	_si_font_medium = pygame.font.SysFont("Courier New", 20, bold=True)
	_si_font_small  = pygame.font.SysFont("Courier New", 14)

def _si_spawn_enemies(wave):
	rows = min(4 + wave, 7)
	cols = min(9 + wave, 14)
	pad_x = 10
	pad_y = 8
	cell_w = (_SI_GW - pad_x * 2) // cols
	cell_h = 36
	start_x = _SI_GX + pad_x
	start_y  = _SI_GY + 50
	enemies = []
	for r in range(rows):
		for c in range(cols):
			ex = start_x + c * cell_w + cell_w // 2
			ey = start_y + r * cell_h
			if r == 0:
				kind = 2
				pts  = 30
			elif r <= 2:
				kind = 1
				pts  = 20
			else:
				kind = 0
				pts  = 10
			enemies.append({
				"x": float(ex),
				"y": float(ey),
				"w": 28,
				"h": 18,
				"kind": kind,
				"alive": True,
				"anim": 0,
				"anim_timer": 0.0,
			})
	return enemies

def _si_spawn_bg_stars():
	stars = []
	for _ in range(80):
		stars.append({
			"x": random.uniform(_SI_GX, _SI_GX + _SI_GW),
			"y": random.uniform(_SI_GY, _SI_GY + _SI_GH),
			"spd": random.uniform(12, 40),
			"r": random.choice([1, 1, 1, 2]),
			"bri": random.randint(80, 200),
		})
	return stars

def init_space_invaders():
	global _si
	if _si_font_large is None:
		_si_make_fonts()
	with _si_lock:
		_si["player_x"]            = float(_SI_GX + _SI_GW // 2)
		_si["player_y"]            = float(_SI_GY + _SI_GH - 36)
		_si["bullets"]             = []
		_si["enemy_bullets"]       = []
		_si["score"]               = 0
		_si["lives"]               = 3
		_si["game_over"]           = False
		_si["won"]                 = False
		_si["shoot_cooldown"]      = 0.0
		_si["enemy_dir"]           = 1
		_si["enemy_speed"]         = 60.0
		_si["enemy_drop"]          = 18
		_si["enemy_shoot_timer"]   = 0.0
		_si["enemy_shoot_interval"] = 1.4
		_si["last_time"]           = time.time()
		_si["explosions"]          = []
		_si["stars"]               = _si_spawn_bg_stars()
		_si["wave"]                = 1
		_si["flash_timer"]         = 0.0
		_si["scroll_y"]            = 0.0
		_si["enemies"]             = _si_spawn_enemies(1)

def _si_next_wave():
	with _si_lock:
		_si["wave"]               += 1
		_si["enemy_speed"]         = min(60.0 + (_si["wave"] - 1) * 18.0, 200.0)
		_si["enemy_shoot_interval"] = max(1.4 - (_si["wave"] - 1) * 0.15, 0.45)
		_si["bullets"]             = []
		_si["enemy_bullets"]       = []
		_si["explosions"]          = []
		_si["enemies"]             = _si_spawn_enemies(_si["wave"])
		_si["player_x"]            = float(_SI_GX + _SI_GW // 2)
		_si["flash_timer"]         = 1.2
		_si["won"]                 = False
		_si["game_over"]           = False

def _si_rect_collide(ax, ay, aw, ah, bx, by, bw, bh):
	return (abs(ax - bx) < (aw + bw) / 2 and abs(ay - by) < (ah + bh) / 2)

def update_space_invaders():
	global mini_game_active
	now = time.time()
	with _si_lock:
		dt = min(now - _si["last_time"], 0.05)
		_si["last_time"] = now

		if _si["game_over"] or _si["won"]:
			return

		for s in _si["stars"]:
			s["y"] += s["spd"] * dt
			if s["y"] > _SI_GY + _SI_GH:
				s["y"] = float(_SI_GY)
				s["x"] = random.uniform(_SI_GX, _SI_GX + _SI_GW)

		if _si["flash_timer"] > 0:
			_si["flash_timer"] -= dt

		keys = pygame.key.get_pressed()
		px = _si["player_x"]
		pw = _si["player_w"]
		spd = _si["player_speed"]
		left_bound  = _SI_GX + pw // 2 + 4
		right_bound = _SI_GX + _SI_GW - pw // 2 - 4
		if keys[pygame.K_LEFT] or keys[pygame.K_a]:
			px -= spd * dt
		if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
			px += spd * dt
		px = max(left_bound, min(right_bound, px))
		_si["player_x"] = px

		if _si["shoot_cooldown"] > 0:
			_si["shoot_cooldown"] -= dt
		if keys[pygame.K_F1] and _si["shoot_cooldown"] <= 0:
			_si["bullets"].append({
				"x": _si["player_x"],
				"y": _si["player_y"] - _si["player_h"] // 2 - 2,
				"spd": 480.0,
			})
			_si["shoot_cooldown"] = 0.22

		new_bullets = []
		for b in _si["bullets"]:
			b["y"] -= b["spd"] * dt
			if b["y"] >= _SI_GY:
				new_bullets.append(b)
		_si["bullets"] = new_bullets

		alive_enemies = [e for e in _si["enemies"] if e["alive"]]

		hit_bullets = set()
		for bi, b in enumerate(_si["bullets"]):
			for e in alive_enemies:
				if _si_rect_collide(b["x"], b["y"], 4, 12, e["x"], e["y"], e["w"], e["h"]):
					e["alive"] = False
					hit_bullets.add(bi)
					pts = 30 if e["kind"] == 2 else (20 if e["kind"] == 1 else 10)
					_si["score"] += pts
					_si["explosions"].append({
						"x": e["x"], "y": e["y"],
						"r": 4, "max_r": 22,
						"alpha": 255, "timer": 0.38,
						"color": (255, 200, 60) if e["kind"] == 2 else (80, 220, 255),
					})
					break
		_si["bullets"] = [b for bi, b in enumerate(_si["bullets"]) if bi not in hit_bullets]

		if alive_enemies:
			xs = [e["x"] for e in alive_enemies]
			min_x = min(xs)
			max_x = max(xs)
			half_w = 14
			move = _si["enemy_speed"] * dt * _si["enemy_dir"]
			drop = False
			if _si["enemy_dir"] == 1 and max_x + half_w + move >= _SI_GX + _SI_GW - 4:
				drop = True
			elif _si["enemy_dir"] == -1 and min_x - half_w + move <= _SI_GX + 4:
				drop = True
			if drop:
				_si["enemy_dir"] *= -1
				for e in alive_enemies:
					e["y"] += _si["enemy_drop"]
			else:
				for e in alive_enemies:
					e["x"] += move

			for e in _si["enemies"]:
				e["anim_timer"] += dt
				if e["anim_timer"] >= 0.5:
					e["anim_timer"] = 0.0
					e["anim"] = 1 - e["anim"]

			_si["enemy_shoot_timer"] -= dt
			if _si["enemy_shoot_timer"] <= 0:
				_si["enemy_shoot_timer"] = _si["enemy_shoot_interval"] + random.uniform(-0.1, 0.2)
				shooters = random.sample(alive_enemies, min(2, len(alive_enemies)))
				for sh in shooters:
					_si["enemy_bullets"].append({
						"x": sh["x"],
						"y": sh["y"] + sh["h"] // 2 + 2,
						"spd": 190.0 + random.uniform(0, 60),
					})

			for e in alive_enemies:
				if e["y"] + e["h"] // 2 >= _si["player_y"] - _si["player_h"] // 2:
					_si["game_over"] = True
					break

		new_eb = []
		for eb in _si["enemy_bullets"]:
			eb["y"] += eb["spd"] * dt
			if eb["y"] > _SI_GY + _SI_GH:
				continue
			if _si_rect_collide(eb["x"], eb["y"], 4, 10, _si["player_x"], _si["player_y"], _si["player_w"], _si["player_h"]):
				_si["lives"] -= 1
				_si["explosions"].append({
					"x": _si["player_x"], "y": _si["player_y"],
					"r": 6, "max_r": 30,
					"alpha": 255, "timer": 0.55,
					"color": (255, 80, 40),
				})
				if _si["lives"] <= 0:
					_si["game_over"] = True
				continue
			new_eb.append(eb)
		_si["enemy_bullets"] = new_eb

		new_exp = []
		for ex in _si["explosions"]:
			ex["timer"] -= dt
			ex["r"]     += (ex["max_r"] - ex["r"]) * dt * 6
			ex["alpha"]  = int(255 * max(0, ex["timer"] / 0.55))
			if ex["timer"] > 0:
				new_exp.append(ex)
		_si["explosions"] = new_exp

		alive_enemies = [e for e in _si["enemies"] if e["alive"]]
		if not alive_enemies and not _si["game_over"]:
			_si["won"] = True
			if _si["score"] > _si.get("hi_score", 0):
				_si["hi_score"] = _si["score"]

def _si_draw_enemy(surf, e, ox, oy):
	ex = int(e["x"])
	ey = int(e["y"])
	ew = e["w"]
	eh = e["h"]
	anim = e["anim"]
	kind = e["kind"]
	if kind == 2:
		col_body  = (80, 220, 255)
		col_eye   = (255, 255, 100)
		col_leg   = (40, 180, 220)
		pygame.draw.ellipse(surf, col_body, (ex - 13, ey - 8, 26, 14))
		pygame.draw.circle(surf, col_eye, (ex - 4, ey - 3), 3)
		pygame.draw.circle(surf, col_eye, (ex + 4, ey - 3), 3)
		if anim == 0:
			pygame.draw.line(surf, col_leg, (ex - 12, ey + 5), (ex - 16, ey + 10), 2)
			pygame.draw.line(surf, col_leg, (ex,      ey + 6), (ex,      ey + 11), 2)
			pygame.draw.line(surf, col_leg, (ex + 12, ey + 5), (ex + 16, ey + 10), 2)
		else:
			pygame.draw.line(surf, col_leg, (ex - 12, ey + 5), (ex - 8,  ey + 11), 2)
			pygame.draw.line(surf, col_leg, (ex,      ey + 6), (ex - 4,  ey + 11), 2)
			pygame.draw.line(surf, col_leg, (ex + 12, ey + 5), (ex + 8,  ey + 11), 2)
	elif kind == 1:
		col_body  = (120, 255, 140)
		col_eye   = (255, 80, 80)
		col_leg   = (60, 180, 80)
		pygame.draw.rect(surf, col_body, (ex - 11, ey - 7, 22, 12), border_radius=3)
		pygame.draw.circle(surf, col_eye, (ex - 4, ey - 2), 2)
		pygame.draw.circle(surf, col_eye, (ex + 4, ey - 2), 2)
		if anim == 0:
			pygame.draw.line(surf, col_leg, (ex - 9, ey + 4), (ex - 13, ey + 9), 2)
			pygame.draw.line(surf, col_leg, (ex + 9, ey + 4), (ex + 13, ey + 9), 2)
		else:
			pygame.draw.line(surf, col_leg, (ex - 9, ey + 4), (ex - 6,  ey + 9), 2)
			pygame.draw.line(surf, col_leg, (ex + 9, ey + 4), (ex + 6,  ey + 9), 2)
	else:
		col_body  = (220, 180, 255)
		col_eye   = (255, 255, 255)
		col_leg   = (160, 120, 220)
		pygame.draw.ellipse(surf, col_body, (ex - 10, ey - 6, 20, 12))
		pygame.draw.circle(surf, col_eye, (ex - 3, ey - 1), 2)
		pygame.draw.circle(surf, col_eye, (ex + 3, ey - 1), 2)
		if anim == 0:
			pygame.draw.line(surf, col_leg, (ex - 8, ey + 5), (ex - 12, ey + 9), 2)
			pygame.draw.line(surf, col_leg, (ex,     ey + 6), (ex,      ey + 10), 2)
			pygame.draw.line(surf, col_leg, (ex + 8, ey + 5), (ex + 12, ey + 9), 2)
		else:
			pygame.draw.line(surf, col_leg, (ex - 8, ey + 5), (ex - 4,  ey + 9), 2)
			pygame.draw.line(surf, col_leg, (ex,     ey + 6), (ex + 4,  ey + 10), 2)
			pygame.draw.line(surf, col_leg, (ex + 8, ey + 5), (ex + 4,  ey + 9), 2)

def _si_draw_player(surf, px, py, pw, ph):
	cx = int(px)
	cy = int(py)
	col_hull    = (80, 200, 255)
	col_cockpit = (40, 120, 200)
	col_engine  = (60, 160, 220)
	col_exhaust = (255, 160, 40)
	points_hull = [
		(cx,        cy - ph // 2 - 4),
		(cx - pw // 2, cy + ph // 2),
		(cx + pw // 2, cy + ph // 2),
	]
	pygame.draw.polygon(surf, col_hull, points_hull)
	pygame.draw.polygon(surf, (120, 220, 255), points_hull, 1)
	pygame.draw.ellipse(surf, col_cockpit, (cx - 6, cy - 8, 12, 10))
	pygame.draw.line(surf, col_engine, (cx - pw // 2, cy + ph // 2 - 2), (cx - pw // 2 - 6, cy + ph // 2), 2)
	pygame.draw.line(surf, col_engine, (cx + pw // 2, cy + ph // 2 - 2), (cx + pw // 2 + 6, cy + ph // 2), 2)
	flicker = random.randint(0, 30)
	pygame.draw.line(surf, (255, max(0, 100 + flicker), 0), (cx, cy + ph // 2), (cx, cy + ph // 2 + 8 + flicker // 8), 3)

def draw_space_invaders():
	with _si_lock:
		snap_player_x      = _si["player_x"]
		snap_player_y      = _si["player_y"]
		snap_player_w      = _si["player_w"]
		snap_player_h      = _si["player_h"]
		snap_bullets       = list(_si["bullets"])
		snap_enemy_bullets = list(_si["enemy_bullets"])
		snap_enemies       = [dict(e) for e in _si["enemies"]]
		snap_score         = _si["score"]
		snap_lives         = _si["lives"]
		snap_game_over     = _si["game_over"]
		snap_won           = _si["won"]
		snap_explosions    = [dict(ex) for ex in _si["explosions"]]
		snap_stars         = list(_si["stars"])
		snap_wave          = _si["wave"]
		snap_flash         = _si["flash_timer"]
		snap_hi            = _si.get("hi_score", 0)

	screen.fill((2, 2, 8))

	gx = _SI_GX
	gy = _SI_GY
	gw = _SI_GW
	gh = _SI_GH

	pygame.draw.rect(screen, (4, 6, 20), (gx, gy, gw, gh))

	for s in snap_stars:
		bri = int(s["bri"])
		pygame.draw.circle(screen, (bri, bri, bri), (int(s["x"]), int(s["y"])), s["r"])

	pygame.draw.rect(screen, (0, 50, 120), (gx, gy, gw, gh), 2)

	ground_y = gy + gh - 2
	pygame.draw.line(screen, (0, 160, 220), (gx, ground_y), (gx + gw, ground_y), 2)

	for e in snap_enemies:
		if e["alive"]:
			_si_draw_enemy(screen, e, gx, gy)

	for b in snap_bullets:
		bx = int(b["x"])
		by = int(b["y"])
		pygame.draw.rect(screen, (80, 220, 255), (bx - 2, by - 6, 4, 12))
		pygame.draw.rect(screen, (200, 240, 255), (bx - 1, by - 6, 2, 8))

	for eb in snap_enemy_bullets:
		bx = int(eb["x"])
		by = int(eb["y"])
		pygame.draw.rect(screen, (255, 80, 80), (bx - 2, by - 5, 4, 10))
		pygame.draw.rect(screen, (255, 200, 200), (bx - 1, by - 4, 2, 6))

	_si_draw_player(screen, snap_player_x, snap_player_y, snap_player_w, snap_player_h)

	for ex in snap_explosions:
		r     = int(ex["r"])
		alpha = ex["alpha"]
		ecol  = ex["color"]
		esurf = pygame.Surface((r * 2 + 2, r * 2 + 2), pygame.SRCALPHA)
		pygame.draw.circle(esurf, (*ecol, alpha),        (r + 1, r + 1), r)
		pygame.draw.circle(esurf, (255, 255, 255, alpha // 2), (r + 1, r + 1), max(1, r // 2))
		screen.blit(esurf, (int(ex["x"]) - r - 1, int(ex["y"]) - r - 1))

	hud_y = gy - 44
	pygame.draw.rect(screen, (6, 8, 28), (gx, hud_y, gw, 40))
	pygame.draw.rect(screen, (0, 80, 160), (gx, hud_y, gw, 40), 1)

	score_surf = _si_font_medium.render(f"SCORE  {snap_score:06d}", True, (0, 220, 255))
	screen.blit(score_surf, (gx + 14, hud_y + 10))

	hi_surf = _si_font_medium.render(f"BEST  {snap_hi:06d}", True, (180, 180, 80))
	screen.blit(hi_surf, (gx + gw // 2 - hi_surf.get_width() // 2, hud_y + 10))

	wave_surf = _si_font_medium.render(f"WAVE  {snap_wave}", True, (120, 255, 160))
	screen.blit(wave_surf, (gx + gw - wave_surf.get_width() - 14, hud_y + 10))

	lives_y = gy + gh + 6
	pygame.draw.rect(screen, (6, 8, 28), (gx, lives_y, gw, 30))
	pygame.draw.rect(screen, (0, 80, 160), (gx, lives_y, gw, 30), 1)
	lives_label = _si_font_small.render("SHIPS:", True, (100, 180, 255))
	screen.blit(lives_label, (gx + 10, lives_y + 8))
	for li in range(snap_lives):
		lx = gx + 70 + li * 26
		ly = lives_y + 14
		pts = [(lx, ly - 9), (lx - 9, ly + 5), (lx + 9, ly + 5)]
		pygame.draw.polygon(screen, (60, 180, 255), pts)

	hint_surf = _si_font_small.render("[F8 / CLOSE]   [ARROWS/AD / MOVE]   [F1 / SHOOT]", True, (60, 80, 110))
	screen.blit(hint_surf, (gx + gw - hint_surf.get_width() - 10, lives_y + 8))

	if snap_flash > 0 and not snap_game_over and not snap_won:
		t = snap_flash
		alpha = int(min(255, t * 220))
		fsurf = pygame.Surface((gw, gh), pygame.SRCALPHA)
		fsurf.fill((80, 220, 120, alpha // 6))
		screen.blit(fsurf, (gx, gy))
		wave_big = _si_font_large.render(f"WAVE  {snap_wave}", True, (80, 255, 160))
		wx = gx + gw // 2 - wave_big.get_width() // 2
		wy = gy + gh // 2 - 20
		screen.blit(wave_big, (wx, wy))

	if snap_game_over:
		osurf = pygame.Surface((gw, gh), pygame.SRCALPHA)
		osurf.fill((0, 0, 0, 160))
		screen.blit(osurf, (gx, gy))
		go_surf = _si_font_large.render("GAME  OVER", True, (255, 80, 80))
		screen.blit(go_surf, (gx + gw // 2 - go_surf.get_width() // 2, gy + gh // 2 - 50))
		sc_surf = _si_font_medium.render(f"FINAL SCORE  {snap_score}", True, (220, 180, 80))
		screen.blit(sc_surf, (gx + gw // 2 - sc_surf.get_width() // 2, gy + gh // 2))
		rs_surf = _si_font_small.render("PRESS  F3  TO  RESTART   ·   F8  TO  CLOSE", True, (140, 140, 160))
		screen.blit(rs_surf, (gx + gw // 2 - rs_surf.get_width() // 2, gy + gh // 2 + 38))

	if snap_won:
		osurf = pygame.Surface((gw, gh), pygame.SRCALPHA)
		osurf.fill((0, 0, 0, 140))
		screen.blit(osurf, (gx, gy))
		w_surf = _si_font_large.render("WAVE  CLEARED!", True, (80, 255, 160))
		screen.blit(w_surf, (gx + gw // 2 - w_surf.get_width() // 2, gy + gh // 2 - 50))
		sc_surf = _si_font_medium.render(f"SCORE  {snap_score}", True, (220, 220, 80))
		screen.blit(sc_surf, (gx + gw // 2 - sc_surf.get_width() // 2, gy + gh // 2))
		rs_surf = _si_font_small.render("PRESS  F2  FOR  NEXT  WAVE   ·   F3  TO  RESTART   ·   F8  TO  CLOSE", True, (140, 140, 160))
		screen.blit(rs_surf, (gx + gw // 2 - rs_surf.get_width() // 2, gy + gh // 2 + 38))

	title_surf = _si_font_small.render("SPACE  ATTACK  —  EASTER EGG  —  F8  TO  RETURN", True, (40, 60, 90))
	screen.blit(title_surf, (screen_x // 2 - title_surf.get_width() // 2, 18))

	pygame.draw.rect(screen, (0, 60, 140), (0, 0, screen_x, screen_y), 2)
	pygame.display.flip()

def handle_quit():
	global screen_x, screen_y, screen, _current_theme, mini_game_active
	for ev in pygame.event.get():
		if ev.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if ev.type == pygame.VIDEORESIZE:
			screen_x, screen_y = ev.w, ev.h
			screen = pygame.display.set_mode((screen_x, screen_y), pygame.RESIZABLE)
		if ev.type == pygame.KEYDOWN:
			if ev.key == pygame.K_F9:
				_current_theme = (_current_theme + 1) % THEME_COUNT
				_save_theme(_current_theme)
			if ev.key == pygame.K_F8:
				if not mini_game_active:
					mini_game_active = True
					init_space_invaders()
				else:
					mini_game_active = False
			if mini_game_active:
				if ev.key == pygame.K_F3:
					with _si_lock:
						hi = _si.get("hi_score", 0)
					init_space_invaders()
					with _si_lock:
						_si["hi_score"] = hi
				if ev.key == pygame.K_F2:
					with _si_lock:
						won = _si["won"]
					if won:
						hi_before    = _si.get("hi_score", 0)
						score_before = _si["score"]
						_si_next_wave()
						with _si_lock:
							_si["won"]      = False
							_si["hi_score"] = max(hi_before, score_before)

def _draw_zip_panel(status_line, file_line, pct, phase_label):
	if mini_game_active:
		update_space_invaders()
		draw_space_invaders()
		return
	draw_verify_bg()
	_pad = 40
	_mid = screen_x // 2
	_bw  = screen_x - (_pad * 2)
	_y   = 16
	_gap = 8
	pygame.draw.rect(screen, _theme_panel_bg(), (_pad, _y, _bw, 44))
	pygame.draw.rect(screen, _theme_panel_border(), (_pad, _y, _bw, 44), 1)
	_ts = font.render("ELUCIDATE RPG  —  PACKAGE INSTALLATION SYSTEM", True, _theme_text_main())
	screen.blit(_ts, (_mid - _ts.get_width() // 2, _y + 13))
	_y += 44 + _gap
	pygame.draw.rect(screen, _theme_sub_bg(), (_pad, _y, _bw, 32))
	pygame.draw.rect(screen, _theme_sub_border(), (_pad, _y, _bw, 32), 1)
	draw_text_ui(phase_label, _pad + 14, _y + 8, _theme_text_dim())
	_y += 32 + _gap
	_ob_top = _y
	pygame.draw.rect(screen, _theme_sub_bg(), (_pad, _ob_top, _bw, 90))
	pygame.draw.rect(screen, _theme_sub_border(), (_pad, _ob_top, _bw, 90), 1)
	_y = _ob_top + 8
	draw_text_ui("EXTRACTION PROGRESS", _pad + 14, _y, _theme_text_label())
	_y += 20
	pygame.draw.rect(screen, _theme_bar_empty_bg(), (_pad + 10, _y, _bw - 20, 22))
	pygame.draw.rect(screen, _theme_sub_border(), (_pad + 10, _y, _bw - 20, 22), 1)
	_ofw = int(min(pct, 100) / 100 * (_bw - 20))
	if _ofw > 0:
		pygame.draw.rect(screen, _theme_bar_fill(), (_pad + 10, _y, _ofw, 22))
		pygame.draw.rect(screen, _theme_bar_shine(), (_pad + 10, _y, _ofw, 4))
	_y += 22 + 6
	draw_text_ui(f"EXTRACTED  {int(pct)}%", _pad + 14, _y, _theme_text_main())
	_y = _ob_top + 90 + _gap
	_cf_top = _y
	pygame.draw.rect(screen, _theme_sub_bg(), (_pad, _cf_top, _bw, 56))
	pygame.draw.rect(screen, _theme_sub_border(), (_pad, _cf_top, _bw, 56), 1)
	_y = _cf_top + 8
	draw_text_ui("CURRENT ENTRY", _pad + 14, _y, _theme_text_label())
	_y += 20
	draw_text_ui("FILE   ›   " + (file_line[:90] if file_line else "—"), _pad + 14, _y, _theme_text_main())
	_y = _cf_top + 56 + _gap
	pygame.draw.rect(screen, _theme_sub_bg(), (_pad, _y, _bw, 40))
	pygame.draw.rect(screen, _theme_sub_border(), (_pad, _y, _bw, 40), 1)
	draw_text_ui("STATUS   " + status_line, _pad + 14, _y + 11, _theme_text_dim())
	pygame.draw.rect(screen, _theme_outer_border(), (0, 0, screen_x, screen_y), 1)
	pygame.display.flip()

def zip_download(url):
	handle_quit()
	temp_zip = "temp_download.zip"
	temp_extract = "temp_extract"
	_draw_zip_panel(status_line="  SCANNING PACKAGE INTEGRITY...", file_line="", pct=0, phase_label="PHASE   1  /  3   —   PRE-FLIGHT VALIDATION")
	try:
		if os.path.exists(temp_zip):
			os.remove(temp_zip)
		if os.path.exists(temp_extract):
			shutil.rmtree(temp_extract)
		_draw_zip_panel(status_line="  CONNECTED TO PACKAGE SERVER — DOWNLOADING REQUIRED FILES", file_line="package bundle", pct=0, phase_label="PHASE   2  /  3   —   DOWNLOADING COMPRESSED PACKAGE")
		gdown.download(url, temp_zip, quiet=False)
		if not os.path.exists(temp_zip) or os.path.getsize(temp_zip) < 10000:
			_draw_zip_panel(status_line="  PACKAGE INVALID OR CORRUPTED — ABORTING", file_line="", pct=0, phase_label="PHASE   —   VALIDATION FAILED")
			pygame.time.delay(2000)
			return False
		_draw_zip_panel(status_line="  CONNECTED TO PACKAGE — USING DEFLATE COMPRESSION TO EXTRACT ", file_line="reading archive...", pct=0, phase_label="PHASE   3  /  3   —   PACKAGE EXTRACTION")
		with zipfile.ZipFile(temp_zip, 'r') as zip_ref:
			all_files = zip_ref.namelist()
			total_files = len(all_files)
			for idx, member in enumerate(all_files):
				zip_ref.extract(member, temp_extract)
				handle_quit()
				pct = ((idx + 1) / total_files * 100) if total_files > 0 else 100
				_draw_zip_panel(status_line="  CONNECTED TO PACKAGE — EXTRACTING REQUIRED FILES", file_line=member, pct=pct, phase_label="PHASE   3  /  3   —   PACKAGE EXTRACTION")
		patch_items = os.listdir(temp_extract)
		total_patch = len(patch_items)
		for pidx, item in enumerate(patch_items):
			src = os.path.join(temp_extract, item)
			dst = os.path.join(".", item)
			handle_quit()
			if os.path.exists(dst):
				if os.path.isdir(dst):
					shutil.rmtree(dst)
				else:
					os.remove(dst)
			if os.path.isdir(src):
				shutil.move(src, dst)
			else:
				shutil.move(src, dst)
			pct = ((pidx + 1) / total_patch * 100) if total_patch > 0 else 100
			_draw_zip_panel(status_line="  APPLYING PATCH FILES TO INSTALLATION DIRECTORY", file_line=item, pct=pct, phase_label="PHASE   3  /  3   —   WRITING PATCH FILES")
		os.remove(temp_zip)
		shutil.rmtree(temp_extract)
		_draw_zip_panel(status_line="  PACKAGE INSTALLATION COMPLETE", file_line="all files installed successfully", pct=100, phase_label="PHASE   —   INSTALLATION COMPLETE")
		pygame.time.delay(1800)
		return True
	except Exception as e:
		_draw_zip_panel(status_line="  DOWNLOAD FAILED", file_line=str(e)[:90], pct=0, phase_label="PHASE   —   ERROR")
		pygame.time.delay(2500)
		return False

def verify(filename, url):
	global _g_current_folder, _g_current_file, _g_current_status
	global _g_total_bytes, _g_received_bytes, _g_last_pct
	headers = {
		"User-Agent": "Mozilla/5.0",
		"Accept": "image/png,image/*;q=0.8,*/*;q=0.5",
		"Connection": "keep-alive"
	}
	_g_current_folder = os.path.dirname(filename)
	_g_current_file   = os.path.basename(filename)
	dirname = os.path.dirname(filename)
	if dirname != "":
		os.makedirs(dirname, exist_ok=True)
	if os.path.exists(filename):
		_g_current_status = f"   FILE FOUND"
		_g_total_bytes    = 0
		_g_received_bytes = 0
		_g_last_pct       = 100
		handle_quit()
		_draw_global_panel()
	else:
		_g_current_status = f"   FILE NOT FOUND"
		_g_total_bytes    = 0
		_g_received_bytes = 0
		_g_last_pct       = 0
		handle_quit()
		_draw_global_panel()
		tries = 0
		for attempt in range(30):
			handle_quit()
			try:
				with requests.get(url, headers=headers, stream=True, timeout=10) as r:
					r.raise_for_status()
					_g_total_bytes    = int(r.headers.get("Content-Length", 0))
					_g_received_bytes = 0
					_g_current_status = f"   DOWNLOADING"
					with open(filename, "wb") as f:
						for chunk in r.iter_content(1024):
							if chunk:
								f.write(chunk)
								_g_received_bytes += len(chunk)
								if _g_total_bytes > 0:
									_g_last_pct = int((_g_received_bytes / _g_total_bytes) * 100)
								handle_quit()
								_draw_global_panel()
				_g_current_status = f"   FILE DOWNLOADED"
				_g_last_pct = 100
				_draw_global_panel()
				break
			except Exception:
				tries += 1
				_g_current_status = f"   ERROR: CHECK YOUR INTERNET CONNECTION"
				_draw_global_panel()
				pygame.time.delay(100)
		else:
			_g_current_status = f"   DOWNLOAD FAILED"
			_draw_global_panel()

_g_total_assets   = 0
_g_done_assets    = 0
_g_total_bytes    = 0
_g_received_bytes = 0
_g_current_folder = ""
_g_current_file   = ""
_g_current_status = "INITIALIZING..."
_g_last_pct       = 0
_g_start_time     = time.time()

def _draw_global_panel():
	if mini_game_active:
		update_space_invaders()
		draw_space_invaders()
		return
	draw_verify_bg()
	_pad = 40
	_mid = screen_x // 2
	_bw  = screen_x - (_pad * 2)
	_y   = 16
	_gap = 8
	pygame.draw.rect(screen, _theme_panel_bg(), (_pad, _y, _bw, 44))
	pygame.draw.rect(screen, _theme_panel_border(), (_pad, _y, _bw, 44), 1)
	_ts = font.render("ELUCIDATE RPG  —  ASSET VERIFICATION & DOWNLOAD", True, _theme_text_main())
	screen.blit(_ts, (_mid - _ts.get_width() // 2, _y + 13))
	_y += 44 + _gap
	pygame.draw.rect(screen, _theme_sub_bg(), (_pad, _y, _bw, 32))
	pygame.draw.rect(screen, _theme_sub_border(), (_pad, _y, _bw, 32), 1)
	draw_text_ui(f"ASSET   {_g_done_assets}  /  {_g_total_assets}", _pad + 14, _y + 8, _theme_text_dim())
	_y += 32 + _gap
	_ob_top = _y
	pygame.draw.rect(screen, _theme_sub_bg(), (_pad, _ob_top, _bw, 90))
	pygame.draw.rect(screen, _theme_sub_border(), (_pad, _ob_top, _bw, 90), 1)
	_y = _ob_top + 8
	draw_text_ui("OVERALL PROGRESS", _pad + 14, _y, _theme_text_label())
	_y += 20
	pygame.draw.rect(screen, _theme_bar_empty_bg(), (_pad + 10, _y, _bw - 20, 22))
	pygame.draw.rect(screen, _theme_sub_border(), (_pad + 10, _y, _bw - 20, 22), 1)
	if _g_total_assets > 0:
		_op  = int((_g_done_assets / _g_total_assets) * 100)
		_ofw = int((_g_done_assets / _g_total_assets) * (_bw - 20))
	else:
		_op = 0; _ofw = 0
	if _ofw > 0:
		pygame.draw.rect(screen, _theme_bar_fill(), (_pad + 10, _y, _ofw, 22))
		pygame.draw.rect(screen, _theme_bar_shine(), (_pad + 10, _y, _ofw, 4))
	_y += 22 + 6
	draw_text_ui(f"OVERALL  {_op}%", _pad + 14, _y, _theme_text_main())
	_y = _ob_top + 90 + _gap
	_cf_top = _y
	pygame.draw.rect(screen, _theme_sub_bg(), (_pad, _cf_top, _bw, 80))
	pygame.draw.rect(screen, _theme_sub_border(), (_pad, _cf_top, _bw, 80), 1)
	_y = _cf_top + 8
	draw_text_ui("CURRENT FILE", _pad + 14, _y, _theme_text_label())
	_y += 20
	draw_text_ui("FOLDER   ›   " + (_g_current_folder if _g_current_folder else "root"), _pad + 14, _y, _theme_text_dim())
	_y += 22
	draw_text_ui("FILE     ›   " + _g_current_file, _pad + 14, _y, _theme_text_main())
	_y = _cf_top + 80 + _gap
	_fb_top = _y
	pygame.draw.rect(screen, _theme_sub_bg(), (_pad, _fb_top, _bw, 90))
	pygame.draw.rect(screen, _theme_sub_border(), (_pad, _fb_top, _bw, 90), 1)
	_y = _fb_top + 8
	draw_text_ui("FILE PROGRESS", _pad + 14, _y, _theme_text_label())
	_y += 20
	pygame.draw.rect(screen, _theme_bar_empty_bg(), (_pad + 10, _y, _bw - 20, 22))
	pygame.draw.rect(screen, _theme_sub_border(), (_pad + 10, _y, _bw - 20, 22), 1)
	if _g_total_bytes > 0:
		_fp  = int((_g_received_bytes / _g_total_bytes) * 100)
		_ffw = int((_g_received_bytes / _g_total_bytes) * (_bw - 20))
		_size_str = f"{_g_received_bytes // 1024} KB  /  {_g_total_bytes // 1024} KB"
	else:
		_fp = _g_last_pct; _ffw = 0
		_size_str = f"{_g_received_bytes // 1024} KB  /  unknown"
	if _ffw > 0:
		pygame.draw.rect(screen, _theme_bar_fill(), (_pad + 10, _y, _ffw, 22))
		pygame.draw.rect(screen, _theme_bar_shine(), (_pad + 10, _y, _ffw, 3))
	_y += 22 + 6
	draw_text_ui(f"FILE  {_fp}%", _pad + 14, _y, _theme_text_main())
	_y = _fb_top + 90 + _gap
	pygame.draw.rect(screen, _theme_sub_bg(), (_pad, _y, _bw, 56))
	pygame.draw.rect(screen, _theme_sub_border(), (_pad, _y, _bw, 56), 1)
	draw_text_ui("RECEIVED   " + _size_str,         _pad + 14, _y + 10, _theme_text_dim())
	draw_text_ui("STATUS     " + _g_current_status, _pad + 14, _y + 32, _theme_text_main())
	_y += 56 + _gap
	_elapsed     = int(time.time() - _g_start_time)
	_hours       = _elapsed // 3600
	_minutes     = (_elapsed % 3600) // 60
	_seconds     = _elapsed % 60
	if _hours > 0:
		_time_str = f"{_hours}h  {_minutes:02d}m  {_seconds:02d}s"
	elif _minutes > 0:
		_time_str = f"{_minutes}m  {_seconds:02d}s"
	else:
		_time_str = f"{_seconds}s"
	pygame.draw.rect(screen, _theme_sub_bg(), (_pad, _y, _bw, 34))
	pygame.draw.rect(screen, _theme_sub_border(), (_pad, _y, _bw, 34), 1)
	draw_text_ui("TIME TAKEN   " + _time_str, _pad + 14, _y + 8, _theme_text_dim())
	pygame.draw.rect(screen, _theme_outer_border(), (0, 0, screen_x, screen_y), 1)
	pygame.display.flip()

draw_text("Loading...", 5, 5)
pygame.draw.rect(screen, _theme_outer_border(), (0, 0, screen_x, screen_y), 1)
pygame.display.flip()
_g_total_assets = sum(1 for line in open(__file__, encoding="utf-8") if line.strip().startswith('verify('))
_g_done_assets  = 0

# verify here :)
#
#example:
#	# --- items / accessories
#	verify("items/accessories/arm_guard.png",     "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/armour_armwear_arm_guard.png"); _g_done_assets += 1
#	verify("items/accessories/blue_amulet.png",   "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/armour_accessories_blue_amulet.png"); _g_done_assets += 1
#	verify("items/accessories/red_amulet.png",    "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/armour_accessories_red_amulet.png"); _g_done_assets += 1
#	verify("items/accessories/red_scarf.png",     "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/armour_accessories_red_scarf.png"); _g_done_assets += 1
#	verify("items/accessories/ring.png",          "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/armour_accessories_ring.png"); _g_done_assets += 1
#	verify("items/accessories/swift_boots.png",   "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/armour_accessories_swift_boots.png"); _g_done_assets += 1
#
# add before the for loop of verify