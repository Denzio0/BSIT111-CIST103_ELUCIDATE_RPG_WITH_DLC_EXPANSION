# =============================================================================
#  elucidate_devkit.py  —  v2.0
#  Elucidate RPG  —  Developer / Debug Toolkit
#  © 2026  Group WOZ | FGC UNAUX  —  All Rights Reserved
#
#  ─────────────────────────────────────────────────────────────────────────────
#  QUICK-START (3 steps)
#  ─────────────────────────────────────────────────────────────────────────────
#  1. Place this file next to NPC_SIMULATION_AND_MAP_RECT_TOOL.py
#
#  2. Add at the very top of main.py (after existing imports):
#         from elucidate_devkit import ElucidateDevKit
#
#  3. See "═══ INSERTION GUIDE ═══" at the bottom of this file for the exact
#     paste blocks for every insertion point.
#
#  ─────────────────────────────────────────────────────────────────────────────
#  SECRET ACTIVATION
#  ─────────────────────────────────────────────────────────────────────────────
#  All dev hotkeys are LOCKED during normal play.
#  Hold  CAPS LOCK  then press  A  to toggle Developer Mode ON / OFF.
#  (FN key cannot be detected in pygame — CAPS LOCK + A is the practical
#   equivalent: it is a chord that never occurs in normal gameplay.)
#
#  When ENABLED a small "DEVELOPER MODE ENABLED" banner appears top-center.
#  When DISABLED a "DEVELOPER MODE DISABLED" banner appears, then fades.
#  All F1-F12 tools are completely inert while dev mode is OFF.
#
#  ─────────────────────────────────────────────────────────────────────────────
#  HOTKEY TABLE  (only active while Developer Mode is ON)
#  ─────────────────────────────────────────────────────────────────────────────
#  Key   Function
#  ───── ──────────────────────────────────────────────────────────────────────
#  F1    Warp Creator  — draw warp zones visually, auto-prints code to terminal
#  F2    Rect Visualiser — toggle all registered / drawn collision rects
#  F3    No-Clip — player ignores wall collisions
#  F4    Give Item Console — type: give <name> <qty|=N|-N|remove>
#  F5    Inventory Editor — visual +/- editor for live inventory dict
#  F6    Apply Effects — cycle test effect onto player
#  F7    NPC Spawner — type sprite key + mode, click to place
#  F8    Rect Draw Tool  [MIGRATED from main.py F8]
#  F9    NPC Debug Tool  [MIGRATED from main.py F9]
#  F10   Debug Panel — FPS, map, coords, NPC count, effects
#  F11   Save / Load Test slot  (SHIFT+F11 = load)
#  F12   Master Dev Menu — button overlay for all tools
# =============================================================================

import pygame
import json
import os
import time
import random as _random

# ---------------------------------------------------------------------------
#  GUARD — set ELUCIDATE_DEV=0 to completely disable all overhead in release
# ---------------------------------------------------------------------------
DEV_MODE = os.environ.get("ELUCIDATE_DEV", "1") != "0"

# ---------------------------------------------------------------------------
#  Colour palette
# ---------------------------------------------------------------------------
_C = {
    "bg":          (10,  10,  10,  210),
    "border":      (160,  0,   0),
    "border_dim":  (80,  80,  75),
    "text":        (220, 215, 205),
    "text_dim":    (130, 125, 115),
    "text_hi":     (255, 255, 255),
    "green":       (80,  220,  80),
    "cyan":        (0,   220, 255),
    "yellow":      (255, 220,  60),
    "orange":      (255, 140,   0),
    "red":         (220,  60,  60),
    "blue":        (80,  140, 255),
    "purple":      (180,  80, 255),
    "warp":        (0,   200, 255),
    "collision":   (255,  60,  60),
    "npc":         (80,  255, 140),
    "event":       (255, 220,  60),
    "custom":      (200, 200, 200),
}

# ---------------------------------------------------------------------------
#  Effect definitions used by F6
# ---------------------------------------------------------------------------
EFFECT_DEFS = {
    "speed_boost":    {"stat": "speed",    "delta": +1,  "label": "Speed Boost"},
    "speed_slow":     {"stat": "speed",    "delta": -1,  "label": "Slowed"},
    "defense_buff":   {"stat": "defense",  "delta": +10, "label": "Defense Buff"},
    "defense_debuff": {"stat": "defense",  "delta": -10, "label": "Defense Debuff"},
    "damage_buff":    {"stat": "damage",   "delta": +5,  "label": "Damage Buff"},
    "mind_boost":     {"stat": "mind_res", "delta": +1,  "label": "Mind Boost"},
    "poison":         {"stat": "hp",       "delta": -5,  "label": "Poison",       "tick": True},
    "regen":          {"stat": "hp",       "delta": +5,  "label": "Regeneration", "tick": True},
    "cursed":         {"stat": "damage",   "delta": -8,  "label": "Cursed"},
    "mana_restore":   {"stat": "mind",     "delta": +20, "label": "Mana Restore"},
}


