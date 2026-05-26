import importlib
import subprocess
import sys
import json
import datetime

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
import webbrowser
import math
import threading

_VERIFY_HEADERS = {
	"User-Agent": "Mozilla/5.0",
	"Accept": "image/png,image/*;q=0.8,*/*;q=0.5",
	"Connection": "keep-alive",
}

filename = "wiki_images/ELUCIDATE-WEBSITE-EYE-LOGO.png"
url = "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/ELUCIDATE-WEBSITE-EYE-LOGO.png"

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
	_g_current_status = "   FILE FOUND"
	_g_total_bytes    = 0
	_g_received_bytes = 0
	_g_last_pct       = 100
else:
	_g_current_status = "   FILE NOT FOUND"
	_g_total_bytes    = 0
	_g_received_bytes = 0
	_g_last_pct       = 0
	tries = 0
	for attempt in range(30):
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
			_g_current_status = f"   FILE DOWNLOADED"
			_g_last_pct = 100
			break
		except Exception:
			_g_current_status = "   ERROR: CHECK YOUR INTERNET CONNECTION"
			time.sleep(0.05)
	else:
		_g_current_status = f"   DOWNLOAD FAILED"

pygame.init()
screen_x, screen_y = 1275, 710
screen = pygame.display.set_mode((screen_x, screen_y), pygame.RESIZABLE)
try:
	_game_icon = pygame.image.load("wiki_images/ELUCIDATE-WEBSITE-EYE-LOGO.png").convert_alpha()
	pygame.display.set_icon(_game_icon)
except Exception:
	_game_icon = None
pygame.display.set_caption("Elucidate RPG  —  Launcher")

_fps_samples   = []
_fps_last_draw = time.time()

def _update_fps():
	global _fps_samples, _fps_last_draw
	now = time.time()
	dt  = now - _fps_last_draw
	_fps_last_draw = now
	if dt > 0:
		_fps_samples.append(1.0 / dt)
	if len(_fps_samples) > 30:
		_fps_samples.pop(0)

def _avg_fps():
	return sum(_fps_samples) / len(_fps_samples) if _fps_samples else 0.0
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

ACTIVITY_LOG_FILE = "launcher_activity.json"
_MAX_LOG_ENTRIES  = 20

def _load_activity_log():
	try:
		with open(ACTIVITY_LOG_FILE, "r", encoding="utf-8") as f:
			data = json.load(f)
			return data if isinstance(data, list) else []
	except Exception:
		return []