# =============================================================================
#  ElucidateDevKit  —  main class
# =============================================================================
class ElucidateDevKit:
    """
    All developer systems in one object.

    Constructor arguments
    ---------------------
    screen      : pygame.Surface  — the main display surface
    fonts       : dict            — {size: pygame.font.Font, ...}
    get_state   : callable()      — returns current state string
    set_state   : callable(s)     — sets state string in main.py
    npc_sprites : dict            — the SPRITES dict from main.py (for F7/F9 previews)
    NPC_class   : class           — your NPC class (pass None to disable spawning)
    pyperclip   : module|None     — pass pyperclip if available, else None
    """

    # ------------------------------------------------------------------
    #  INIT
    # ------------------------------------------------------------------
    def __init__(self, screen, fonts, get_state, set_state,
                 npc_sprites=None, NPC_class=None, pyperclip=None):
        if not DEV_MODE:
            return

        self.screen      = screen
        self.fonts       = fonts
        self.get_state   = get_state
        self.set_state   = set_state
        self._SPRITES    = npc_sprites or {}
        self._NPC_class  = NPC_class
        self._pyperclip  = pyperclip

        sx, sy = screen.get_size()
        self._sx = sx
        self._sy = sy

        # ── shared font shortcuts ──────────────────────────────────────
        self._f10 = fonts.get(10, pygame.font.SysFont("Times New Roman", 10))
        self._f15 = fonts.get(15, pygame.font.SysFont("Times New Roman", 15))
        self._f20 = fonts.get(20, pygame.font.SysFont("Times New Roman", 20))
        self._f25 = fonts.get(25, pygame.font.SysFont("Times New Roman", 25))
        self._f30 = fonts.get(30, pygame.font.SysFont("Times New Roman", 30))
        self._fcode = pygame.font.SysFont("Courier New", 13)
        self._fcode_sm = pygame.font.SysFont("Courier New", 11)

        # ── SECRET ACTIVATION ─────────────────────────────────────────
        self.dev_enabled       = False
        self._dev_banner_text  = ""
        self._dev_banner_timer = 0.0

        # ── F1  WARP CREATOR ──────────────────────────────────────────
        self._warp_active       = False
        self._warp_drawing      = False
        self._warp_start_wx     = 0
        self._warp_start_wy     = 0
        self._warp_rects        = []     # list of (wx,wy,ww,wh,label)
        self._warp_label_ctr    = [0]
        self._warps_registered  = {}     # map_id -> list of WarpDef (runtime warps)
        self._warp_debug_vis    = False

        # ── F2  RECT VISUALISER ───────────────────────────────────────
        self._rect_debug     = False
        self._rect_registry  = []        # list of {rect, label, type}

        # ── F3  NO-CLIP ───────────────────────────────────────────────
        self.noclip = False

        # ── F4  GIVE ITEM ─────────────────────────────────────────────
        self._give_open     = False
        self._give_input    = ""
        self._give_feedback = ""
        self._give_fb_timer = 0

        # ── F5  INVENTORY EDITOR ──────────────────────────────────────
        self._inv_editor_open = False

        # ── F6  EFFECTS ───────────────────────────────────────────────
        self._active_effects  = []

        # ── F7  NPC SPAWNER (text-console style) ──────────────────────
        self._npc_console_open  = False
        self._npc_console_input = ""
        self._npc_console_fb    = ""
        self._npc_console_fb_t  = 0

        # ── F8  RECT DRAW TOOL  (migrated from main.py) ───────────────
        self._rdt_active       = False
        self._rdt_drawing      = False
        self._rdt_start_wx     = 0
        self._rdt_start_wy     = 0
        self._rdt_rects        = []      # list of (wx,wy,ww,wh,label)
        self._rdt_label_ctr    = [0]

        # ── F9  NPC DEBUG TOOL  (migrated from main.py) ───────────────
        self._ndt_active          = False
        self._ndt_npcs            = []
        self._ndt_labels          = []
        self._ndt_counter         = [0]
        self._ndt_mode            = "idle"
        self._ndt_sprite_index    = [0]
        self._ndt_interact_label  = [""]
        self._ndt_rename_idx      = 0
        self._ndt_sprite_keys     = [
            "no",
            "male_civilian","female_civilian","male_civilian_variant","female_civilian_variant",
            "male_villager","female_villager","male_villager_variant","female_villager_variant",
            "male_faithful_citizen","female_faithful_citizen","chuAttendants",
            "supply_merchant","male_market_merchant","female_market_merchant","tavern_keeper",
            "travelling_merchant","travelling_bard","blacksmith",
            "merchant_guild_master","merchant_guild_member","harbor_captain",
            "tribe_warrior","female_tribal_warrior","tribe_elder","tribe_chief",
            "guards","guard_captain","draft_officer","holyknight","librarian_scholar",
            "church_spy_npc","church_assassin_npc","church_medical_staff",
            "mercenary","cultist","priest","shaman","merchant",
            "cultist_soldier","cultist_archer_npc","cultist_channeler_npc",
            "cultist_priest","cult_leader",
            "corrupted1_cultist","corrupted2_cultist","corrupted3_cultist",
            "amalgamated_villagers","amalgamated_knights","amalgamated_civilians",
            "melted_male_villager","melted_female_villager",
            "caligo_manifestation",
            "imprisoned_experiment_1","imprisoned_experiment_2","imprisoned_experiment_hostile",
        ]
        self._ndt_categories = {
            "CIVILIAN": ["no","male_civilian","female_civilian","male_civilian_variant",
                         "female_civilian_variant","male_villager","female_villager",
                         "male_villager_variant","female_villager_variant",
                         "male_faithful_citizen","female_faithful_citizen","chuAttendants"],
            "MERCHANT": ["supply_merchant","male_market_merchant","female_market_merchant",
                         "tavern_keeper","travelling_merchant","travelling_bard","blacksmith",
                         "merchant_guild_master","merchant_guild_member","harbor_captain"],
            "TRIBE":    ["tribe_warrior","female_tribal_warrior","tribe_elder","tribe_chief"],
            "MILITARY": ["guards","guard_captain","draft_officer","holyknight","librarian_scholar",
                         "church_spy_npc","church_assassin_npc","church_medical_staff"],
            "STORY":    ["mercenary","cultist","priest","shaman","merchant"],
            "CULTIST":  ["cultist_soldier","cultist_archer_npc","cultist_channeler_npc",
                         "cultist_priest","cult_leader"],
            "CORRUPT":  ["corrupted1_cultist","corrupted2_cultist","corrupted3_cultist",
                         "amalgamated_villagers","amalgamated_knights","amalgamated_civilians"],
            "MELTED":   ["melted_male_villager","melted_female_villager"],
            "SPECIAL":  ["caligo_manifestation","imprisoned_experiment_1",
                         "imprisoned_experiment_2","imprisoned_experiment_hostile"],
        }
        self._all_maps = [
            "map_01","map_02","map_03","map_04","map_05","map_06","map_07","map_08",
            "map_09","map_10","map_11","map_12","map_13","map_14","map_15","map_16",
            "map_17","map_18","map_19","map_20","map_21","map_22","map_23","map_24",
            "map_25","map_26","map_27","map_28","map_29","map_30","map_31","map_32",
            "map_33","map_34","map_35","map_36","map_37","map_38","map_39","map_40",
            "map_41","map_42","map_43","map_44","map_46","map_47","map_48",
            "map_49","map_50","map_51","map_52","map_53",
        ]

        # ── F10 DEBUG PANEL ───────────────────────────────────────────
        self._debug_panel = True

        # ── F11 SAVE / LOAD ───────────────────────────────────────────
        self._save_slot  = {}
        self._save_fb    = ""
        self._save_fb_t  = 0

        # ── F12 MASTER MENU ───────────────────────────────────────────
        self._menu_open    = False
        self._menu_buttons = self._build_menu_buttons()

        # ── NOTIFICATION QUEUE ────────────────────────────────────────
        self._notifications = []   # [(text, expire_time)]

    # ==================================================================
    #  ── SECRET ACTIVATION  (CAPS LOCK + A) ───────────────────────────
    # ==================================================================

    def _check_secret_combo(self, event):
        """
        Call this inside the event loop BEFORE any F-key routing.
        Returns True if the combo was detected (event consumed).

        How it works
        ─────────────
        pygame reports CAPS LOCK state via pygame.key.get_mods().
        When CAPS LOCK is ACTIVE (LED on) and the user presses A,
        pygame.KMOD_CAPS is set in event.mod.

        This is the closest practical equivalent to FN+CAPS LOCK+A:
          • CAPS LOCK must be toggled ON  (LED lit)
          • Then press  A
        In normal gameplay, typing with CAPS LOCK on + pressing A
        would produce an uppercase 'A' — a character that has no
        binding in the game's control scheme, making the combo safe.

        To use SHIFT+CAPS LOCK+A instead, also require:
            event.mod & pygame.KMOD_SHIFT
        """
        if not DEV_MODE:
            return False
        if event.type != pygame.KEYDOWN:
            return False
        if event.key == pygame.K_a and (event.mod & pygame.KMOD_CAPS):
            self.dev_enabled = not self.dev_enabled
            if self.dev_enabled:
                self._dev_banner_text  = "DEVELOPER MODE ENABLED"
                self._dev_banner_timer = time.time() + 3.0
                self._notify("DEV MODE ON  —  F1-F12 unlocked")
                print("\n[ ELUCIDATE DEVKIT ] DEVELOPER MODE ENABLED — F1-F12 active")
            else:
                self._dev_banner_text  = "DEVELOPER MODE DISABLED"
                self._dev_banner_timer = time.time() + 2.0
                self._notify("DEV MODE OFF")
                print("[ ELUCIDATE DEVKIT ] DEVELOPER MODE DISABLED")
            return True
        return False

    def _draw_dev_banner(self):
        """Draw the DEVELOPER MODE ENABLED / DISABLED banner."""
        if not DEV_MODE or not self._dev_banner_text:
            return
        now = time.time()
        remaining = self._dev_banner_timer - now
        if remaining <= 0:
            self._dev_banner_text = ""
            return
        alpha = min(255, int(remaining / 0.5 * 255))
        col   = _C["green"] if "ENABLED" in self._dev_banner_text else _C["red"]
        lbl   = self._f25.render(self._dev_banner_text, True, col)
        surf  = pygame.Surface(lbl.get_size(), pygame.SRCALPHA)
        surf.blit(lbl, (0, 0))
        surf.set_alpha(alpha)
        self.screen.blit(surf, (self._sx // 2 - lbl.get_width() // 2, 18))

    # ==================================================================
    #  ── MASTER HOTKEY HANDLER ─────────────────────────────────────────
    # ==================================================================

    def handle_hotkeys(self, event, p=None, inventory_dict=None,
                       npc_list=None, world_x=0, world_y=0, mouse_pos=None):
        """
        Call inside the event loop for EVERY event.

        Parameters
        ----------
        event          : pygame.event
        p              : Player object
        inventory_dict : live inventory dict (e.g. {"Short Sword":1, ...})
        npc_list       : live list of NPC objects (appended to by F7/F9)
        world_x        : camera scroll X
        world_y        : camera scroll Y
        mouse_pos      : (mx, my) from pygame.mouse.get_pos()

        Returns True if the event was consumed by the devkit.
        """
        if not DEV_MODE:
            return False

        # Secret combo check — always runs regardless of dev_enabled
        if self._check_secret_combo(event):
            return True

        # Everything below requires dev mode to be active
        if not self.dev_enabled:
            return False

        if event.type != pygame.KEYDOWN and event.type != pygame.MOUSEBUTTONDOWN \
                and event.type != pygame.MOUSEBUTTONUP and event.type != pygame.MOUSEMOTION:
            return False

        mx, my = mouse_pos if mouse_pos else pygame.mouse.get_pos()

        # ── Text-input sub-menus get priority ─────────────────────────
        if self._give_open:
            if event.type == pygame.KEYDOWN:
                self._handle_give_key(event, inventory_dict or {})
                return True
        if self._npc_console_open:
            if event.type == pygame.KEYDOWN:
                self._handle_npc_console_key(event, npc_list or [], p, world_x, world_y)
                return True

        # ── F9 NPC DEBUG TOOL: mouse & keys ───────────────────────────
        if self._ndt_active:
            if event.type == pygame.KEYDOWN:
                consumed = self._ndt_handle_key(event, p, npc_list or [], world_x, world_y, mx, my)
                if consumed:
                    return True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not self._rdt_active:
                    self._ndt_place(mx, my, world_x, world_y, npc_list or [])
                    return True

        # ── F8 RECT DRAW TOOL: mouse ──────────────────────────────────
        if self._rdt_active:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not self._ndt_active:
                    self._rdt_drawing  = True
                    self._rdt_start_wx = int(mx + world_x)
                    self._rdt_start_wy = int(my + world_y)
                    return True
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self._rdt_drawing:
                    self._rdt_finish(mx, my, world_x, world_y)
                    return True

        # ── F-key dispatch ────────────────────────────────────────────
        if event.type != pygame.KEYDOWN:
            return False
        k = event.key

        if k == pygame.K_F1:
            self._toggle_warp_creator()
            return True
        if k == pygame.K_F2:
            self.toggle_rect_debug()
            return True
        if k == pygame.K_F3:
            self.toggle_noclip()
            return True
        if k == pygame.K_F4:
            self._give_open = not self._give_open
            self._give_input = ""
            return True
        if k == pygame.K_F5:
            self._inv_editor_open = not self._inv_editor_open
            return True
        if k == pygame.K_F6:
            self._cycle_test_effect(p)
            return True
        if k == pygame.K_F7:
            self._npc_console_open = not self._npc_console_open
            self._npc_console_input = ""
            return True
        if k == pygame.K_F8:
            self._rdt_active   = not self._rdt_active
            self._rdt_drawing  = False
            state_str = "ON" if self._rdt_active else "OFF"
            self._notify(f"Rect Draw Tool: {state_str}")
            if self._rdt_active:
                print("[ F8 RECT TOOL ] ON  |  Click+Drag=draw  |  Backspace=undo  |  C=clear  |  G=print code")
            return True
        if k == pygame.K_F9:
            self._ndt_active = not self._ndt_active
            self._ndt_interact_label[0] = ""
            state_str = "ON" if self._ndt_active else "OFF"
            self._notify(f"NPC Debug Tool: {state_str}")
            if self._ndt_active:
                print("[ F9 NPC TOOL ] ON  |  Click=place  Tab=mode  Arrows=sprite  M/N=map  G=code  R=rename  Backspace=undo  C=clear")
            return True
        if k == pygame.K_F10:
            self.toggle_debug_panel()
            return True
        if k == pygame.K_F11:
            if event.mod & pygame.KMOD_SHIFT:
                if p and inventory_dict is not None:
                    self.load_test(p, inventory_dict)
            else:
                if p and inventory_dict is not None:
                    self.save_test(p, inventory_dict)
            return True
        if k == pygame.K_F12:
            self._menu_open = not self._menu_open
            return True

        # ── F8 tool backspace / clear ──────────────────────────────────
        if self._rdt_active:
            if k == pygame.K_BACKSPACE:
                if self._rdt_rects:
                    self._rdt_rects.pop()
                    return True
            if k == pygame.K_c:
                self._rdt_rects.clear()
                self._rdt_label_ctr[0] = 0
                return True
            if k == pygame.K_g:
                self._rdt_print_code()
                return True

        return False

    # ==================================================================
    #  ── SECTION F1 :  WARP CREATOR ────────────────────────────────────
    # ==================================================================

    def _toggle_warp_creator(self):
        self._warp_active     = not self._warp_active
        self._warp_drawing    = False
        self._warp_debug_vis  = self._warp_active
        state_str = "ON" if self._warp_active else "OFF"
        self._notify(f"Warp Creator: {state_str}")
        if self._warp_active:
            print("[ F1 WARP CREATOR ] ON  |  Click+Drag=draw zone  |  Backspace=undo  |  G=print code")

    def handle_warp_draw(self, event, world_x, world_y, mouse_pos=None):
        """
        Call inside event loop. Handles mouse events for the warp creator.
        Call this from handle_hotkeys or separately.
        """
        if not DEV_MODE or not self.dev_enabled or not self._warp_active:
            return
        mx, my = mouse_pos if mouse_pos else pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._warp_drawing    = True
            self._warp_start_wx   = int(mx + world_x)
            self._warp_start_wy   = int(my + world_y)
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self._warp_drawing:
            self._warp_drawing = False
            cur_wx = int(mx + world_x)
            cur_wy = int(my + world_y)
            rx = min(self._warp_start_wx, cur_wx)
            ry = min(self._warp_start_wy, cur_wy)
            rw = abs(cur_wx - self._warp_start_wx)
            rh = abs(cur_wy - self._warp_start_wy)
            if rw > 2 and rh > 2:
                self._warp_label_ctr[0] += 1
                label = f"warp_{self._warp_label_ctr[0]}"
                self._warp_rects.append((rx, ry, rw, rh, label))
                print(f"[ WARP ZONE ] {label}: Rect({rx},{ry},{rw},{rh})")
                print(f"  devkit.create_warp({rx},{ry},{rw},{rh}, target_x=?, target_y=?, target_state='?', map_id='{self.get_state()}')")
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE and self._warp_rects:
                self._warp_rects.pop()
            if event.key == pygame.K_g:
                self._warp_print_code()

    def create_warp(self, rect_x, rect_y, w, h, target_x, target_y,
                    target_state, map_id="*", enabled=True, label=""):
        """Register a runtime warp zone (used in production code, not just debug)."""
        if not DEV_MODE:
            return
        entry = {
            "rect":         pygame.Rect(rect_x, rect_y, w, h),
            "target_x":     target_x,
            "target_y":     target_y,
            "target_state": target_state,
            "map_id":       map_id,
            "enabled":      enabled,
            "label":        label or f"warp→{target_state}",
        }
        self._warps_registered.setdefault(map_id, []).append(entry)

    def process_warps(self, p, current_state):
        """Call every update frame. Returns True + teleports if player hits a warp."""
        if not DEV_MODE:
            return False
        pools = self._warps_registered.get(current_state, []) + \
                self._warps_registered.get("*", [])
        p_rect = p.get_rect() if hasattr(p, "get_rect") else \
                 pygame.Rect(p.x, p.y, 32, 32)
        for w in pools:
            if not w["enabled"]:
                continue
            if w["map_id"] not in ("*", current_state):
                continue
            if p_rect.colliderect(w["rect"]):
                p.x = w["target_x"]
                p.y = w["target_y"]
                self.set_state(w["target_state"])
                self._notify(f"Warped → {w['target_state']} ({w['target_x']},{w['target_y']})")
                return True
        return False

    def draw_warps(self, world_x=0, world_y=0):
        """Render warp zone overlays. Call inside render block."""
        if not DEV_MODE or not self._warp_debug_vis:
            return
        state = self.get_state()
        pools = self._warps_registered.get(state, []) + \
                self._warps_registered.get("*", [])
        for w in pools:
            r  = w["rect"]
            sx = r.x - int(world_x)
            sy = r.y - int(world_y)
            col = _C["warp"]
            s  = pygame.Surface((r.w, r.h), pygame.SRCALPHA)
            s.fill((*col, 50))
            self.screen.blit(s, (sx, sy))
            pygame.draw.rect(self.screen, col, (sx, sy, r.w, r.h), 2)
            lbl = self._fcode_sm.render(w["label"], True, col)
            self.screen.blit(lbl, (sx + 2, sy + 2))
        # Also draw F1 creator zones
        mx, my = pygame.mouse.get_pos()
        for (rx, ry, rw, rh, label) in self._warp_rects:
            sx = rx - int(world_x)
            sy = ry - int(world_y)
            s  = pygame.Surface((rw, rh), pygame.SRCALPHA)
            s.fill((*_C["warp"], 55))
            self.screen.blit(s, (sx, sy))
            pygame.draw.rect(self.screen, _C["warp"], (sx, sy, rw, rh), 2)
            lbl2 = self._fcode_sm.render(label, True, _C["warp"])
            self.screen.blit(lbl2, (sx + 2, sy + 2))
            out  = self._fcode_sm.render(f"Rect({rx},{ry},{rw},{rh})", True, _C["cyan"])
            self.screen.blit(out, (sx + 2, sy + 14))

    def _warp_print_code(self):
        print("\n# ── F1 WARP CREATOR — Generated Code ───────────────────────")
        state = self.get_state()
        print(f"# Map: {state}")
        for (rx, ry, rw, rh, label) in self._warp_rects:
            print(f"# {label}")
            print(f"devkit.create_warp({rx},{ry},{rw},{rh}, target_x=?, target_y=?, target_state='?', map_id='{state}')")
        print("# ─────────────────────────────────────────────────────────────\n")

    # ==================================================================
    #  ── SECTION F2 :  RECT VISUALISER ────────────────────────────────
    # ==================================================================

    def register_rect(self, rect, label="", rect_type="custom"):
        """Register a pygame.Rect for visual debug display."""
        if not DEV_MODE:
            return
        self._rect_registry.append({"rect": rect, "label": label, "type": rect_type})

    def register_rects_bulk(self, rect_list, label_prefix="", rect_type="custom"):
        for i, r in enumerate(rect_list):
            self.register_rect(r, f"{label_prefix}{i}", rect_type)

    def clear_rects(self):
        self._rect_registry.clear()

    def toggle_rect_debug(self):
        if not DEV_MODE:
            return
        self._rect_debug = not self._rect_debug
        self._notify("Rect debug: " + ("ON" if self._rect_debug else "OFF"))

    def draw_rects(self, world_x=0, world_y=0):
        """Render all registered rects. Call inside render block."""
        if not DEV_MODE or not self._rect_debug:
            return
        for entry in self._rect_registry:
            r   = entry["rect"]
            col = _C.get(entry["type"], _C["custom"])
            sx  = r.x - int(world_x)
            sy  = r.y - int(world_y)
            s   = pygame.Surface((r.w, r.h), pygame.SRCALPHA)
            s.fill((*col, 40))
            self.screen.blit(s, (sx, sy))
            pygame.draw.rect(self.screen, col, (sx, sy, r.w, r.h), 1)
            if entry["label"]:
                lbl = self._fcode_sm.render(entry["label"], True, col)
                self.screen.blit(lbl, (sx + 2, sy + 2))
                dim = self._fcode_sm.render(f"({r.x},{r.y},{r.w},{r.h})", True, _C["text_dim"])
                self.screen.blit(dim, (sx + 2, sy + 12))

    # ==================================================================
    #  ── SECTION F3 :  NO-CLIP ─────────────────────────────────────────
    # ==================================================================

    def toggle_noclip(self):
        if not DEV_MODE:
            return
        self.noclip = not self.noclip
        self._notify("No-clip: " + ("ON" if self.noclip else "OFF"))

    def apply_noclip(self, p=None, walls=None):
        """
        Returns True if no-clip is ON (skip wall collision).
        Usage in main.py update block:
            if not devkit.apply_noclip():
                p.move(walls + entity_walls)
        """
        return DEV_MODE and self.dev_enabled and self.noclip

    # ==================================================================
    #  ── SECTION F4 :  GIVE ITEM CONSOLE ──────────────────────────────
    # ==================================================================

    def _handle_give_key(self, event, inv):
        if event.key == pygame.K_RETURN:
            self._execute_give(self._give_input.strip(), inv)
            self._give_input = ""
        elif event.key == pygame.K_BACKSPACE:
            self._give_input = self._give_input[:-1]
        elif event.key == pygame.K_ESCAPE:
            self._give_open = False
        else:
            self._give_input += event.unicode

    def _execute_give(self, cmd, inv):
        if not cmd:
            return
        parts = cmd.rsplit(" ", 1)
        if len(parts) != 2:
            self._give_feedback = "[!] Syntax: give <item name> <amount|=N|-N|remove>"
            self._give_fb_timer = time.time() + 3
            return
        item_name, amount_str = parts[0].strip(), parts[1].strip()
        if amount_str.lower() == "remove":
            if item_name in inv:
                del inv[item_name]
                self._give_feedback = f"[OK] Removed '{item_name}'"
            else:
                self._give_feedback = f"[!] '{item_name}' not in inventory"
            self._give_fb_timer = time.time() + 3
            self._notify(self._give_feedback)
            return
        try:
            if amount_str.startswith("="):
                mode, val = "set", int(amount_str[1:])
            elif amount_str.startswith("-"):
                mode, val = "sub", int(amount_str[1:])
            else:
                mode, val = "add", int(amount_str)
        except ValueError:
            self._give_feedback = f"[!] Bad amount: '{amount_str}'"
            self._give_fb_timer = time.time() + 3
            return
        current = inv.get(item_name, 0)
        if mode == "set":
            inv[item_name] = val
        elif mode == "sub":
            inv[item_name] = max(0, current - val)
        else:
            inv[item_name] = current + val
        self._give_feedback = f"[OK] {item_name} {mode} {val}  → now {inv[item_name]}"
        self._give_fb_timer = time.time() + 3
        self._notify(self._give_feedback)

    def draw_give_menu(self):
        if not DEV_MODE or not self.dev_enabled or not self._give_open:
            return
        bw, bh = 520, 105
        bx = self._sx // 2 - bw // 2
        by = self._sy // 2 - bh // 2
        s  = pygame.Surface((bw, bh), pygame.SRCALPHA)
        s.fill((12, 12, 12, 235))
        self.screen.blit(s, (bx, by))
        pygame.draw.rect(self.screen, _C["yellow"], (bx, by, bw, bh), 1)
        self._txt(self.screen, "F4  GIVE ITEM  —  ESC to close",
                  _C["yellow"], (bx + 10, by + 8), self._f15)
        self._txt(self.screen, "give <name> <qty>  |  =N set  |  -N remove  |  remove delete",
                  _C["text_dim"], (bx + 10, by + 26), self._fcode_sm)
        self._txt(self.screen, f"> {self._give_input}_",
                  _C["text_hi"], (bx + 10, by + 52), self._f20)
        if self._give_feedback and time.time() < self._give_fb_timer:
            col = _C["green"] if "[OK]" in self._give_feedback else _C["red"]
            self._txt(self.screen, self._give_feedback, col, (bx + 10, by + 82), self._fcode_sm)

    # ==================================================================
    #  ── SECTION F5 :  INVENTORY VISUAL EDITOR ─────────────────────────
    # ==================================================================

    def draw_inv_editor(self, inventory_dict, events=None):
        """
        Render a scrollable +/- inventory editor.
        Call inside render block, pass the live frame's event list.
        """
        if not DEV_MODE or not self.dev_enabled or not self._inv_editor_open:
            return
        pw, ph = 370, min(430, self._sy - 80)
        px = self._sx - pw - 10
        py = 40
        bg = pygame.Surface((pw, ph), pygame.SRCALPHA)
        bg.fill((12, 12, 12, 225))
        self.screen.blit(bg, (px, py))
        pygame.draw.rect(self.screen, _C["yellow"], (px, py, pw, ph), 1)
        self._txt(self.screen, "F5  INVENTORY EDITOR",
                  _C["yellow"], (px + 8, py + 6), self._f15)
        self._txt(self.screen, "Click +/- to adjust",
                  _C["text_dim"], (px + 8, py + 23), self._fcode_sm)
        items   = list(inventory_dict.items())
        row_h   = 22
        visible = (ph - 50) // row_h
        mx, my  = pygame.mouse.get_pos()
        for i, (name, count) in enumerate(items[:visible]):
            ry = py + 40 + i * row_h
            hover = py + 40 + i * row_h <= my < py + 40 + (i + 1) * row_h and px <= mx < px + pw
            if hover:
                pygame.draw.rect(self.screen, (30, 30, 30), (px + 2, ry, pw - 4, row_h - 1))
            self._txt(self.screen, name, _C["text"], (px + 8, ry + 4), self._fcode_sm)
            self._txt(self.screen, str(count), _C["cyan"], (px + 250, ry + 4), self._fcode_sm)
            plus_r  = pygame.Rect(px + pw - 46, ry + 2, 18, 18)
            minus_r = pygame.Rect(px + pw - 24, ry + 2, 18, 18)
            pygame.draw.rect(self.screen, (30, 60, 30), plus_r)
            pygame.draw.rect(self.screen, (60, 30, 30), minus_r)
            self._txt(self.screen, "+", _C["green"],  (plus_r.x + 4, plus_r.y + 2), self._fcode_sm)
            self._txt(self.screen, "-", _C["red"],    (minus_r.x + 5, minus_r.y + 2), self._fcode_sm)
            if events:
                for ev in events:
                    if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                        if plus_r.collidepoint(ev.pos):
                            inventory_dict[name] = count + 1
                        if minus_r.collidepoint(ev.pos):
                            inventory_dict[name] = max(0, count - 1)
        if len(items) > visible:
            self._txt(self.screen,
                      f"… {len(items) - visible} more not shown",
                      _C["text_dim"], (px + 8, py + ph - 16), self._fcode_sm)

    # ==================================================================
    #  ── SECTION F6 :  PLAYER EFFECTS ──────────────────────────────────
    # ==================================================================

    def apply_effect(self, p, effect_key, duration_seconds=10):
        """Apply a named effect from EFFECT_DEFS to the player."""
        if not DEV_MODE:
            return
        if effect_key not in EFFECT_DEFS:
            self._notify(f"[!] Unknown effect: {effect_key}")
            return
        defn  = EFFECT_DEFS[effect_key]
        entry = {
            "key":       effect_key,
            "defn":      defn,
            "expires":   time.time() + duration_seconds,
            "tick":      defn.get("tick", False),
            "last_tick": time.time(),
            "applied":   False,
        }
        self._active_effects = [e for e in self._active_effects if e["key"] != effect_key]
        self._active_effects.append(entry)
        self._notify(f"Effect: {defn['label']}  ({duration_seconds}s)")

    def update_effects(self, p):
        """Call once per update frame."""
        if not DEV_MODE:
            return
        now   = time.time()
        alive = []
        for e in self._active_effects:
            if now > e["expires"]:
                if e["applied"] and not e["tick"]:
                    stat  = e["defn"]["stat"]
                    delta = e["defn"]["delta"]
                    if hasattr(p, stat):
                        setattr(p, stat, getattr(p, stat) - delta)
                self._notify(f"Effect expired: {e['defn']['label']}")
                continue
            if not e["tick"] and not e["applied"]:
                stat  = e["defn"]["stat"]
                delta = e["defn"]["delta"]
                if hasattr(p, stat):
                    setattr(p, stat, getattr(p, stat) + delta)
                e["applied"] = True
            if e["tick"] and now - e["last_tick"] >= 1.0:
                stat  = e["defn"]["stat"]
                delta = e["defn"]["delta"]
                if hasattr(p, stat):
                    setattr(p, stat, max(0, getattr(p, stat) + delta))
                e["last_tick"] = now
            alive.append(e)
        self._active_effects = alive

    def draw_effects_hud(self):
        """Render small effect pills in top-right corner."""
        if not DEV_MODE or not self.dev_enabled or not self._active_effects:
            return
        now = time.time()
        for i, e in enumerate(self._active_effects):
            remaining = max(0, e["expires"] - now)
            label = f"{e['defn']['label']}  {remaining:.1f}s"
            col   = _C["purple"]
            w     = self._fcode_sm.size(label)[0] + 10
            rx    = self._sx - w - 5
            ry    = 5 + i * 18
            pygame.draw.rect(self.screen, (30, 0, 40), (rx, ry, w, 14))
            pygame.draw.rect(self.screen, col, (rx, ry, w, 14), 1)
            self._txt(self.screen, label, col, (rx + 5, ry + 2), self._fcode_sm)

    def _cycle_test_effect(self, p):
        keys = list(EFFECT_DEFS.keys())
        if not keys or p is None:
            return
        chosen = _random.choice(keys)
        self.apply_effect(p, chosen, duration_seconds=8)

    # ==================================================================
    #  ── SECTION F7 :  NPC SPAWNER (text console) ──────────────────────
    # ==================================================================

    def _handle_npc_console_key(self, event, npc_list, p, world_x, world_y):
        if event.key == pygame.K_RETURN:
            self._npc_console_execute(self._npc_console_input.strip(), npc_list, p)
            self._npc_console_input = ""
        elif event.key == pygame.K_BACKSPACE:
            self._npc_console_input = self._npc_console_input[:-1]
        elif event.key == pygame.K_ESCAPE:
            self._npc_console_open = False
        else:
            self._npc_console_input += event.unicode

    def _npc_console_execute(self, cmd, npc_list, p):
        if not cmd or self._NPC_class is None:
            if self._NPC_class is None:
                self._npc_console_fb   = "[!] NPC_class not provided to DevKit constructor"
                self._npc_console_fb_t = time.time() + 3
            return
        parts  = cmd.split()
        modes  = ("idle", "roaming", "hostile", "companion")
        mode   = parts[-1] if len(parts) > 1 and parts[-1] in modes else "idle"
        sprite = " ".join(parts[:-1]) if len(parts) > 1 and parts[-1] in modes else cmd
        state  = self.get_state()
        try:
            npc = self._NPC_class([state], state,
                                   int(p.x) + 80, int(p.y), 7000, 3500, sprite)
            if hasattr(npc, "mode"):
                npc.mode = mode
            npc_list.append(npc)
            self._npc_console_fb = f"[OK] Spawned '{sprite}' ({mode}) at ({int(p.x)+80},{int(p.y)})"
        except Exception as err:
            self._npc_console_fb = f"[!] Spawn failed: {err}"
        self._npc_console_fb_t = time.time() + 3
        self._notify(self._npc_console_fb)

    def draw_npc_console(self):
        if not DEV_MODE or not self.dev_enabled or not self._npc_console_open:
            return
        bw, bh = 520, 95
        bx = self._sx // 2 - bw // 2
        by = self._sy // 2 + 60
        s  = pygame.Surface((bw, bh), pygame.SRCALPHA)
        s.fill((12, 12, 12, 235))
        self.screen.blit(s, (bx, by))
        pygame.draw.rect(self.screen, _C["green"], (bx, by, bw, bh), 1)
        self._txt(self.screen, "F7  NPC SPAWNER  —  ESC to close",
                  _C["green"], (bx + 10, by + 6), self._f15)
        self._txt(self.screen, "Syntax:  <sprite_key> [idle|roaming|hostile|companion]",
                  _C["text_dim"], (bx + 10, by + 22), self._fcode_sm)
        self._txt(self.screen, f"> {self._npc_console_input}_",
                  _C["text_hi"], (bx + 10, by + 44), self._f20)
        if self._npc_console_fb and time.time() < self._npc_console_fb_t:
            col = _C["green"] if "[OK]" in self._npc_console_fb else _C["red"]
            self._txt(self.screen, self._npc_console_fb, col, (bx + 10, by + 72), self._fcode_sm)

    # ==================================================================
    #  ── SECTION F8 :  RECT DRAW TOOL  (migrated from main.py) ─────────
    # ==================================================================

    def _rdt_finish(self, mx, my, world_x, world_y):
        self._rdt_drawing = False
        cur_wx = int(mx + world_x)
        cur_wy = int(my + world_y)
        rx = min(self._rdt_start_wx, cur_wx)
        ry = min(self._rdt_start_wy, cur_wy)
        rw = abs(cur_wx - self._rdt_start_wx)
        rh = abs(cur_wy - self._rdt_start_wy)
        if rw > 2 and rh > 2:
            self._rdt_label_ctr[0] += 1
            label = f"rect_{self._rdt_label_ctr[0]}"
            self._rdt_rects.append((rx, ry, rw, rh, label))
            line = f"{label} = pygame.Rect({rx}, {ry}, {rw}, {rh})"
            print(line)
            if self._pyperclip:
                all_output = "\n".join(
                    f"{r[4]} = pygame.Rect({r[0]}, {r[1]}, {r[2]}, {r[3]})"
                    for r in self._rdt_rects
                )
                try:
                    self._pyperclip.copy(all_output)
                except Exception:
                    pass

    def _rdt_print_code(self):
        print("\n# ── F8 RECT DRAW TOOL — All Rects ──────────────────────────")
        for (rx, ry, rw, rh, label) in self._rdt_rects:
            print(f"{label} = pygame.Rect({rx}, {ry}, {rw}, {rh})")
        print("# ─────────────────────────────────────────────────────────────\n")

    def draw_rdt(self, world_x=0, world_y=0, mouse_pos=None):
        """Render the rect draw tool overlay. Call inside render block."""
        if not DEV_MODE or not self.dev_enabled or not self._rdt_active:
            return
        mx, my = mouse_pos if mouse_pos else pygame.mouse.get_pos()
        cur_wx = int(mx + world_x)
        cur_wy = int(my + world_y)
        # Finalized rects
        for (rx, ry, rw, rh, label) in self._rdt_rects:
            sx = rx - int(world_x)
            sy = ry - int(world_y)
            s  = pygame.Surface((rw, rh), pygame.SRCALPHA)
            s.fill((255, 100, 0, 55))
            self.screen.blit(s, (sx, sy))
            pygame.draw.rect(self.screen, (255, 140, 0), (sx, sy, rw, rh), 2)
            lbl = self._fcode_sm.render(label, True, (255, 220, 0))
            self.screen.blit(lbl, (sx + 2, sy - 14))
            out = self._fcode_sm.render(f"pygame.Rect({rx},{ry},{rw},{rh})", True, (255, 255, 180))
            self.screen.blit(out, (sx + 2, sy + 2))
        # Live drag preview
        if self._rdt_drawing:
            drag_wx = int(mx + world_x)
            drag_wy = int(my + world_y)
            rx = min(self._rdt_start_wx, drag_wx)
            ry = min(self._rdt_start_wy, drag_wy)
            rw = abs(drag_wx - self._rdt_start_wx)
            rh = abs(drag_wy - self._rdt_start_wy)
            sx = rx - int(world_x)
            sy = ry - int(world_y)
            if rw > 0 and rh > 0:
                s2 = pygame.Surface((rw, rh), pygame.SRCALPHA)
                s2.fill((0, 200, 255, 60))
                self.screen.blit(s2, (sx, sy))
                pygame.draw.rect(self.screen, (0, 220, 255), (sx, sy, rw, rh), 2)
        # HUD
        hx = 5
        hy = self._sy - 140
        pygame.draw.rect(self.screen, (0, 0, 0), (hx - 2, hy - 2, 370, 136))
        pygame.draw.rect(self.screen, (255, 140, 0), (hx - 2, hy - 2, 370, 136), 1)
        self._txt(self.screen, "[ F8: RECT TOOL ]  Backspace=undo  C=clear  G=code",
                  (255, 200, 0), (hx, hy), self._fcode_sm)
        self._txt(self.screen, f"Mouse World  X:{cur_wx}  Y:{cur_wy}",
                  (200, 255, 200), (hx, hy + 16), self._fcode_sm)
        if self._rdt_drawing:
            dw = abs(cur_wx - self._rdt_start_wx)
            dh = abs(cur_wy - self._rdt_start_wy)
            self._txt(self.screen, f"Drawing...  W:{dw}  H:{dh}  Start({self._rdt_start_wx},{self._rdt_start_wy})",
                      (0, 220, 255), (hx, hy + 32), self._fcode_sm)
        else:
            self._txt(self.screen, "Click+Drag to draw a rectangle",
                      (160, 160, 160), (hx, hy + 32), self._fcode_sm)
        self._txt(self.screen, f"Rects saved: {len(self._rdt_rects)}",
                  (200, 200, 200), (hx, hy + 64), self._fcode_sm)
        if self._rdt_rects:
            rx, ry, rw, rh, label = self._rdt_rects[-1]
            self._txt(self.screen, f"Last: pygame.Rect({rx},{ry},{rw},{rh})",
                      (255, 255, 100), (hx, hy + 80), self._fcode_sm)
            self._txt(self.screen, f"      {label}", (255, 220, 100), (hx, hy + 96), self._fcode_sm)

    # ==================================================================
    #  ── SECTION F9 :  NPC DEBUG TOOL  (migrated from main.py) ─────────
    # ==================================================================

    def _ndt_place(self, mx, my, world_x, world_y, npc_list):
        sk    = self._ndt_sprite_keys[self._ndt_sprite_index[0]]
        wx    = int(mx + world_x)
        wy    = int(my + world_y)
        self._ndt_counter[0] += 1
        label = f"npc_{self._ndt_counter[0]}_{sk}"
        if self._NPC_class is not None:
            try:
                new_npc = self._NPC_class(
                    [self._ndt_mode], self._ndt_mode,
                    wx, wy, 7000, 3500, sk
                )
                self._ndt_npcs.append(new_npc)
                self._ndt_labels.append(label)
                npc_list.append(new_npc)
                print(f'[ PLACED ] {label} = NPC(["{self._ndt_mode}"], "{self._ndt_mode}", {wx}, {wy}, 7000, 3500, "{sk}")')
            except Exception as err:
                self._notify(f"[!] NPC place failed: {err}")
        else:
            self._notify("[!] NPC_class not provided to DevKit constructor")

    def _ndt_handle_key(self, event, p, npc_list, world_x, world_y, mx, my):
        k = event.key
        modes = ["idle", "roaming", "hostile", "companion"]
        consumed = False
        if k == pygame.K_TAB:
            self._ndt_mode = modes[(modes.index(self._ndt_mode) + 1) % len(modes)]
            self._notify(f"NPC mode → {self._ndt_mode.upper()}")
            consumed = True
        elif k == pygame.K_LEFT:
            self._ndt_sprite_index[0] = (self._ndt_sprite_index[0] - 1) % len(self._ndt_sprite_keys)
            self._notify(f"Sprite → {self._ndt_sprite_keys[self._ndt_sprite_index[0]]}")
            consumed = True
        elif k == pygame.K_RIGHT:
            self._ndt_sprite_index[0] = (self._ndt_sprite_index[0] + 1) % len(self._ndt_sprite_keys)
            self._notify(f"Sprite → {self._ndt_sprite_keys[self._ndt_sprite_index[0]]}")
            consumed = True
        elif k == pygame.K_BACKSPACE:
            if self._ndt_npcs:
                removed = self._ndt_labels.pop()
                self._ndt_npcs.pop()
                # also remove from npc_list if present
                if npc_list and npc_list:
                    try:
                        npc_list.pop()
                    except Exception:
                        pass
                self._notify(f"Removed: {removed}")
            consumed = True
        elif k == pygame.K_c:
            # Remove devkit-placed NPCs from the live list
            for dn in self._ndt_npcs:
                try:
                    npc_list.remove(dn)
                except ValueError:
                    pass
            self._ndt_npcs.clear()
            self._ndt_labels.clear()
            self._ndt_counter[0] = 0
            self._notify("NPC tool: cleared all debug NPCs")
            consumed = True
        elif k == pygame.K_g:
            self._ndt_print_code()
            consumed = True
        elif k == pygame.K_d:
            if self._ndt_npcs:
                src = self._ndt_npcs[-1]
                self._ndt_counter[0] += 1
                if self._NPC_class is not None:
                    try:
                        dup   = self._NPC_class([src.state], src.state,
                                                 int(mx + world_x), int(my + world_y),
                                                 7000, 3500, src.sprite_key)
                        dlabel = f"npc_{self._ndt_counter[0]}_{src.sprite_key}_dup"
                        self._ndt_npcs.append(dup)
                        self._ndt_labels.append(dlabel)
                        npc_list.append(dup)
                        self._notify(f"Duplicated → {dlabel}")
                    except Exception as err:
                        self._notify(f"[!] Dup failed: {err}")
            consumed = True
        elif k == pygame.K_h:
            if self._ndt_npcs:
                ln = self._ndt_npcs[-1]
                ln.state = "hostile" if ln.state != "hostile" else "idle"
                ln.allowed_states = [ln.state]
                self._notify(f"{self._ndt_labels[-1]} → {ln.state}")
            consumed = True
        elif k == pygame.K_f:
            face_cycle = ["up", "down", "left", "right"]
            if self._ndt_npcs:
                ln = self._ndt_npcs[-1]
                cf = getattr(ln, "facing", "down")
                ln.facing    = face_cycle[(face_cycle.index(cf) + 1) % 4] \
                               if cf in face_cycle else "down"
                ln.direction = ln.facing
                self._notify(f"Facing → {ln.facing}")
            consumed = True
        elif k == pygame.K_r:
            preset_names = ["guard","villager","merchant","scholar","elder","chief",
                            "attendant","soldier","archer","spy","priest","bard","blacksmith"]
            if self._ndt_labels:
                new_name = preset_names[self._ndt_rename_idx % len(preset_names)]
                old      = self._ndt_labels[-1]
                self._ndt_labels[-1] = f"{new_name}_{self._ndt_counter[0]}_npc"
                self._ndt_rename_idx += 1
                self._notify(f"Renamed: {old} → {self._ndt_labels[-1]}")
            consumed = True
        elif k == pygame.K_m or k == pygame.K_n:
            cur_state = self.get_state()
            cur_idx   = self._all_maps.index(cur_state) \
                        if cur_state in self._all_maps else 0
            nxt_idx   = (cur_idx + 1) % len(self._all_maps) \
                        if k == pygame.K_m \
                        else (cur_idx - 1) % len(self._all_maps)
            next_map  = self._all_maps[nxt_idx]
            if p:
                p.x = float(self._sx // 2)
                p.y = float(self._sy // 2)
            self.set_state(next_map)
            for dn in self._ndt_npcs:
                try:
                    npc_list.remove(dn)
                except ValueError:
                    pass
            self._ndt_npcs.clear()
            self._ndt_labels.clear()
            self._ndt_counter[0] = 0
            self._notify(f"Map → {next_map}")
            consumed = True
        elif k == pygame.K_SLASH:
            cur_sk    = self._ndt_sprite_keys[self._ndt_sprite_index[0]]
            cats      = list(self._ndt_categories.values())
            found_cat = next((i for i, v in enumerate(cats) if cur_sk in v), 0)
            next_cat  = cats[(found_cat + 1) % len(cats)]
            first_sk  = next_cat[0]
            if first_sk in self._ndt_sprite_keys:
                self._ndt_sprite_index[0] = self._ndt_sprite_keys.index(first_sk)
            self._notify(f"Category → {first_sk}")
            consumed = True
        return consumed

    def _ndt_print_code(self):
        print("\n# ════════════════════════════════════════════════════")
        print(f"# F9 NPC DEBUG TOOL — Generated Code  |  Map: {self.get_state()}")
        print("# ════════════════════════════════════════════════════")
        if self._ndt_npcs:
            for npc, label in zip(self._ndt_npcs, self._ndt_labels):
                print(f'{label} = NPC(["{npc.state}"], "{npc.state}", {int(npc.x)}, {int(npc.y)}, 7000, 3500, "{npc.sprite_key}")')
            print(f"\n# Transition into {self.get_state()}:")
            print("npcs = []")
            print("entity_walls = []")
            print("npcs = [" + ", ".join(self._ndt_labels) + "]")
            print("\n# Before logic accumulator:")
            print("entity_walls = get_entity_walls(npcs, p)")
            print("\n# Inside logic accumulator after p.border():")
            print("for npc in npcs:")
            print("    npc.update(p, walls, npcs)")
            print("\n# In render section before p.draw():")
            print("for npc in npcs:")
            print("    npc.draw(screen, world_x, world_y)")
        else:
            print("# No debug NPCs placed yet.")
        print("# ════════════════════════════════════════════════════\n")

    def update_ndt(self, p, walls, world_x=0, world_y=0):
        """
        Call once per frame in the update block.
        Updates all F9 debug NPCs and sets the interact label.
        """
        if not DEV_MODE or not self.dev_enabled or not self._ndt_active:
            return
        self._ndt_interact_label[0] = ""
        cur_walls = walls if walls else []
        for npc in self._ndt_npcs:
            try:
                npc.update(p, cur_walls, [])
            except Exception:
                pass
            if abs(p.x - npc.x) < 80 and abs(p.y - npc.y) < 80:
                idx   = self._ndt_npcs.index(npc)
                label = self._ndt_labels[idx] if idx < len(self._ndt_labels) else "?"
                self._ndt_interact_label[0] = f"[E] {label}  |  {npc.state}  |  {npc.sprite_key}"

    def draw_ndt(self, world_x=0, world_y=0, mouse_pos=None):
        """Render the F9 NPC debug tool overlay. Call inside render block."""
        if not DEV_MODE or not self.dev_enabled or not self._ndt_active:
            return
        mx, my = mouse_pos if mouse_pos else pygame.mouse.get_pos()
        # Draw NPCs
        for npc, label in zip(self._ndt_npcs, self._ndt_labels):
            try:
                npc.draw(self.screen, world_x, world_y)
            except Exception:
                pass
            sx = int(npc.x - world_x)
            sy = int(npc.y - world_y)
            pygame.draw.rect(self.screen, (0, 255, 100), (sx, sy, 72, 72), 1)
            nl = self._fcode_sm.render(label, True, (100, 255, 100))
            self.screen.blit(nl, (sx, sy - 16))
            nc = self._fcode_sm.render(f"({int(npc.x)},{int(npc.y)})", True, (180, 255, 180))
            self.screen.blit(nc, (sx, sy + 74))
        # Ghost preview
        preview_sk = self._ndt_sprite_keys[self._ndt_sprite_index[0]]
        if preview_sk in self._SPRITES:
            try:
                ghost = self._SPRITES[preview_sk]["idle"]["down"].copy()
                ghost.set_alpha(130)
                self.screen.blit(ghost, (mx - 36, my - 36))
            except Exception:
                pass
        pygame.draw.rect(self.screen, (100, 255, 100), (mx - 36, my - 36, 72, 72), 1)
        # Interact label
        if self._ndt_interact_label[0]:
            ip = self._fcode.render(self._ndt_interact_label[0], True, (255, 255, 80))
            self.screen.blit(ip, (self._sx // 2 - ip.get_width() // 2, self._sy - 60))
        # HUD
        hx = self._sx - 430
        hy = 5
        pygame.draw.rect(self.screen, (0, 0, 0), (hx - 4, hy - 4, 429, 300))
        pygame.draw.rect(self.screen, (80, 220, 80), (hx - 4, hy - 4, 429, 300), 1)
        mode_col = {"idle":(160,160,255),"roaming":(255,220,80),"hostile":(255,80,80),"companion":(80,255,160)}
        lines = [
            ("[ F9: NPC DEBUG TOOL ]",  (80, 255, 80)),
            (f"Map: {self.get_state()}   M=next  N=prev", (255, 220, 80)),
            (f"Sprite [{self._ndt_sprite_index[0]+1}/{len(self._ndt_sprite_keys)}]: {preview_sk}", (180, 255, 180)),
            (f"Mode: {self._ndt_mode.upper()}   Tab=cycle", mode_col.get(self._ndt_mode, (255,255,255))),
            (f"Mouse World  X:{int(mx+world_x)}  Y:{int(my+world_y)}", (200, 200, 200)),
            (f"NPCs placed: {len(self._ndt_npcs)}   Backspace=undo  C=clear", (180, 180, 180)),
            ("Click=place  D=dup  H=hostile  F=face  R=rename  /=cat", (140, 140, 140)),
            ("G=print code  ←/→=sprite", (120, 120, 120)),
        ]
        for i, (text, col) in enumerate(lines):
            s = self._fcode_sm.render(text, True, col)
            self.screen.blit(s, (hx, hy + i * 16))
        # Category label
        cur_cat = next((c for c, keys in self._ndt_categories.items()
                        if preview_sk in keys), "OTHER")
        cat_surf = self._fcode_sm.render(f"Category: {cur_cat}", True, (120, 220, 255))
        self.screen.blit(cat_surf, (hx, hy + 136))
        # Sprite thumbnail
        if preview_sk in self._SPRITES:
            try:
                thumb = pygame.transform.scale(self._SPRITES[preview_sk]["idle"]["down"], (48, 48))
                self.screen.blit(thumb, (hx + 374, hy + 4))
                pygame.draw.rect(self.screen, (80, 220, 80), (hx + 374, hy + 4, 48, 48), 1)
            except Exception:
                pass
        # Last placed line
        if self._ndt_npcs:
            ln    = self._ndt_npcs[-1]
            ll    = self._ndt_labels[-1]
            ls    = self._fcode_sm.render(
                f'Last: {ll}=NPC(["{ln.state}"],"{ln.state}",{int(ln.x)},{int(ln.y)},7000,3500,"{ln.sprite_key}")',
                True, (255, 255, 120))
            self.screen.blit(ls, (hx - 100, hy + 154))
        # Mini list (last 5)
        for li, (ln2, ll2) in enumerate(zip(self._ndt_npcs[-5:], self._ndt_labels[-5:])):
            ls = self._fcode_sm.render(
                f"  {ll2}  ({int(ln2.x)},{int(ln2.y)})  [{ln2.state}]  {ln2.sprite_key}",
                True, (160, 220, 160))
            self.screen.blit(ls, (hx - 100, hy + 172 + li * 13))

    # ==================================================================
    #  ── SECTION F10 :  DEBUG PANEL ─────────────────────────────────────
    # ==================================================================

    def toggle_debug_panel(self):
        if not DEV_MODE:
            return
        self._debug_panel = not self._debug_panel

    def draw_debug_panel(self, p, clock, npc_list=None, walls=None):
        """
        Render the F10 debug overlay (top-left corner).
        clock     — pygame.time.Clock instance
        npc_list  — optional list of NPC objects
        walls     — optional list of wall rects
        """
        if not DEV_MODE or not self.dev_enabled or not self._debug_panel:
            return
        lines = [
            ("FPS",       f"{clock.get_fps():.1f}",                  _C["green"]),
            ("Player X",  f"{getattr(p,'x',0):.1f}",                 _C["cyan"]),
            ("Player Y",  f"{getattr(p,'y',0):.1f}",                 _C["cyan"]),
            ("HP",        str(getattr(p, "hp", "?")),                 _C["text"]),
            ("State",     str(self.get_state()),                      _C["yellow"]),
            ("No-Clip",   "ON" if self.noclip else "OFF",
                          _C["orange"] if self.noclip else _C["text_dim"]),
            ("Rects",     "ON" if self._rect_debug else "OFF",        _C["text_dim"]),
            ("RDT",       "ON" if self._rdt_active  else "OFF",       _C["text_dim"]),
            ("NDT",       "ON" if self._ndt_active  else "OFF",       _C["text_dim"]),
            ("NPCs",      str(len(npc_list)) if npc_list is not None else "?", _C["text"]),
            ("Walls",     str(len(walls))    if walls    is not None else "?", _C["text"]),
            ("Effects",   str(len(self._active_effects)),             _C["purple"]),
        ]
        pw = 210
        ph = len(lines) * 16 + 14
        bg = pygame.Surface((pw, ph), pygame.SRCALPHA)
        bg.fill((8, 8, 8, 205))
        self.screen.blit(bg, (4, 4))
        pygame.draw.rect(self.screen, _C["border_dim"], (4, 4, pw, ph), 1)
        self._txt(self.screen, "[ DEV PANEL ]", _C["border"], (8, 6), self._fcode_sm)
        for i, (key, val, col) in enumerate(lines):
            y = 20 + i * 16
            self._txt(self.screen, key, _C["text_dim"], (8,  y), self._fcode_sm)
            self._txt(self.screen, val, col,             (95, y), self._fcode_sm)

    # ==================================================================
    #  ── SECTION F11 :  SAVE / LOAD TEST SLOT ──────────────────────────
    # ==================================================================

    def save_test(self, p, inventory_dict, extra=None):
        """Snapshot player + inventory into a memory slot."""
        if not DEV_MODE:
            return
        self._save_slot = {
            "x":         getattr(p, "x",       0),
            "y":         getattr(p, "y",       0),
            "hp":        getattr(p, "hp",      0),
            "mind":      getattr(p, "mind",    0),
            "defense":   getattr(p, "defense", 0),
            "damage":    getattr(p, "damage",  0),
            "speed":     getattr(p, "speed",   0),
            "state":     self.get_state(),
            "inventory": dict(inventory_dict),
            "extra":     extra or {},
        }
        self._save_fb   = "[OK] Test slot saved"
        self._save_fb_t = time.time() + 2
        self._notify("Test slot saved")

    def load_test(self, p, inventory_dict):
        """Restore snapshot from memory slot."""
        if not DEV_MODE:
            return
        if not self._save_slot:
            self._save_fb   = "[!] No save slot — F11 to save first"
            self._save_fb_t = time.time() + 3
            return
        s = self._save_slot
        for attr in ("x", "y", "hp", "mind", "defense", "damage", "speed"):
            if attr in s and hasattr(p, attr):
                setattr(p, attr, s[attr])
        self.set_state(s.get("state", self.get_state()))
        inventory_dict.clear()
        inventory_dict.update(s.get("inventory", {}))
        self._save_fb   = "[OK] Test slot loaded"
        self._save_fb_t = time.time() + 2
        self._notify("Test slot loaded")

    def export_save_json(self, filepath="dev_save.json"):
        """Dump the test slot to a JSON file on disk."""
        if not DEV_MODE or not self._save_slot:
            return
        try:
            with open(filepath, "w") as f:
                json.dump(self._save_slot, f, indent=2)
            self._notify(f"Exported → {filepath}")
        except Exception as e:
            self._notify(f"Export failed: {e}")

    def draw_save_feedback(self):
        if not DEV_MODE or not self.dev_enabled:
            return
        if self._save_fb and time.time() < self._save_fb_t:
            col = _C["green"] if "[OK]" in self._save_fb else _C["red"]
            lbl = self._f15.render(self._save_fb, True, col)
            self.screen.blit(lbl, (self._sx // 2 - lbl.get_width() // 2, self._sy - 55))

    # ==================================================================
    #  ── SECTION F12 :  MASTER DEV MENU ────────────────────────────────
    # ==================================================================

    def _build_menu_buttons(self):
        return [
            ("Warp Creator",   "warp"),
            ("Rect Visualise", "rect_debug"),
            ("Rect Draw (F8)", "rdt"),
            ("NPC Tool (F9)",  "ndt"),
            ("No-Clip",        "noclip"),
            ("Give Item",      "give"),
            ("Inv Editor",     "inv_editor"),
            ("NPC Console",    "npc_console"),
            ("Debug Panel",    "debug_panel"),
            ("Save Test",      "save"),
            ("Load Test",      "load"),
            ("Export JSON",    "export"),
            ("Close Menu",     "close"),
        ]

    def draw_menu(self):
        if not DEV_MODE or not self.dev_enabled or not self._menu_open:
            return
        cols    = 3
        bw, bh  = 168, 38
        pad     = 8
        total_w = cols * bw + (cols - 1) * pad + 24
        rows    = (len(self._menu_buttons) + cols - 1) // cols
        total_h = rows * bh + (rows - 1) * pad + 54
        ox      = self._sx // 2 - total_w // 2
        oy      = self._sy // 2 - total_h // 2
        bg = pygame.Surface((total_w, total_h), pygame.SRCALPHA)
        bg.fill((10, 10, 10, 240))
        self.screen.blit(bg, (ox, oy))
        pygame.draw.rect(self.screen, _C["yellow"], (ox, oy, total_w, total_h), 2)
        self._txt(self.screen, "F12  MASTER DEV MENU  —  CAPS+A to toggle mode",
                  _C["yellow"], (ox + 10, oy + 10), self._f15)
        mx, my = pygame.mouse.get_pos()
        for i, (label, key) in enumerate(self._menu_buttons):
            ci = i % cols
            ri = i // cols
            bx = ox + 12 + ci * (bw + pad)
            by = oy + 44 + ri * (bh + pad)
            hover = bx <= mx < bx + bw and by <= my < by + bh
            active = (
                (key == "noclip"      and self.noclip)              or
                (key == "rect_debug"  and self._rect_debug)         or
                (key == "rdt"         and self._rdt_active)         or
                (key == "ndt"         and self._ndt_active)         or
                (key == "warp"        and self._warp_active)        or
                (key == "give"        and self._give_open)          or
                (key == "inv_editor"  and self._inv_editor_open)    or
                (key == "npc_console" and self._npc_console_open)   or
                (key == "debug_panel" and self._debug_panel)
            )
            border_col = _C["green"] if active else (_C["cyan"] if hover else _C["border_dim"])
            bg_col     = (0, 40, 0, 180) if active else (20, 20, 20, 200)
            bs = pygame.Surface((bw, bh), pygame.SRCALPHA)
            bs.fill(bg_col)
            self.screen.blit(bs, (bx, by))
            pygame.draw.rect(self.screen, border_col, (bx, by, bw, bh), 1)
            txt_col = _C["green"] if active else (_C["text_hi"] if hover else _C["text"])
            lw = self._f15.size(label)[0]
            self._txt(self.screen, label, txt_col,
                      (bx + bw // 2 - lw // 2, by + bh // 2 - 8), self._f15)
        self._txt(self.screen, "Click a button  |  F12 to close  |  CAPS+A = dev mode toggle",
                  _C["text_dim"], (ox + 10, oy + total_h - 20), self._fcode_sm)

    def handle_menu_click(self, event, p=None, inventory_dict=None):
        """Pass MOUSEBUTTONDOWN events while menu is open."""
        if not DEV_MODE or not self.dev_enabled or not self._menu_open:
            return None
        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return None
        cols    = 3
        bw, bh  = 168, 38
        pad     = 8
        total_w = cols * bw + (cols - 1) * pad + 24
        rows    = (len(self._menu_buttons) + cols - 1) // cols
        total_h = rows * bh + (rows - 1) * pad + 54
        ox      = self._sx // 2 - total_w // 2
        oy      = self._sy // 2 - total_h // 2
        mx, my  = event.pos
        for i, (label, key) in enumerate(self._menu_buttons):
            ci = i % cols
            ri = i // cols
            bx = ox + 12 + ci * (bw + pad)
            by = oy + 44 + ri * (bh + pad)
            if bx <= mx < bx + bw and by <= my < by + bh:
                self._dispatch_menu_action(key, p, inventory_dict)
                return key
        return None

    def _dispatch_menu_action(self, key, p, inv):
        if key == "warp":
            self._toggle_warp_creator()
        elif key == "rect_debug":
            self.toggle_rect_debug()
        elif key == "rdt":
            self._rdt_active = not self._rdt_active
            self._notify("Rect Draw: " + ("ON" if self._rdt_active else "OFF"))
        elif key == "ndt":
            self._ndt_active = not self._ndt_active
            self._notify("NPC Tool: " + ("ON" if self._ndt_active else "OFF"))
        elif key == "noclip":
            self.toggle_noclip()
        elif key == "give":
            self._give_open = True
            self._menu_open = False
        elif key == "inv_editor":
            self._inv_editor_open = not self._inv_editor_open
            self._menu_open       = False
        elif key == "npc_console":
            self._npc_console_open = True
            self._menu_open        = False
        elif key == "debug_panel":
            self.toggle_debug_panel()
        elif key == "save"   and p and inv is not None:
            self.save_test(p, inv)
        elif key == "load"   and p and inv is not None:
            self.load_test(p, inv)
        elif key == "export":
            self.export_save_json()
        elif key == "close":
            self._menu_open = False

    # ==================================================================
    #  ── NOTIFICATION SYSTEM ───────────────────────────────────────────
    # ==================================================================

    def _notify(self, text, duration=2.5):
        self._notifications.append((text, time.time() + duration))

    def draw_notifications(self):
        if not DEV_MODE:
            return
        now = time.time()
        self._notifications = [(t, e) for t, e in self._notifications if now < e]
        for i, (text, exp) in enumerate(self._notifications[-6:]):
            alpha = min(255, int((exp - now) / 0.4 * 255))
            lbl   = self._f15.render(text, True, _C["yellow"])
            surf  = pygame.Surface(lbl.get_size(), pygame.SRCALPHA)
            surf.blit(lbl, (0, 0))
            surf.set_alpha(alpha)
            self.screen.blit(surf, (self._sx - lbl.get_width() - 12, self._sy - 32 - i * 20))

    # ==================================================================
    #  ── MASTER DRAW ───────────────────────────────────────────────────
    # ==================================================================

    def draw(self, p=None, clock=None, npc_list=None, walls=None,
             inventory_dict=None, world_x=0, world_y=0, events=None,
             mouse_pos=None):
        """
        Single render call for all devkit overlays.
        Place this at the very END of your render block, BEFORE display().
        """
        if not DEV_MODE:
            return
        mx, my = mouse_pos if mouse_pos else pygame.mouse.get_pos()
        self.draw_warps(world_x, world_y)
        self.draw_rects(world_x, world_y)
        self.draw_rdt(world_x, world_y, (mx, my))
        self.draw_ndt(world_x, world_y, (mx, my))
        self.draw_effects_hud()
        if clock and p:
            self.draw_debug_panel(p, clock, npc_list, walls)
        self.draw_give_menu()
        self.draw_npc_console()
        if inventory_dict is not None:
            self.draw_inv_editor(inventory_dict, events)
        self.draw_menu()
        self.draw_save_feedback()
        self._draw_dev_banner()
        self.draw_notifications()

    # ==================================================================
    #  ── INTERNAL HELPER ───────────────────────────────────────────────
    # ==================================================================

    @staticmethod
    def _txt(surface, text, color, pos, font):
        surface.blit(font.render(str(text), True, color), pos)


# =============================================================================
#
#  ═══════════════════════════════════════════════════════════════════════════
#  INSERTION GUIDE FOR NPC_SIMULATION_AND_MAP_RECT_TOOL.py
#  ═══════════════════════════════════════════════════════════════════════════
#
#  ── STEP 1 ─ REMOVE FROM main.py ────────────────────────────────────────
#
#  FIND this block (the F8 rect tool init variables, ~line 3020):
#
#       # ── RECT DEBUG TOOL ─────────────────────────────────────────────
#       _rdt_active       = False
#       _rdt_drawing      = False
#       _rdt_start_wx     = 0
#       _rdt_start_wy     = 0
#       _rdt_rects        = []
#       _rdt_label_counter = [0]
#       _rdt_font         = pygame.font.SysFont("Courier New", 14)
#       _rdt_font_sm      = pygame.font.SysFont("Courier New", 12)
#       # ────────────────────────────────────────────────────────────────
#
#  DELETE the entire block above.
#
#  ─────────────────────────────────────────────────────────────────────────
#
#  FIND this block (the F9 NPC debug tool init variables, ~line 3030):
#
#       # ── NPC DEBUG TOOL ──────────────────────────────────────────────
#       class _ndt_rename_idx_holder:
#           v = 0
#       _ndt_active           = False
#       _ndt_npcs             = []
#       _ndt_labels           = []
#       _ndt_counter          = [0]
#       _ndt_mode             = "idle"
#       _ndt_font             = pygame.font.SysFont("Courier New", 14)
#       _ndt_font_sm          = pygame.font.SysFont("Courier New", 12)
#       _ndt_sprite_keys      = [  ...long list...  ]
#       _ndt_sprite_index     = [0]
#       _ndt_interact_label   = [""]
#       # ────────────────────────────────────────────────────────────────
#
#  DELETE the entire block above (including the _ndt_sprite_keys list).
#
#  ─────────────────────────────────────────────────────────────────────────
#
#  FIND this event-loop block (F8 / F9 key handling, inside event loop):
#
#       for event in events:
#           ...
#           if event.type == pygame.KEYDOWN:
#               if event.key == pygame.K_F9:
#                   _ndt_active = not _ndt_active
#                   ...
#           if _ndt_active:
#               if event.type == pygame.KEYDOWN:
#                   if event.key == pygame.K_TAB:
#                   ...
#               if _ndt_active:
#                   if event.type == pygame.MOUSEBUTTONDOWN ...
#                       _ndt_place(...)
#           if event.type == pygame.KEYDOWN:
#               if event.key == pygame.K_F8:
#                   _rdt_active = not _rdt_active
#                   ...
#           if _rdt_active:
#               if event.type == pygame.MOUSEBUTTONDOWN ...
#                   _rdt_drawing = True
#               if event.type == pygame.MOUSEBUTTONUP ...
#                   _rdt_finish(...)
#
#  DELETE all of the above inside-the-event-loop F8/F9 code.
#  (Keep the outer `for event in events:` and the QUIT handler.)
#
#  ─────────────────────────────────────────────────────────────────────────
#
#  FIND this render-block section (F8/F9 draw code, near the bottom of the
#  while loop after all map states):
#
#       # ── NPC DEBUG TOOL: UPDATE + DRAW + HUD ─────────────────────
#       if _ndt_active:
#           ...   (very long block, ~100 lines)
#       # ─────────────────────────────────────────────────────────────
#       # ── RECT DEBUG TOOL: DRAW ────────────────────────────────────
#       if _rdt_active:
#           ...   (long block, ~70 lines)
#       # ─────────────────────────────────────────────────────────────
#
#  DELETE both of those draw blocks entirely.
#
#  ─────────────────────────────────────────────────────────────────────────
#
#  ── STEP 2 ─ INSERT AT TOP OF main.py ────────────────────────────────────
#
#  After the existing imports (pygame, random, sys, time, etc.) add:
#
#       from elucidate_devkit import ElucidateDevKit
#
#       try:
#           import pyperclip as _pyperclip
#           _HAS_PYPERCLIP = True
#       except Exception:
#           _pyperclip    = None
#           _HAS_PYPERCLIP = False
#
#  (Remove the duplicate pyperclip try/except if it already exists.)
#
#  ─────────────────────────────────────────────────────────────────────────
#
#  ── STEP 3 ─ INSERT BEFORE THE GAME LOOP ─────────────────────────────────
#
#  After `p = player(...)`, `state = "version_check"`, and all your other
#  pre-loop setup, add these lines:
#
#       # ── DEVKIT INIT ─────────────────────────────────────────────────
#       _state_ref = [state]                         # mutable wrapper
#       def _dk_get_state():   return _state_ref[0]
#       def _dk_set_state(s):
#           global state
#           _state_ref[0] = s
#           state = s
#
#       devkit = ElucidateDevKit(
#           screen,
#           fonts,
#           _dk_get_state,
#           _dk_set_state,
#           npc_sprites = SPRITES,          # the SPRITES dict
#           NPC_class   = NPC,              # your NPC class
#           pyperclip   = _pyperclip,       # or None
#       )
#
#       # Optional: pre-register static rects for F2 visualisation
#       # devkit.register_rect(pygame.Rect(447,541,122,16), "map01_exit", "warp")
#
#       # Optional: register runtime warps (replaces raw colliderect warp code)
#       # devkit.create_warp(447,541,122,16, 921,548, "map_02", map_id="map_01")
#       # ────────────────────────────────────────────────────────────────
#
#  ─────────────────────────────────────────────────────────────────────────
#
#  ── STEP 4 ─ INSERT INSIDE EVENT LOOP ────────────────────────────────────
#
#  Inside `for event in events:` (right after the QUIT check):
#
#       consumed = devkit.handle_hotkeys(
#           event,
#           p              = p,
#           inventory_dict = inventory_items,   # your inventory dict
#           npc_list       = npcs,
#           world_x        = world_x,
#           world_y        = world_y,
#           mouse_pos      = (mouse_x, mouse_y),
#       )
#       devkit.handle_menu_click(event, p=p, inventory_dict=inventory_items)
#       devkit.handle_warp_draw(event, world_x, world_y, (mouse_x, mouse_y))
#
#  ─────────────────────────────────────────────────────────────────────────
#
#  ── STEP 5 ─ INSERT INSIDE UPDATE BLOCK ──────────────────────────────────
#
#  Inside `while logic_accumulator >= 1.0 / logic_tick:` after `p.border()`:
#
#       # ── DEVKIT UPDATE ────────────────────────────────────────────────
#       devkit.update_effects(p)
#       devkit.update_ndt(p, walls, world_x, world_y)
#
#  Replace every raw `p.move(walls + entity_walls)` call with:
#
#       if devkit.apply_noclip():
#           pass    # skip wall collision while no-clip is ON
#       else:
#           p.move(walls + entity_walls)
#
#  After the logic accumulator block, sync state if devkit changed it:
#
#       state = _state_ref[0]
#
#  ─────────────────────────────────────────────────────────────────────────
#
#  ── STEP 6 ─ INSERT INSIDE RENDER BLOCK ──────────────────────────────────
#
#  At the VERY END of the render section, BEFORE `mouse()` and BEFORE
#  `display()`, add:
#
#       devkit.draw(
#           p              = p,
#           clock          = py_clock,
#           npc_list       = npcs,
#           walls          = walls,
#           inventory_dict = inventory_items,   # or None if not on map
#           world_x        = world_x,
#           world_y        = world_y,
#           events         = events,
#           mouse_pos      = (mouse_x, mouse_y),
#       )
#
#  ─────────────────────────────────────────────────────────────────────────
#
#  ── STEP 7 ─ ACTIVATION ──────────────────────────────────────────────────
#
#  Start the game.  Press CAPS LOCK (turn it ON, LED should light).
#  Then press  A .
#  You will see:  "DEVELOPER MODE ENABLED"
#
#  Now F1–F12 all work.  Press CAPS LOCK + A again to disable.
#
#  ═══════════════════════════════════════════════════════════════════════════
#  HOTKEY SUMMARY
#  ═══════════════════════════════════════════════════════════════════════════
#
#   Activation:  CAPS LOCK on, then press A
#
#   Key    Function
#   ─────  ───────────────────────────────────────────────────────────────
#   F1     Warp Creator  — draw + auto-print warp zone code
#   F2     Rect Visualiser — toggle registered/drawn rects
#   F3     No-Clip — player ignores all wall collision
#   F4     Give Item Console  (give <name> <qty|=N|-N|remove>)
#   F5     Inventory Editor — visual +/- panel
#   F6     Apply random timed effect to player
#   F7     NPC Spawner console  (<sprite> [mode])
#   F8     Rect Draw Tool  [migrated from main.py]
#   F9     NPC Debug Tool  [migrated from main.py]
#   F10    Debug panel — FPS / map / coords / NPC / effect counts
#   F11    Save test slot   (SHIFT+F11 = load)
#   F12    Master Dev Menu button overlay
#
#  ═══════════════════════════════════════════════════════════════════════════
#  COMMON MISTAKES TO AVOID
#  ═══════════════════════════════════════════════════════════════════════════
#
#  ✗ Circular import
#      This file must NEVER import main.py or any module that imports main.py.
#
#  ✗ State not syncing
#      Always add `state = _state_ref[0]` after any devkit call that can
#      change state (process_warps, switch_map, ndt map navigation).
#
#  ✗ F8/F9 code still in main.py
#      If you see duplicate rect/NPC overlays, the old code is still active.
#      Follow STEP 1 exactly — remove both the init variables AND the event/
#      render blocks.
#
#  ✗ NPC_class not passed
#      F7 and F9 will display "[!] NPC_class not provided" if you forgot to
#      pass NPC_class=NPC in the constructor.  All other tools still work.
#
#  ✗ Dev tools active during normal play
#      They are NOT — every F-key check is guarded by `self.dev_enabled`.
#      Only the CAPS+A combo check runs unconditionally (it is a single
#      two-key lookup with no rendering cost).
#
#  ✗ Release build overhead
#      Set  ELUCIDATE_DEV=0  as an environment variable, or change the top-
#      of-file constant to  DEV_MODE = False .  Every public method returns
#      immediately in that case.
#
# =============================================================================