def _append_activity(entry: str):
	log = _load_activity_log()
	log.insert(0, {"time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), "entry": entry})
	del log[_MAX_LOG_ENTRIES:]
	try:
		with open(ACTIVITY_LOG_FILE, "w", encoding="utf-8") as f:
			json.dump(log, f, indent=2)
	except Exception:
		pass

_activity_log = _load_activity_log()
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
	_neon_cols = [
		(0, 255, 200),
		(255, 0, 180),
		(0, 150, 255),
		(200, 0, 255),
		(0, 255, 100),
		(255, 80, 0),
	]
	if not hasattr(_draw_neon_bg, "_surf") or _draw_neon_bg._surf.get_size() != (screen_x, screen_y):
		_draw_neon_bg._surf = pygame.Surface((screen_x, screen_y), pygame.SRCALPHA)
	_neon_line_surf = _draw_neon_bg._surf
	_neon_line_surf.fill((0, 0, 0, 0))
	for i in range(6):
		t   = _neon_time + i * 1.05
		x1  = int(screen_x * (0.5 + 0.5 * math.sin(t * 0.31 + i)))
		y1  = int(screen_y * (0.5 + 0.5 * math.cos(t * 0.27 + i * 0.7)))
		x2  = int(screen_x * (0.5 + 0.5 * math.cos(t * 0.19 + i * 1.3)))
		y2  = int(screen_y * (0.5 + 0.5 * math.sin(t * 0.23 + i * 0.4)))
		c = _neon_cols[i % len(_neon_cols)]
		pygame.draw.line(_neon_line_surf, (*c, 18), (x1, y1), (x2, y2), 2)
	screen.blit(_neon_line_surf, (0, 0))
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
		if keys[pygame.K_UP] and _si["shoot_cooldown"] <= 0:
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
		r     = max(1, int(ex["r"]))
		alpha = ex["alpha"]
		ecol  = ex["color"]

		esurf = pygame.Surface((r * 2 + 2, r * 2 + 2), pygame.SRCALPHA)
		pygame.draw.circle(esurf, (*ecol, alpha),              (r + 1, r + 1), r)
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

	hint_surf = _si_font_small.render("[F8 / CLOSE]   [ARROWS/AD / MOVE]   [UP / SHOOT]", True, (60, 80, 110))
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
		rs_surf = _si_font_small.render("PRESS  M  TO  RESTART   ·   F8  TO  CLOSE", True, (140, 140, 160))
		screen.blit(rs_surf, (gx + gw // 2 - rs_surf.get_width() // 2, gy + gh // 2 + 38))

	if snap_won:
		osurf = pygame.Surface((gw, gh), pygame.SRCALPHA)
		osurf.fill((0, 0, 0, 140))
		screen.blit(osurf, (gx, gy))
		w_surf = _si_font_large.render("WAVE  CLEARED!", True, (80, 255, 160))
		screen.blit(w_surf, (gx + gw // 2 - w_surf.get_width() // 2, gy + gh // 2 - 50))
		sc_surf = _si_font_medium.render(f"SCORE  {snap_score}", True, (220, 220, 80))
		screen.blit(sc_surf, (gx + gw // 2 - sc_surf.get_width() // 2, gy + gh // 2))
		rs_surf = _si_font_small.render("PRESS  DOWN  FOR  NEXT  WAVE   ·   M  TO  RESTART   ·   F8  TO  CLOSE", True, (140, 140, 160))
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
			if _game_icon is not None:
				pygame.display.set_icon(_game_icon)
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
				if ev.key == pygame.K_m:
					with _si_lock:
						hi = _si.get("hi_score", 0)
					init_space_invaders()
					with _si_lock:
						_si["hi_score"] = hi
				if ev.key == pygame.K_DOWN:
					with _si_lock:
						won = _si["won"]
					if won:
						hi_before = _si.get("hi_score", 0)
						score_before = _si["score"]
						_si_next_wave()
						with _si_lock:
							_si["won"] = False
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
			_inv_t0 = time.time()
			while time.time() - _inv_t0 < 2.5:
				handle_quit()
				pygame.display.flip()
				py_clock.tick(60)
				if any(e.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN) for e in pygame.event.get()):
					break
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
			shutil.move(src, dst)
			pct = ((pidx + 1) / total_patch * 100) if total_patch > 0 else 100
			_draw_zip_panel(status_line="  APPLYING PATCH FILES TO INSTALLATION DIRECTORY", file_line=item, pct=pct, phase_label="PHASE   3  /  3   —   WRITING PATCH FILES")
		os.remove(temp_zip)
		shutil.rmtree(temp_extract)
		_draw_zip_panel(status_line="  PACKAGE INSTALLATION COMPLETE", file_line="all files installed successfully",
						pct=100, phase_label="PHASE   —   INSTALLATION COMPLETE")
		# Show a brief "done" screen then return — user can close or wait.
		_done_font = pygame.font.SysFont("Times New Roman", 22)
		_t0 = time.time()
		while time.time() - _t0 < 2.0:
			handle_quit()
			_draw_zip_panel(status_line="  PACKAGE INSTALLATION COMPLETE", file_line="all files installed successfully",
							pct=100, phase_label="PHASE   —   INSTALLATION COMPLETE")
			_done_msg = _done_font.render("Installation complete!  Press any key to continue.", True, (100, 255, 120))
			screen.blit(_done_msg, (_done_msg.get_rect(center=(screen_x // 2, screen_y - 60)).topleft))
			pygame.display.flip()
			py_clock.tick(60)
			_k = pygame.event.get()
			if any(e.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN) for e in _k):
				break
		return True
	except Exception as e:
		_draw_zip_panel(status_line="  DOWNLOAD FAILED", file_line=str(e)[:90], pct=0, phase_label="PHASE   —   ERROR")
		_err_t0 = time.time()
		while time.time() - _err_t0 < 3.0:
			handle_quit()
			pygame.display.flip()
			py_clock.tick(60)
			_ek = pygame.event.get()
			if any(ev.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN) for ev in _ek):
				break
		try:
			if os.path.exists(temp_zip):
				os.remove(temp_zip)
			if os.path.exists(temp_extract):
				shutil.rmtree(temp_extract)
		except Exception:
			pass
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
		_g_current_status = "   FILE FOUND"
		_g_total_bytes    = 0
		_g_received_bytes = 0
		_g_last_pct       = 100
		handle_quit()
		_draw_global_panel()
	else:
		_g_current_status = "   FILE NOT FOUND"
		_g_total_bytes    = 0
		_g_received_bytes = 0
		_g_last_pct       = 0
		handle_quit()
		_draw_global_panel()
		tries = 0
		for attempt in range(30):
			handle_quit()
			try:
				with requests.get(url, headers=_VERIFY_HEADERS, stream=True, timeout=15) as r:
					r.raise_for_status()
					_g_total_bytes    = int(r.headers.get("Content-Length", 0))
					_g_received_bytes = 0
					_g_current_status = "   DOWNLOADING"
					with open(filename, "wb") as f:
						for chunk in r.iter_content(8192):
							if chunk:
								f.write(chunk)
								_g_received_bytes += len(chunk)
								if _g_total_bytes > 0:
									_g_last_pct = int((_g_received_bytes / _g_total_bytes) * 100)
								handle_quit()
								_draw_global_panel()
				_g_current_status = "   FILE DOWNLOADED"
				_g_last_pct = 100
				_draw_global_panel()
				break
			except Exception:
				tries += 1
				_g_current_status = "   ERROR: CHECK YOUR INTERNET CONNECTION"
				_draw_global_panel()
				handle_quit()
				pygame.time.delay(80)
		else:
			_g_current_status = "   DOWNLOAD FAILED"
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
try:
	with open(__file__, encoding="utf-8") as _selffile:
		_g_total_assets = sum(1 for line in _selffile if line.strip().startswith('verify('))
except Exception:
	_g_total_assets = 1
_g_done_assets  = 0

for i in range(1):
	verify("items/materials_special_small_caligo_fragment_tribe.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_special_small_caligo_fragment_tribe.png"); _g_done_assets += 1
	verify("items/materials_special_small_caligo_fragment_port.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_special_small_caligo_fragment_port.png"); _g_done_assets += 1
	verify("items/materials_special_big_caligo_fragment.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_special_big_caligo_fragmrnt.png"); _g_done_assets += 1
	verify("items/weapon_1handed_short_sword.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/weapon_1handed_short_sword.png"); _g_done_assets += 1
	verify("items/weapon_1handed_cleaver.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/weapon_1handed_cleaver.png"); _g_done_assets += 1
	verify("items/weapon_1handed_knife.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/weapon_1handed_knife.png"); _g_done_assets += 1
	verify("items/materials_sheet_ancient_paper.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_sheet_ancient_paper.png"); _g_done_assets += 1
	verify("items/armour_headware_iron_mask.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/armour_headware_iron_mask.png"); _g_done_assets += 1
	verify("items/armour_body_armour_dark_priests_robe.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/armour_body_armour_dark_priests_robe.png"); _g_done_assets += 1
	verify("items/armour_body_armour_priests_robe.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/armour_body_armour_priests_robe.png"); _g_done_assets += 1
	verify("items/armour_headware_plate_helmet.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/armour_headware_plate_helmet.png"); _g_done_assets += 1
	verify("items/armour_headware_padded_cap.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/armour_headware_padded_cap.png"); _g_done_assets += 1
	verify("items/armour_body_armour_iron_cuirass.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/armour_body_armour_iron_cuirass.png"); _g_done_assets += 1
	verify("items/armour_body_armour_loincloth.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/armour_body_armour_loincloth.png"); _g_done_assets += 1
	verify("items/armour_accessories_red_scarf.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/armour_accessories_red_scarf.png"); _g_done_assets += 1
	verify("items/armour_headware_iron_helmet.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/armour_headware_iron_helmet.png"); _g_done_assets += 1
	verify("items/armour_headware_guard_bascinet.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/armour_headware_guard_bascinet.png"); _g_done_assets += 1
	verify("items/armour_headware_guard_coif.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/armour_headware_guard_coif.png"); _g_done_assets += 1
	verify("items/armour_headware_chainmail_hood.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/armour_headware_chainmail_hood.png"); _g_done_assets += 1
	verify("items/armour_body_armour_black_dress.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/armour_body_armour_black_dress.png"); _g_done_assets += 1
	verify("items/armour_body_armour_trench_coat.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/armour_body_armour_trench_coat.png"); _g_done_assets += 1
	verify("items/weapon_1handed_corsairs_saber.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/weapon_1handed_corsairs_saber.png"); _g_done_assets += 1
	verify("items/weapon_1handed_cloth_hood.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/weapon_1handed_cloth_hood.png"); _g_done_assets += 1
	verify("items/armour_body_armour_leather_coat.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/armour_body_armour_leather_coat.png"); _g_done_assets += 1
	verify("items/armour_body_armour_leather_vest.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/armour_body_armour_leather_jvest.png"); _g_done_assets += 1
	verify("items/armour_body_armour_plated_mail.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/armour_body_armour_plated_mail.png"); _g_done_assets += 1
	verify("items/armour_shield_scutum.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/armour_shield_scutum.png"); _g_done_assets += 1
	verify("items/weapon_longrange_musket.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/weapon_longrange_musket.png"); _g_done_assets += 1
	verify("items/weapon_2handed_spear.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/weapon_2handed_spear.png"); _g_done_assets += 1
	verify("items/armour_body_armour_hard_leather_armor.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/armour_body_armour_hard_leather_armor.png"); _g_done_assets += 1
	verify("items/armour_body_armour_iron_plate.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/armour_body_armour_iron_plate.png"); _g_done_assets += 1
	verify("items/weapon_1handed_stiletto.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/weapon_1handed_stiletto.png"); _g_done_assets += 1
	verify("items/armour_armwear_arm_guard.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/armour_armwear_arm_guard.png"); _g_done_assets += 1
	verify("items/weapon_1handed_iron_axe.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/weapon_1handed_iron_axe.png"); _g_done_assets += 1
	verify("items/weapon_longrange_short_bow.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/weapon_longrange_short_bow.png"); _g_done_assets += 1
	verify("items/materials_scrap_leather_scraps.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_scrap_leather_scraps.png"); _g_done_assets += 1
	verify("items/materials_skill_book_of_rapid_fire.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_skill_book_of_rapid_fire.png"); _g_done_assets += 1
	verify("items/materials_skill_book_of_instincts.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_skill_book_of_instincts.png"); _g_done_assets += 1
	verify("items/armour_accessories_swift_boots.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/armour_accessories_swift_boots.png"); _g_done_assets += 1
	verify("items/weapon_longrange_heavy_crossbow.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/weapon_longrange_heavy_crossbow.png"); _g_done_assets += 1
	verify("items/weapon_longrange_longbow.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/weapon_longrange_longbow.png"); _g_done_assets += 1
	verify("items/weapon_2handed_maul.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/weapon_2handed_maul.png"); _g_done_assets += 1
	verify("items/weapon_2handed_claymore.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/weapon_2handed_claymore.png"); _g_done_assets += 1
	verify("items/weapon_1handed_scimitar.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/weapon_1handed_scimitar.png"); _g_done_assets += 1
	verify("items/weapon_1handed_improvised_shiv.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/weapon_1handed_improvised_shiv.png"); _g_done_assets += 1
	verify("items/weapon_1handed_steel_hammer.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/weapon_1handed_steel_hammer.png"); _g_done_assets += 1
	verify("items/material_toy_black_dressed_doll.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/material_toy_black_dressed_doll.png"); _g_done_assets += 1
	verify("items/weapon_1handed_dirk.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/weapon_1handed_dirk.png"); _g_done_assets += 1
	verify("items/materials_plank_wooden_plank.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_plank_wooden_plank.png"); _g_done_assets += 1
	verify("items/weapon_1handed_dagger.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/weapon_1handed_dagger.png"); _g_done_assets += 1
	verify("items/materials_component_silver_wire.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_component_silver_wire.png"); _g_done_assets += 1
	verify("items/armour_accessories_red_amulet.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/armour_accessories_red_amulet.png"); _g_done_assets += 1
	verify("items/armour_accessories_blue_amulet.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/armour_accessories_blue_amulet.png"); _g_done_assets += 1
	verify("items/materials_component_stick.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_component_stick.png"); _g_done_assets += 1
	verify("items/armour_accessories_ring.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/armour_accessories_ring.png"); _g_done_assets += 1
	verify("items/materials_skill_book_of_marksmanship.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_skill_book_of_marksmanship.png"); _g_done_assets += 1
	verify("items/materials_skill_book_of_stars.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_skill_book_of_stars.png"); _g_done_assets += 1
	verify("items/materials_skill_book_of_crafsmanship.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_skill_book_of_crafsmanship.png"); _g_done_assets += 1
	verify("items/materials_skill_book_of_agility.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_skill_book_of_agility.png"); _g_done_assets += 1
	verify("items/materials_skill_book_of_healing.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_skill_book_of_healing.png"); _g_done_assets += 1
	verify("items/materials_skill_book_of_the_secrets.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_skill_book_of_the_secrets.png"); _g_done_assets += 1
	verify("items/materials_save_book_of_enlightenment.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_save_book_of_enlightenment.png"); _g_done_assets += 1
	verify("items/materials_skill_book_of_cowardice_i.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_skill_book_of_cowardice_i.png"); _g_done_assets += 1
	verify("items/materials_skill_book_of_cowardice_ii.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_skill_book_of_cowardice_ii.png"); _g_done_assets += 1
	verify("items/materials_skill_book_of_pestilence_i.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_skill_book_of_pestilence_i.png"); _g_done_assets += 1
	verify("items/materials_skill_book_of_pestilence_ii.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_skill_book_of_pestilence_ii.png"); _g_done_assets += 1
	verify("items/materials_skill_book_of_pestilence_iii.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_skill_book_of_pestilence_iii.png"); _g_done_assets += 1
	verify("items/materials_skill_book_of_pestilence_iv.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_skill_book_of_pestilence_iv.png"); _g_done_assets += 1
	verify("items/materials_skill_book_of_pestilence_v.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_skill_book_of_pestilence_v.png"); _g_done_assets += 1
	verify("items/materials_skill_book_of_pestilence_vi.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_skill_book_of_pestilence_vi.png"); _g_done_assets += 1
	verify("items/materials_skill_book_of_pestilence_vii.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_skill_book_of_pestilence_vii.png"); _g_done_assets += 1
	verify("items/materials_skill_book_of_pestilence_viii.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_skill_book_of_pestilence_viii.png"); _g_done_assets += 1
	verify("items/materials_skill_book_of_trade_i.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_skill_book_of_trade_i.png"); _g_done_assets += 1
	verify("items/materials_skill_book_of_trade_ii.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_skill_book_of_trade_ii.png"); _g_done_assets += 1
	verify("items/materials_skill_book_of_trade_iii.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_skill_book_of_trade_iii.png"); _g_done_assets += 1
	verify("items/materials_gem_red_gem.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_gem_red_gem.png"); _g_done_assets += 1
	verify("items/materials_gem_blue_gem.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_gem_blue_gem.png"); _g_done_assets += 1
	verify("items/materials_beverage_ale.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_beverage_ale.png"); _g_done_assets += 1
	verify("items/materials_beverage_wine.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_beverage_wine.png"); _g_done_assets += 1
	verify("items/materials_beverage_rum.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_beverage_rum.png"); _g_done_assets += 1
	verify("items/materials_bar_iron_ingot.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_bar_iron_ingot.png"); _g_done_assets += 1
	verify("items/materials_ore_raw_iron.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_ore_raw_iron.png"); _g_done_assets += 1
	verify("items/materials_foliage_blue_herb-1.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_foliage_blue_herb-1.png"); _g_done_assets += 1
	verify("items/materials_foliage_green_herb.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_foliage_green_herb.png"); _g_done_assets += 1
	verify("items/materials_sheet_paper.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_sheet_paper.png"); _g_done_assets += 1
	verify("items/materials_potion_antibiotics.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_potion_antibiotics.png"); _g_done_assets += 1
	verify("items/materials_potion_betadine.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_potion_betadine.png"); _g_done_assets += 1
	verify("items/materials_potion_red_vial.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_potion_red_vial.png"); _g_done_assets += 1
	verify("items/materials_container_empty_vial.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_container_empty_vial.png"); _g_done_assets += 1
	verify("items/weapon_2handed_longsword.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/weapon_2handed_longsword.png"); _g_done_assets += 1
	verify("items/armour_shield_wooden_buckler.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/armour_shield_wooden_buckler.png"); _g_done_assets += 1
	verify("items/weapon_1handed_cultist_dagger.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/weapon_1handed_cultist_dagger.png"); _g_done_assets += 1
	verify("items/weapon_longrange_flintlock.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/weapon_longrange_flintlock.png"); _g_done_assets += 1
	verify("items/weapon_2handed_makeshift_spear.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/weapon_2handed_makeshift_spear.png"); _g_done_assets += 1
	verify("items/weapon_longrange_blunderbuss.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/weapon_longrange_blunderbuss.png"); _g_done_assets += 1
	verify("items/weapon_1handed_shaman_dagger.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/weapon_1handed_shaman_dagger.png"); _g_done_assets += 1
	verify("items/weapon_2handed_priest_staff.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/weapon_2handed_priest_staff.png"); _g_done_assets += 1
	verify("items/weapon_longrange_cultist_crossbow.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/weapon_longrange_cultist_crossbow.png"); _g_done_assets += 1
	verify("items/materials_component_bow_string.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_component_bow_string.png"); _g_done_assets += 1
	verify("maps/l_o_outer_gate_district.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Outer-Gate-District.png"); _g_done_assets += 1
	verify("maps/l_i_inside_the_wall.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Inside-The-Wall.png"); _g_done_assets += 1
	verify("maps/l_o_inner_military_district.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Inner-Military-Disctrict.png"); _g_done_assets += 1
	verify("maps/l_i_church_chapel.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/CHURCH-CHAPEL.png"); _g_done_assets += 1
	verify("maps/l_i_barracks_hall.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/BARRACKS-HALL.png"); _g_done_assets += 1
	verify("maps/l_o_church_outpost.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Church-Outpost.png"); _g_done_assets += 1
	verify("maps/l_i_orphanage_access.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Orphanage-Access-1.png"); _g_done_assets += 1
	verify("maps/l_i_theocratic_battleground_endingb.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Theocratic-Battleground-Ending-B.png"); _g_done_assets += 1
	verify("maps/l_i_main_cathedral.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Main-Cathedral.png"); _g_done_assets += 1
	verify("maps/l_o_destroy_theocracy.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Destroy-Theoracy.png"); _g_done_assets += 1
	verify("maps/l_i_church_administrative_wing.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Church-Administrative-Wing.png"); _g_done_assets += 1
	verify("maps/l_o_cathedral_plaza.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Cathedral-Plaza.png"); _g_done_assets += 1
	verify("maps/l_o_rare_nexus_points.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Rare-Nexus-Points-Zone-of-Terror.png"); _g_done_assets += 1
	verify("maps/f_o_deep_terror_zone.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Deep-Terror-Zone.png"); _g_done_assets += 1
	verify("maps/l_o_corrupted_frontier.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Corrupted-Frontier.png"); _g_done_assets += 1
	verify("maps/t_o_anomaly_forest.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Anomaly-Forest.png"); _g_done_assets += 1
	verify("maps/l_i_lab_office_under_administrative_wing.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Lab-Office-Under-Church-Administrative-WIng.png"); _g_done_assets += 1
	verify("maps/l_i_active_laboratory_under_administrative_wing.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Active-Laboratory-Under-Church-Administrative-WIng.png"); _g_done_assets += 1
	verify("maps/l_i_subterranean_labyrinth_exit.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Subterranean-Labyrithn-Exit.png"); _g_done_assets += 1
	verify("maps/l_i_subterranean_labyrinth.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Subterranean-Labyrithn-Slowed-Movements-Connected-to-New-Laboratory-Theocratic-Capital.png"); _g_done_assets += 1
	verify("maps/l_i_old_laboratory.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Old-Laboratory.png"); _g_done_assets += 1
	verify("maps/l_i_tutorial_ground.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Tutorial-Ground.png"); _g_done_assets += 1
	verify("maps/t_o_tutorial_ground_shaman.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Tutorial-Ground-Shaman-DLC.png"); _g_done_assets += 1
	verify("maps/l_i_tutorial_ground_dlc.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Tutorial-Ground-DLC.png"); _g_done_assets += 1
	verify("maps/l_i_tutorial_ground_first_version.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/First-Version.png"); _g_done_assets += 1
	verify("maps/t_i_escape_route.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Excape-Route.png"); _g_done_assets += 1
	verify("maps/t_o_destroyed_tribe_settlement.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Destroyed-Tribe-Settlement.png"); _g_done_assets += 1
	verify("maps/t_o_tribe_settlement.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Tribe-Settlement.png"); _g_done_assets += 1
	verify("maps/t_o_tribe_perimeter.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Tribe-Perimeter.png"); _g_done_assets += 1
	verify("maps/t_i_storage_cave.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Storage-Cave.png"); _g_done_assets += 1
	verify("maps/t_i_healing_hut.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Healing-Hut.png"); _g_done_assets += 1
	verify("maps/l_i_headmaster_office.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Headmaster-Office.png"); _g_done_assets += 1
	verify("maps/l_i_the_play_room.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/The-Play-Room.png"); _g_done_assets += 1
	verify("maps/l_o_the_old_orphanage.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/The-Old-Orphanage.png"); _g_done_assets += 1
	verify("maps/l_o_home_village_entry.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Home-Village-Entry.png"); _g_done_assets += 1
	verify("maps/l_o_home_village_center.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Home-Village-Center.png"); _g_done_assets += 1
	verify("maps/l_i_chief_home.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Chief_s-Home.png"); _g_done_assets += 1
	verify("maps/f_o_village_market.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Village-Market-Village-Outskirts.png"); _g_done_assets += 1
	verify("maps/f_i_tunnel_passage_to_tribe.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Tunnel-Passage-to-Tribe.png"); _g_done_assets += 1
	verify("maps/f_o_residential_area.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Residential-Area-Village-Outskirts.png"); _g_done_assets += 1
	verify("maps/f_i_inside_chief_home.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Int.-Chief_s-Home.png"); _g_done_assets += 1
	verify("maps/f_o_outside_chief_home.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Ext.-Chief_s-Home.png"); _g_done_assets += 1
	verify("maps/f_i_inside_elder_house.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Elder-House-Int.png"); _g_done_assets += 1
	verify("maps/c_o_lowms_cultist_battleground.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Low-MS-Cultist-Battleground.png"); _g_done_assets += 1
	verify("maps/c_i_inner_sanctum.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Inner-Sanctum-Cult.png"); _g_done_assets += 1
	verify("maps/c_o_cultist_battleground.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Cultist-Battleground.png"); _g_done_assets += 1
	verify("maps/c_o_cult_village.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Cult-VIllage.png"); _g_done_assets += 1
	verify("maps/c_i_cult_leader_fortress.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Cult-Leader-Fortress.png"); _g_done_assets += 1
	verify("maps/c_o_cult_funeris_encounter.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Cult-Funeris-Encounter-CULTIST-SPAWN.png"); _g_done_assets += 1
	verify("maps/c_o_coastal_landing.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Coastal-Landing.png"); _g_done_assets += 1
	verify("maps/l_i_merchant_bank.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Merchant-Bank.png"); _g_done_assets += 1
	verify("maps/l_i_the_ship.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/The-Ship-Transitioning.png"); _g_done_assets += 1
	verify("maps/l_i_ship_lower_part.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Ship-Lower-Part-DLC-EXCLUSIVE.png"); _g_done_assets += 1
	verify("maps/l_i_merchant_tavern.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Merchant-Tavern.png"); _g_done_assets += 1
	verify("maps/l_o_merchant_quarter.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Merchant-Quarter.png"); _g_done_assets += 1
	verify("maps/l_i_merchant_guild_hall.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Merchant-Guild-Hall.png"); _g_done_assets += 1
	verify("maps/l_i_lumen_spy_merchant_guild.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Lumen-Spy-Merchant-Guild-DLC-EXCLUSIVE-.png"); _g_done_assets += 1
	verify("maps/l_o_harbor_district.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Harbor-District.png"); _g_done_assets += 1
	verify("maps/l_i_clearance_office.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/2-Clearance-Office.png"); _g_done_assets += 1
	verify("maps/l_i_customs_office.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/1-Customs-Office.png"); _g_done_assets += 1
	verify("sprites/npc_e_cult_leader/elucidate_idle_cult_leader_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_cult_leader_npc_down.png"); _g_done_assets += 1
	verify("sprites/npc_e_cult_leader/elucidate_idle_cult_leader_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_cult_leader_npc_up.png"); _g_done_assets += 1
	verify("sprites/npc_e_cult_leader/elucidate_idle_cult_leader_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_cult_leader_npc_left.png"); _g_done_assets += 1
	verify("sprites/npc_e_cult_leader/elucidate_idle_cult_leader_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_cult_leader_npc_right.png"); _g_done_assets += 1
	verify("sprites/npc_e_cult_soldier/elucidate_idle_cultist_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_cultist_npc_up.png"); _g_done_assets += 1
	verify("sprites/npc_e_cult_soldier/elucidate_idle_cultist_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_cultist_npc_right.png"); _g_done_assets += 1
	verify("sprites/npc_e_cult_soldier/elucidate_idle_cultist_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_cultist_npc_left.png"); _g_done_assets += 1
	verify("sprites/npc_e_cult_soldier/elucidate_idle_cultist_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_cultist_npc_down.png"); _g_done_assets += 1
	verify("sprites/npc_e_s1_corrupted_cultist/elucidate_idle_corrupted1_cultist_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_corrupted1_cultist_npc_right.png"); _g_done_assets += 1
	verify("sprites/npc_e_s1_corrupted_cultist/elucidate_idle_corrupted1_cultist_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_corrupted1_cultist_npc_left.png"); _g_done_assets += 1
	verify("sprites/npc_e_s1_corrupted_cultist/elucidate_idle_corrupted1_cultist_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_corrupted1_cultist_npc_down.png"); _g_done_assets += 1
	verify("sprites/npc_e_s1_corrupted_cultist/elucidate_idle_corrupted1_cultist_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_corrupted1_cultist_npc_up.png"); _g_done_assets += 1
	verify("sprites/npc_e_amalgamated_villagers/elucidate_idle_amalgamated_villagers_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_amalgamated_villagers_npc_right.png"); _g_done_assets += 1
	verify("sprites/npc_e_amalgamated_villagers/elucidate_idle_amalgamated_villagers_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_amalgamated_villagers_npc_left.png"); _g_done_assets += 1
	verify("sprites/npc_e_amalgamated_knights/elucidate_idle_amalgamated_knights_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_amalgamated_knights_npc_right.png"); _g_done_assets += 1
	verify("sprites/npc_e_amalgamated_knights/elucidate_idle_amalgamated_knights_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_amalgamated_knights_npc_left.png"); _g_done_assets += 1
	verify("sprites/npc_e_amalgamated_civilians/elucidate_idle_amalgamated_civillians_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_amalgamated_civillians_npc_right.png"); _g_done_assets += 1
	verify("sprites/npc_e_amalgamated_civilians/elucidate_idle_amalgamated_civillians_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_amalgamated_civillians_npc_left.png"); _g_done_assets += 1
	verify("sprites/npc_e_melted_villager_male/elucidate_idle_melted_male_villager_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_melted_male_villager_npc_right.png"); _g_done_assets += 1
	verify("sprites/npc_e_melted_villager_male/elucidate_idle_melted_male_villager_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_melted_male_villager_npc_left.png"); _g_done_assets += 1
	verify("sprites/npc_e_melted_villager_male/elucidate_idle_melted_male_villager_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_melted_male_villager_npc_up.png"); _g_done_assets += 1
	verify("sprites/npc_e_melted_villager_male/elucidate_idle_melted_male_villager_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_melted_male_villager_npc_down.png"); _g_done_assets += 1
	verify("sprites/npc_e_melted_villager_female/elucidate_idle_melted_female_villager_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_melted_female_villager_npc_up.png"); _g_done_assets += 1
	verify("sprites/npc_e_melted_villager_female/elucidate_idle_melted_female_villager_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_melted_female_villager_npc_right.png"); _g_done_assets += 1
	verify("sprites/npc_e_melted_villager_female/elucidate_idle_melted_female_villager_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_melted_female_villager_npc_left.png"); _g_done_assets += 1
	verify("sprites/npc_e_melted_villager_female/elucidate_idle_melted_female_villager_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_melted_female_villager_npc_down.png"); _g_done_assets += 1
	verify("sprites/npc_e_s3_corrupted_cultist/elucidate_idle_corrupted3_cultist_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_corrupted3_cultist_npc_up.png"); _g_done_assets += 1
	verify("sprites/npc_e_s3_corrupted_cultist/elucidate_idle_corrupted3_cultist_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_corrupted3_cultist_npc_right.png"); _g_done_assets += 1
	verify("sprites/npc_e_s3_corrupted_cultist/elucidate_idle_corrupted3_cultist_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_corrupted3_cultist_npc_left.png"); _g_done_assets += 1
	verify("sprites/npc_e_s3_corrupted_cultist/elucidate_idle_corrupted3_cultist_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_corrupted3_cultist_npc_down.png"); _g_done_assets += 1
	verify("sprites/npc_e_s2_corrupted_cultist/elucidate_idle_corrupted2_cultist_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_corrupted3_cultist_npc_up.png"); _g_done_assets += 1
	verify("sprites/npc_e_s2_corrupted_cultist/elucidate_idle_corrupted2_cultist_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_corrupted3_cultist_npc_right.png"); _g_done_assets += 1
	verify("sprites/npc_e_s2_corrupted_cultist/elucidate_idle_corrupted2_cultist_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_corrupted3_cultist_npc_left.png"); _g_done_assets += 1
	verify("sprites/npc_e_s2_corrupted_cultist/elucidate_idle_corrupted2_cultist_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_corrupted3_cultist_npc_down.png"); _g_done_assets += 1
	verify("sprites/npc_n_librarian_scholar/elucidate_idle_librarian_scholar_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_librarian_scholar_npc_up.png"); _g_done_assets += 1
	verify("sprites/npc_n_librarian_scholar/elucidate_idle_librarian_scholar_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_librarian_scholar_npc_right.png"); _g_done_assets += 1
	verify("sprites/npc_n_librarian_scholar/elucidate_idle_librarian_scholar_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_librarian_scholar_npc_left.png"); _g_done_assets += 1
	verify("sprites/npc_n_librarian_scholar/elucidate_idle_librarian_scholar_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_librarian_scholar_npc_down.png"); _g_done_assets += 1
	verify("sprites/npc_e_luminarian_knight/elucidate_idle_holyknight_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_holyknight_npc_up.png"); _g_done_assets += 1
	verify("sprites/npc_e_luminarian_knight/elucidate_idle_holyknight_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_holyknight_npc_right.png"); _g_done_assets += 1
	verify("sprites/npc_e_luminarian_knight/elucidate_idle_holyknight_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_holyknight_npc_left.png"); _g_done_assets += 1
	verify("sprites/npc_e_luminarian_knight/elucidate_idle_holyknight_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_holyknight_npc_down.png"); _g_done_assets += 1
	verify("sprites/npc_n_faithful_luminarian/elucidate_idle_male_faithful_citizen_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_male_faithful_citizen_npc_up.png"); _g_done_assets += 1
	verify("sprites/npc_n_faithful_luminarian/elucidate_idle_male_faithful_citizen_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_male_faithful_citizen_npc_right.png"); _g_done_assets += 1
	verify("sprites/npc_n_faithful_luminarian/elucidate_idle_male_faithful_citizen_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_male_faithful_citizen_npc_left.png"); _g_done_assets += 1
	verify("sprites/npc_n_faithful_luminarian/elucidate_idle_male_faithful_citizen_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_male_faithful_citizen_npc_down.png"); _g_done_assets += 1
	verify("sprites/npc_n_faithful_luminarie/elucidate_idle_female_faithful_citizen_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_female_faithful_citizen_npc_up.png"); _g_done_assets += 1
	verify("sprites/npc_n_faithful_luminarie/elucidate_idle_female_faithful_citizen_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_female_faithful_citizen_npc_right.png"); _g_done_assets += 1
	verify("sprites/npc_n_faithful_luminarie/elucidate_idle_female_faithful_citizen_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_female_faithful_citizen_npc_left.png"); _g_done_assets += 1
	verify("sprites/npc_n_faithful_luminarie/elucidate_idle_female_faithful_citizen_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_female_faithful_citizen_npc_down.png"); _g_done_assets += 1
	verify("sprites/npc_n_luminarian_priest/elucidate_idle_sprite_chuAttendants_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_sprite_chuAttendants_up.png"); _g_done_assets += 1
	verify("sprites/npc_n_luminarian_priest/elucidate_idle_sprite_chuAttendants_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_sprite_chuAttendants_right.png"); _g_done_assets += 1
	verify("sprites/npc_n_luminarian_priest/elucidate_idle_sprite_chuAttendants_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_sprite_chuAttendants_left.png"); _g_done_assets += 1
	verify("sprites/npc_n_luminarian_priest/elucidate_idle_sprite_chuAttendants_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_sprite_chuAttendants_down.png"); _g_done_assets += 1
	verify("sprites/npc_e_lunar_assasin/elucidate_idle_assassin_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_assassin_npc_up.png"); _g_done_assets += 1
	verify("sprites/npc_e_lunar_assasin/elucidate_idle_assassin_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_assassin_npc_right.png"); _g_done_assets += 1
	verify("sprites/npc_e_lunar_assasin/elucidate_idle_assassin_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_assassin_npc_left.png"); _g_done_assets += 1
	verify("sprites/npc_e_lunar_assasin/elucidate_idle_assassin_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_assassin_npc_down.png"); _g_done_assets += 1
	verify("sprites/npc_n_seekers_warrior_male/elucidate_idle_tribe_warrior_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_tribe_warrior_npc_up.png"); _g_done_assets += 1
	verify("sprites/npc_n_seekers_warrior_male/elucidate_idle_tribe_warrior_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_tribe_warrior_npc_right.png"); _g_done_assets += 1
	verify("sprites/npc_n_seekers_warrior_male/elucidate_idle_tribe_warrior_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_tribe_warrior_npc_left.png"); _g_done_assets += 1
	verify("sprites/npc_n_seekers_warrior_male/elucidate_idle_tribe_warrior_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_tribe_warrior_npc_down.png"); _g_done_assets += 1
	verify("sprites/npc_n_seekers_elder/elucidate_idle_tribe_elder_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_tribe_elder_npc_up.png"); _g_done_assets += 1
	verify("sprites/npc_n_seekers_elder/elucidate_idle_tribe_elder_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_tribe_elder_npc_right.png"); _g_done_assets += 1
	verify("sprites/npc_n_seekers_elder/elucidate_idle_tribe_elder_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_tribe_elder_npc_left.png"); _g_done_assets += 1
	verify("sprites/npc_n_seekers_elder/elucidate_idle_tribe_elder_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_tribe_elder_npc_down.png"); _g_done_assets += 1
	verify("sprites/npc_n_seekers_chieftain/elucidate_idle_tribe_chief_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_tribe_chief_npc_up.png"); _g_done_assets += 1
	verify("sprites/npc_n_seekers_chieftain/elucidate_idle_tribe_chief_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_tribe_chief_npc_right.png"); _g_done_assets += 1
	verify("sprites/npc_n_seekers_chieftain/elucidate_idle_tribe_chief_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_tribe_chief_npc_left.png"); _g_done_assets += 1
	verify("sprites/npc_n_seekers_chieftain/elucidate_idle_tribe_chief_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_tribe_chief_npc_down.png"); _g_done_assets += 1
	verify("sprites/npc_n_traveling_merchant/elucidate_idle_supply_merchant_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_supply_merchant_npc_down.png"); _g_done_assets += 1
	verify("sprites/npc_n_traveling_merchant/elucidate_idle_supply_merchant_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_supply_merchant_npc_up.png"); _g_done_assets += 1
	verify("sprites/npc_n_traveling_merchant/elucidate_idle_supply_merchant_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_supply_merchant_npc_right.png"); _g_done_assets += 1
	verify("sprites/npc_n_traveling_merchant/elucidate_idle_supply_merchant_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_supply_merchant_npc_left.png"); _g_done_assets += 1
	verify("sprites/npc_n_merchant_guild_member/elucidate_idle_merchant_guild_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_merchant_guild_npc_up.png"); _g_done_assets += 1
	verify("sprites/npc_n_merchant_guild_member/elucidate_idle_merchant_guild_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_merchant_guild_npc_right.png"); _g_done_assets += 1
	verify("sprites/npc_n_merchant_guild_member/elucidate_idle_merchant_guild_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_merchant_guild_npc_left.png"); _g_done_assets += 1
	verify("sprites/npc_n_merchant_guild_member/elucidate_idle_merchant_guild_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_merchant_guild_npc_down.png"); _g_done_assets += 1
	verify("sprites/npc_n_merchant_guild_director/elucidate_idle_merchant_guild_master_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_merchant_guild_master_npc_up.png"); _g_done_assets += 1
	verify("sprites/npc_n_merchant_guild_director/elucidate_idle_merchant_guild_master_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_merchant_guild_master_npc_right.png"); _g_done_assets += 1
	verify("sprites/npc_n_merchant_guild_director/elucidate_idle_merchant_guild_master_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_merchant_guild_master_npc_left.png"); _g_done_assets += 1
	verify("sprites/npc_n_merchant_guild_director/elucidate_idle_merchant_guild_master_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_merchant_guild_master_npc_down.png"); _g_done_assets += 1
	verify("sprites/npc_n_harbor_captain/elucidate_idle_harbor_captain_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_harbor_captain_npc_up.png"); _g_done_assets += 1
	verify("sprites/npc_n_harbor_captain/elucidate_idle_harbor_captain_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_harbor_captain_npc_right.png"); _g_done_assets += 1
	verify("sprites/npc_n_harbor_captain/elucidate_idle_harbor_captain_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_harbor_captain_npc_left.png"); _g_done_assets += 1
	verify("sprites/npc_n_harbor_captain/elucidate_idle_harbor_captain_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_harbor_captain_npc_down.png"); _g_done_assets += 1
	verify("sprites/npc_n_s2_outskirts_villagers/elucidate_idle_male_villager_variant_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_male_villager_variant_npc_up.png"); _g_done_assets += 1
	verify("sprites/npc_n_s2_outskirts_villagers/elucidate_idle_male_villager_variant_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_male_villager_variant_npc_right.png"); _g_done_assets += 1
	verify("sprites/npc_n_s2_outskirts_villagers/elucidate_idle_male_villager_variant_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_male_villager_variant_npc_left.png"); _g_done_assets += 1
	verify("sprites/npc_n_s2_outskirts_villagers/elucidate_idle_male_villager_variant_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_male_villager_variant_npc_down.png"); _g_done_assets += 1
	verify("sprites/npc_n_s1_outskirts_villagers/elucidate_idle_male_villager_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_male_villager_npc_up.png"); _g_done_assets += 1
	verify("sprites/npc_n_s1_outskirts_villagers/elucidate_idle_male_villager_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_male_villager_npc_right.png"); _g_done_assets += 1
	verify("sprites/npc_n_s1_outskirts_villagers/elucidate_idle_male_villager_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_male_villager_npc_left.png"); _g_done_assets += 1
	verify("sprites/npc_n_s1_outskirts_villagers/elucidate_idle_male_villager_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_male_villager_npc_down.png"); _g_done_assets += 1
	verify("sprites/npc_n_s2_outskirts_villagers/elucidate_idle_female_villager_variant_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_female_villager_variant_npc_up.png"); _g_done_assets += 1
	verify("sprites/npc_n_s2_outskirts_villagers/elucidate_idle_female_villager_variant_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_female_villager_variant_npc_right.png"); _g_done_assets += 1
	verify("sprites/npc_n_s2_outskirts_villagers/elucidate_idle_female_villager_variant_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_female_villager_variant_npc_left.png"); _g_done_assets += 1
	verify("sprites/npc_n_s2_outskirts_villagers/elucidate_idle_female_villager_variant_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_female_villager_variant_npc_down.png"); _g_done_assets += 1
	verify("sprites/npc_n_s1_outskirts_villagers/elucidate_idle_female_villager_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_female_villager_npc_up.png"); _g_done_assets += 1
	verify("sprites/npc_n_s1_outskirts_villagers/elucidate_idle_female_villager_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_female_villager_npc_right.png"); _g_done_assets += 1
	verify("sprites/npc_n_s1_outskirts_villagers/elucidate_idle_female_villager_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_female_villager_npc_left.png"); _g_done_assets += 1
	verify("sprites/npc_n_s1_outskirts_villagers/elucidate_idle_female_villager_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_female_villager_npc_down.png"); _g_done_assets += 1
	verify("sprites/npc_n_guards/elucidate_idle_guards_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_guards_npc_up.png"); _g_done_assets += 1
	verify("sprites/npc_n_guards/elucidate_idle_guards_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_guards_npc_right.png"); _g_done_assets += 1
	verify("sprites/npc_n_guards/elucidate_idle_guards_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_guards_npc_left.png"); _g_done_assets += 1
	verify("sprites/npc_n_guards/elucidate_idle_guards_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_guards_npc_down.png"); _g_done_assets += 1
	verify("sprites/npc_n_guard_captain/elucidate_idle_guard_captain_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_guard_captain_npc_up.png"); _g_done_assets += 1
	verify("sprites/npc_n_guard_captain/elucidate_idle_guard_captain_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_guard_captain_npc_right.png"); _g_done_assets += 1
	verify("sprites/npc_n_guard_captain/elucidate_idle_guard_captain_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_guard_captain_npc_left.png"); _g_done_assets += 1
	verify("sprites/npc_n_guard_captain/elucidate_idle_guard_captain_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_guard_captain_npc_down.png"); _g_done_assets += 1
	verify("sprites/npc_n_draft_officer/elucidate_idle_draft_officer_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_draft_officer_npc_up.png"); _g_done_assets += 1
	verify("sprites/npc_n_draft_officer/elucidate_idle_draft_officer_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_draft_officer_npc_right.png"); _g_done_assets += 1
	verify("sprites/npc_n_draft_officer/elucidate_idle_draft_officer_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_draft_officer_npc_left.png"); _g_done_assets += 1
	verify("sprites/npc_n_draft_officer/elucidate_idle_draft_officer_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_draft_officer_npc_down.png"); _g_done_assets += 1
	verify("sprites/npc_n_s1_walled_city_civilians_male/elucidate_idle_male_civilian_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_male_civilian_npc_up.png"); _g_done_assets += 1
	verify("sprites/npc_n_s1_walled_city_civilians_male/elucidate_idle_male_civilian_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_male_civilian_npc_right.png"); _g_done_assets += 1
	verify("sprites/npc_n_s1_walled_city_civilians_male/elucidate_idle_male_civilian_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_male_civilian_npc_left.png"); _g_done_assets += 1
	verify("sprites/npc_n_s1_walled_city_civilians_male/elucidate_idle_male_civilian_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_male_civilian_npc_down.png"); _g_done_assets += 1
	verify("sprites/npc_n_s1_walled_city_civilians_female/elucidate_idle_female_civilian_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_female_civilian_npc_up.png"); _g_done_assets += 1
	verify("sprites/npc_n_s1_walled_city_civilians_female/elucidate_idle_female_civilian_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_female_civilian_npc_right.png"); _g_done_assets += 1
	verify("sprites/npc_n_s1_walled_city_civilians_female/elucidate_idle_female_civilian_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_female_civilian_npc_left.png"); _g_done_assets += 1
	verify("sprites/npc_n_s1_walled_city_civilians_female/elucidate_idle_female_civilian_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_female_civilian_npc_down.png"); _g_done_assets += 1
	verify("sprites/npc_n_blacksmith_conrad/elucidate_idle_blacksmith_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_blacksmith_npc_up.png"); _g_done_assets += 1
	verify("sprites/npc_n_blacksmith_conrad/elucidate_idle_blacksmith_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_blacksmith_npc_right.png"); _g_done_assets += 1
	verify("sprites/npc_n_blacksmith_conrad/elucidate_idle_blacksmith_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_blacksmith_npc_left.png"); _g_done_assets += 1
	verify("sprites/npc_n_blacksmith_conrad/elucidate_idle_blacksmith_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_blacksmith_npc_down.png"); _g_done_assets += 1
	verify("sprites/player_shaman/elucidate_sprite_shaman_left_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_shaman_left_001.png"); _g_done_assets += 1
	verify("sprites/player_shaman/elucidate_sprite_shaman_left_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_shaman_left_002.png"); _g_done_assets += 1
	verify("sprites/player_shaman/elucidate_sprite_shaman_left_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_shaman_left_003.png"); _g_done_assets += 1
	verify("sprites/player_shaman/elucidate_attack_shaman_left_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_attack_shaman_left_001.png"); _g_done_assets += 1
	verify("sprites/player_shaman/elucidate_attack_shaman_left_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_attack_shaman_left_002.png"); _g_done_assets += 1
	verify("sprites/player_shaman/elucidate_sprite_shaman_down_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_shaman_down_002-1.png"); _g_done_assets += 1
	verify("sprites/player_shaman/elucidate_sprite_shaman_down_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_shaman_down_001.png"); _g_done_assets += 1
	verify("sprites/player_shaman/elucidate_sprite_shaman_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_shaman_down_002.png"); _g_done_assets += 1
	verify("sprites/player_shaman/elucidate_attack_shaman_down_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_attack_shaman_down_001.png"); _g_done_assets += 1
	verify("sprites/player_shaman/elucidate_attack_shaman_down_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_attack_shaman_down_002.png"); _g_done_assets += 1
	verify("sprites/player_shaman/elucidate_sprite_shaman_up_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_shaman_up_002.png"); _g_done_assets += 1
	verify("sprites/player_shaman/elucidate_sprite_shaman_up_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_shaman_up_001-1.png"); _g_done_assets += 1
	verify("sprites/player_shaman/elucidate_sprite_shaman_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_shaman_up_001.png"); _g_done_assets += 1
	verify("sprites/player_shaman/elucidate_attack_shaman_up_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_attack_shaman_up_001.png"); _g_done_assets += 1
	verify("sprites/player_shaman/elucidate_attack_shaman_up_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_attack_shaman_up_002.png"); _g_done_assets += 1
	verify("sprites/player_shaman/elucidate_sprite_shaman_right_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_shaman_right_002.png"); _g_done_assets += 1
	verify("sprites/player_shaman/elucidate_sprite_shaman_right_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_shaman_right_001.png"); _g_done_assets += 1
	verify("sprites/player_shaman/elucidate_sprite_shaman_right_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_shaman_right_004.png"); _g_done_assets += 1
	verify("sprites/player_shaman/elucidate_attack_shaman_right_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_attack_shaman_right_001.png"); _g_done_assets += 1
	verify("sprites/player_shaman/elucidate_attack_shaman_right_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_attack_shaman_right_002.png"); _g_done_assets += 1
	verify("sprites/player_merchant/elucidate_sprite_merchant_up_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_merchant_up_002.png"); _g_done_assets += 1
	verify("sprites/player_merchant/elucidate_sprite_merchant_up_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_merchant_up_001-1.png"); _g_done_assets += 1
	verify("sprites/player_merchant/elucidate_sprite_merchant_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_merchant_up_001.png"); _g_done_assets += 1
	verify("sprites/player_merchant/elucidate_attack_merchant_up_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_attack_merchant_up_001.png"); _g_done_assets += 1
	verify("sprites/player_merchant/elucidate_attack_merchant_up_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_attack_merchant_up_002.png"); _g_done_assets += 1
	verify("sprites/player_merchant/elucidate_sprite_merchant_right_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_merchant_right_002.png"); _g_done_assets += 1
	verify("sprites/player_merchant/elucidate_sprite_merchant_right_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_merchant_right_001.png"); _g_done_assets += 1
	verify("sprites/player_merchant/elucidate_sprite_merchant_right_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_merchant_right_004.png"); _g_done_assets += 1
	verify("sprites/player_merchant/elucidate_attack_merchant_right_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_attack_merchant_right_001.png"); _g_done_assets += 1
	verify("sprites/player_merchant/elucidate_attack_merchant_right_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_attack_merchant_right_002.png"); _g_done_assets += 1
	verify("sprites/player_merchant/elucidate_sprite_merchant_left_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_merchant_left_002.png"); _g_done_assets += 1
	verify("sprites/player_merchant/elucidate_sprite_merchant_left_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_merchant_left_001.png"); _g_done_assets += 1
	verify("sprites/player_merchant/elucidate_sprite_merchant_left_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_merchant_left_003.png"); _g_done_assets += 1
	verify("sprites/player_merchant/elucidate_attack_merchant_left_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_attack_merchant_left_001.png"); _g_done_assets += 1
	verify("sprites/player_merchant/elucidate_attack_merchant_left_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_attack_merchant_left_002.png"); _g_done_assets += 1
	verify("sprites/player_merchant/elucidate_sprite_merchant_down_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_merchant_down_002.png"); _g_done_assets += 1
	verify("sprites/player_merchant/elucidate_sprite_merchant_down_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_merchant_down_001.png"); _g_done_assets += 1
	verify("sprites/player_merchant/elucidate_sprite_merchant_down_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_merchant_down_002.png"); _g_done_assets += 1
	verify("sprites/player_merchant/elucidate_attack_merchant_down_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_attack_merchant_down_001.png"); _g_done_assets += 1
	verify("sprites/player_merchant/elucidate_attack_merchant_down_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_attack_merchant_down_002.png"); _g_done_assets += 1
	verify("sprites/player_priest/elucidate_sprite_priest_left_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_priest_left_002.png"); _g_done_assets += 1
	verify("sprites/player_priest/elucidate_sprite_priest_left_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_priest_left_001.png"); _g_done_assets += 1
	verify("sprites/player_priest/elucidate_sprite_priest_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_priest_left.png"); _g_done_assets += 1
	verify("sprites/player_priest/elucidate_attack_priest_left_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_attack_priest_left_001.png"); _g_done_assets += 1
	verify("sprites/player_priest/elucidate_attack_priest_left_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_attack_priest_left_002.png"); _g_done_assets += 1
	verify("sprites/player_priest/elucidate_sprite_priest_down_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_priest_down_002.png"); _g_done_assets += 1
	verify("sprites/player_priest/elucidate_sprite_priest_down_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_priest_down_001-1.png"); _g_done_assets += 1
	verify("sprites/player_priest/elucidate_sprite_priest_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_priest_down.png"); _g_done_assets += 1
	verify("sprites/player_priest/elucidate_attack_priest_down_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_attack_priest_down_001.png"); _g_done_assets += 1
	verify("sprites/player_priest/elucidate_attack_priest_down_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_attack_priest_down_002.png"); _g_done_assets += 1
	verify("sprites/player_priest/elucidate_sprite_priest_up_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_priest_up_002.png"); _g_done_assets += 1
	verify("sprites/player_priest/elucidate_sprite_priest_up_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_priest_up_001-1.png"); _g_done_assets += 1
	verify("sprites/player_priest/elucidate_sprite_priest_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_priest_up.png"); _g_done_assets += 1
	verify("sprites/player_priest/elucidate_attack_priest_up_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_attack_priest_up_001.png"); _g_done_assets += 1
	verify("sprites/player_priest/elucidate_attack_priest_up_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_attack_priest_up_002.png"); _g_done_assets += 1
	verify("sprites/player_priest/elucidate_sprite_priest_right_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_priest_right_002.png"); _g_done_assets += 1
	verify("sprites/player_priest/elucidate_sprite_priest_right_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_priest_right_001.png"); _g_done_assets += 1
	verify("sprites/player_priest/elucidate_sprite_priest_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_priest_right.png"); _g_done_assets += 1
	verify("sprites/player_priest/elucidate_attack_priest_right_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_attack_priest_right_001.png"); _g_done_assets += 1
	verify("sprites/player_priest/elucidate_attack_priest_right_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_attack_priest_right_002.png"); _g_done_assets += 1
	verify("sprites/player_cultist/elucidate_walking_sprite_cultist_down_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walking_sprite_cultist_down_002.png"); _g_done_assets += 1
	verify("sprites/player_cultist/elucidate_walking_sprite_cultist_down_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walking_sprite_cultist_down_001.png"); _g_done_assets += 1
	verify("sprites/player_cultist/elucidate_sprite_cultist_down_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_sprite_cultist_down_002.png"); _g_done_assets += 1
	verify("sprites/player_cultist/elucidate_attack_cultist_down_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_attack_cultist_down_001.png"); _g_done_assets += 1
	verify("sprites/player_cultist/elucidate_attack_cultist_down_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_attack_cultist_down_002.png"); _g_done_assets += 1
	verify("sprites/player_cultist/elucidate_walking_sprite_cultist_up_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walking_sprite_cultist_up_002.png"); _g_done_assets += 1
	verify("sprites/player_cultist/elucidate_walking_sprite_cultist_up_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walking_sprite_cultist_up_001.png"); _g_done_assets += 1
	verify("sprites/player_cultist/elucidate_sprite_cultist_up_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_sprite_cultist_up_001.png"); _g_done_assets += 1
	verify("sprites/player_cultist/elucidate_attack_cultist_up_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_attack_cultist_up_001.png"); _g_done_assets += 1
	verify("sprites/player_cultist/elucidate_attack_cultist_up_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_attack_cultist_up_002.png"); _g_done_assets += 1
	verify("sprites/player_cultist/elucidate_walking_sprite_cultist_right_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walking_sprite_cultist_right_002.png"); _g_done_assets += 1
	verify("sprites/player_cultist/elucidate_walking_sprite_cultist_right_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walking_sprite_cultist_right_001.png"); _g_done_assets += 1
	verify("sprites/player_cultist/elucidate_sprite_cultist_right_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_cultist_right_004.png"); _g_done_assets += 1
	verify("sprites/player_cultist/elucidate_attack_cultist_right_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_attack_cultist_right_001.png"); _g_done_assets += 1
	verify("sprites/player_cultist/elucidate_attack_cultist_right_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_attack_cultist_right_002.png"); _g_done_assets += 1
	verify("sprites/player_cultist/elucidate_walking_sprite_cultist_left_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walking_sprite_cultist_left_002.png"); _g_done_assets += 1
	verify("sprites/player_cultist/elucidate_walking_sprite_cultist_left_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walking_sprite_cultist_left_001.png"); _g_done_assets += 1
	verify("sprites/player_cultist/elucidate_sprite_cultist_left_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_cultist_left_003.png"); _g_done_assets += 1
	verify("sprites/player_cultist/elucidate_attack_cultist_left_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_attack_cultist_left_001.png"); _g_done_assets += 1
	verify("sprites/player_cultist/elucidate_attack_cultist_left_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_attack_cultist_left_002.png"); _g_done_assets += 1
	verify("sprites/npc_e_caligo_manifestation/elucidate_idle_caligo_manifestation.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_caligo_manifestationenemy.png"); _g_done_assets += 1
	verify("sprites/npc_e_caligo_manifestation/elucidate_idle_caligo_manifestation_black_bg.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_caligo_manifestation_black_bg.png"); _g_done_assets += 1
	verify("sprites/npc_n_imprisoned_experiment/elucidate_idle_imprisoned_experiment_1_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_imprisoned_experiment_1_npc_down.png"); _g_done_assets += 1
	verify("sprites/npc_n_imprisoned_experiment/elucidate_idle_imprisoned_experiment_2_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_imprisoned_experiment_2_npc_down.png"); _g_done_assets += 1
	verify("sprites/npc_e_imprisoned_experiment/elucidate_idle_imprisoned_experiment_hostile_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_imprisoned_experiment_hostile_npc_down.png"); _g_done_assets += 1
	verify("sprites/npc_n_luminarian_scientist/elucidate_idle_church_medical_staff_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_church_medical_staff_npc_down.png"); _g_done_assets += 1
	verify("sprites/npc_n_luminarian_scientist/elucidate_idle_church_medical_staff_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_church_medical_staff_npc_right.png"); _g_done_assets += 1
	verify("sprites/npc_n_luminarian_scientist/elucidate_idle_church_medical_staff_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_church_medical_staff_npc_up.png"); _g_done_assets += 1
	verify("sprites/npc_n_luminarian_scientist/elucidate_idle_church_medical_staff_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_church_medical_staff_npc_left.png"); _g_done_assets += 1
	verify("sprites/npc_e_luminarian_spy/elucidate_idle_church_spy_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_church_spy_npc_down.png"); _g_done_assets += 1
	verify("sprites/npc_e_luminarian_spy/elucidate_walk_church_spy_npc_down_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walk_church_spy_npc_down_001.png"); _g_done_assets += 1
	verify("sprites/npc_e_luminarian_spy/elucidate_walk_church_spy_npc_down_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walk_church_spy_npc_down_002.png"); _g_done_assets += 1
	verify("sprites/npc_e_luminarian_spy/elucidate_idle_church_spy_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_church_spy_npc_left.png"); _g_done_assets += 1
	verify("sprites/npc_e_luminarian_spy/elucidate_walk_church_spy_npc_left_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walk_church_spy_npc_left_001.png"); _g_done_assets += 1
	verify("sprites/npc_e_luminarian_spy/elucidate_walk_church_spy_npc_left_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walk_church_spy_npc_left_002.png"); _g_done_assets += 1
	verify("sprites/npc_e_luminarian_spy/elucidate_idle_church_spy_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_church_spy_npc_right.png"); _g_done_assets += 1
	verify("sprites/npc_e_luminarian_spy/elucidate_walk_church_spy_npc_right_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walk_church_spy_npc_right_001.png"); _g_done_assets += 1
	verify("sprites/npc_e_luminarian_spy/elucidate_walk_church_spy_npc_right_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walk_church_spy_npc_right_002.png"); _g_done_assets += 1
	verify("sprites/npc_e_luminarian_spy/elucidate_idle_church_spy_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_church_spy_npc_up.png"); _g_done_assets += 1
	verify("sprites/npc_e_luminarian_spy/elucidate_walk_church_spy_npc_up_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walk_church_spy_npc_up_001.png"); _g_done_assets += 1
	verify("sprites/npc_e_luminarian_spy/elucidate_walk_church_spy_npc_up_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walk_church_spy_npc_up_002.png"); _g_done_assets += 1
	verify("sprites/npc_n_market_merchant_female/elucidate_idle_female_market_merchant_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_female_market_merchant_npc_down.png"); _g_done_assets += 1
	verify("sprites/npc_n_market_merchant_female/elucidate_idle_female_market_merchant_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_female_market_merchant_npc_left.png"); _g_done_assets += 1
	verify("sprites/npc_n_market_merchant_female/elucidate_idle_female_market_merchant_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_female_market_merchant_npc_right.png"); _g_done_assets += 1
	verify("sprites/npc_n_market_merchant_female/elucidate_idle_female_market_merchant_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_female_market_merchant_npc_up.png"); _g_done_assets += 1
	verify("sprites/npc_n_market_merchant_male/elucidate_idle_male_market_merchant_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_male_market_merchant_npc_down.png"); _g_done_assets += 1
	verify("sprites/npc_n_market_merchant_male/elucidate_idle_male_market_merchant_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_male_market_merchant_npc_left.png"); _g_done_assets += 1
	verify("sprites/npc_n_market_merchant_male/elucidate_idle_male_market_merchant_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_male_market_merchant_npc_right.png"); _g_done_assets += 1
	verify("sprites/npc_n_market_merchant_male/elucidate_idle_male_market_merchant_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_male_market_merchant_npc_up.png"); _g_done_assets += 1
	verify("sprites/npc_n_ghost_memories/elucidate_idle_ghost_memory1_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_ghost_memory1_npc_left.png"); _g_done_assets += 1
	verify("sprites/npc_n_ghost_memories/elucidate_idle_ghost_memory1_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_ghost_memory1_npc_right.png"); _g_done_assets += 1
	verify("sprites/npc_n_ghost_memories/elucidate_idle_ghost_memory2_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_ghost_memory2_npc_left1.png.png"); _g_done_assets += 1
	verify("sprites/npc_n_ghost_memories/elucidate_idle_ghost_memory2_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_ghost_memory2_npc_right.png"); _g_done_assets += 1
	verify("sprites/npc_n_seekers_warrior_female/elucidate_idle_female_tribal_warrior_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_female_tribal_warrior_npc_down.png"); _g_done_assets += 1
	verify("sprites/npc_n_seekers_warrior_female/elucidate_idle_female_tribal_warrior_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_female_tribal_warrior_npc_left.png"); _g_done_assets += 1
	verify("sprites/npc_n_seekers_warrior_female/elucidate_idle_female_tribal_warrior_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_female_tribal_warrior_npc_right.png"); _g_done_assets += 1
	verify("sprites/npc_n_seekers_warrior_female/elucidate_idle_female_tribal_warrior_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_female_tribal_warrior_npc_up.png"); _g_done_assets += 1
	verify("sprites/npc_n_travelling_bard/elucidate_idle_travelling_merchant_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_travelling_merchant_npc_down.png"); _g_done_assets += 1
	verify("sprites/npc_n_travelling_bard/elucidate_idle_travelling_merchant_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_travelling_merchant_npc_left.png"); _g_done_assets += 1
	verify("sprites/npc_n_travelling_bard/elucidate_idle_travelling_merchant_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_travelling_merchant_npc_right.png"); _g_done_assets += 1
	verify("sprites/npc_n_travelling_bard/elucidate_idle_travelling_merchant_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_travelling_merchant_npc_up.png"); _g_done_assets += 1
	verify("sprites/npc_n_cult_priest/elucidate_idle_cultist_priest_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_cultist_priest_npc_down.png"); _g_done_assets += 1
	verify("sprites/npc_n_cult_priest/elucidate_idle_cultist_priest_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_cultist_priest_npc_left.png"); _g_done_assets += 1
	verify("sprites/npc_n_cult_priest/elucidate_idle_cultist_priest_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_cultist_priest_npc_right.png"); _g_done_assets += 1
	verify("sprites/npc_n_cult_priest/elucidate_idle_cultist_priest_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_cultist_priest_npc_up.png"); _g_done_assets += 1
	verify("sprites/npc_n_tavern_keeper/elucidate_idle_tavern_keeper_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_tavern_keeper_npc_down.png"); _g_done_assets += 1
	verify("sprites/npc_n_tavern_keeper/elucidate_idle_tavern_keeper_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_tavern_keeper_npc_left.png"); _g_done_assets += 1
	verify("sprites/npc_n_tavern_keeper/elucidate_idle_tavern_keeper_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_tavern_keeper_npc_right.png"); _g_done_assets += 1
	verify("sprites/npc_n_tavern_keeper/elucidate_idle_tavern_keeper_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_tavern_keeper_npc_up.png"); _g_done_assets += 1
	verify("sprites/npc_e_cult_archers/elucidate_idle_cultist_archer_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_cultist_archer_npc_down.png"); _g_done_assets += 1
	verify("sprites/npc_e_cult_archers/elucidate_walk_cultist_archer_npc_down_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walk_cultist_archer_npc_down_001.png"); _g_done_assets += 1
	verify("sprites/npc_e_cult_archers/elucidate_walk_cultist_archer_npc_down_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walk_cultist_archer_npc_down_002.png"); _g_done_assets += 1
	verify("sprites/npc_e_cult_archers/elucidate_idle_cultist_archer_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_cultist_archer_npc_left.png"); _g_done_assets += 1
	verify("sprites/npc_e_cult_archers/elucidate_walk_cultist_archer_npc_left_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walk_cultist_archer_npc_left_001.png"); _g_done_assets += 1
	verify("sprites/npc_e_cult_archers/elucidate_walk_cultist_archer_npc_left_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walk_cultist_archer_npc_left_002.png"); _g_done_assets += 1
	verify("sprites/npc_e_cult_archers/elucidate_idle_cultist_archer_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_cultist_archer_npc_right.png"); _g_done_assets += 1
	verify("sprites/npc_e_cult_archers/elucidate_walk_cultist_archer_npc_right_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walk_cultist_archer_npc_right_001.png"); _g_done_assets += 1
	verify("sprites/npc_e_cult_archers/elucidate_walk_cultist_archer_npc_right_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walk_cultist_archer_npc_right_002.png"); _g_done_assets += 1
	verify("sprites/npc_e_cult_archers/elucidate_idle_cultist_archer_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_cultist_archer_npc_up.png"); _g_done_assets += 1
	verify("sprites/npc_e_cult_archers/elucidate_walk_cultist_archer_npc_up_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walk_cultist_archer_npc_up_001.png"); _g_done_assets += 1
	verify("sprites/npc_e_cult_archers/elucidate_walk_cultist_archer_npc_up_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walk_cultist_archer_npc_up_002.png"); _g_done_assets += 1
	verify("sprites/npc_e_cult_eldritch_channelers/elucidate_idle_cultist_channeler_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_cultist_channeler_npc_down.png"); _g_done_assets += 1
	verify("sprites/npc_e_cult_eldritch_channelers/elucidate_walk_cultist_chaneller_npc_down_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walk_cultist_chaneller_npc_down_002.png"); _g_done_assets += 1
	verify("sprites/npc_e_cult_eldritch_channelers/elucidate_walk_cultist_chaneller_npc_down_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walk_cultist_chaneller_npc_down_001.png"); _g_done_assets += 1
	verify("sprites/npc_e_cult_eldritch_channelers/elucidate_idle_cultist_channeler_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_cultist_channeler_npc_right.png"); _g_done_assets += 1
	verify("sprites/npc_e_cult_eldritch_channelers/elucidate_walk_cultist_chaneller_npc_right_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walk_cultist_chaneller_npc_right_002.png"); _g_done_assets += 1
	verify("sprites/npc_e_cult_eldritch_channelers/elucidate_walk_cultist_chaneller_npc_right_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walk_cultist_chaneller_npc_right_001.png"); _g_done_assets += 1
	verify("sprites/npc_e_cult_eldritch_channelers/elucidate_idle_cultist_channeler_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_cultist_channeler_npc_left.png"); _g_done_assets += 1
	verify("sprites/npc_e_cult_eldritch_channelers/elucidate_walk_cultist_chaneller_npc_left_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walk_cultist_chaneller_npc_left_002.png"); _g_done_assets += 1
	verify("sprites/npc_e_cult_eldritch_channelers/elucidate_walk_cultist_chaneller_npc_left_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walk_cultist_chaneller_npc_left_001.png"); _g_done_assets += 1
	verify("sprites/npc_e_cult_eldritch_channelers/elucidate_idle_cultist_channeler_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_cultist_channeler_npc_up.png"); _g_done_assets += 1
	verify("sprites/npc_e_cult_eldritch_channelers/elucidate_walk_cultist_chaneller_npc_up_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walk_cultist_chaneller_npc_up_002.png"); _g_done_assets += 1
	verify("sprites/npc_e_cult_eldritch_channelers/elucidate_walk_cultist_chaneller_npc_up_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walk_cultist_chaneller_npc_up_001.png"); _g_done_assets += 1
	verify("sprites/npc_e_lunar_assasin/elucidate_idle_assassin_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_assassin_npc_down.png"); _g_done_assets += 1
	verify("sprites/npc_e_lunar_assasin/elucidate_walk_church_assassin_npc_down_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walk_church_assassin_npc_down_001.png"); _g_done_assets += 1
	verify("sprites/npc_e_lunar_assasin/elucidate_walk_church_assassin_npc_down_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walk_church_assassin_npc_down_002.png"); _g_done_assets += 1
	verify("sprites/npc_e_lunar_assasin/elucidate_idle_assassin_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_assassin_npc_left.png"); _g_done_assets += 1
	verify("sprites/npc_e_lunar_assasin/elucidate_walk_church_assassin_npc_left_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walk_church_assassin_npc_left_001.png"); _g_done_assets += 1
	verify("sprites/npc_e_lunar_assasin/elucidate_walk_church_assassin_npc_left_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walk_church_assassin_npc_left_002.png"); _g_done_assets += 1
	verify("sprites/npc_e_lunar_assasin/elucidate_idle_assassin_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_assassin_npc_right.png"); _g_done_assets += 1
	verify("sprites/npc_e_lunar_assasin/elucidate_walk_church_assassin_npc_right_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walk_church_assassin_npc_right_001.png"); _g_done_assets += 1
	verify("sprites/npc_e_lunar_assasin/elucidate_walk_church_assassin_npc_right_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walk_church_assassin_npc_right_002.png"); _g_done_assets += 1
	verify("sprites/npc_e_lunar_assasin/elucidate_idle_assassin_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_assassin_npc_up.png"); _g_done_assets += 1
	verify("sprites/npc_e_lunar_assasin/elucidate_walk_church_assassin_npc_up_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walk_church_assassin_npc_up_001.png"); _g_done_assets += 1
	verify("sprites/npc_e_lunar_assasin/elucidate_walk_church_assassin_npc_up_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walk_church_assassin_npc_up_002.png"); _g_done_assets += 1
	verify("sprites/elucidate_player_sprite_idle_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_player_sprite_idle_down.png"); _g_done_assets += 1
	verify("sprites/elucidate_player_sprite_walking_down_1.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_player_sprite_walking_down_1.png"); _g_done_assets += 1
	verify("sprites/elucidate_player_sprite_walking_down_2.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_player_sprite_walking_down_2.png"); _g_done_assets += 1
	verify("sprites/elucidate_player_sprite_attack_down_1.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_player_sprite_attack_down_1.png"); _g_done_assets += 1
	verify("sprites/elucidate_player_sprite_attack_down_2.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_player_sprite_attack_down_2.png"); _g_done_assets += 1
	verify("sprites/elucidate_player_sprite_idle_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_player_sprite_idle_right.png"); _g_done_assets += 1
	verify("sprites/elucidate_player_sprite_walking_right_1.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_player_sprite_walking_right_1.png"); _g_done_assets += 1
	verify("sprites/elucidate_player_sprite_walking_right_2.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_player_sprite_walking_right_2.png"); _g_done_assets += 1
	verify("sprites/elucidate_player_sprite_attack_right_1.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_player_sprite_attack_right_1.png"); _g_done_assets += 1
	verify("sprites/elucidate_player_sprite_attack_right_2.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_player_sprite_attack_right_2.png"); _g_done_assets += 1
	verify("sprites/elucidate_player_sprite_idle_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_player_sprite_idle_left.png"); _g_done_assets += 1
	verify("sprites/elucidate_player_sprite_walking_left_1.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_player_sprite_walking_left_1.png"); _g_done_assets += 1
	verify("sprites/elucidate_player_sprite_walking_left_2.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_player_sprite_walking_left_2.png"); _g_done_assets += 1
	verify("sprites/elucidate_player_sprite_attack_left_1.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_player_sprite_attack_left_1.png"); _g_done_assets += 1
	verify("sprites/elucidate_player_sprite_attack_left_2.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_player_sprite_attack_left_2.png"); _g_done_assets += 1
	verify("sprites/elucidate_player_sprite_idle_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_player_sprite_idle_up.png"); _g_done_assets += 1
	verify("sprites/elucidate_player_sprite_walking_up_1.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_player_sprite_walking_up_1.png"); _g_done_assets += 1
	verify("sprites/elucidate_player_sprite_walking_up_2.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_player_sprite_walking_up_2.png"); _g_done_assets += 1
	verify("sprites/elucidate_player_sprite_attack_up_1.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_player_sprite_attack_up_1.png"); _g_done_assets += 1
	verify("sprites/elucidate_player_sprite_attack_up_2.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_player_sprite_attack_up_2.png"); _g_done_assets += 1
	verify("images/elucidate_empty_bg_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_empty_bg_001.jpg"); _g_done_assets += 1
	verify("images/elucidate_floor_bg_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_floor_bg_001.png"); _g_done_assets += 1
	verify("images/elucidate_inventory.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_inventory.png"); _g_done_assets += 1
	verify("images/elucidate_map_long1.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_map_long1.png"); _g_done_assets += 1
	verify("images/elucidate_mcguy_portrait_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_mcguy_portrait_001.png"); _g_done_assets += 1
	verify("images/elucidate_bg_launcher_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_bg_launcher_001-2.png"); _g_done_assets += 1
	verify("images/elucidate_no_texture.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_no_texture.png"); _g_done_assets += 1
	verify("images/elucidate_play_bg.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_play_bg.png"); _g_done_assets += 1
	verify("images/elucidate_select.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_select.png"); _g_done_assets += 1
	verify("images/elucidate_select_background.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_select_background.png"); _g_done_assets += 1
	verify("images/elucidate_select_full.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_select_full.png"); _g_done_assets += 1
	verify("images/elucidate_show_selection.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_show_selection.png"); _g_done_assets += 1
	verify("images/elucidate_show_selection_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_show_selection_001.png"); _g_done_assets += 1
	verify("images/elucidate_show_selection_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_show_selection_002.png"); _g_done_assets += 1
	verify("images/elucidate_title.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_title.png"); _g_done_assets += 1
	verify("images/elucidate_user_elected_play.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_user_elected_play.png"); _g_done_assets += 1
	verify("images/elucidate_user_selection_bg.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_user_selection_bg.png"); _g_done_assets += 1
	verify("images/mercenary_portrait_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/mercenary_portrait_001.png"); _g_done_assets += 1
	verify("images/mercenary_portrait_001_full.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/mercenary_portrait_001_full.png"); _g_done_assets += 1
	verify("images/elucidate_bg_empty_room_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_bg_empty_room_001.png"); _g_done_assets += 1
	verify("images/elucidate_dungeon_grounds_bg_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_dungeon_grounds_bg_001.png"); _g_done_assets += 1
	verify("images/elucidate_silver_chest_closed_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_silver_chest_closed_001.png"); _g_done_assets += 1
	verify("images/elucidate_silver_chest_opened_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_silver_chest_opened_002.png"); _g_done_assets += 1
	verify("images/elucidate_gold_chest_closed_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_gold_chest_closed_003.png"); _g_done_assets += 1
	verify("images/elucidate_gold_chest_opened_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_gold_chest_opened_004.png"); _g_done_assets += 1
	verify("images/elucidate_bag_craft_inventory_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_bag_craft_inventory_001.png"); _g_done_assets += 1
	verify("images/elucidate_bag_craft_inventory_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_bag_craft_inventory_002.png"); _g_done_assets += 1
	verify("images/elucidate_bag_craft_inventory_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_bag_craft_inventory_003.png"); _g_done_assets += 1
	verify("images/elucidate_bag_craft_inventory_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_bag_craft_inventory_004.png"); _g_done_assets += 1
	verify("images/elucidate_bag_inventory_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_bag_inventory_001.png"); _g_done_assets += 1
	verify("images/elucidate_bag_inventory_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_bag_inventory_002.png"); _g_done_assets += 1
	verify("images/elucidate_bag_inventory_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_bag_inventory_003.png"); _g_done_assets += 1
	verify("images/elucidate_craft_only_inventory_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_craft_only_inventory_001.png"); _g_done_assets += 1
	verify("images/elucidate_craft_only_inventory_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_craft_only_inventory_002.png"); _g_done_assets += 1
	verify("images/elucidate_craft_only_inventory_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_craft_only_inventory_003.png"); _g_done_assets += 1
	verify("images/elucidate_craft_only_inventory_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_craft_only_inventory_004.png"); _g_done_assets += 1
	verify("images/elucidate_craft_only_inventory_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_craft_only_inventory_005.png"); _g_done_assets += 1
	verify("images/elucidate_dlc_inventory_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_dlc_inventory_001.png"); _g_done_assets += 1
	verify("images/elucidate_dlc_inventory_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_dlc_inventory_002.png"); _g_done_assets += 1
	verify("images/elucidate_dlc_inventory_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_dlc_inventory_003.png"); _g_done_assets += 1
	verify("images/elucidate_dlc_user_selected_play_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_dlc_user_selected_play_001.png"); _g_done_assets += 1
	verify("images/elucidate_dlc_user_selected_play_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_dlc_user_selected_play_002.png"); _g_done_assets += 1
	verify("images/elucidate_dlc_user_selected_play_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_dlc_user_selected_play_003.png"); _g_done_assets += 1
	verify("images/elucidate_dlc_user_selection_bg_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_dlc_user_selection_bg_001.png"); _g_done_assets += 1
	verify("images/elucidate_dlc_user_selection_bg_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_dlc_user_selection_bg_002.png"); _g_done_assets += 1
	verify("images/elucidate_dlc_user_selection_bg_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_dlc_user_selection_bg_003.png"); _g_done_assets += 1
	verify("images/elucidate_dlc_user_selection_bg_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_dlc_user_selection_bg_004.png"); _g_done_assets += 1
	verify("images/elucidate_dlc_user_selection_bg_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_dlc_user_selection_bg_005.png"); _g_done_assets += 1
	verify("images/elucidate_dlc_user_selection_bg_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_dlc_user_selection_bg_006.png"); _g_done_assets += 1
	verify("images/elucidate_enemy_attack_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_enemy_attack_001.png"); _g_done_assets += 1
	verify("images/elucidate_enemy_escape_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_enemy_escape_001.png"); _g_done_assets += 1
	verify("images/elucidate_enemy_escape_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_enemy_escape_002.png"); _g_done_assets += 1
	verify("images/elucidate_enemy_escape_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_enemy_escape_003.png"); _g_done_assets += 1
	verify("images/elucidate_enemy_interaction_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_enemy_interaction_001.png"); _g_done_assets += 1
	verify("images/elucidate_enemy_interaction_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_enemy_interaction_002.png"); _g_done_assets += 1
	verify("images/elucidate_enemy_interaction_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_enemy_interaction_003.png"); _g_done_assets += 1
	verify("images/elucidate_enemy_interaction_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_enemy_interaction_004.png"); _g_done_assets += 1
	verify("images/elucidate_enemy_interaction_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_enemy_interaction_005.png"); _g_done_assets += 1
	verify("images/elucidate_enemy_inventory_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_enemy_inventory_001.png"); _g_done_assets += 1
	verify("images/elucidate_enemy_skill_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_enemy_skill_001.png"); _g_done_assets += 1
	verify("images/elucidate_enemy_skill_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_enemy_skill_002.png"); _g_done_assets += 1
	verify("images/elucidate_enemy_skill_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_enemy_skill_003.png"); _g_done_assets += 1
	verify("images/elucidate_equipment_inventory_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_equipment_inventory_001.png"); _g_done_assets += 1
	verify("images/elucidate_equipment_inventory_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_equipment_inventory_002.png"); _g_done_assets += 1
	verify("images/elucidate_equipment_inventory_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_equipment_inventory_003.png"); _g_done_assets += 1
	verify("images/elucidate_full_text_portait_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_full_text_portait_001.png"); _g_done_assets += 1
	verify("images/elucidate_inventory_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_inventory_001.png"); _g_done_assets += 1
	verify("images/elucidate_inventory_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_inventory_002.png"); _g_done_assets += 1
	verify("images/elucidate_map_portait_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_map_portait_001.png"); _g_done_assets += 1
	verify("images/elucidate_map_portait_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_map_portait_002.png"); _g_done_assets += 1
	verify("images/elucidate_map_portait_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_map_portait_003.png"); _g_done_assets += 1
	verify("images/elucidate_map_portait_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_map_portait_004.png"); _g_done_assets += 1
	verify("images/elucidate_map_portait_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_map_portait_005.png"); _g_done_assets += 1
	verify("images/elucidate_map_portait_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_map_portait_006.png"); _g_done_assets += 1
	verify("images/elucidate_map_portait_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_map_portait_007.png"); _g_done_assets += 1
	verify("images/elucidate_map_portait_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_map_portait_008.png"); _g_done_assets += 1
	verify("images/elucidate_menu_bg_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_menu_bg_001-1.png"); _g_done_assets += 1
	verify("images/elucidate_menu_bg_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_menu_bg_002-1.png"); _g_done_assets += 1
	verify("images/elucidate_menu_bg_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_menu_bg_003-1.png"); _g_done_assets += 1
	verify("images/elucidate_menu_bg_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_menu_bg_004-1.png"); _g_done_assets += 1
	verify("images/elucidate_menu_bg_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_menu_bg_005-1.png"); _g_done_assets += 1
	verify("images/elucidate_menu_bg_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_menu_bg_006-1.png"); _g_done_assets += 1
	verify("images/elucidate_menu_bg_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_menu_bg_007-1.png"); _g_done_assets += 1
	verify("images/elucidate_menu_bg_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_menu_bg_008-1.png"); _g_done_assets += 1
	verify("images/elucidate_menu_bg_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_menu_bg_009-1.png"); _g_done_assets += 1
	verify("images/elucidate_menu_bg_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_menu_bg_010.png"); _g_done_assets += 1
	verify("images/elucidate_menu_bg_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_menu_bg_011.png"); _g_done_assets += 1
	verify("images/elucidate_mini_games_select_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_mini_games_select_001.png"); _g_done_assets += 1
	verify("images/elucidate_mini_games_select_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_mini_games_select_002.png"); _g_done_assets += 1
	verify("images/elucidate_mini_games_select_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_mini_games_select_003.png"); _g_done_assets += 1
	verify("images/elucidate_mini_games_select_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_mini_games_select_004.png"); _g_done_assets += 1
	verify("images/elucidate_mini_games_select_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_mini_games_select_005.png"); _g_done_assets += 1
	verify("images/elucidate_mini_games_select_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_mini_games_select_006.png"); _g_done_assets += 1
	verify("images/elucidate_mini_games_select_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_mini_games_select_007.png"); _g_done_assets += 1
	verify("images/elucidate_mini_games_select_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_mini_games_select_008.png"); _g_done_assets += 1
	verify("images/elucidate_mini_games_select_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_mini_games_select_009.png"); _g_done_assets += 1
	verify("images/elucidate_mini_games_select_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_mini_games_select_010.png"); _g_done_assets += 1
	verify("images/elucidate_mini_games_select_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_mini_games_select_011.png"); _g_done_assets += 1
	verify("images/elucidate_mini_games_select_012.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_mini_games_select_012.png"); _g_done_assets += 1
	verify("images/elucidate_mini_games_select_013.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_mini_games_select_013.png"); _g_done_assets += 1
	verify("images/elucidate_mini_games_select_014.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_mini_games_select_014.png"); _g_done_assets += 1
	verify("images/elucidate_mini_games_select_015.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_mini_games_select_015.png"); _g_done_assets += 1
	verify("images/elucidate_mini_games_select_016.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_mini_games_select_016.png"); _g_done_assets += 1
	verify("images/elucidate_no_texture_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_no_texture_001.png"); _g_done_assets += 1
	verify("images/elucidate_play_bg.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_play_bg.png"); _g_done_assets += 1
	verify("images/elucidate_select_background.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_select_background.png"); _g_done_assets += 1
	verify("images/elucidate_show_selection_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_show_selection_001.png"); _g_done_assets += 1
	verify("images/elucidate_show_selection_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_show_selection_002.png"); _g_done_assets += 1
	verify("images/elucidate_user_selected_play_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_user_selected_play_001.png"); _g_done_assets += 1
	verify("images/elucidate_user_selected_play_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_user_selected_play_002.png"); _g_done_assets += 1
	verify("images/elucidate_user_selection_bg_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_user_selection_bg_001.png"); _g_done_assets += 1
	verify("images/elucidate_user_selection_bg_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_user_selection_bg_002.png"); _g_done_assets += 1
	verify("images/elucidate_user_selection_bg_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_user_selection_bg_003.png"); _g_done_assets += 1
	verify("images/elucidate_version_select_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_version_select_001.png"); _g_done_assets += 1
	verify("images/elucidate_version_select_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_version_select_002.png"); _g_done_assets += 1
	verify("images/elucidate_version_select_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_version_select_003.png"); _g_done_assets += 1
	verify("images/elucidate_version_select_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_version_select_004.png"); _g_done_assets += 1
	verify("images/elucidate_version_select_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_version_select_005.png"); _g_done_assets += 1
	verify("images/elucidate_left_gradient_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_left_gradient_001.png"); _g_done_assets += 1
	verify("images/elucidate_left_purple_gradient_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_left_purple_gradient_001.png"); _g_done_assets += 1
	verify("images/elucidate_middle_gradient_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_middle_gradient_001.png"); _g_done_assets += 1
	verify("images/elucidate_middle_purple_gradient_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_middle_purple_gradient_001.png"); _g_done_assets += 1
	verify("images/elucidate_middle_purple_gradient_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_middle_purple_gradient_002.png"); _g_done_assets += 1
	verify("images/elucidate_right_gradient_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_right_gradient_001.png"); _g_done_assets += 1
	verify("images/elucidate_right_purple_gradient_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_right_purple_gradient_001.png"); _g_done_assets += 1
	verify("images/walled_mercenary_with_draft_officer_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_mercenary_with_draft_officer_001.png"); _g_done_assets += 1
	verify("images/walled_mercenary_with_draft_officer_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_mercenary_with_draft_officer_002.png"); _g_done_assets += 1
	verify("images/walled_mercenary_with_draft_officer_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_mercenary_with_draft_officer_003.png"); _g_done_assets += 1
	verify("images/walled_mercenary_with_draft_officer_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_mercenary_with_draft_officer_004.png"); _g_done_assets += 1
	verify("images/walled_mercenary_with_draft_officer_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_mercenary_with_draft_officer_005.png"); _g_done_assets += 1
	verify("images/walled_mercenary_with_draft_officer_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_mercenary_with_draft_officer_006.png"); _g_done_assets += 1
	verify("images/walled_mercenary_with_draft_officer_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_mercenary_with_draft_officer_007.png"); _g_done_assets += 1
	verify("images/walled_mercenary_with_draft_officer_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_mercenary_with_draft_officer_008.png"); _g_done_assets += 1
	verify("images/walled_mercenary_with_blacksmith_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_mercenary_with_blacksmith_001.png"); _g_done_assets += 1
	verify("images/walled_mercenary_with_blacksmith_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_mercenary_with_blacksmith_002.png"); _g_done_assets += 1
	verify("images/walled_mercenary_with_blacksmith_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_mercenary_with_blacksmith_003.png"); _g_done_assets += 1
	verify("images/walled_mercenary_with_blacksmith_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_mercenary_with_blacksmith_004.png"); _g_done_assets += 1
	verify("images/walled_mercenary_with_blacksmith_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_mercenary_with_blacksmith_005.png"); _g_done_assets += 1
	verify("images/walled_mercenary_with_blacksmith_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_mercenary_with_blacksmith_006.png"); _g_done_assets += 1
	verify("images/walled_mercenary_with_blacksmith_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_mercenary_with_blacksmith_007.png"); _g_done_assets += 1
	verify("images/walled_mercenary_with_blacksmith_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_mercenary_with_blacksmith_008.png"); _g_done_assets += 1
	verify("images/walled_mercenary_with_blacksmith_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_mercenary_with_blacksmith_009.png"); _g_done_assets += 1
	verify("images/walled_mercenary_with_blacksmith_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_mercenary_with_blacksmith_010.png"); _g_done_assets += 1
	verify("images/walled_mercenary_with_blacksmith_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_mercenary_with_blacksmith_011.png"); _g_done_assets += 1
	verify("images/walled_mercenary_with_blacksmith_012.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_mercenary_with_blacksmith_012.png"); _g_done_assets += 1
	verify("images/walled_mercenary_with_blacksmith_013.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_mercenary_with_blacksmith_013.png"); _g_done_assets += 1
	verify("images/walled_mercenary_with_blacksmith_014.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_mercenary_with_blacksmith_014.png"); _g_done_assets += 1
	verify("images/walled_mercenary_poster_interact_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_mercenary_poster_interact_001.png"); _g_done_assets += 1
	verify("images/walled_mercenary_poster_interact_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_mercenary_poster_interact_002.png"); _g_done_assets += 1
	verify("images/walled_mercenary_poster_interact_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_mercenary_poster_interact_003.png"); _g_done_assets += 1
	verify("images/theocratic_mercenary_with_priest_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_priest_001.png"); _g_done_assets += 1
	verify("images/theocratic_mercenary_with_priest_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_priest_002.png"); _g_done_assets += 1
	verify("images/theocratic_mercenary_with_priest_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_priest_003.png"); _g_done_assets += 1
	verify("images/theocratic_mercenary_with_priest_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_priest_004.png"); _g_done_assets += 1
	verify("images/theocratic_mercenary_with_priest_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_priest_005.png"); _g_done_assets += 1
	verify("images/theocratic_mercenary_with_priest_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_priest_006.png"); _g_done_assets += 1
	verify("images/theocratic_mercenary_with_priest_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_priest_007.png"); _g_done_assets += 1
	verify("images/theocratic_mercenary_with_priest_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_priest_008.png"); _g_done_assets += 1
	verify("images/theocratic_mercenary_with_priest_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_priest_009.png"); _g_done_assets += 1
	verify("images/theocratic_mercenary_with_priest_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_priest_010.png"); _g_done_assets += 1
	verify("images/theocratic_mercenary_with_priest_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_priest_011.png"); _g_done_assets += 1
	verify("images/theocratic_mercenary_with_priest_012.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_priest_012.png"); _g_done_assets += 1
	verify("images/theocratic_mercenary_with_priest_013.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_priest_013.png"); _g_done_assets += 1
	verify("images/theocratic_mercenary_with_priest_014.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_priest_014.png"); _g_done_assets += 1
	verify("images/theocratic_mercenary_with_priest_015.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_priest_015.png"); _g_done_assets += 1
	verify("images/theocratic_mercenary_with_priest_016.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_priest_016.png"); _g_done_assets += 1
	verify("images/theocratic_mercenary_with_priest_017.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_priest_017.png"); _g_done_assets += 1
	verify("images/theocratic_mercenary_with_priest_018.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_priest_018.png"); _g_done_assets += 1
	verify("images/theocratic_mercenary_with_priest_019.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_priest_019.png"); _g_done_assets += 1
	verify("images/theocratic_mercenary_with_priest_020.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_priest_020.png"); _g_done_assets += 1
	verify("images/theocratic_mercenary_with_priest_021.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_priest_021.png"); _g_done_assets += 1
	verify("images/theocratic_mercenary_with_priest_022.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_priest_022.png"); _g_done_assets += 1
	verify("images/theocratic_mercenary_with_priest_023.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_priest_023.png"); _g_done_assets += 1
	verify("images/theocratic_mercenary_with_priest_024.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_priest_024.png"); _g_done_assets += 1
	verify("images/theocratic_mercenary_with_priest_025.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_priest_025.png"); _g_done_assets += 1
	verify("images/theocratic_mercenary_with_priest_026.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_priest_026.png"); _g_done_assets += 1
	verify("images/theocratic_mercenary_with_priest_027.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_priest_027.png"); _g_done_assets += 1
	verify("images/theocratic_mercenary_with_priest_028.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_priest_028.png"); _g_done_assets += 1
	verify("images/theocratic_mercenary_with_librarian_scholar_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_librarian_scholar_001.png"); _g_done_assets += 1
	verify("images/theocratic_mercenary_with_librarian_scholar_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_librarian_scholar_002.png"); _g_done_assets += 1
	verify("images/theocratic_mercenary_with_librarian_scholar_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_librarian_scholar_003.png"); _g_done_assets += 1
	verify("images/theocratic_mercenary_with_librarian_scholar_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_librarian_scholar_004.png"); _g_done_assets += 1
	verify("images/theocratic_mercenary_with_librarian_scholar_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_librarian_scholar_005.png"); _g_done_assets += 1
	verify("images/theocratic_mercenary_with_librarian_scholar_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_librarian_scholar_006.png"); _g_done_assets += 1
	verify("images/theocratic_mercenary_with_librarian_scholar_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_librarian_scholar_007.png"); _g_done_assets += 1
	verify("images/theocratic_mercenary_with_librarian_scholar_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_librarian_scholar_008.png"); _g_done_assets += 1
	verify("images/theocratic_mercenary_with_librarian_scholar_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_librarian_scholar_009.png"); _g_done_assets += 1
	verify("images/theocratic_mercenary_with_librarian_scholar_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_librarian_scholar_010.png"); _g_done_assets += 1
	verify("images/theocratic_mercenary_with_librarian_scholar_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_librarian_scholar_011.png"); _g_done_assets += 1
	verify("images/theocratic_mercenary_with_librarian_scholar_012.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_librarian_scholar_012.png"); _g_done_assets += 1
	verify("images/theocratic_mercenary_with_librarian_scholar_013.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_librarian_scholar_013.png"); _g_done_assets += 1
	verify("images/theocratic_mercenary_with_librarian_scholar_014.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_librarian_scholar_014.png"); _g_done_assets += 1
	verify("images/theocratic_mercenary_with_librarian_scholar_015.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_librarian_scholar_015.png"); _g_done_assets += 1
	verify("images/theocratic_mercenary_with_librarian_scholar_016.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_librarian_scholar_016.png"); _g_done_assets += 1
	verify("images/theocratic_mercenary_with_confession_booth_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_confession_booth_001.png"); _g_done_assets += 1
	verify("images/theocratic_mercenary_with_confession_booth_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_confession_booth_002.png"); _g_done_assets += 1
	verify("images/theocratic_mercenary_with_confession_booth_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_confession_booth_003.png"); _g_done_assets += 1
	verify("images/theocratic_mercenary_with_confession_booth_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_confession_booth_004.png"); _g_done_assets += 1
	verify("images/theocratic_mercenary_with_confession_booth_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_confession_booth_005.png"); _g_done_assets += 1
	verify("images/theocratic_mercenary_with_confession_booth_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_confession_booth_006.png"); _g_done_assets += 1
	verify("images/theocratic_battle_mercenary_with_priest_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_mercenary_with_priest_001.png"); _g_done_assets += 1
	verify("images/theocratic_battle_mercenary_with_priest_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_mercenary_with_priest_002.png"); _g_done_assets += 1
	verify("images/theocratic_battle_mercenary_with_priest_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_mercenary_with_priest_003.png"); _g_done_assets += 1
	verify("images/theocratic_battle_mercenary_with_priest_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_mercenary_with_priest_004.png"); _g_done_assets += 1
	verify("images/theocratic_battle_mercenary_with_priest_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_mercenary_with_priest_005.png"); _g_done_assets += 1
	verify("images/theocratic_battle_mercenary_with_priest_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_mercenary_with_priest_006.png"); _g_done_assets += 1
	verify("images/theocratic_battle_mercenary_with_priest_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_mercenary_with_priest_007.png"); _g_done_assets += 1
	verify("images/theocratic_battle_mercenary_with_priest_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_mercenary_with_priest_008.png"); _g_done_assets += 1
	verify("images/theocratic_battle_mercenary_with_priest_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_mercenary_with_priest_009.png"); _g_done_assets += 1
	verify("images/theocratic_battle_mercenary_with_priest_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_mercenary_with_priest_010.png"); _g_done_assets += 1
	verify("images/theocratic_battle_mercenary_with_priest_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_mercenary_with_priest_011.png"); _g_done_assets += 1
	verify("images/theocratic_battle_mercenary_with_priest_012.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_mercenary_with_priest_012.png"); _g_done_assets += 1
	verify("images/theocratic_battle_mercenary_with_priest_013.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_mercenary_with_priest_013.png"); _g_done_assets += 1
	verify("images/theocratic_battle_mercenary_with_priest_014.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_mercenary_with_priest_014.png"); _g_done_assets += 1
	verify("images/theocratic_battle_mercenary_with_priest_015.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_mercenary_with_priest_015.png"); _g_done_assets += 1
	verify("images/theocratic_battle_mercenary_with_priest_016.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_mercenary_with_priest_016.png"); _g_done_assets += 1
	verify("images/theocratic_battle_mercenary_with_priest_017.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_mercenary_with_priest_017.png"); _g_done_assets += 1
	verify("images/theocratic_battle_mercenary_with_priest_018.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_mercenary_with_priest_018.png"); _g_done_assets += 1
	verify("images/theocratic_battle_mercenary_with_priest_019.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_mercenary_with_priest_019.png"); _g_done_assets += 1
	verify("images/theocratic_battle_mercenary_with_priest_020.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_mercenary_with_priest_020.png"); _g_done_assets += 1
	verify("images/theocratic_battle_mercenary_with_priest_021.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_mercenary_with_priest_021.png"); _g_done_assets += 1
	verify("images/theocratic_battle_mercenary_with_priest_022.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_mercenary_with_priest_022.png"); _g_done_assets += 1
	verify("images/theocratic_battle_mercenary_with_priest_023.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_mercenary_with_priest_023.png"); _g_done_assets += 1
	verify("images/theocratic_battle_mercenary_with_priest_024.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_mercenary_with_priest_024.png"); _g_done_assets += 1
	verify("images/theocratic_battle_mercenary_with_priest_025.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_mercenary_with_priest_025.png"); _g_done_assets += 1
	verify("images/theocratic_battle_mercenary_with_priest_026.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_mercenary_with_priest_026.png"); _g_done_assets += 1
	verify("images/theocratic_battle_mercenary_with_priest_027.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_mercenary_with_priest_027.png"); _g_done_assets += 1
	verify("images/theocratic_battle_mercenary_with_priest_028.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_mercenary_with_priest_028.png"); _g_done_assets += 1
	verify("images/theocratic_battle_mercenary_with_priest_029.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_mercenary_with_priest_029.png"); _g_done_assets += 1
	verify("images/theocratic_battle_mercenary_with_priest_030.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_mercenary_with_priest_030.png"); _g_done_assets += 1
	verify("images/home_village_mercenary_with_memory_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_mercenary_with_memory_001.png"); _g_done_assets += 1
	verify("images/home_village_mercenary_with_memory_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_mercenary_with_memory_002.png"); _g_done_assets += 1
	verify("images/home_village_mercenary_with_memory_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_mercenary_with_memory_003.png"); _g_done_assets += 1
	verify("images/home_village_mercenary_with_memory_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_mercenary_with_memory_004.png"); _g_done_assets += 1
	verify("images/home_village_mercenary_with_memory_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_mercenary_with_memory_005.png"); _g_done_assets += 1
	verify("images/home_village_mercenary_with_memory_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_mercenary_with_memory_006.png"); _g_done_assets += 1
	verify("images/home_village_mercenary_with_memory_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_mercenary_with_memory_007.png"); _g_done_assets += 1
	verify("images/home_village_mercenary_with_memory_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_mercenary_with_memory_008.png"); _g_done_assets += 1
	verify("images/home_village_mercenary_with_memory_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_mercenary_with_memory_009.png"); _g_done_assets += 1
	verify("images/home_village_mercenary_with_memory_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_mercenary_with_memory_010.png"); _g_done_assets += 1
	verify("images/home_village_mercenary_with_memory_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_mercenary_with_memory_011.png"); _g_done_assets += 1
	verify("images/home_village_mercenary_with_memory_012.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_mercenary_with_memory_012.png"); _g_done_assets += 1
	verify("images/home_village_mercenary_with_memory_013.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_mercenary_with_memory_013.png"); _g_done_assets += 1
	verify("images/home_village_mercenary_with_memory_014.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_mercenary_with_memory_014.png"); _g_done_assets += 1
	verify("images/home_village_mercenary_with_memory_015.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_mercenary_with_memory_015.png"); _g_done_assets += 1
	verify("images/home_village_mercenary_with_memory_016.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_mercenary_with_memory_016.png"); _g_done_assets += 1
	verify("images/home_village_mercenary_with_memory_017.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_mercenary_with_memory_017.png"); _g_done_assets += 1
	verify("images/home_village_mercenary_with_memory_018.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_mercenary_with_memory_018.png"); _g_done_assets += 1
	verify("images/home_village_mercenary_with_memory_019.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_mercenary_with_memory_019.png"); _g_done_assets += 1
	verify("images/home_village_mercenary_with_memory_020.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_mercenary_with_memory_020.png"); _g_done_assets += 1
	verify("images/home_village_mercenary_with_memory_021.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_mercenary_with_memory_021.png"); _g_done_assets += 1
	verify("images/home_village_mercenary_with_memory_022.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_mercenary_with_memory_022.png"); _g_done_assets += 1
	verify("images/home_village_mercenary_with_memory_023.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_mercenary_with_memory_023.png"); _g_done_assets += 1
	verify("images/home_village_mercenary_with_memory_024.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_mercenary_with_memory_024.png"); _g_done_assets += 1
	verify("images/home_village_mercenary_with_memory_025.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_mercenary_with_memory_025.png"); _g_done_assets += 1
	verify("images/home_village_mercenary_with_memory_026.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_mercenary_with_memory_026.png"); _g_done_assets += 1
	verify("images/home_village_mercenary_with_memory_027.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_mercenary_with_memory_027.png"); _g_done_assets += 1
	verify("images/outskirts_village_mercenary_with_village_chief_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_village_chief_001.png"); _g_done_assets += 1
	verify("images/outskirts_village_mercenary_with_village_chief_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_village_chief_002.png"); _g_done_assets += 1
	verify("images/outskirts_village_mercenary_with_village_chief_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_village_chief_003.png"); _g_done_assets += 1
	verify("images/outskirts_village_mercenary_with_village_chief_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_village_chief_004.png"); _g_done_assets += 1
	verify("images/outskirts_village_mercenary_with_village_chief_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_village_chief_005.png"); _g_done_assets += 1
	verify("images/outskirts_village_mercenary_with_village_chief_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_village_chief_006.png"); _g_done_assets += 1
	verify("images/outskirts_village_mercenary_with_village_chief_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_village_chief_007.png"); _g_done_assets += 1
	verify("images/outskirts_village_mercenary_with_village_chief_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_village_chief_008.png"); _g_done_assets += 1
	verify("images/outskirts_village_mercenary_with_village_chief_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_village_chief_009.png"); _g_done_assets += 1
	verify("images/outskirts_village_mercenary_with_village_chief_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_village_chief_010.png"); _g_done_assets += 1
	verify("images/outskirts_village_mercenary_with_village_chief_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_village_chief_011.png"); _g_done_assets += 1
	verify("images/outskirts_market_mercenary_with_village_market_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_market_mercenary_with_village_market_001.png"); _g_done_assets += 1
	verify("images/outskirts_market_mercenary_with_village_market_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_market_mercenary_with_village_market_002.png"); _g_done_assets += 1
	verify("images/outskirts_market_mercenary_with_village_market_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_market_mercenary_with_village_market_003.png"); _g_done_assets += 1
	verify("images/outskirts_market_mercenary_with_village_market_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_market_mercenary_with_village_market_004.png"); _g_done_assets += 1
	verify("images/outskirts_market_mercenary_with_village_market_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_market_mercenary_with_village_market_005.png"); _g_done_assets += 1
	verify("images/outskirts_market_mercenary_with_village_market_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_market_mercenary_with_village_market_006.png"); _g_done_assets += 1
	verify("images/outskirts_market_mercenary_with_village_market_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_market_mercenary_with_village_market_007.png"); _g_done_assets += 1
	verify("images/outskirts_market_mercenary_with_village_market_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_market_mercenary_with_village_market_008.png"); _g_done_assets += 1
	verify("images/outskirts_village_mercenary_with_villagers_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_villagers_001.png"); _g_done_assets += 1
	verify("images/outskirts_village_mercenary_with_villagers_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_villagers_002.png"); _g_done_assets += 1
	verify("images/outskirts_village_mercenary_with_villagers_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_villagers_003.png"); _g_done_assets += 1
	verify("images/outskirts_village_mercenary_with_villagers_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_villagers_004.png"); _g_done_assets += 1
	verify("images/outskirts_village_mercenary_with_villagers_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_villagers_005.png"); _g_done_assets += 1
	verify("images/outskirts_village_mercenary_with_villagers_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_villagers_006.png"); _g_done_assets += 1
	verify("images/outskirts_village_mercenary_with_travelling_bard_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_travelling_bard_001.png"); _g_done_assets += 1
	verify("images/outskirts_village_mercenary_with_travelling_bard_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_travelling_bard_002.png"); _g_done_assets += 1
	verify("images/outskirts_village_mercenary_with_travelling_bard_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_travelling_bard_003.png"); _g_done_assets += 1
	verify("images/outskirts_village_mercenary_with_travelling_bard_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_travelling_bard_004.png"); _g_done_assets += 1
	verify("images/outskirts_village_mercenary_with_travelling_bard_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_travelling_bard_005.png"); _g_done_assets += 1
	verify("images/outskirts_village_mercenary_with_travelling_bard_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_travelling_bard_006.png"); _g_done_assets += 1
	verify("images/outskirts_village_mercenary_with_travelling_bard_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_travelling_bard_007.png"); _g_done_assets += 1
	verify("images/outskirts_village_mercenary_with_travelling_bard_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_travelling_bard_008.png"); _g_done_assets += 1
	verify("images/outskirts_village_mercenary_with_travelling_bard_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_travelling_bard_009.png"); _g_done_assets += 1
	verify("images/outskirts_village_mercenary_with_travelling_bard_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_travelling_bard_010.png"); _g_done_assets += 1
	verify("images/outskirts_village_mercenary_with_travelling_bard_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_travelling_bard_011.png"); _g_done_assets += 1
	verify("images/outskirts_village_mercenary_with_travelling_bard_012.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_travelling_bard_012.png"); _g_done_assets += 1
	verify("images/outskirts_village_mercenary_with_travelling_bard_013.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_travelling_bard_013.png"); _g_done_assets += 1
	verify("images/outskirts_village_mercenary_with_travelling_bard_014.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_travelling_bard_014.png"); _g_done_assets += 1
	verify("images/outskirts_village_mercenary_with_travelling_bard_015.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_travelling_bard_015.png"); _g_done_assets += 1
	verify("images/outskirts_village_mercenary_with_travelling_bard_016.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_travelling_bard_016.png"); _g_done_assets += 1
	verify("images/outskirts_village_mercenary_with_travelling_bard_017.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_travelling_bard_017.png"); _g_done_assets += 1
	verify("images/outskirts_village_mercenary_with_travelling_bard_018.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_travelling_bard_018.png"); _g_done_assets += 1
	verify("images/outskirts_village_mercenary_with_travelling_bard_019.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_travelling_bard_019.png"); _g_done_assets += 1
	verify("images/outskirts_village_mercenary_with_travelling_bard_020.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_travelling_bard_020.png"); _g_done_assets += 1
	verify("images/outskirts_village_mercenary_with_travelling_bard_021.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_travelling_bard_021.png"); _g_done_assets += 1
	verify("images/zone_terror_mercenary_to_himself_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_mercenary_to_himself_001.png"); _g_done_assets += 1
	verify("images/zone_terror_mercenary_to_himself_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_mercenary_to_himself_002.png"); _g_done_assets += 1
	verify("images/zone_terror_mercenary_to_himself_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_mercenary_to_himself_003.png"); _g_done_assets += 1
	verify("images/zone_terror_mercenary_to_himself_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_mercenary_to_himself_004.png"); _g_done_assets += 1
	verify("images/zone_terror_mercenary_to_himself_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_mercenary_to_himself_005.png"); _g_done_assets += 1
	verify("images/tribe_perimeter_mercenary_with_tribe_elder_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_perimeter_mercenary_with_tribe_elder_001.png"); _g_done_assets += 1
	verify("images/tribe_perimeter_mercenary_with_tribe_elder_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_perimeter_mercenary_with_tribe_elder_002.png"); _g_done_assets += 1
	verify("images/tribe_perimeter_mercenary_with_tribe_elder_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_perimeter_mercenary_with_tribe_elder_003.png"); _g_done_assets += 1
	verify("images/tribe_perimeter_mercenary_with_tribe_elder_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_perimeter_mercenary_with_tribe_elder_004.png"); _g_done_assets += 1
	verify("images/tribe_perimeter_mercenary_with_tribe_elder_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_perimeter_mercenary_with_tribe_elder_005.png"); _g_done_assets += 1
	verify("images/tribe_perimeter_mercenary_with_tribe_elder_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_perimeter_mercenary_with_tribe_elder_006.png"); _g_done_assets += 1
	verify("images/tribe_perimeter_mercenary_with_tribe_elder_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_perimeter_mercenary_with_tribe_elder_007.png"); _g_done_assets += 1
	verify("images/tribe_perimeter_mercenary_with_tribe_elder_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_perimeter_mercenary_with_tribe_elder_008.png"); _g_done_assets += 1
	verify("images/tribe_perimeter_mercenary_with_tribe_elder_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_perimeter_mercenary_with_tribe_elder_009.png"); _g_done_assets += 1
	verify("images/tribe_perimeter_mercenary_with_tribe_elder_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_perimeter_mercenary_with_tribe_elder_010.png"); _g_done_assets += 1
	verify("images/tribe_perimeter_mercenary_with_tribe_elder_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_perimeter_mercenary_with_tribe_elder_011.png"); _g_done_assets += 1
	verify("images/tribe_perimeter_mercenary_with_tribe_elder_012.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_perimeter_mercenary_with_tribe_elder_012.png"); _g_done_assets += 1
	verify("images/tribe_perimeter_warrior_with_assassin_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_perimeter_warrior_with_assassin_001.png"); _g_done_assets += 1
	verify("images/tribe_perimeter_warrior_with_assassin_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_perimeter_warrior_with_assassin_002.png"); _g_done_assets += 1
	verify("images/tribe_perimeter_warrior_with_assassin_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_perimeter_warrior_with_assassin_003.png"); _g_done_assets += 1
	verify("images/tribe_perimeter_warrior_with_assassin_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_perimeter_warrior_with_assassin_004.png"); _g_done_assets += 1
	verify("images/tribe_perimeter_warrior_with_assassin_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_perimeter_warrior_with_assassin_005.png"); _g_done_assets += 1
	verify("images/tribe_storage_mercenary_with_shaman_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_mercenary_with_shaman_001.png"); _g_done_assets += 1
	verify("images/tribe_storage_mercenary_with_shaman_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_mercenary_with_shaman_002.png"); _g_done_assets += 1
	verify("images/tribe_storage_mercenary_with_shaman_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_mercenary_with_shaman_003.png"); _g_done_assets += 1
	verify("images/tribe_storage_mercenary_with_shaman_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_mercenary_with_shaman_004.png"); _g_done_assets += 1
	verify("images/tribe_storage_mercenary_with_shaman_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_mercenary_with_shaman_005.png"); _g_done_assets += 1
	verify("images/tribe_storage_mercenary_with_shaman_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_mercenary_with_shaman_006.png"); _g_done_assets += 1
	verify("images/tribe_storage_mercenary_with_shaman_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_mercenary_with_shaman_007.png"); _g_done_assets += 1
	verify("images/tribe_storage_mercenary_with_shaman_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_mercenary_with_shaman_008.png"); _g_done_assets += 1
	verify("images/tribe_storage_mercenary_with_shaman_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_mercenary_with_shaman_009.png"); _g_done_assets += 1
	verify("images/tribe_storage_mercenary_with_shaman_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_mercenary_with_shaman_010.png"); _g_done_assets += 1
	verify("images/tribe_storage_mercenary_with_shaman_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_mercenary_with_shaman_011.png"); _g_done_assets += 1
	verify("images/tribe_storage_mercenary_with_shaman_012.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_mercenary_with_shaman_012.png"); _g_done_assets += 1
	verify("images/tribe_storage_mercenary_with_shaman_013.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_mercenary_with_shaman_013.png"); _g_done_assets += 1
	verify("images/tribe_storage_mercenary_with_shaman_014.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_mercenary_with_shaman_014.png"); _g_done_assets += 1
	verify("images/tribe_storage_mercenary_with_shaman_015.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_mercenary_with_shaman_015.png"); _g_done_assets += 1
	verify("images/tribe_storage_mercenary_with_shaman_016.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_mercenary_with_shaman_016.png"); _g_done_assets += 1
	verify("images/tribe_storage_mercenary_with_shaman_017.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_mercenary_with_shaman_017.png"); _g_done_assets += 1
	verify("images/tribe_storage_mercenary_with_shaman_018.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_mercenary_with_shaman_018.png"); _g_done_assets += 1
	verify("images/tribe_storage_mercenary_with_shaman_019.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_mercenary_with_shaman_019.png"); _g_done_assets += 1
	verify("images/tribe_storage_mercenary_with_shaman_020.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_mercenary_with_shaman_020.png"); _g_done_assets += 1
	verify("images/tribe_storage_mercenary_with_shaman_021.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_mercenary_with_shaman_021.png"); _g_done_assets += 1
	verify("images/tribe_storage_mercenary_with_shaman_022.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_mercenary_with_shaman_022.png"); _g_done_assets += 1
	verify("images/tribe_tunnel_mercenary_with_tibe_chief_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_tunnel_mercenary_with_tibe_chief_001.png"); _g_done_assets += 1
	verify("images/tribe_tunnel_mercenary_with_tibe_chief_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_tunnel_mercenary_with_tibe_chief_002.png"); _g_done_assets += 1
	verify("images/tribe_tunnel_mercenary_with_tibe_chief_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_tunnel_mercenary_with_tibe_chief_003.png"); _g_done_assets += 1
	verify("images/tribe_tunnel_mercenary_with_tibe_chief_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_tunnel_mercenary_with_tibe_chief_004.png"); _g_done_assets += 1
	verify("images/tribe_tunnel_mercenary_with_tibe_chief_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_tunnel_mercenary_with_tibe_chief_005.png"); _g_done_assets += 1
	verify("images/zone_terror_mercenary_with_shaman_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_mercenary_with_shaman_001.png"); _g_done_assets += 1
	verify("images/zone_terror_mercenary_with_shaman_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_mercenary_with_shaman_002.png"); _g_done_assets += 1
	verify("images/zone_terror_mercenary_with_shaman_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_mercenary_with_shaman_003.png"); _g_done_assets += 1
	verify("images/zone_terror_mercenary_with_shaman_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_mercenary_with_shaman_004.png"); _g_done_assets += 1
	verify("images/zone_terror_mercenary_with_shaman_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_mercenary_with_shaman_005.png"); _g_done_assets += 1
	verify("images/zone_terror_mercenary_with_shaman_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_mercenary_with_shaman_006.png"); _g_done_assets += 1
	verify("images/zone_terror_mercenary_with_shaman_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_mercenary_with_shaman_007.png"); _g_done_assets += 1
	verify("images/zone_terror_mercenary_with_shaman_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_mercenary_with_shaman_008.png"); _g_done_assets += 1
	verify("images/zone_terror_mercenary_with_shaman_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_mercenary_with_shaman_009.png"); _g_done_assets += 1
	verify("images/zone_terror_mercenary_with_shaman_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_mercenary_with_shaman_010.png"); _g_done_assets += 1
	verify("images/zone_terror_mercenary_with_shaman_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_mercenary_with_shaman_011.png"); _g_done_assets += 1
	verify("images/zone_terror_mercenary_with_shaman_012.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_mercenary_with_shaman_012.png"); _g_done_assets += 1
	verify("images/zone_terror_mercenary_with_shaman_013.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_mercenary_with_shaman_013.png"); _g_done_assets += 1
	verify("images/zone_terror_mercenary_with_shaman_014.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_mercenary_with_shaman_014.png"); _g_done_assets += 1
	verify("images/zone_terror_mercenary_with_shaman_015.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_mercenary_with_shaman_015.png"); _g_done_assets += 1
	verify("images/zone_terror_mercenary_with_shaman_016.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_mercenary_with_shaman_016.png"); _g_done_assets += 1
	verify("images/zone_terror_mercenary_with_shaman_017.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_mercenary_with_shaman_017.png"); _g_done_assets += 1
	verify("images/port_city_mercenary_with_merchant_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_001.png"); _g_done_assets += 1
	verify("images/port_city_mercenary_with_merchant_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_002.png"); _g_done_assets += 1
	verify("images/port_city_mercenary_with_merchant_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_003.png"); _g_done_assets += 1
	verify("images/port_city_mercenary_with_merchant_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_004.png"); _g_done_assets += 1
	verify("images/port_city_mercenary_with_merchant_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_005.png"); _g_done_assets += 1
	verify("images/port_city_mercenary_with_merchant_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_006.png"); _g_done_assets += 1
	verify("images/port_city_mercenary_with_merchant_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_007.png"); _g_done_assets += 1
	verify("images/port_city_mercenary_with_merchant_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_008.png"); _g_done_assets += 1
	verify("images/port_city_mercenary_with_merchant_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_009.png"); _g_done_assets += 1
	verify("images/port_city_mercenary_with_merchant_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_010.png"); _g_done_assets += 1
	verify("images/port_city_mercenary_with_merchant_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_011.png"); _g_done_assets += 1
	verify("images/port_city_mercenary_with_merchant_012.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_012.png"); _g_done_assets += 1
	verify("images/port_city_mercenary_with_merchant_013.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_013.png"); _g_done_assets += 1
	verify("images/port_city_mercenary_with_merchant_014.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_014.png"); _g_done_assets += 1
	verify("images/port_city_mercenary_with_merchant_015.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_015.png"); _g_done_assets += 1
	verify("images/port_city_mercenary_with_merchant_016.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_016.png"); _g_done_assets += 1
	verify("images/port_city_mercenary_with_merchant_017.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_017.png"); _g_done_assets += 1
	verify("images/port_city_mercenary_with_merchant_018.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_018.png"); _g_done_assets += 1
	verify("images/port_city_mercenary_with_merchant_019.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_019.png"); _g_done_assets += 1
	verify("images/port_city_mercenary_with_merchant_020.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_020.png"); _g_done_assets += 1
	verify("images/port_city_mercenary_with_merchant_021.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_021.png"); _g_done_assets += 1
	verify("images/port_city_mercenary_with_merchant_022.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_022.png"); _g_done_assets += 1
	verify("images/port_city_mercenary_with_merchant_023.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_023.png"); _g_done_assets += 1
	verify("images/port_city_mercenary_with_merchant_024.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_024.png"); _g_done_assets += 1
	verify("images/port_city_mercenary_with_merchant_025.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_025.png"); _g_done_assets += 1
	verify("images/port_city_mercenary_with_merchant_026.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_026.png"); _g_done_assets += 1
	verify("images/port_city_mercenary_with_merchant_027.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_027.png"); _g_done_assets += 1
	verify("images/port_city_mercenary_with_merchant_028.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_028.png"); _g_done_assets += 1
	verify("images/port_city_mercenary_with_merchant_029.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_029.png"); _g_done_assets += 1
	verify("images/port_city_mercenary_with_merchant_030.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_030.png"); _g_done_assets += 1
	verify("images/port_city_mercenary_with_merchant_031.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_031.png"); _g_done_assets += 1
	verify("images/port_city_mercenary_with_merchant_032.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_032.png"); _g_done_assets += 1
	verify("images/port_city_mercenary_with_merchant_033.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_033.png"); _g_done_assets += 1
	verify("images/port_city_mercenary_with_merchant_034.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_034.png"); _g_done_assets += 1
	verify("images/port_city_mercenary_with_merchant_035.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_035.png"); _g_done_assets += 1
	verify("images/port_city_mercenary_with_merchant_036.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_036.png"); _g_done_assets += 1
	verify("images/port_city_mercenary_with_merchant_037.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_037.png"); _g_done_assets += 1
	verify("images/port_city_mercenary_decision_node_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_decision_node_001.png"); _g_done_assets += 1
	verify("images/port_city_mercenary_decision_node_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_decision_node_002.png"); _g_done_assets += 1
	verify("images/port_city_mercenary_decision_node_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_decision_node_003.png"); _g_done_assets += 1
	verify("images/port_city_mercenary_response_node_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_response_node_001.png"); _g_done_assets += 1
	verify("images/port_city_mercenary_response_node_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_response_node_002.png"); _g_done_assets += 1
	verify("images/port_city_mercenary_response_node_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_response_node_003.png"); _g_done_assets += 1
	verify("images/port_city_mercenary_with_tavern_keeper_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_tavern_keeper_001.png"); _g_done_assets += 1
	verify("images/port_city_mercenary_with_tavern_keeper_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_tavern_keeper_002.png"); _g_done_assets += 1
	verify("images/port_city_mercenary_with_tavern_keeper_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_tavern_keeper_003.png"); _g_done_assets += 1
	verify("images/port_city_mercenary_with_tavern_keeper_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_tavern_keeper_004.png"); _g_done_assets += 1
	verify("images/port_city_mercenary_with_tavern_keeper_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_tavern_keeper_005.png"); _g_done_assets += 1
	verify("images/port_city_mercenary_with_tavern_keeper_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_tavern_keeper_006.png"); _g_done_assets += 1
	verify("images/port_city_mercenary_with_tavern_keeper_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_tavern_keeper_007.png"); _g_done_assets += 1
	verify("images/port_city_mercenary_with_tavern_keeper_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_tavern_keeper_008.png"); _g_done_assets += 1
	verify("images/port_city_mercenary_with_tavern_keeper_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_tavern_keeper_009.png"); _g_done_assets += 1
	verify("images/port_city_mercenary_with_tavern_keeper_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_tavern_keeper_010.png"); _g_done_assets += 1
	verify("images/port_city_mercenary_with_tavern_keeper_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_tavern_keeper_011.png"); _g_done_assets += 1
	verify("images/port_city_mercenary_with_tavern_keeper_012.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_tavern_keeper_012.png"); _g_done_assets += 1
	verify("images/port_city_mercenary_with_tavern_keeper_013.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_tavern_keeper_013.png"); _g_done_assets += 1
	verify("images/port_city_mercenary_with_tavern_keeper_014.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_tavern_keeper_014.png"); _g_done_assets += 1
	verify("images/port_city_mercenary_with_tavern_keeper_015.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_tavern_keeper_015.png"); _g_done_assets += 1
	verify("images/port_city_mercenary_with_tavern_keeper_016.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_tavern_keeper_016.png"); _g_done_assets += 1
	verify("images/port_city_mercenary_with_tavern_keeper_017.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_tavern_keeper_017.png"); _g_done_assets += 1
	verify("images/port_city_mercenary_with_harbor_captain_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_harbor_captain_001.png"); _g_done_assets += 1
	verify("images/port_city_mercenary_with_harbor_captain_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_harbor_captain_002.png"); _g_done_assets += 1
	verify("images/port_city_mercenary_with_harbor_captain_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_harbor_captain_003.png"); _g_done_assets += 1
	verify("images/port_city_mercenary_with_harbor_captain_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_harbor_captain_004.png"); _g_done_assets += 1
	verify("images/port_city_mercenary_with_harbor_captain_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_harbor_captain_005.png"); _g_done_assets += 1
	verify("images/port_city_mercenary_with_harbor_captain_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_harbor_captain_006.png"); _g_done_assets += 1
	verify("images/port_city_mercenary_with_harbor_captain_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_harbor_captain_007.png"); _g_done_assets += 1
	verify("images/port_city_mercenary_with_harbor_captain_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_harbor_captain_008.png"); _g_done_assets += 1
	verify("images/cultist_island_mercenary_with_cultist_soldier_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_cultist_soldier_001.png"); _g_done_assets += 1
	verify("images/cultist_island_mercenary_with_cultist_soldier_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_cultist_soldier_002.png"); _g_done_assets += 1
	verify("images/cultist_island_mercenary_with_cultist_soldier_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_cultist_soldier_003.png"); _g_done_assets += 1
	verify("images/cultist_island_mercenary_with_cultist_soldier_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_cultist_soldier_004.png"); _g_done_assets += 1
	verify("images/cultist_island_mercenary_with_cultist_priest_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_cultist_priest_001.png"); _g_done_assets += 1
	verify("images/cultist_island_mercenary_with_cultist_priest_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_cultist_priest_002.png"); _g_done_assets += 1
	verify("images/cultist_island_mercenary_with_cultist_priest_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_cultist_priest_003.png"); _g_done_assets += 1
	verify("images/cultist_island_mercenary_with_cultist_priest_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_cultist_priest_004.png"); _g_done_assets += 1
	verify("images/cultist_island_mercenary_with_experiments_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_experiments_001.png"); _g_done_assets += 1
	verify("images/cultist_island_mercenary_with_experiments_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_experiments_002.png"); _g_done_assets += 1
	verify("images/cultist_island_mercenary_with_experiments_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_experiments_003.png"); _g_done_assets += 1
	verify("images/cultist_island_mercenary_with_experiments_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_experiments_004.png"); _g_done_assets += 1
	verify("images/cultist_island_mercenary_with_experiments_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_experiments_005.png"); _g_done_assets += 1
	verify("images/cultist_island_mercenary_with_experiments_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_experiments_006.png"); _g_done_assets += 1
	verify("images/cultist_island_mercenary_with_experiments_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_experiments_007.png"); _g_done_assets += 1
	verify("images/cultist_island_mercenary_with_experiments_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_experiments_008.png"); _g_done_assets += 1
	verify("images/cultist_island_mercenary_with_funeris_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_funeris_001.png"); _g_done_assets += 1
	verify("images/cultist_island_mercenary_with_funeris_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_funeris_002.png"); _g_done_assets += 1
	verify("images/cultist_island_mercenary_with_funeris_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_funeris_003.png"); _g_done_assets += 1
	verify("images/cultist_island_mercenary_with_funeris_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_funeris_004.png"); _g_done_assets += 1
	verify("images/cultist_island_mercenary_with_funeris_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_funeris_005.png"); _g_done_assets += 1
	verify("images/cultist_island_mercenary_with_funeris_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_funeris_006.png"); _g_done_assets += 1
	verify("images/cultist_island_mercenary_with_funeris_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_funeris_007.png"); _g_done_assets += 1
	verify("images/cultist_island_mercenary_with_funeris_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_funeris_008.png"); _g_done_assets += 1
	verify("images/cultist_island_mercenary_with_funeris_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_funeris_009.png"); _g_done_assets += 1
	verify("images/cultist_island_mercenary_with_funeris_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_funeris_010.png"); _g_done_assets += 1
	verify("images/cultist_island_mercenary_with_funeris_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_funeris_011.png"); _g_done_assets += 1
	verify("images/cultist_island_mercenary_with_funeris_012.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_funeris_012.png"); _g_done_assets += 1
	verify("images/cultist_island_mercenary_with_funeris_013.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_funeris_013.png"); _g_done_assets += 1
	verify("images/cultist_island_mercenary_with_funeris_014.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_funeris_014.png"); _g_done_assets += 1
	verify("images/cultist_island_mercenary_with_funeris_015.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_funeris_015.png"); _g_done_assets += 1
	verify("images/cultist_island_mercenary_with_funeris_016.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_funeris_016.png"); _g_done_assets += 1
	verify("images/cultist_island_mercenary_with_funeris_017.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_funeris_017.png"); _g_done_assets += 1
	verify("images/cultist_island_mercenary_with_funeris_018.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_funeris_018.png"); _g_done_assets += 1
	verify("images/cultist_island_mercenary_with_funeris_019.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_funeris_019.png"); _g_done_assets += 1
	verify("images/cultist_island_mercenary_with_funeris_020.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_funeris_020.png"); _g_done_assets += 1
	verify("images/cultist_island_mercenary_with_funeris_021.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_funeris_021.png"); _g_done_assets += 1
	verify("images/cultist_island_mercenary_with_funeris_022.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_funeris_022.png"); _g_done_assets += 1
	verify("images/cultist_island_mercenary_with_funeris_023.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_funeris_023.png"); _g_done_assets += 1
	verify("images/cultist_island_mercenary_with_funeris_024.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_funeris_024.png"); _g_done_assets += 1
	verify("images/cultist_island_mercenary_with_funeris_025.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_funeris_025.png"); _g_done_assets += 1
	verify("images/cultist_island_mercenary_with_funeris_026.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_funeris_026.png"); _g_done_assets += 1
	verify("images/cultist_island_mercenary_with_funeris_027.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_funeris_027.png"); _g_done_assets += 1
	verify("images/cultist_island_mercenary_with_funeris_028.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_funeris_028.png"); _g_done_assets += 1
	verify("images/cultist_island_mercenary_with_funeris_029.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_funeris_029.png"); _g_done_assets += 1
	verify("images/cultist_island_mercenary_with_funeris_030.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_funeris_030.png"); _g_done_assets += 1
	verify("images/cultist_island_mercenary_with_cult_leader_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_cult_leader_001.png"); _g_done_assets += 1
	verify("images/cultist_island_mercenary_with_cult_leader_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_cult_leader_002.png"); _g_done_assets += 1
	verify("images/cultist_island_mercenary_with_cult_leader_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_cult_leader_003.png"); _g_done_assets += 1
	verify("images/cultist_island_mercenary_with_cult_leader_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_cult_leader_004.png"); _g_done_assets += 1
	verify("images/cultist_island_mercenary_with_cult_leader_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_cult_leader_005.png"); _g_done_assets += 1
	verify("images/cultist_island_mercenary_with_cult_leader_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_cult_leader_006.png"); _g_done_assets += 1
	verify("images/cultist_island_mercenary_with_cult_leader_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_cult_leader_007.png"); _g_done_assets += 1
	verify("images/cultist_island_mercenary_with_cult_leader_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_cult_leader_008.png"); _g_done_assets += 1
	verify("images/cultist_island_mercenary_with_cult_leader_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_cult_leader_009.png"); _g_done_assets += 1
	verify("images/cultist_island_mercenary_with_cult_leader_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_cult_leader_010.png"); _g_done_assets += 1
	verify("images/cultist_island_mercenary_with_cult_leader_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_cult_leader_011.png"); _g_done_assets += 1
	verify("images/cultist_island_mercenary_with_cult_leader_012.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_cult_leader_012.png"); _g_done_assets += 1
	verify("images/cultist_island_mercenary_with_cult_leader_013.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_cult_leader_013.png"); _g_done_assets += 1
	verify("images/cultist_island_mercenary_with_cult_leader_014.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_cult_leader_014.png"); _g_done_assets += 1
	verify("images/cultist_island_mercenary_with_cult_leader_015.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_cult_leader_015.png"); _g_done_assets += 1
	verify("images/cultist_island_mercenary_with_cult_leader_016.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_cult_leader_016.png"); _g_done_assets += 1
	verify("images/cultist_island_mercenary_with_cult_leader_017.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_cult_leader_017.png"); _g_done_assets += 1
	verify("images/cultist_island_mercenary_with_cult_leader_018.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_cult_leader_018.png"); _g_done_assets += 1
	verify("images/cultist_island_mercenary_with_cult_leader_019.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_cult_leader_019.png"); _g_done_assets += 1
	verify("images/cultist_island_mercenary_with_cult_leader_020.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_cult_leader_020.png"); _g_done_assets += 1
	verify("images/cultist_island_funeris_with_cult_leader_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_funeris_with_cult_leader_001.png"); _g_done_assets += 1
	verify("images/cultist_island_funeris_with_cult_leader_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_funeris_with_cult_leader_002.png"); _g_done_assets += 1
	verify("images/cultist_island_funeris_with_cult_leader_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_funeris_with_cult_leader_003.png"); _g_done_assets += 1
	verify("images/cultist_island_funeris_with_cult_leader_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_funeris_with_cult_leader_004.png"); _g_done_assets += 1
	verify("images/cultist_island_funeris_with_cult_leader_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_funeris_with_cult_leader_005.png"); _g_done_assets += 1
	verify("images/cultist_island_funeris_with_cult_leader_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_funeris_with_cult_leader_006.png"); _g_done_assets += 1
	verify("images/cultist_island_funeris_with_cult_leader_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_funeris_with_cult_leader_007.png"); _g_done_assets += 1
	verify("images/cultist_island_funeris_with_cult_leader_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_funeris_with_cult_leader_008.png"); _g_done_assets += 1
	verify("images/cultist_island_funeris_with_cult_leader_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_funeris_with_cult_leader_009.png"); _g_done_assets += 1
	verify("images/cultist_island_funeris_with_cult_leader_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_funeris_with_cult_leader_010.png"); _g_done_assets += 1
	verify("images/cultist_island_funeris_with_cult_leader_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_funeris_with_cult_leader_011.png"); _g_done_assets += 1
	verify("images/cultist_island_funeris_with_cult_leader_012.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_funeris_with_cult_leader_012.png"); _g_done_assets += 1
	verify("images/cultist_island_funeris_with_cult_leader_013.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_funeris_with_cult_leader_013.png"); _g_done_assets += 1
	verify("images/cultist_island_funeris_with_cult_leader_014.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_funeris_with_cult_leader_014.png"); _g_done_assets += 1
	verify("images/cultist_island_funeris_with_cult_leader_015.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_funeris_with_cult_leader_015.png"); _g_done_assets += 1
	verify("images/cultist_island_funeris_with_cult_soldiers_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_funeris_with_cult_soldiers_001.png"); _g_done_assets += 1
	verify("images/cultist_island_funeris_with_cult_soldiers_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_funeris_with_cult_soldiers_002.png"); _g_done_assets += 1
	verify("images/cultist_island_funeris_with_cult_soldiers_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_funeris_with_cult_soldiers_003.png"); _g_done_assets += 1
	verify("images/cultist_island_funeris_with_cult_soldiers_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_funeris_with_cult_soldiers_004.png"); _g_done_assets += 1
	verify("images/cultist_island_funeris_with_cult_soldiers_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_funeris_with_cult_soldiers_005.png"); _g_done_assets += 1
	verify("images/cultist_island_funeris_with_cult_soldiers_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_funeris_with_cult_soldiers_006.png"); _g_done_assets += 1
	verify("images/zone_terrors_funeris_to_herself_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terrors_funeris_to_herself_001.png"); _g_done_assets += 1
	verify("images/zone_terrors_funeris_to_herself_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terrors_funeris_to_herself_002.png"); _g_done_assets += 1
	verify("images/zone_terrors_funeris_to_herself_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terrors_funeris_to_herself_003.png"); _g_done_assets += 1
	verify("images/zone_terrors_funeris_to_herself_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terrors_funeris_to_herself_004.png"); _g_done_assets += 1
	verify("images/zone_terrors_funeris_to_herself_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terrors_funeris_to_herself_005.png"); _g_done_assets += 1
	verify("images/zone_terrors_funeris_to_herself_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terrors_funeris_to_herself_006.png"); _g_done_assets += 1
	verify("images/zone_terrors_funeris_to_herself_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terrors_funeris_to_herself_007.png"); _g_done_assets += 1
	verify("images/zone_terrors_funeris_to_herself_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terrors_funeris_to_herself_008.png"); _g_done_assets += 1
	verify("images/zone_terrors_funeris_to_herself_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terrors_funeris_to_herself_009.png"); _g_done_assets += 1
	verify("images/zone_terrors_funeris_to_herself_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terrors_funeris_to_herself_010.png"); _g_done_assets += 1
	verify("images/zone_terrors_funeris_to_herself_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terrors_funeris_to_herself_011.png"); _g_done_assets += 1
	verify("images/zone_terrors_funeris_to_herself_012.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terrors_funeris_to_herself_012.png"); _g_done_assets += 1
	verify("images/zone_terrors_funeris_to_herself_013.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terrors_funeris_to_herself_013.png"); _g_done_assets += 1
	verify("images/zone_terrors_funeris_to_herself_014.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terrors_funeris_to_herself_014.png"); _g_done_assets += 1
	verify("images/home_village_funeris_to_memory_fragment_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_funeris_to_memory_fragment_001.png"); _g_done_assets += 1
	verify("images/home_village_funeris_to_memory_fragment_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_funeris_to_memory_fragment_002.png"); _g_done_assets += 1
	verify("images/home_village_funeris_to_memory_fragment_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_funeris_to_memory_fragment_003.png"); _g_done_assets += 1
	verify("images/home_village_funeris_to_memory_fragment_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_funeris_to_memory_fragment_004.png"); _g_done_assets += 1
	verify("images/home_village_funeris_to_memory_fragment_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_funeris_to_memory_fragment_005.png"); _g_done_assets += 1
	verify("images/home_village_funeris_to_memory_fragment_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_funeris_to_memory_fragment_006.png"); _g_done_assets += 1
	verify("images/home_village_funeris_to_memory_fragment_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_funeris_to_memory_fragment_007.png"); _g_done_assets += 1
	verify("images/home_village_funeris_to_memory_fragment_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_funeris_to_memory_fragment_008.png"); _g_done_assets += 1
	verify("images/home_village_funeris_to_memory_fragment_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_funeris_to_memory_fragment_009.png"); _g_done_assets += 1
	verify("images/home_village_funeris_to_memory_fragment_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_funeris_to_memory_fragment_010.png"); _g_done_assets += 1
	verify("images/home_village_funeris_to_memory_fragment_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_funeris_to_memory_fragment_011.png"); _g_done_assets += 1
	verify("images/home_village_funeris_to_memory_fragment_012.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_funeris_to_memory_fragment_012.png"); _g_done_assets += 1
	verify("images/home_village_funeris_to_memory_fragment_013.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_funeris_to_memory_fragment_013.png"); _g_done_assets += 1
	verify("images/home_village_funeris_to_memory_fragment_014.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_funeris_to_memory_fragment_014.png"); _g_done_assets += 1
	verify("images/home_village_funeris_to_memory_fragment_015.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_funeris_to_memory_fragment_015.png"); _g_done_assets += 1
	verify("images/home_village_funeris_to_memory_fragment_016.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_funeris_to_memory_fragment_016.png"); _g_done_assets += 1
	verify("images/home_village_funeris_to_memory_fragment_017.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_funeris_to_memory_fragment_017.png"); _g_done_assets += 1
	verify("images/home_village_funeris_to_memory_fragment_018.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_funeris_to_memory_fragment_018.png"); _g_done_assets += 1
	verify("images/home_village_funeris_to_memory_fragment_019.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_funeris_to_memory_fragment_019.png"); _g_done_assets += 1
	verify("images/home_village_funeris_to_memory_fragment_020.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_funeris_to_memory_fragment_020.png"); _g_done_assets += 1
	verify("images/home_village_funeris_decision_node_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_funeris_decision_node_001.png"); _g_done_assets += 1
	verify("images/home_village_funeris_decision_node_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_funeris_decision_node_002.png"); _g_done_assets += 1
	verify("images/home_village_funeris_decision_node_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_funeris_decision_node_003.png"); _g_done_assets += 1
	verify("images/home_village_funeris_response_node_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_funeris_response_node_001.png"); _g_done_assets += 1
	verify("images/home_village_funeris_response_node_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_funeris_response_node_002.png"); _g_done_assets += 1
	verify("images/home_village_funeris_response_node_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_funeris_response_node_003.png"); _g_done_assets += 1
	verify("images/laboratory_funeris_with_priest_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_priest_001.png"); _g_done_assets += 1
	verify("images/laboratory_funeris_with_priest_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_priest_002.png"); _g_done_assets += 1
	verify("images/laboratory_funeris_with_priest_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_priest_003.png"); _g_done_assets += 1
	verify("images/laboratory_funeris_with_priest_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_priest_004.png"); _g_done_assets += 1
	verify("images/laboratory_funeris_with_priest_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_priest_005.png"); _g_done_assets += 1
	verify("images/laboratory_funeris_with_priest_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_priest_006.png"); _g_done_assets += 1
	verify("images/laboratory_funeris_with_priest_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_priest_007.png"); _g_done_assets += 1
	verify("images/laboratory_funeris_with_priest_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_priest_008.png"); _g_done_assets += 1
	verify("images/laboratory_funeris_with_priest_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_priest_009.png"); _g_done_assets += 1
	verify("images/laboratory_funeris_with_priest_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_priest_010.png"); _g_done_assets += 1
	verify("images/laboratory_funeris_with_priest_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_priest_011.png"); _g_done_assets += 1
	verify("images/laboratory_funeris_with_priest_012.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_priest_012.png"); _g_done_assets += 1
	verify("images/laboratory_funeris_with_priest_013.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_priest_013.png"); _g_done_assets += 1
	verify("images/laboratory_funeris_with_priest_014.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_priest_014.png"); _g_done_assets += 1
	verify("images/laboratory_funeris_with_priest_015.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_priest_015.png"); _g_done_assets += 1
	verify("images/laboratory_funeris_with_priest_016.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_priest_016.png"); _g_done_assets += 1
	verify("images/laboratory_funeris_with_priest_017.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_priest_017.png"); _g_done_assets += 1
	verify("images/laboratory_funeris_with_priest_018.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_priest_018.png"); _g_done_assets += 1
	verify("images/laboratory_funeris_with_priest_019.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_priest_019.png"); _g_done_assets += 1
	verify("images/laboratory_funeris_with_priest_020.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_priest_020.png"); _g_done_assets += 1
	verify("images/laboratory_funeris_with_priest_021.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_priest_021.png"); _g_done_assets += 1
	verify("images/laboratory_funeris_with_priest_022.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_priest_022.png"); _g_done_assets += 1
	verify("images/laboratory_funeris_with_priest_023.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_priest_023.png"); _g_done_assets += 1
	verify("images/laboratory_funeris_with_priest_024.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_priest_024.png"); _g_done_assets += 1
	verify("images/laboratory_funeris_with_priest_025.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_priest_025.png"); _g_done_assets += 1
	verify("images/laboratory_funeris_with_priest_026.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_priest_026.png"); _g_done_assets += 1
	verify("images/laboratory_funeris_with_priest_027.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_priest_027.png"); _g_done_assets += 1
	verify("images/laboratory_funeris_with_priest_028.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_priest_028.png"); _g_done_assets += 1
	verify("images/laboratory_funeris_with_priest_029.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_priest_029.png"); _g_done_assets += 1
	verify("images/laboratory_funeris_with_priest_030.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_priest_030.png"); _g_done_assets += 1
	verify("images/laboratory_funeris_with_priest_031.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_priest_031.png"); _g_done_assets += 1
	verify("images/laboratory_funeris_with_priest_032.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_priest_032.png"); _g_done_assets += 1
	verify("images/laboratory_funeris_with_priest_033.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_priest_033.png"); _g_done_assets += 1
	verify("images/laboratory_funeris_with_priest_034.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_priest_034.png"); _g_done_assets += 1
	verify("images/laboratory_funeris_with_assassin_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_assassin_001.png"); _g_done_assets += 1
	verify("images/walled_priest_with_draft_officer_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_priest_with_draft_officer_001.png"); _g_done_assets += 1
	verify("images/walled_priest_with_draft_officer_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_priest_with_draft_officer_002.png"); _g_done_assets += 1
	verify("images/walled_priest_with_draft_officer_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_priest_with_draft_officer_003.png"); _g_done_assets += 1
	verify("images/walled_priest_with_draft_officer_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_priest_with_draft_officer_004.png"); _g_done_assets += 1
	verify("images/walled_chapel_priest_with_guard_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_chapel_priest_with_guard_001.png"); _g_done_assets += 1
	verify("images/walled_chapel_priest_with_guard_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_chapel_priest_with_guard_002.png"); _g_done_assets += 1
	verify("images/walled_chapel_priest_with_guard_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_chapel_priest_with_guard_003.png"); _g_done_assets += 1
	verify("images/walled_chapel_priest_with_guard_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_chapel_priest_with_guard_004.png"); _g_done_assets += 1
	verify("images/walled_chapel_priest_with_guard_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_chapel_priest_with_guard_005.png"); _g_done_assets += 1
	verify("images/walled_chapel_priest_with_guard_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_chapel_priest_with_guard_006.png"); _g_done_assets += 1
	verify("images/theocratic_priest_with_church_attendance_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_attendance_001.png"); _g_done_assets += 1
	verify("images/theocratic_priest_with_church_attendance_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_attendance_002.png"); _g_done_assets += 1
	verify("images/theocratic_priest_with_church_attendance_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_attendance_003.png"); _g_done_assets += 1
	verify("images/theocratic_priest_with_church_attendance_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_attendance_004.png"); _g_done_assets += 1
	verify("images/theocratic_priest_with_church_attendance_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_attendance_005.png"); _g_done_assets += 1
	verify("images/theocratic_priest_with_church_attendance_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_attendance_006.png"); _g_done_assets += 1
	verify("images/theocratic_priest_with_church_attendance_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_attendance_007.png"); _g_done_assets += 1
	verify("images/theocratic_priest_with_church_attendance_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_attendance_008.png"); _g_done_assets += 1
	verify("images/theocratic_priest_with_church_attendance_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_attendance_009.png"); _g_done_assets += 1
	verify("images/theocratic_priest_with_church_attendance_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_attendance_010.png"); _g_done_assets += 1
	verify("images/theocratic_priest_with_church_attendance_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_attendance_011.png"); _g_done_assets += 1
	verify("images/theocratic_priest_with_church_attendance_012.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_attendance_012.png"); _g_done_assets += 1
	verify("images/theocratic_priest_with_church_attendance_013.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_attendance_013.png"); _g_done_assets += 1
	verify("images/theocratic_priest_with_church_attendance_014.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_attendance_014.png"); _g_done_assets += 1
	verify("images/theocratic_priest_with_church_attendance_015.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_attendance_015.png"); _g_done_assets += 1
	verify("images/theocratic_priest_with_church_attendance_016.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_attendance_016.png"); _g_done_assets += 1
	verify("images/theocratic_priest_with_church_attendance_017.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_attendance_017.png"); _g_done_assets += 1
	verify("images/theocratic_priest_with_church_attendance_018.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_attendance_018.png"); _g_done_assets += 1
	verify("images/theocratic_priest_with_church_attendance_019.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_attendance_019.png"); _g_done_assets += 1
	verify("images/theocratic_priest_with_church_attendance_020.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_attendance_020.png"); _g_done_assets += 1
	verify("images/theocratic_priest_with_church_official_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_official_001.png"); _g_done_assets += 1
	verify("images/theocratic_priest_with_church_official_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_official_002.png"); _g_done_assets += 1
	verify("images/theocratic_priest_with_church_official_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_official_003.png"); _g_done_assets += 1
	verify("images/theocratic_priest_with_church_official_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_official_004.png"); _g_done_assets += 1
	verify("images/theocratic_priest_with_church_official_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_official_005.png"); _g_done_assets += 1
	verify("images/theocratic_priest_with_church_official_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_official_006.png"); _g_done_assets += 1
	verify("images/theocratic_priest_with_church_official_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_official_007.png"); _g_done_assets += 1
	verify("images/theocratic_priest_with_church_official_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_official_008.png"); _g_done_assets += 1
	verify("images/theocratic_priest_with_church_official_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_official_009.png"); _g_done_assets += 1
	verify("images/theocratic_priest_with_church_official_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_official_010.png"); _g_done_assets += 1
	verify("images/theocratic_priest_with_church_official_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_official_011.png"); _g_done_assets += 1
	verify("images/theocratic_priest_with_church_official_012.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_official_012.png"); _g_done_assets += 1
	verify("images/theocratic_priest_with_church_official_013.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_official_013.png"); _g_done_assets += 1
	verify("images/theocratic_priest_with_church_official_014.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_official_014.png"); _g_done_assets += 1
	verify("images/theocratic_priest_with_church_official_015.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_official_015.png"); _g_done_assets += 1
	verify("images/theocratic_priest_with_church_official_016.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_official_016.png"); _g_done_assets += 1
	verify("images/theocratic_priest_with_church_official_017.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_official_017.png"); _g_done_assets += 1
	verify("images/theocratic_priest_with_church_official_018.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_official_018.png"); _g_done_assets += 1
	verify("images/laboratory_priest_to_himself_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_to_himself_001.png"); _g_done_assets += 1
	verify("images/laboratory_priest_to_himself_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_to_himself_002.png"); _g_done_assets += 1
	verify("images/laboratory_priest_to_himself_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_to_himself_003.png"); _g_done_assets += 1
	verify("images/laboratory_priest_to_himself_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_to_himself_004.png"); _g_done_assets += 1
	verify("images/laboratory_priest_to_himself_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_to_himself_005.png"); _g_done_assets += 1
	verify("images/laboratory_priest_to_himself_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_to_himself_006.png"); _g_done_assets += 1
	verify("images/laboratory_priest_to_himself_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_to_himself_007.png"); _g_done_assets += 1
	verify("images/laboratory_priest_to_himself_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_to_himself_008.png"); _g_done_assets += 1
	verify("images/laboratory_priest_to_himself_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_to_himself_009.png"); _g_done_assets += 1
	verify("images/laboratory_priest_decision_node_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_decision_node_001.png"); _g_done_assets += 1
	verify("images/laboratory_priest_decision_node_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_decision_node_002.png"); _g_done_assets += 1
	verify("images/laboratory_priest_decision_node_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_decision_node_003.png"); _g_done_assets += 1
	verify("images/laboratory_priest_response_node_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_response_node_001.png"); _g_done_assets += 1
	verify("images/laboratory_priest_response_node_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_response_node_002.png"); _g_done_assets += 1
	verify("images/laboratory_priest_response_node_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_response_node_003.png"); _g_done_assets += 1
	verify("images/zone_terror_priest_with_medical_staff_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_priest_with_medical_staff_001.png"); _g_done_assets += 1
	verify("images/zone_terror_priest_with_medical_staff_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_priest_with_medical_staff_002.png"); _g_done_assets += 1
	verify("images/zone_terror_priest_with_medical_staff_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_priest_with_medical_staff_003.png"); _g_done_assets += 1
	verify("images/zone_terror_priest_with_medical_staff_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_priest_with_medical_staff_004.png"); _g_done_assets += 1
	verify("images/zone_terror_priest_with_medical_staff_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_priest_with_medical_staff_005.png"); _g_done_assets += 1
	verify("images/zone_terror_priest_with_church_knight_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_priest_with_church_knight_001.png"); _g_done_assets += 1
	verify("images/zone_terror_priest_with_church_knight_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_priest_with_church_knight_002.png"); _g_done_assets += 1
	verify("images/zone_terror_priest_with_church_knight_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_priest_with_church_knight_003.png"); _g_done_assets += 1
	verify("images/zone_terror_priest_with_church_knight_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_priest_with_church_knight_004.png"); _g_done_assets += 1
	verify("images/zone_terror_priest_with_church_knight_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_priest_with_church_knight_005.png"); _g_done_assets += 1
	verify("images/zone_terror_priest_with_church_knight_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_priest_with_church_knight_006.png"); _g_done_assets += 1
	verify("images/zone_terror_priest_with_church_knight_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_priest_with_church_knight_007.png"); _g_done_assets += 1
	verify("images/zone_terror_priest_with_church_knight_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_priest_with_church_knight_008.png"); _g_done_assets += 1
	verify("images/laboratory_priest_to_medical_staff_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_to_medical_staff_001.png"); _g_done_assets += 1
	verify("images/laboratory_priest_to_medical_staff_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_to_medical_staff_002.png"); _g_done_assets += 1
	verify("images/laboratory_priest_to_medical_staff_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_to_medical_staff_003.png"); _g_done_assets += 1
	verify("images/laboratory_priest_to_medical_staff_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_to_medical_staff_004.png"); _g_done_assets += 1
	verify("images/laboratory_priest_to_medical_staff_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_to_medical_staff_005.png"); _g_done_assets += 1
	verify("images/laboratory_priest_to_medical_staff_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_to_medical_staff_006.png"); _g_done_assets += 1
	verify("images/laboratory_priest_to_medical_staff_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_to_medical_staff_007.png"); _g_done_assets += 1
	verify("images/laboratory_priest_to_medical_staff_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_to_medical_staff_008.png"); _g_done_assets += 1
	verify("images/laboratory_priest_to_medical_staff_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_to_medical_staff_009.png"); _g_done_assets += 1
	verify("images/laboratory_priest_to_medical_staff_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_to_medical_staff_010.png"); _g_done_assets += 1
	verify("images/laboratory_priest_to_medical_staff_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_to_medical_staff_011.png"); _g_done_assets += 1
	verify("images/laboratory_priest_to_medical_staff_012.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_to_medical_staff_012.png"); _g_done_assets += 1
	verify("images/laboratory_priest_to_medical_staff_013.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_to_medical_staff_013.png"); _g_done_assets += 1
	verify("images/laboratory_priest_to_medical_staff_014.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_to_medical_staff_014.png"); _g_done_assets += 1
	verify("images/laboratory_priest_to_medical_staff_015.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_to_medical_staff_015.png"); _g_done_assets += 1
	verify("images/laboratory_priest_to_medical_staff_016.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_to_medical_staff_016.png"); _g_done_assets += 1
	verify("images/laboratory_priest_to_medical_staff_017.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_to_medical_staff_017.png"); _g_done_assets += 1
	verify("images/laboratory_priest_to_medical_staff_018.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_to_medical_staff_018.png"); _g_done_assets += 1
	verify("images/laboratory_priest_to_medical_staff_019.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_to_medical_staff_019.png"); _g_done_assets += 1
	verify("images/laboratory_priest_to_medical_staff_020.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_to_medical_staff_020.png"); _g_done_assets += 1
	verify("images/laboratory_priest_to_medical_staff_021.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_to_medical_staff_021.png"); _g_done_assets += 1
	verify("images/laboratory_priest_to_medical_staff_022.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_to_medical_staff_022.png"); _g_done_assets += 1
	verify("images/laboratory_priest_to_medical_staff_023.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_to_medical_staff_023.png"); _g_done_assets += 1
	verify("images/theocratic_battle_priest_with_lucidus_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_priest_with_lucidus_001.png"); _g_done_assets += 1
	verify("images/theocratic_battle_priest_with_lucidus_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_priest_with_lucidus_002.png"); _g_done_assets += 1
	verify("images/theocratic_battle_priest_with_lucidus_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_priest_with_lucidus_003.png"); _g_done_assets += 1
	verify("images/theocratic_battle_priest_with_lucidus_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_priest_with_lucidus_004.png"); _g_done_assets += 1
	verify("images/theocratic_battle_priest_with_lucidus_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_priest_with_lucidus_005.png"); _g_done_assets += 1
	verify("images/theocratic_battle_priest_with_lucidus_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_priest_with_lucidus_006.png"); _g_done_assets += 1
	verify("images/tribe_storage_shaman_with_mercenary_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_shaman_with_mercenary_001.png"); _g_done_assets += 1
	verify("images/tribe_storage_shaman_with_mercenary_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_shaman_with_mercenary_002.png"); _g_done_assets += 1
	verify("images/tribe_storage_shaman_with_mercenary_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_shaman_with_mercenary_003.png"); _g_done_assets += 1
	verify("images/tribe_storage_shaman_with_mercenary_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_shaman_with_mercenary_004.png"); _g_done_assets += 1
	verify("images/tribe_storage_shaman_with_mercenary_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_shaman_with_mercenary_005.png"); _g_done_assets += 1
	verify("images/tribe_storage_shaman_with_mercenary_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_shaman_with_mercenary_006.png"); _g_done_assets += 1
	verify("images/tribe_storage_shaman_with_mercenary_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_shaman_with_mercenary_007.png"); _g_done_assets += 1
	verify("images/tribe_storage_shaman_with_mercenary_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_shaman_with_mercenary_008.png"); _g_done_assets += 1
	verify("images/tribe_storage_shaman_with_mercenary_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_shaman_with_mercenary_009.png"); _g_done_assets += 1
	verify("images/tribe_storage_shaman_with_mercenary_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_shaman_with_mercenary_010.png"); _g_done_assets += 1
	verify("images/tribe_storage_shaman_with_mercenary_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_shaman_with_mercenary_011.png"); _g_done_assets += 1
	verify("images/tribe_storage_shaman_with_mercenary_012.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_shaman_with_mercenary_012.png"); _g_done_assets += 1
	verify("images/tribe_storage_shaman_with_mercenary_013.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_shaman_with_mercenary_013.png"); _g_done_assets += 1
	verify("images/tribe_storage_shaman_with_mercenary_014.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_shaman_with_mercenary_014.png"); _g_done_assets += 1
	verify("images/tribe_storage_shaman_with_mercenary_015.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_shaman_with_mercenary_015.png"); _g_done_assets += 1
	verify("images/tribe_storage_shaman_with_mercenary_016.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_shaman_with_mercenary_016.png"); _g_done_assets += 1
	verify("images/tribe_storage_shaman_with_mercenary_017.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_shaman_with_mercenary_017.png"); _g_done_assets += 1
	verify("images/tribe_storage_shaman_with_mercenary_018.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_shaman_with_mercenary_018.png"); _g_done_assets += 1
	verify("images/tribe_storage_shaman_with_mercenary_019.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_shaman_with_mercenary_019.png"); _g_done_assets += 1
	verify("images/tribe_storage_shaman_with_mercenary_020.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_shaman_with_mercenary_020.png"); _g_done_assets += 1
	verify("images/tribe_storage_shaman_with_mercenary_021.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_shaman_with_mercenary_021.png"); _g_done_assets += 1
	verify("images/tribe_storage_shaman_with_mercenary_022.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_shaman_with_mercenary_022.png"); _g_done_assets += 1
	verify("images/tribe_tunnel_shaman_with_tribe_chief_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_tunnel_shaman_with_tribe_chief_001.png"); _g_done_assets += 1
	verify("images/tribe_tunnel_shaman_with_tribe_chief_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_tunnel_shaman_with_tribe_chief_002.png"); _g_done_assets += 1
	verify("images/tribe_tunnel_shaman_with_tribe_chief_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_tunnel_shaman_with_tribe_chief_003.png"); _g_done_assets += 1
	verify("images/tribe_tunnel_shaman_with_tribe_chief_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_tunnel_shaman_with_tribe_chief_004.png"); _g_done_assets += 1
	verify("images/tribe_tunnel_shaman_with_mercenary_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_tunnel_shaman_with_mercenary_001.png"); _g_done_assets += 1
	verify("images/tribe_tunnel_shaman_with_mercenary_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_tunnel_shaman_with_mercenary_002.png"); _g_done_assets += 1
	verify("images/tribe_tunnel_shaman_with_mercenary_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_tunnel_shaman_with_mercenary_003.png"); _g_done_assets += 1
	verify("images/tribe_tunnel_shaman_with_mercenary_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_tunnel_shaman_with_mercenary_004.png"); _g_done_assets += 1
	verify("images/tribe_tunnel_shaman_with_mercenary_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_tunnel_shaman_with_mercenary_005.png"); _g_done_assets += 1
	verify("images/tribe_tunnel_shaman_with_mercenary_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_tunnel_shaman_with_mercenary_006.png"); _g_done_assets += 1
	verify("images/tribe_tunnel_shaman_with_mercenary_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_tunnel_shaman_with_mercenary_007.png"); _g_done_assets += 1
	verify("images/tribe_tunnel_shaman_with_mercenary_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_tunnel_shaman_with_mercenary_008.png"); _g_done_assets += 1
	verify("images/tribe_tunnel_shaman_with_mercenary_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_tunnel_shaman_with_mercenary_009.png"); _g_done_assets += 1
	verify("images/tribe_tunnel_shaman_with_mercenary_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_tunnel_shaman_with_mercenary_010.png"); _g_done_assets += 1
	verify("images/tribe_tunnel_shaman_with_mercenary_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_tunnel_shaman_with_mercenary_011.png"); _g_done_assets += 1
	verify("images/tribe_tunnel_shaman_with_mercenary_012.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_tunnel_shaman_with_mercenary_012.png"); _g_done_assets += 1
	verify("images/tribe_shaman_foresight_low_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_shaman_foresight_low_001.png"); _g_done_assets += 1
	verify("images/tribe_shaman_foresight_low_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_shaman_foresight_low_002.png"); _g_done_assets += 1
	verify("images/tribe_shaman_foresight_low_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_shaman_foresight_low_003.png"); _g_done_assets += 1
	verify("images/tribe_shaman_foresight_mid_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_shaman_foresight_mid_001.png"); _g_done_assets += 1
	verify("images/tribe_shaman_foresight_mid_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_shaman_foresight_mid_002.png"); _g_done_assets += 1
	verify("images/tribe_shaman_foresight_mid_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_shaman_foresight_mid_003.png"); _g_done_assets += 1
	verify("images/tribe_shaman_foresight_high_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_shaman_foresight_high_001.png"); _g_done_assets += 1
	verify("images/tribe_shaman_foresight_high_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_shaman_foresight_high_002.png"); _g_done_assets += 1
	verify("images/tribe_shaman_foresight_high_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_shaman_foresight_high_003.png"); _g_done_assets += 1
	verify("images/tribe_shaman_foresight_high_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_shaman_foresight_high_004.png"); _g_done_assets += 1
	verify("images/tribe_shaman_foresight_high_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_shaman_foresight_high_005.png"); _g_done_assets += 1
	verify("images/zone_terror_shaman_with_mercenary_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_shaman_with_mercenary_001.png"); _g_done_assets += 1
	verify("images/zone_terror_shaman_with_mercenary_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_shaman_with_mercenary_002.png"); _g_done_assets += 1
	verify("images/zone_terror_shaman_with_mercenary_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_shaman_with_mercenary_003.png"); _g_done_assets += 1
	verify("images/zone_terror_shaman_with_mercenary_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_shaman_with_mercenary_004.png"); _g_done_assets += 1
	verify("images/zone_terror_shaman_with_mercenary_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_shaman_with_mercenary_005.png"); _g_done_assets += 1
	verify("images/zone_terror_shaman_with_mercenary_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_shaman_with_mercenary_006.png"); _g_done_assets += 1
	verify("images/zone_terror_shaman_with_mercenary_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_shaman_with_mercenary_007.png"); _g_done_assets += 1
	verify("images/zone_terror_shaman_with_mercenary_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_shaman_with_mercenary_008.png"); _g_done_assets += 1
	verify("images/zone_terror_shaman_with_mercenary_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_shaman_with_mercenary_009.png"); _g_done_assets += 1
	verify("images/zone_terror_shaman_with_mercenary_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_shaman_with_mercenary_010.png"); _g_done_assets += 1
	verify("images/zone_terror_shaman_with_mercenary_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_shaman_with_mercenary_011.png"); _g_done_assets += 1
	verify("images/zone_terror_shaman_with_mercenary_012.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_shaman_with_mercenary_012.png"); _g_done_assets += 1
	verify("images/zone_terror_shaman_with_mercenary_013.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_shaman_with_mercenary_013.png"); _g_done_assets += 1
	verify("images/zone_terror_shaman_with_mercenary_014.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_shaman_with_mercenary_014.png"); _g_done_assets += 1
	verify("images/zone_terror_shaman_with_mercenary_015.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_shaman_with_mercenary_015.png"); _g_done_assets += 1
	verify("images/zone_terror_shaman_with_mercenary_016.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_shaman_with_mercenary_016.png"); _g_done_assets += 1
	verify("images/zone_terror_shaman_with_mercenary_017.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_shaman_with_mercenary_017.png"); _g_done_assets += 1
	verify("images/zone_terror_shaman_with_mercenary_018.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_shaman_with_mercenary_018.png"); _g_done_assets += 1
	verify("images/zone_terror_shaman_with_mercenary_019.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_shaman_with_mercenary_019.png"); _g_done_assets += 1
	verify("images/zone_terror_shaman_with_mercenary_020.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_shaman_with_mercenary_020.png"); _g_done_assets += 1
	verify("images/zone_terror_shaman_with_mercenary_021.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_shaman_with_mercenary_021.png"); _g_done_assets += 1
	verify("images/zone_terror_shaman_with_mercenary_022.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_shaman_with_mercenary_022.png"); _g_done_assets += 1
	verify("images/zone_terror_shaman_with_mercenary_023.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_shaman_with_mercenary_023.png"); _g_done_assets += 1
	verify("images/zone_terror_shaman_with_mercenary_024.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_shaman_with_mercenary_024.png"); _g_done_assets += 1
	verify("images/zone_terror_shaman_with_mercenary_025.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_shaman_with_mercenary_025.png"); _g_done_assets += 1
	verify("images/zone_terror_shaman_with_mercenary_026.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_shaman_with_mercenary_026.png"); _g_done_assets += 1
	verify("images/zone_terror_shaman_with_mercenary_027.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_shaman_with_mercenary_027.png"); _g_done_assets += 1
	verify("images/zone_terror_shaman_with_mercenary_028.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_shaman_with_mercenary_028.png"); _g_done_assets += 1
	verify("images/zone_terror_shaman_with_mercenary_029.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_shaman_with_mercenary_029.png"); _g_done_assets += 1
	verify("images/port_city_shaman_with_mercenary_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_shaman_with_mercenary_001.png"); _g_done_assets += 1
	verify("images/port_city_shaman_with_mercenary_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_shaman_with_mercenary_002.png"); _g_done_assets += 1
	verify("images/port_city_shaman_with_mercenary_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_shaman_with_mercenary_003.png"); _g_done_assets += 1
	verify("images/port_city_shaman_with_mercenary_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_shaman_with_mercenary_004.png"); _g_done_assets += 1
	verify("images/port_city_shaman_with_mercenary_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_shaman_with_mercenary_005.png"); _g_done_assets += 1
	verify("images/port_city_shaman_with_mercenary_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_shaman_with_mercenary_006.png"); _g_done_assets += 1
	verify("images/port_city_shaman_with_mercenary_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_shaman_with_mercenary_007.png"); _g_done_assets += 1
	verify("images/port_city_shaman_with_mercenary_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_shaman_with_mercenary_008.png"); _g_done_assets += 1
	verify("images/port_city_shaman_with_mercenary_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_shaman_with_mercenary_009.png"); _g_done_assets += 1
	verify("images/port_city_shaman_with_mercenary_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_shaman_with_mercenary_010.png"); _g_done_assets += 1
	verify("images/port_city_shaman_with_mercenary_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_shaman_with_mercenary_011.png"); _g_done_assets += 1
	verify("images/port_city_shaman_with_mercenary_012.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_shaman_with_mercenary_012.png"); _g_done_assets += 1
	verify("images/port_city_shaman_with_mercenary_013.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_shaman_with_mercenary_013.png"); _g_done_assets += 1
	verify("images/port_city_shaman_with_mercenary_014.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_shaman_with_mercenary_014.png"); _g_done_assets += 1
	verify("images/port_city_shaman_with_mercenary_015.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_shaman_with_mercenary_015.png"); _g_done_assets += 1
	verify("images/port_city_shaman_with_mercenary_016.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_shaman_with_mercenary_016.png"); _g_done_assets += 1
	verify("images/port_city_shaman_with_mercenary_017.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_shaman_with_mercenary_017.png"); _g_done_assets += 1
	verify("images/cultist_island_shaman_with_mercenary_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_shaman_with_mercenary_001.png"); _g_done_assets += 1
	verify("images/cultist_island_shaman_with_mercenary_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_shaman_with_mercenary_002.png"); _g_done_assets += 1
	verify("images/cultist_island_shaman_with_mercenary_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_shaman_with_mercenary_003.png"); _g_done_assets += 1
	verify("images/cultist_island_shaman_with_mercenary_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_shaman_with_mercenary_004.png"); _g_done_assets += 1
	verify("images/cultist_island_shaman_with_mercenary_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_shaman_with_mercenary_005.png"); _g_done_assets += 1
	verify("images/cultist_island_shaman_with_mercenary_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_shaman_with_mercenary_006.png"); _g_done_assets += 1
	verify("images/cultist_island_shaman_with_mercenary_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_shaman_with_mercenary_007.png"); _g_done_assets += 1
	verify("images/cultist_island_shaman_with_mercenary_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_shaman_with_mercenary_008.png"); _g_done_assets += 1
	verify("images/cultist_island_shaman_with_mercenary_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_shaman_with_mercenary_009.png"); _g_done_assets += 1
	verify("images/cultist_island_shaman_with_mercenary_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_shaman_with_mercenary_010.png"); _g_done_assets += 1
	verify("images/cultist_island_shaman_with_mercenary_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_shaman_with_mercenary_011.png"); _g_done_assets += 1
	verify("images/cultist_island_shaman_with_mercenary_012.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_shaman_with_mercenary_012.png"); _g_done_assets += 1
	verify("images/cultist_island_shaman_with_mercenary_013.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_shaman_with_mercenary_013.png"); _g_done_assets += 1
	verify("images/cultist_island_shaman_with_mercenary_014.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_shaman_with_mercenary_014.png"); _g_done_assets += 1
	verify("images/cultist_island_shaman_with_mercenary_015.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_shaman_with_mercenary_015.png"); _g_done_assets += 1
	verify("images/cultist_island_shaman_with_mercenary_016.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_shaman_with_mercenary_016.png"); _g_done_assets += 1
	verify("images/cultist_island_shaman_with_mercenary_017.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_shaman_with_mercenary_017.png"); _g_done_assets += 1
	verify("images/cultist_island_shaman_with_mercenary_018.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_shaman_with_mercenary_018.png"); _g_done_assets += 1
	verify("images/cultist_island_shaman_with_mercenary_019.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_shaman_with_mercenary_019.png"); _g_done_assets += 1
	verify("images/cultist_island_shaman_with_mercenary_020.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_shaman_with_mercenary_020.png"); _g_done_assets += 1
	verify("images/outskirts_village_shaman_with_village_chief_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_shaman_with_village_chief_001.png"); _g_done_assets += 1
	verify("images/outskirts_village_shaman_with_village_chief_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_shaman_with_village_chief_002.png"); _g_done_assets += 1
	verify("images/outskirts_village_shaman_with_village_chief_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_shaman_with_village_chief_003.png"); _g_done_assets += 1
	verify("images/outskirts_village_shaman_with_village_chief_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_shaman_with_village_chief_004.png"); _g_done_assets += 1
	verify("images/outskirts_village_shaman_with_village_chief_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_shaman_with_village_chief_005.png"); _g_done_assets += 1
	verify("images/outskirts_village_shaman_with_villager_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_shaman_with_villager_001.png"); _g_done_assets += 1
	verify("images/outskirts_village_shaman_with_villager_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_shaman_with_villager_002.png"); _g_done_assets += 1
	verify("images/outskirts_village_shaman_with_villager_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_shaman_with_villager_003.png"); _g_done_assets += 1
	verify("images/outskirts_village_shaman_with_villager_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_shaman_with_villager_004.png"); _g_done_assets += 1
	verify("images/outskirts_village_shaman_with_villager_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_shaman_with_villager_005.png"); _g_done_assets += 1
	verify("images/outskirts_village_shaman_with_travelling_bard_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_shaman_with_travelling_bard_001.png"); _g_done_assets += 1
	verify("images/outskirts_village_shaman_with_travelling_bard_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_shaman_with_travelling_bard_002.png"); _g_done_assets += 1
	verify("images/outskirts_village_shaman_with_travelling_bard_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_shaman_with_travelling_bard_003.png"); _g_done_assets += 1
	verify("images/outskirts_village_shaman_with_travelling_bard_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_shaman_with_travelling_bard_004.png"); _g_done_assets += 1
	verify("images/outskirts_village_shaman_with_travelling_bard_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_shaman_with_travelling_bard_005.png"); _g_done_assets += 1
	verify("images/tribe_destroyed_shaman_to_herself_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_destroyed_shaman_to_herself_001.png"); _g_done_assets += 1
	verify("images/tribe_destroyed_shaman_to_herself_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_destroyed_shaman_to_herself_002.png"); _g_done_assets += 1
	verify("images/tribe_destroyed_shaman_to_herself_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_destroyed_shaman_to_herself_003.png"); _g_done_assets += 1
	verify("images/tribe_destroyed_shaman_to_herself_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_destroyed_shaman_to_herself_004.png"); _g_done_assets += 1
	verify("images/tribe_destroyed_shaman_to_herself_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_destroyed_shaman_to_herself_005.png"); _g_done_assets += 1
	verify("images/tribe_destroyed_shaman_to_herself_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_destroyed_shaman_to_herself_006.png"); _g_done_assets += 1
	verify("images/tribe_destroyed_shaman_to_herself_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_destroyed_shaman_to_herself_007.png"); _g_done_assets += 1
	verify("images/tribe_destroyed_shaman_to_herself_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_destroyed_shaman_to_herself_008.png"); _g_done_assets += 1
	verify("images/tribe_destroyed_shaman_to_herself_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_destroyed_shaman_to_herself_009.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_guild_master_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_guild_master_001.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_guild_master_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_guild_master_002.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_guild_master_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_guild_master_003.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_guild_master_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_guild_master_004.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_guild_master_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_guild_master_005.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_guild_master_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_guild_master_006.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_guild_master_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_guild_master_007.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_guild_master_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_guild_master_008.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_guild_master_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_guild_master_009.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_guild_master_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_guild_master_010.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_guild_master_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_guild_master_011.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_guild_master_012.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_guild_master_012.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_guild_master_013.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_guild_master_013.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_guild_master_014.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_guild_master_014.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_guild_master_015.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_guild_master_015.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_guild_master_016.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_guild_master_016.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_guild_master_017.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_guild_master_017.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_guild_master_018.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_guild_master_018.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_guild_master_019.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_guild_master_019.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_guild_master_020.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_guild_master_020.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_guild_master_021.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_guild_master_021.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_guild_master_022.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_guild_master_022.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_guild_master_023.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_guild_master_023.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_guild_master_024.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_guild_master_024.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_guild_master_025.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_guild_master_025.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_guild_master_026.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_guild_master_026.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_guild_master_027.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_guild_master_027.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_tavern_keeper_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_tavern_keeper_001.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_tavern_keeper_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_tavern_keeper_002.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_tavern_keeper_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_tavern_keeper_003.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_tavern_keeper_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_tavern_keeper_004.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_tavern_keeper_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_tavern_keeper_005.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_tavern_keeper_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_tavern_keeper_006.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_tavern_keeper_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_tavern_keeper_007.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_tavern_keeper_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_tavern_keeper_008.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_tavern_keeper_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_tavern_keeper_009.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_tavern_keeper_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_tavern_keeper_010.png"); _g_done_assets += 1
	verify("images/port_city_merchant_decision_node_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_decision_node_001.png"); _g_done_assets += 1
	verify("images/port_city_merchant_decision_node_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_decision_node_002.png"); _g_done_assets += 1
	verify("images/port_city_merchant_decision_node_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_decision_node_003.png"); _g_done_assets += 1
	verify("images/port_city_merchant_response_node_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_response_node_001.png"); _g_done_assets += 1
	verify("images/port_city_merchant_response_node_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_response_node_002.png"); _g_done_assets += 1
	verify("images/port_city_merchant_response_node_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_response_node_003.png"); _g_done_assets += 1
	verify("images/walled_merchant_with_blacksmith_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_merchant_with_blacksmith_001.png"); _g_done_assets += 1
	verify("images/walled_merchant_with_blacksmith_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_merchant_with_blacksmith_002.png"); _g_done_assets += 1
	verify("images/walled_merchant_with_blacksmith_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_merchant_with_blacksmith_003.png"); _g_done_assets += 1
	verify("images/walled_merchant_with_blacksmith_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_merchant_with_blacksmith_004.png"); _g_done_assets += 1
	verify("images/walled_merchant_with_blacksmith_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_merchant_with_blacksmith_005.png"); _g_done_assets += 1
	verify("images/walled_merchant_with_blacksmith_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_merchant_with_blacksmith_006.png"); _g_done_assets += 1
	verify("images/walled_merchant_with_blacksmith_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_merchant_with_blacksmith_007.png"); _g_done_assets += 1
	verify("images/walled_merchant_with_blacksmith_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_merchant_with_blacksmith_008.png"); _g_done_assets += 1
	verify("images/walled_merchant_with_blacksmith_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_merchant_with_blacksmith_009.png"); _g_done_assets += 1
	verify("images/walled_merchant_with_blacksmith_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_merchant_with_blacksmith_010.png"); _g_done_assets += 1
	verify("images/walled_merchant_with_blacksmith_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_merchant_with_blacksmith_011.png"); _g_done_assets += 1
	verify("images/outskirts_village_merchant_with_village_chief_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_merchant_with_village_chief_001.png"); _g_done_assets += 1
	verify("images/outskirts_village_merchant_with_village_chief_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_merchant_with_village_chief_002.png"); _g_done_assets += 1
	verify("images/outskirts_village_merchant_with_village_chief_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_merchant_with_village_chief_003.png"); _g_done_assets += 1
	verify("images/outskirts_village_merchant_with_village_chief_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_merchant_with_village_chief_004.png"); _g_done_assets += 1
	verify("images/outskirts_village_merchant_with_village_chief_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_merchant_with_village_chief_005.png"); _g_done_assets += 1
	verify("images/outskirts_village_merchant_with_village_chief_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_merchant_with_village_chief_006.png"); _g_done_assets += 1
	verify("images/outskirts_village_merchant_with_village_chief_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_merchant_with_village_chief_007.png"); _g_done_assets += 1
	verify("images/zone_terrors_merchant_to_himself_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terrors_merchant_to_himself_001.png"); _g_done_assets += 1
	verify("images/zone_terrors_merchant_to_himself_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terrors_merchant_to_himself_002.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_harbor_captain_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_harbor_captain_001.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_harbor_captain_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_harbor_captain_002.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_harbor_captain_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_harbor_captain_003.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_harbor_captain_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_harbor_captain_004.png"); _g_done_assets += 1
	verify("images/home_village_merchant_to_himself_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_merchant_to_himself_001.png"); _g_done_assets += 1
	verify("images/home_village_merchant_to_himself_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_merchant_to_himself_002.png"); _g_done_assets += 1
	verify("images/home_village_merchant_to_himself_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_merchant_to_himself_003.png"); _g_done_assets += 1
	verify("images/home_village_merchant_to_himself_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_merchant_to_himself_004.png"); _g_done_assets += 1
	verify("images/port_outpost_mechant_with_church_spy_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_outpost_mechant_with_church_spy_001.png"); _g_done_assets += 1
	verify("images/port_outpost_mechant_with_church_spy_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_outpost_mechant_with_church_spy_002.png"); _g_done_assets += 1
	verify("images/port_outpost_mechant_with_church_spy_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_outpost_mechant_with_church_spy_003.png"); _g_done_assets += 1
	verify("images/port_outpost_mechant_with_church_spy_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_outpost_mechant_with_church_spy_004.png"); _g_done_assets += 1
	verify("images/port_outpost_mechant_with_church_spy_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_outpost_mechant_with_church_spy_005.png"); _g_done_assets += 1
	verify("images/port_outpost_mechant_with_church_spy_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_outpost_mechant_with_church_spy_006.png"); _g_done_assets += 1
	verify("images/port_outpost_mechant_with_church_spy_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_outpost_mechant_with_church_spy_007.png"); _g_done_assets += 1
	verify("images/port_outpost_mechant_with_church_spy_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_outpost_mechant_with_church_spy_008.png"); _g_done_assets += 1
	verify("images/port_outpost_mechant_with_church_spy_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_outpost_mechant_with_church_spy_009.png"); _g_done_assets += 1
	verify("images/port_outpost_mechant_with_church_spy_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_outpost_mechant_with_church_spy_010.png"); _g_done_assets += 1
	verify("images/port_outpost_mechant_with_church_spy_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_outpost_mechant_with_church_spy_011.png"); _g_done_assets += 1
	verify("images/port_outpost_mechant_with_church_spy_012.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_outpost_mechant_with_church_spy_012.png"); _g_done_assets += 1
	verify("images/port_outpost_mechant_with_church_spy_013.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_outpost_mechant_with_church_spy_013.png"); _g_done_assets += 1
	verify("images/port_outpost_mechant_with_church_spy_014.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_outpost_mechant_with_church_spy_014.png"); _g_done_assets += 1
	verify("images/port_outpost_mechant_with_church_spy_015.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_outpost_mechant_with_church_spy_015.png"); _g_done_assets += 1
	verify("images/port_outpost_mechant_with_church_spy_016.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_outpost_mechant_with_church_spy_016.png"); _g_done_assets += 1
	verify("images/port_outpost_mechant_with_church_spy_017.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_outpost_mechant_with_church_spy_017.png"); _g_done_assets += 1
	verify("images/port_outpost_mechant_with_church_spy_018.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_outpost_mechant_with_church_spy_018.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_captain_and_spy_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_captain_and_spy_001.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_captain_and_spy_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_captain_and_spy_002.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_captain_and_spy_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_captain_and_spy_003.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_captain_and_spy_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_captain_and_spy_004.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_captain_and_spy_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_captain_and_spy_005.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_captain_and_spy_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_captain_and_spy_006.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_captain_and_spy_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_captain_and_spy_007.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_captain_and_spy_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_captain_and_spy_008.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_captain_and_spy_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_captain_and_spy_009.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_captain_and_spy_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_captain_and_spy_010.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_captain_and_spy_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_captain_and_spy_011.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_captain_and_spy_012.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_captain_and_spy_012.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_captain_and_spy_013.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_captain_and_spy_013.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_captain_and_spy_014.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_captain_and_spy_014.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_captain_and_spy_015.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_captain_and_spy_015.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_captain_and_spy_016.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_captain_and_spy_016.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_captain_and_spy_017.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_captain_and_spy_017.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_captain_and_spy_018.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_captain_and_spy_018.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_captain_and_spy_019.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_captain_and_spy_019.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_captain_and_spy_020.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_captain_and_spy_020.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_mercenary_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_mercenary_001.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_mercenary_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_mercenary_002.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_mercenary_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_mercenary_003.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_mercenary_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_mercenary_004.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_mercenary_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_mercenary_005.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_mercenary_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_mercenary_006.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_mercenary_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_mercenary_007.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_mercenary_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_mercenary_008.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_mercenary_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_mercenary_009.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_mercenary_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_mercenary_010.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_mercenary_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_mercenary_011.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_mercenary_012.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_mercenary_012.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_mercenary_013.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_mercenary_013.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_mercenary_014.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_mercenary_014.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_mercenary_015.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_mercenary_015.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_mercenary_016.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_mercenary_016.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_mercenary_017.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_mercenary_017.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_mercenary_018.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_mercenary_018.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_mercenary_019.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_mercenary_019.png"); _g_done_assets += 1
	verify("images/port_city_merchant_with_mercenary_020.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_mercenary_020.png"); _g_done_assets += 1
	verify("images/theocratic_merchant_with_archive_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_archive_001.png"); _g_done_assets += 1
	verify("images/theocratic_merchant_with_archive_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_archive_002.png"); _g_done_assets += 1
	verify("images/theocratic_merchant_with_archive_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_archive_003.png"); _g_done_assets += 1
	verify("images/theocratic_merchant_with_archive_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_archive_004.png"); _g_done_assets += 1
	verify("images/theocratic_merchant_with_archive_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_archive_005.png"); _g_done_assets += 1
	verify("images/theocratic_merchant_with_archive_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_archive_006.png"); _g_done_assets += 1
	verify("images/theocratic_merchant_with_archive_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_archive_007.png"); _g_done_assets += 1
	verify("images/theocratic_merchant_with_archive_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_archive_008.png"); _g_done_assets += 1
	verify("images/theocratic_merchant_with_archive_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_archive_009.png"); _g_done_assets += 1
	verify("images/theocratic_merchant_with_church_knight_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_church_knight_001.png"); _g_done_assets += 1
	verify("images/theocratic_merchant_with_church_knight_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_church_knight_002.png"); _g_done_assets += 1
	verify("images/theocratic_merchant_with_church_knight_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_church_knight_003.png"); _g_done_assets += 1
	verify("images/theocratic_merchant_with_church_knight_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_church_knight_004.png"); _g_done_assets += 1
	verify("images/theocratic_merchant_with_church_knight_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_church_knight_005.png"); _g_done_assets += 1
	verify("images/theocratic_merchant_with_church_knight_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_church_knight_006.png"); _g_done_assets += 1
	verify("images/theocratic_merchant_with_church_knight_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_church_knight_007.png"); _g_done_assets += 1
	verify("images/theocratic_merchant_with_church_knight_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_church_knight_008.png"); _g_done_assets += 1
	verify("images/theocratic_merchant_with_church_knight_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_church_knight_009.png"); _g_done_assets += 1
	verify("images/theocratic_merchant_with_church_knight_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_church_knight_010.png"); _g_done_assets += 1
	verify("images/theocratic_merchant_with_church_knight_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_church_knight_011.png"); _g_done_assets += 1
	verify("images/theocratic_merchant_with_church_knight_012.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_church_knight_012.png"); _g_done_assets += 1
	verify("images/theocratic_merchant_with_church_knight_013.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_church_knight_013.png"); _g_done_assets += 1
	verify("images/theocratic_merchant_with_church_knight_014.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_church_knight_014.png"); _g_done_assets += 1
	verify("images/theocratic_merchant_with_church_knight_015.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_church_knight_015.png"); _g_done_assets += 1
	verify("images/theocratic_merchant_with_priest_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_001.png"); _g_done_assets += 1
	verify("images/theocratic_merchant_with_priest_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_002.png"); _g_done_assets += 1
	verify("images/theocratic_merchant_with_priest_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_003.png"); _g_done_assets += 1
	verify("images/theocratic_merchant_with_priest_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_004.png"); _g_done_assets += 1
	verify("images/theocratic_merchant_with_priest_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_005.png"); _g_done_assets += 1
	verify("images/theocratic_merchant_with_priest_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_006.png"); _g_done_assets += 1
	verify("images/theocratic_merchant_with_priest_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_007.png"); _g_done_assets += 1
	verify("images/theocratic_merchant_with_priest_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_008.png"); _g_done_assets += 1
	verify("images/theocratic_merchant_with_priest_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_009.png"); _g_done_assets += 1
	verify("images/theocratic_merchant_with_priest_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_010.png"); _g_done_assets += 1
	verify("images/theocratic_merchant_with_priest_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_011.png"); _g_done_assets += 1
	verify("images/theocratic_merchant_with_priest_012.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_012.png"); _g_done_assets += 1
	verify("images/theocratic_merchant_with_priest_013.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_013.png"); _g_done_assets += 1
	verify("images/theocratic_merchant_with_priest_014.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_014.png"); _g_done_assets += 1
	verify("images/theocratic_merchant_with_priest_015.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_015.png"); _g_done_assets += 1
	verify("images/theocratic_merchant_with_priest_016.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_016.png"); _g_done_assets += 1
	verify("images/theocratic_merchant_with_priest_017.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_017.png"); _g_done_assets += 1
	verify("images/theocratic_merchant_with_priest_018.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_018.png"); _g_done_assets += 1
	verify("images/theocratic_merchant_with_priest_019.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_019.png"); _g_done_assets += 1
	verify("images/theocratic_merchant_with_priest_020.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_020.png"); _g_done_assets += 1
	verify("images/theocratic_merchant_with_priest_021.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_021.png"); _g_done_assets += 1
	verify("images/theocratic_merchant_with_priest_022.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_022.png"); _g_done_assets += 1
	verify("images/theocratic_merchant_with_priest_023.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_023.png"); _g_done_assets += 1
	verify("images/theocratic_merchant_with_priest_024.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_024.png"); _g_done_assets += 1
	verify("images/theocratic_merchant_with_priest_025.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_025.png"); _g_done_assets += 1
	verify("images/theocratic_merchant_with_priest_026.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_026.png"); _g_done_assets += 1
	verify("images/theocratic_merchant_with_priest_027.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_027.png"); _g_done_assets += 1
	verify("images/theocratic_merchant_with_priest_028.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_028.png"); _g_done_assets += 1
	verify("images/theocratic_merchant_with_priest_029.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_029.png"); _g_done_assets += 1
	verify("images/theocratic_merchant_with_priest_030.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_030.png"); _g_done_assets += 1
	verify("images/theocratic_merchant_with_priest_031.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_031.png"); _g_done_assets += 1
	verify("images/theocratic_merchant_with_priest_032.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_032.png"); _g_done_assets += 1
	verify("images/theocratic_merchant_with_priest_033.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_033.png"); _g_done_assets += 1
	verify("images/theocratic_merchant_with_priest_034.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_034.png"); _g_done_assets += 1
	verify("images/theocratic_merchant_with_priest_035.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_035.png"); _g_done_assets += 1
	verify("images/theocratic_merchant_with_priest_036.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_036.png"); _g_done_assets += 1
	verify("images/theocratic_merchant_with_priest_037.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_037.png"); _g_done_assets += 1
	verify("images/theocratic_merchant_with_priest_038.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_038.png"); _g_done_assets += 1
	verify("images/theocratic_merchant_with_priest_039.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_039.png"); _g_done_assets += 1
	verify("images/theocratic_merchant_with_priest_040.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_040.png"); _g_done_assets += 1
	verify("images/theocratic_merchant_with_priest_041.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_041.png"); _g_done_assets += 1
	verify("images/theocratic_merchant_with_priest_042.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_042.png"); _g_done_assets += 1
	verify("images/theocratic_merchant_with_priest_043.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_043.png"); _g_done_assets += 1
	verify("sprites/npc_n_s2_walled_city_civilians_male/elucidate_idle_male_civilian_variant_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_male_civilian_variant_npc_up.png"); _g_done_assets += 1
	verify("sprites/npc_n_s2_walled_city_civilians_male/elucidate_idle_male_civilian_variant_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_male_civilian_variant_npc_right.png"); _g_done_assets += 1
	verify("sprites/npc_n_s2_walled_city_civilians_male/elucidate_idle_male_civilian_variant_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_male_civilian_variant_npc_left.png"); _g_done_assets += 1
	verify("sprites/npc_n_s2_walled_city_civilians_male/elucidate_idle_male_civilian_variant_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_male_civilian_variant_npc_down.png"); _g_done_assets += 1
	verify("sprites/npc_n_s2_walled_city_civilians_female/elucidate_idle_female_civilian_variant_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_female_civilian_variant_npc_up.png"); _g_done_assets += 1
	verify("sprites/npc_n_s2_walled_city_civilians_female/elucidate_idle_female_civilian_variant_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_female_civilian_variant_npc_right.png"); _g_done_assets += 1
	verify("sprites/npc_n_s2_walled_city_civilians_female/elucidate_idle_female_civilian_variant_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_female_civilian_variant_npc_left.png"); _g_done_assets += 1
	verify("sprites/npc_n_s2_walled_city_civilians_female/elucidate_idle_female_civilian_variant_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_female_civilian_variant_npc_down.png"); _g_done_assets += 1
	verify("sprites/player_mercenary/elucidate_mercenary_sprite_idle_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_mercenary_up_001.png"); _g_done_assets += 1
	verify("sprites/player_mercenary/elucidate_mercenary_move_up_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_mercenary_move_up_001.png"); _g_done_assets += 1
	verify("sprites/player_mercenary/elucidate_mercenary_move_up_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_mercenary_move_up_002.png"); _g_done_assets += 1
	verify("sprites/player_mercenary/elucidate_mercenary_sprite_idle_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_mercenary_right_004.png"); _g_done_assets += 1
	verify("sprites/player_mercenary/elucidate_mercenary_move_right_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_mercenary_move_right_001.png"); _g_done_assets += 1
	verify("sprites/player_mercenary/elucidate_mercenary_move_right_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_mercenary_move_right_002.png"); _g_done_assets += 1
	verify("sprites/player_mercenary/elucidate_mercenary_sprite_idle_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_mercenary_left_003.png"); _g_done_assets += 1
	verify("sprites/player_mercenary/elucidate_mercenary_move_left_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_mercenary_move_left_001.png"); _g_done_assets += 1
	verify("sprites/player_mercenary/elucidate_mercenary_move_left_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_mercenary_move_left_002.png"); _g_done_assets += 1
	verify("sprites/player_mercenary/elucidate_mercenary_sprite_idle_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_mercenary_down_002.png"); _g_done_assets += 1
	verify("sprites/player_mercenary/elucidate_mercenary_move_down_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_mercenary_move_down_001.png"); _g_done_assets += 1
	verify("sprites/player_mercenary/elucidate_mercenary_move_down_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_mercenary_move_down_002.png"); _g_done_assets += 1
	verify("sprites/npc_e_s2_corrupted_cultist/elucidate_idle_corrupted2_cultist_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_corrupted2_cultist_npc_up.png"); _g_done_assets += 1
	verify("sprites/npc_e_s2_corrupted_cultist/elucidate_idle_corrupted2_cultist_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_corrupted2_cultist_npc_right.png"); _g_done_assets += 1
	verify("sprites/npc_e_s2_corrupted_cultist/elucidate_idle_corrupted2_cultist_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_corrupted2_cultist_npc_left.png"); _g_done_assets += 1
	verify("sprites/npc_e_s2_corrupted_cultist/elucidate_idle_corrupted2_cultist_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_corrupted2_cultist_npc_down.png"); _g_done_assets += 1
	verify("sprites/npc_e_luminarian_spy/elucidate_walk_church_spy_npc_right_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walk_church_spy_npc_right_001.png"); _g_done_assets += 1
	verify("sprites/npc_n_ghost_memories/elucidate_idle_ghost_memory2_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_ghost_memory2_npc_left.png"); _g_done_assets += 1
	verify("sprites/player_mercenary/elucidate_atk_sprite_mercenary_up_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_atk_sprite_mercenary_up_001.png"); _g_done_assets += 1
	verify("sprites/player_mercenary/elucidate_atk_sprite_mercenary_up_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_atk_sprite_mercenary_up_002.png"); _g_done_assets += 1
	verify("sprites/player_mercenary/elucidate_atk_sprite_mercenary_right_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_atk_sprite_mercenary_right_001.png"); _g_done_assets += 1
	verify("sprites/player_mercenary/elucidate_atk_sprite_mercenary_right_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_atk_sprite_mercenary_right_002.png"); _g_done_assets += 1
	verify("sprites/player_mercenary/elucidate_atk_sprite_mercenary_left_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_atk_sprite_mercenary_left_001.png"); _g_done_assets += 1
	verify("sprites/player_mercenary/elucidate_atk_sprite_mercenary_left_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_atk_sprite_mercenary_left_002.png"); _g_done_assets += 1
	verify("sprites/player_mercenary/elucidate_atk_sprite_mercenary_down_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_atk_sprite_mercenary_down_001.png"); _g_done_assets += 1
	verify("sprites/player_mercenary/elucidate_atk_sprite_mercenary_down_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_atk_sprite_mercenary_down_002.png"); _g_done_assets += 1
	verify("wiki_images/wiki_elucidate_characterspage.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/wiki_elucidate_characterspage.png"); _g_done_assets += 1
	verify("wiki_images/wiki_elucidate_developerspage.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/wiki_elucidate_developerspage.png"); _g_done_assets += 1
	verify("wiki_images/wiki_elucidate_downloadpage.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/wiki_elucidate_downloadpage.png"); _g_done_assets += 1
	verify("wiki_images/wiki_elucidate_environmentspage1.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/wiki_elucidate_environmentspage1.png"); _g_done_assets += 1
	verify("wiki_images/wiki_elucidate_environmentspage2.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/wiki_elucidate_environmentspage2.png"); _g_done_assets += 1
	verify("wiki_images/wiki_elucidate_fanartspage.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/wiki_elucidate_fanartspage.png"); _g_done_assets += 1
	verify("wiki_images/wiki_elucidate_homepage.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/wiki_elucidate_homepage.png"); _g_done_assets += 1
	verify("wiki_images/wiki_elucidate_itemspage1.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/wiki_elucidate_itemspage1.png"); _g_done_assets += 1
	verify("wiki_images/wiki_elucidate_itemspage2.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/wiki_elucidate_itemspage2.png"); _g_done_assets += 1
	verify("wiki_images/wiki_elucidate_lorepage.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/wiki_elucidate_lorepage.png"); _g_done_assets += 1
	verify("wiki_images/wiki_elucidate_npcspage1.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/wiki_elucidate_npcspage1.png"); _g_done_assets += 1
	verify("wiki_images/wiki_elucidate_npcspage2.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/wiki_elucidate_npcspage2.png"); _g_done_assets += 1
	verify("wiki_images/ELUCIDATE-WEBSITE-EYE-LOGO.png","http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/ELUCIDATE-WEBSITE-EYE-LOGO.png"); _g_done_assets += 1

y_offset = 25
if os.path.exists("music/elucidate_calm.wav"):
	screen.fill((0, 0, 0))
	draw_text("music/elucidate_calm.wav", 5, y_offset)
	draw_text(" | file verified.", 5, y_offset + 20)
	pygame.draw.rect(screen, (160, 160, 145), (0, 0, screen_x, screen_y), 1)
	pygame.display.flip()
else:
	zip_download("https://drive.google.com/uc?id=1gYxGbDhVr-5FWPb3sxbgW3_h2VsJHBS5")
if os.path.exists("music/elucidate_depths.wav"):
	screen.fill((0, 0, 0))
	draw_text("music/elucidate_depths.wav", 5, y_offset)
	draw_text(" | file verified.", 5, y_offset + 20)
	pygame.draw.rect(screen, (160, 160, 145), (0, 0, screen_x, screen_y), 1)
	pygame.display.flip()
else:
	zip_download("https://drive.google.com/uc?id=1gYxGbDhVr-5FWPb3sxbgW3_h2VsJHBS5")
if os.path.exists("music/elucidate_end.wav"):
	screen.fill((0, 0, 0))
	draw_text("music/elucidate_end.wav", 5, y_offset)
	draw_text(" | file verified.", 5, y_offset + 20)
	pygame.draw.rect(screen, (160, 160, 145), (0, 0, screen_x, screen_y), 1)
	pygame.display.flip()
else:
	zip_download("https://drive.google.com/uc?id=1gYxGbDhVr-5FWPb3sxbgW3_h2VsJHBS5")
if os.path.exists("music/elucidate_last_battle.wav"):
	screen.fill((0, 0, 0))
	draw_text("music/elucidate_last_battle.wav", 5, y_offset)
	draw_text(" | file verified.", 5, y_offset + 20)
	pygame.draw.rect(screen, (160, 160, 145), (0, 0, screen_x, screen_y), 1)
	pygame.display.flip()
else:
	zip_download("https://drive.google.com/uc?id=1gYxGbDhVr-5FWPb3sxbgW3_h2VsJHBS5")
if os.path.exists("music/elucidate_losing_it.wav"):
	screen.fill((0, 0, 0))
	draw_text("music/elucidate_losing_it.wav", 5, y_offset)
	draw_text(" | file verified.", 5, y_offset + 20)
	pygame.draw.rect(screen, (160, 160, 145), (0, 0, screen_x, screen_y), 1)
	pygame.display.flip()
else:
	zip_download("https://drive.google.com/uc?id=1gYxGbDhVr-5FWPb3sxbgW3_h2VsJHBS5")
if os.path.exists("music/elucidate_menu.wav"):
	screen.fill((0, 0, 0))
	draw_text("music/elucidate_menu.wav", 5, y_offset)
	draw_text(" | file verified.", 5, y_offset + 20)
	pygame.draw.rect(screen, (160, 160, 145), (0, 0, screen_x, screen_y), 1)
	pygame.display.flip()
else:
	zip_download("https://drive.google.com/uc?id=1gYxGbDhVr-5FWPb3sxbgW3_h2VsJHBS5")
if os.path.exists("music/elucidate_tense.wav"):
	screen.fill((0, 0, 0))
	draw_text("music/elucidate_tense.wav", 5, y_offset)
	draw_text(" | file verified.", 5, y_offset + 20)
	pygame.draw.rect(screen, (160, 160, 145), (0, 0, screen_x, screen_y), 1)
	pygame.display.flip()
else:
	zip_download("https://drive.google.com/uc?id=1gYxGbDhVr-5FWPb3sxbgW3_h2VsJHBS5")
if os.path.exists("music/elucidate_the_dark.wav"):
	screen.fill((0, 0, 0))
	draw_text("music/elucidate_the_dark.wav", 5, y_offset)
	draw_text(" | file verified.", 5, y_offset + 20)
	pygame.draw.rect(screen, (160, 160, 145), (0, 0, screen_x, screen_y), 1)
	pygame.display.flip()
else:
	zip_download("https://drive.google.com/uc?id=1gYxGbDhVr-5FWPb3sxbgW3_h2VsJHBS5")
if os.path.exists("music/elucidate_the_wait.wav"):
	screen.fill((0, 0, 0))
	draw_text("music/elucidate_the_wait.wav", 5, y_offset)
	draw_text(" | file verified.", 5, y_offset + 20)
	pygame.draw.rect(screen, (160, 160, 145), (0, 0, screen_x, screen_y), 1)
	pygame.display.flip()

else:
	zip_download("https://drive.google.com/uc?id=1gYxGbDhVr-5FWPb3sxbgW3_h2VsJHBS5")

py_clock = pygame.time.Clock()
logic_tick = 60
render_fps = 60
walls = []

screen.fill((0, 0, 0))
try:
	_title_img = pygame.image.load("images/elucidate_title.png")
	_title_resized = pygame.transform.scale(_title_img, (screen_x // 2, screen_y // 2))
	screen.blit(_title_resized, (screen_x // 4, screen_y // 4))
	_sel_img = pygame.image.load("images/elucidate_select_full.png")
	_sel_resized = pygame.transform.scale(_sel_img, (screen_x // 2, 30))
	screen.blit(_sel_resized, (screen_x // 4, screen_y - 115))
except Exception:
	pass
_load_font_a = pygame.font.SysFont("Times New Roman", 25)
_load_font_b = pygame.font.SysFont("Times New Roman", 20)
_load_surf_a = _load_font_a.render("Loading Assets", True, (255, 255, 255))
_load_rect_a = _load_surf_a.get_rect(center=(screen_x // 2, screen_y - 100))
screen.blit(_load_surf_a, _load_rect_a)
_load_surf_b = _load_font_b.render("Loading...", True, (255, 255, 255))
_load_rect_b = _load_surf_b.get_rect(center=(screen_x // 2, screen_y - 20))
screen.blit(_load_surf_b, _load_rect_b)
pygame.display.flip()
for ev in pygame.event.get():
	if ev.type == pygame.QUIT:
		pygame.quit()
		sys.exit()

fonts = {
	10: pygame.font.SysFont("Times New Roman", 10),
	15: pygame.font.SysFont("Times New Roman", 15),
	20: pygame.font.SysFont("Times New Roman", 20),
	25: pygame.font.SysFont("Times New Roman", 25),
	30: pygame.font.SysFont("Times New Roman", 30),
	35: pygame.font.SysFont("Times New Roman", 35),
	40: pygame.font.SysFont("Times New Roman", 40),
	45: pygame.font.SysFont("Times New Roman", 45),
	50: pygame.font.SysFont("Times New Roman", 50),
	55: pygame.font.SysFont("Times New Roman", 55),
	60: pygame.font.SysFont("Times New Roman", 60),
	80: pygame.font.SysFont("Times New Roman", 80),
}
_hex_decode_cache = {}


def _load(rel, alpha=False):
	try:
		img = pygame.image.load(rel)
		return img.convert_alpha() if alpha else img.convert()
	except Exception:
		surf = pygame.Surface((72, 72))
		surf.fill((255, 0, 255))
		return surf


_preloaded_images = {
	"elucidate_title": _load("images/elucidate_title.png"),
	"elucidate_version_select_001": _load("images/elucidate_version_select_001.png"),
	"elucidate_version_select_002": _load("images/elucidate_version_select_002.png"),
	"elucidate_version_select_003": _load("images/elucidate_version_select_003.png"),
	"elucidate_version_select_004": _load("images/elucidate_version_select_004.png"),
	"elucidate_version_select_005": _load("images/elucidate_version_select_005.png"),
	"elucidate_middle_gradient_001": _load("images/elucidate_middle_gradient_001.png", True),
	"elucidate_launcher_bg": _load("images/elucidate_bg_launcher_001.png"),
}

_sc = pygame.transform.scale
_scaled_images = {
	"elucidate_middle_gradient_001": _sc(_preloaded_images["elucidate_middle_gradient_001"], (200, 30)),
	"elucidate_middle_gradient_002": _sc(_preloaded_images["elucidate_middle_gradient_001"], (300, 30)),
}

sys_bg_color = (0, 0, 0)
sys_bd_color_sc_area = (180, 180, 180)
sys_audio_volume = 1.0
ui_white = (245, 245, 245)
ui_crimson = (160, 0, 0)
ui_dark_crimson = (120, 0, 0)
ui_gray = (180, 180, 180)
sys_audio_muted = False
sys_controls_mode = "keyboard"


def sys_tick(n):
	py_clock.tick(n)


def elucidate_sys_exit():
	pygame.quit()
	sys.exit()


def display():
	pygame.display.flip()
	if render_fps == 0:
		py_clock.tick()
	else:
		py_clock.tick(render_fps)


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

_dust_particles = []
_dust_color = (180, 160, 130)
_dust_surf_cache = None

def effects_dust(rgb):
	global _dust_particles, _dust_color, _dust_surf_cache
	_dust_color = rgb

	for _ in range(4):
		_dust_particles.append({
			"x": random.uniform(0, screen_x),
			"y": random.uniform(screen_y * 0.6, screen_y + 10),
			"vx": random.uniform(-0.4, 0.4),
			"vy": random.uniform(-0.8, -0.2),
			"size": random.randint(1, 3),
			"alpha": random.randint(60, 200),
			"life": 0.0,
			"max_life": random.uniform(0.6, 1.0),
		})
	if _dust_surf_cache is None or _dust_surf_cache.get_size() != (screen_x, screen_y):
		_dust_surf_cache = pygame.Surface((screen_x, screen_y), pygame.SRCALPHA)
	_psurf = _dust_surf_cache
	_psurf.fill((0, 0, 0, 0))
	keep = []
	for p in _dust_particles:
		p["life"] += 0.016
		if p["life"] >= p["max_life"]:
			continue
		p["x"] += p["vx"]
		p["y"] += p["vy"]
		frac = p["life"] / p["max_life"]
		a = int(p["alpha"] * (1.0 - frac))
		a = max(0, min(255, a))
		r, g, b = _dust_color
		pygame.draw.circle(_psurf, (r, g, b, a), (int(p["x"]), int(p["y"])), p["size"])
		keep.append(p)
	_dust_particles = keep
	screen.blit(_psurf, (0, 0))


_vt_pulse = 0.0

def _version_text_hover(label, y, mx, my, size=60):
	"""Draw a version label; glows gold when the mouse is near."""
	global _vt_pulse
	_vt_pulse += 0.07
	fnt = sys_font(size)
	surf = fnt.render(label, True, (255, 255, 255))
	rect = surf.get_rect(center=(screen_x / 2, y))
	hovered = rect.collidepoint(mx, my)
	if hovered:

		glow_alpha = int(80 + 60 * math.sin(_vt_pulse))
		glow_surf = fnt.render(label, True, (128, 0, 120))
		glow_surf.set_alpha(glow_alpha)
		for ox, oy in ((-2, 0), (2, 0), (0, -2), (0, 2)):
			screen.blit(glow_surf, rect.move(ox, oy))

		screen.blit(surf, rect)
	else:

		bri = int(200 + 55 * (0.5 + 0.5 * math.sin(_vt_pulse * 0.5)))
		dim_surf = fnt.render(label, True, (bri, bri, bri))
		screen.blit(dim_surf, rect)

state = "main_hub"

_btn_downloads = pygame.Rect(1224, 3, 49, 49)
_btn_email     = pygame.Rect(1224, 66, 49, 49)
_btn_feedback  = pygame.Rect(1224, 129, 49, 49)
_btn_website   = pygame.Rect(1224, 193, 49, 49)
_btn_fanart    = pygame.Rect(1224, 257, 49, 49)

screen_x, screen_y = 1275, 710
screen = pygame.display.set_mode((screen_x, screen_y))
play = pygame.Rect((screen_x / 2) - 50, (screen_y / 2) - 35, 100, 30)
jhvb = pygame.Rect((screen_x / 2) - 50, (screen_y / 2) + 5, 300, 30)

_hint_font_cached = pygame.font.SysFont("Times New Roman", 13)
_hint_surf_cached = _hint_font_cached.render(
	"F9: Cycle Theme  |  F8: Mini-game  |  F12: Debug", True, (100, 100, 100)
)
del _hint_font_cached

while True:
	events = pygame.event.get()
	for event in events:
		if event.type == pygame.QUIT:
			elucidate_sys_exit()
	mouse_x, mouse_y = pygame.mouse.get_pos()
	screen.fill((0, 0, 0))
	screen.blit(_preloaded_images["elucidate_launcher_bg"], (0, 0))

	static_text_raw_center("PLAY", color=(255, 255, 255), position=(screen_x / 2, int((screen_y / 2)) - 20), size=30)
	static_text_raw_center("SELECT VERSION", color=(255, 255, 255), position=(screen_x / 2, int((screen_y / 2)) + 20),
						   size=30)
	static_text_raw_center("2026 All Rights Reserved. Powered By FGC Productions", color=(180, 180, 180),
						   position=(screen_x / 2, screen_y - 30), size=15)

	screen.blit(_hint_surf_cached, (8, screen_y - 16))

	for event in events:
		if event.type == pygame.MOUSEBUTTONDOWN:
			if _btn_downloads.collidepoint(mouse_x, mouse_y):
				webbrowser.open("https://elucidate.unaux.com/downloads-page/")
			if _btn_email.collidepoint(mouse_x, mouse_y):
				webbrowser.open("mailto:marcrodenfamero@gmail.com")
			if _btn_feedback.collidepoint(mouse_x, mouse_y):
				webbrowser.open("https://docs.google.com/forms/d/e/1FAIpQLSfm4NG2MSFb_70hxthK6vTZtddUYbYSkgOtg7aRkBfhiApX2Q/viewform?usp=dialog")
			if _btn_website.collidepoint(mouse_x, mouse_y):
				webbrowser.open("https://elucidate.unaux.com")
			if _btn_fanart.collidepoint(mouse_x, mouse_y):
				webbrowser.open("https://elucidate.unaux.com/fanart-page/")

	if play.collidepoint(mouse_x, mouse_y):
		screen.blit(_scaled_images["elucidate_middle_gradient_001"], ((screen_x // 2) - 100, (screen_y / 2) - 35))
		static_text_raw_center("PLAY", color=(0, 0, 0), position=(screen_x / 2, int((screen_y / 2)) - 20), size=30)
		for event in events:
			if event.type == pygame.MOUSEBUTTONDOWN:
				try:
					_append_activity("Launched game (PLAY button)")
					from main import *
				except Exception as _launch_err:
					_err_font = pygame.font.SysFont("Times New Roman", 20)
					_err_msg = f"Could not launch game: {_launch_err}"
					for _t in range(180):
						screen.fill((20, 0, 0))
						screen.blit(_err_font.render(_err_msg[:120], True, (255, 80, 80)), (40, screen_y // 2 - 20))
						screen.blit(
							_err_font.render("Press any key or wait to return to launcher.", True, (200, 200, 200)),
							(40, screen_y // 2 + 20))
						pygame.display.flip()
						py_clock.tick(60)
						_ev2 = pygame.event.get()
						if any(e.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN) for e in _ev2):
							break
	if jhvb.collidepoint(mouse_x, mouse_y):
		screen.blit(_scaled_images["elucidate_middle_gradient_002"], ((screen_x // 2) - 150, (screen_y / 2) + 5))
		static_text_raw_center("SELECT VERSION", color=(0, 0, 0), position=(screen_x / 2, int((screen_y / 2)) + 20),
							   size=30)
		for event in events:
			if event.type == pygame.MOUSEBUTTONDOWN:
				loop = True
				log1 = pygame.Rect(260, 106, 748, 105)
				log2 = pygame.Rect(263, 237, 748, 105)
				log3 = pygame.Rect(263, 370, 748, 105)
				log4 = pygame.Rect(263, 500, 748, 105)
				bg = 0
				while loop:
					events = pygame.event.get()
					for event in events:
						if event.type == pygame.QUIT:
							elucidate_sys_exit()
					mouse_x, mouse_y = pygame.mouse.get_pos()
					screen.fill((0, 0, 0))
					if bg == 1:
						screen.blit(_preloaded_images["elucidate_version_select_002"], (0, 0))
					elif bg == 2:
						screen.blit(_preloaded_images["elucidate_version_select_003"], (0, 0))
					elif bg == 3:
						screen.blit(_preloaded_images["elucidate_version_select_004"], (0, 0))
					elif bg == 4:
						screen.blit(_preloaded_images["elucidate_version_select_005"], (0, 0))
					else:
						screen.blit(_preloaded_images["elucidate_version_select_001"], (0, 0))
					bg = 0
					if log1.collidepoint(mouse_x, mouse_y):
						bg = 1
						for event in events:
							if event.type == pygame.MOUSEBUTTONDOWN:
								zip_download("https://drive.google.com/uc?id=1s40HslBSWJcNEXwDmPc2I5ev3ioMNgyH")
								_append_activity("Downloaded: Elucidate Beta 1.1.0")
								loop = False
					if log2.collidepoint(mouse_x, mouse_y):
						bg = 2
						for event in events:
							if event.type == pygame.MOUSEBUTTONDOWN:
								zip_download("https://drive.google.com/uc?id=19PQ7We-MLvs831EruOYa4JwBwhjwy0eJ")
								loop = False
					if log3.collidepoint(mouse_x, mouse_y):
						bg = 3
						for event in events:
							if event.type == pygame.MOUSEBUTTONDOWN:
								zip_download("https://drive.google.com/uc?id=1jM_SHQFU4MVnOnqWUvfvgEef_oDyMt-J")
								loop = False
					if log4.collidepoint(mouse_x, mouse_y):
						bg = 4
						for event in events:
							if event.type == pygame.MOUSEBUTTONDOWN:
								zip_download("https://drive.google.com/uc?id=1CJ02Ljh6tbMY9ITGgZQYwg0mfQUqj-1F")
								loop = False
					_version_text_hover("Elucidate Beta 1.1.0",    165, mouse_x, mouse_y, size=60)
					_version_text_hover("Elucidate Alpha 1.0.244", 295, mouse_x, mouse_y, size=60)
					_version_text_hover("Elucidate Alpha 1.0.204", 430, mouse_x, mouse_y, size=60)
					_version_text_hover("Elucidate Alpha 1.0.185", 555, mouse_x, mouse_y, size=60)
					effects_dust((140, 140, 140))
					display()
	display()