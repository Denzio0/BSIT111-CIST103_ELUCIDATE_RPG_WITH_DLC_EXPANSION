import pygame
import random
import sys
import time
import json
import os

try:
    import psutil as _psutil

    _HAS_PSUTIL = True
except Exception:
    _psutil = None
    _HAS_PSUTIL = False


def sys_gen_update_error():
    pass


def elucidate():
    global tick_counter
    _sys_max_cores = (_psutil.cpu_count(logical=True) or 1) if _HAS_PSUTIL else 1
    _sys_total_ram_gb = max(1, int(_psutil.virtual_memory().total / (1024 * 1024 * 1024))) if _HAS_PSUTIL else 2
    ram_limit_gb = 4
    limit = ram_limit_gb * 1024 * 1024 * 1024 * 15
    process = _psutil.Process(os.getpid()) if _HAS_PSUTIL else None

    dlc = True

    try:
        pygame.init()
    except Exception:
        pass
    try:
        pygame.mixer.init()
    except Exception:
        pass

    screen_x, screen_y = 1275, 710
    screen = pygame.display.set_mode((screen_x, screen_y))
    pygame.display.set_caption("Elucidate RPG")

    screen.fill((0, 0, 0))
    try:
        _title_img = pygame.image.load("images/elucidate_full_text_portait_001.png")
        _title_resized = pygame.transform.scale(_title_img, (screen_x // 2, screen_y // 2))
        screen.blit(_title_resized, (screen_x // 4, screen_y // 4))
        _sel_img = pygame.image.load("images/elucidate_select_full.png")
        _sel_resized = pygame.transform.scale(_sel_img, (screen_x // 2, 30))
        screen.blit(_sel_resized, (screen_x // 4, screen_y - 115))
    except Exception:
        pass
    _load_font_a = pygame.font.SysFont("Times New Roman", 25)
    _load_font_b = pygame.font.SysFont("Times New Roman", 20)
    _load_surf_a = _load_font_a.render("Game Initializing", True, (0, 0, 0))
    _load_rect_a = _load_surf_a.get_rect(center=(screen_x // 2, screen_y - 100))
    screen.blit(_load_surf_a, _load_rect_a)
    _load_surf_b = _load_font_b.render("Loading...", True, (255, 255, 255))
    _load_rect_b = _load_surf_b.get_rect(center=(screen_x // 2, screen_y - 20))
    screen.blit(_load_surf_b, _load_rect_b)
    pygame.draw.rect(screen, (160, 0, 0), (0, 0, screen_x, screen_y), 1)
    pygame.display.flip()
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    py_clock = pygame.time.Clock()
    logic_tick = 60
    render_fps = 60
    render_fps_options = [30, 60, 120, 144, 0]
    render_fps_index = 1
    fps_slider_dragging = False
    cpu_core_limit = 10
    cpu_slider_dragging = False
    ram_slider_dragging = False
    walls = []

    fonts = {10: pygame.font.SysFont("Times New Roman", 10), 15: pygame.font.SysFont("Times New Roman", 15),
             20: pygame.font.SysFont("Times New Roman", 20), 25: pygame.font.SysFont("Times New Roman", 25),
             30: pygame.font.SysFont("Times New Roman", 30), 35: pygame.font.SysFont("Times New Roman", 35),
             40: pygame.font.SysFont("Times New Roman", 40), 45: pygame.font.SysFont("Times New Roman", 45),
             50: pygame.font.SysFont("Times New Roman", 50), 55: pygame.font.SysFont("Times New Roman", 55),
             60: pygame.font.SysFont("Times New Roman", 60), }

    _hex_decode_cache = {}
    user_add_speed = 7
    PLAYER_CLASSES = {"mercenary": user_add_speed, "cultist": user_add_speed, "priest": user_add_speed,
                      "shaman": user_add_speed, "merchant": user_add_speed, }

    def _load(rel, alpha=False):
        try:
            img = pygame.image.load(rel)
            return img.convert_alpha() if alpha else img.convert()
        except Exception:
            surf = pygame.Surface((72, 72))
            surf.fill((255, 0, 255))
            return surf

    screen.fill((0, 0, 0))
    try:
        _title_img = pygame.image.load("images/elucidate_full_text_portait_001.png")
        _title_resized = pygame.transform.scale(_title_img, (screen_x // 2, screen_y // 2))
        screen.blit(_title_resized, (screen_x // 4, screen_y // 4))
        _sel_img = pygame.image.load("images/elucidate_select_full.png")
        _sel_resized = pygame.transform.scale(_sel_img, (screen_x // 2, 30))
        screen.blit(_sel_resized, (screen_x // 4, screen_y - 115))
    except Exception:
        pass
    _load_font_a = pygame.font.SysFont("Times New Roman", 25)
    _load_font_b = pygame.font.SysFont("Times New Roman", 20)
    _load_surf_a = _load_font_a.render("Loading Assets", True, (0, 0, 0))
    _load_rect_a = _load_surf_a.get_rect(center=(screen_x // 2, screen_y - 100))
    screen.blit(_load_surf_a, _load_rect_a)
    _load_surf_b = _load_font_b.render("Loading...", True, (255, 255, 255))
    _load_rect_b = _load_surf_b.get_rect(center=(screen_x // 2, screen_y - 20))
    screen.blit(_load_surf_b, _load_rect_b)
    pygame.draw.rect(screen, (160, 0, 0), (0, 0, screen_x, screen_y), 1)
    pygame.display.flip()
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    _preloaded_images = {"elucidate_title": _load("images/elucidate_title.png"),
                         "elucidate_select": _load("images/elucidate_select.png"),
                         "elucidate_select_full": _load("images/elucidate_select_full.png"),
                         "elucidate_no_texture": _load("images/elucidate_no_texture.png"),
                         "idle_male_civilian_variant_npc_up": _load(
                             "sprites/npc_n_s2_walled_city_civilians_male/elucidate_idle_male_civilian_variant_npc_up.png",
                             True), "idle_male_civilian_variant_npc_right": _load(
            "sprites/npc_n_s2_walled_city_civilians_male/elucidate_idle_male_civilian_variant_npc_right.png", True),
                         "idle_male_civilian_variant_npc_left": _load(
                             "sprites/npc_n_s2_walled_city_civilians_male/elucidate_idle_male_civilian_variant_npc_left.png",
                             True), "idle_male_civilian_variant_npc_down": _load(
            "sprites/npc_n_s2_walled_city_civilians_male/elucidate_idle_male_civilian_variant_npc_down.png", True),
                         "idle_female_civilian_variant_npc_up": _load(
                             "sprites/npc_n_s2_walled_city_civilians_female/elucidate_idle_female_civilian_variant_npc_up.png",
                             True), "idle_female_civilian_variant_npc_right": _load(
            "sprites/npc_n_s2_walled_city_civilians_female/elucidate_idle_female_civilian_variant_npc_right.png", True),
                         "idle_female_civilian_variant_npc_left": _load(
                             "sprites/npc_n_s2_walled_city_civilians_female/elucidate_idle_female_civilian_variant_npc_left.png",
                             True), "idle_female_civilian_variant_npc_down": _load(
            "sprites/npc_n_s2_walled_city_civilians_female/elucidate_idle_female_civilian_variant_npc_down.png", True),
                         "elucidate_no_sprite_idle_1": _load("sprites/elucidate_player_sprite_idle_up.png", True),
                         "elucidate_no_sprite_idle_2": _load("sprites/elucidate_player_sprite_idle_down.png", True),
                         "elucidate_no_sprite_idle_3": _load("sprites/elucidate_player_sprite_idle_left.png", True),
                         "elucidate_no_sprite_idle_4": _load("sprites/elucidate_player_sprite_idle_right.png", True),
                         "elucidate_no_sprite_walk_1_1": _load("sprites/elucidate_player_sprite_walking_up_1.png",
                                                               True),
                         "elucidate_no_sprite_walk_1_2": _load("sprites/elucidate_player_sprite_walking_up_2.png",
                                                               True),
                         "elucidate_no_sprite_walk_2_1": _load("sprites/elucidate_player_sprite_walking_down_1.png",
                                                               True),
                         "elucidate_no_sprite_walk_2_2": _load("sprites/elucidate_player_sprite_walking_down_2.png",
                                                               True),
                         "elucidate_no_sprite_walk_3_1": _load("sprites/elucidate_player_sprite_walking_left_1.png",
                                                               True),
                         "elucidate_no_sprite_walk_3_2": _load("sprites/elucidate_player_sprite_walking_left_2.png",
                                                               True),
                         "elucidate_no_sprite_walk_4_1": _load("sprites/elucidate_player_sprite_walking_right_1.png",
                                                               True),
                         "elucidate_no_sprite_walk_4_2": _load("sprites/elucidate_player_sprite_walking_right_2.png",
                                                               True),
                         "elucidate_no_sprite_attack_1_1": _load("sprites/elucidate_player_sprite_attack_up_1.png",
                                                                 True),
                         "elucidate_no_sprite_attack_1_2": _load("sprites/elucidate_player_sprite_attack_up_2.png",
                                                                 True),
                         "elucidate_no_sprite_attack_2_1": _load("sprites/elucidate_player_sprite_attack_down_1.png",
                                                                 True),
                         "elucidate_no_sprite_attack_2_2": _load("sprites/elucidate_player_sprite_attack_down_2.png",
                                                                 True),
                         "elucidate_no_sprite_attack_3_1": _load("sprites/elucidate_player_sprite_attack_left_1.png",
                                                                 True),
                         "elucidate_no_sprite_attack_3_2": _load("sprites/elucidate_player_sprite_attack_left_2.png",
                                                                 True),
                         "elucidate_no_sprite_attack_4_1": _load("sprites/elucidate_player_sprite_attack_right_1.png",
                                                                 True),
                         "elucidate_no_sprite_attack_4_2": _load("sprites/elucidate_player_sprite_attack_right_2.png",
                                                                 True), "elucidate_mercenary_sprite_idle_1": _load(
            "sprites/player_mercenary/elucidate_mercenary_sprite_idle_up.png", True),
                         "elucidate_mercenary_sprite_idle_2": _load(
                             "sprites/player_mercenary/elucidate_mercenary_sprite_idle_down.png", True),
                         "elucidate_mercenary_sprite_idle_3": _load(
                             "sprites/player_mercenary/elucidate_mercenary_sprite_idle_left.png", True),
                         "elucidate_mercenary_sprite_idle_4": _load(
                             "sprites/player_mercenary/elucidate_mercenary_sprite_idle_right.png", True),
                         "elucidate_mercenary_sprite_walk_1_1": _load(
                             "sprites/player_mercenary/elucidate_mercenary_move_up_001.png", True),
                         "elucidate_mercenary_sprite_walk_1_2": _load(
                             "sprites/player_mercenary/elucidate_mercenary_move_up_002.png", True),
                         "elucidate_mercenary_sprite_walk_2_1": _load(
                             "sprites/player_mercenary/elucidate_mercenary_move_down_001.png", True),
                         "elucidate_mercenary_sprite_walk_2_2": _load(
                             "sprites/player_mercenary/elucidate_mercenary_move_down_002.png", True),
                         "elucidate_mercenary_sprite_walk_3_1": _load(
                             "sprites/player_mercenary/elucidate_mercenary_move_left_001.png", True),
                         "elucidate_mercenary_sprite_walk_3_2": _load(
                             "sprites/player_mercenary/elucidate_mercenary_move_left_002.png", True),
                         "elucidate_mercenary_sprite_walk_4_1": _load(
                             "sprites/player_mercenary/elucidate_mercenary_move_right_001.png", True),
                         "elucidate_mercenary_sprite_walk_4_2": _load(
                             "sprites/player_mercenary/elucidate_mercenary_move_right_002.png", True),
                         "elucidate_mercenary_sprite_attack_1_1": _load(
                             "sprites/elucidate_player_sprite_attack_up_1.png", True),
                         "elucidate_mercenary_sprite_attack_1_2": _load(
                             "sprites/elucidate_player_sprite_attack_up_2.png", True),
                         "elucidate_mercenary_sprite_attack_2_1": _load(
                             "sprites/elucidate_player_sprite_attack_down_1.png", True),
                         "elucidate_mercenary_sprite_attack_2_2": _load(
                             "sprites/elucidate_player_sprite_attack_down_2.png", True),
                         "elucidate_mercenary_sprite_attack_3_1": _load(
                             "sprites/elucidate_player_sprite_attack_left_1.png", True),
                         "elucidate_mercenary_sprite_attack_3_2": _load(
                             "sprites/elucidate_player_sprite_attack_left_2.png", True),
                         "elucidate_mercenary_sprite_attack_4_1": _load(
                             "sprites/elucidate_player_sprite_attack_right_1.png", True),
                         "elucidate_mercenary_sprite_attack_4_2": _load(
                             "sprites/elucidate_player_sprite_attack_right_2.png", True),
                         "elucidate_select_bg_001": _load("images/elucidate_select_background.png"),
                         "elucidate_select_bg_002": _load("images/elucidate_empty_bg_001.png"),
                         "elucidate_select_ui_001": _load("images/elucidate_show_selection_002.png"),
                         "elucidate_select_ui_002": _load("images/elucidate_show_selection_001.png", True),
                         "elucidate_mcguy_001": _load("images/elucidate_mcguy_portrait_001.png", True),
                         "elucidate_select_player_001": _load("images/elucidate_user_selection_bg.png"),
                         "elucidate_select_player_002": _load("images/elucidate_user_elected_play.png"),
                         "elucidate_area_empty_room": _load("images/elucidate_bg_empty_room_001.png"),
                         "elucidate_dungeon_area_001": _load("images/elucidate_dungeon_grounds_bg_001.png"),
                         "elucidate_dungeon_area_002": _load("images/elucidate_dungeon_grounds_bg_002.png"),
                         "elucidate_full_scale_test": _load("images/elucidate_map_long1.png"),
                         "elucidate_inventory": _load("images/elucidate_inventory.png"),
                         "elucidate_launcher_bg": _load("images/elucidate_bg_launcher_001.png"),
                         "l_o_outer_gate_district": _load("maps/l_o_outer_gate_district.png"),
                         "l_i_inside_the_wall": _load("maps/l_i_inside_the_wall.png"),
                         "l_o_inner_military_district": _load("maps/l_o_inner_military_district.png"),
                         "l_i_church_chapel": _load("maps/l_i_church_chapel.png"),
                         "l_i_barracks_hall": _load("maps/l_i_barracks_hall.png"),
                         "l_o_church_outpost": _load("maps/l_o_church_outpost.png"),
                         "l_i_orphanage_access": _load("maps/l_i_orphanage_access.png"),
                         "l_i_theocratic_battleground_endingb": _load("maps/l_i_theocratic_battleground_endingb.png"),
                         "l_i_main_cathedral": _load("maps/l_i_main_cathedral.png"),
                         "l_o_destroy_theocracy": _load("maps/l_o_destroy_theocracy.png"),
                         "l_i_church_administrative_wing": _load("maps/l_i_church_administrative_wing.png"),
                         "l_o_cathedral_plaza": _load("maps/l_o_cathedral_plaza.png"),
                         "l_o_rare_nexus_points": _load("maps/l_o_rare_nexus_points.png"),
                         "f_o_deep_terror_zone": _load("maps/f_o_deep_terror_zone.png"),
                         "l_o_corrupted_frontier": _load("maps/l_o_corrupted_frontier.png"),
                         "t_o_anomaly_forest": _load("maps/t_o_anomaly_forest.png"),
                         "l_i_lab_office_under_administrative_wing": _load(
                             "maps/l_i_lab_office_under_administrative_wing.png"),
                         "l_i_active_laboratory_under_administrative_wing": _load(
                             "maps/l_i_active_laboratory_under_administrative_wing.png"),
                         "l_i_subterranean_labyrinth_exit": _load("maps/l_i_subterranean_labyrinth_exit.png"),
                         "l_i_subterranean_labyrinth": _load("maps/l_i_subterranean_labyrinth.png"),
                         "l_i_old_laboratory": _load("maps/l_i_old_laboratory.png"),
                         "l_i_tutorial_ground": _load("maps/l_i_tutorial_ground.png"),
                         "t_o_tutorial_ground_shaman": _load("maps/t_o_tutorial_ground_shaman.png"),
                         "l_i_tutorial_ground_dlc": _load("maps/l_i_tutorial_ground_dlc.png"),
                         "l_i_tutorial_ground_first_version": _load("maps/l_i_tutorial_ground_first_version.png"),
                         "t_i_escape_route": _load("maps/t_i_escape_route.png"),
                         "t_o_destroyed_tribe_settlement": _load("maps/t_o_destroyed_tribe_settlement.png"),
                         "t_o_tribe_settlement": _load("maps/t_o_tribe_settlement.png"),
                         "t_o_tribe_perimeter": _load("maps/t_o_tribe_perimeter.png"),
                         "t_i_storage_cave": _load("maps/t_i_storage_cave.png"),
                         "t_i_healing_hut": _load("maps/t_i_healing_hut.png"),
                         "l_i_headmaster_office": _load("maps/l_i_headmaster_office.png"),
                         "l_i_the_play_room": _load("maps/l_i_the_play_room.png"),
                         "l_o_the_old_orphanage": _load("maps/l_o_the_old_orphanage.png"),
                         "l_o_home_village_entry": _load("maps/l_o_home_village_entry.png"),
                         "l_o_home_village_center": _load("maps/l_o_home_village_center.png"),
                         "l_i_chief_home": _load("maps/l_i_chief_home.png"),
                         "f_o_village_market": _load("maps/f_o_village_market.png", True),
                         "f_i_tunnel_passage_to_tribe": _load("maps/f_i_tunnel_passage_to_tribe.png"),
                         "f_o_residential_area": _load("maps/f_o_residential_area.png"),
                         "f_i_inside_chief_home": _load("maps/f_i_inside_chief_home.png"),
                         "f_o_outside_chief_home": _load("maps/f_o_outside_chief_home.png"),
                         "f_i_inside_elder_house": _load("maps/f_i_inside_elder_house.png"),
                         "c_o_lowms_cultist_battleground": _load("maps/c_o_lowms_cultist_battleground.png"),
                         "c_i_inner_sanctum": _load("maps/c_i_inner_sanctum.png"),
                         "c_o_cultist_battleground": _load("maps/c_o_cultist_battleground.png"),
                         "c_o_cult_village": _load("maps/c_o_cult_village.png"),
                         "c_i_cult_leader_fortress": _load("maps/c_i_cult_leader_fortress.png"),
                         "c_o_cult_funeris_encounter": _load("maps/c_o_cult_funeris_encounter.png"),
                         "c_o_coastal_landing": _load("maps/c_o_coastal_landing.png"),
                         "l_i_merchant_bank": _load("maps/l_i_merchant_bank.png"),
                         "l_i_the_ship": _load("maps/l_i_the_ship.png"),
                         "l_i_ship_lower_part": _load("maps/l_i_ship_lower_part.png"),
                         "l_i_merchant_tavern": _load("maps/l_i_merchant_tavern.png"),
                         "l_o_merchant_quarter": _load("maps/l_o_merchant_quarter.png"),
                         "l_i_merchant_guild_hall": _load("maps/l_i_merchant_guild_hall.png"),
                         "l_i_lumen_spy_merchant_guild": _load("maps/l_i_lumen_spy_merchant_guild.png"),
                         "l_o_harbor_district": _load("maps/l_o_harbor_district.png"),
                         "l_i_clearance_office": _load("maps/l_i_clearance_office.png"),
                         "l_i_customs_office": _load("maps/l_i_customs_office.png"),  # GUI AND BACKGROUNDS
                         "elucidate_bag_craft_inventory_001": _load("images/elucidate_bag_craft_inventory_001.png"),
                         "elucidate_bag_craft_inventory_002": _load("images/elucidate_bag_craft_inventory_002.png"),
                         "elucidate_bag_craft_inventory_003": _load("images/elucidate_bag_craft_inventory_003.png"),
                         "elucidate_bag_craft_inventory_004": _load("images/elucidate_bag_craft_inventory_004.png"),
                         "elucidate_bag_inventory_001": _load("images/elucidate_bag_inventory_001.png"),
                         "elucidate_bag_inventory_002": _load("images/elucidate_bag_inventory_002.png"),
                         "elucidate_bag_inventory_003": _load("images/elucidate_bag_inventory_003.png"),
                         "elucidate_bg_launcher_001": _load("images/elucidate_bg_launcher_001.png"),
                         "elucidate_craft_only_inventory_001": _load("images/elucidate_craft_only_inventory_001.png"),
                         "elucidate_craft_only_inventory_002": _load("images/elucidate_craft_only_inventory_002.png"),
                         "elucidate_craft_only_inventory_003": _load("images/elucidate_craft_only_inventory_003.png"),
                         "elucidate_craft_only_inventory_004": _load("images/elucidate_craft_only_inventory_004.png"),
                         "elucidate_craft_only_inventory_005": _load("images/elucidate_craft_only_inventory_005.png"),
                         "elucidate_dlc_inventory_001": _load("images/elucidate_dlc_inventory_001.png"),
                         "elucidate_dlc_inventory_002": _load("images/elucidate_dlc_inventory_002.png"),
                         "elucidate_dlc_inventory_003": _load("images/elucidate_dlc_inventory_003.png"),
                         "elucidate_dlc_user_selected_play_001": _load(
                             "images/elucidate_dlc_user_selected_play_001.png"),
                         "elucidate_dlc_user_selected_play_002": _load(
                             "images/elucidate_dlc_user_selected_play_002.png"),
                         "elucidate_dlc_user_selected_play_003": _load(
                             "images/elucidate_dlc_user_selected_play_003.png"),
                         "elucidate_dlc_user_selection_bg_001": _load("images/elucidate_dlc_user_selection_bg_001.png"),
                         "elucidate_dlc_user_selection_bg_002": _load("images/elucidate_dlc_user_selection_bg_002.png"),
                         "elucidate_dlc_user_selection_bg_003": _load("images/elucidate_dlc_user_selection_bg_003.png"),
                         "elucidate_dlc_user_selection_bg_004": _load("images/elucidate_dlc_user_selection_bg_004.png"),
                         "elucidate_dlc_user_selection_bg_005": _load("images/elucidate_dlc_user_selection_bg_005.png"),
                         "elucidate_dlc_user_selection_bg_006": _load("images/elucidate_dlc_user_selection_bg_006.png"),
                         "elucidate_enemy_attack_001": _load("images/elucidate_enemy_attack_001.png"),
                         "elucidate_enemy_escape_001": _load("images/elucidate_enemy_escape_001.png"),
                         "elucidate_enemy_escape_002": _load("images/elucidate_enemy_escape_002.png"),
                         "elucidate_enemy_escape_003": _load("images/elucidate_enemy_escape_003.png"),
                         "elucidate_enemy_interaction_001": _load("images/elucidate_enemy_interaction_001.png"),
                         "elucidate_enemy_interaction_002": _load("images/elucidate_enemy_interaction_002.png"),
                         "elucidate_enemy_interaction_003": _load("images/elucidate_enemy_interaction_003.png"),
                         "elucidate_enemy_interaction_004": _load("images/elucidate_enemy_interaction_004.png"),
                         "elucidate_enemy_interaction_005": _load("images/elucidate_enemy_interaction_005.png"),
                         "elucidate_enemy_inventory_001": _load("images/elucidate_enemy_inventory_001.png"),
                         "elucidate_enemy_skill_001": _load("images/elucidate_enemy_skill_001.png"),
                         "elucidate_enemy_skill_002": _load("images/elucidate_enemy_skill_002.png"),
                         "elucidate_enemy_skill_003": _load("images/elucidate_enemy_skill_003.png"),
                         "elucidate_equipment_inventory_001": _load("images/elucidate_equipment_inventory_001.png"),
                         "elucidate_equipment_inventory_002": _load("images/elucidate_equipment_inventory_002.png"),
                         "elucidate_equipment_inventory_003": _load("images/elucidate_equipment_inventory_003.png"),
                         "elucidate_full_text_portait_001": _load("images/elucidate_full_text_portait_001.png"),
                         "elucidate_inventory_001": _load("images/elucidate_inventory_001.png"),
                         "elucidate_inventory_002": _load("images/elucidate_inventory_002.png"),
                         "elucidate_map_portait_001": _load("images/elucidate_map_portait_001.png"),
                         "elucidate_map_portait_002": _load("images/elucidate_map_portait_002.png"),
                         "elucidate_map_portait_003": _load("images/elucidate_map_portait_003.png"),
                         "elucidate_map_portait_004": _load("images/elucidate_map_portait_004.png"),
                         "elucidate_map_portait_005": _load("images/elucidate_map_portait_005.png"),
                         "elucidate_map_portait_006": _load("images/elucidate_map_portait_006.png"),
                         "elucidate_map_portait_007": _load("images/elucidate_map_portait_007.png"),
                         "elucidate_map_portait_008": _load("images/elucidate_map_portait_008.png"),
                         "elucidate_menu_bg_001": _load("images/elucidate_menu_bg_001.png"),
                         "elucidate_menu_bg_002": _load("images/elucidate_menu_bg_002.png"),
                         "elucidate_menu_bg_003": _load("images/elucidate_menu_bg_003.png"),
                         "elucidate_menu_bg_004": _load("images/elucidate_menu_bg_004.png"),
                         "elucidate_menu_bg_005": _load("images/elucidate_menu_bg_005.png"),
                         "elucidate_menu_bg_006": _load("images/elucidate_menu_bg_006.png"),
                         "elucidate_menu_bg_007": _load("images/elucidate_menu_bg_007.png"),
                         "elucidate_menu_bg_008": _load("images/elucidate_menu_bg_008.png"),
                         "elucidate_menu_bg_009": _load("images/elucidate_menu_bg_009.png"),
                         "elucidate_menu_bg_010": _load("images/elucidate_menu_bg_010.png"),
                         "elucidate_menu_bg_011": _load("images/elucidate_menu_bg_011.png"),
                         "elucidate_mini_games_select_001": _load("images/elucidate_mini_games_select_001.png"),
                         "elucidate_mini_games_select_002": _load("images/elucidate_mini_games_select_002.png"),
                         "elucidate_mini_games_select_003": _load("images/elucidate_mini_games_select_003.png"),
                         "elucidate_mini_games_select_004": _load("images/elucidate_mini_games_select_004.png"),
                         "elucidate_mini_games_select_005": _load("images/elucidate_mini_games_select_005.png"),
                         "elucidate_mini_games_select_006": _load("images/elucidate_mini_games_select_006.png"),
                         "elucidate_mini_games_select_007": _load("images/elucidate_mini_games_select_007.png"),
                         "elucidate_mini_games_select_008": _load("images/elucidate_mini_games_select_008.png"),
                         "elucidate_mini_games_select_009": _load("images/elucidate_mini_games_select_009.png"),
                         "elucidate_mini_games_select_010": _load("images/elucidate_mini_games_select_010.png"),
                         "elucidate_mini_games_select_011": _load("images/elucidate_mini_games_select_011.png"),
                         "elucidate_mini_games_select_012": _load("images/elucidate_mini_games_select_012.png"),
                         "elucidate_mini_games_select_013": _load("images/elucidate_mini_games_select_013.png"),
                         "elucidate_mini_games_select_014": _load("images/elucidate_mini_games_select_014.png"),
                         "elucidate_mini_games_select_015": _load("images/elucidate_mini_games_select_015.png"),
                         "elucidate_mini_games_select_016": _load("images/elucidate_mini_games_select_016.png"),
                         "elucidate_no_texture_001": _load("images/elucidate_no_texture_001.png"),
                         "elucidate_play_bg": _load("images/elucidate_play_bg.png"),
                         "elucidate_select_background": _load("images/elucidate_select_background.png"),
                         "elucidate_show_selection_001": _load("images/elucidate_show_selection_001.png"),
                         "elucidate_show_selection_002": _load("images/elucidate_show_selection_002.png"),
                         "elucidate_user_selected_play_001": _load("images/elucidate_user_selected_play_001.png"),
                         "elucidate_user_selected_play_002": _load("images/elucidate_user_selected_play_002.png"),
                         "elucidate_user_selection_bg_001": _load("images/elucidate_user_selection_bg_001.png"),
                         "elucidate_user_selection_bg_002": _load("images/elucidate_user_selection_bg_002.png"),
                         "elucidate_user_selection_bg_003": _load("images/elucidate_user_selection_bg_003.png"),
                         "elucidate_version_select_001": _load("images/elucidate_version_select_001.png"),
                         "elucidate_version_select_002": _load("images/elucidate_version_select_002.png"),
                         "elucidate_version_select_003": _load("images/elucidate_version_select_003.png"),
                         "elucidate_version_select_004": _load("images/elucidate_version_select_004.png"),
                         "elucidate_version_select_005": _load("images/elucidate_version_select_005.png"),
                         "elucidate_left_gradient_001": _load("images/elucidate_left_gradient_001.png", True),
                         "elucidate_left_purple_gradient_001": _load("images/elucidate_left_purple_gradient_001.png",
                                                                     True),
                         "elucidate_middle_gradient_001": _load("images/elucidate_middle_gradient_001.png", True),
                         "elucidate_middle_purple_gradient_001": _load(
                             "images/elucidate_middle_purple_gradient_001.png", True),
                         "elucidate_middle_purple_gradient_002": _load(
                             "images/elucidate_middle_purple_gradient_002.png", True),
                         "elucidate_right_gradient_001": _load("images/elucidate_right_gradient_001.png", True),
                         "elucidate_right_purple_gradient_001": _load("images/elucidate_right_purple_gradient_001.png",
                                                                      True),

                         # MERCENARY DIALOGUE
                         "walled_mercenary_with_draft_officer_001": _load(
                             "images/walled_mercenary_with_draft_officer_001.png", True),
                         "walled_mercenary_with_draft_officer_002": _load(
                             "images/walled_mercenary_with_draft_officer_002.png", True),
                         "walled_mercenary_with_draft_officer_003": _load(
                             "images/walled_mercenary_with_draft_officer_003.png", True),
                         "walled_mercenary_with_draft_officer_004": _load(
                             "images/walled_mercenary_with_draft_officer_004.png", True),
                         "walled_mercenary_with_draft_officer_005": _load(
                             "images/walled_mercenary_with_draft_officer_005.png", True),
                         "walled_mercenary_with_draft_officer_006": _load(
                             "images/walled_mercenary_with_draft_officer_006.png", True),
                         "walled_mercenary_with_draft_officer_007": _load(
                             "images/walled_mercenary_with_draft_officer_007.png", True),
                         "walled_mercenary_with_draft_officer_008": _load(
                             "images/walled_mercenary_with_draft_officer_008.png", True),
                         "walled_mercenary_with_blacksmith_001": _load(
                             "images/walled_mercenary_with_blacksmith_001.png", True),
                         "walled_mercenary_with_blacksmith_002": _load(
                             "images/walled_mercenary_with_blacksmith_002.png", True),
                         "walled_mercenary_with_blacksmith_003": _load(
                             "images/walled_mercenary_with_blacksmith_003.png", True),
                         "walled_mercenary_with_blacksmith_004": _load(
                             "images/walled_mercenary_with_blacksmith_004.png", True),
                         "walled_mercenary_with_blacksmith_005": _load(
                             "images/walled_mercenary_with_blacksmith_005.png", True),
                         "walled_mercenary_with_blacksmith_006": _load(
                             "images/walled_mercenary_with_blacksmith_006.png", True),
                         "walled_mercenary_with_blacksmith_007": _load(
                             "images/walled_mercenary_with_blacksmith_007.png", True),
                         "walled_mercenary_with_blacksmith_008": _load(
                             "images/walled_mercenary_with_blacksmith_008.png", True),
                         "walled_mercenary_with_blacksmith_009": _load(
                             "images/walled_mercenary_with_blacksmith_009.png", True),
                         "walled_mercenary_with_blacksmith_010": _load(
                             "images/walled_mercenary_with_blacksmith_010.png", True),
                         "walled_mercenary_with_blacksmith_011": _load(
                             "images/walled_mercenary_with_blacksmith_011.png", True),
                         "walled_mercenary_with_blacksmith_012": _load(
                             "images/walled_mercenary_with_blacksmith_012.png", True),
                         "walled_mercenary_with_blacksmith_013": _load(
                             "images/walled_mercenary_with_blacksmith_013.png", True),
                         "walled_mercenary_with_blacksmith_014": _load(
                             "images/walled_mercenary_with_blacksmith_014.png", True),
                         "walled_mercenary_poster_interact_001": _load(
                             "images/walled_mercenary_poster_interact_001.png", True),
                         "walled_mercenary_poster_interact_002": _load(
                             "images/walled_mercenary_poster_interact_002.png", True),
                         "walled_mercenary_poster_interact_003": _load(
                             "images/walled_mercenary_poster_interact_003.png", True),
                         "theocratic_mercenary_with_priest_001": _load(
                             "images/theocratic_mercenary_with_priest_001.png", True),
                         "theocratic_mercenary_with_priest_002": _load(
                             "images/theocratic_mercenary_with_priest_002.png", True),
                         "theocratic_mercenary_with_priest_003": _load(
                             "images/theocratic_mercenary_with_priest_003.png", True),
                         "theocratic_mercenary_with_priest_004": _load(
                             "images/theocratic_mercenary_with_priest_004.png", True),
                         "theocratic_mercenary_with_priest_005": _load(
                             "images/theocratic_mercenary_with_priest_005.png", True),
                         "theocratic_mercenary_with_priest_006": _load(
                             "images/theocratic_mercenary_with_priest_006.png", True),
                         "theocratic_mercenary_with_priest_007": _load(
                             "images/theocratic_mercenary_with_priest_007.png", True),
                         "theocratic_mercenary_with_priest_008": _load(
                             "images/theocratic_mercenary_with_priest_008.png", True),
                         "theocratic_mercenary_with_priest_009": _load(
                             "images/theocratic_mercenary_with_priest_009.png", True),
                         "theocratic_mercenary_with_priest_010": _load(
                             "images/theocratic_mercenary_with_priest_010.png", True),
                         "theocratic_mercenary_with_priest_011": _load(
                             "images/theocratic_mercenary_with_priest_011.png", True),
                         "theocratic_mercenary_with_priest_012": _load(
                             "images/theocratic_mercenary_with_priest_012.png", True),
                         "theocratic_mercenary_with_priest_013": _load(
                             "images/theocratic_mercenary_with_priest_013.png", True),
                         "theocratic_mercenary_with_priest_014": _load(
                             "images/theocratic_mercenary_with_priest_014.png", True),
                         "theocratic_mercenary_with_priest_015": _load(
                             "images/theocratic_mercenary_with_priest_015.png", True),
                         "theocratic_mercenary_with_priest_016": _load(
                             "images/theocratic_mercenary_with_priest_016.png", True),
                         "theocratic_mercenary_with_priest_017": _load(
                             "images/theocratic_mercenary_with_priest_017.png", True),
                         "theocratic_mercenary_with_priest_018": _load(
                             "images/theocratic_mercenary_with_priest_018.png", True),
                         "theocratic_mercenary_with_priest_019": _load(
                             "images/theocratic_mercenary_with_priest_019.png", True),
                         "theocratic_mercenary_with_priest_020": _load(
                             "images/theocratic_mercenary_with_priest_020.png", True),
                         "theocratic_mercenary_with_priest_021": _load(
                             "images/theocratic_mercenary_with_priest_021.png", True),
                         "theocratic_mercenary_with_priest_022": _load(
                             "images/theocratic_mercenary_with_priest_022.png", True),
                         "theocratic_mercenary_with_priest_023": _load(
                             "images/theocratic_mercenary_with_priest_023.png", True),
                         "theocratic_mercenary_with_priest_024": _load(
                             "images/theocratic_mercenary_with_priest_024.png", True),
                         "theocratic_mercenary_with_priest_025": _load(
                             "images/theocratic_mercenary_with_priest_025.png", True),
                         "theocratic_mercenary_with_priest_026": _load(
                             "images/theocratic_mercenary_with_priest_026.png", True),
                         "theocratic_mercenary_with_priest_027": _load(
                             "images/theocratic_mercenary_with_priest_027.png", True),
                         "theocratic_mercenary_with_priest_028": _load(
                             "images/theocratic_mercenary_with_priest_028.png", True),
                         "theocratic_mercenary_with_librarian_scholar_001": _load(
                             "images/theocratic_mercenary_with_librarian_scholar_001.png", True),
                         "theocratic_mercenary_with_librarian_scholar_002": _load(
                             "images/theocratic_mercenary_with_librarian_scholar_002.png", True),
                         "theocratic_mercenary_with_librarian_scholar_003": _load(
                             "images/theocratic_mercenary_with_librarian_scholar_003.png", True),
                         "theocratic_mercenary_with_librarian_scholar_004": _load(
                             "images/theocratic_mercenary_with_librarian_scholar_004.png", True),
                         "theocratic_mercenary_with_librarian_scholar_005": _load(
                             "images/theocratic_mercenary_with_librarian_scholar_005.png", True),
                         "theocratic_mercenary_with_librarian_scholar_006": _load(
                             "images/theocratic_mercenary_with_librarian_scholar_006.png", True),
                         "theocratic_mercenary_with_librarian_scholar_007": _load(
                             "images/theocratic_mercenary_with_librarian_scholar_007.png", True),
                         "theocratic_mercenary_with_librarian_scholar_008": _load(
                             "images/theocratic_mercenary_with_librarian_scholar_008.png", True),
                         "theocratic_mercenary_with_librarian_scholar_009": _load(
                             "images/theocratic_mercenary_with_librarian_scholar_009.png", True),
                         "theocratic_mercenary_with_librarian_scholar_010": _load(
                             "images/theocratic_mercenary_with_librarian_scholar_010.png", True),
                         "theocratic_mercenary_with_librarian_scholar_011": _load(
                             "images/theocratic_mercenary_with_librarian_scholar_011.png", True),
                         "theocratic_mercenary_with_librarian_scholar_012": _load(
                             "images/theocratic_mercenary_with_librarian_scholar_012.png", True),
                         "theocratic_mercenary_with_librarian_scholar_013": _load(
                             "images/theocratic_mercenary_with_librarian_scholar_013.png", True),
                         "theocratic_mercenary_with_librarian_scholar_014": _load(
                             "images/theocratic_mercenary_with_librarian_scholar_014.png", True),
                         "theocratic_mercenary_with_librarian_scholar_015": _load(
                             "images/theocratic_mercenary_with_librarian_scholar_015.png", True),
                         "theocratic_mercenary_with_librarian_scholar_016": _load(
                             "images/theocratic_mercenary_with_librarian_scholar_016.png", True),
                         "theocratic_mercenary_with_confession_booth_001": _load(
                             "images/theocratic_mercenary_with_confession_booth_001.png", True),
                         "theocratic_mercenary_with_confession_booth_002": _load(
                             "images/theocratic_mercenary_with_confession_booth_002.png", True),
                         "theocratic_mercenary_with_confession_booth_003": _load(
                             "images/theocratic_mercenary_with_confession_booth_003.png", True),
                         "theocratic_mercenary_with_confession_booth_004": _load(
                             "images/theocratic_mercenary_with_confession_booth_004.png", True),
                         "theocratic_mercenary_with_confession_booth_005": _load(
                             "images/theocratic_mercenary_with_confession_booth_005.png", True),
                         "theocratic_mercenary_with_confession_booth_006": _load(
                             "images/theocratic_mercenary_with_confession_booth_006.png", True),
                         "theocratic_battle_mercenary_with_priest_001": _load(
                             "images/theocratic_battle_mercenary_with_priest_001.png", True),
                         "theocratic_battle_mercenary_with_priest_002": _load(
                             "images/theocratic_battle_mercenary_with_priest_002.png", True),
                         "theocratic_battle_mercenary_with_priest_003": _load(
                             "images/theocratic_battle_mercenary_with_priest_003.png", True),
                         "theocratic_battle_mercenary_with_priest_004": _load(
                             "images/theocratic_battle_mercenary_with_priest_004.png", True),
                         "theocratic_battle_mercenary_with_priest_005": _load(
                             "images/theocratic_battle_mercenary_with_priest_005.png", True),
                         "theocratic_battle_mercenary_with_priest_006": _load(
                             "images/theocratic_battle_mercenary_with_priest_006.png", True),
                         "theocratic_battle_mercenary_with_priest_007": _load(
                             "images/theocratic_battle_mercenary_with_priest_007.png", True),
                         "theocratic_battle_mercenary_with_priest_008": _load(
                             "images/theocratic_battle_mercenary_with_priest_008.png", True),
                         "theocratic_battle_mercenary_with_priest_009": _load(
                             "images/theocratic_battle_mercenary_with_priest_009.png", True),
                         "theocratic_battle_mercenary_with_priest_010": _load(
                             "images/theocratic_battle_mercenary_with_priest_010.png", True),
                         "theocratic_battle_mercenary_with_priest_011": _load(
                             "images/theocratic_battle_mercenary_with_priest_011.png", True),
                         "theocratic_battle_mercenary_with_priest_012": _load(
                             "images/theocratic_battle_mercenary_with_priest_012.png", True),
                         "theocratic_battle_mercenary_with_priest_013": _load(
                             "images/theocratic_battle_mercenary_with_priest_013.png", True),
                         "theocratic_battle_mercenary_with_priest_014": _load(
                             "images/theocratic_battle_mercenary_with_priest_014.png", True),
                         "theocratic_battle_mercenary_with_priest_015": _load(
                             "images/theocratic_battle_mercenary_with_priest_015.png", True),
                         "theocratic_battle_mercenary_with_priest_016": _load(
                             "images/theocratic_battle_mercenary_with_priest_016.png", True),
                         "theocratic_battle_mercenary_with_priest_017": _load(
                             "images/theocratic_battle_mercenary_with_priest_017.png", True),
                         "theocratic_battle_mercenary_with_priest_018": _load(
                             "images/theocratic_battle_mercenary_with_priest_018.png", True),
                         "theocratic_battle_mercenary_with_priest_019": _load(
                             "images/theocratic_battle_mercenary_with_priest_019.png", True),
                         "theocratic_battle_mercenary_with_priest_020": _load(
                             "images/theocratic_battle_mercenary_with_priest_020.png", True),
                         "theocratic_battle_mercenary_with_priest_021": _load(
                             "images/theocratic_battle_mercenary_with_priest_021.png", True),
                         "theocratic_battle_mercenary_with_priest_022": _load(
                             "images/theocratic_battle_mercenary_with_priest_022.png", True),
                         "theocratic_battle_mercenary_with_priest_023": _load(
                             "images/theocratic_battle_mercenary_with_priest_023.png", True),
                         "theocratic_battle_mercenary_with_priest_024": _load(
                             "images/theocratic_battle_mercenary_with_priest_024.png", True),
                         "theocratic_battle_mercenary_with_priest_025": _load(
                             "images/theocratic_battle_mercenary_with_priest_025.png", True),
                         "theocratic_battle_mercenary_with_priest_026": _load(
                             "images/theocratic_battle_mercenary_with_priest_026.png", True),
                         "theocratic_battle_mercenary_with_priest_027": _load(
                             "images/theocratic_battle_mercenary_with_priest_027.png", True),
                         "theocratic_battle_mercenary_with_priest_028": _load(
                             "images/theocratic_battle_mercenary_with_priest_028.png", True),
                         "theocratic_battle_mercenary_with_priest_029": _load(
                             "images/theocratic_battle_mercenary_with_priest_029.png", True),
                         "theocratic_battle_mercenary_with_priest_030": _load(
                             "images/theocratic_battle_mercenary_with_priest_030.png", True),
                         "home_village_mercenary_with_memory_001": _load(
                             "images/home_village_mercenary_with_memory_001.png", True),
                         "home_village_mercenary_with_memory_002": _load(
                             "images/home_village_mercenary_with_memory_002.png", True),
                         "home_village_mercenary_with_memory_003": _load(
                             "images/home_village_mercenary_with_memory_003.png", True),
                         "home_village_mercenary_with_memory_004": _load(
                             "images/home_village_mercenary_with_memory_004.png", True),
                         "home_village_mercenary_with_memory_005": _load(
                             "images/home_village_mercenary_with_memory_005.png", True),
                         "home_village_mercenary_with_memory_006": _load(
                             "images/home_village_mercenary_with_memory_006.png", True),
                         "home_village_mercenary_with_memory_007": _load(
                             "images/home_village_mercenary_with_memory_007.png", True),
                         "home_village_mercenary_with_memory_008": _load(
                             "images/home_village_mercenary_with_memory_008.png", True),
                         "home_village_mercenary_with_memory_009": _load(
                             "images/home_village_mercenary_with_memory_009.png", True),
                         "home_village_mercenary_with_memory_010": _load(
                             "images/home_village_mercenary_with_memory_010.png", True),
                         "home_village_mercenary_with_memory_011": _load(
                             "images/home_village_mercenary_with_memory_011.png", True),
                         "home_village_mercenary_with_memory_012": _load(
                             "images/home_village_mercenary_with_memory_012.png", True),
                         "home_village_mercenary_with_memory_013": _load(
                             "images/home_village_mercenary_with_memory_013.png", True),
                         "home_village_mercenary_with_memory_014": _load(
                             "images/home_village_mercenary_with_memory_014.png", True),
                         "home_village_mercenary_with_memory_015": _load(
                             "images/home_village_mercenary_with_memory_015.png", True),
                         "home_village_mercenary_with_memory_016": _load(
                             "images/home_village_mercenary_with_memory_016.png", True),
                         "home_village_mercenary_with_memory_017": _load(
                             "images/home_village_mercenary_with_memory_017.png", True),
                         "home_village_mercenary_with_memory_018": _load(
                             "images/home_village_mercenary_with_memory_018.png", True),
                         "home_village_mercenary_with_memory_019": _load(
                             "images/home_village_mercenary_with_memory_019.png", True),
                         "home_village_mercenary_with_memory_020": _load(
                             "images/home_village_mercenary_with_memory_020.png", True),
                         "home_village_mercenary_with_memory_021": _load(
                             "images/home_village_mercenary_with_memory_021.png", True),
                         "home_village_mercenary_with_memory_022": _load(
                             "images/home_village_mercenary_with_memory_022.png", True),
                         "home_village_mercenary_with_memory_023": _load(
                             "images/home_village_mercenary_with_memory_023.png", True),
                         "home_village_mercenary_with_memory_024": _load(
                             "images/home_village_mercenary_with_memory_024.png", True),
                         "home_village_mercenary_with_memory_025": _load(
                             "images/home_village_mercenary_with_memory_025.png", True),
                         "home_village_mercenary_with_memory_026": _load(
                             "images/home_village_mercenary_with_memory_026.png", True),
                         "home_village_mercenary_with_memory_027": _load(
                             "images/home_village_mercenary_with_memory_027.png", True),
                         "outskirts_village_mercenary_with_village_chief_001": _load(
                             "images/outskirts_village_mercenary_with_village_chief_001.png", True),
                         "outskirts_village_mercenary_with_village_chief_002": _load(
                             "images/outskirts_village_mercenary_with_village_chief_002.png", True),
                         "outskirts_village_mercenary_with_village_chief_003": _load(
                             "images/outskirts_village_mercenary_with_village_chief_003.png", True),
                         "outskirts_village_mercenary_with_village_chief_004": _load(
                             "images/outskirts_village_mercenary_with_village_chief_004.png", True),
                         "outskirts_village_mercenary_with_village_chief_005": _load(
                             "images/outskirts_village_mercenary_with_village_chief_005.png", True),
                         "outskirts_village_mercenary_with_village_chief_006": _load(
                             "images/outskirts_village_mercenary_with_village_chief_006.png", True),
                         "outskirts_village_mercenary_with_village_chief_007": _load(
                             "images/outskirts_village_mercenary_with_village_chief_007.png", True),
                         "outskirts_village_mercenary_with_village_chief_008": _load(
                             "images/outskirts_village_mercenary_with_village_chief_008.png", True),
                         "outskirts_village_mercenary_with_village_chief_009": _load(
                             "images/outskirts_village_mercenary_with_village_chief_009.png", True),
                         "outskirts_village_mercenary_with_village_chief_010": _load(
                             "images/outskirts_village_mercenary_with_village_chief_010.png", True),
                         "outskirts_village_mercenary_with_village_chief_011": _load(
                             "images/outskirts_village_mercenary_with_village_chief_011.png", True),
                         "outskirts_market_mercenary_with_village_market_001": _load(
                             "images/outskirts_market_mercenary_with_village_market_001.png", True),
                         "outskirts_market_mercenary_with_village_market_002": _load(
                             "images/outskirts_market_mercenary_with_village_market_002.png", True),
                         "outskirts_market_mercenary_with_village_market_003": _load(
                             "images/outskirts_market_mercenary_with_village_market_003.png", True),
                         "outskirts_market_mercenary_with_village_market_004": _load(
                             "images/outskirts_market_mercenary_with_village_market_004.png", True),
                         "outskirts_market_mercenary_with_village_market_005": _load(
                             "images/outskirts_market_mercenary_with_village_market_005.png", True),
                         "outskirts_market_mercenary_with_village_market_006": _load(
                             "images/outskirts_market_mercenary_with_village_market_006.png", True),
                         "outskirts_market_mercenary_with_village_market_007": _load(
                             "images/outskirts_market_mercenary_with_village_market_007.png", True),
                         "outskirts_market_mercenary_with_village_market_008": _load(
                             "images/outskirts_market_mercenary_with_village_market_008.png", True),
                         "outskirts_village_mercenary_with_villagers_001": _load(
                             "images/outskirts_village_mercenary_with_villagers_001.png", True),
                         "outskirts_village_mercenary_with_villagers_002": _load(
                             "images/outskirts_village_mercenary_with_villagers_002.png", True),
                         "outskirts_village_mercenary_with_villagers_003": _load(
                             "images/outskirts_village_mercenary_with_villagers_003.png", True),
                         "outskirts_village_mercenary_with_villagers_004": _load(
                             "images/outskirts_village_mercenary_with_villagers_004.png", True),
                         "outskirts_village_mercenary_with_villagers_005": _load(
                             "images/outskirts_village_mercenary_with_villagers_005.png", True),
                         "outskirts_village_mercenary_with_villagers_006": _load(
                             "images/outskirts_village_mercenary_with_villagers_006.png", True),
                         "outskirts_village_mercenary_with_travelling_bard_001": _load(
                             "images/outskirts_village_mercenary_with_travelling_bard_001.png", True),
                         "outskirts_village_mercenary_with_travelling_bard_002": _load(
                             "images/outskirts_village_mercenary_with_travelling_bard_002.png", True),
                         "outskirts_village_mercenary_with_travelling_bard_003": _load(
                             "images/outskirts_village_mercenary_with_travelling_bard_003.png", True),
                         "outskirts_village_mercenary_with_travelling_bard_004": _load(
                             "images/outskirts_village_mercenary_with_travelling_bard_004.png", True),
                         "outskirts_village_mercenary_with_travelling_bard_005": _load(
                             "images/outskirts_village_mercenary_with_travelling_bard_005.png", True),
                         "outskirts_village_mercenary_with_travelling_bard_006": _load(
                             "images/outskirts_village_mercenary_with_travelling_bard_006.png", True),
                         "outskirts_village_mercenary_with_travelling_bard_007": _load(
                             "images/outskirts_village_mercenary_with_travelling_bard_007.png", True),
                         "outskirts_village_mercenary_with_travelling_bard_008": _load(
                             "images/outskirts_village_mercenary_with_travelling_bard_008.png", True),
                         "outskirts_village_mercenary_with_travelling_bard_009": _load(
                             "images/outskirts_village_mercenary_with_travelling_bard_009.png", True),
                         "outskirts_village_mercenary_with_travelling_bard_010": _load(
                             "images/outskirts_village_mercenary_with_travelling_bard_010.png", True),
                         "outskirts_village_mercenary_with_travelling_bard_011": _load(
                             "images/outskirts_village_mercenary_with_travelling_bard_011.png", True),
                         "outskirts_village_mercenary_with_travelling_bard_012": _load(
                             "images/outskirts_village_mercenary_with_travelling_bard_012.png", True),
                         "outskirts_village_mercenary_with_travelling_bard_013": _load(
                             "images/outskirts_village_mercenary_with_travelling_bard_013.png", True),
                         "outskirts_village_mercenary_with_travelling_bard_014": _load(
                             "images/outskirts_village_mercenary_with_travelling_bard_014.png", True),
                         "outskirts_village_mercenary_with_travelling_bard_015": _load(
                             "images/outskirts_village_mercenary_with_travelling_bard_015.png", True),
                         "outskirts_village_mercenary_with_travelling_bard_016": _load(
                             "images/outskirts_village_mercenary_with_travelling_bard_016.png", True),
                         "outskirts_village_mercenary_with_travelling_bard_017": _load(
                             "images/outskirts_village_mercenary_with_travelling_bard_017.png", True),
                         "outskirts_village_mercenary_with_travelling_bard_018": _load(
                             "images/outskirts_village_mercenary_with_travelling_bard_018.png", True),
                         "outskirts_village_mercenary_with_travelling_bard_019": _load(
                             "images/outskirts_village_mercenary_with_travelling_bard_019.png", True),
                         "outskirts_village_mercenary_with_travelling_bard_020": _load(
                             "images/outskirts_village_mercenary_with_travelling_bard_020.png", True),
                         "outskirts_village_mercenary_with_travelling_bard_021": _load(
                             "images/outskirts_village_mercenary_with_travelling_bard_021.png", True),
                         "zone_terror_mercenary_to_himself_001": _load(
                             "images/zone_terror_mercenary_to_himself_001.png", True),
                         "zone_terror_mercenary_to_himself_002": _load(
                             "images/zone_terror_mercenary_to_himself_002.png", True),
                         "zone_terror_mercenary_to_himself_003": _load(
                             "images/zone_terror_mercenary_to_himself_003.png", True),
                         "zone_terror_mercenary_to_himself_004": _load(
                             "images/zone_terror_mercenary_to_himself_004.png", True),
                         "zone_terror_mercenary_to_himself_005": _load(
                             "images/zone_terror_mercenary_to_himself_005.png", True),
                         "tribe_perimeter_mercenary_with_tribe_elder_001": _load(
                             "images/tribe_perimeter_mercenary_with_tribe_elder_001.png", True),
                         "tribe_perimeter_mercenary_with_tribe_elder_002": _load(
                             "images/tribe_perimeter_mercenary_with_tribe_elder_002.png", True),
                         "tribe_perimeter_mercenary_with_tribe_elder_003": _load(
                             "images/tribe_perimeter_mercenary_with_tribe_elder_003.png", True),
                         "tribe_perimeter_mercenary_with_tribe_elder_004": _load(
                             "images/tribe_perimeter_mercenary_with_tribe_elder_004.png", True),
                         "tribe_perimeter_mercenary_with_tribe_elder_005": _load(
                             "images/tribe_perimeter_mercenary_with_tribe_elder_005.png", True),
                         "tribe_perimeter_mercenary_with_tribe_elder_006": _load(
                             "images/tribe_perimeter_mercenary_with_tribe_elder_006.png", True),
                         "tribe_perimeter_mercenary_with_tribe_elder_007": _load(
                             "images/tribe_perimeter_mercenary_with_tribe_elder_007.png", True),
                         "tribe_perimeter_mercenary_with_tribe_elder_008": _load(
                             "images/tribe_perimeter_mercenary_with_tribe_elder_008.png", True),
                         "tribe_perimeter_mercenary_with_tribe_elder_009": _load(
                             "images/tribe_perimeter_mercenary_with_tribe_elder_009.png", True),
                         "tribe_perimeter_mercenary_with_tribe_elder_010": _load(
                             "images/tribe_perimeter_mercenary_with_tribe_elder_010.png", True),
                         "tribe_perimeter_mercenary_with_tribe_elder_011": _load(
                             "images/tribe_perimeter_mercenary_with_tribe_elder_011.png", True),
                         "tribe_perimeter_mercenary_with_tribe_elder_012": _load(
                             "images/tribe_perimeter_mercenary_with_tribe_elder_012.png", True),
                         "tribe_perimeter_warrior_with_assassin_001": _load(
                             "images/tribe_perimeter_warrior_with_assassin_001.png", True),
                         "tribe_perimeter_warrior_with_assassin_002": _load(
                             "images/tribe_perimeter_warrior_with_assassin_002.png", True),
                         "tribe_perimeter_warrior_with_assassin_003": _load(
                             "images/tribe_perimeter_warrior_with_assassin_003.png", True),
                         "tribe_perimeter_warrior_with_assassin_004": _load(
                             "images/tribe_perimeter_warrior_with_assassin_004.png", True),
                         "tribe_perimeter_warrior_with_assassin_005": _load(
                             "images/tribe_perimeter_warrior_with_assassin_005.png", True),
                         "tribe_storage_mercenary_with_shaman_001": _load(
                             "images/tribe_storage_mercenary_with_shaman_001.png", True),
                         "tribe_storage_mercenary_with_shaman_002": _load(
                             "images/tribe_storage_mercenary_with_shaman_002.png", True),
                         "tribe_storage_mercenary_with_shaman_003": _load(
                             "images/tribe_storage_mercenary_with_shaman_003.png", True),
                         "tribe_storage_mercenary_with_shaman_004": _load(
                             "images/tribe_storage_mercenary_with_shaman_004.png", True),
                         "tribe_storage_mercenary_with_shaman_005": _load(
                             "images/tribe_storage_mercenary_with_shaman_005.png", True),
                         "tribe_storage_mercenary_with_shaman_006": _load(
                             "images/tribe_storage_mercenary_with_shaman_006.png", True),
                         "tribe_storage_mercenary_with_shaman_007": _load(
                             "images/tribe_storage_mercenary_with_shaman_007.png", True),
                         "tribe_storage_mercenary_with_shaman_008": _load(
                             "images/tribe_storage_mercenary_with_shaman_008.png", True),
                         "tribe_storage_mercenary_with_shaman_009": _load(
                             "images/tribe_storage_mercenary_with_shaman_009.png", True),
                         "tribe_storage_mercenary_with_shaman_010": _load(
                             "images/tribe_storage_mercenary_with_shaman_010.png", True),
                         "tribe_storage_mercenary_with_shaman_011": _load(
                             "images/tribe_storage_mercenary_with_shaman_011.png", True),
                         "tribe_storage_mercenary_with_shaman_012": _load(
                             "images/tribe_storage_mercenary_with_shaman_012.png", True),
                         "tribe_storage_mercenary_with_shaman_013": _load(
                             "images/tribe_storage_mercenary_with_shaman_013.png", True),
                         "tribe_storage_mercenary_with_shaman_014": _load(
                             "images/tribe_storage_mercenary_with_shaman_014.png", True),
                         "tribe_storage_mercenary_with_shaman_015": _load(
                             "images/tribe_storage_mercenary_with_shaman_015.png", True),
                         "tribe_storage_mercenary_with_shaman_016": _load(
                             "images/tribe_storage_mercenary_with_shaman_016.png", True),
                         "tribe_storage_mercenary_with_shaman_017": _load(
                             "images/tribe_storage_mercenary_with_shaman_017.png", True),
                         "tribe_storage_mercenary_with_shaman_018": _load(
                             "images/tribe_storage_mercenary_with_shaman_018.png", True),
                         "tribe_storage_mercenary_with_shaman_019": _load(
                             "images/tribe_storage_mercenary_with_shaman_019.png", True),
                         "tribe_storage_mercenary_with_shaman_020": _load(
                             "images/tribe_storage_mercenary_with_shaman_020.png", True),
                         "tribe_storage_mercenary_with_shaman_021": _load(
                             "images/tribe_storage_mercenary_with_shaman_021.png", True),
                         "tribe_storage_mercenary_with_shaman_022": _load(
                             "images/tribe_storage_mercenary_with_shaman_022.png", True),
                         "tribe_tunnel_mercenary_with_tibe_chief_001": _load(
                             "images/tribe_tunnel_mercenary_with_tibe_chief_001.png", True),
                         "tribe_tunnel_mercenary_with_tibe_chief_002": _load(
                             "images/tribe_tunnel_mercenary_with_tibe_chief_002.png", True),
                         "tribe_tunnel_mercenary_with_tibe_chief_003": _load(
                             "images/tribe_tunnel_mercenary_with_tibe_chief_003.png", True),
                         "tribe_tunnel_mercenary_with_tibe_chief_004": _load(
                             "images/tribe_tunnel_mercenary_with_tibe_chief_004.png", True),
                         "tribe_tunnel_mercenary_with_tibe_chief_005": _load(
                             "images/tribe_tunnel_mercenary_with_tibe_chief_005.png", True),
                         "zone_terror_mercenary_with_shaman_001": _load(
                             "images/zone_terror_mercenary_with_shaman_001.png", True),
                         "zone_terror_mercenary_with_shaman_002": _load(
                             "images/zone_terror_mercenary_with_shaman_002.png", True),
                         "zone_terror_mercenary_with_shaman_003": _load(
                             "images/zone_terror_mercenary_with_shaman_003.png", True),
                         "zone_terror_mercenary_with_shaman_004": _load(
                             "images/zone_terror_mercenary_with_shaman_004.png", True),
                         "zone_terror_mercenary_with_shaman_005": _load(
                             "images/zone_terror_mercenary_with_shaman_005.png", True),
                         "zone_terror_mercenary_with_shaman_006": _load(
                             "images/zone_terror_mercenary_with_shaman_006.png", True),
                         "zone_terror_mercenary_with_shaman_007": _load(
                             "images/zone_terror_mercenary_with_shaman_007.png", True),
                         "zone_terror_mercenary_with_shaman_008": _load(
                             "images/zone_terror_mercenary_with_shaman_008.png", True),
                         "zone_terror_mercenary_with_shaman_009": _load(
                             "images/zone_terror_mercenary_with_shaman_009.png", True),
                         "zone_terror_mercenary_with_shaman_010": _load(
                             "images/zone_terror_mercenary_with_shaman_010.png", True),
                         "zone_terror_mercenary_with_shaman_011": _load(
                             "images/zone_terror_mercenary_with_shaman_011.png", True),
                         "zone_terror_mercenary_with_shaman_012": _load(
                             "images/zone_terror_mercenary_with_shaman_012.png", True),
                         "zone_terror_mercenary_with_shaman_013": _load(
                             "images/zone_terror_mercenary_with_shaman_013.png", True),
                         "zone_terror_mercenary_with_shaman_014": _load(
                             "images/zone_terror_mercenary_with_shaman_014.png", True),
                         "zone_terror_mercenary_with_shaman_015": _load(
                             "images/zone_terror_mercenary_with_shaman_015.png", True),
                         "zone_terror_mercenary_with_shaman_016": _load(
                             "images/zone_terror_mercenary_with_shaman_016.png", True),
                         "zone_terror_mercenary_with_shaman_017": _load(
                             "images/zone_terror_mercenary_with_shaman_017.png", True),
                         "port_city_mercenary_with_merchant_001": _load(
                             "images/port_city_mercenary_with_merchant_001.png", True),
                         "port_city_mercenary_with_merchant_002": _load(
                             "images/port_city_mercenary_with_merchant_002.png", True),
                         "port_city_mercenary_with_merchant_003": _load(
                             "images/port_city_mercenary_with_merchant_003.png", True),
                         "port_city_mercenary_with_merchant_004": _load(
                             "images/port_city_mercenary_with_merchant_004.png", True),
                         "port_city_mercenary_with_merchant_005": _load(
                             "images/port_city_mercenary_with_merchant_005.png", True),
                         "port_city_mercenary_with_merchant_006": _load(
                             "images/port_city_mercenary_with_merchant_006.png", True),
                         "port_city_mercenary_with_merchant_007": _load(
                             "images/port_city_mercenary_with_merchant_007.png", True),
                         "port_city_mercenary_with_merchant_008": _load(
                             "images/port_city_mercenary_with_merchant_008.png", True),
                         "port_city_mercenary_with_merchant_009": _load(
                             "images/port_city_mercenary_with_merchant_009.png", True),
                         "port_city_mercenary_with_merchant_010": _load(
                             "images/port_city_mercenary_with_merchant_010.png", True),
                         "port_city_mercenary_with_merchant_011": _load(
                             "images/port_city_mercenary_with_merchant_011.png", True),
                         "port_city_mercenary_with_merchant_012": _load(
                             "images/port_city_mercenary_with_merchant_012.png", True),
                         "port_city_mercenary_with_merchant_013": _load(
                             "images/port_city_mercenary_with_merchant_013.png", True),
                         "port_city_mercenary_with_merchant_014": _load(
                             "images/port_city_mercenary_with_merchant_014.png", True),
                         "port_city_mercenary_with_merchant_015": _load(
                             "images/port_city_mercenary_with_merchant_015.png", True),
                         "port_city_mercenary_with_merchant_016": _load(
                             "images/port_city_mercenary_with_merchant_016.png", True),
                         "port_city_mercenary_with_merchant_017": _load(
                             "images/port_city_mercenary_with_merchant_017.png", True),
                         "port_city_mercenary_with_merchant_018": _load(
                             "images/port_city_mercenary_with_merchant_018.png", True),
                         "port_city_mercenary_with_merchant_019": _load(
                             "images/port_city_mercenary_with_merchant_019.png", True),
                         "port_city_mercenary_with_merchant_020": _load(
                             "images/port_city_mercenary_with_merchant_020.png", True),
                         "port_city_mercenary_with_merchant_021": _load(
                             "images/port_city_mercenary_with_merchant_021.png", True),
                         "port_city_mercenary_with_merchant_022": _load(
                             "images/port_city_mercenary_with_merchant_022.png", True),
                         "port_city_mercenary_with_merchant_023": _load(
                             "images/port_city_mercenary_with_merchant_023.png", True),
                         "port_city_mercenary_with_merchant_024": _load(
                             "images/port_city_mercenary_with_merchant_024.png", True),
                         "port_city_mercenary_with_merchant_025": _load(
                             "images/port_city_mercenary_with_merchant_025.png", True),
                         "port_city_mercenary_with_merchant_026": _load(
                             "images/port_city_mercenary_with_merchant_026.png", True),
                         "port_city_mercenary_with_merchant_027": _load(
                             "images/port_city_mercenary_with_merchant_027.png", True),
                         "port_city_mercenary_with_merchant_028": _load(
                             "images/port_city_mercenary_with_merchant_028.png", True),
                         "port_city_mercenary_with_merchant_029": _load(
                             "images/port_city_mercenary_with_merchant_029.png", True),
                         "port_city_mercenary_with_merchant_030": _load(
                             "images/port_city_mercenary_with_merchant_030.png", True),
                         "port_city_mercenary_with_merchant_031": _load(
                             "images/port_city_mercenary_with_merchant_031.png", True),
                         "port_city_mercenary_with_merchant_032": _load(
                             "images/port_city_mercenary_with_merchant_032.png", True),
                         "port_city_mercenary_with_merchant_033": _load(
                             "images/port_city_mercenary_with_merchant_033.png", True),
                         "port_city_mercenary_with_merchant_034": _load(
                             "images/port_city_mercenary_with_merchant_034.png", True),
                         "port_city_mercenary_with_merchant_035": _load(
                             "images/port_city_mercenary_with_merchant_035.png", True),
                         "port_city_mercenary_with_merchant_036": _load(
                             "images/port_city_mercenary_with_merchant_036.png", True),
                         "port_city_mercenary_with_merchant_037": _load(
                             "images/port_city_mercenary_with_merchant_037.png", True),
                         "port_city_mercenary_decision_node_001": _load(
                             "images/port_city_mercenary_decision_node_001.png", True),
                         "port_city_mercenary_decision_node_002": _load(
                             "images/port_city_mercenary_decision_node_002.png", True),
                         "port_city_mercenary_decision_node_003": _load(
                             "images/port_city_mercenary_decision_node_003.png", True),
                         "port_city_mercenary_response_node_001": _load(
                             "images/port_city_mercenary_response_node_001.png", True),
                         "port_city_mercenary_response_node_002": _load(
                             "images/port_city_mercenary_response_node_002.png", True),
                         "port_city_mercenary_response_node_003": _load(
                             "images/port_city_mercenary_response_node_003.png", True),
                         "port_city_mercenary_with_tavern_keeper_001": _load(
                             "images/port_city_mercenary_with_tavern_keeper_001.png", True),
                         "port_city_mercenary_with_tavern_keeper_002": _load(
                             "images/port_city_mercenary_with_tavern_keeper_002.png", True),
                         "port_city_mercenary_with_tavern_keeper_003": _load(
                             "images/port_city_mercenary_with_tavern_keeper_003.png", True),
                         "port_city_mercenary_with_tavern_keeper_004": _load(
                             "images/port_city_mercenary_with_tavern_keeper_004.png", True),
                         "port_city_mercenary_with_tavern_keeper_005": _load(
                             "images/port_city_mercenary_with_tavern_keeper_005.png", True),
                         "port_city_mercenary_with_tavern_keeper_006": _load(
                             "images/port_city_mercenary_with_tavern_keeper_006.png", True),
                         "port_city_mercenary_with_tavern_keeper_007": _load(
                             "images/port_city_mercenary_with_tavern_keeper_007.png", True),
                         "port_city_mercenary_with_tavern_keeper_008": _load(
                             "images/port_city_mercenary_with_tavern_keeper_008.png", True),
                         "port_city_mercenary_with_tavern_keeper_009": _load(
                             "images/port_city_mercenary_with_tavern_keeper_009.png", True),
                         "port_city_mercenary_with_tavern_keeper_010": _load(
                             "images/port_city_mercenary_with_tavern_keeper_010.png", True),
                         "port_city_mercenary_with_tavern_keeper_011": _load(
                             "images/port_city_mercenary_with_tavern_keeper_011.png", True),
                         "port_city_mercenary_with_tavern_keeper_012": _load(
                             "images/port_city_mercenary_with_tavern_keeper_012.png", True),
                         "port_city_mercenary_with_tavern_keeper_013": _load(
                             "images/port_city_mercenary_with_tavern_keeper_013.png", True),
                         "port_city_mercenary_with_tavern_keeper_014": _load(
                             "images/port_city_mercenary_with_tavern_keeper_014.png", True),
                         "port_city_mercenary_with_tavern_keeper_015": _load(
                             "images/port_city_mercenary_with_tavern_keeper_015.png", True),
                         "port_city_mercenary_with_tavern_keeper_016": _load(
                             "images/port_city_mercenary_with_tavern_keeper_016.png", True),
                         "port_city_mercenary_with_tavern_keeper_017": _load(
                             "images/port_city_mercenary_with_tavern_keeper_017.png", True),
                         "port_city_mercenary_with_harbor_captain_001": _load(
                             "images/port_city_mercenary_with_harbor_captain_001.png", True),
                         "port_city_mercenary_with_harbor_captain_002": _load(
                             "images/port_city_mercenary_with_harbor_captain_002.png", True),
                         "port_city_mercenary_with_harbor_captain_003": _load(
                             "images/port_city_mercenary_with_harbor_captain_003.png", True),
                         "port_city_mercenary_with_harbor_captain_004": _load(
                             "images/port_city_mercenary_with_harbor_captain_004.png", True),
                         "port_city_mercenary_with_harbor_captain_005": _load(
                             "images/port_city_mercenary_with_harbor_captain_005.png", True),
                         "port_city_mercenary_with_harbor_captain_006": _load(
                             "images/port_city_mercenary_with_harbor_captain_006.png", True),
                         "port_city_mercenary_with_harbor_captain_007": _load(
                             "images/port_city_mercenary_with_harbor_captain_007.png", True),
                         "port_city_mercenary_with_harbor_captain_008": _load(
                             "images/port_city_mercenary_with_harbor_captain_008.png", True),
                         "cultist_island_mercenary_with_cultist_soldier_001": _load(
                             "images/cultist_island_mercenary_with_cultist_soldier_001.png", True),
                         "cultist_island_mercenary_with_cultist_soldier_002": _load(
                             "images/cultist_island_mercenary_with_cultist_soldier_002.png", True),
                         "cultist_island_mercenary_with_cultist_soldier_003": _load(
                             "images/cultist_island_mercenary_with_cultist_soldier_003.png", True),
                         "cultist_island_mercenary_with_cultist_soldier_004": _load(
                             "images/cultist_island_mercenary_with_cultist_soldier_004.png", True),
                         "cultist_island_mercenary_with_cultist_priest_001": _load(
                             "images/cultist_island_mercenary_with_cultist_priest_001.png", True),
                         "cultist_island_mercenary_with_cultist_priest_002": _load(
                             "images/cultist_island_mercenary_with_cultist_priest_002.png", True),
                         "cultist_island_mercenary_with_cultist_priest_003": _load(
                             "images/cultist_island_mercenary_with_cultist_priest_003.png", True),
                         "cultist_island_mercenary_with_cultist_priest_004": _load(
                             "images/cultist_island_mercenary_with_cultist_priest_004.png", True),
                         "cultist_island_mercenary_with_experiments_001": _load(
                             "images/cultist_island_mercenary_with_experiments_001.png", True),
                         "cultist_island_mercenary_with_experiments_002": _load(
                             "images/cultist_island_mercenary_with_experiments_002.png", True),
                         "cultist_island_mercenary_with_experiments_003": _load(
                             "images/cultist_island_mercenary_with_experiments_003.png", True),
                         "cultist_island_mercenary_with_experiments_004": _load(
                             "images/cultist_island_mercenary_with_experiments_004.png", True),
                         "cultist_island_mercenary_with_experiments_005": _load(
                             "images/cultist_island_mercenary_with_experiments_005.png", True),
                         "cultist_island_mercenary_with_experiments_006": _load(
                             "images/cultist_island_mercenary_with_experiments_006.png", True),
                         "cultist_island_mercenary_with_experiments_007": _load(
                             "images/cultist_island_mercenary_with_experiments_007.png", True),
                         "cultist_island_mercenary_with_experiments_008": _load(
                             "images/cultist_island_mercenary_with_experiments_008.png", True),
                         "cultist_island_mercenary_with_funeris_001": _load(
                             "images/cultist_island_mercenary_with_funeris_001.png", True),
                         "cultist_island_mercenary_with_funeris_002": _load(
                             "images/cultist_island_mercenary_with_funeris_002.png", True),
                         "cultist_island_mercenary_with_funeris_003": _load(
                             "images/cultist_island_mercenary_with_funeris_003.png", True),
                         "cultist_island_mercenary_with_funeris_004": _load(
                             "images/cultist_island_mercenary_with_funeris_004.png", True),
                         "cultist_island_mercenary_with_funeris_005": _load(
                             "images/cultist_island_mercenary_with_funeris_005.png", True),
                         "cultist_island_mercenary_with_funeris_006": _load(
                             "images/cultist_island_mercenary_with_funeris_006.png", True),
                         "cultist_island_mercenary_with_funeris_007": _load(
                             "images/cultist_island_mercenary_with_funeris_007.png", True),
                         "cultist_island_mercenary_with_funeris_008": _load(
                             "images/cultist_island_mercenary_with_funeris_008.png", True),
                         "cultist_island_mercenary_with_funeris_009": _load(
                             "images/cultist_island_mercenary_with_funeris_009.png", True),
                         "cultist_island_mercenary_with_funeris_010": _load(
                             "images/cultist_island_mercenary_with_funeris_010.png", True),
                         "cultist_island_mercenary_with_funeris_011": _load(
                             "images/cultist_island_mercenary_with_funeris_011.png", True),
                         "cultist_island_mercenary_with_funeris_012": _load(
                             "images/cultist_island_mercenary_with_funeris_012.png", True),
                         "cultist_island_mercenary_with_funeris_013": _load(
                             "images/cultist_island_mercenary_with_funeris_013.png", True),
                         "cultist_island_mercenary_with_funeris_014": _load(
                             "images/cultist_island_mercenary_with_funeris_014.png", True),
                         "cultist_island_mercenary_with_funeris_015": _load(
                             "images/cultist_island_mercenary_with_funeris_015.png", True),
                         "cultist_island_mercenary_with_funeris_016": _load(
                             "images/cultist_island_mercenary_with_funeris_016.png", True),
                         "cultist_island_mercenary_with_funeris_017": _load(
                             "images/cultist_island_mercenary_with_funeris_017.png", True),
                         "cultist_island_mercenary_with_funeris_018": _load(
                             "images/cultist_island_mercenary_with_funeris_018.png", True),
                         "cultist_island_mercenary_with_funeris_019": _load(
                             "images/cultist_island_mercenary_with_funeris_019.png", True),
                         "cultist_island_mercenary_with_funeris_020": _load(
                             "images/cultist_island_mercenary_with_funeris_020.png", True),
                         "cultist_island_mercenary_with_funeris_021": _load(
                             "images/cultist_island_mercenary_with_funeris_021.png", True),
                         "cultist_island_mercenary_with_funeris_022": _load(
                             "images/cultist_island_mercenary_with_funeris_022.png", True),
                         "cultist_island_mercenary_with_funeris_023": _load(
                             "images/cultist_island_mercenary_with_funeris_023.png", True),
                         "cultist_island_mercenary_with_funeris_024": _load(
                             "images/cultist_island_mercenary_with_funeris_024.png", True),
                         "cultist_island_mercenary_with_funeris_025": _load(
                             "images/cultist_island_mercenary_with_funeris_025.png", True),
                         "cultist_island_mercenary_with_funeris_026": _load(
                             "images/cultist_island_mercenary_with_funeris_026.png", True),
                         "cultist_island_mercenary_with_funeris_027": _load(
                             "images/cultist_island_mercenary_with_funeris_027.png", True),
                         "cultist_island_mercenary_with_funeris_028": _load(
                             "images/cultist_island_mercenary_with_funeris_028.png", True),
                         "cultist_island_mercenary_with_funeris_029": _load(
                             "images/cultist_island_mercenary_with_funeris_029.png", True),
                         "cultist_island_mercenary_with_funeris_030": _load(
                             "images/cultist_island_mercenary_with_funeris_030.png", True),
                         "cultist_island_mercenary_with_cult_leader_001": _load(
                             "images/cultist_island_mercenary_with_cult_leader_001.png", True),
                         "cultist_island_mercenary_with_cult_leader_002": _load(
                             "images/cultist_island_mercenary_with_cult_leader_002.png", True),
                         "cultist_island_mercenary_with_cult_leader_003": _load(
                             "images/cultist_island_mercenary_with_cult_leader_003.png", True),
                         "cultist_island_mercenary_with_cult_leader_004": _load(
                             "images/cultist_island_mercenary_with_cult_leader_004.png", True),
                         "cultist_island_mercenary_with_cult_leader_005": _load(
                             "images/cultist_island_mercenary_with_cult_leader_005.png", True),
                         "cultist_island_mercenary_with_cult_leader_006": _load(
                             "images/cultist_island_mercenary_with_cult_leader_006.png", True),
                         "cultist_island_mercenary_with_cult_leader_007": _load(
                             "images/cultist_island_mercenary_with_cult_leader_007.png", True),
                         "cultist_island_mercenary_with_cult_leader_008": _load(
                             "images/cultist_island_mercenary_with_cult_leader_008.png", True),
                         "cultist_island_mercenary_with_cult_leader_009": _load(
                             "images/cultist_island_mercenary_with_cult_leader_009.png", True),
                         "cultist_island_mercenary_with_cult_leader_010": _load(
                             "images/cultist_island_mercenary_with_cult_leader_010.png", True),
                         "cultist_island_mercenary_with_cult_leader_011": _load(
                             "images/cultist_island_mercenary_with_cult_leader_011.png", True),
                         "cultist_island_mercenary_with_cult_leader_012": _load(
                             "images/cultist_island_mercenary_with_cult_leader_012.png", True),
                         "cultist_island_mercenary_with_cult_leader_013": _load(
                             "images/cultist_island_mercenary_with_cult_leader_013.png", True),
                         "cultist_island_mercenary_with_cult_leader_014": _load(
                             "images/cultist_island_mercenary_with_cult_leader_014.png", True),
                         "cultist_island_mercenary_with_cult_leader_015": _load(
                             "images/cultist_island_mercenary_with_cult_leader_015.png", True),
                         "cultist_island_mercenary_with_cult_leader_016": _load(
                             "images/cultist_island_mercenary_with_cult_leader_016.png", True),
                         "cultist_island_mercenary_with_cult_leader_017": _load(
                             "images/cultist_island_mercenary_with_cult_leader_017.png", True),
                         "cultist_island_mercenary_with_cult_leader_018": _load(
                             "images/cultist_island_mercenary_with_cult_leader_018.png", True),
                         "cultist_island_mercenary_with_cult_leader_019": _load(
                             "images/cultist_island_mercenary_with_cult_leader_019.png", True),
                         "cultist_island_mercenary_with_cult_leader_020": _load(
                             "images/cultist_island_mercenary_with_cult_leader_020.png", True),

                         # CULTIST DIALOGUE
                         "cultist_island_funeris_with_cult_leader_001": _load(
                             "images/cultist_island_funeris_with_cult_leader_001.png", True),
                         "cultist_island_funeris_with_cult_leader_002": _load(
                             "images/cultist_island_funeris_with_cult_leader_002.png", True),
                         "cultist_island_funeris_with_cult_leader_003": _load(
                             "images/cultist_island_funeris_with_cult_leader_003.png", True),
                         "cultist_island_funeris_with_cult_leader_004": _load(
                             "images/cultist_island_funeris_with_cult_leader_004.png", True),
                         "cultist_island_funeris_with_cult_leader_005": _load(
                             "images/cultist_island_funeris_with_cult_leader_005.png", True),
                         "cultist_island_funeris_with_cult_leader_006": _load(
                             "images/cultist_island_funeris_with_cult_leader_006.png", True),
                         "cultist_island_funeris_with_cult_leader_007": _load(
                             "images/cultist_island_funeris_with_cult_leader_007.png", True),
                         "cultist_island_funeris_with_cult_leader_008": _load(
                             "images/cultist_island_funeris_with_cult_leader_008.png", True),
                         "cultist_island_funeris_with_cult_leader_009": _load(
                             "images/cultist_island_funeris_with_cult_leader_009.png", True),
                         "cultist_island_funeris_with_cult_leader_010": _load(
                             "images/cultist_island_funeris_with_cult_leader_010.png", True),
                         "cultist_island_funeris_with_cult_leader_011": _load(
                             "images/cultist_island_funeris_with_cult_leader_011.png", True),
                         "cultist_island_funeris_with_cult_leader_012": _load(
                             "images/cultist_island_funeris_with_cult_leader_012.png", True),
                         "cultist_island_funeris_with_cult_leader_013": _load(
                             "images/cultist_island_funeris_with_cult_leader_013.png", True),
                         "cultist_island_funeris_with_cult_leader_014": _load(
                             "images/cultist_island_funeris_with_cult_leader_014.png", True),
                         "cultist_island_funeris_with_cult_leader_015": _load(
                             "images/cultist_island_funeris_with_cult_leader_015.png", True),
                         "cultist_island_funeris_with_cult_soldiers_001": _load(
                             "images/cultist_island_funeris_with_cult_soldiers_001.png", True),
                         "cultist_island_funeris_with_cult_soldiers_002": _load(
                             "images/cultist_island_funeris_with_cult_soldiers_002.png", True),
                         "cultist_island_funeris_with_cult_soldiers_003": _load(
                             "images/cultist_island_funeris_with_cult_soldiers_003.png", True),
                         "cultist_island_funeris_with_cult_soldiers_004": _load(
                             "images/cultist_island_funeris_with_cult_soldiers_004.png", True),
                         "cultist_island_funeris_with_cult_soldiers_005": _load(
                             "images/cultist_island_funeris_with_cult_soldiers_005.png", True),
                         "cultist_island_funeris_with_cult_soldiers_006": _load(
                             "images/cultist_island_funeris_with_cult_soldiers_006.png", True),
                         "zone_terrors_funeris_to_herself_001": _load("images/zone_terrors_funeris_to_herself_001.png",
                                                                      True),
                         "zone_terrors_funeris_to_herself_002": _load("images/zone_terrors_funeris_to_herself_002.png",
                                                                      True),
                         "zone_terrors_funeris_to_herself_003": _load("images/zone_terrors_funeris_to_herself_003.png",
                                                                      True),
                         "zone_terrors_funeris_to_herself_004": _load("images/zone_terrors_funeris_to_herself_004.png",
                                                                      True),
                         "zone_terrors_funeris_to_herself_005": _load("images/zone_terrors_funeris_to_herself_005.png",
                                                                      True),
                         "zone_terrors_funeris_to_herself_006": _load("images/zone_terrors_funeris_to_herself_006.png",
                                                                      True),
                         "zone_terrors_funeris_to_herself_007": _load("images/zone_terrors_funeris_to_herself_007.png",
                                                                      True),
                         "zone_terrors_funeris_to_herself_008": _load("images/zone_terrors_funeris_to_herself_008.png",
                                                                      True),
                         "zone_terrors_funeris_to_herself_009": _load("images/zone_terrors_funeris_to_herself_009.png",
                                                                      True),
                         "zone_terrors_funeris_to_herself_010": _load("images/zone_terrors_funeris_to_herself_010.png",
                                                                      True),
                         "zone_terrors_funeris_to_herself_011": _load("images/zone_terrors_funeris_to_herself_011.png",
                                                                      True),
                         "zone_terrors_funeris_to_herself_012": _load("images/zone_terrors_funeris_to_herself_012.png",
                                                                      True),
                         "zone_terrors_funeris_to_herself_013": _load("images/zone_terrors_funeris_to_herself_013.png",
                                                                      True),
                         "zone_terrors_funeris_to_herself_014": _load("images/zone_terrors_funeris_to_herself_014.png",
                                                                      True),
                         "home_village_funeris_to_memory_fragment_001": _load(
                             "images/home_village_funeris_to_memory_fragment_001.png", True),
                         "home_village_funeris_to_memory_fragment_002": _load(
                             "images/home_village_funeris_to_memory_fragment_002.png", True),
                         "home_village_funeris_to_memory_fragment_003": _load(
                             "images/home_village_funeris_to_memory_fragment_003.png", True),
                         "home_village_funeris_to_memory_fragment_004": _load(
                             "images/home_village_funeris_to_memory_fragment_004.png", True),
                         "home_village_funeris_to_memory_fragment_005": _load(
                             "images/home_village_funeris_to_memory_fragment_005.png", True),
                         "home_village_funeris_to_memory_fragment_006": _load(
                             "images/home_village_funeris_to_memory_fragment_006.png", True),
                         "home_village_funeris_to_memory_fragment_007": _load(
                             "images/home_village_funeris_to_memory_fragment_007.png", True),
                         "home_village_funeris_to_memory_fragment_008": _load(
                             "images/home_village_funeris_to_memory_fragment_008.png", True),
                         "home_village_funeris_to_memory_fragment_009": _load(
                             "images/home_village_funeris_to_memory_fragment_009.png", True),
                         "home_village_funeris_to_memory_fragment_010": _load(
                             "images/home_village_funeris_to_memory_fragment_010.png", True),
                         "home_village_funeris_to_memory_fragment_011": _load(
                             "images/home_village_funeris_to_memory_fragment_011.png", True),
                         "home_village_funeris_to_memory_fragment_012": _load(
                             "images/home_village_funeris_to_memory_fragment_012.png", True),
                         "home_village_funeris_to_memory_fragment_013": _load(
                             "images/home_village_funeris_to_memory_fragment_013.png", True),
                         "home_village_funeris_to_memory_fragment_014": _load(
                             "images/home_village_funeris_to_memory_fragment_014.png", True),
                         "home_village_funeris_to_memory_fragment_015": _load(
                             "images/home_village_funeris_to_memory_fragment_015.png", True),
                         "home_village_funeris_to_memory_fragment_016": _load(
                             "images/home_village_funeris_to_memory_fragment_016.png", True),
                         "home_village_funeris_to_memory_fragment_017": _load(
                             "images/home_village_funeris_to_memory_fragment_017.png", True),
                         "home_village_funeris_to_memory_fragment_018": _load(
                             "images/home_village_funeris_to_memory_fragment_018.png", True),
                         "home_village_funeris_to_memory_fragment_019": _load(
                             "images/home_village_funeris_to_memory_fragment_019.png", True),
                         "home_village_funeris_to_memory_fragment_020": _load(
                             "images/home_village_funeris_to_memory_fragment_020.png", True),
                         "home_village_funeris_decision_node_001": _load(
                             "images/home_village_funeris_decision_node_001.png", True),
                         "home_village_funeris_decision_node_002": _load(
                             "images/home_village_funeris_decision_node_002.png", True),
                         "home_village_funeris_decision_node_003": _load(
                             "images/home_village_funeris_decision_node_003.png", True),
                         "home_village_funeris_response_node_001": _load(
                             "images/home_village_funeris_response_node_001.png", True),
                         "home_village_funeris_response_node_002": _load(
                             "images/home_village_funeris_response_node_002.png", True),
                         "home_village_funeris_response_node_003": _load(
                             "images/home_village_funeris_response_node_003.png", True),
                         "laboratory_funeris_with_priest_001": _load("images/laboratory_funeris_with_priest_001.png",
                                                                     True),
                         "laboratory_funeris_with_priest_002": _load("images/laboratory_funeris_with_priest_002.png",
                                                                     True),
                         "laboratory_funeris_with_priest_003": _load("images/laboratory_funeris_with_priest_003.png",
                                                                     True),
                         "laboratory_funeris_with_priest_004": _load("images/laboratory_funeris_with_priest_004.png",
                                                                     True),
                         "laboratory_funeris_with_priest_005": _load("images/laboratory_funeris_with_priest_005.png",
                                                                     True),
                         "laboratory_funeris_with_priest_006": _load("images/laboratory_funeris_with_priest_006.png",
                                                                     True),
                         "laboratory_funeris_with_priest_007": _load("images/laboratory_funeris_with_priest_007.png",
                                                                     True),
                         "laboratory_funeris_with_priest_008": _load("images/laboratory_funeris_with_priest_008.png",
                                                                     True),
                         "laboratory_funeris_with_priest_009": _load("images/laboratory_funeris_with_priest_009.png",
                                                                     True),
                         "laboratory_funeris_with_priest_010": _load("images/laboratory_funeris_with_priest_010.png",
                                                                     True),
                         "laboratory_funeris_with_priest_011": _load("images/laboratory_funeris_with_priest_011.png",
                                                                     True),
                         "laboratory_funeris_with_priest_012": _load("images/laboratory_funeris_with_priest_012.png",
                                                                     True),
                         "laboratory_funeris_with_priest_013": _load("images/laboratory_funeris_with_priest_013.png",
                                                                     True),
                         "laboratory_funeris_with_priest_014": _load("images/laboratory_funeris_with_priest_014.png",
                                                                     True),
                         "laboratory_funeris_with_priest_015": _load("images/laboratory_funeris_with_priest_015.png",
                                                                     True),
                         "laboratory_funeris_with_priest_016": _load("images/laboratory_funeris_with_priest_016.png",
                                                                     True),
                         "laboratory_funeris_with_priest_017": _load("images/laboratory_funeris_with_priest_017.png",
                                                                     True),
                         "laboratory_funeris_with_priest_018": _load("images/laboratory_funeris_with_priest_018.png",
                                                                     True),
                         "laboratory_funeris_with_priest_019": _load("images/laboratory_funeris_with_priest_019.png",
                                                                     True),
                         "laboratory_funeris_with_priest_020": _load("images/laboratory_funeris_with_priest_020.png",
                                                                     True),
                         "laboratory_funeris_with_priest_021": _load("images/laboratory_funeris_with_priest_021.png",
                                                                     True),
                         "laboratory_funeris_with_priest_022": _load("images/laboratory_funeris_with_priest_022.png",
                                                                     True),
                         "laboratory_funeris_with_priest_023": _load("images/laboratory_funeris_with_priest_023.png",
                                                                     True),
                         "laboratory_funeris_with_priest_024": _load("images/laboratory_funeris_with_priest_024.png",
                                                                     True),
                         "laboratory_funeris_with_priest_025": _load("images/laboratory_funeris_with_priest_025.png",
                                                                     True),
                         "laboratory_funeris_with_priest_026": _load("images/laboratory_funeris_with_priest_026.png",
                                                                     True),
                         "laboratory_funeris_with_priest_027": _load("images/laboratory_funeris_with_priest_027.png",
                                                                     True),
                         "laboratory_funeris_with_priest_028": _load("images/laboratory_funeris_with_priest_028.png",
                                                                     True),
                         "laboratory_funeris_with_priest_029": _load("images/laboratory_funeris_with_priest_029.png",
                                                                     True),
                         "laboratory_funeris_with_priest_030": _load("images/laboratory_funeris_with_priest_030.png",
                                                                     True),
                         "laboratory_funeris_with_priest_031": _load("images/laboratory_funeris_with_priest_031.png",
                                                                     True),
                         "laboratory_funeris_with_priest_032": _load("images/laboratory_funeris_with_priest_032.png",
                                                                     True),
                         "laboratory_funeris_with_priest_033": _load("images/laboratory_funeris_with_priest_033.png",
                                                                     True),
                         "laboratory_funeris_with_priest_034": _load("images/laboratory_funeris_with_priest_034.png",
                                                                     True),
                         "laboratory_funeris_with_assassin_001": _load(
                             "images/laboratory_funeris_with_assassin_001.png", True),

                         # PRIEST DIALOGUE
                         "walled_priest_with_draft_officer_001": _load(
                             "images/walled_priest_with_draft_officer_001.png", True),
                         "walled_priest_with_draft_officer_002": _load(
                             "images/walled_priest_with_draft_officer_002.png", True),
                         "walled_priest_with_draft_officer_003": _load(
                             "images/walled_priest_with_draft_officer_003.png", True),
                         "walled_priest_with_draft_officer_004": _load(
                             "images/walled_priest_with_draft_officer_004.png", True),
                         "walled_chapel_priest_with_guard_001": _load("images/walled_chapel_priest_with_guard_001.png",
                                                                      True),
                         "walled_chapel_priest_with_guard_002": _load("images/walled_chapel_priest_with_guard_002.png",
                                                                      True),
                         "walled_chapel_priest_with_guard_003": _load("images/walled_chapel_priest_with_guard_003.png",
                                                                      True),
                         "walled_chapel_priest_with_guard_004": _load("images/walled_chapel_priest_with_guard_004.png",
                                                                      True),
                         "walled_chapel_priest_with_guard_005": _load("images/walled_chapel_priest_with_guard_005.png",
                                                                      True),
                         "walled_chapel_priest_with_guard_006": _load("images/walled_chapel_priest_with_guard_006.png",
                                                                      True),
                         "theocratic_priest_with_church_attendance_001": _load(
                             "images/theocratic_priest_with_church_attendance_001.png", True),
                         "theocratic_priest_with_church_attendance_002": _load(
                             "images/theocratic_priest_with_church_attendance_002.png", True),
                         "theocratic_priest_with_church_attendance_003": _load(
                             "images/theocratic_priest_with_church_attendance_003.png", True),
                         "theocratic_priest_with_church_attendance_004": _load(
                             "images/theocratic_priest_with_church_attendance_004.png", True),
                         "theocratic_priest_with_church_attendance_005": _load(
                             "images/theocratic_priest_with_church_attendance_005.png", True),
                         "theocratic_priest_with_church_attendance_006": _load(
                             "images/theocratic_priest_with_church_attendance_006.png", True),
                         "theocratic_priest_with_church_attendance_007": _load(
                             "images/theocratic_priest_with_church_attendance_007.png", True),
                         "theocratic_priest_with_church_attendance_008": _load(
                             "images/theocratic_priest_with_church_attendance_008.png", True),
                         "theocratic_priest_with_church_attendance_009": _load(
                             "images/theocratic_priest_with_church_attendance_009.png", True),
                         "theocratic_priest_with_church_attendance_010": _load(
                             "images/theocratic_priest_with_church_attendance_010.png", True),
                         "theocratic_priest_with_church_attendance_011": _load(
                             "images/theocratic_priest_with_church_attendance_011.png", True),
                         "theocratic_priest_with_church_attendance_012": _load(
                             "images/theocratic_priest_with_church_attendance_012.png", True),
                         "theocratic_priest_with_church_attendance_013": _load(
                             "images/theocratic_priest_with_church_attendance_013.png", True),
                         "theocratic_priest_with_church_attendance_014": _load(
                             "images/theocratic_priest_with_church_attendance_014.png", True),
                         "theocratic_priest_with_church_attendance_015": _load(
                             "images/theocratic_priest_with_church_attendance_015.png", True),
                         "theocratic_priest_with_church_attendance_016": _load(
                             "images/theocratic_priest_with_church_attendance_016.png", True),
                         "theocratic_priest_with_church_attendance_017": _load(
                             "images/theocratic_priest_with_church_attendance_017.png", True),
                         "theocratic_priest_with_church_attendance_018": _load(
                             "images/theocratic_priest_with_church_attendance_018.png", True),
                         "theocratic_priest_with_church_attendance_019": _load(
                             "images/theocratic_priest_with_church_attendance_019.png", True),
                         "theocratic_priest_with_church_attendance_020": _load(
                             "images/theocratic_priest_with_church_attendance_020.png", True),
                         "theocratic_priest_with_church_official_001": _load(
                             "images/theocratic_priest_with_church_official_001.png", True),
                         "theocratic_priest_with_church_official_002": _load(
                             "images/theocratic_priest_with_church_official_002.png", True),
                         "theocratic_priest_with_church_official_003": _load(
                             "images/theocratic_priest_with_church_official_003.png", True),
                         "theocratic_priest_with_church_official_004": _load(
                             "images/theocratic_priest_with_church_official_004.png", True),
                         "theocratic_priest_with_church_official_005": _load(
                             "images/theocratic_priest_with_church_official_005.png", True),
                         "theocratic_priest_with_church_official_006": _load(
                             "images/theocratic_priest_with_church_official_006.png", True),
                         "theocratic_priest_with_church_official_007": _load(
                             "images/theocratic_priest_with_church_official_007.png", True),
                         "theocratic_priest_with_church_official_008": _load(
                             "images/theocratic_priest_with_church_official_008.png", True),
                         "theocratic_priest_with_church_official_009": _load(
                             "images/theocratic_priest_with_church_official_009.png", True),
                         "theocratic_priest_with_church_official_010": _load(
                             "images/theocratic_priest_with_church_official_010.png", True),
                         "theocratic_priest_with_church_official_011": _load(
                             "images/theocratic_priest_with_church_official_011.png", True),
                         "theocratic_priest_with_church_official_012": _load(
                             "images/theocratic_priest_with_church_official_012.png", True),
                         "theocratic_priest_with_church_official_013": _load(
                             "images/theocratic_priest_with_church_official_013.png", True),
                         "theocratic_priest_with_church_official_014": _load(
                             "images/theocratic_priest_with_church_official_014.png", True),
                         "theocratic_priest_with_church_official_015": _load(
                             "images/theocratic_priest_with_church_official_015.png", True),
                         "theocratic_priest_with_church_official_016": _load(
                             "images/theocratic_priest_with_church_official_016.png", True),
                         "theocratic_priest_with_church_official_017": _load(
                             "images/theocratic_priest_with_church_official_017.png", True),
                         "theocratic_priest_with_church_official_018": _load(
                             "images/theocratic_priest_with_church_official_018.png", True),
                         "laboratory_priest_to_himself_001": _load("images/laboratory_priest_to_himself_001.png", True),
                         "laboratory_priest_to_himself_002": _load("images/laboratory_priest_to_himself_002.png", True),
                         "laboratory_priest_to_himself_003": _load("images/laboratory_priest_to_himself_003.png", True),
                         "laboratory_priest_to_himself_004": _load("images/laboratory_priest_to_himself_004.png", True),
                         "laboratory_priest_to_himself_005": _load("images/laboratory_priest_to_himself_005.png", True),
                         "laboratory_priest_to_himself_006": _load("images/laboratory_priest_to_himself_006.png", True),
                         "laboratory_priest_to_himself_007": _load("images/laboratory_priest_to_himself_007.png", True),
                         "laboratory_priest_to_himself_008": _load("images/laboratory_priest_to_himself_008.png", True),
                         "laboratory_priest_to_himself_009": _load("images/laboratory_priest_to_himself_009.png", True),
                         "laboratory_priest_decision_node_001": _load("images/laboratory_priest_decision_node_001.png",
                                                                      True),
                         "laboratory_priest_decision_node_002": _load("images/laboratory_priest_decision_node_002.png",
                                                                      True),
                         "laboratory_priest_decision_node_003": _load("images/laboratory_priest_decision_node_003.png",
                                                                      True),
                         "laboratory_priest_response_node_001": _load("images/laboratory_priest_response_node_001.png",
                                                                      True),
                         "laboratory_priest_response_node_002": _load("images/laboratory_priest_response_node_002.png",
                                                                      True),
                         "laboratory_priest_response_node_003": _load("images/laboratory_priest_response_node_003.png",
                                                                      True),
                         "zone_terror_priest_with_medical_staff_001": _load(
                             "images/zone_terror_priest_with_medical_staff_001.png", True),
                         "zone_terror_priest_with_medical_staff_002": _load(
                             "images/zone_terror_priest_with_medical_staff_002.png", True),
                         "zone_terror_priest_with_medical_staff_003": _load(
                             "images/zone_terror_priest_with_medical_staff_003.png", True),
                         "zone_terror_priest_with_medical_staff_004": _load(
                             "images/zone_terror_priest_with_medical_staff_004.png", True),
                         "zone_terror_priest_with_medical_staff_005": _load(
                             "images/zone_terror_priest_with_medical_staff_005.png", True),
                         "zone_terror_priest_with_church_knight_001": _load(
                             "images/zone_terror_priest_with_church_knight_001.png", True),
                         "zone_terror_priest_with_church_knight_002": _load(
                             "images/zone_terror_priest_with_church_knight_002.png", True),
                         "zone_terror_priest_with_church_knight_003": _load(
                             "images/zone_terror_priest_with_church_knight_003.png", True),
                         "zone_terror_priest_with_church_knight_004": _load(
                             "images/zone_terror_priest_with_church_knight_004.png", True),
                         "zone_terror_priest_with_church_knight_005": _load(
                             "images/zone_terror_priest_with_church_knight_005.png", True),
                         "zone_terror_priest_with_church_knight_006": _load(
                             "images/zone_terror_priest_with_church_knight_006.png", True),
                         "zone_terror_priest_with_church_knight_007": _load(
                             "images/zone_terror_priest_with_church_knight_007.png", True),
                         "zone_terror_priest_with_church_knight_008": _load(
                             "images/zone_terror_priest_with_church_knight_008.png", True),
                         "laboratory_priest_to_medical_staff_001": _load(
                             "images/laboratory_priest_to_medical_staff_001.png", True),
                         "laboratory_priest_to_medical_staff_002": _load(
                             "images/laboratory_priest_to_medical_staff_002.png", True),
                         "laboratory_priest_to_medical_staff_003": _load(
                             "images/laboratory_priest_to_medical_staff_003.png", True),
                         "laboratory_priest_to_medical_staff_004": _load(
                             "images/laboratory_priest_to_medical_staff_004.png", True),
                         "laboratory_priest_to_medical_staff_005": _load(
                             "images/laboratory_priest_to_medical_staff_005.png", True),
                         "laboratory_priest_to_medical_staff_006": _load(
                             "images/laboratory_priest_to_medical_staff_006.png", True),
                         "laboratory_priest_to_medical_staff_007": _load(
                             "images/laboratory_priest_to_medical_staff_007.png", True),
                         "laboratory_priest_to_medical_staff_008": _load(
                             "images/laboratory_priest_to_medical_staff_008.png", True),
                         "laboratory_priest_to_medical_staff_009": _load(
                             "images/laboratory_priest_to_medical_staff_009.png", True),
                         "laboratory_priest_to_medical_staff_010": _load(
                             "images/laboratory_priest_to_medical_staff_010.png", True),
                         "laboratory_priest_to_medical_staff_011": _load(
                             "images/laboratory_priest_to_medical_staff_011.png", True),
                         "laboratory_priest_to_medical_staff_012": _load(
                             "images/laboratory_priest_to_medical_staff_012.png", True),
                         "laboratory_priest_to_medical_staff_013": _load(
                             "images/laboratory_priest_to_medical_staff_013.png", True),
                         "laboratory_priest_to_medical_staff_014": _load(
                             "images/laboratory_priest_to_medical_staff_014.png", True),
                         "laboratory_priest_to_medical_staff_015": _load(
                             "images/laboratory_priest_to_medical_staff_015.png", True),
                         "laboratory_priest_to_medical_staff_016": _load(
                             "images/laboratory_priest_to_medical_staff_016.png", True),
                         "laboratory_priest_to_medical_staff_017": _load(
                             "images/laboratory_priest_to_medical_staff_017.png", True),
                         "laboratory_priest_to_medical_staff_018": _load(
                             "images/laboratory_priest_to_medical_staff_018.png", True),
                         "laboratory_priest_to_medical_staff_019": _load(
                             "images/laboratory_priest_to_medical_staff_019.png", True),
                         "laboratory_priest_to_medical_staff_020": _load(
                             "images/laboratory_priest_to_medical_staff_020.png", True),
                         "laboratory_priest_to_medical_staff_021": _load(
                             "images/laboratory_priest_to_medical_staff_021.png", True),
                         "laboratory_priest_to_medical_staff_022": _load(
                             "images/laboratory_priest_to_medical_staff_022.png", True),
                         "laboratory_priest_to_medical_staff_023": _load(
                             "images/laboratory_priest_to_medical_staff_023.png", True),
                         "theocratic_battle_priest_with_lucidus_001": _load(
                             "images/theocratic_battle_priest_with_lucidus_001.png", True),
                         "theocratic_battle_priest_with_lucidus_002": _load(
                             "images/theocratic_battle_priest_with_lucidus_002.png", True),
                         "theocratic_battle_priest_with_lucidus_003": _load(
                             "images/theocratic_battle_priest_with_lucidus_003.png", True),
                         "theocratic_battle_priest_with_lucidus_004": _load(
                             "images/theocratic_battle_priest_with_lucidus_004.png", True),
                         "theocratic_battle_priest_with_lucidus_005": _load(
                             "images/theocratic_battle_priest_with_lucidus_005.png", True),
                         "theocratic_battle_priest_with_lucidus_006": _load(
                             "images/theocratic_battle_priest_with_lucidus_006.png", True),

                         # SHAMAN DIALOGUE
                         "tribe_storage_shaman_with_mercenary_001": _load(
                             "images/tribe_storage_shaman_with_mercenary_001.png", True),
                         "tribe_storage_shaman_with_mercenary_002": _load(
                             "images/tribe_storage_shaman_with_mercenary_002.png", True),
                         "tribe_storage_shaman_with_mercenary_003": _load(
                             "images/tribe_storage_shaman_with_mercenary_003.png", True),
                         "tribe_storage_shaman_with_mercenary_004": _load(
                             "images/tribe_storage_shaman_with_mercenary_004.png", True),
                         "tribe_storage_shaman_with_mercenary_005": _load(
                             "images/tribe_storage_shaman_with_mercenary_005.png", True),
                         "tribe_storage_shaman_with_mercenary_006": _load(
                             "images/tribe_storage_shaman_with_mercenary_006.png", True),
                         "tribe_storage_shaman_with_mercenary_007": _load(
                             "images/tribe_storage_shaman_with_mercenary_007.png", True),
                         "tribe_storage_shaman_with_mercenary_008": _load(
                             "images/tribe_storage_shaman_with_mercenary_008.png", True),
                         "tribe_storage_shaman_with_mercenary_009": _load(
                             "images/tribe_storage_shaman_with_mercenary_009.png", True),
                         "tribe_storage_shaman_with_mercenary_010": _load(
                             "images/tribe_storage_shaman_with_mercenary_010.png", True),
                         "tribe_storage_shaman_with_mercenary_011": _load(
                             "images/tribe_storage_shaman_with_mercenary_011.png", True),
                         "tribe_storage_shaman_with_mercenary_012": _load(
                             "images/tribe_storage_shaman_with_mercenary_012.png", True),
                         "tribe_storage_shaman_with_mercenary_013": _load(
                             "images/tribe_storage_shaman_with_mercenary_013.png", True),
                         "tribe_storage_shaman_with_mercenary_014": _load(
                             "images/tribe_storage_shaman_with_mercenary_014.png", True),
                         "tribe_storage_shaman_with_mercenary_015": _load(
                             "images/tribe_storage_shaman_with_mercenary_015.png", True),
                         "tribe_storage_shaman_with_mercenary_016": _load(
                             "images/tribe_storage_shaman_with_mercenary_016.png", True),
                         "tribe_storage_shaman_with_mercenary_017": _load(
                             "images/tribe_storage_shaman_with_mercenary_017.png", True),
                         "tribe_storage_shaman_with_mercenary_018": _load(
                             "images/tribe_storage_shaman_with_mercenary_018.png", True),
                         "tribe_storage_shaman_with_mercenary_019": _load(
                             "images/tribe_storage_shaman_with_mercenary_019.png", True),
                         "tribe_storage_shaman_with_mercenary_020": _load(
                             "images/tribe_storage_shaman_with_mercenary_020.png", True),
                         "tribe_storage_shaman_with_mercenary_021": _load(
                             "images/tribe_storage_shaman_with_mercenary_021.png", True),
                         "tribe_storage_shaman_with_mercenary_022": _load(
                             "images/tribe_storage_shaman_with_mercenary_022.png", True),
                         "tribe_tunnel_shaman_with_tribe_chief_001": _load(
                             "images/tribe_tunnel_shaman_with_tribe_chief_001.png", True),
                         "tribe_tunnel_shaman_with_tribe_chief_002": _load(
                             "images/tribe_tunnel_shaman_with_tribe_chief_002.png", True),
                         "tribe_tunnel_shaman_with_tribe_chief_003": _load(
                             "images/tribe_tunnel_shaman_with_tribe_chief_003.png", True),
                         "tribe_tunnel_shaman_with_tribe_chief_004": _load(
                             "images/tribe_tunnel_shaman_with_tribe_chief_004.png", True),
                         "tribe_tunnel_shaman_with_mercenary_001": _load(
                             "images/tribe_tunnel_shaman_with_mercenary_001.png", True),
                         "tribe_tunnel_shaman_with_mercenary_002": _load(
                             "images/tribe_tunnel_shaman_with_mercenary_002.png", True),
                         "tribe_tunnel_shaman_with_mercenary_003": _load(
                             "images/tribe_tunnel_shaman_with_mercenary_003.png", True),
                         "tribe_tunnel_shaman_with_mercenary_004": _load(
                             "images/tribe_tunnel_shaman_with_mercenary_004.png", True),
                         "tribe_tunnel_shaman_with_mercenary_005": _load(
                             "images/tribe_tunnel_shaman_with_mercenary_005.png", True),
                         "tribe_tunnel_shaman_with_mercenary_006": _load(
                             "images/tribe_tunnel_shaman_with_mercenary_006.png", True),
                         "tribe_tunnel_shaman_with_mercenary_007": _load(
                             "images/tribe_tunnel_shaman_with_mercenary_007.png", True),
                         "tribe_tunnel_shaman_with_mercenary_008": _load(
                             "images/tribe_tunnel_shaman_with_mercenary_008.png", True),
                         "tribe_tunnel_shaman_with_mercenary_009": _load(
                             "images/tribe_tunnel_shaman_with_mercenary_009.png", True),
                         "tribe_tunnel_shaman_with_mercenary_010": _load(
                             "images/tribe_tunnel_shaman_with_mercenary_010.png", True),
                         "tribe_tunnel_shaman_with_mercenary_011": _load(
                             "images/tribe_tunnel_shaman_with_mercenary_011.png", True),
                         "tribe_tunnel_shaman_with_mercenary_012": _load(
                             "images/tribe_tunnel_shaman_with_mercenary_012.png", True),
                         "tribe_shaman_foresight_low_001": _load("images/tribe_shaman_foresight_low_001.png", True),
                         "tribe_shaman_foresight_low_002": _load("images/tribe_shaman_foresight_low_002.png", True),
                         "tribe_shaman_foresight_low_003": _load("images/tribe_shaman_foresight_low_003.png", True),
                         "tribe_shaman_foresight_mid_001": _load("images/tribe_shaman_foresight_mid_001.png", True),
                         "tribe_shaman_foresight_mid_002": _load("images/tribe_shaman_foresight_mid_002.png", True),
                         "tribe_shaman_foresight_mid_003": _load("images/tribe_shaman_foresight_mid_003.png", True),
                         "tribe_shaman_foresight_high_001": _load("images/tribe_shaman_foresight_high_001.png", True),
                         "tribe_shaman_foresight_high_002": _load("images/tribe_shaman_foresight_high_002.png", True),
                         "tribe_shaman_foresight_high_003": _load("images/tribe_shaman_foresight_high_003.png", True),
                         "tribe_shaman_foresight_high_004": _load("images/tribe_shaman_foresight_high_004.png", True),
                         "tribe_shaman_foresight_high_005": _load("images/tribe_shaman_foresight_high_005.png", True),
                         "zone_terror_shaman_with_mercenary_001": _load(
                             "images/zone_terror_shaman_with_mercenary_001.png", True),
                         "zone_terror_shaman_with_mercenary_002": _load(
                             "images/zone_terror_shaman_with_mercenary_002.png", True),
                         "zone_terror_shaman_with_mercenary_003": _load(
                             "images/zone_terror_shaman_with_mercenary_003.png", True),
                         "zone_terror_shaman_with_mercenary_004": _load(
                             "images/zone_terror_shaman_with_mercenary_004.png", True),
                         "zone_terror_shaman_with_mercenary_005": _load(
                             "images/zone_terror_shaman_with_mercenary_005.png", True),
                         "zone_terror_shaman_with_mercenary_006": _load(
                             "images/zone_terror_shaman_with_mercenary_006.png", True),
                         "zone_terror_shaman_with_mercenary_007": _load(
                             "images/zone_terror_shaman_with_mercenary_007.png", True),
                         "zone_terror_shaman_with_mercenary_008": _load(
                             "images/zone_terror_shaman_with_mercenary_008.png", True),
                         "zone_terror_shaman_with_mercenary_009": _load(
                             "images/zone_terror_shaman_with_mercenary_009.png", True),
                         "zone_terror_shaman_with_mercenary_010": _load(
                             "images/zone_terror_shaman_with_mercenary_010.png", True),
                         "zone_terror_shaman_with_mercenary_011": _load(
                             "images/zone_terror_shaman_with_mercenary_011.png", True),
                         "zone_terror_shaman_with_mercenary_012": _load(
                             "images/zone_terror_shaman_with_mercenary_012.png", True),
                         "zone_terror_shaman_with_mercenary_013": _load(
                             "images/zone_terror_shaman_with_mercenary_013.png", True),
                         "zone_terror_shaman_with_mercenary_014": _load(
                             "images/zone_terror_shaman_with_mercenary_014.png", True),
                         "zone_terror_shaman_with_mercenary_015": _load(
                             "images/zone_terror_shaman_with_mercenary_015.png", True),
                         "zone_terror_shaman_with_mercenary_016": _load(
                             "images/zone_terror_shaman_with_mercenary_016.png", True),
                         "zone_terror_shaman_with_mercenary_017": _load(
                             "images/zone_terror_shaman_with_mercenary_017.png", True),
                         "zone_terror_shaman_with_mercenary_018": _load(
                             "images/zone_terror_shaman_with_mercenary_018.png", True),
                         "zone_terror_shaman_with_mercenary_019": _load(
                             "images/zone_terror_shaman_with_mercenary_019.png", True),
                         "zone_terror_shaman_with_mercenary_020": _load(
                             "images/zone_terror_shaman_with_mercenary_020.png", True),
                         "zone_terror_shaman_with_mercenary_021": _load(
                             "images/zone_terror_shaman_with_mercenary_021.png", True),
                         "zone_terror_shaman_with_mercenary_022": _load(
                             "images/zone_terror_shaman_with_mercenary_022.png", True),
                         "zone_terror_shaman_with_mercenary_023": _load(
                             "images/zone_terror_shaman_with_mercenary_023.png", True),
                         "zone_terror_shaman_with_mercenary_024": _load(
                             "images/zone_terror_shaman_with_mercenary_024.png", True),
                         "zone_terror_shaman_with_mercenary_025": _load(
                             "images/zone_terror_shaman_with_mercenary_025.png", True),
                         "zone_terror_shaman_with_mercenary_026": _load(
                             "images/zone_terror_shaman_with_mercenary_026.png", True),
                         "zone_terror_shaman_with_mercenary_027": _load(
                             "images/zone_terror_shaman_with_mercenary_027.png", True),
                         "zone_terror_shaman_with_mercenary_028": _load(
                             "images/zone_terror_shaman_with_mercenary_028.png", True),
                         "zone_terror_shaman_with_mercenary_029": _load(
                             "images/zone_terror_shaman_with_mercenary_029.png", True),
                         "port_city_shaman_with_mercenary_001": _load("images/port_city_shaman_with_mercenary_001.png",
                                                                      True),
                         "port_city_shaman_with_mercenary_002": _load("images/port_city_shaman_with_mercenary_002.png",
                                                                      True),
                         "port_city_shaman_with_mercenary_003": _load("images/port_city_shaman_with_mercenary_003.png",
                                                                      True),
                         "port_city_shaman_with_mercenary_004": _load("images/port_city_shaman_with_mercenary_004.png",
                                                                      True),
                         "port_city_shaman_with_mercenary_005": _load("images/port_city_shaman_with_mercenary_005.png",
                                                                      True),
                         "port_city_shaman_with_mercenary_006": _load("images/port_city_shaman_with_mercenary_006.png",
                                                                      True),
                         "port_city_shaman_with_mercenary_007": _load("images/port_city_shaman_with_mercenary_007.png",
                                                                      True),
                         "port_city_shaman_with_mercenary_008": _load("images/port_city_shaman_with_mercenary_008.png",
                                                                      True),
                         "port_city_shaman_with_mercenary_009": _load("images/port_city_shaman_with_mercenary_009.png",
                                                                      True),
                         "port_city_shaman_with_mercenary_010": _load("images/port_city_shaman_with_mercenary_010.png",
                                                                      True),
                         "port_city_shaman_with_mercenary_011": _load("images/port_city_shaman_with_mercenary_011.png",
                                                                      True),
                         "port_city_shaman_with_mercenary_012": _load("images/port_city_shaman_with_mercenary_012.png",
                                                                      True),
                         "port_city_shaman_with_mercenary_013": _load("images/port_city_shaman_with_mercenary_013.png",
                                                                      True),
                         "port_city_shaman_with_mercenary_014": _load("images/port_city_shaman_with_mercenary_014.png",
                                                                      True),
                         "port_city_shaman_with_mercenary_015": _load("images/port_city_shaman_with_mercenary_015.png",
                                                                      True),
                         "port_city_shaman_with_mercenary_016": _load("images/port_city_shaman_with_mercenary_016.png",
                                                                      True),
                         "port_city_shaman_with_mercenary_017": _load("images/port_city_shaman_with_mercenary_017.png",
                                                                      True),
                         "cultist_island_shaman_with_mercenary_001": _load(
                             "images/cultist_island_shaman_with_mercenary_001.png", True),
                         "cultist_island_shaman_with_mercenary_002": _load(
                             "images/cultist_island_shaman_with_mercenary_002.png", True),
                         "cultist_island_shaman_with_mercenary_003": _load(
                             "images/cultist_island_shaman_with_mercenary_003.png", True),
                         "cultist_island_shaman_with_mercenary_004": _load(
                             "images/cultist_island_shaman_with_mercenary_004.png", True),
                         "cultist_island_shaman_with_mercenary_005": _load(
                             "images/cultist_island_shaman_with_mercenary_005.png", True),
                         "cultist_island_shaman_with_mercenary_006": _load(
                             "images/cultist_island_shaman_with_mercenary_006.png", True),
                         "cultist_island_shaman_with_mercenary_007": _load(
                             "images/cultist_island_shaman_with_mercenary_007.png", True),
                         "cultist_island_shaman_with_mercenary_008": _load(
                             "images/cultist_island_shaman_with_mercenary_008.png", True),
                         "cultist_island_shaman_with_mercenary_009": _load(
                             "images/cultist_island_shaman_with_mercenary_009.png", True),
                         "cultist_island_shaman_with_mercenary_010": _load(
                             "images/cultist_island_shaman_with_mercenary_010.png", True),
                         "cultist_island_shaman_with_mercenary_011": _load(
                             "images/cultist_island_shaman_with_mercenary_011.png", True),
                         "cultist_island_shaman_with_mercenary_012": _load(
                             "images/cultist_island_shaman_with_mercenary_012.png", True),
                         "cultist_island_shaman_with_mercenary_013": _load(
                             "images/cultist_island_shaman_with_mercenary_013.png", True),
                         "cultist_island_shaman_with_mercenary_014": _load(
                             "images/cultist_island_shaman_with_mercenary_014.png", True),
                         "cultist_island_shaman_with_mercenary_015": _load(
                             "images/cultist_island_shaman_with_mercenary_015.png", True),
                         "cultist_island_shaman_with_mercenary_016": _load(
                             "images/cultist_island_shaman_with_mercenary_016.png", True),
                         "cultist_island_shaman_with_mercenary_017": _load(
                             "images/cultist_island_shaman_with_mercenary_017.png", True),
                         "cultist_island_shaman_with_mercenary_018": _load(
                             "images/cultist_island_shaman_with_mercenary_018.png", True),
                         "cultist_island_shaman_with_mercenary_019": _load(
                             "images/cultist_island_shaman_with_mercenary_019.png", True),
                         "cultist_island_shaman_with_mercenary_020": _load(
                             "images/cultist_island_shaman_with_mercenary_020.png", True),
                         "outskirts_village_shaman_with_village_chief_001": _load(
                             "images/outskirts_village_shaman_with_village_chief_001.png", True),
                         "outskirts_village_shaman_with_village_chief_002": _load(
                             "images/outskirts_village_shaman_with_village_chief_002.png", True),
                         "outskirts_village_shaman_with_village_chief_003": _load(
                             "images/outskirts_village_shaman_with_village_chief_003.png", True),
                         "outskirts_village_shaman_with_village_chief_004": _load(
                             "images/outskirts_village_shaman_with_village_chief_004.png", True),
                         "outskirts_village_shaman_with_village_chief_005": _load(
                             "images/outskirts_village_shaman_with_village_chief_005.png", True),
                         "outskirts_village_shaman_with_villager_001": _load(
                             "images/outskirts_village_shaman_with_villager_001.png", True),
                         "outskirts_village_shaman_with_villager_002": _load(
                             "images/outskirts_village_shaman_with_villager_002.png", True),
                         "outskirts_village_shaman_with_villager_003": _load(
                             "images/outskirts_village_shaman_with_villager_003.png", True),
                         "outskirts_village_shaman_with_villager_004": _load(
                             "images/outskirts_village_shaman_with_villager_004.png", True),
                         "outskirts_village_shaman_with_villager_005": _load(
                             "images/outskirts_village_shaman_with_villager_005.png", True),
                         "outskirts_village_shaman_with_travelling_bard_001": _load(
                             "images/outskirts_village_shaman_with_travelling_bard_001.png", True),
                         "outskirts_village_shaman_with_travelling_bard_002": _load(
                             "images/outskirts_village_shaman_with_travelling_bard_002.png", True),
                         "outskirts_village_shaman_with_travelling_bard_003": _load(
                             "images/outskirts_village_shaman_with_travelling_bard_003.png", True),
                         "outskirts_village_shaman_with_travelling_bard_004": _load(
                             "images/outskirts_village_shaman_with_travelling_bard_004.png", True),
                         "outskirts_village_shaman_with_travelling_bard_005": _load(
                             "images/outskirts_village_shaman_with_travelling_bard_005.png", True),
                         "tribe_destroyed_shaman_to_herself_001": _load(
                             "images/tribe_destroyed_shaman_to_herself_001.png", True),
                         "tribe_destroyed_shaman_to_herself_002": _load(
                             "images/tribe_destroyed_shaman_to_herself_002.png", True),
                         "tribe_destroyed_shaman_to_herself_003": _load(
                             "images/tribe_destroyed_shaman_to_herself_003.png", True),
                         "tribe_destroyed_shaman_to_herself_004": _load(
                             "images/tribe_destroyed_shaman_to_herself_004.png", True),
                         "tribe_destroyed_shaman_to_herself_005": _load(
                             "images/tribe_destroyed_shaman_to_herself_005.png", True),
                         "tribe_destroyed_shaman_to_herself_006": _load(
                             "images/tribe_destroyed_shaman_to_herself_006.png", True),
                         "tribe_destroyed_shaman_to_herself_007": _load(
                             "images/tribe_destroyed_shaman_to_herself_007.png", True),
                         "tribe_destroyed_shaman_to_herself_008": _load(
                             "images/tribe_destroyed_shaman_to_herself_008.png", True),
                         "tribe_destroyed_shaman_to_herself_009": _load(
                             "images/tribe_destroyed_shaman_to_herself_009.png", True),

                         # MERCHANT DIALOGUE
                         "port_city_merchant_with_guild_master_001": _load(
                             "images/port_city_merchant_with_guild_master_001.png", True),
                         "port_city_merchant_with_guild_master_002": _load(
                             "images/port_city_merchant_with_guild_master_002.png", True),
                         "port_city_merchant_with_guild_master_003": _load(
                             "images/port_city_merchant_with_guild_master_003.png", True),
                         "port_city_merchant_with_guild_master_004": _load(
                             "images/port_city_merchant_with_guild_master_004.png", True),
                         "port_city_merchant_with_guild_master_005": _load(
                             "images/port_city_merchant_with_guild_master_005.png", True),
                         "port_city_merchant_with_guild_master_006": _load(
                             "images/port_city_merchant_with_guild_master_006.png", True),
                         "port_city_merchant_with_guild_master_007": _load(
                             "images/port_city_merchant_with_guild_master_007.png", True),
                         "port_city_merchant_with_guild_master_008": _load(
                             "images/port_city_merchant_with_guild_master_008.png", True),
                         "port_city_merchant_with_guild_master_009": _load(
                             "images/port_city_merchant_with_guild_master_009.png", True),
                         "port_city_merchant_with_guild_master_010": _load(
                             "images/port_city_merchant_with_guild_master_010.png", True),
                         "port_city_merchant_with_guild_master_011": _load(
                             "images/port_city_merchant_with_guild_master_011.png", True),
                         "port_city_merchant_with_guild_master_012": _load(
                             "images/port_city_merchant_with_guild_master_012.png", True),
                         "port_city_merchant_with_guild_master_013": _load(
                             "images/port_city_merchant_with_guild_master_013.png", True),
                         "port_city_merchant_with_guild_master_014": _load(
                             "images/port_city_merchant_with_guild_master_014.png", True),
                         "port_city_merchant_with_guild_master_015": _load(
                             "images/port_city_merchant_with_guild_master_015.png", True),
                         "port_city_merchant_with_guild_master_016": _load(
                             "images/port_city_merchant_with_guild_master_016.png", True),
                         "port_city_merchant_with_guild_master_017": _load(
                             "images/port_city_merchant_with_guild_master_017.png", True),
                         "port_city_merchant_with_guild_master_018": _load(
                             "images/port_city_merchant_with_guild_master_018.png", True),
                         "port_city_merchant_with_guild_master_019": _load(
                             "images/port_city_merchant_with_guild_master_019.png", True),
                         "port_city_merchant_with_guild_master_020": _load(
                             "images/port_city_merchant_with_guild_master_020.png", True),
                         "port_city_merchant_with_guild_master_021": _load(
                             "images/port_city_merchant_with_guild_master_021.png", True),
                         "port_city_merchant_with_guild_master_022": _load(
                             "images/port_city_merchant_with_guild_master_022.png", True),
                         "port_city_merchant_with_guild_master_023": _load(
                             "images/port_city_merchant_with_guild_master_023.png", True),
                         "port_city_merchant_with_guild_master_024": _load(
                             "images/port_city_merchant_with_guild_master_024.png", True),
                         "port_city_merchant_with_guild_master_025": _load(
                             "images/port_city_merchant_with_guild_master_025.png", True),
                         "port_city_merchant_with_guild_master_026": _load(
                             "images/port_city_merchant_with_guild_master_026.png", True),
                         "port_city_merchant_with_guild_master_027": _load(
                             "images/port_city_merchant_with_guild_master_027.png", True),
                         "port_city_merchant_with_tavern_keeper_001": _load(
                             "images/port_city_merchant_with_tavern_keeper_001.png", True),
                         "port_city_merchant_with_tavern_keeper_002": _load(
                             "images/port_city_merchant_with_tavern_keeper_002.png", True),
                         "port_city_merchant_with_tavern_keeper_003": _load(
                             "images/port_city_merchant_with_tavern_keeper_003.png", True),
                         "port_city_merchant_with_tavern_keeper_004": _load(
                             "images/port_city_merchant_with_tavern_keeper_004.png", True),
                         "port_city_merchant_with_tavern_keeper_005": _load(
                             "images/port_city_merchant_with_tavern_keeper_005.png", True),
                         "port_city_merchant_with_tavern_keeper_006": _load(
                             "images/port_city_merchant_with_tavern_keeper_006.png", True),
                         "port_city_merchant_with_tavern_keeper_007": _load(
                             "images/port_city_merchant_with_tavern_keeper_007.png", True),
                         "port_city_merchant_with_tavern_keeper_008": _load(
                             "images/port_city_merchant_with_tavern_keeper_008.png", True),
                         "port_city_merchant_with_tavern_keeper_009": _load(
                             "images/port_city_merchant_with_tavern_keeper_009.png", True),
                         "port_city_merchant_with_tavern_keeper_010": _load(
                             "images/port_city_merchant_with_tavern_keeper_010.png", True),
                         "port_city_merchant_decision_node_001": _load(
                             "images/port_city_merchant_decision_node_001.png", True),
                         "port_city_merchant_decision_node_002": _load(
                             "images/port_city_merchant_decision_node_002.png", True),
                         "port_city_merchant_decision_node_003": _load(
                             "images/port_city_merchant_decision_node_003.png", True),
                         "port_city_merchant_response_node_001": _load(
                             "images/port_city_merchant_response_node_001.png", True),
                         "port_city_merchant_response_node_002": _load(
                             "images/port_city_merchant_response_node_002.png", True),
                         "port_city_merchant_response_node_003": _load(
                             "images/port_city_merchant_response_node_003.png", True),
                         "walled_merchant_with_blacksmith_001": _load("images/walled_merchant_with_blacksmith_001.png",
                                                                      True),
                         "walled_merchant_with_blacksmith_002": _load("images/walled_merchant_with_blacksmith_002.png",
                                                                      True),
                         "walled_merchant_with_blacksmith_003": _load("images/walled_merchant_with_blacksmith_003.png",
                                                                      True),
                         "walled_merchant_with_blacksmith_004": _load("images/walled_merchant_with_blacksmith_004.png",
                                                                      True),
                         "walled_merchant_with_blacksmith_005": _load("images/walled_merchant_with_blacksmith_005.png",
                                                                      True),
                         "walled_merchant_with_blacksmith_006": _load("images/walled_merchant_with_blacksmith_006.png",
                                                                      True),
                         "walled_merchant_with_blacksmith_007": _load("images/walled_merchant_with_blacksmith_007.png",
                                                                      True),
                         "walled_merchant_with_blacksmith_008": _load("images/walled_merchant_with_blacksmith_008.png",
                                                                      True),
                         "walled_merchant_with_blacksmith_009": _load("images/walled_merchant_with_blacksmith_009.png",
                                                                      True),
                         "walled_merchant_with_blacksmith_010": _load("images/walled_merchant_with_blacksmith_010.png",
                                                                      True),
                         "walled_merchant_with_blacksmith_011": _load("images/walled_merchant_with_blacksmith_011.png",
                                                                      True),
                         "outskirts_village_merchant_with_village_chief_001": _load(
                             "images/outskirts_village_merchant_with_village_chief_001.png", True),
                         "outskirts_village_merchant_with_village_chief_002": _load(
                             "images/outskirts_village_merchant_with_village_chief_002.png", True),
                         "outskirts_village_merchant_with_village_chief_003": _load(
                             "images/outskirts_village_merchant_with_village_chief_003.png", True),
                         "outskirts_village_merchant_with_village_chief_004": _load(
                             "images/outskirts_village_merchant_with_village_chief_004.png", True),
                         "outskirts_village_merchant_with_village_chief_005": _load(
                             "images/outskirts_village_merchant_with_village_chief_005.png", True),
                         "outskirts_village_merchant_with_village_chief_006": _load(
                             "images/outskirts_village_merchant_with_village_chief_006.png", True),
                         "outskirts_village_merchant_with_village_chief_007": _load(
                             "images/outskirts_village_merchant_with_village_chief_007.png", True),
                         "zone_terrors_merchant_to_himself_001": _load(
                             "images/zone_terrors_merchant_to_himself_001.png", True),
                         "zone_terrors_merchant_to_himself_002": _load(
                             "images/zone_terrors_merchant_to_himself_002.png", True),
                         "port_city_merchant_with_harbor_captain_001": _load(
                             "images/port_city_merchant_with_harbor_captain_001.png", True),
                         "port_city_merchant_with_harbor_captain_002": _load(
                             "images/port_city_merchant_with_harbor_captain_002.png", True),
                         "port_city_merchant_with_harbor_captain_003": _load(
                             "images/port_city_merchant_with_harbor_captain_003.png", True),
                         "port_city_merchant_with_harbor_captain_004": _load(
                             "images/port_city_merchant_with_harbor_captain_004.png", True),
                         "home_village_merchant_to_himself_001": _load(
                             "images/home_village_merchant_to_himself_001.png", True),
                         "home_village_merchant_to_himself_002": _load(
                             "images/home_village_merchant_to_himself_002.png", True),
                         "home_village_merchant_to_himself_003": _load(
                             "images/home_village_merchant_to_himself_003.png", True),
                         "home_village_merchant_to_himself_004": _load(
                             "images/home_village_merchant_to_himself_004.png", True),
                         "port_outpost_merchant_with_church_spy_001": _load(
                             "images/port_outpost_mechant_with_church_spy_001.png", True),
                         "port_outpost_merchant_with_church_spy_002": _load(
                             "images/port_outpost_mechant_with_church_spy_002.png", True),
                         "port_outpost_merchant_with_church_spy_003": _load(
                             "images/port_outpost_mechant_with_church_spy_003.png", True),
                         "port_outpost_merchant_with_church_spy_004": _load(
                             "images/port_outpost_mechant_with_church_spy_004.png", True),
                         "port_outpost_merchant_with_church_spy_005": _load(
                             "images/port_outpost_mechant_with_church_spy_005.png", True),
                         "port_outpost_merchant_with_church_spy_006": _load(
                             "images/port_outpost_mechant_with_church_spy_006.png", True),
                         "port_outpost_merchant_with_church_spy_007": _load(
                             "images/port_outpost_mechant_with_church_spy_007.png", True),
                         "port_outpost_merchant_with_church_spy_008": _load(
                             "images/port_outpost_mechant_with_church_spy_008.png", True),
                         "port_outpost_merchant_with_church_spy_009": _load(
                             "images/port_outpost_mechant_with_church_spy_009.png", True),
                         "port_outpost_merchant_with_church_spy_010": _load(
                             "images/port_outpost_mechant_with_church_spy_010.png", True),
                         "port_outpost_merchant_with_church_spy_011": _load(
                             "images/port_outpost_mechant_with_church_spy_011.png", True),
                         "port_outpost_merchant_with_church_spy_012": _load(
                             "images/port_outpost_mechant_with_church_spy_012.png", True),
                         "port_outpost_merchant_with_church_spy_013": _load(
                             "images/port_outpost_mechant_with_church_spy_013.png", True),
                         "port_outpost_merchant_with_church_spy_014": _load(
                             "images/port_outpost_mechant_with_church_spy_014.png", True),
                         "port_outpost_merchant_with_church_spy_015": _load(
                             "images/port_outpost_mechant_with_church_spy_015.png", True),
                         "port_outpost_merchant_with_church_spy_016": _load(
                             "images/port_outpost_mechant_with_church_spy_016.png", True),
                         "port_outpost_merchant_with_church_spy_017": _load(
                             "images/port_outpost_mechant_with_church_spy_017.png", True),
                         "port_outpost_merchant_with_church_spy_018": _load(
                             "images/port_outpost_mechant_with_church_spy_018.png", True),
                         "port_city_merchant_with_captain_and_spy_001": _load(
                             "images/port_city_merchant_with_captain_and_spy_001.png", True),
                         "port_city_merchant_with_captain_and_spy_002": _load(
                             "images/port_city_merchant_with_captain_and_spy_002.png", True),
                         "port_city_merchant_with_captain_and_spy_003": _load(
                             "images/port_city_merchant_with_captain_and_spy_003.png", True),
                         "port_city_merchant_with_captain_and_spy_004": _load(
                             "images/port_city_merchant_with_captain_and_spy_004.png", True),
                         "port_city_merchant_with_captain_and_spy_005": _load(
                             "images/port_city_merchant_with_captain_and_spy_005.png", True),
                         "port_city_merchant_with_captain_and_spy_006": _load(
                             "images/port_city_merchant_with_captain_and_spy_006.png", True),
                         "port_city_merchant_with_captain_and_spy_007": _load(
                             "images/port_city_merchant_with_captain_and_spy_007.png", True),
                         "port_city_merchant_with_captain_and_spy_008": _load(
                             "images/port_city_merchant_with_captain_and_spy_008.png", True),
                         "port_city_merchant_with_captain_and_spy_009": _load(
                             "images/port_city_merchant_with_captain_and_spy_009.png", True),
                         "port_city_merchant_with_captain_and_spy_010": _load(
                             "images/port_city_merchant_with_captain_and_spy_010.png", True),
                         "port_city_merchant_with_captain_and_spy_011": _load(
                             "images/port_city_merchant_with_captain_and_spy_011.png", True),
                         "port_city_merchant_with_captain_and_spy_012": _load(
                             "images/port_city_merchant_with_captain_and_spy_012.png", True),
                         "port_city_merchant_with_captain_and_spy_013": _load(
                             "images/port_city_merchant_with_captain_and_spy_013.png", True),
                         "port_city_merchant_with_captain_and_spy_014": _load(
                             "images/port_city_merchant_with_captain_and_spy_014.png", True),
                         "port_city_merchant_with_captain_and_spy_015": _load(
                             "images/port_city_merchant_with_captain_and_spy_015.png", True),
                         "port_city_merchant_with_captain_and_spy_016": _load(
                             "images/port_city_merchant_with_captain_and_spy_016.png", True),
                         "port_city_merchant_with_captain_and_spy_017": _load(
                             "images/port_city_merchant_with_captain_and_spy_017.png", True),
                         "port_city_merchant_with_captain_and_spy_018": _load(
                             "images/port_city_merchant_with_captain_and_spy_018.png", True),
                         "port_city_merchant_with_captain_and_spy_019": _load(
                             "images/port_city_merchant_with_captain_and_spy_019.png", True),
                         "port_city_merchant_with_captain_and_spy_020": _load(
                             "images/port_city_merchant_with_captain_and_spy_020.png", True),
                         "port_city_merchant_with_mercenary_001": _load(
                             "images/port_city_merchant_with_mercenary_001.png", True),
                         "port_city_merchant_with_mercenary_002": _load(
                             "images/port_city_merchant_with_mercenary_002.png", True),
                         "port_city_merchant_with_mercenary_003": _load(
                             "images/port_city_merchant_with_mercenary_003.png", True),
                         "port_city_merchant_with_mercenary_004": _load(
                             "images/port_city_merchant_with_mercenary_004.png", True),
                         "port_city_merchant_with_mercenary_005": _load(
                             "images/port_city_merchant_with_mercenary_005.png", True),
                         "port_city_merchant_with_mercenary_006": _load(
                             "images/port_city_merchant_with_mercenary_006.png", True),
                         "port_city_merchant_with_mercenary_007": _load(
                             "images/port_city_merchant_with_mercenary_007.png", True),
                         "port_city_merchant_with_mercenary_008": _load(
                             "images/port_city_merchant_with_mercenary_008.png", True),
                         "port_city_merchant_with_mercenary_009": _load(
                             "images/port_city_merchant_with_mercenary_009.png", True),
                         "port_city_merchant_with_mercenary_010": _load(
                             "images/port_city_merchant_with_mercenary_010.png", True),
                         "port_city_merchant_with_mercenary_011": _load(
                             "images/port_city_merchant_with_mercenary_011.png", True),
                         "port_city_merchant_with_mercenary_012": _load(
                             "images/port_city_merchant_with_mercenary_012.png", True),
                         "port_city_merchant_with_mercenary_013": _load(
                             "images/port_city_merchant_with_mercenary_013.png", True),
                         "port_city_merchant_with_mercenary_014": _load(
                             "images/port_city_merchant_with_mercenary_014.png", True),
                         "port_city_merchant_with_mercenary_015": _load(
                             "images/port_city_merchant_with_mercenary_015.png", True),
                         "port_city_merchant_with_mercenary_016": _load(
                             "images/port_city_merchant_with_mercenary_016.png", True),
                         "port_city_merchant_with_mercenary_017": _load(
                             "images/port_city_merchant_with_mercenary_017.png", True),
                         "port_city_merchant_with_mercenary_018": _load(
                             "images/port_city_merchant_with_mercenary_018.png", True),
                         "port_city_merchant_with_mercenary_019": _load(
                             "images/port_city_merchant_with_mercenary_019.png", True),
                         "port_city_merchant_with_mercenary_020": _load(
                             "images/port_city_merchant_with_mercenary_020.png", True),
                         "theocratic_merchant_with_archive_001": _load(
                             "images/theocratic_merchant_with_archive_001.png", True),
                         "theocratic_merchant_with_archive_002": _load(
                             "images/theocratic_merchant_with_archive_002.png", True),
                         "theocratic_merchant_with_archive_003": _load(
                             "images/theocratic_merchant_with_archive_003.png", True),
                         "theocratic_merchant_with_archive_004": _load(
                             "images/theocratic_merchant_with_archive_004.png", True),
                         "theocratic_merchant_with_archive_005": _load(
                             "images/theocratic_merchant_with_archive_005.png", True),
                         "theocratic_merchant_with_archive_006": _load(
                             "images/theocratic_merchant_with_archive_006.png", True),
                         "theocratic_merchant_with_archive_007": _load(
                             "images/theocratic_merchant_with_archive_007.png", True),
                         "theocratic_merchant_with_archive_008": _load(
                             "images/theocratic_merchant_with_archive_008.png", True),
                         "theocratic_merchant_with_archive_009": _load(
                             "images/theocratic_merchant_with_archive_009.png", True),
                         "theocratic_merchant_with_church_knight_001": _load(
                             "images/theocratic_merchant_with_church_knight_001.png", True),
                         "theocratic_merchant_with_church_knight_002": _load(
                             "images/theocratic_merchant_with_church_knight_002.png", True),
                         "theocratic_merchant_with_church_knight_003": _load(
                             "images/theocratic_merchant_with_church_knight_003.png", True),
                         "theocratic_merchant_with_church_knight_004": _load(
                             "images/theocratic_merchant_with_church_knight_004.png", True),
                         "theocratic_merchant_with_church_knight_005": _load(
                             "images/theocratic_merchant_with_church_knight_005.png", True),
                         "theocratic_merchant_with_church_knight_006": _load(
                             "images/theocratic_merchant_with_church_knight_006.png", True),
                         "theocratic_merchant_with_church_knight_007": _load(
                             "images/theocratic_merchant_with_church_knight_007.png", True),
                         "theocratic_merchant_with_church_knight_008": _load(
                             "images/theocratic_merchant_with_church_knight_008.png", True),
                         "theocratic_merchant_with_church_knight_009": _load(
                             "images/theocratic_merchant_with_church_knight_009.png", True),
                         "theocratic_merchant_with_church_knight_010": _load(
                             "images/theocratic_merchant_with_church_knight_010.png", True),
                         "theocratic_merchant_with_church_knight_011": _load(
                             "images/theocratic_merchant_with_church_knight_011.png", True),
                         "theocratic_merchant_with_church_knight_012": _load(
                             "images/theocratic_merchant_with_church_knight_012.png", True),
                         "theocratic_merchant_with_church_knight_013": _load(
                             "images/theocratic_merchant_with_church_knight_013.png", True),
                         "theocratic_merchant_with_church_knight_014": _load(
                             "images/theocratic_merchant_with_church_knight_014.png", True),
                         "theocratic_merchant_with_church_knight_015": _load(
                             "images/theocratic_merchant_with_church_knight_015.png", True),
                         "theocratic_merchant_with_priest_001": _load("images/theocratic_merchant_with_priest_001.png",
                                                                      True),
                         "theocratic_merchant_with_priest_002": _load("images/theocratic_merchant_with_priest_002.png",
                                                                      True),
                         "theocratic_merchant_with_priest_003": _load("images/theocratic_merchant_with_priest_003.png",
                                                                      True),
                         "theocratic_merchant_with_priest_004": _load("images/theocratic_merchant_with_priest_004.png",
                                                                      True),
                         "theocratic_merchant_with_priest_005": _load("images/theocratic_merchant_with_priest_005.png",
                                                                      True),
                         "theocratic_merchant_with_priest_006": _load("images/theocratic_merchant_with_priest_006.png",
                                                                      True),
                         "theocratic_merchant_with_priest_007": _load("images/theocratic_merchant_with_priest_007.png",
                                                                      True),
                         "theocratic_merchant_with_priest_008": _load("images/theocratic_merchant_with_priest_008.png",
                                                                      True),
                         "theocratic_merchant_with_priest_009": _load("images/theocratic_merchant_with_priest_009.png",
                                                                      True),
                         "theocratic_merchant_with_priest_010": _load("images/theocratic_merchant_with_priest_010.png",
                                                                      True),
                         "theocratic_merchant_with_priest_011": _load("images/theocratic_merchant_with_priest_011.png",
                                                                      True),
                         "theocratic_merchant_with_priest_012": _load("images/theocratic_merchant_with_priest_012.png",
                                                                      True),
                         "theocratic_merchant_with_priest_013": _load("images/theocratic_merchant_with_priest_013.png",
                                                                      True),
                         "theocratic_merchant_with_priest_014": _load("images/theocratic_merchant_with_priest_014.png",
                                                                      True),
                         "theocratic_merchant_with_priest_015": _load("images/theocratic_merchant_with_priest_015.png",
                                                                      True),
                         "theocratic_merchant_with_priest_016": _load("images/theocratic_merchant_with_priest_016.png",
                                                                      True),
                         "theocratic_merchant_with_priest_017": _load("images/theocratic_merchant_with_priest_017.png",
                                                                      True),
                         "theocratic_merchant_with_priest_018": _load("images/theocratic_merchant_with_priest_018.png",
                                                                      True),
                         "theocratic_merchant_with_priest_019": _load("images/theocratic_merchant_with_priest_019.png",
                                                                      True),
                         "theocratic_merchant_with_priest_020": _load("images/theocratic_merchant_with_priest_020.png",
                                                                      True),
                         "theocratic_merchant_with_priest_021": _load("images/theocratic_merchant_with_priest_021.png",
                                                                      True),
                         "theocratic_merchant_with_priest_022": _load("images/theocratic_merchant_with_priest_022.png",
                                                                      True),
                         "theocratic_merchant_with_priest_023": _load("images/theocratic_merchant_with_priest_023.png",
                                                                      True),
                         "theocratic_merchant_with_priest_024": _load("images/theocratic_merchant_with_priest_024.png",
                                                                      True),
                         "theocratic_merchant_with_priest_025": _load("images/theocratic_merchant_with_priest_025.png",
                                                                      True),
                         "theocratic_merchant_with_priest_026": _load("images/theocratic_merchant_with_priest_026.png",
                                                                      True),
                         "theocratic_merchant_with_priest_027": _load("images/theocratic_merchant_with_priest_027.png",
                                                                      True),
                         "theocratic_merchant_with_priest_028": _load("images/theocratic_merchant_with_priest_028.png",
                                                                      True),
                         "theocratic_merchant_with_priest_029": _load("images/theocratic_merchant_with_priest_029.png",
                                                                      True),
                         "theocratic_merchant_with_priest_030": _load("images/theocratic_merchant_with_priest_030.png",
                                                                      True),
                         "theocratic_merchant_with_priest_031": _load("images/theocratic_merchant_with_priest_031.png",
                                                                      True),
                         "theocratic_merchant_with_priest_032": _load("images/theocratic_merchant_with_priest_032.png",
                                                                      True),
                         "theocratic_merchant_with_priest_033": _load("images/theocratic_merchant_with_priest_033.png",
                                                                      True),
                         "theocratic_merchant_with_priest_034": _load("images/theocratic_merchant_with_priest_034.png",
                                                                      True),
                         "theocratic_merchant_with_priest_035": _load("images/theocratic_merchant_with_priest_035.png",
                                                                      True),
                         "theocratic_merchant_with_priest_036": _load("images/theocratic_merchant_with_priest_036.png",
                                                                      True),
                         "theocratic_merchant_with_priest_037": _load("images/theocratic_merchant_with_priest_037.png",
                                                                      True),
                         "theocratic_merchant_with_priest_038": _load("images/theocratic_merchant_with_priest_038.png",
                                                                      True),
                         "theocratic_merchant_with_priest_039": _load("images/theocratic_merchant_with_priest_039.png",
                                                                      True),
                         "theocratic_merchant_with_priest_040": _load("images/theocratic_merchant_with_priest_040.png",
                                                                      True),
                         "theocratic_merchant_with_priest_041": _load("images/theocratic_merchant_with_priest_041.png",
                                                                      True),
                         "theocratic_merchant_with_priest_042": _load("images/theocratic_merchant_with_priest_042.png",
                                                                      True),
                         "theocratic_merchant_with_priest_043": _load("images/theocratic_merchant_with_priest_043.png",
                                                                      True),
                         "materials_special_small_caligo_fragment_tribe": _load(
                             "images/materials_special_small_caligo_fragment_tribe.png", True),
                         "materials_special_small_caligo_fragment_port": _load(
                             "images/materials_special_small_caligo_fragment_port.png", True),
                         "materials_special_big_caligo_fragmrnt": _load(
                             "images/materials_special_big_caligo_fragmrnt.png", True),
                         "weapon_1handed_short_sword": _load("images/weapon_1handed_short_sword.png", True),
                         "weapon_1handed_cleaver": _load("images/weapon_1handed_cleaver.png", True),
                         "weapon_1handed_knife": _load("images/weapon_1handed_knife.png", True),
                         "materials_sheet_ancient_paper": _load("images/materials_sheet_ancient_paper.png", True),
                         "armour_headware_iron_mask": _load("images/armour_headware_iron_mask.png", True),
                         "armour_body_armour_dark_priests_robe": _load(
                             "images/armour_body_armour_dark_priests_robe.png", True),
                         "armour_body_armour_priests_robe": _load("images/armour_body_armour_priests_robe.png", True),
                         "armour_headware_plate_helmet": _load("images/armour_headware_plate_helmet.png", True),
                         "armour_headware_padded_cap": _load("images/armour_headware_padded_cap.png", True),
                         "armour_body_armour_iron_cuirass": _load("images/armour_body_armour_iron_cuirass.png", True),
                         "armour_body_armour_loincloth": _load("images/armour_body_armour_loincloth.png", True),
                         "armour_accessories_red_scarf": _load("images/armour_accessories_red_scarf.png", True),
                         "armour_headware_iron_helmet": _load("images/armour_headware_iron_helmet.png", True),
                         "armour_headware_guard_bascinet": _load("images/armour_headware_guard_bascinet.png", True),
                         "armour_headware_guard_coif": _load("images/armour_headware_guard_coif.png", True),
                         "armour_headware_chainmail_hood": _load("images/armour_headware_chainmail_hood.png", True),
                         "armour_body_armour_black_dress": _load("images/armour_body_armour_black_dress.png", True),
                         "armour_body_armour_trench_coat": _load("images/armour_body_armour_trench_coat.png", True),
                         "weapon_1handed_corsairs_saber": _load("images/weapon_1handed_corsairs_saber.png", True),
                         "weapon_1handed_cloth_hood": _load("images/weapon_1handed_cloth_hood.png", True),
                         "armour_body_armour_leather_coat": _load("images/armour_body_armour_leather_coat.png", True),
                         "armour_body_armour_leather_jvest": _load("images/armour_body_armour_leather_jvest.png", True),
                         "armour_body_armour_plated_mail": _load("images/armour_body_armour_plated_mail.png", True),
                         "armour_shield_scutum": _load("images/armour_shield_scutum.png", True),
                         "weapon_longrange_musket": _load("images/weapon_longrange_musket.png", True),
                         "weapon_2handed_spear": _load("images/weapon_2handed_spear.png", True),
                         "armour_body_armour_hard_leather_armor": _load(
                             "images/armour_body_armour_hard_leather_armor.png", True),
                         "armour_body_armour_iron_plate": _load("images/armour_body_armour_iron_plate.png", True),
                         "weapon_1handed_stiletto": _load("images/weapon_1handed_stiletto.png", True),
                         "armour_armwear_arm_guard": _load("images/armour_armwear_arm_guard.png", True),
                         "weapon_1handed_iron_axe": _load("images/weapon_1handed_iron_axe.png", True),
                         "weapon_longrange_short_bow": _load("images/weapon_longrange_short_bow.png", True),
                         "materials_scrap_leather_scraps": _load("images/materials_scrap_leather_scraps.png", True),
                         "materials_skill_book_of_rapid_fire": _load("images/materials_skill_book_of_rapid_fire.png",
                                                                     True),
                         "materials_skill_book_of_instincts": _load("images/materials_skill_book_of_instincts.png",
                                                                    True),
                         "armour_accessories_swift_boots": _load("images/armour_accessories_swift_boots.png", True),
                         "weapon_longrange_heavy_crossbow": _load("images/weapon_longrange_heavy_crossbow.png", True),
                         "weapon_longrange_longbow": _load("images/weapon_longrange_longbow.png", True),
                         "weapon_2handed_maul": _load("images/weapon_2handed_maul.png", True),
                         "weapon_2handed_claymore": _load("images/weapon_2handed_claymore.png", True),
                         "weapon_1handed_scimitar": _load("images/weapon_1handed_scimitar.png", True),
                         "weapon_1handed_improvised_shiv": _load("images/weapon_1handed_improvised_shiv.png", True),
                         "weapon_1handed_steel_hammer": _load("images/weapon_1handed_steel_hammer.png", True),
                         "material_toy_black_dressed_doll": _load("images/material_toy_black_dressed_doll.png", True),
                         "weapon_1handed_dirk": _load("images/weapon_1handed_dirk.png", True),
                         "materials_plank_wooden_plank": _load("images/materials_plank_wooden_plank.png", True),
                         "weapon_1handed_dagger": _load("images/weapon_1handed_dagger.png", True),
                         "materials_component_silver_wire": _load("images/materials_component_silver_wire.png", True),
                         "armour_accessories_red_amulet": _load("images/armour_accessories_red_amulet.png", True),
                         "armour_accessories_blue_amulet": _load("images/armour_accessories_blue_amulet.png", True),
                         "materials_component_stick": _load("images/materials_component_stick.png", True),
                         "armour_accessories_ring": _load("images/armour_accessories_ring.png", True),
                         "materials_skill_book_of_marksmanship": _load(
                             "images/materials_skill_book_of_marksmanship.png", True),
                         "materials_skill_book_of_stars": _load("images/materials_skill_book_of_stars.png", True),
                         "materials_skill_book_of_crafsmanship": _load(
                             "images/materials_skill_book_of_crafsmanship.png", True),
                         "materials_skill_book_of_agility": _load("images/materials_skill_book_of_agility.png", True),
                         "materials_skill_book_of_healing": _load("images/materials_skill_book_of_healing.png", True),
                         "materials_skill_book_of_the_secrets": _load("images/materials_skill_book_of_the_secrets.png",
                                                                      True),
                         "materials_save_book_of_enlightenment": _load(
                             "images/materials_save_book_of_enlightenment.png", True),
                         "materials_skill_book_of_cowardice_i": _load("images/materials_skill_book_of_cowardice_i.png",
                                                                      True),
                         "materials_skill_book_of_cowardice_ii": _load(
                             "images/materials_skill_book_of_cowardice_ii.png", True),
                         "materials_skill_book_of_pestilence_i": _load(
                             "images/materials_skill_book_of_pestilence_i.png", True),
                         "materials_skill_book_of_pestilence_ii": _load(
                             "images/materials_skill_book_of_pestilence_ii.png", True),
                         "materials_skill_book_of_pestilence_iii": _load(
                             "images/materials_skill_book_of_pestilence_iii.png", True),
                         "materials_skill_book_of_pestilence_iv": _load(
                             "images/materials_skill_book_of_pestilence_iv.png", True),
                         "materials_skill_book_of_pestilence_v": _load(
                             "images/materials_skill_book_of_pestilence_v.png", True),
                         "materials_skill_book_of_pestilence_vi": _load(
                             "images/materials_skill_book_of_pestilence_vi.png", True),
                         "materials_skill_book_of_pestilence_vii": _load(
                             "images/materials_skill_book_of_pestilence_vii.png", True),
                         "materials_skill_book_of_pestilence_viii": _load(
                             "images/materials_skill_book_of_pestilence_viii.png", True),
                         "materials_skill_book_of_trade_i": _load("images/materials_skill_book_of_trade_i.png", True),
                         "materials_skill_book_of_trade_ii": _load("images/materials_skill_book_of_trade_ii.png", True),
                         "materials_skill_book_of_trade_iii": _load("images/materials_skill_book_of_trade_iii.png",
                                                                    True),
                         "materials_gem_red_gem": _load("images/materials_gem_red_gem.png", True),
                         "materials_gem_blue_gem": _load("images/materials_gem_blue_gem.png", True),
                         "materials_beverage_ale": _load("images/materials_beverage_ale.png", True),
                         "materials_beverage_wine": _load("images/materials_beverage_wine.png", True),
                         "materials_beverage_rum": _load("images/materials_beverage_rum.png", True),
                         "materials_bar_iron_ingot": _load("images/materials_bar_iron_ingot.png", True),
                         "materials_ore_raw_iron": _load("images/materials_ore_raw_iron.png", True),
                         "materials_foliage_blue_herb-1": _load("images/materials_foliage_blue_herb-1.png", True),
                         "materials_foliage_green_herb": _load("images/materials_foliage_green_herb.png", True),
                         "materials_sheet_paper": _load("images/materials_sheet_paper.png", True),
                         "materials_potion_antibiotics": _load("images/materials_potion_antibiotics.png", True),
                         "materials_potion_betadine": _load("images/materials_potion_betadine.png", True),
                         "materials_potion_red_vial": _load("images/materials_potion_red_vial.png", True),
                         "materials_container_empty_vial": _load("images/materials_container_empty_vial.png", True),
                         "weapon_2handed_longsword": _load("images/weapon_2handed_longsword.png", True),
                         "armour_shield_wooden_buckler": _load("images/armour_shield_wooden_buckler.png", True),
                         "weapon_1handed_cultist_dagger": _load("images/weapon_1handed_cultist_dagger.png", True),
                         "weapon_longrange_flintlock": _load("images/weapon_longrange_flintlock.png", True),
                         "weapon_2handed_makeshift_spear": _load("images/weapon_2handed_makeshift_spear.png", True),
                         "weapon_longrange_blunderbuss": _load("images/weapon_longrange_blunderbuss.png", True),
                         "weapon_1handed_shaman_dagger": _load("images/weapon_1handed_shaman_dagger.png", True),
                         "weapon_2handed_priest_staff": _load("images/weapon_2handed_priest_staff.png", True),
                         "weapon_longrange_cultist_crossbow": _load("images/weapon_longrange_cultist_crossbow.png",
                                                                    True),
                         "materials_component_bow_string": _load("images/materials_component_bow_string.png", True),
                         "user_item_short_sword": _load("items/weapon_1handed_short_sword.png", True),
                         "user_item_cleaver": _load("items/weapon_1handed_cleaver.png", True),
                         "user_item_knife": _load("items/weapon_1handed_knife.png", True),
                         "user_item_ancient_paper": _load("items/materials_sheet_ancient_paper.png", True),
                         "user_item_iron_mask": _load("items/armour_headware_iron_mask.png", True),
                         "user_item_dark_priests_robe": _load("items/armour_body_armour_dark_priests_robe.png", True),
                         "user_item_priests_robe": _load("items/armour_body_armour_priests_robe.png", True),
                         "user_item_plate_helmet": _load("items/armour_headware_plate_helmet.png", True),
                         "user_item_padded_cap": _load("items/armour_headware_padded_cap.png", True),
                         "user_item_iron_cuirass": _load("items/armour_body_armour_iron_cuirass.png", True),
                         "user_item_loincloth": _load("items/armour_body_armour_loincloth.png", True),
                         "user_item_red_scarf": _load("items/armour_accessories_red_scarf.png", True),
                         "user_item_iron_helmet": _load("items/armour_headware_iron_helmet.png", True),
                         "user_item_guard_bascinet": _load("items/armour_headware_guard_bascinet.png", True),
                         "armour_headware_guard_coif": _load("items/armour_headware_guard_coif.png", True),
                         "user_item_chainmail_hood": _load("items/armour_headware_chainmail_hood.png", True),
                         "user_item_black_dress": _load("items/armour_body_armour_black_dress.png", True),
                         "user_item_trench_coat": _load("items/armour_body_armour_trench_coat.png", True),
                         "user_item_corsairs_saber": _load("items/weapon_1handed_corsairs_saber.png", True),
                         "user_item_cloth_hood": _load("items/weapon_1handed_cloth_hood.png", True),
                         "user_item_leather_coat": _load("items/armour_body_armour_leather_coat.png", True),
                         "user_item_leather_vest": _load("items/armour_body_armour_leather_vest.png", True),
                         "user_item_plated_mail": _load("items/armour_body_armour_plated_mail.png", True),
                         "user_item_shield_scutum": _load("items/armour_shield_scutum.png", True),
                         "user_item_musket": _load("items/weapon_longrange_musket.png", True),
                         "user_item_spear": _load("items/weapon_2handed_spear.png", True),
                         "user_item_hard_leather_armor": _load("items/armour_body_armour_hard_leather_armor.png", True),
                         "user_item_iron_plate": _load("items/armour_body_armour_iron_plate.png", True),
                         "user_item_stiletto": _load("items/weapon_1handed_stiletto.png", True),
                         "user_item_arm_guard": _load("items/armour_armwear_arm_guard.png", True),
                         "user_item_iron_axe": _load("items/weapon_1handed_iron_axe.png", True),
                         "user_item_short_bow": _load("items/weapon_longrange_short_bow.png", True),
                         "user_item_leather_scraps": _load("items/materials_scrap_leather_scraps.png", True),
                         "user_item_book_of_rapid_fire": _load("items/materials_skill_book_of_rapid_fire.png", True),
                         "user_item_book_of_instincts": _load("items/materials_skill_book_of_instincts.png", True),
                         "user_item_swift_boots": _load("items/armour_accessories_swift_boots.png", True),
                         "user_item_heavy_crossbow": _load("items/weapon_longrange_heavy_crossbow.png", True),
                         "user_item_longbow": _load("items/weapon_longrange_longbow.png", True),
                         "user_item_maul": _load("items/weapon_2handed_maul.png", True),
                         "user_item_claymore": _load("items/weapon_2handed_claymore.png", True),
                         "user_item_scimitar": _load("items/weapon_1handed_scimitar.png", True),
                         "user_item_improvised_shiv": _load("items/weapon_1handed_improvised_shiv.png", True),
                         "user_item_steel_hammer": _load("items/weapon_1handed_steel_hammer.png", True),
                         "user_item_black_dressed_doll": _load("items/material_toy_black_dressed_doll.png", True),
                         "user_item_dirk": _load("items/weapon_1handed_dirk.png", True),
                         "user_item_wooden_plank": _load("items/materials_plank_wooden_plank.png", True),
                         "user_item_dagger": _load("items/weapon_1handed_dagger.png", True),
                         "user_item_silver_wire": _load("items/materials_component_silver_wire.png", True),
                         "user_item_red_amulet": _load("items/armour_accessories_red_amulet.png", True),
                         "user_item_blue_amulet": _load("items/armour_accessories_blue_amulet.png", True),
                         "user_item_stick": _load("items/materials_component_stick.png", True),
                         "user_item_ring": _load("items/armour_accessories_ring.png", True),
                         "user_item_book_of_marksmanship": _load("items/materials_skill_book_of_marksmanship.png",
                                                                 True),
                         "user_item_book_of_stars": _load("items/materials_skill_book_of_stars.png", True),
                         "user_item_book_of_crafsmanship": _load("items/materials_skill_book_of_crafsmanship.png",
                                                                  True),
                         "user_item_book_of_agility": _load("items/materials_skill_book_of_agility.png", True),
                         "user_item_book_of_healing": _load("items/materials_skill_book_of_healing.png", True),
                         "user_item_book_of_the_secrets": _load("items/materials_skill_book_of_the_secrets.png", True),
                         "user_item_book_of_enlightenment": _load("items/materials_save_book_of_enlightenment.png",
                                                                  True),
                         "user_item_book_of_cowardice_i": _load("items/materials_skill_book_of_cowardice_i.png", True),
                         "user_item_book_of_cowardice_ii": _load("items/materials_skill_book_of_cowardice_ii.png",
                                                                 True),
                         "user_item_book_of_pestilence_i": _load("items/materials_skill_book_of_pestilence_i.png",
                                                                 True),
                         "user_item_book_of_pestilence_ii": _load("items/materials_skill_book_of_pestilence_ii.png",
                                                                  True),
                         "user_item_book_of_pestilence_iii": _load("items/materials_skill_book_of_pestilence_iii.png",
                                                                   True),
                         "user_item_book_of_pestilence_iv": _load("items/materials_skill_book_of_pestilence_iv.png",
                                                                  True),
                         "user_item_book_of_pestilence_v": _load("items/materials_skill_book_of_pestilence_v.png",
                                                                 True),
                         "user_item_book_of_pestilence_vi": _load("items/materials_skill_book_of_pestilence_vi.png",
                                                                  True),
                         "user_item_book_of_pestilence_vii": _load("items/materials_skill_book_of_pestilence_vii.png",
                                                                   True),
                         "user_item_book_of_pestilence_viii": _load("items/materials_skill_book_of_pestilence_viii.png",
                                                                    True),
                         "user_item_book_of_trade_i": _load("items/materials_skill_book_of_trade_i.png", True),
                         "user_item_book_of_trade_ii": _load("items/materials_skill_book_of_trade_ii.png", True),
                         "user_item_book_of_trade_iii": _load("items/materials_skill_book_of_trade_iii.png", True),
                         "user_item_red_gem": _load("items/materials_gem_red_gem.png", True),
                         "user_item_blue_gem": _load("items/materials_gem_blue_gem.png", True),
                         "user_item_ale": _load("items/materials_beverage_ale.png", True),
                         "user_item_wine": _load("items/materials_beverage_wine.png", True),
                         "user_item_rum": _load("items/materials_beverage_rum.png", True),
                         "user_item_iron_ingot": _load("items/materials_bar_iron_ingot.png", True),
                         "user_item_raw_iron": _load("items/materials_ore_raw_iron.png", True),
                         "user_item_blue_herb": _load("items/materials_foliage_blue_herb-1.png", True),
                         "user_item_green_herb": _load("items/materials_foliage_green_herb.png", True),
                         "user_item_paper": _load("items/materials_sheet_paper.png", True),
                         "user_item_antibiotics": _load("items/materials_potion_antibiotics.png", True),
                         "user_item_betadine": _load("items/materials_potion_betadine.png", True),
                         "user_item_red_vial": _load("items/materials_potion_red_vial.png", True),
                         "user_item_empty_vial": _load("items/materials_container_empty_vial.png", True),
                         "user_item_longsword": _load("items/weapon_2handed_longsword.png", True),
                         "user_item_wooden_buckler": _load("items/armour_shield_wooden_buckler.png", True),
                         "user_item_cultist_dagger": _load("items/weapon_1handed_cultist_dagger.png", True),
                         "user_item_flintlock": _load("items/weapon_longrange_flintlock.png", True),
                         "user_item_makeshift_spear": _load("items/weapon_2handed_makeshift_spear.png", True),
                         "user_item_blunderbuss": _load("items/weapon_longrange_blunderbuss.png", True),
                         "user_item_shaman_dagger": _load("items/weapon_1handed_shaman_dagger.png", True),
                         "user_item_priest_staff": _load("items/weapon_2handed_priest_staff.png", True),
                         "user_item_cultist_crossbow": _load("items/weapon_longrange_cultist_crossbow.png", True),
                         "materials_component_bow_string": _load("items/materials_component_bow_string.png", True),
                         "silver_chest_closed": _load("sprites/elucidate_silver_chest_closed_001.png", True),
                         "silver_chest_opened": _load("sprites/elucidate_silver_chest_opened_002.png", True),
                         "gold_chest_closed": _load("sprites/elucidate_gold_chest_closed_003.png", True),
                         "gold_chest_opened": _load("sprites/elucidate_gold_chest_opened_004.png", True),
                         "idle_cult_leader_npc_down": _load(
                             "sprites/npc_e_cult_leader/elucidate_idle_cult_leader_npc_down.png", True),
                         "idle_cult_leader_npc_up": _load(
                             "sprites/npc_e_cult_leader/elucidate_idle_cult_leader_npc_up.png", True),
                         "idle_cult_leader_npc_left": _load(
                             "sprites/npc_e_cult_leader/elucidate_idle_cult_leader_npc_left.png", True),
                         "idle_cult_leader_npc_right": _load(
                             "sprites/npc_e_cult_leader/elucidate_idle_cult_leader_npc_right.png", True),
                         "idle_cultist_soldier_npc_up": _load(
                             "sprites/npc_e_cult_soldier/elucidate_idle_cultist_npc_up.png", True),
                         "idle_cultist_soldier_npc_right": _load(
                             "sprites/npc_e_cult_soldier/elucidate_idle_cultist_npc_right.png", True),
                         "idle_cultist_soldier_npc_left": _load(
                             "sprites/npc_e_cult_soldier/elucidate_idle_cultist_npc_left.png", True),
                         "idle_cultist_soldier_npc_down": _load(
                             "sprites/npc_e_cult_soldier/elucidate_idle_cultist_npc_down.png", True),
                         "idle_corrupted1_cultist_npc_right": _load(
                             "sprites/npc_e_s1_corrupted_cultist/elucidate_idle_corrupted1_cultist_npc_right.png",
                             True), "idle_corrupted1_cultist_npc_left": _load(
            "sprites/npc_e_s1_corrupted_cultist/elucidate_idle_corrupted1_cultist_npc_left.png", True),
                         "idle_corrupted1_cultist_npc_down": _load(
                             "sprites/npc_e_s1_corrupted_cultist/elucidate_idle_corrupted1_cultist_npc_down.png", True),
                         "idle_corrupted1_cultist_npc_up": _load(
                             "sprites/npc_e_s1_corrupted_cultist/elucidate_idle_corrupted1_cultist_npc_up.png", True),
                         "idle_amalgamated_villagers_npc_right": _load(
                             "sprites/npc_e_amalgamated_villagers/elucidate_idle_amalgamated_villagers_npc_right.png",
                             True), "idle_amalgamated_villagers_npc_left": _load(
            "sprites/npc_e_amalgamated_villagers/elucidate_idle_amalgamated_villagers_npc_left.png", True),
                         "idle_amalgamated_knights_npc_right": _load(
                             "sprites/npc_e_amalgamated_knights/elucidate_idle_amalgamated_knights_npc_right.png",
                             True), "idle_amalgamated_knights_npc_left": _load(
            "sprites/npc_e_amalgamated_knights/elucidate_idle_amalgamated_knights_npc_left.png", True),
                         "idle_amalgamated_civillians_npc_right": _load(
                             "sprites/npc_e_amalgamated_civillians/elucidate_idle_amalgamated_civillians_npc_right.png",
                             True), "idle_amalgamated_civillians_npc_left": _load(
            "sprites/npc_e_amalgamated_civillians/elucidate_idle_amalgamated_civillians_npc_left.png", True),
                         "idle_melted_male_villager_npc_right": _load(
                             "sprites/npc_e_melted_villager_male/elucidate_idle_melted_male_villager_npc_right.png",
                             True), "idle_melted_male_villager_npc_left": _load(
            "sprites/npc_e_melted_villager_male/elucidate_idle_melted_male_villager_npc_left.png", True),
                         "idle_melted_male_villager_npc_up": _load(
                             "sprites/npc_e_melted_villager_male/elucidate_idle_melted_male_villager_npc_up.png", True),
                         "idle_melted_male_villager_npc_down": _load(
                             "sprites/npc_e_melted_villager_male/elucidate_idle_melted_male_villager_npc_down.png",
                             True), "idle_melted_female_villager_npc_up": _load(
            "sprites/npc_e_melted_villager_female/elucidate_idle_melted_female_villager_npc_up.png", True),
                         "idle_melted_female_villager_npc_right": _load(
                             "sprites/npc_e_melted_villager_female/elucidate_idle_melted_female_villager_npc_right.png",
                             True), "idle_melted_female_villager_npc_left": _load(
            "sprites/npc_e_melted_villager_female/elucidate_idle_melted_female_villager_npc_left.png", True),
                         "idle_melted_female_villager_npc_down": _load(
                             "sprites/npc_e_melted_villager_female/elucidate_idle_melted_female_villager_npc_down.png",
                             True), "idle_corrupted3_cultist_npc_up": _load(
            "sprites/npc_e_s3_corrupted_cultist/elucidate_idle_corrupted3_cultist_npc_up.png", True),
                         "idle_corrupted3_cultist_npc_right": _load(
                             "sprites/npc_e_s3_corrupted_cultist/elucidate_idle_corrupted3_cultist_npc_right.png",
                             True), "idle_corrupted3_cultist_npc_left": _load(
            "sprites/npc_e_s3_corrupted_cultist/elucidate_idle_corrupted3_cultist_npc_left.png", True),
                         "idle_corrupted3_cultist_npc_down": _load(
                             "sprites/npc_e_s3_corrupted_cultist/elucidate_idle_corrupted3_cultist_npc_down.png", True),
                         "idle_corrupted2_cultist_npc_up": _load(
                             "sprites/npc_e_s2_corrupted_cultist/elucidate_idle_corrupted2_cultist_npc_up.png", True),
                         "idle_corrupted2_cultist_npc_right": _load(
                             "sprites/npc_e_s2_corrupted_cultist/elucidate_idle_corrupted2_cultist_npc_right.png",
                             True), "idle_corrupted2_cultist_npc_left": _load(
            "sprites/npc_e_s2_corrupted_cultist/elucidate_idle_corrupted2_cultist_npc_left.png", True),
                         "idle_corrupted2_cultist_npc_down": _load(
                             "sprites/npc_e_s2_corrupted_cultist/elucidate_idle_corrupted2_cultist_npc_down.png", True),
                         "idle_librarian_scholar_npc_up": _load(
                             "sprites/npc_n_librarian_scholar/elucidate_idle_librarian_scholar_npc_up.png", True),
                         "idle_librarian_scholar_npc_right": _load(
                             "sprites/npc_n_librarian_scholar/elucidate_idle_librarian_scholar_npc_right.png", True),
                         "idle_librarian_scholar_npc_left": _load(
                             "sprites/npc_n_librarian_scholar/elucidate_idle_librarian_scholar_npc_left.png", True),
                         "idle_librarian_scholar_npc_down": _load(
                             "sprites/npc_n_librarian_scholar/elucidate_idle_librarian_scholar_npc_down.png", True),
                         "idle_holyknight_npc_up": _load(
                             "sprites/npc_e_luminarian_knight/elucidate_idle_holyknight_npc_up.png", True),
                         "idle_holyknight_npc_right": _load(
                             "sprites/npc_e_luminarian_knight/elucidate_idle_holyknight_npc_right.png", True),
                         "idle_holyknight_npc_left": _load(
                             "sprites/npc_e_luminarian_knight/elucidate_idle_holyknight_npc_left.png", True),
                         "idle_holyknight_npc_down": _load(
                             "sprites/npc_e_luminarian_knight/elucidate_idle_holyknight_npc_down.png", True),
                         "idle_male_faithful_citizen_npc_up": _load(
                             "sprites/npc_n_faithful_luminarian/elucidate_idle_male_faithful_citizen_npc_up.png", True),
                         "idle_male_faithful_citizen_npc_right": _load(
                             "sprites/npc_n_faithful_luminarian/elucidate_idle_male_faithful_citizen_npc_right.png",
                             True), "idle_male_faithful_citizen_npc_left": _load(
            "sprites/npc_n_faithful_luminarian/elucidate_idle_male_faithful_citizen_npc_left.png", True),
                         "idle_male_faithful_citizen_npc_down": _load(
                             "sprites/npc_n_faithful_luminarian/elucidate_idle_male_faithful_citizen_npc_down.png",
                             True), "idle_female_faithful_citizen_npc_up": _load(
            "sprites/npc_n_faithful_luminarie/elucidate_idle_female_faithful_citizen_npc_up.png", True),
                         "idle_female_faithful_citizen_npc_right": _load(
                             "sprites/npc_n_faithful_luminarie/elucidate_idle_female_faithful_citizen_npc_right.png",
                             True), "idle_female_faithful_citizen_npc_left": _load(
            "sprites/npc_n_faithful_luminarie/elucidate_idle_female_faithful_citizen_npc_left.png", True),
                         "idle_female_faithful_citizen_npc_down": _load(
                             "sprites/npc_n_faithful_luminarie/elucidate_idle_female_faithful_citizen_npc_down.png",
                             True), "idle_sprite_chuAttendants_up": _load(
            "sprites/npc_n_luminarian_priest/elucidate_idle_sprite_chuAttendants_up.png", True),
                         "idle_sprite_chuAttendants_right": _load(
                             "sprites/npc_n_luminarian_priest/elucidate_idle_sprite_chuAttendants_right.png", True),
                         "idle_sprite_chuAttendants_left": _load(
                             "sprites/npc_n_luminarian_priest/elucidate_idle_sprite_chuAttendants_left.png", True),
                         "idle_sprite_chuAttendants_down": _load(
                             "sprites/npc_n_luminarian_priest/elucidate_idle_sprite_chuAttendants_down.png", True),
                         "idle_assassin_npc_up": _load("sprites/npc_e_lunar_assasin/elucidate_idle_assassin_npc_up.png",
                                                       True), "idle_assassin_npc_right": _load(
            "sprites/npc_e_lunar_assasin/elucidate_idle_assassin_npc_right.png", True), "idle_assassin_npc_left": _load(
            "sprites/npc_e_lunar_assasin/elucidate_idle_assassin_npc_left.png", True), "idle_assassin_npc_down": _load(
            "sprites/npc_e_lunar_assasin/elucidate_idle_assassin_npc_down.png", True),
                         "idle_tribe_warrior_npc_up": _load(
                             "sprites/npc_n_seekers_warrior_male/elucidate_idle_tribe_warrior_npc_up.png", True),
                         "idle_tribe_warrior_npc_right": _load(
                             "sprites/npc_n_seekers_warrior_male/elucidate_idle_tribe_warrior_npc_right.png", True),
                         "idle_tribe_warrior_npc_left": _load(
                             "sprites/npc_n_seekers_warrior_male/elucidate_idle_tribe_warrior_npc_left.png", True),
                         "idle_tribe_warrior_npc_down": _load(
                             "sprites/npc_n_seekers_warrior_male/elucidate_idle_tribe_warrior_npc_down.png", True),
                         "idle_tribe_elder_npc_up": _load(
                             "sprites/npc_n_seekers_elder/elucidate_idle_tribe_elder_npc_up.png", True),
                         "idle_tribe_elder_npc_right": _load(
                             "sprites/npc_n_seekers_elder/elucidate_idle_tribe_elder_npc_right.png", True),
                         "idle_tribe_elder_npc_left": _load(
                             "sprites/npc_n_seekers_elder/elucidate_idle_tribe_elder_npc_left.png", True),
                         "idle_tribe_elder_npc_down": _load(
                             "sprites/npc_n_seekers_elder/elucidate_idle_tribe_elder_npc_down.png", True),
                         "idle_tribe_chief_npc_up": _load(
                             "sprites/npc_n_seekers_chieftain/elucidate_idle_tribe_chief_npc_up.png", True),
                         "idle_tribe_chief_npc_right": _load(
                             "sprites/npc_n_seekers_chieftain/elucidate_idle_tribe_chief_npc_right.png", True),
                         "idle_tribe_chief_npc_left": _load(
                             "sprites/npc_n_seekers_chieftain/elucidate_idle_tribe_chief_npc_left.png", True),
                         "idle_tribe_chief_npc_down": _load(
                             "sprites/npc_n_seekers_chieftain/elucidate_idle_tribe_chief_npc_down.png", True),
                         "idle_supply_merchant_npc_down": _load(
                             "sprites/npc_n_traveling_merchant/elucidate_idle_supply_merchant_npc_down.png", True),
                         "idle_supply_merchant_npc_up": _load(
                             "sprites/npc_n_traveling_merchant/elucidate_idle_supply_merchant_npc_up.png", True),
                         "idle_supply_merchant_npc_right": _load(
                             "sprites/npc_n_traveling_merchant/elucidate_idle_supply_merchant_npc_right.png", True),
                         "idle_supply_merchant_npc_left": _load(
                             "sprites/npc_n_traveling_merchant/elucidate_idle_supply_merchant_npc_left.png", True),
                         "idle_merchant_guild_member_npc_up": _load(
                             "sprites/npc_n_merchant_guild_member/elucidate_idle_merchant_guild_npc_up.png", True),
                         "idle_merchant_guild_member_npc_right": _load(
                             "sprites/npc_n_merchant_guild_member/elucidate_idle_merchant_guild_npc_right.png", True),
                         "idle_merchant_guild_member_npc_left": _load(
                             "sprites/npc_n_merchant_guild_member/elucidate_idle_merchant_guild_npc_left.png", True),
                         "idle_merchant_guild_member_npc_down": _load(
                             "sprites/npc_n_merchant_guild_member/elucidate_idle_merchant_guild_npc_down.png", True),
                         "idle_merchant_guild_master_npc_up": _load(
                             "sprites/npc_n_merchant_guild_director/elucidate_idle_merchant_guild_master_npc_up.png",
                             True), "idle_merchant_guild_master_npc_right": _load(
            "sprites/npc_n_merchant_guild_director/elucidate_idle_merchant_guild_master_npc_right.png", True),
                         "idle_merchant_guild_master_npc_left": _load(
                             "sprites/npc_n_merchant_guild_director/elucidate_idle_merchant_guild_master_npc_left.png",
                             True), "idle_merchant_guild_master_npc_down": _load(
            "sprites/npc_n_merchant_guild_director/elucidate_idle_merchant_guild_master_npc_down.png", True),
                         "idle_harbor_captain_npc_up": _load(
                             "sprites/npc_n_harbor_captain/elucidate_idle_harbor_captain_npc_up.png", True),
                         "idle_harbor_captain_npc_right": _load(
                             "sprites/npc_n_harbor_captain/elucidate_idle_harbor_captain_npc_right.png", True),
                         "idle_harbor_captain_npc_left": _load(
                             "sprites/npc_n_harbor_captain/elucidate_idle_harbor_captain_npc_left.png", True),
                         "idle_harbor_captain_npc_down": _load(
                             "sprites/npc_n_harbor_captain/elucidate_idle_harbor_captain_npc_down.png", True),
                         "idle_male_villager_variant_npc_up": _load(
                             "sprites/npc_n_s2_outskirts_villagers/elucidate_idle_male_villager_variant_npc_up.png",
                             True), "idle_male_villager_variant_npc_right": _load(
            "sprites/npc_n_s2_outskirts_villagers/elucidate_idle_male_villager_variant_npc_right.png", True),
                         "idle_male_villager_variant_npc_left": _load(
                             "sprites/npc_n_s2_outskirts_villagers/elucidate_idle_male_villager_variant_npc_left.png",
                             True), "idle_male_villager_variant_npc_down": _load(
            "sprites/npc_n_s2_outskirts_villagers/elucidate_idle_male_villager_variant_npc_down.png", True),
                         "idle_male_villager_npc_up": _load(
                             "sprites/npc_n_s1_outskirts_villagers/elucidate_idle_male_villager_npc_up.png", True),
                         "idle_male_villager_npc_right": _load(
                             "sprites/npc_n_s1_outskirts_villagers/elucidate_idle_male_villager_npc_right.png", True),
                         "idle_male_villager_npc_left": _load(
                             "sprites/npc_n_s1_outskirts_villagers/elucidate_idle_male_villager_npc_left.png", True),
                         "idle_male_villager_npc_down": _load(
                             "sprites/npc_n_s1_outskirts_villagers/elucidate_idle_male_villager_npc_down.png", True),
                         "idle_female_villager_variant_npc_up": _load(
                             "sprites/npc_n_s2_outskirts_villagers/elucidate_idle_female_villager_variant_npc_up.png",
                             True), "idle_female_villager_variant_npc_right": _load(
            "sprites/npc_n_s2_outskirts_villagers/elucidate_idle_female_villager_variant_npc_right.png", True),
                         "idle_female_villager_variant_npc_left": _load(
                             "sprites/npc_n_s2_outskirts_villagers/elucidate_idle_female_villager_variant_npc_left.png",
                             True), "idle_female_villager_variant_npc_down": _load(
            "sprites/npc_n_s2_outskirts_villagers/elucidate_idle_female_villager_variant_npc_down.png", True),
                         "idle_female_villager_npc_up": _load(
                             "sprites/npc_n_s1_outskirts_villagers/elucidate_idle_female_villager_npc_up.png", True),
                         "idle_female_villager_npc_right": _load(
                             "sprites/npc_n_s1_outskirts_villagers/elucidate_idle_female_villager_npc_right.png", True),
                         "idle_female_villager_npc_left": _load(
                             "sprites/npc_n_s1_outskirts_villagers/elucidate_idle_female_villager_npc_left.png", True),
                         "idle_female_villager_npc_down": _load(
                             "sprites/npc_n_s1_outskirts_villagers/elucidate_idle_female_villager_npc_down.png", True),
                         "idle_guards_npc_up": _load("sprites/npc_n_guards/elucidate_idle_guards_npc_up.png", True),
                         "idle_guards_npc_right": _load("sprites/npc_n_guards/elucidate_idle_guards_npc_right.png",
                                                        True),
                         "idle_guards_npc_left": _load("sprites/npc_n_guards/elucidate_idle_guards_npc_left.png", True),
                         "idle_guards_npc_down": _load("sprites/npc_n_guards/elucidate_idle_guards_npc_down.png", True),
                         "idle_guard_captain_npc_up": _load(
                             "sprites/npc_n_guard_captain/elucidate_idle_guard_captain_npc_up.png", True),
                         "idle_guard_captain_npc_right": _load(
                             "sprites/npc_n_guard_captain/elucidate_idle_guard_captain_npc_right.png", True),
                         "idle_guard_captain_npc_left": _load(
                             "sprites/npc_n_guard_captain/elucidate_idle_guard_captain_npc_left.png", True),
                         "idle_guard_captain_npc_down": _load(
                             "sprites/npc_n_guard_captain/elucidate_idle_guard_captain_npc_down.png", True),
                         "idle_draft_officer_npc_up": _load(
                             "sprites/npc_n_draft_officer/elucidate_idle_draft_officer_npc_up.png", True),
                         "idle_draft_officer_npc_right": _load(
                             "sprites/npc_n_draft_officer/elucidate_idle_draft_officer_npc_right.png", True),
                         "idle_draft_officer_npc_left": _load(
                             "sprites/npc_n_draft_officer/elucidate_idle_draft_officer_npc_left.png", True),
                         "idle_draft_officer_npc_down": _load(
                             "sprites/npc_n_draft_officer/elucidate_idle_draft_officer_npc_down.png", True),
                         "idle_male_civilian_npc_up": _load(
                             "sprites/npc_n_s1_walled_city_civilians_male/elucidate_idle_male_civilian_npc_up.png",
                             True), "idle_male_civilian_npc_right": _load(
            "sprites/npc_n_s1_walled_city_civilians_male/elucidate_idle_male_civilian_npc_right.png", True),
                         "idle_male_civilian_npc_left": _load(
                             "sprites/npc_n_s1_walled_city_civilians_male/elucidate_idle_male_civilian_npc_left.png",
                             True), "idle_male_civilian_npc_down": _load(
            "sprites/npc_n_s1_walled_city_civilians_male/elucidate_idle_male_civilian_npc_down.png", True),
                         "idle_female_civilian_npc_up": _load(
                             "sprites/npc_n_s1_walled_city_civilians_female/elucidate_idle_female_civilian_npc_up.png",
                             True), "idle_female_civilian_npc_right": _load(
            "sprites/npc_n_s1_walled_city_civilians_female/elucidate_idle_female_civilian_npc_right.png", True),
                         "idle_female_civilian_npc_left": _load(
                             "sprites/npc_n_s1_walled_city_civilians_female/elucidate_idle_female_civilian_npc_left.png",
                             True), "idle_female_civilian_npc_down": _load(
            "sprites/npc_n_s1_walled_city_civilians_female/elucidate_idle_female_civilian_npc_down.png", True),
                         "idle_blacksmith_npc_up": _load(
                             "sprites/npc_n_blacksmith_conrad/elucidate_idle_blacksmith_npc_up.png", True),
                         "idle_blacksmith_npc_right": _load(
                             "sprites/npc_n_blacksmith_conrad/elucidate_idle_blacksmith_npc_right.png", True),
                         "idle_blacksmith_npc_left": _load(
                             "sprites/npc_n_blacksmith_conrad/elucidate_idle_blacksmith_npc_left.png", True),
                         "idle_blacksmith_npc_down": _load(
                             "sprites/npc_n_blacksmith_conrad/elucidate_idle_blacksmith_npc_down.png", True),
                         "idle_caligo_manifestation_npc_down": _load(
                             "sprites/npc_e_caligo_manifestation/elucidate_idle_caligo_manifestation.png", True),
                         "idle_caligo_manifestation_black_bg": _load(
                             "sprites/npc_e_caligo_manifestation/elucidate_idle_caligo_manifestation_black_bg.png",
                             True), "idle_imprisoned_experiment_1_npc_down": _load(
            "sprites/npc_e_imprisoned_experiment/elucidate_idle_imprisoned_experiment_1_npc_down.png", True),
                         "idle_imprisoned_experiment_2_npc_down": _load(
                             "sprites/npc_e_imprisoned_experiment/elucidate_idle_imprisoned_experiment_2_npc_down.png",
                             True), "idle_imprisoned_experiment_hostile_npc_down": _load(
            "sprites/npc_e_imprisoned_experiment/elucidate_idle_imprisoned_experiment_hostile_npc_down.png", True),
                         "idle_church_medical_staff_npc_down": _load(
                             "sprites/npc_n_luminarian_scientist/elucidate_idle_church_medical_staff_npc_down.png",
                             True), "idle_church_medical_staff_npc_right": _load(
            "sprites/npc_n_luminarian_scientist/elucidate_idle_church_medical_staff_npc_right.png", True),
                         "idle_church_medical_staff_npc_left": _load(
                             "sprites/npc_n_luminarian_scientist/elucidate_idle_church_medical_staff_npc_left.png",
                             True), "idle_church_medical_staff_npc_up": _load(
            "sprites/npc_n_luminarian_scientist/elucidate_idle_church_medical_staff_npc_up.png", True),
                         "idle_church_spy_npc_down": _load(
                             "sprites/npc_e_luminarian_spy/elucidate_idle_church_spy_npc_down.png", True),
                         "walk_church_spy_npc_down_001": _load(
                             "sprites/npc_e_luminarian_spy/elucidate_walk_church_spy_npc_down_001.png", True),
                         "walk_church_spy_npc_down_002": _load(
                             "sprites/npc_e_luminarian_spy/elucidate_walk_church_spy_npc_down_002.png", True),
                         "idle_church_spy_npc_right": _load(
                             "sprites/npc_e_luminarian_spy/elucidate_idle_church_spy_npc_right.png", True),
                         "walk_church_spy_npc_right_001": _load(
                             "sprites/npc_e_luminarian_spy/elucidate_walk_church_spy_npc_right_001.png", True),
                         "walk_church_spy_npc_right_002": _load(
                             "sprites/npc_e_luminarian_spy/elucidate_walk_church_spy_npc_right_002.png", True),
                         "idle_church_spy_npc_left": _load(
                             "sprites/npc_e_luminarian_spy/elucidate_idle_church_spy_npc_left.png", True),
                         "walk_church_spy_npc_left_001": _load(
                             "sprites/npc_e_luminarian_spy/elucidate_walk_church_spy_npc_left_001.png", True),
                         "walk_church_spy_npc_left_002": _load(
                             "sprites/npc_e_luminarian_spy/elucidate_walk_church_spy_npc_left_002.png", True),
                         "idle_church_spy_npc_up": _load(
                             "sprites/npc_e_luminarian_spy/elucidate_idle_church_spy_npc_up.png", True),
                         "walk_church_spy_npc_up_001": _load(
                             "sprites/npc_e_luminarian_spy/elucidate_walk_church_spy_npc_up_001.png", True),
                         "walk_church_spy_npc_up_002": _load(
                             "sprites/npc_e_luminarian_spy/elucidate_walk_church_spy_npc_up_002.png", True),
                         "idle_female_market_merchant_npc_down": _load(
                             "sprites/npc_n_market_merchant_female/elucidate_idle_female_market_merchant_npc_down.png",
                             True), "idle_female_market_merchant_npc_right": _load(
            "sprites/npc_n_market_merchant_female/elucidate_idle_female_market_merchant_npc_right.png", True),
                         "idle_female_market_merchant_npc_left": _load(
                             "sprites/npc_n_market_merchant_female/elucidate_idle_female_market_merchant_npc_left.png",
                             True), "idle_female_market_merchant_npc_up": _load(
            "sprites/npc_n_market_merchant_female/elucidate_idle_female_market_merchant_npc_up.png", True),
                         "idle_male_market_merchant_npc_down": _load(
                             "sprites/npc_n_market_merchant_male/elucidate_idle_male_market_merchant_npc_down.png",
                             True), "idle_male_market_merchant_npc_right": _load(
            "sprites/npc_n_market_merchant_male/elucidate_idle_male_market_merchant_npc_right.png", True),
                         "idle_male_market_merchant_npc_left": _load(
                             "sprites/npc_n_market_merchant_male/elucidate_idle_male_market_merchant_npc_left.png",
                             True), "idle_male_market_merchant_npc_up": _load(
            "sprites/npc_n_market_merchant_male/elucidate_idle_male_market_merchant_npc_up.png", True),
                         "idle_ghost_memory1_npc_left": _load(
                             "sprites/npc_n_ghost_memories/elucidate_idle_ghost_memory1_npc_left.png", True),
                         "idle_ghost_memory1_npc_right": _load(
                             "sprites/npc_n_ghost_memories/elucidate_idle_ghost_memory1_npc_right.png", True),
                         "idle_ghost_memory2_npc_left": _load(
                             "sprites/npc_n_ghost_memories/elucidate_idle_ghost_memory2_npc_left.png", True),
                         "idle_ghost_memory2_npc_right": _load(
                             "sprites/npc_n_ghost_memories/elucidate_idle_ghost_memory2_npc_right.png", True),
                         "idle_female_tribal_warrior_npc_down": _load(
                             "sprites/npc_n_seekers_warrior_female/elucidate_idle_female_tribal_warrior_npc_down.png",
                             True), "idle_female_tribal_warrior_npc_left": _load(
            "sprites/npc_n_seekers_warrior_female/elucidate_idle_female_tribal_warrior_npc_left.png", True),
                         "idle_female_tribal_warrior_npc_right": _load(
                             "sprites/npc_n_seekers_warrior_female/elucidate_idle_female_tribal_warrior_npc_right.png",
                             True), "idle_female_tribal_warrior_npc_up": _load(
            "sprites/npc_n_seekers_warrior_female/elucidate_idle_female_tribal_warrior_npc_up.png", True),
                         "idle_travelling_bard_npc_down": _load(
                             "sprites/npc_n_traveling_merchant/elucidate_idle_supply_merchant_npc_down.png", True),
                         "idle_travelling_bard_npc_left": _load(
                             "sprites/npc_n_traveling_merchant/elucidate_idle_supply_merchant_npc_left.png", True),
                         "idle_travelling_bard_npc_right": _load(
                             "sprites/npc_n_traveling_merchant/elucidate_idle_supply_merchant_npc_right.png", True),
                         "idle_travelling_bard_npc_up": _load(
                             "sprites/npc_n_traveling_merchant/elucidate_idle_supply_merchant_npc_up.png", True),
                         "idle_cultist_priest_npc_down": _load(
                             "sprites/npc_n_cult_priest/elucidate_idle_cultist_priest_npc_down.png", True),
                         "idle_cultist_priest_npc_left": _load(
                             "sprites/npc_n_cult_priest/elucidate_idle_cultist_priest_npc_left.png", True),
                         "idle_cultist_priest_npc_right": _load(
                             "sprites/npc_n_cult_priest/elucidate_idle_cultist_priest_npc_right.png", True),
                         "idle_cultist_priest_npc_up": _load(
                             "sprites/npc_n_cult_priest/elucidate_idle_cultist_priest_npc_up.png", True),
                         "idle_tavern_keeper_npc_down": _load(
                             "sprites/npc_n_tavern_keeper/elucidate_idle_tavern_keeper_npc_down.png", True),
                         "idle_tavern_keeper_npc_left": _load(
                             "sprites/npc_n_tavern_keeper/elucidate_idle_tavern_keeper_npc_left.png", True),
                         "idle_tavern_keeper_npc_right": _load(
                             "sprites/npc_n_tavern_keeper/elucidate_idle_tavern_keeper_npc_right.png", True),
                         "idle_tavern_keeper_npc_up": _load(
                             "sprites/npc_n_tavern_keeper/elucidate_idle_tavern_keeper_npc_up.png", True),
                         "idle_cultist_archer_npc_down": _load(
                             "sprites/npc_e_cult_archers/elucidate_idle_cultist_archer_npc_down.png", True),
                         "walk_cultist_archer_npc_down_001": _load(
                             "sprites/npc_e_cult_archers/elucidate_walk_cultist_archer_npc_down_001.png", True),
                         "walk_cultist_archer_npc_down_002": _load(
                             "sprites/npc_e_cult_archers/elucidate_walk_cultist_archer_npc_down_002.png", True),
                         "idle_cultist_archer_npc_left": _load(
                             "sprites/npc_e_cult_archers/elucidate_idle_cultist_archer_npc_left.png", True),
                         "walk_cultist_archer_npc_left_001": _load(
                             "sprites/npc_e_cult_archers/elucidate_walk_cultist_archer_npc_left_001.png", True),
                         "walk_cultist_archer_npc_left_002": _load(
                             "sprites/npc_e_cult_archers/elucidate_walk_cultist_archer_npc_left_002.png", True),
                         "idle_cultist_archer_npc_right": _load(
                             "sprites/npc_e_cult_archers/elucidate_idle_cultist_archer_npc_right.png", True),
                         "walk_cultist_archer_npc_right_001": _load(
                             "sprites/npc_e_cult_archers/elucidate_walk_cultist_archer_npc_right_001.png", True),
                         "walk_cultist_archer_npc_right_002": _load(
                             "sprites/npc_e_cult_archers/elucidate_walk_cultist_archer_npc_right_002.png", True),
                         "idle_cultist_archer_npc_up": _load(
                             "sprites/npc_e_cult_archers/elucidate_idle_cultist_archer_npc_up.png", True),
                         "walk_cultist_archer_npc_up_001": _load(
                             "sprites/npc_e_cult_archers/elucidate_walk_cultist_archer_npc_up_001.png", True),
                         "walk_cultist_archer_npc_up_002": _load(
                             "sprites/npc_e_cult_archers/elucidate_walk_cultist_archer_npc_up_002.png", True),
                         "idle_cultist_channeler_npc_down": _load(
                             "sprites/npc_e_cult_eldritch_channelers/elucidate_idle_cultist_channeler_npc_down.png",
                             True), "walk_cultist_channeler_npc_down_001": _load(
            "sprites/npc_e_cult_eldritch_channelers/elucidate_walk_cultist_chaneller_npc_down_001.png", True),
                         "walk_cultist_channeler_npc_down_002": _load(
                             "sprites/npc_e_cult_eldritch_channelers/elucidate_walk_cultist_chaneller_npc_down_002.png",
                             True), "idle_cultist_channeler_npc_right": _load(
            "sprites/npc_e_cult_eldritch_channelers/elucidate_idle_cultist_channeler_npc_right.png", True),
                         "walk_cultist_channeler_npc_right_001": _load(
                             "sprites/npc_e_cult_eldritch_channelers/elucidate_walk_cultist_chaneller_npc_right_001.png",
                             True),
                         "walk_cultist_channeler_npc_right_002": _load(
                             "sprites/npc_e_cult_eldritch_channelers/elucidate_walk_cultist_chaneller_npc_right_002.png",
                             True),
                         "idle_cultist_channeler_npc_left": _load(
                             "sprites/npc_e_cult_eldritch_channelers/elucidate_idle_cultist_channeler_npc_left.png",
                             True), "walk_cultist_channeler_npc_left_001": _load(
            "sprites/npc_e_cult_eldritch_channelers/elucidate_walk_cultist_chaneller_npc_left_001.png", True),
                         "walk_cultist_channeler_npc_left_002": _load(
                             "sprites/npc_e_cult_eldritch_channelers/elucidate_walk_cultist_chaneller_npc_left_002.png",
                             True), "idle_cultist_channeler_npc_up": _load(
            "sprites/npc_e_cult_eldritch_channelers/elucidate_idle_cultist_channeler_npc_up.png", True),
                         "walk_cultist_channeler_npc_up_001": _load(
                             "sprites/npc_e_cult_eldritch_channelers/elucidate_walk_cultist_chaneller_npc_up_001.png",
                             True), "walk_cultist_channeler_npc_up_002": _load(
            "sprites/npc_e_cult_eldritch_channelers/elucidate_walk_cultist_chaneller_npc_up_002.png", True),
                         "idle_assassin_npc_down": _load(
                             "sprites/npc_e_lunar_assasin/elucidate_idle_assassin_npc_down.png", True),
                         "walk_church_assassin_npc_down_001": _load(
                             "sprites/npc_e_lunar_assasin/elucidate_walk_church_assassin_npc_down_001.png", True),
                         "walk_church_assassin_npc_down_002": _load(
                             "sprites/npc_e_lunar_assasin/elucidate_walk_church_assassin_npc_down_002.png", True),
                         "idle_assassin_npc_left": _load(
                             "sprites/npc_e_lunar_assasin/elucidate_idle_assassin_npc_left.png", True),
                         "walk_church_assassin_npc_left_001": _load(
                             "sprites/npc_e_lunar_assasin/elucidate_walk_church_assassin_npc_left_001.png", True),
                         "walk_church_assassin_npc_left_002": _load(
                             "sprites/npc_e_lunar_assasin/elucidate_walk_church_assassin_npc_left_002.png", True),
                         "idle_assassin_npc_right": _load(
                             "sprites/npc_e_lunar_assasin/elucidate_idle_assassin_npc_right.png", True),
                         "walk_church_assassin_npc_right_001": _load(
                             "sprites/npc_e_lunar_assasin/elucidate_walk_church_assassin_npc_right_001.png", True),
                         "walk_church_assassin_npc_right_002": _load(
                             "sprites/npc_e_lunar_assasin/elucidate_walk_church_assassin_npc_right_002.png", True),
                         "idle_assassin_npc_up": _load("sprites/npc_e_lunar_assasin/elucidate_idle_assassin_npc_up.png",
                                                       True), "walk_church_assassin_npc_up_001": _load(
            "sprites/npc_e_lunar_assasin/elucidate_walk_church_assassin_npc_up_002.png", True),
                         "walk_church_assassin_npc_up_002": _load(
                             "sprites/npc_e_lunar_assasin/elucidate_walk_church_assassin_npc_up_002.png", True),
                         "walk_shaman_left_001": _load("sprites/player_shaman/elucidate_sprite_shaman_left_001.png",
                                                       True),
                         "walk_shaman_left_002": _load("sprites/player_shaman/elucidate_sprite_shaman_left_002.png",
                                                       True),
                         "idle_shaman_left": _load("sprites/player_shaman/elucidate_sprite_shaman_left_003.png", True),
                         "attack_shaman_left_001": _load("sprites/player_shaman/elucidate_attack_shaman_left_001.png",
                                                         True),
                         "attack_shaman_left_002": _load("sprites/player_shaman/elucidate_attack_shaman_left_002.png",
                                                         True),
                         "walk_shaman_down_001": _load("sprites/player_shaman/elucidate_sprite_shaman_down_001.png",
                                                       True),
                         "walk_shaman_down_002": _load("sprites/player_shaman/elucidate_sprite_shaman_down_002.png",
                                                       True),
                         "idle_shaman_down": _load("sprites/player_shaman/elucidate_sprite_shaman_down.png", True),
                         "attack_shaman_down_001": _load("sprites/player_shaman/elucidate_attack_shaman_down_001.png",
                                                         True),
                         "attack_shaman_down_002": _load("sprites/player_shaman/elucidate_attack_shaman_down_002.png",
                                                         True),
                         "walk_shaman_up_001": _load("sprites/player_shaman/elucidate_sprite_shaman_up_001.png", True),
                         "walk_shaman_up_002": _load("sprites/player_shaman/elucidate_sprite_shaman_up_002.png", True),
                         "idle_shaman_up": _load("sprites/player_shaman/elucidate_sprite_shaman_up.png", True),
                         "attack_shaman_up_001": _load("sprites/player_shaman/elucidate_attack_shaman_up_001.png",
                                                       True),
                         "attack_shaman_up_002": _load("sprites/player_shaman/elucidate_attack_shaman_up_002.png",
                                                       True),
                         "walk_shaman_right_001": _load("sprites/player_shaman/elucidate_sprite_shaman_right_001.png",
                                                        True),
                         "walk_shaman_right_002": _load("sprites/player_shaman/elucidate_sprite_shaman_right_002.png",
                                                        True),
                         "idle_shaman_right": _load("sprites/player_shaman/elucidate_sprite_shaman_right_004.png",
                                                    True),
                         "attack_shaman_right_001": _load("sprites/player_shaman/elucidate_attack_shaman_right_001.png",
                                                          True),
                         "attack_shaman_right_002": _load("sprites/player_shaman/elucidate_attack_shaman_right_002.png",
                                                          True),
                         "walk_merchant_up_001": _load("sprites/player_merchant/elucidate_sprite_merchant_up_001.png",
                                                       True),
                         "walk_merchant_up_002": _load("sprites/player_merchant/elucidate_sprite_merchant_up_002.png",
                                                       True),
                         "idle_merchant_up": _load("sprites/player_merchant/elucidate_sprite_merchant_up.png", True),
                         "attack_merchant_up_001": _load("sprites/player_merchant/elucidate_attack_merchant_up_001.png",
                                                         True),
                         "attack_merchant_up_002": _load("sprites/player_merchant/elucidate_attack_merchant_up_002.png",
                                                         True), "walk_merchant_right_001": _load(
            "sprites/player_merchant/elucidate_sprite_merchant_right_001.png", True), "walk_merchant_right_002": _load(
            "sprites/player_merchant/elucidate_sprite_merchant_right_002.png", True),
                         "idle_merchant_right": _load("sprites/player_merchant/elucidate_sprite_merchant_right_004.png",
                                                      True), "attack_merchant_right_001": _load(
            "sprites/player_merchant/elucidate_attack_merchant_right_001.png", True),
                         "attack_merchant_right_002": _load(
                             "sprites/player_merchant/elucidate_attack_merchant_right_002.png", True),
                         "walk_merchant_left_001": _load(
                             "sprites/player_merchant/elucidate_sprite_merchant_left_001.png", True),
                         "walk_merchant_left_002": _load(
                             "sprites/player_merchant/elucidate_sprite_merchant_left_002.png", True),
                         "idle_merchant_left": _load("sprites/player_merchant/elucidate_sprite_merchant_left_003.png",
                                                     True), "attack_merchant_left_001": _load(
            "sprites/player_merchant/elucidate_attack_merchant_left_001.png", True), "attack_merchant_left_002": _load(
            "sprites/player_merchant/elucidate_attack_merchant_left_002.png", True), "walk_merchant_down_001": _load(
            "sprites/player_merchant/elucidate_sprite_merchant_down_001.png", True), "walk_merchant_down_002": _load(
            "sprites/player_merchant/elucidate_sprite_merchant_down_002.png", True),
                         "idle_merchant_down": _load("sprites/player_merchant/elucidate_sprite_merchant_down_002.png",
                                                     True), "attack_merchant_down_001": _load(
            "sprites/player_merchant/elucidate_attack_merchant_down_001.png", True), "attack_merchant_down_002": _load(
            "sprites/player_merchant/elucidate_attack_merchant_down_002.png", True),
                         "walk_priest_left_001": _load("sprites/player_priest/elucidate_sprite_priest_left_001.png",
                                                       True),
                         "walk_priest_left_002": _load("sprites/player_priest/elucidate_sprite_priest_left_002.png",
                                                       True),
                         "idle_priest_left": _load("sprites/player_priest/elucidate_sprite_priest_left.png", True),
                         "attack_priest_left_001": _load("sprites/player_priest/elucidate_attack_priest_left_001.png",
                                                         True),
                         "attack_priest_left_002": _load("sprites/player_priest/elucidate_attack_priest_left_002.png",
                                                         True),
                         "walk_priest_down_001": _load("sprites/player_priest/elucidate_sprite_priest_down_001.png",
                                                       True),
                         "walk_priest_down_002": _load("sprites/player_priest/elucidate_sprite_priest_down_002.png",
                                                       True),
                         "idle_priest_down": _load("sprites/player_priest/elucidate_sprite_priest_down.png", True),
                         "attack_priest_down_001": _load("sprites/player_priest/elucidate_attack_priest_down_001.png",
                                                         True),
                         "attack_priest_down_002": _load("sprites/player_priest/elucidate_attack_priest_down_002.png",
                                                         True),
                         "walk_priest_up_001": _load("sprites/player_priest/elucidate_sprite_priest_up_001.png", True),
                         "walk_priest_up_002": _load("sprites/player_priest/elucidate_sprite_priest_up_002.png", True),
                         "idle_priest_up": _load("sprites/player_priest/elucidate_sprite_priest_up.png", True),
                         "attack_priest_up_001": _load("sprites/player_priest/elucidate_attack_priest_up_001.png",
                                                       True),
                         "attack_priest_up_002": _load("sprites/player_priest/elucidate_attack_priest_up_002.png",
                                                       True),
                         "walk_priest_right_001": _load("sprites/player_priest/elucidate_sprite_priest_right_001.png",
                                                        True),
                         "walk_priest_right_002": _load("sprites/player_priest/elucidate_sprite_priest_right_002.png",
                                                        True),
                         "idle_priest_right": _load("sprites/player_priest/elucidate_sprite_priest_right.png", True),
                         "attack_priest_right_001": _load("sprites/player_priest/elucidate_attack_priest_right_001.png",
                                                          True),
                         "attack_priest_right_002": _load("sprites/player_priest/elucidate_attack_priest_right_002.png",
                                                          True), "walk_cultist_down_001": _load(
            "sprites/player_cultist/elucidate_walking_sprite_cultist_down_001.png", True),
                         "walk_cultist_down_002": _load(
                             "sprites/player_cultist/elucidate_walking_sprite_cultist_down_002.png", True),
                         "idle_cultist_down": _load("sprites/player_cultist/elucidate_sprite_cultist_down_002.png",
                                                    True), "attack_cultist_down_001": _load(
            "sprites/player_cultist/elucidate_attack_cultist_down_001.png", True), "attack_cultist_down_002": _load(
            "sprites/player_cultist/elucidate_attack_cultist_down_002.png", True), "walk_cultist_up_001": _load(
            "sprites/player_cultist/elucidate_walking_sprite_cultist_up_001.png", True), "walk_cultist_up_002": _load(
            "sprites/player_cultist/elucidate_walking_sprite_cultist_up_002.png", True),
                         "idle_cultist_up": _load("sprites/player_cultist/elucidate_sprite_cultist_up_001.png", True),
                         "attack_cultist_up_001": _load("sprites/player_cultist/elucidate_attack_cultist_up_001.png",
                                                        True),
                         "attack_cultist_up_002": _load("sprites/player_cultist/elucidate_attack_cultist_up_002.png",
                                                        True), "walk_cultist_right_001": _load(
            "sprites/player_cultist/elucidate_walking_sprite_cultist_right_001.png", True),
                         "walk_cultist_right_002": _load(
                             "sprites/player_cultist/elucidate_walking_sprite_cultist_right_002.png", True),
                         "idle_cultist_right": _load("sprites/player_cultist/elucidate_sprite_cultist_right_004.png",
                                                     True), "attack_cultist_right_001": _load(
            "sprites/player_cultist/elucidate_attack_cultist_right_001.png", True), "attack_cultist_right_002": _load(
            "sprites/player_cultist/elucidate_attack_cultist_right_002.png", True), "walk_cultist_left_001": _load(
            "sprites/player_cultist/elucidate_walking_sprite_cultist_left_001.png", True),
                         "walk_cultist_left_002": _load(
                             "sprites/player_cultist/elucidate_walking_sprite_cultist_left_002.png", True),
                         "idle_cultist_left": _load("sprites/player_cultist/elucidate_sprite_cultist_left_003.png",
                                                    True), "attack_cultist_left_001": _load(
            "sprites/player_cultist/elucidate_attack_cultist_left_001.png", True), "attack_cultist_left_002": _load(
            "sprites/player_cultist/elucidate_attack_cultist_left_002.png", True),
                         "attack_sprite_mercenary_up_001": _load(
                             "sprites/player_mercenary/elucidate_atk_sprite_mercenary_up_001.png", True),
                         "attack_sprite_mercenary_up_002": _load(
                             "sprites/player_mercenary/elucidate_atk_sprite_mercenary_up_002.png", True),
                         "attack_sprite_mercenary_right_001": _load(
                             "sprites/player_mercenary/elucidate_atk_sprite_mercenary_right_001.png", True),
                         "attack_sprite_mercenary_right_002": _load(
                             "sprites/player_mercenary/elucidate_atk_sprite_mercenary_right_002.png", True),
                         "attack_sprite_mercenary_left_001": _load(
                             "sprites/player_mercenary/elucidate_atk_sprite_mercenary_left_001.png", True),
                         "attack_sprite_mercenary_left_002": _load(
                             "sprites/player_mercenary/elucidate_atk_sprite_mercenary_left_002.png", True),
                         "attack_sprite_mercenary_down_001": _load(
                             "sprites/player_mercenary/elucidate_atk_sprite_mercenary_down_001.png", True),
                         "attack_sprite_mercenary_down_002": _load(
                             "sprites/player_mercenary/elucidate_atk_sprite_mercenary_down_002.png", True), }

    screen.fill((0, 0, 0))
    try:
        _title_img = pygame.image.load("images/elucidate_full_text_portait_001.png")
        _title_resized = pygame.transform.scale(_title_img, (screen_x // 2, screen_y // 2))
        screen.blit(_title_resized, (screen_x // 4, screen_y // 4))
        _sel_img = pygame.image.load("images/elucidate_select_full.png")
        _sel_resized = pygame.transform.scale(_sel_img, (screen_x // 2, 30))
        screen.blit(_sel_resized, (screen_x // 4, screen_y - 115))
    except Exception:
        pass
    _load_font_a = pygame.font.SysFont("Times New Roman", 25)
    _load_font_b = pygame.font.SysFont("Times New Roman", 20)
    _load_surf_a = _load_font_a.render("Scaling Assets", True, (0, 0, 0))
    _load_rect_a = _load_surf_a.get_rect(center=(screen_x // 2, screen_y - 100))
    screen.blit(_load_surf_a, _load_rect_a)
    _load_surf_b = _load_font_b.render("Building Environment Resources...", True, (255, 255, 255))
    _load_rect_b = _load_surf_b.get_rect(center=(screen_x // 2, screen_y - 20))
    screen.blit(_load_surf_b, _load_rect_b)
    pygame.draw.rect(screen, (160, 0, 0), (0, 0, screen_x, screen_y), 1)
    pygame.display.flip()
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    _sc = pygame.transform.scale
    _scaled_images = {"l_o_outer_gate_district": _sc(_preloaded_images["l_o_outer_gate_district"],
                                                     (int(5997 / 2.7), int(3350 / 2.7))),
                      "l_i_customs_office": _sc(_preloaded_images["l_i_customs_office"],
                                                (int(5997 / 4.7), int(3350 / 4.7))),
                      "l_o_merchant_quarter": _sc(_preloaded_images["l_o_merchant_quarter"],
                                                  (int(5997 / 2.7), int(3350 / 2.7))),
                      "map_39": _sc(_preloaded_images.get("map_39", _preloaded_images["c_o_cult_funeris_encounter"]),
                                    (int(5997 / 3.3), int(3350 / 3.3))),
                      "l_i_inside_the_wall": _sc(_preloaded_images["l_i_inside_the_wall"],
                                                 (int(5997 / 6), int(3350 / 6))),
                      "l_o_inner_military_district": _sc(_preloaded_images["l_o_inner_military_district"],
                                                         (int(5997 / 2.3), int(3350 / 2.3))),
                      "l_i_barracks_hall": _sc(_preloaded_images["l_i_barracks_hall"], (int(5997 / 4), int(3350 / 4))),
                      "l_i_ship_lower_part": _sc(_preloaded_images["l_i_ship_lower_part"],
                                                 (int(5769 / 2.8), int(3350 / 2.8))),
                      "l_i_the_play_room": _sc(_preloaded_images["l_i_the_play_room"], (int(6375 / 4), int(2942 / 4))),
                      "l_i_the_ship": _sc(_preloaded_images["l_i_the_ship"], (int(6345 / 4), int(3350 / 4))),
                      "l_i_tutorial_ground": _sc(_preloaded_images["l_i_tutorial_ground"],
                                                 (int(6352 / 4), int(3350 / 4))),
                      "l_i_tutorial_ground_dlc": _sc(_preloaded_images["l_i_tutorial_ground_dlc"],
                                                     (int(6352 / 6), int(3350 / 6))),
                      "l_o_cathedral_plaza": _sc(_preloaded_images["l_o_cathedral_plaza"],
                                                 (int(6345 / 2.7), int(3350 / 2.7))),
                      "l_o_church_outpost": _sc(_preloaded_images["l_o_church_outpost"],
                                                (int(6352 / 3.7), int(3350 / 3.7))),
                      "l_o_corrupted_frontier": _sc(_preloaded_images["l_o_corrupted_frontier"],
                                                    (int(6345 / 2.2), int(3350 / 2.2))),
                      "l_o_harbor_district": _sc(_preloaded_images["l_o_harbor_district"],
                                                 (int(5876 / 2.2), int(3350 / 2.2))),
                      "l_o_home_village_center": _sc(_preloaded_images["l_o_home_village_center"],
                                                     (int(5876 / 4), int(3350 / 4))),
                      "l_o_home_village_entry": _sc(_preloaded_images["l_o_home_village_entry"],
                                                    (int(6375 / 2.7), int(3188 / 2.7))),
                      "l_o_rare_nexus_points": _sc(_preloaded_images["l_o_rare_nexus_points"],
                                                   (int(6345 / 1.5), int(3550 / 1.5))),
                      "l_o_the_old_orphanage": _sc(_preloaded_images["l_o_the_old_orphanage"],
                                                   (int(6375 / 3.4), int(3188 / 3.4))),
                      "t_i_escape_route": _sc(_preloaded_images["t_i_escape_route"],
                                              (int(6345 / 3.8), int(3350 / 3.8))),
                      "t_i_healing_hut": _sc(_preloaded_images["t_i_healing_hut"], (int(3863 / 4.8), int(3350 / 4.8))),
                      "t_i_storage_cave": _sc(_preloaded_images["t_i_storage_cave"],
                                              (int(6345 / 3.8), int(3350 / 3.8))),
                      "t_o_anomaly_forest": _sc(_preloaded_images["t_o_anomaly_forest"],
                                                (int(6375 / 3.8), int(2994 / 3.8))),
                      "t_o_tribe_perimeter": _sc(_preloaded_images["t_o_tribe_perimeter"],
                                                 (int(6375 / 4.3), int(3176 / 4.3))),
                      "t_o_tribe_settlement": _sc(_preloaded_images["t_o_tribe_settlement"],
                                                  (int(6375 / 2.8), int(3013 / 2.8))),
                      "t_o_tutorial_ground_shaman": _sc(_preloaded_images["t_o_tutorial_ground_shaman"],
                                                        (int(6352 / 6), int(3350 / 6))),
                      "c_i_cult_leader_fortress": _sc(_preloaded_images["c_i_cult_leader_fortress"],
                                                      (int(5997 / 3.2), int(3350 / 3.2))),
                      "c_i_inner_sanctum": _sc(_preloaded_images["c_i_inner_sanctum"],
                                               (int(5997 / 3.2), int(3350 / 3.2))),
                      "c_o_coastal_landing": _sc(_preloaded_images["c_o_coastal_landing"],
                                                 (int(5997 / 3.1), int(3350 / 3.1))),
                      "c_o_cult_funeris_encounter": _sc(_preloaded_images["c_o_cult_funeris_encounter"],
                                                        (int(5997 / 3.3), int(3350 / 3.3))),
                      "c_o_cult_village": _sc(_preloaded_images["c_o_cult_village"], (int(5997 / 2), int(3350 / 2))),
                      "c_o_cultist_battleground": _sc(_preloaded_images["c_o_cultist_battleground"],
                                                      (int(5997 / 3.7), int(3350 / 3.7))),
                      "c_o_lowms_cultist_battleground": _sc(_preloaded_images["c_o_lowms_cultist_battleground"],
                                                            (int(5997 / 3.7), int(3350 / 3.7))),
                      "l_i_theocratic_battleground_endingb": _sc(
                          _preloaded_images["l_i_theocratic_battleground_endingb"],
                          (int(5997 / 4), int(3350 / 4))),
                      "f_i_inside_chief_home": _sc(_preloaded_images["f_i_inside_chief_home"],
                                                   (int(5997 / 6), int(3350 / 6))),
                      "f_i_inside_elder_house": _sc(_preloaded_images["f_i_inside_elder_house"],
                                                    (int(5997 / 7), int(3350 / 7))),
                      "f_i_tunnel_passage_to_tribe": _sc(_preloaded_images["f_i_tunnel_passage_to_tribe"],
                                                         (int(5997 / 5), int(3350 / 5))),
                      "f_o_deep_terror_zone": _sc(_preloaded_images["f_o_deep_terror_zone"],
                                                  (int(5997 / 3.3), int(3350 / 3.3))),
                      "f_o_outside_chief_home": _sc(_preloaded_images["f_o_outside_chief_home"],
                                                    (int(5997 / 3.3), int(3350 / 3.3))),
                      "f_o_village_market": _sc(_preloaded_images["f_o_village_market"],
                                                (int(5997 / 3.3), int(3350 / 3.3))),
                      "f_o_residential_area": _sc(_preloaded_images["f_o_residential_area"],
                                                  (int(5997 / 3.3), int(3350 / 3.3))),
                      "l_o_destroy_theocracy": _sc(_preloaded_images["l_o_destroy_theocracy"],
                                                   (int(5997 / 2.7), int(3350 / 2.7))),
                      "l_i_orphanage_access": _sc(_preloaded_images["l_i_orphanage_access"],
                                                  (int(5997 / 4), int(3350 / 4))),
                      "l_i_active_laboratory_under_administrative_wing": _sc(
                          _preloaded_images["l_i_active_laboratory_under_administrative_wing"],
                          (int(5997 / 4), int(3350 / 4))),
                      "l_i_lab_office_under_administrative_wing": _sc(
                          _preloaded_images["l_i_lab_office_under_administrative_wing"],
                          (int(5997 / 4), int(3350 / 4))),
                      "l_i_old_laboratory": _sc(_preloaded_images["l_i_old_laboratory"],
                                                (int(5997 / 4), int(3350 / 4))),
                      "l_i_subterranean_labyrinth": _sc(_preloaded_images["l_i_subterranean_labyrinth"],
                                                        (int(5997 / 3.2), int(3350 / 3.2))),
                      "l_i_subterranean_labyrinth_exit": _sc(_preloaded_images["l_i_subterranean_labyrinth_exit"],
                                                             (int(5997 / 3.2), int(3350 / 3.2))),
                      "l_i_chief_home": _sc(_preloaded_images["l_i_chief_home"], (int(5997 / 7), int(3350 / 7))),
                      "l_i_church_administrative_wing": _sc(_preloaded_images["l_i_church_administrative_wing"],
                                                            (int(5997 / 5), int(3350 / 5))),
                      "l_i_church_chapel": _sc(_preloaded_images["l_i_church_chapel"],
                                               (int(5997 / 4.7), int(3350 / 4.7))),
                      "l_i_clearance_office": _sc(_preloaded_images["l_i_clearance_office"],
                                                  (int(2167 / 4.7), int(3350 / 4.7))),
                      "l_i_headmaster_office": _sc(_preloaded_images["l_i_headmaster_office"],
                                                   (int(5997 / 8), int(3350 / 8))),
                      "l_i_lumen_spy_merchant_guild": _sc(_preloaded_images["l_i_lumen_spy_merchant_guild"],
                                                          (int(5997 / 5.1), int(3350 / 5.1))),
                      "l_i_main_cathedral": _sc(_preloaded_images["l_i_main_cathedral"],
                                                (int(5997 / 4.5), int(3350 / 4.5))),
                      "l_i_merchant_bank": _sc(_preloaded_images["l_i_merchant_bank"],
                                               (int(5997 / 5.1), int(3350 / 5.1))),
                      "l_i_merchant_guild_hall": _sc(_preloaded_images["l_i_merchant_guild_hall"],
                                                     (int(5997 / 3.7), int(3350 / 3.7))),
                      "l_i_merchant_tavern": _sc(_preloaded_images["l_i_merchant_tavern"],
                                                 (int(5997 / 3.9), int(3350 / 3.9))),
                      "elucidate_mercenary_sprite_idle_1": _sc(_preloaded_images["elucidate_mercenary_sprite_idle_1"],
                                                               (72, 72)),
                      "elucidate_mercenary_sprite_idle_2": _sc(_preloaded_images["elucidate_mercenary_sprite_idle_2"],
                                                               (72, 72)),
                      "elucidate_mercenary_sprite_idle_3": _sc(_preloaded_images["elucidate_mercenary_sprite_idle_3"],
                                                               (72, 72)),
                      "elucidate_mercenary_sprite_idle_4": _sc(_preloaded_images["elucidate_mercenary_sprite_idle_4"],
                                                               (72, 72)), "elucidate_mercenary_sprite_walk_1_1": _sc(
            _preloaded_images["elucidate_mercenary_sprite_walk_1_1"], (72, 72)),
                      "elucidate_mercenary_sprite_walk_1_2": _sc(
                          _preloaded_images["elucidate_mercenary_sprite_walk_1_2"], (72, 72)),
                      "elucidate_mercenary_sprite_walk_2_1": _sc(
                          _preloaded_images["elucidate_mercenary_sprite_walk_2_1"], (72, 72)),
                      "elucidate_mercenary_sprite_walk_2_2": _sc(
                          _preloaded_images["elucidate_mercenary_sprite_walk_2_2"], (72, 72)),
                      "elucidate_mercenary_sprite_walk_3_1": _sc(
                          _preloaded_images["elucidate_mercenary_sprite_walk_3_1"], (72, 72)),
                      "elucidate_mercenary_sprite_walk_3_2": _sc(
                          _preloaded_images["elucidate_mercenary_sprite_walk_3_2"], (72, 72)),
                      "elucidate_mercenary_sprite_walk_4_1": _sc(
                          _preloaded_images["elucidate_mercenary_sprite_walk_4_1"], (72, 72)),
                      "elucidate_mercenary_sprite_walk_4_2": _sc(
                          _preloaded_images["elucidate_mercenary_sprite_walk_4_2"], (72, 72)),
                      "elucidate_mercenary_sprite_attack_1_1": _sc(
                          _preloaded_images["elucidate_mercenary_sprite_attack_1_1"], (72, 72)),
                      "elucidate_mercenary_sprite_attack_1_2": _sc(
                          _preloaded_images["elucidate_mercenary_sprite_attack_1_2"], (72, 72)),
                      "elucidate_mercenary_sprite_attack_2_1": _sc(
                          _preloaded_images["elucidate_mercenary_sprite_attack_2_1"], (72, 72)),
                      "elucidate_mercenary_sprite_attack_2_2": _sc(
                          _preloaded_images["elucidate_mercenary_sprite_attack_2_2"], (72, 72)),
                      "elucidate_mercenary_sprite_attack_3_1": _sc(
                          _preloaded_images["elucidate_mercenary_sprite_attack_3_1"], (72, 72)),
                      "elucidate_mercenary_sprite_attack_3_2": _sc(
                          _preloaded_images["elucidate_mercenary_sprite_attack_3_2"], (72, 72)),
                      "elucidate_mercenary_sprite_attack_4_1": _sc(
                          _preloaded_images["elucidate_mercenary_sprite_attack_4_1"], (72, 72)),
                      "elucidate_mercenary_sprite_attack_4_2": _sc(
                          _preloaded_images["elucidate_mercenary_sprite_attack_4_2"], (72, 72)),
                      "elucidate_middle_gradient_001": _sc(_preloaded_images["elucidate_middle_gradient_001"],
                                                           (200, 30)),
                      "elucidate_middle_gradient_002": _sc(_preloaded_images["elucidate_middle_gradient_001"],
                                                           (300, 30)),
                      "elucidate_title_full": _sc(_preloaded_images["elucidate_full_text_portait_001"], (1275, 710)),
                      "elucidate_title_1": _sc(_preloaded_images["elucidate_full_text_portait_001"],
                                               (screen_x // 2, screen_y // 2)),
                      "elucidate_select_load": _sc(_preloaded_images["elucidate_middle_gradient_001"],
                                                   (screen_x // 2, 30)),
                      "elucidate_select_home": _sc(_preloaded_images["elucidate_select"], (250, 35)),
                      "elucidate_select_inv": _sc(_preloaded_images["elucidate_select"], (280, 35)),
                      "elucidate_select_exit": _sc(_preloaded_images["elucidate_middle_gradient_001"], (200, 30)),
                      "elucidate_select_ui_002_play_select": _sc(_preloaded_images["elucidate_select_ui_002"],
                                                                 (500, 300)),
                      "elucidate_mcguy_001_999": _sc(_preloaded_images["elucidate_mcguy_001"], (300, 500)),
                      "elucidate_select_home_1": _sc(_preloaded_images["elucidate_select"], (250, 30)),
                      "elucidate_no_sprite_idle_1": _sc(_preloaded_images["elucidate_no_sprite_idle_1"], (72, 72)),
                      "elucidate_no_sprite_idle_2": _sc(_preloaded_images["elucidate_no_sprite_idle_2"], (72, 72)),
                      "elucidate_no_sprite_idle_3": _sc(_preloaded_images["elucidate_no_sprite_idle_3"], (72, 72)),
                      "elucidate_no_sprite_idle_4": _sc(_preloaded_images["elucidate_no_sprite_idle_4"], (72, 72)),
                      "elucidate_no_sprite_walk_1_1": _sc(_preloaded_images["elucidate_no_sprite_walk_1_1"], (72, 72)),
                      "elucidate_no_sprite_walk_1_2": _sc(_preloaded_images["elucidate_no_sprite_walk_1_2"], (72, 72)),
                      "elucidate_no_sprite_walk_2_1": _sc(_preloaded_images["elucidate_no_sprite_walk_2_1"], (72, 72)),
                      "elucidate_no_sprite_walk_2_2": _sc(_preloaded_images["elucidate_no_sprite_walk_2_2"], (72, 72)),
                      "elucidate_no_sprite_walk_3_1": _sc(_preloaded_images["elucidate_no_sprite_walk_3_1"], (72, 72)),
                      "elucidate_no_sprite_walk_3_2": _sc(_preloaded_images["elucidate_no_sprite_walk_3_2"], (72, 72)),
                      "elucidate_no_sprite_walk_4_1": _sc(_preloaded_images["elucidate_no_sprite_walk_4_1"], (72, 72)),
                      "elucidate_no_sprite_walk_4_2": _sc(_preloaded_images["elucidate_no_sprite_walk_4_2"], (72, 72)),
                      "elucidate_no_sprite_attack_1_1": _sc(_preloaded_images["elucidate_no_sprite_attack_1_1"],
                                                            (72, 72)),
                      "elucidate_no_sprite_attack_1_2": _sc(_preloaded_images["elucidate_no_sprite_attack_1_2"],
                                                            (72, 72)),
                      "elucidate_no_sprite_attack_2_1": _sc(_preloaded_images["elucidate_no_sprite_attack_2_1"],
                                                            (72, 72)),
                      "elucidate_no_sprite_attack_2_2": _sc(_preloaded_images["elucidate_no_sprite_attack_2_2"],
                                                            (72, 72)),
                      "elucidate_no_sprite_attack_3_1": _sc(_preloaded_images["elucidate_no_sprite_attack_3_1"],
                                                            (72, 72)),
                      "elucidate_no_sprite_attack_3_2": _sc(_preloaded_images["elucidate_no_sprite_attack_3_2"],
                                                            (72, 72)),
                      "elucidate_no_sprite_attack_4_1": _sc(_preloaded_images["elucidate_no_sprite_attack_4_1"],
                                                            (72, 72)),
                      "elucidate_no_sprite_attack_4_2": _sc(_preloaded_images["elucidate_no_sprite_attack_4_2"],
                                                            (72, 72)),
                      "elucidate_dungeon_area_001": _sc(_preloaded_images["elucidate_dungeon_area_001"], (1275, 710)),
                      "elucidate_dungeon_area_002": _sc(_preloaded_images["elucidate_dungeon_area_002"], (1275, 710)),
                      "elucidate_npc_test_no_sprite": _sc(_preloaded_images["elucidate_no_texture"], (72, 72)),
                      "materials_special_small_caligo_fragment_tribe": _sc(
                          _preloaded_images["materials_special_small_caligo_fragment_tribe"], (72, 72)),
                      "materials_special_small_caligo_fragment_port": _sc(
                          _preloaded_images["materials_special_small_caligo_fragment_port"], (72, 72)),
                      "materials_special_big_caligo_fragmrnt": _sc(
                          _preloaded_images["materials_special_big_caligo_fragmrnt"], (48, 48)),
                      "weapon_1handed_short_sword": _sc(_preloaded_images["weapon_1handed_short_sword"], (48, 48)),
                      "weapon_1handed_cleaver": _sc(_preloaded_images["weapon_1handed_cleaver"], (48, 48)),
                      "weapon_1handed_knife": _sc(_preloaded_images["weapon_1handed_knife"], (48, 48)),
                      "materials_sheet_ancient_paper": _sc(_preloaded_images["user_item_ancient_paper"],
                                                           (38, 38)),
                      "armour_headware_iron_mask": _sc(_preloaded_images["armour_headware_iron_mask"], (48, 48)),
                      "armour_body_armour_dark_priests_robe": _sc(
                          _preloaded_images["armour_body_armour_dark_priests_robe"], (48, 48)),
                      "armour_body_armour_priests_robe": _sc(_preloaded_images["armour_body_armour_priests_robe"],
                                                             (48, 48)),
                      "armour_headware_plate_helmet": _sc(_preloaded_images["armour_headware_plate_helmet"], (48, 48)),
                      "armour_headware_padded_cap": _sc(_preloaded_images["armour_headware_padded_cap"], (48, 48)),
                      "armour_body_armour_iron_cuirass": _sc(_preloaded_images["armour_body_armour_iron_cuirass"],
                                                             (48, 48)),
                      "armour_body_armour_loincloth": _sc(_preloaded_images["armour_body_armour_loincloth"], (48, 48)),
                      "armour_accessories_red_scarf": _sc(_preloaded_images["armour_accessories_red_scarf"], (48, 48)),
                      "armour_headware_iron_helmet": _sc(_preloaded_images["armour_headware_iron_helmet"], (48, 48)),
                      "armour_headware_guard_bascinet": _sc(_preloaded_images["armour_headware_guard_bascinet"],
                                                            (48, 48)),
                      "armour_headware_guard_coif": _sc(_preloaded_images["armour_headware_guard_coif"], (48, 48)),
                      "armour_headware_chainmail_hood": _sc(_preloaded_images["armour_headware_chainmail_hood"],
                                                            (48, 48)),
                      "armour_body_armour_black_dress": _sc(_preloaded_images["armour_body_armour_black_dress"],
                                                            (48, 48)),
                      "armour_body_armour_trench_coat": _sc(_preloaded_images["armour_body_armour_trench_coat"],
                                                            (48, 48)),
                      "weapon_1handed_corsairs_saber": _sc(_preloaded_images["weapon_1handed_corsairs_saber"],
                                                           (48, 48)),
                      "weapon_1handed_cloth_hood": _sc(_preloaded_images["weapon_1handed_cloth_hood"], (48, 48)),
                      "armour_body_armour_leather_coat": _sc(_preloaded_images["armour_body_armour_leather_coat"],
                                                             (48, 48)),
                      "armour_body_armour_leather_jvest": _sc(_preloaded_images["armour_body_armour_leather_jvest"],
                                                              (48, 48)),
                      "armour_body_armour_plated_mail": _sc(_preloaded_images["armour_body_armour_plated_mail"],
                                                            (48, 48)),
                      "armour_shield_scutum": _sc(_preloaded_images["armour_shield_scutum"], (48, 48)),
                      "weapon_longrange_musket": _sc(_preloaded_images["weapon_longrange_musket"], (48, 48)),
                      "weapon_2handed_spear": _sc(_preloaded_images["weapon_2handed_spear"], (48, 48)),
                      "armour_body_armour_hard_leather_armor": _sc(
                          _preloaded_images["armour_body_armour_hard_leather_armor"], (48, 48)),
                      "armour_body_armour_iron_plate": _sc(_preloaded_images["armour_body_armour_iron_plate"],
                                                           (48, 48)),
                      "weapon_1handed_stiletto": _sc(_preloaded_images["weapon_1handed_stiletto"], (48, 48)),
                      "armour_armwear_arm_guard": _sc(_preloaded_images["user_item_arm_guard"], (48, 48)),
                      "weapon_1handed_iron_axe": _sc(_preloaded_images["weapon_1handed_iron_axe"], (48, 48)),
                      "weapon_longrange_short_bow": _sc(_preloaded_images["weapon_longrange_short_bow"], (48, 48)),
                      "materials_scrap_leather_scraps": _sc(_preloaded_images["user_item_leather_scraps"],
                                                            (48, 48)),
                      "materials_skill_book_of_rapid_fire": _sc(_preloaded_images["user_item_book_of_rapid_fire"],
                                                                (72, 72)),
                      "materials_skill_book_of_instincts": _sc(_preloaded_images["user_item_book_of_instincts"],
                                                               (72, 72)),
                      "armour_accessories_swift_boots": _sc(_preloaded_images["armour_accessories_swift_boots"],
                                                            (48, 48)),
                      "weapon_longrange_heavy_crossbow": _sc(_preloaded_images["weapon_longrange_heavy_crossbow"],
                                                             (48, 48)),
                      "weapon_longrange_longbow": _sc(_preloaded_images["weapon_longrange_longbow"], (48, 48)),
                      "weapon_2handed_maul": _sc(_preloaded_images["weapon_2handed_maul"], (48, 48)),
                      "weapon_2handed_claymore": _sc(_preloaded_images["weapon_2handed_claymore"], (48, 48)),
                      "weapon_1handed_scimitar": _sc(_preloaded_images["weapon_1handed_scimitar"], (48, 48)),
                      "weapon_1handed_improvised_shiv": _sc(_preloaded_images["weapon_1handed_improvised_shiv"],
                                                            (48, 48)),
                      "weapon_1handed_steel_hammer": _sc(_preloaded_images["weapon_1handed_steel_hammer"], (48, 48)),
                      "material_toy_black_dressed_doll": _sc(_preloaded_images["material_toy_black_dressed_doll"],
                                                             (48, 48)),
                      "weapon_1handed_dirk": _sc(_preloaded_images["weapon_1handed_dirk"], (48, 48)),
                      "materials_plank_wooden_plank": _sc(_preloaded_images["user_item_wooden_plank"], (48, 48)),
                      "weapon_1handed_dagger": _sc(_preloaded_images["weapon_1handed_dagger"], (48, 48)),
                      "materials_component_silver_wire": _sc(_preloaded_images["user_item_silver_wire"],
                                                             (48, 48)),
                      "armour_accessories_red_amulet": _sc(_preloaded_images["user_item_red_amulet"],
                                                           (48, 48)),
                      "materials_special_wind_essence": _sc(_preloaded_images["armour_accessories_blue_amulet"],
                                                            (48, 48)),
                      "materials_component_stick": _sc(_preloaded_images["user_item_stick"], (48, 48)),
                      "armour_accessories_ring": _sc(_preloaded_images["user_item_ring"], (48, 48)),
                      "materials_skill_book_of_marksmanship": _sc(
                          _preloaded_images["user_item_book_of_marksmanship"], (72, 72)),
                      "materials_skill_book_of_stars": _sc(_preloaded_images["user_item_book_of_stars"],
                                                           (72, 72)),
                      "materials_skill_book_of_crafsmanship": _sc(_preloaded_images["user_item_book_of_crafsmanship"], (72, 72)),
                      "materials_skill_book_of_agility": _sc(_preloaded_images["user_item_book_of_agility"], (72, 72)),
                      "materials_skill_book_of_healing": _sc(_preloaded_images["user_item_book_of_healing"], (72, 72)),
                      "materials_skill_book_of_the_secrets": _sc(_preloaded_images["user_item_book_of_the_secrets"], (72, 72)),
                      "materials_save_book_of_enlightenment": _sc(_preloaded_images["user_item_book_of_enlightenment"], (72, 72)),
                      "materials_skill_book_of_cowardice_i": _sc(_preloaded_images["user_item_book_of_cowardice_i"], (72, 72)),
                      "materials_skill_book_of_cowardice_ii": _sc(_preloaded_images["user_item_book_of_cowardice_ii"], (72, 72)),
                      "materials_skill_book_of_pestilence_i": _sc(_preloaded_images["user_item_book_of_pestilence_i"], (72, 72)),
                      "materials_skill_book_of_pestilence_ii": _sc(_preloaded_images["user_item_book_of_pestilence_ii"], (72, 72)),
                      "materials_skill_book_of_pestilence_iii": _sc(_preloaded_images["user_item_book_of_pestilence_iii"], (72, 72)),
                      "materials_skill_book_of_pestilence_iv": _sc(_preloaded_images["user_item_book_of_pestilence_iv"], (72, 72)),
                      "materials_skill_book_of_pestilence_v": _sc(_preloaded_images["user_item_book_of_pestilence_v"], (72, 72)),
                      "materials_skill_book_of_pestilence_vi": _sc(_preloaded_images["user_item_book_of_pestilence_vi"], (72, 72)),
                      "materials_skill_book_of_pestilence_vii": _sc(_preloaded_images["user_item_book_of_pestilence_vii"], (72, 72)),
                      "materials_skill_book_of_pestilence_viii": _sc(_preloaded_images["user_item_book_of_pestilence_viii"], (72, 72)),
                      "materials_skill_book_of_trade_i": _sc(_preloaded_images["user_item_book_of_trade_i"], (72, 72)),
                      "materials_skill_book_of_trade_ii": _sc(_preloaded_images["user_item_book_of_trade_ii"], (72, 72)),
                      "materials_skill_book_of_trade_iii": _sc(_preloaded_images["user_item_book_of_trade_iii"], (72, 72)),
                      "materials_gem_red_gem": _sc(_preloaded_images["user_item_red_gem"], (48, 48)),
                      "materials_gem_blue_gem": _sc(_preloaded_images["user_item_blue_gem"], (48, 48)),
                      "materials_beverage_ale": _sc(_preloaded_images["user_item_ale"], (48, 48)),
                      "materials_beverage_wine": _sc(_preloaded_images["user_item_wine"], (48, 48)),
                      "materials_beverage_rum": _sc(_preloaded_images["user_item_rum"], (48, 48)),
                      "materials_bar_iron_ingot": _sc(_preloaded_images["user_item_iron_ingot"], (48, 48)),
                      "materials_ore_raw_iron": _sc(_preloaded_images["user_item_raw_iron"], (48, 48)),
                      "materials_foliage_blue_herb-1": _sc(_preloaded_images["user_item_blue_herb"], (48, 48)),
                      "materials_foliage_green_herb": _sc(_preloaded_images["user_item_green_herb"], (48, 48)),
                      "materials_sheet_paper": _sc(_preloaded_images["user_item_paper"], (48, 48)),
                      "materials_potion_antibiotics": _sc(_preloaded_images["user_item_antibiotics"], (48, 48)),
                      "materials_potion_betadine": _sc(_preloaded_images["user_item_betadine"], (48, 48)),
                      "materials_potion_red_vial": _sc(_preloaded_images["user_item_red_vial"], (48, 48)),
                      "materials_container_empty_vial": _sc(_preloaded_images["user_item_empty_vial"], (48, 48)),
                      "weapon_2handed_longsword": _sc(_preloaded_images["weapon_2handed_longsword"], (72, 72)),
                      "armour_shield_wooden_buckler": _sc(_preloaded_images["armour_shield_wooden_buckler"], (72, 72)),
                      "weapon_1handed_cultist_dagger": _sc(_preloaded_images["weapon_1handed_cultist_dagger"],
                                                           (72, 72)),
                      "weapon_longrange_flintlock": _sc(_preloaded_images["weapon_longrange_flintlock"], (72, 72)),
                      "weapon_2handed_makeshift_spear": _sc(_preloaded_images["weapon_2handed_makeshift_spear"],
                                                            (72, 72)),
                      "weapon_longrange_blunderbuss": _sc(_preloaded_images["weapon_longrange_blunderbuss"], (72, 72)),
                      "weapon_1handed_shaman_dagger": _sc(_preloaded_images["weapon_1handed_shaman_dagger"], (72, 72)),
                      "weapon_2handed_priest_staff": _sc(_preloaded_images["weapon_2handed_priest_staff"], (72, 72)),
                      "weapon_longrange_cultist_crossbow": _sc(_preloaded_images["weapon_longrange_cultist_crossbow"],
                                                               (72, 72)),
                      "materials_component_bow_string": _sc(_preloaded_images["materials_component_bow_string"],
                                                            (72, 72)),
                      "elucidate_silver_chest_closed_001": _sc(_preloaded_images["silver_chest_closed"], (48, 48)),
                      "elucidate_silver_chest_opened_002": _sc(_preloaded_images["silver_chest_opened"], (48, 48)),
                      "elucidate_gold_chest_closed_003": _sc(_preloaded_images["gold_chest_closed"], (48, 48)),
                      "elucidate_gold_chest_opened_004": _sc(_preloaded_images["gold_chest_opened"], (48, 48)),
                      "elucidate_idle_cult_leader_npc_down": _sc(_preloaded_images["idle_cult_leader_npc_down"],
                                                                 (72, 72)),
                      "elucidate_idle_cult_leader_npc_up": _sc(_preloaded_images["idle_cult_leader_npc_up"], (72, 72)),
                      "elucidate_idle_cult_leader_npc_left": _sc(_preloaded_images["idle_cult_leader_npc_left"],
                                                                 (72, 72)),
                      "elucidate_idle_cult_leader_npc_right": _sc(_preloaded_images["idle_cult_leader_npc_right"],
                                                                  (72, 72)),
                      "elucidate_idle_cultist_soldier_npc_up": _sc(_preloaded_images["idle_cultist_soldier_npc_up"],
                                                                   (72, 72)),
                      "elucidate_idle_cultist_soldier_npc_right": _sc(
                          _preloaded_images["idle_cultist_soldier_npc_right"], (72, 72)),
                      "elucidate_idle_cultist_soldier_npc_left": _sc(_preloaded_images["idle_cultist_soldier_npc_left"],
                                                                     (72, 72)),
                      "elucidate_idle_cultist_soldier_npc_down": _sc(_preloaded_images["idle_cultist_soldier_npc_down"],
                                                                     (72, 72)),
                      "elucidate_idle_corrupted1_cultist_npc_right": _sc(
                          _preloaded_images["idle_corrupted1_cultist_npc_right"], (72, 72)),
                      "elucidate_idle_corrupted1_cultist_npc_left": _sc(
                          _preloaded_images["idle_corrupted1_cultist_npc_left"], (72, 72)),
                      "elucidate_idle_corrupted1_cultist_npc_down": _sc(
                          _preloaded_images["idle_corrupted1_cultist_npc_down"], (72, 72)),
                      "elucidate_idle_corrupted1_cultist_npc_up": _sc(
                          _preloaded_images["idle_corrupted1_cultist_npc_up"], (72, 72)),
                      "elucidate_idle_amalgamated_villagers_npc_right": _sc(
                          _preloaded_images["idle_amalgamated_villagers_npc_right"], (72, 72)),
                      "elucidate_idle_amalgamated_villagers_npc_left": _sc(
                          _preloaded_images["idle_amalgamated_villagers_npc_left"], (72, 72)),
                      "elucidate_idle_amalgamated_knights_npc_right": _sc(
                          _preloaded_images["idle_amalgamated_knights_npc_right"], (72, 72)),
                      "elucidate_idle_amalgamated_knights_npc_left": _sc(
                          _preloaded_images["idle_amalgamated_knights_npc_left"], (72, 72)),
                      "elucidate_idle_amalgamated_civillians_npc_right": _sc(
                          _preloaded_images["idle_amalgamated_civillians_npc_right"], (72, 72)),
                      "elucidate_idle_amalgamated_civillians_npc_left": _sc(
                          _preloaded_images["idle_amalgamated_civillians_npc_left"], (72, 72)),
                      "elucidate_idle_melted_male_villager_npc_right": _sc(
                          _preloaded_images["idle_melted_male_villager_npc_right"], (72, 72)),
                      "elucidate_idle_melted_male_villager_npc_left": _sc(
                          _preloaded_images["idle_melted_male_villager_npc_left"], (72, 72)),
                      "elucidate_idle_melted_male_villager_npc_up": _sc(
                          _preloaded_images["idle_melted_male_villager_npc_up"], (72, 72)),
                      "elucidate_idle_melted_male_villager_npc_down": _sc(
                          _preloaded_images["idle_melted_male_villager_npc_down"], (72, 72)),
                      "elucidate_idle_melted_female_villager_npc_up": _sc(
                          _preloaded_images["idle_melted_female_villager_npc_up"], (72, 72)),
                      "elucidate_idle_melted_female_villager_npc_right": _sc(
                          _preloaded_images["idle_melted_female_villager_npc_right"], (72, 72)),
                      "elucidate_idle_melted_female_villager_npc_left": _sc(
                          _preloaded_images["idle_melted_female_villager_npc_left"], (72, 72)),
                      "elucidate_idle_melted_female_villager_npc_down": _sc(
                          _preloaded_images["idle_melted_female_villager_npc_down"], (72, 72)),
                      "elucidate_idle_corrupted3_cultist_npc_up": _sc(
                          _preloaded_images["idle_corrupted3_cultist_npc_up"], (72, 72)),
                      "elucidate_idle_corrupted3_cultist_npc_right": _sc(
                          _preloaded_images["idle_corrupted3_cultist_npc_right"], (72, 72)),
                      "elucidate_idle_corrupted3_cultist_npc_left": _sc(
                          _preloaded_images["idle_corrupted3_cultist_npc_left"], (72, 72)),
                      "elucidate_idle_corrupted3_cultist_npc_down": _sc(
                          _preloaded_images["idle_corrupted3_cultist_npc_down"], (72, 72)),
                      "elucidate_idle_corrupted2_cultist_npc_up": _sc(
                          _preloaded_images["idle_corrupted2_cultist_npc_up"], (72, 72)),
                      "elucidate_idle_corrupted2_cultist_npc_right": _sc(
                          _preloaded_images["idle_corrupted2_cultist_npc_right"], (72, 72)),
                      "elucidate_idle_corrupted2_cultist_npc_left": _sc(
                          _preloaded_images["idle_corrupted2_cultist_npc_left"], (72, 72)),
                      "elucidate_idle_corrupted2_cultist_npc_down": _sc(
                          _preloaded_images["idle_corrupted2_cultist_npc_down"], (72, 72)),
                      "elucidate_idle_librarian_scholar_npc_up": _sc(_preloaded_images["idle_librarian_scholar_npc_up"],
                                                                     (72, 72)),
                      "elucidate_idle_librarian_scholar_npc_right": _sc(
                          _preloaded_images["idle_librarian_scholar_npc_right"], (72, 72)),
                      "elucidate_idle_librarian_scholar_npc_left": _sc(
                          _preloaded_images["idle_librarian_scholar_npc_left"], (72, 72)),
                      "elucidate_idle_librarian_scholar_npc_down": _sc(
                          _preloaded_images["idle_librarian_scholar_npc_down"], (72, 72)),
                      "elucidate_idle_holyknight_npc_up": _sc(_preloaded_images["idle_holyknight_npc_up"], (72, 72)),
                      "elucidate_idle_holyknight_npc_right": _sc(_preloaded_images["idle_holyknight_npc_right"],
                                                                 (72, 72)),
                      "elucidate_idle_holyknight_npc_left": _sc(_preloaded_images["idle_holyknight_npc_left"],
                                                                (72, 72)),
                      "elucidate_idle_holyknight_npc_down": _sc(_preloaded_images["idle_holyknight_npc_down"],
                                                                (72, 72)),
                      "elucidate_idle_male_faithful_citizen_npc_up": _sc(
                          _preloaded_images["idle_male_faithful_citizen_npc_up"], (72, 72)),
                      "elucidate_idle_male_faithful_citizen_npc_right": _sc(
                          _preloaded_images["idle_male_faithful_citizen_npc_right"], (72, 72)),
                      "elucidate_idle_male_faithful_citizen_npc_left": _sc(
                          _preloaded_images["idle_male_faithful_citizen_npc_left"], (72, 72)),
                      "elucidate_idle_male_faithful_citizen_npc_down": _sc(
                          _preloaded_images["idle_male_faithful_citizen_npc_down"], (72, 72)),
                      "elucidate_idle_female_faithful_citizen_npc_up": _sc(
                          _preloaded_images["idle_female_faithful_citizen_npc_up"], (72, 72)),
                      "elucidate_idle_female_faithful_citizen_npc_right": _sc(
                          _preloaded_images["idle_female_faithful_citizen_npc_right"], (72, 72)),
                      "elucidate_idle_female_faithful_citizen_npc_left": _sc(
                          _preloaded_images["idle_female_faithful_citizen_npc_left"], (72, 72)),
                      "elucidate_idle_female_faithful_citizen_npc_down": _sc(
                          _preloaded_images["idle_female_faithful_citizen_npc_down"], (72, 72)),
                      "elucidate_idle_sprite_chuAttendants_up": _sc(_preloaded_images["idle_sprite_chuAttendants_up"],
                                                                    (72, 72)),
                      "elucidate_idle_sprite_chuAttendants_right": _sc(
                          _preloaded_images["idle_sprite_chuAttendants_right"], (72, 72)),
                      "elucidate_idle_sprite_chuAttendants_left": _sc(
                          _preloaded_images["idle_sprite_chuAttendants_left"], (72, 72)),
                      "elucidate_idle_sprite_chuAttendants_down": _sc(
                          _preloaded_images["idle_sprite_chuAttendants_down"], (72, 72)),
                      "elucidate_idle_assassin_npc_up": _sc(_preloaded_images["idle_assassin_npc_up"], (72, 72)),
                      "elucidate_idle_assassin_npc_right": _sc(_preloaded_images["idle_assassin_npc_right"], (72, 72)),
                      "elucidate_idle_assassin_npc_left": _sc(_preloaded_images["idle_assassin_npc_left"], (72, 72)),
                      "elucidate_idle_assassin_npc_down": _sc(_preloaded_images["idle_assassin_npc_down"], (72, 72)),
                      "elucidate_idle_tribe_warrior_npc_up": _sc(_preloaded_images["idle_tribe_warrior_npc_up"],
                                                                 (72, 72)),
                      "elucidate_idle_tribe_warrior_npc_right": _sc(_preloaded_images["idle_tribe_warrior_npc_right"],
                                                                    (72, 72)),
                      "elucidate_idle_tribe_warrior_npc_left": _sc(_preloaded_images["idle_tribe_warrior_npc_left"],
                                                                   (72, 72)),
                      "elucidate_idle_tribe_warrior_npc_down": _sc(_preloaded_images["idle_tribe_warrior_npc_down"],
                                                                   (72, 72)),
                      "elucidate_idle_tribe_elder_npc_up": _sc(_preloaded_images["idle_tribe_elder_npc_up"], (72, 72)),
                      "elucidate_idle_tribe_elder_npc_right": _sc(_preloaded_images["idle_tribe_elder_npc_right"],
                                                                  (72, 72)),
                      "elucidate_idle_tribe_elder_npc_left": _sc(_preloaded_images["idle_tribe_elder_npc_left"],
                                                                 (72, 72)),
                      "elucidate_idle_tribe_elder_npc_down": _sc(_preloaded_images["idle_tribe_elder_npc_down"],
                                                                 (72, 72)),
                      "elucidate_idle_tribe_chief_npc_up": _sc(_preloaded_images["idle_tribe_chief_npc_up"], (72, 72)),
                      "elucidate_idle_tribe_chief_npc_right": _sc(_preloaded_images["idle_tribe_chief_npc_right"],
                                                                  (72, 72)),
                      "elucidate_idle_tribe_chief_npc_left": _sc(_preloaded_images["idle_tribe_chief_npc_left"],
                                                                 (72, 72)),
                      "elucidate_idle_tribe_chief_npc_down": _sc(_preloaded_images["idle_tribe_chief_npc_down"],
                                                                 (72, 72)),
                      "elucidate_idle_supply_merchant_npc_down": _sc(_preloaded_images["idle_supply_merchant_npc_down"],
                                                                     (72, 72)),
                      "elucidate_idle_supply_merchant_npc_up": _sc(_preloaded_images["idle_supply_merchant_npc_up"],
                                                                   (72, 72)),
                      "elucidate_idle_supply_merchant_npc_right": _sc(
                          _preloaded_images["idle_supply_merchant_npc_right"], (72, 72)),
                      "elucidate_idle_supply_merchant_npc_left": _sc(_preloaded_images["idle_supply_merchant_npc_left"],
                                                                     (72, 72)),
                      "elucidate_idle_merchant_guild_npc_up": _sc(
                          _preloaded_images["idle_merchant_guild_member_npc_up"], (72, 72)),
                      "elucidate_idle_merchant_guild_npc_right": _sc(
                          _preloaded_images["idle_merchant_guild_member_npc_right"], (72, 72)),
                      "elucidate_idle_merchant_guild_npc_left": _sc(
                          _preloaded_images["idle_merchant_guild_member_npc_left"], (72, 72)),
                      "elucidate_idle_merchant_guild_npc_down": _sc(
                          _preloaded_images["idle_merchant_guild_member_npc_down"], (72, 72)),
                      "elucidate_idle_merchant_guild_master_npc_up": _sc(
                          _preloaded_images["idle_merchant_guild_master_npc_up"], (72, 72)),
                      "elucidate_idle_merchant_guild_master_npc_right": _sc(
                          _preloaded_images["idle_merchant_guild_master_npc_right"], (72, 72)),
                      "elucidate_idle_merchant_guild_master_npc_left": _sc(
                          _preloaded_images["idle_merchant_guild_master_npc_left"], (72, 72)),
                      "elucidate_idle_merchant_guild_master_npc_down": _sc(
                          _preloaded_images["idle_merchant_guild_master_npc_down"], (72, 72)),
                      "elucidate_idle_harbor_captain_npc_up": _sc(_preloaded_images["idle_harbor_captain_npc_up"],
                                                                  (72, 72)),
                      "elucidate_idle_harbor_captain_npc_right": _sc(_preloaded_images["idle_harbor_captain_npc_right"],
                                                                     (72, 72)),
                      "elucidate_idle_harbor_captain_npc_left": _sc(_preloaded_images["idle_harbor_captain_npc_left"],
                                                                    (72, 72)),
                      "elucidate_idle_harbor_captain_npc_down": _sc(_preloaded_images["idle_harbor_captain_npc_down"],
                                                                    (72, 72)),
                      "elucidate_idle_male_villager_variant_npc_up": _sc(
                          _preloaded_images["idle_male_villager_variant_npc_up"], (72, 72)),
                      "elucidate_idle_male_villager_variant_npc_right": _sc(
                          _preloaded_images["idle_male_villager_variant_npc_right"], (72, 72)),
                      "elucidate_idle_male_villager_variant_npc_left": _sc(
                          _preloaded_images["idle_male_villager_variant_npc_left"], (72, 72)),
                      "elucidate_idle_male_villager_variant_npc_down": _sc(
                          _preloaded_images["idle_male_villager_variant_npc_down"], (72, 72)),
                      "elucidate_idle_male_villager_npc_up": _sc(_preloaded_images["idle_male_villager_npc_up"],
                                                                 (72, 72)),
                      "elucidate_idle_male_villager_npc_right": _sc(_preloaded_images["idle_male_villager_npc_right"],
                                                                    (72, 72)),
                      "elucidate_idle_male_villager_npc_left": _sc(_preloaded_images["idle_male_villager_npc_left"],
                                                                   (72, 72)),
                      "elucidate_idle_male_villager_npc_down": _sc(_preloaded_images["idle_male_villager_npc_down"],
                                                                   (72, 72)),
                      "elucidate_idle_female_villager_variant_npc_up": _sc(
                          _preloaded_images["idle_female_villager_variant_npc_up"], (72, 72)),
                      "elucidate_idle_female_villager_variant_npc_right": _sc(
                          _preloaded_images["idle_female_villager_variant_npc_right"], (72, 72)),
                      "elucidate_idle_female_villager_variant_npc_left": _sc(
                          _preloaded_images["idle_female_villager_variant_npc_left"], (72, 72)),
                      "elucidate_idle_female_villager_variant_npc_down": _sc(
                          _preloaded_images["idle_female_villager_variant_npc_down"], (72, 72)),
                      "elucidate_idle_female_villager_npc_up": _sc(_preloaded_images["idle_female_villager_npc_up"],
                                                                   (72, 72)),
                      "elucidate_idle_female_villager_npc_right": _sc(
                          _preloaded_images["idle_female_villager_npc_right"], (72, 72)),
                      "elucidate_idle_female_villager_npc_left": _sc(_preloaded_images["idle_female_villager_npc_left"],
                                                                     (72, 72)),
                      "elucidate_idle_female_villager_npc_down": _sc(_preloaded_images["idle_female_villager_npc_down"],
                                                                     (72, 72)),
                      "elucidate_idle_guards_npc_up": _sc(_preloaded_images["idle_guards_npc_up"], (72, 72)),
                      "elucidate_idle_guards_npc_right": _sc(_preloaded_images["idle_guards_npc_right"], (72, 72)),
                      "elucidate_idle_guards_npc_left": _sc(_preloaded_images["idle_guards_npc_left"], (72, 72)),
                      "elucidate_idle_guards_npc_down": _sc(_preloaded_images["idle_guards_npc_down"], (72, 72)),
                      "elucidate_idle_guard_captain_npc_up": _sc(_preloaded_images["idle_guard_captain_npc_up"],
                                                                 (72, 72)),
                      "elucidate_idle_guard_captain_npc_right": _sc(_preloaded_images["idle_guard_captain_npc_right"],
                                                                    (72, 72)),
                      "elucidate_idle_guard_captain_npc_left": _sc(_preloaded_images["idle_guard_captain_npc_left"],
                                                                   (72, 72)),
                      "elucidate_idle_guard_captain_npc_down": _sc(_preloaded_images["idle_guard_captain_npc_down"],
                                                                   (72, 72)),
                      "elucidate_idle_draft_officer_npc_up": _sc(_preloaded_images["idle_draft_officer_npc_up"],
                                                                 (72, 72)),
                      "elucidate_idle_draft_officer_npc_right": _sc(_preloaded_images["idle_draft_officer_npc_right"],
                                                                    (72, 72)),
                      "elucidate_idle_draft_officer_npc_left": _sc(_preloaded_images["idle_draft_officer_npc_left"],
                                                                   (72, 72)),
                      "elucidate_idle_draft_officer_npc_down": _sc(_preloaded_images["idle_draft_officer_npc_down"],
                                                                   (72, 72)),
                      "elucidate_idle_male_civilian_npc_up": _sc(_preloaded_images["idle_male_civilian_npc_up"],
                                                                 (72, 72)),
                      "elucidate_idle_male_civilian_npc_right": _sc(_preloaded_images["idle_male_civilian_npc_right"],
                                                                    (72, 72)),
                      "elucidate_idle_male_civilian_npc_left": _sc(_preloaded_images["idle_male_civilian_npc_left"],
                                                                   (72, 72)),
                      "elucidate_idle_male_civilian_npc_down": _sc(_preloaded_images["idle_male_civilian_npc_down"],
                                                                   (72, 72)),
                      "elucidate_idle_female_civilian_npc_up": _sc(_preloaded_images["idle_female_civilian_npc_up"],
                                                                   (72, 72)),
                      "elucidate_idle_female_civilian_npc_right": _sc(
                          _preloaded_images["idle_female_civilian_npc_right"], (72, 72)),
                      "elucidate_idle_female_civilian_npc_left": _sc(_preloaded_images["idle_female_civilian_npc_left"],
                                                                     (72, 72)),
                      "elucidate_idle_female_civilian_npc_down": _sc(_preloaded_images["idle_female_civilian_npc_down"],
                                                                     (72, 72)),
                      "elucidate_idle_male_civilian_variant_npc_up": _sc(
                          _preloaded_images["idle_male_civilian_variant_npc_up"], (72, 72)),
                      "elucidate_idle_male_civilian_variant_npc_right": _sc(
                          _preloaded_images["idle_male_civilian_variant_npc_right"], (72, 72)),
                      "elucidate_idle_male_civilian_variant_npc_left": _sc(
                          _preloaded_images["idle_male_civilian_variant_npc_left"], (72, 72)),
                      "elucidate_idle_male_civilian_variant_npc_down": _sc(
                          _preloaded_images["idle_male_civilian_variant_npc_down"], (72, 72)),
                      "elucidate_idle_female_civilian_variant_npc_up": _sc(
                          _preloaded_images["idle_female_civilian_variant_npc_up"], (72, 72)),
                      "elucidate_idle_female_civilian_variant_npc_right": _sc(
                          _preloaded_images["idle_female_civilian_variant_npc_right"], (72, 72)),
                      "elucidate_idle_female_civilian_variant_npc_left": _sc(
                          _preloaded_images["idle_female_civilian_variant_npc_left"], (72, 72)),
                      "elucidate_idle_female_civilian_variant_npc_down": _sc(
                          _preloaded_images["idle_female_civilian_variant_npc_down"], (72, 72)),
                      "elucidate_idle_blacksmith_npc_up": _sc(_preloaded_images["idle_blacksmith_npc_up"], (72, 72)),
                      "elucidate_idle_blacksmith_npc_right": _sc(_preloaded_images["idle_blacksmith_npc_right"],
                                                                 (72, 72)),
                      "elucidate_idle_blacksmith_npc_left": _sc(_preloaded_images["idle_blacksmith_npc_left"],
                                                                (72, 72)),
                      "elucidate_idle_blacksmith_npc_down": _sc(_preloaded_images["idle_blacksmith_npc_down"],
                                                                (72, 72)), "elucidate_idle_caligo_manifestation": _sc(
            _preloaded_images["idle_caligo_manifestation_npc_down"], (72, 192)),
                      "elucidate_idle_caligo_manifestation_black_bg": _sc(
                          _preloaded_images["idle_caligo_manifestation_black_bg"], (72, 192)),
                      "elucidate_idle_imprisoned_experiment_1_npc_down": _sc(
                          _preloaded_images["idle_imprisoned_experiment_1_npc_down"], (72, 72)),
                      "elucidate_idle_imprisoned_experiment_2_npc_down": _sc(
                          _preloaded_images["idle_imprisoned_experiment_2_npc_down"], (72, 72)),
                      "elucidate_idle_imprisoned_experiment_hostile_npc_down": _sc(
                          _preloaded_images["idle_imprisoned_experiment_hostile_npc_down"], (72, 72)),
                      "elucidate_idle_church_medical_staff_npc_down": _sc(
                          _preloaded_images["idle_church_medical_staff_npc_down"], (72, 72)),
                      "elucidate_idle_church_medical_staff_npc_right": _sc(
                          _preloaded_images["idle_church_medical_staff_npc_right"], (72, 72)),
                      "elucidate_idle_church_medical_staff_npc_left": _sc(
                          _preloaded_images["idle_church_medical_staff_npc_left"], (72, 72)),
                      "elucidate_idle_church_medical_staff_npc_up": _sc(
                          _preloaded_images["idle_church_medical_staff_npc_up"], (72, 72)),
                      "elucidate_idle_church_spy_npc_down": _sc(_preloaded_images["idle_church_spy_npc_down"],
                                                                (72, 72)),
                      "elucidate_walk_church_spy_npc_down_001": _sc(_preloaded_images["walk_church_spy_npc_down_001"],
                                                                    (72, 72)),
                      "elucidate_walk_church_spy_npc_down_002": _sc(_preloaded_images["walk_church_spy_npc_down_002"],
                                                                    (72, 72)),
                      "elucidate_idle_church_spy_npc_right": _sc(_preloaded_images["idle_church_spy_npc_right"],
                                                                 (72, 72)),
                      "elucidate_walk_church_spy_npc_right_001": _sc(_preloaded_images["walk_church_spy_npc_right_001"],
                                                                     (72, 72)),
                      "elucidate_walk_church_spy_npc_right_002": _sc(_preloaded_images["walk_church_spy_npc_right_002"],
                                                                     (72, 72)),
                      "elucidate_idle_church_spy_npc_left": _sc(_preloaded_images["idle_church_spy_npc_left"],
                                                                (72, 72)),
                      "elucidate_walk_church_spy_npc_left_001": _sc(_preloaded_images["walk_church_spy_npc_left_001"],
                                                                    (72, 72)),
                      "elucidate_walk_church_spy_npc_left_002": _sc(_preloaded_images["walk_church_spy_npc_left_002"],
                                                                    (72, 72)),
                      "elucidate_idle_church_spy_npc_up": _sc(_preloaded_images["idle_church_spy_npc_up"], (72, 72)),
                      "elucidate_walk_church_spy_npc_up_001": _sc(_preloaded_images["walk_church_spy_npc_up_001"],
                                                                  (72, 72)),
                      "elucidate_walk_church_spy_npc_up_002": _sc(_preloaded_images["walk_church_spy_npc_up_002"],
                                                                  (72, 72)),
                      "elucidate_idle_female_market_merchant_npc_down": _sc(
                          _preloaded_images["idle_female_market_merchant_npc_down"], (72, 72)),
                      "elucidate_idle_female_market_merchant_npc_right": _sc(
                          _preloaded_images["idle_female_market_merchant_npc_right"], (72, 72)),
                      "elucidate_idle_female_market_merchant_npc_left": _sc(
                          _preloaded_images["idle_female_market_merchant_npc_left"], (72, 72)),
                      "elucidate_idle_female_market_merchant_npc_up": _sc(
                          _preloaded_images["idle_female_market_merchant_npc_up"], (72, 72)),
                      "elucidate_idle_male_market_merchant_npc_down": _sc(
                          _preloaded_images["idle_male_market_merchant_npc_down"], (72, 72)),
                      "elucidate_idle_male_market_merchant_npc_right": _sc(
                          _preloaded_images["idle_male_market_merchant_npc_right"], (72, 72)),
                      "elucidate_idle_male_market_merchant_npc_left": _sc(
                          _preloaded_images["idle_male_market_merchant_npc_left"], (72, 72)),
                      "elucidate_idle_male_market_merchant_npc_up": _sc(
                          _preloaded_images["idle_male_market_merchant_npc_up"], (72, 72)),
                      "elucidate_idle_ghost_memory1_npc_left": _sc(_preloaded_images["idle_ghost_memory1_npc_left"],
                                                                   (72, 72)),
                      "elucidate_idle_ghost_memory1_npc_right": _sc(_preloaded_images["idle_ghost_memory1_npc_right"],
                                                                    (72, 72)),
                      "elucidate_idle_ghost_memory2_npc_left": _sc(_preloaded_images["idle_ghost_memory2_npc_left"],
                                                                   (72, 72)),
                      "elucidate_idle_ghost_memory2_npc_right": _sc(_preloaded_images["idle_ghost_memory2_npc_right"],
                                                                    (72, 72)),
                      "elucidate_idle_female_tribal_warrior_npc_down": _sc(
                          _preloaded_images["idle_female_tribal_warrior_npc_down"], (72, 72)),
                      "elucidate_idle_female_tribal_warrior_npc_left": _sc(
                          _preloaded_images["idle_female_tribal_warrior_npc_left"], (72, 72)),
                      "elucidate_idle_female_tribal_warrior_npc_right": _sc(
                          _preloaded_images["idle_female_tribal_warrior_npc_right"], (72, 72)),
                      "elucidate_idle_female_tribal_warrior_npc_up": _sc(
                          _preloaded_images["idle_female_tribal_warrior_npc_up"], (72, 72)),
                      "elucidate_idle_travelling_bard_npc_down": _sc(_preloaded_images["idle_travelling_bard_npc_down"],
                                                                     (72, 72)),
                      "elucidate_idle_travelling_bard_npc_left": _sc(_preloaded_images["idle_travelling_bard_npc_left"],
                                                                     (72, 72)),
                      "elucidate_idle_travelling_bard_npc_right": _sc(
                          _preloaded_images["idle_travelling_bard_npc_right"], (72, 72)),
                      "elucidate_idle_travelling_bard_npc_up": _sc(_preloaded_images["idle_travelling_bard_npc_up"],
                                                                   (72, 72)),
                      "elucidate_idle_cultist_priest_npc_down": _sc(_preloaded_images["idle_cultist_priest_npc_down"],
                                                                    (72, 72)),
                      "elucidate_idle_cultist_priest_npc_left": _sc(_preloaded_images["idle_cultist_priest_npc_left"],
                                                                    (72, 72)),
                      "elucidate_idle_cultist_priest_npc_right": _sc(_preloaded_images["idle_cultist_priest_npc_right"],
                                                                     (72, 72)),
                      "elucidate_idle_cultist_priest_npc_up": _sc(_preloaded_images["idle_cultist_priest_npc_up"],
                                                                  (72, 72)),
                      "elucidate_idle_tavern_keeper_npc_down": _sc(_preloaded_images["idle_tavern_keeper_npc_down"],
                                                                   (72, 72)),
                      "elucidate_idle_tavern_keeper_npc_left": _sc(_preloaded_images["idle_tavern_keeper_npc_left"],
                                                                   (72, 72)),
                      "elucidate_idle_tavern_keeper_npc_right": _sc(_preloaded_images["idle_tavern_keeper_npc_right"],
                                                                    (72, 72)),
                      "elucidate_idle_tavern_keeper_npc_up": _sc(_preloaded_images["idle_tavern_keeper_npc_up"],
                                                                 (72, 72)),
                      "elucidate_idle_cultist_archer_npc_down": _sc(_preloaded_images["idle_cultist_archer_npc_down"],
                                                                    (72, 72)),
                      "elucidate_walk_cultist_archer_npc_down_001": _sc(
                          _preloaded_images["walk_cultist_archer_npc_down_001"], (72, 72)),
                      "elucidate_walk_cultist_archer_npc_down_002": _sc(
                          _preloaded_images["walk_cultist_archer_npc_down_002"], (72, 72)),
                      "elucidate_idle_cultist_archer_npc_left": _sc(_preloaded_images["idle_cultist_archer_npc_left"],
                                                                    (72, 72)),
                      "elucidate_walk_cultist_archer_npc_left_001": _sc(
                          _preloaded_images["walk_cultist_archer_npc_left_001"], (72, 72)),
                      "elucidate_walk_cultist_archer_npc_left_002": _sc(
                          _preloaded_images["walk_cultist_archer_npc_left_002"], (72, 72)),
                      "elucidate_idle_cultist_archer_npc_right": _sc(_preloaded_images["idle_cultist_archer_npc_right"],
                                                                     (72, 72)),
                      "elucidate_walk_cultist_archer_npc_right_001": _sc(
                          _preloaded_images["walk_cultist_archer_npc_right_001"], (72, 72)),
                      "elucidate_walk_cultist_archer_npc_right_002": _sc(
                          _preloaded_images["walk_cultist_archer_npc_right_002"], (72, 72)),
                      "elucidate_idle_cultist_archer_npc_up": _sc(_preloaded_images["idle_cultist_archer_npc_up"],
                                                                  (72, 72)),
                      "elucidate_walk_cultist_archer_npc_up_001": _sc(
                          _preloaded_images["walk_cultist_archer_npc_up_001"], (72, 72)),
                      "elucidate_walk_cultist_archer_npc_up_002": _sc(
                          _preloaded_images["walk_cultist_archer_npc_up_002"], (72, 72)),
                      "elucidate_idle_cultist_channeler_npc_down": _sc(
                          _preloaded_images["idle_cultist_channeler_npc_down"], (72, 72)),
                      "elucidate_walk_cultist_channeler_npc_down_001": _sc(
                          _preloaded_images["walk_cultist_channeler_npc_down_001"], (72, 72)),
                      "elucidate_walk_cultist_channeler_npc_down_002": _sc(
                          _preloaded_images["walk_cultist_channeler_npc_down_002"], (72, 72)),
                      "elucidate_idle_cultist_channeler_npc_right": _sc(
                          _preloaded_images["idle_cultist_channeler_npc_right"], (72, 72)),
                      "elucidate_walk_cultist_channeler_npc_right_001": _sc(
                          _preloaded_images["walk_cultist_channeler_npc_right_001"], (72, 72)),
                      "elucidate_walk_cultist_channeler_npc_right_002": _sc(
                          _preloaded_images["walk_cultist_channeler_npc_right_002"], (72, 72)),
                      "elucidate_idle_cultist_channeler_npc_left": _sc(
                          _preloaded_images["idle_cultist_channeler_npc_left"], (72, 72)),
                      "elucidate_walk_cultist_channeler_npc_left_001": _sc(
                          _preloaded_images["walk_cultist_channeler_npc_left_001"], (72, 72)),
                      "elucidate_walk_cultist_channeler_npc_left_002": _sc(
                          _preloaded_images["walk_cultist_channeler_npc_left_002"], (72, 72)),
                      "elucidate_idle_cultist_channeler_npc_up": _sc(_preloaded_images["idle_cultist_channeler_npc_up"],
                                                                     (72, 72)),
                      "elucidate_walk_cultist_channeler_npc_up_001": _sc(
                          _preloaded_images["walk_cultist_channeler_npc_up_001"], (72, 72)),
                      "elucidate_walk_cultist_channeler_npc_up_002": _sc(
                          _preloaded_images["walk_cultist_channeler_npc_up_002"], (72, 72)),
                      "elucidate_idle_church_assassin_npc_down": _sc(_preloaded_images["idle_assassin_npc_down"],
                                                                     (72, 72)),
                      "elucidate_walk_church_assassin_npc_down_001": _sc(
                          _preloaded_images["walk_church_assassin_npc_down_001"], (72, 72)),
                      "elucidate_walk_church_assassin_npc_down_002": _sc(
                          _preloaded_images["walk_church_assassin_npc_down_002"], (72, 72)),
                      "elucidate_idle_church_assassin_npc_left": _sc(_preloaded_images["idle_assassin_npc_left"],
                                                                     (72, 72)),
                      "elucidate_walk_church_assassin_npc_left_001": _sc(
                          _preloaded_images["walk_church_assassin_npc_left_001"], (72, 72)),
                      "elucidate_walk_church_assassin_npc_left_002": _sc(
                          _preloaded_images["walk_church_assassin_npc_left_002"], (72, 72)),
                      "elucidate_idle_church_assassin_npc_right": _sc(_preloaded_images["idle_assassin_npc_right"],
                                                                      (72, 72)),
                      "elucidate_walk_church_assassin_npc_right_001": _sc(
                          _preloaded_images["walk_church_assassin_npc_right_001"], (72, 72)),
                      "elucidate_walk_church_assassin_npc_right_002": _sc(
                          _preloaded_images["walk_church_assassin_npc_right_002"], (72, 72)),
                      "elucidate_idle_church_assassin_npc_up": _sc(_preloaded_images["idle_assassin_npc_up"], (72, 72)),
                      "elucidate_walk_church_assassin_npc_up_001": _sc(
                          _preloaded_images["walk_church_assassin_npc_up_001"], (72, 72)),
                      "elucidate_walk_church_assassin_npc_up_002": _sc(
                          _preloaded_images["walk_church_assassin_npc_up_002"], (72, 72)),
                      "walk_shaman_left_001": _sc(_preloaded_images["walk_shaman_left_001"], (72, 72)),
                      "walk_shaman_left_002": _sc(_preloaded_images["walk_shaman_left_002"], (72, 72)),
                      "idle_shaman_left": _sc(_preloaded_images["idle_shaman_left"], (72, 72)),
                      "attack_shaman_left_001": _sc(_preloaded_images["attack_shaman_left_001"], (72, 72)),
                      "attack_shaman_left_002": _sc(_preloaded_images["attack_shaman_left_002"], (72, 72)),
                      "walk_shaman_down_001": _sc(_preloaded_images["walk_shaman_down_001"], (72, 72)),
                      "walk_shaman_down_002": _sc(_preloaded_images["walk_shaman_down_002"], (72, 72)),
                      "idle_shaman_down": _sc(_preloaded_images["idle_shaman_down"], (72, 72)),
                      "attack_shaman_down_001": _sc(_preloaded_images["attack_shaman_down_001"], (72, 72)),
                      "attack_shaman_down_002": _sc(_preloaded_images["attack_shaman_down_002"], (72, 72)),
                      "walk_shaman_up_001": _sc(_preloaded_images["walk_shaman_up_001"], (72, 72)),
                      "walk_shaman_up_002": _sc(_preloaded_images["walk_shaman_up_002"], (72, 72)),
                      "idle_shaman_up": _sc(_preloaded_images["idle_shaman_up"], (72, 72)),
                      "attack_shaman_up_001": _sc(_preloaded_images["attack_shaman_up_001"], (72, 72)),
                      "attack_shaman_up_002": _sc(_preloaded_images["attack_shaman_up_002"], (72, 72)),
                      "walk_shaman_right_001": _sc(_preloaded_images["walk_shaman_right_001"], (72, 72)),
                      "walk_shaman_right_002": _sc(_preloaded_images["walk_shaman_right_002"], (72, 72)),
                      "idle_shaman_right": _sc(_preloaded_images["idle_shaman_right"], (72, 72)),
                      "attack_shaman_right_001": _sc(_preloaded_images["attack_shaman_right_001"], (72, 72)),
                      "attack_shaman_right_002": _sc(_preloaded_images["attack_shaman_right_002"], (72, 72)),
                      "walk_merchant_up_001": _sc(_preloaded_images["walk_merchant_up_001"], (72, 72)),
                      "walk_merchant_up_002": _sc(_preloaded_images["walk_merchant_up_002"], (72, 72)),
                      "idle_merchant_up": _sc(_preloaded_images["idle_merchant_up"], (72, 72)),
                      "attack_merchant_up_001": _sc(_preloaded_images["attack_merchant_up_001"], (72, 72)),
                      "attack_merchant_up_002": _sc(_preloaded_images["attack_merchant_up_002"], (72, 72)),
                      "walk_merchant_right_001": _sc(_preloaded_images["walk_merchant_right_001"], (72, 72)),
                      "walk_merchant_right_002": _sc(_preloaded_images["walk_merchant_right_002"], (72, 72)),
                      "idle_merchant_right": _sc(_preloaded_images["idle_merchant_right"], (72, 72)),
                      "attack_merchant_right_001": _sc(_preloaded_images["attack_merchant_right_001"], (72, 72)),
                      "attack_merchant_right_002": _sc(_preloaded_images["attack_merchant_right_002"], (72, 72)),
                      "walk_merchant_left_001": _sc(_preloaded_images["walk_merchant_left_001"], (72, 72)),
                      "walk_merchant_left_002": _sc(_preloaded_images["walk_merchant_left_002"], (72, 72)),
                      "idle_merchant_left": _sc(_preloaded_images["idle_merchant_left"], (72, 72)),
                      "attack_merchant_left_001": _sc(_preloaded_images["attack_merchant_left_001"], (72, 72)),
                      "attack_merchant_left_002": _sc(_preloaded_images["attack_merchant_left_002"], (72, 72)),
                      "walk_merchant_down_001": _sc(_preloaded_images["walk_merchant_down_001"], (72, 72)),
                      "walk_merchant_down_002": _sc(_preloaded_images["walk_merchant_down_002"], (72, 72)),
                      "attack_merchant_down_001": _sc(_preloaded_images["attack_merchant_down_001"], (72, 72)),
                      "attack_merchant_down_002": _sc(_preloaded_images["attack_merchant_down_002"], (72, 72)),
                      "idle_merchant_down": _sc(_preloaded_images["idle_merchant_down"], (72, 72)),
                      "walk_priest_left_001": _sc(_preloaded_images["walk_priest_left_001"], (72, 72)),
                      "walk_priest_left_002": _sc(_preloaded_images["walk_priest_left_002"], (72, 72)),
                      "idle_priest_left": _sc(_preloaded_images["idle_priest_left"], (72, 72)),
                      "attack_priest_left_001": _sc(_preloaded_images["attack_priest_left_001"], (72, 72)),
                      "attack_priest_left_002": _sc(_preloaded_images["attack_priest_left_002"], (72, 72)),
                      "walk_priest_down_001": _sc(_preloaded_images["walk_priest_down_001"], (72, 72)),
                      "walk_priest_down_002": _sc(_preloaded_images["walk_priest_down_002"], (72, 72)),
                      "idle_priest_down": _sc(_preloaded_images["idle_priest_down"], (72, 72)),
                      "attack_priest_down_001": _sc(_preloaded_images["attack_priest_down_001"], (72, 72)),
                      "attack_priest_down_002": _sc(_preloaded_images["attack_priest_down_002"], (72, 72)),
                      "walk_priest_up_001": _sc(_preloaded_images["walk_priest_up_001"], (72, 72)),
                      "walk_priest_up_002": _sc(_preloaded_images["walk_priest_up_002"], (72, 72)),
                      "idle_priest_up": _sc(_preloaded_images["idle_priest_up"], (72, 72)),
                      "attack_priest_up_001": _sc(_preloaded_images["attack_priest_up_001"], (72, 72)),
                      "attack_priest_up_002": _sc(_preloaded_images["attack_priest_up_002"], (72, 72)),
                      "walk_priest_right_001": _sc(_preloaded_images["walk_priest_right_001"], (72, 72)),
                      "walk_priest_right_002": _sc(_preloaded_images["walk_priest_right_002"], (72, 72)),
                      "idle_priest_right": _sc(_preloaded_images["idle_priest_right"], (72, 72)),
                      "attack_priest_right_001": _sc(_preloaded_images["attack_priest_right_001"], (72, 72)),
                      "attack_priest_right_002": _sc(_preloaded_images["attack_priest_right_002"], (72, 72)),
                      "walk_cultist_down_001": _sc(_preloaded_images["walk_cultist_down_001"], (72, 72)),
                      "walk_cultist_down_002": _sc(_preloaded_images["walk_cultist_down_002"], (72, 72)),
                      "idle_cultist_down": _sc(_preloaded_images["idle_cultist_down"], (72, 72)),
                      "elucidate_attack_cultist_down_001": _sc(_preloaded_images["attack_cultist_down_001"], (72, 72)),
                      "elucidate_attack_cultist_down_002": _sc(_preloaded_images["attack_cultist_down_002"], (72, 72)),
                      "walk_cultist_up_001": _sc(_preloaded_images["walk_cultist_up_001"], (72, 72)),
                      "walk_cultist_up_002": _sc(_preloaded_images["walk_cultist_up_002"], (72, 72)),
                      "idle_cultist_up": _sc(_preloaded_images["idle_cultist_up"], (72, 72)),
                      "elucidate_attack_cultist_up_001": _sc(_preloaded_images["attack_cultist_up_001"], (72, 72)),
                      "elucidate_attack_cultist_up_002": _sc(_preloaded_images["attack_cultist_up_002"], (72, 72)),
                      "walk_cultist_right_001": _sc(_preloaded_images["walk_cultist_right_001"], (72, 72)),
                      "walk_cultist_right_002": _sc(_preloaded_images["walk_cultist_right_002"], (72, 72)),
                      "idle_cultist_right": _sc(_preloaded_images["idle_cultist_right"], (72, 72)),
                      "elucidate_attack_cultist_right_001": _sc(_preloaded_images["attack_cultist_right_001"],
                                                                (72, 72)),
                      "elucidate_attack_cultist_right_002": _sc(_preloaded_images["attack_cultist_right_002"],
                                                                (72, 72)),
                      "walk_cultist_left_001": _sc(_preloaded_images["walk_cultist_left_001"], (72, 72)),
                      "walk_cultist_left_002": _sc(_preloaded_images["walk_cultist_left_002"], (72, 72)),
                      "idle_cultist_left": _sc(_preloaded_images["idle_cultist_left"], (72, 72)),
                      "elucidate_attack_cultist_left_001": _sc(_preloaded_images["attack_cultist_left_001"], (72, 72)),
                      "elucidate_attack_cultist_left_002": _sc(_preloaded_images["attack_cultist_left_002"], (72, 72)),
                      "l_i_merchant_guild_hall": _sc(_preloaded_images["l_i_merchant_guild_hall"],
                                                     (int(5997 / 3.7), int(3350 / 3.7))), }

    _rotated_images = {"elucidate_title_1_r": pygame.transform.rotate(_scaled_images["elucidate_title_1"], 360),
                       "elucidate_select_ui_002_play_select_r": pygame.transform.rotate(
                           _scaled_images["elucidate_select_ui_002_play_select"], 90),
                       "elucidate_middle_gradient_001_r": pygame.transform.rotate(_preloaded_images["elucidate_middle_gradient_001"], 360),}

    PLAYER_SPRITES = {"mercenary": "mercenary", "cultist": "cultist", "priest": "priest", "shaman": "shaman",
                      "merchant": "merchant", }

    SPRITES = {
        "no": {
            "idle": {
                "up": _scaled_images["elucidate_no_sprite_idle_1"],
                "down": _scaled_images["elucidate_no_sprite_idle_2"],
                "left": _scaled_images["elucidate_no_sprite_idle_3"],
                "right": _scaled_images["elucidate_no_sprite_idle_4"], },
            "walk": {
                "up": [_scaled_images["elucidate_no_sprite_walk_1_1"], _scaled_images["elucidate_no_sprite_walk_1_2"]],
                "down": [_scaled_images["elucidate_no_sprite_walk_2_1"],
                         _scaled_images["elucidate_no_sprite_walk_2_2"]],
                "left": [_scaled_images["elucidate_no_sprite_walk_3_1"],
                         _scaled_images["elucidate_no_sprite_walk_3_2"]],
                "right": [_scaled_images["elucidate_no_sprite_walk_4_1"],
                          _scaled_images["elucidate_no_sprite_walk_4_2"]], },
            "attack": {
                "up": [_scaled_images["elucidate_no_sprite_attack_1_1"],
                       _scaled_images["elucidate_no_sprite_attack_1_2"]],
                "down": [_scaled_images["elucidate_no_sprite_attack_2_1"],
                         _scaled_images["elucidate_no_sprite_attack_2_2"]],
                "left": [_scaled_images["elucidate_no_sprite_attack_3_1"],
                         _scaled_images["elucidate_no_sprite_attack_3_2"]],
                "right": [_scaled_images["elucidate_no_sprite_attack_4_1"],
                          _scaled_images["elucidate_no_sprite_attack_4_2"]], }, },

        "mercenary": {"idle": {"up": _scaled_images["elucidate_mercenary_sprite_idle_1"],
                               "down": _scaled_images["elucidate_mercenary_sprite_idle_2"],
                               "left": _scaled_images["elucidate_mercenary_sprite_idle_3"],
                               "right": _scaled_images["elucidate_mercenary_sprite_idle_4"], }, "walk": {
            "up": [_scaled_images["elucidate_mercenary_sprite_walk_1_1"],
                   _scaled_images["elucidate_mercenary_sprite_walk_1_2"]],
            "down": [_scaled_images["elucidate_mercenary_sprite_walk_2_1"],
                     _scaled_images["elucidate_mercenary_sprite_walk_2_2"]],
            "left": [_scaled_images["elucidate_mercenary_sprite_walk_3_1"],
                     _scaled_images["elucidate_mercenary_sprite_walk_3_2"]],
            "right": [_scaled_images["elucidate_mercenary_sprite_walk_4_1"],
                      _scaled_images["elucidate_mercenary_sprite_walk_4_2"]], }, "attack": {
            "up": [_scaled_images["elucidate_mercenary_sprite_attack_1_1"],
                   _scaled_images["elucidate_mercenary_sprite_attack_1_2"]],
            "down": [_scaled_images["elucidate_mercenary_sprite_attack_2_1"],
                     _scaled_images["elucidate_mercenary_sprite_attack_2_2"]],
            "left": [_scaled_images["elucidate_mercenary_sprite_attack_3_1"],
                     _scaled_images["elucidate_mercenary_sprite_attack_3_2"]],
            "right": [_scaled_images["elucidate_mercenary_sprite_attack_4_1"],
                      _scaled_images["elucidate_mercenary_sprite_attack_4_2"]], }, },

        "cultist": {
            "idle": {"up": _scaled_images["idle_cultist_up"], "down": _scaled_images["idle_cultist_down"],
                     "left": _scaled_images["idle_cultist_left"],
                     "right": _scaled_images["idle_cultist_right"], },
            "walk": {"up": [_scaled_images["walk_cultist_up_001"], _scaled_images["walk_cultist_up_002"]],
                     "down": [_scaled_images["walk_cultist_down_001"], _scaled_images["walk_cultist_down_002"]],
                     "left": [_scaled_images["walk_cultist_left_001"], _scaled_images["walk_cultist_left_002"]],
                     "right": [_scaled_images["walk_cultist_right_001"],
                               _scaled_images["walk_cultist_right_002"]], }, "attack": {
                "up": [_scaled_images["elucidate_attack_cultist_up_001"],
                       _scaled_images["elucidate_attack_cultist_up_002"]],
                "down": [_scaled_images["elucidate_attack_cultist_down_001"],
                         _scaled_images["elucidate_attack_cultist_down_002"]],
                "left": [_scaled_images["elucidate_attack_cultist_left_001"],
                         _scaled_images["elucidate_attack_cultist_left_002"]],
                "right": [_scaled_images["elucidate_attack_cultist_right_001"],
                          _scaled_images["elucidate_attack_cultist_right_002"]], }, },

        "priest": {"idle": {"up": _scaled_images["idle_priest_up"], "down": _scaled_images["idle_priest_down"],
                            "left": _scaled_images["idle_priest_left"],
                            "right": _scaled_images["idle_priest_right"], },
                   "walk": {"up": [_scaled_images["walk_priest_up_001"], _scaled_images["walk_priest_up_002"]],
                            "down": [_scaled_images["walk_priest_down_001"],
                                     _scaled_images["walk_priest_down_002"]],
                            "left": [_scaled_images["walk_priest_left_001"],
                                     _scaled_images["walk_priest_left_002"]],
                            "right": [_scaled_images["walk_priest_right_001"],
                                      _scaled_images["walk_priest_right_002"]], }, "attack": {
                "up": [_scaled_images["attack_priest_up_001"], _scaled_images["attack_priest_up_002"]],
                "down": [_scaled_images["attack_priest_down_001"], _scaled_images["attack_priest_down_002"]],
                "left": [_scaled_images["attack_priest_left_001"], _scaled_images["attack_priest_left_002"]],
                "right": [_scaled_images["attack_priest_right_001"],
                          _scaled_images["attack_priest_right_002"]], }, },

        "merchant": {
            "idle": {"up": _scaled_images["idle_merchant_up"], "down": _scaled_images["idle_merchant_down"],
                     "left": _scaled_images["idle_merchant_left"],
                     "right": _scaled_images["idle_merchant_right"], },
            "walk": {"up": [_scaled_images["walk_merchant_up_001"], _scaled_images["walk_merchant_up_002"]],
                     "down": [_scaled_images["walk_merchant_down_001"],
                              _scaled_images["walk_merchant_down_002"]],
                     "left": [_scaled_images["walk_merchant_left_001"],
                              _scaled_images["walk_merchant_left_002"]],
                     "right": [_scaled_images["walk_merchant_right_001"],
                               _scaled_images["walk_merchant_right_002"]], }, "attack": {
                "up": [_scaled_images["attack_merchant_up_001"], _scaled_images["attack_merchant_up_002"]],
                "down": [_scaled_images["attack_merchant_down_001"], _scaled_images["attack_merchant_down_002"]],
                "left": [_scaled_images["attack_merchant_left_001"], _scaled_images["attack_merchant_left_002"]],
                "right": [_scaled_images["attack_merchant_right_001"],
                          _scaled_images["attack_merchant_right_002"]], }, },

        "shaman": {"idle": {"up": _scaled_images["idle_shaman_up"], "down": _scaled_images["idle_shaman_down"],
                            "left": _scaled_images["idle_shaman_left"],
                            "right": _scaled_images["idle_shaman_right"], },
                   "walk": {"up": [_scaled_images["walk_shaman_up_001"], _scaled_images["walk_shaman_up_002"]],
                            "down": [_scaled_images["walk_shaman_down_001"],
                                     _scaled_images["walk_shaman_down_002"]],
                            "left": [_scaled_images["walk_shaman_left_001"],
                                     _scaled_images["walk_shaman_left_002"]],
                            "right": [_scaled_images["walk_shaman_right_001"],
                                      _scaled_images["walk_shaman_right_002"]], }, "attack": {
                "up": [_scaled_images["attack_shaman_up_001"], _scaled_images["attack_shaman_up_002"]],
                "down": [_scaled_images["attack_shaman_down_001"], _scaled_images["attack_shaman_down_002"]],
                "left": [_scaled_images["attack_shaman_left_001"], _scaled_images["attack_shaman_left_002"]],
                "right": [_scaled_images["attack_shaman_right_001"],
                          _scaled_images["attack_shaman_right_002"]], }, }, "church_spy_npc": {
            "idle": {"up": _scaled_images["elucidate_idle_church_spy_npc_up"],
                     "down": _scaled_images["elucidate_idle_church_spy_npc_down"],
                     "left": _scaled_images["elucidate_idle_church_spy_npc_left"],
                     "right": _scaled_images["elucidate_idle_church_spy_npc_right"], }, "walk": {
                "up": [_scaled_images["elucidate_walk_church_spy_npc_up_001"],
                       _scaled_images["elucidate_walk_church_spy_npc_up_002"]],
                "down": [_scaled_images["elucidate_walk_church_spy_npc_down_001"],
                         _scaled_images["elucidate_walk_church_spy_npc_down_002"]],
                "left": [_scaled_images["elucidate_walk_church_spy_npc_left_001"],
                         _scaled_images["elucidate_walk_church_spy_npc_left_002"]],
                "right": [_scaled_images["elucidate_walk_church_spy_npc_right_001"],
                          _scaled_images["elucidate_walk_church_spy_npc_right_002"]], }, "attack": {
                "up": [_scaled_images["elucidate_walk_church_spy_npc_up_001"],
                       _scaled_images["elucidate_walk_church_spy_npc_up_002"]],
                "down": [_scaled_images["elucidate_walk_church_spy_npc_down_001"],
                         _scaled_images["elucidate_walk_church_spy_npc_down_002"]],
                "left": [_scaled_images["elucidate_walk_church_spy_npc_left_001"],
                         _scaled_images["elucidate_walk_church_spy_npc_left_002"]],
                "right": [_scaled_images["elucidate_walk_church_spy_npc_right_001"],
                          _scaled_images["elucidate_walk_church_spy_npc_right_002"]], }, }, "cultist_archer_npc": {
            "idle": {"up": _scaled_images["elucidate_idle_cultist_archer_npc_up"],
                     "down": _scaled_images["elucidate_idle_cultist_archer_npc_down"],
                     "left": _scaled_images["elucidate_idle_cultist_archer_npc_left"],
                     "right": _scaled_images["elucidate_idle_cultist_archer_npc_right"], }, "walk": {
                "up": [_scaled_images["elucidate_walk_cultist_archer_npc_up_001"],
                       _scaled_images["elucidate_walk_cultist_archer_npc_up_002"]],
                "down": [_scaled_images["elucidate_walk_cultist_archer_npc_down_001"],
                         _scaled_images["elucidate_walk_cultist_archer_npc_down_002"]],
                "left": [_scaled_images["elucidate_walk_cultist_archer_npc_left_001"],
                         _scaled_images["elucidate_walk_cultist_archer_npc_left_002"]],
                "right": [_scaled_images["elucidate_walk_cultist_archer_npc_right_001"],
                          _scaled_images["elucidate_walk_cultist_archer_npc_right_002"]], }, "attack": {
                "up": [_scaled_images["elucidate_walk_cultist_archer_npc_up_001"],
                       _scaled_images["elucidate_walk_cultist_archer_npc_up_002"]],
                "down": [_scaled_images["elucidate_walk_cultist_archer_npc_down_001"],
                         _scaled_images["elucidate_walk_cultist_archer_npc_down_002"]],
                "left": [_scaled_images["elucidate_walk_cultist_archer_npc_left_001"],
                         _scaled_images["elucidate_walk_cultist_archer_npc_left_002"]],
                "right": [_scaled_images["elucidate_walk_cultist_archer_npc_right_001"],
                          _scaled_images["elucidate_walk_cultist_archer_npc_right_002"]], }, },
        "cultist_channeler_npc": {
            "idle": {"up": _scaled_images["elucidate_idle_cultist_channeler_npc_up"],
                     "down": _scaled_images["elucidate_idle_cultist_channeler_npc_down"],
                     "left": _scaled_images["elucidate_idle_cultist_channeler_npc_left"],
                     "right": _scaled_images["elucidate_idle_cultist_channeler_npc_right"], }, "walk": {
                "up": [_scaled_images["elucidate_walk_cultist_channeler_npc_up_001"],
                       _scaled_images["elucidate_walk_cultist_channeler_npc_up_002"]],
                "down": [_scaled_images["elucidate_walk_cultist_channeler_npc_down_001"],
                         _scaled_images["elucidate_walk_cultist_channeler_npc_down_002"]],
                "left": [_scaled_images["elucidate_walk_cultist_channeler_npc_left_001"],
                         _scaled_images["elucidate_walk_cultist_channeler_npc_left_002"]],
                "right": [_scaled_images["elucidate_walk_cultist_channeler_npc_right_001"],
                          _scaled_images["elucidate_walk_cultist_channeler_npc_right_002"]], }, "attack": {
                "up": [_scaled_images["elucidate_walk_cultist_channeler_npc_up_001"],
                       _scaled_images["elucidate_walk_cultist_channeler_npc_up_002"]],
                "down": [_scaled_images["elucidate_walk_cultist_channeler_npc_down_001"],
                         _scaled_images["elucidate_walk_cultist_channeler_npc_down_002"]],
                "left": [_scaled_images["elucidate_walk_cultist_channeler_npc_left_001"],
                         _scaled_images["elucidate_walk_cultist_channeler_npc_left_002"]],
                "right": [_scaled_images["elucidate_walk_cultist_channeler_npc_right_001"],
                          _scaled_images["elucidate_walk_cultist_channeler_npc_right_002"]],
            },
        },
        "church_assassin_npc": {
            "idle": {"up": _scaled_images["elucidate_idle_church_assassin_npc_up"],
                     "down": _scaled_images["elucidate_idle_church_assassin_npc_down"],
                     "left": _scaled_images["elucidate_idle_church_assassin_npc_left"],
                     "right": _scaled_images["elucidate_idle_church_assassin_npc_right"], }, "walk": {
                "up": [_scaled_images["elucidate_walk_church_assassin_npc_up_001"],
                       _scaled_images["elucidate_walk_church_assassin_npc_up_002"]],
                "down": [_scaled_images["elucidate_walk_church_assassin_npc_down_001"],
                         _scaled_images["elucidate_walk_church_assassin_npc_down_002"]],
                "left": [_scaled_images["elucidate_walk_church_assassin_npc_left_001"],
                         _scaled_images["elucidate_walk_church_assassin_npc_left_002"]],
                "right": [_scaled_images["elucidate_walk_church_assassin_npc_right_001"],
                          _scaled_images["elucidate_walk_church_assassin_npc_right_002"]], }, "attack": {
                "up": [_scaled_images["elucidate_walk_church_assassin_npc_up_001"],
                       _scaled_images["elucidate_walk_church_assassin_npc_up_002"]],
                "down": [_scaled_images["elucidate_walk_church_assassin_npc_down_001"],
                         _scaled_images["elucidate_walk_church_assassin_npc_down_002"]],
                "left": [_scaled_images["elucidate_walk_church_assassin_npc_left_001"],
                         _scaled_images["elucidate_walk_church_assassin_npc_left_002"]],
                "right": [_scaled_images["elucidate_walk_church_assassin_npc_right_001"],
                          _scaled_images["elucidate_walk_church_assassin_npc_right_002"]], }, }, "cult_leader": {
            "idle": {"up": _scaled_images["elucidate_idle_cult_leader_npc_up"],
                     "down": _scaled_images["elucidate_idle_cult_leader_npc_down"],
                     "left": _scaled_images["elucidate_idle_cult_leader_npc_left"],
                     "right": _scaled_images["elucidate_idle_cult_leader_npc_right"], }, "walk": {
                "up": [_scaled_images["elucidate_idle_cult_leader_npc_up"],
                       _scaled_images["elucidate_idle_cult_leader_npc_up"]],
                "down": [_scaled_images["elucidate_idle_cult_leader_npc_down"],
                         _scaled_images["elucidate_idle_cult_leader_npc_down"]],
                "left": [_scaled_images["elucidate_idle_cult_leader_npc_left"],
                         _scaled_images["elucidate_idle_cult_leader_npc_left"]],
                "right": [_scaled_images["elucidate_idle_cult_leader_npc_right"],
                          _scaled_images["elucidate_idle_cult_leader_npc_right"]], }, "attack": {
                "up": [_scaled_images["elucidate_idle_cult_leader_npc_up"],
                       _scaled_images["elucidate_idle_cult_leader_npc_up"]],
                "down": [_scaled_images["elucidate_idle_cult_leader_npc_down"],
                         _scaled_images["elucidate_idle_cult_leader_npc_down"]],
                "left": [_scaled_images["elucidate_idle_cult_leader_npc_left"],
                         _scaled_images["elucidate_idle_cult_leader_npc_left"]],
                "right": [_scaled_images["elucidate_idle_cult_leader_npc_right"],
                          _scaled_images["elucidate_idle_cult_leader_npc_right"]], }, }, "cultist_soldier": {
            "idle": {"up": _scaled_images["elucidate_idle_cultist_soldier_npc_up"],
                     "down": _scaled_images["elucidate_idle_cultist_soldier_npc_down"],
                     "left": _scaled_images["elucidate_idle_cultist_soldier_npc_left"],
                     "right": _scaled_images["elucidate_idle_cultist_soldier_npc_right"], }, "walk": {
                "up": [_scaled_images["elucidate_idle_cultist_soldier_npc_up"],
                       _scaled_images["elucidate_idle_cultist_soldier_npc_up"]],
                "down": [_scaled_images["elucidate_idle_cultist_soldier_npc_down"],
                         _scaled_images["elucidate_idle_cultist_soldier_npc_down"]],
                "left": [_scaled_images["elucidate_idle_cultist_soldier_npc_left"],
                         _scaled_images["elucidate_idle_cultist_soldier_npc_left"]],
                "right": [_scaled_images["elucidate_idle_cultist_soldier_npc_right"],
                          _scaled_images["elucidate_idle_cultist_soldier_npc_right"]], }, "attack": {
                "up": [_scaled_images["elucidate_idle_cultist_soldier_npc_up"],
                       _scaled_images["elucidate_idle_cultist_soldier_npc_up"]],
                "down": [_scaled_images["elucidate_idle_cultist_soldier_npc_down"],
                         _scaled_images["elucidate_idle_cultist_soldier_npc_down"]],
                "left": [_scaled_images["elucidate_idle_cultist_soldier_npc_left"],
                         _scaled_images["elucidate_idle_cultist_soldier_npc_left"]],
                "right": [_scaled_images["elucidate_idle_cultist_soldier_npc_right"],
                          _scaled_images["elucidate_idle_cultist_soldier_npc_right"]], }, }, "corrupted1_cultist": {
            "idle": {"up": _scaled_images["elucidate_idle_corrupted1_cultist_npc_up"],
                     "down": _scaled_images["elucidate_idle_corrupted1_cultist_npc_down"],
                     "left": _scaled_images["elucidate_idle_corrupted1_cultist_npc_left"],
                     "right": _scaled_images["elucidate_idle_corrupted1_cultist_npc_right"], }, "walk": {
                "up": [_scaled_images["elucidate_idle_corrupted1_cultist_npc_up"],
                       _scaled_images["elucidate_idle_corrupted1_cultist_npc_up"]],
                "down": [_scaled_images["elucidate_idle_corrupted1_cultist_npc_down"],
                         _scaled_images["elucidate_idle_corrupted1_cultist_npc_down"]],
                "left": [_scaled_images["elucidate_idle_corrupted1_cultist_npc_left"],
                         _scaled_images["elucidate_idle_corrupted1_cultist_npc_left"]],
                "right": [_scaled_images["elucidate_idle_corrupted1_cultist_npc_right"],
                          _scaled_images["elucidate_idle_corrupted1_cultist_npc_right"]], }, "attack": {
                "up": [_scaled_images["elucidate_idle_corrupted1_cultist_npc_up"],
                       _scaled_images["elucidate_idle_corrupted1_cultist_npc_up"]],
                "down": [_scaled_images["elucidate_idle_corrupted1_cultist_npc_down"],
                         _scaled_images["elucidate_idle_corrupted1_cultist_npc_down"]],
                "left": [_scaled_images["elucidate_idle_corrupted1_cultist_npc_left"],
                         _scaled_images["elucidate_idle_corrupted1_cultist_npc_left"]],
                "right": [_scaled_images["elucidate_idle_corrupted1_cultist_npc_right"],
                          _scaled_images["elucidate_idle_corrupted1_cultist_npc_right"]], }, },
        "amalgamated_villagers": {
            "idle": {"up": _scaled_images["elucidate_idle_amalgamated_villagers_npc_right"],
                     "down": _scaled_images["elucidate_idle_amalgamated_villagers_npc_right"],
                     "left": _scaled_images["elucidate_idle_amalgamated_villagers_npc_left"],
                     "right": _scaled_images["elucidate_idle_amalgamated_villagers_npc_right"], }, "walk": {
                "up": [_scaled_images["elucidate_idle_amalgamated_villagers_npc_right"],
                       _scaled_images["elucidate_idle_amalgamated_villagers_npc_right"]],
                "down": [_scaled_images["elucidate_idle_amalgamated_villagers_npc_right"],
                         _scaled_images["elucidate_idle_amalgamated_villagers_npc_right"]],
                "left": [_scaled_images["elucidate_idle_amalgamated_villagers_npc_left"],
                         _scaled_images["elucidate_idle_amalgamated_villagers_npc_left"]],
                "right": [_scaled_images["elucidate_idle_amalgamated_villagers_npc_right"],
                          _scaled_images["elucidate_idle_amalgamated_villagers_npc_right"]], }, "attack": {
                "up": [_scaled_images["elucidate_idle_amalgamated_villagers_npc_right"],
                       _scaled_images["elucidate_idle_amalgamated_villagers_npc_right"]],
                "down": [_scaled_images["elucidate_idle_amalgamated_villagers_npc_right"],
                         _scaled_images["elucidate_idle_amalgamated_villagers_npc_right"]],
                "left": [_scaled_images["elucidate_idle_amalgamated_villagers_npc_left"],
                         _scaled_images["elucidate_idle_amalgamated_villagers_npc_left"]],
                "right": [_scaled_images["elucidate_idle_amalgamated_villagers_npc_right"],
                          _scaled_images["elucidate_idle_amalgamated_villagers_npc_right"]], }, },
        "amalgamated_knights": {
            "idle": {"up": _scaled_images["elucidate_idle_amalgamated_knights_npc_right"],
                     "down": _scaled_images["elucidate_idle_amalgamated_knights_npc_right"],
                     "left": _scaled_images["elucidate_idle_amalgamated_knights_npc_left"],
                     "right": _scaled_images["elucidate_idle_amalgamated_knights_npc_right"], }, "walk": {
                "up": [_scaled_images["elucidate_idle_amalgamated_knights_npc_right"],
                       _scaled_images["elucidate_idle_amalgamated_knights_npc_right"]],
                "down": [_scaled_images["elucidate_idle_amalgamated_knights_npc_right"],
                         _scaled_images["elucidate_idle_amalgamated_knights_npc_right"]],
                "left": [_scaled_images["elucidate_idle_amalgamated_knights_npc_left"],
                         _scaled_images["elucidate_idle_amalgamated_knights_npc_left"]],
                "right": [_scaled_images["elucidate_idle_amalgamated_knights_npc_right"],
                          _scaled_images["elucidate_idle_amalgamated_knights_npc_right"]], }, "attack": {
                "up": [_scaled_images["elucidate_idle_amalgamated_knights_npc_right"],
                       _scaled_images["elucidate_idle_amalgamated_knights_npc_right"]],
                "down": [_scaled_images["elucidate_idle_amalgamated_knights_npc_right"],
                         _scaled_images["elucidate_idle_amalgamated_knights_npc_right"]],
                "left": [_scaled_images["elucidate_idle_amalgamated_knights_npc_left"],
                         _scaled_images["elucidate_idle_amalgamated_knights_npc_left"]],
                "right": [_scaled_images["elucidate_idle_amalgamated_knights_npc_right"],
                          _scaled_images["elucidate_idle_amalgamated_knights_npc_right"]], }, },
        "amalgamated_civilians": {
            "idle": {"up": _scaled_images["elucidate_idle_amalgamated_civillians_npc_right"],
                     "down": _scaled_images["elucidate_idle_amalgamated_civillians_npc_right"],
                     "left": _scaled_images["elucidate_idle_amalgamated_civillians_npc_left"],
                     "right": _scaled_images["elucidate_idle_amalgamated_civillians_npc_right"], }, "walk": {
                "up": [_scaled_images["elucidate_idle_amalgamated_civillians_npc_right"],
                       _scaled_images["elucidate_idle_amalgamated_civillians_npc_right"]],
                "down": [_scaled_images["elucidate_idle_amalgamated_civillians_npc_right"],
                         _scaled_images["elucidate_idle_amalgamated_civillians_npc_right"]],
                "left": [_scaled_images["elucidate_idle_amalgamated_civillians_npc_left"],
                         _scaled_images["elucidate_idle_amalgamated_civillians_npc_left"]],
                "right": [_scaled_images["elucidate_idle_amalgamated_civillians_npc_right"],
                          _scaled_images["elucidate_idle_amalgamated_civillians_npc_right"]], }, "attack": {
                "up": [_scaled_images["elucidate_idle_amalgamated_civillians_npc_right"],
                       _scaled_images["elucidate_idle_amalgamated_civillians_npc_right"]],
                "down": [_scaled_images["elucidate_idle_amalgamated_civillians_npc_right"],
                         _scaled_images["elucidate_idle_amalgamated_civillians_npc_right"]],
                "left": [_scaled_images["elucidate_idle_amalgamated_civillians_npc_left"],
                         _scaled_images["elucidate_idle_amalgamated_civillians_npc_left"]],
                "right": [_scaled_images["elucidate_idle_amalgamated_civillians_npc_right"],
                          _scaled_images["elucidate_idle_amalgamated_civillians_npc_right"]], }, },
        "melted_male_villager": {
            "idle": {"up": _scaled_images["elucidate_idle_melted_male_villager_npc_up"],
                     "down": _scaled_images["elucidate_idle_melted_male_villager_npc_down"],
                     "left": _scaled_images["elucidate_idle_melted_male_villager_npc_left"],
                     "right": _scaled_images["elucidate_idle_melted_male_villager_npc_right"], }, "walk": {
                "up": [_scaled_images["elucidate_idle_melted_male_villager_npc_up"],
                       _scaled_images["elucidate_idle_melted_male_villager_npc_up"]],
                "down": [_scaled_images["elucidate_idle_melted_male_villager_npc_down"],
                         _scaled_images["elucidate_idle_melted_male_villager_npc_down"]],
                "left": [_scaled_images["elucidate_idle_melted_male_villager_npc_left"],
                         _scaled_images["elucidate_idle_melted_male_villager_npc_left"]],
                "right": [_scaled_images["elucidate_idle_melted_male_villager_npc_right"],
                          _scaled_images["elucidate_idle_melted_male_villager_npc_right"]], }, "attack": {
                "up": [_scaled_images["elucidate_idle_melted_male_villager_npc_up"],
                       _scaled_images["elucidate_idle_melted_male_villager_npc_up"]],
                "down": [_scaled_images["elucidate_idle_melted_male_villager_npc_down"],
                         _scaled_images["elucidate_idle_melted_male_villager_npc_down"]],
                "left": [_scaled_images["elucidate_idle_melted_male_villager_npc_left"],
                         _scaled_images["elucidate_idle_melted_male_villager_npc_left"]],
                "right": [_scaled_images["elucidate_idle_melted_male_villager_npc_right"],
                          _scaled_images["elucidate_idle_melted_male_villager_npc_right"]], }, },
        "melted_female_villager": {
            "idle": {"up": _scaled_images["elucidate_idle_melted_female_villager_npc_up"],
                     "down": _scaled_images["elucidate_idle_melted_female_villager_npc_down"],
                     "left": _scaled_images["elucidate_idle_melted_female_villager_npc_left"],
                     "right": _scaled_images["elucidate_idle_melted_female_villager_npc_right"], }, "walk": {
                "up": [_scaled_images["elucidate_idle_melted_female_villager_npc_up"],
                       _scaled_images["elucidate_idle_melted_female_villager_npc_up"]],
                "down": [_scaled_images["elucidate_idle_melted_female_villager_npc_down"],
                         _scaled_images["elucidate_idle_melted_female_villager_npc_down"]],
                "left": [_scaled_images["elucidate_idle_melted_female_villager_npc_left"],
                         _scaled_images["elucidate_idle_melted_female_villager_npc_left"]],
                "right": [_scaled_images["elucidate_idle_melted_female_villager_npc_right"],
                          _scaled_images["elucidate_idle_melted_female_villager_npc_right"]], }, "attack": {
                "up": [_scaled_images["elucidate_idle_melted_female_villager_npc_up"],
                       _scaled_images["elucidate_idle_melted_female_villager_npc_up"]],
                "down": [_scaled_images["elucidate_idle_melted_female_villager_npc_down"],
                         _scaled_images["elucidate_idle_melted_female_villager_npc_down"]],
                "left": [_scaled_images["elucidate_idle_melted_female_villager_npc_left"],
                         _scaled_images["elucidate_idle_melted_female_villager_npc_left"]],
                "right": [_scaled_images["elucidate_idle_melted_female_villager_npc_right"],
                          _scaled_images["elucidate_idle_melted_female_villager_npc_right"]], }, },
        "corrupted3_cultist": {
            "idle": {"up": _scaled_images["elucidate_idle_corrupted3_cultist_npc_up"],
                     "down": _scaled_images["elucidate_idle_corrupted3_cultist_npc_down"],
                     "left": _scaled_images["elucidate_idle_corrupted3_cultist_npc_left"],
                     "right": _scaled_images["elucidate_idle_corrupted3_cultist_npc_right"], }, "walk": {
                "up": [_scaled_images["elucidate_idle_corrupted3_cultist_npc_up"],
                       _scaled_images["elucidate_idle_corrupted3_cultist_npc_up"]],
                "down": [_scaled_images["elucidate_idle_corrupted3_cultist_npc_down"],
                         _scaled_images["elucidate_idle_corrupted3_cultist_npc_down"]],
                "left": [_scaled_images["elucidate_idle_corrupted3_cultist_npc_left"],
                         _scaled_images["elucidate_idle_corrupted3_cultist_npc_left"]],
                "right": [_scaled_images["elucidate_idle_corrupted3_cultist_npc_right"],
                          _scaled_images["elucidate_idle_corrupted3_cultist_npc_right"]], }, "attack": {
                "up": [_scaled_images["elucidate_idle_corrupted3_cultist_npc_up"],
                       _scaled_images["elucidate_idle_corrupted3_cultist_npc_up"]],
                "down": [_scaled_images["elucidate_idle_corrupted3_cultist_npc_down"],
                         _scaled_images["elucidate_idle_corrupted3_cultist_npc_down"]],
                "left": [_scaled_images["elucidate_idle_corrupted3_cultist_npc_left"],
                         _scaled_images["elucidate_idle_corrupted3_cultist_npc_left"]],
                "right": [_scaled_images["elucidate_idle_corrupted3_cultist_npc_right"],
                          _scaled_images["elucidate_idle_corrupted3_cultist_npc_right"]], }, }, "corrupted2_cultist": {
            "idle": {"up": _scaled_images["elucidate_idle_corrupted2_cultist_npc_up"],
                     "down": _scaled_images["elucidate_idle_corrupted2_cultist_npc_down"],
                     "left": _scaled_images["elucidate_idle_corrupted2_cultist_npc_left"],
                     "right": _scaled_images["elucidate_idle_corrupted2_cultist_npc_right"], }, "walk": {
                "up": [_scaled_images["elucidate_idle_corrupted2_cultist_npc_up"],
                       _scaled_images["elucidate_idle_corrupted2_cultist_npc_up"]],
                "down": [_scaled_images["elucidate_idle_corrupted2_cultist_npc_down"],
                         _scaled_images["elucidate_idle_corrupted2_cultist_npc_down"]],
                "left": [_scaled_images["elucidate_idle_corrupted2_cultist_npc_left"],
                         _scaled_images["elucidate_idle_corrupted2_cultist_npc_left"]],
                "right": [_scaled_images["elucidate_idle_corrupted2_cultist_npc_right"],
                          _scaled_images["elucidate_idle_corrupted2_cultist_npc_right"]], }, "attack": {
                "up": [_scaled_images["elucidate_idle_corrupted2_cultist_npc_up"],
                       _scaled_images["elucidate_idle_corrupted2_cultist_npc_up"]],
                "down": [_scaled_images["elucidate_idle_corrupted2_cultist_npc_down"],
                         _scaled_images["elucidate_idle_corrupted2_cultist_npc_down"]],
                "left": [_scaled_images["elucidate_idle_corrupted2_cultist_npc_left"],
                         _scaled_images["elucidate_idle_corrupted2_cultist_npc_left"]],
                "right": [_scaled_images["elucidate_idle_corrupted2_cultist_npc_right"],
                          _scaled_images["elucidate_idle_corrupted2_cultist_npc_right"]], }, }, "librarian_scholar": {
            "idle": {"up": _scaled_images["elucidate_idle_librarian_scholar_npc_up"],
                     "down": _scaled_images["elucidate_idle_librarian_scholar_npc_down"],
                     "left": _scaled_images["elucidate_idle_librarian_scholar_npc_left"],
                     "right": _scaled_images["elucidate_idle_librarian_scholar_npc_right"], }, "walk": {
                "up": [_scaled_images["elucidate_idle_librarian_scholar_npc_up"],
                       _scaled_images["elucidate_idle_librarian_scholar_npc_up"]],
                "down": [_scaled_images["elucidate_idle_librarian_scholar_npc_down"],
                         _scaled_images["elucidate_idle_librarian_scholar_npc_down"]],
                "left": [_scaled_images["elucidate_idle_librarian_scholar_npc_left"],
                         _scaled_images["elucidate_idle_librarian_scholar_npc_left"]],
                "right": [_scaled_images["elucidate_idle_librarian_scholar_npc_right"],
                          _scaled_images["elucidate_idle_librarian_scholar_npc_right"]], }, "attack": {
                "up": [_scaled_images["elucidate_no_sprite_attack_1_1"],
                       _scaled_images["elucidate_no_sprite_attack_1_2"]],
                "down": [_scaled_images["elucidate_no_sprite_attack_2_1"],
                         _scaled_images["elucidate_no_sprite_attack_2_2"]],
                "left": [_scaled_images["elucidate_no_sprite_attack_3_1"],
                         _scaled_images["elucidate_no_sprite_attack_3_2"]],
                "right": [_scaled_images["elucidate_no_sprite_attack_4_1"],
                          _scaled_images["elucidate_no_sprite_attack_4_2"]], }, }, "holyknight": {
            "idle": {"up": _scaled_images["elucidate_idle_holyknight_npc_up"],
                     "down": _scaled_images["elucidate_idle_holyknight_npc_down"],
                     "left": _scaled_images["elucidate_idle_holyknight_npc_left"],
                     "right": _scaled_images["elucidate_idle_holyknight_npc_right"], }, "walk": {
                "up": [_scaled_images["elucidate_idle_holyknight_npc_up"],
                       _scaled_images["elucidate_idle_holyknight_npc_up"]],
                "down": [_scaled_images["elucidate_idle_holyknight_npc_down"],
                         _scaled_images["elucidate_idle_holyknight_npc_down"]],
                "left": [_scaled_images["elucidate_idle_holyknight_npc_left"],
                         _scaled_images["elucidate_idle_holyknight_npc_left"]],
                "right": [_scaled_images["elucidate_idle_holyknight_npc_right"],
                          _scaled_images["elucidate_idle_holyknight_npc_right"]], }, "attack": {
                "up": [_scaled_images["elucidate_idle_holyknight_npc_up"],
                       _scaled_images["elucidate_idle_holyknight_npc_up"]],
                "down": [_scaled_images["elucidate_idle_holyknight_npc_down"],
                         _scaled_images["elucidate_idle_holyknight_npc_down"]],
                "left": [_scaled_images["elucidate_idle_holyknight_npc_left"],
                         _scaled_images["elucidate_idle_holyknight_npc_left"]],
                "right": [_scaled_images["elucidate_idle_holyknight_npc_right"],
                          _scaled_images["elucidate_idle_holyknight_npc_right"]], }, }, "male_faithful_citizen": {
            "idle": {"up": _scaled_images["elucidate_idle_male_faithful_citizen_npc_up"],
                     "down": _scaled_images["elucidate_idle_male_faithful_citizen_npc_down"],
                     "left": _scaled_images["elucidate_idle_male_faithful_citizen_npc_left"],
                     "right": _scaled_images["elucidate_idle_male_faithful_citizen_npc_right"], }, "walk": {
                "up": [_scaled_images["elucidate_idle_male_faithful_citizen_npc_up"],
                       _scaled_images["elucidate_idle_male_faithful_citizen_npc_up"]],
                "down": [_scaled_images["elucidate_idle_male_faithful_citizen_npc_down"],
                         _scaled_images["elucidate_idle_male_faithful_citizen_npc_down"]],
                "left": [_scaled_images["elucidate_idle_male_faithful_citizen_npc_left"],
                         _scaled_images["elucidate_idle_male_faithful_citizen_npc_left"]],
                "right": [_scaled_images["elucidate_idle_male_faithful_citizen_npc_right"],
                          _scaled_images["elucidate_idle_male_faithful_citizen_npc_right"]],
                "down": [_scaled_images["elucidate_no_sprite_walk_2_1"],
                         _scaled_images["elucidate_no_sprite_walk_2_2"]],
                "left": [_scaled_images["elucidate_no_sprite_walk_3_1"],
                         _scaled_images["elucidate_no_sprite_walk_3_2"]],
                "right": [_scaled_images["elucidate_no_sprite_walk_4_1"],
                          _scaled_images["elucidate_no_sprite_walk_4_2"]], }, "attack": {
                "up": [_scaled_images["elucidate_no_sprite_attack_1_1"],
                       _scaled_images["elucidate_no_sprite_attack_1_2"]],
                "down": [_scaled_images["elucidate_no_sprite_attack_2_1"],
                         _scaled_images["elucidate_no_sprite_attack_2_2"]],
                "left": [_scaled_images["elucidate_no_sprite_attack_3_1"],
                         _scaled_images["elucidate_no_sprite_attack_3_2"]],
                "right": [_scaled_images["elucidate_no_sprite_attack_4_1"],
                          _scaled_images["elucidate_no_sprite_attack_4_2"]], }, }, "female_faithful_citizen": {
            "idle": {"up": _scaled_images["elucidate_idle_female_faithful_citizen_npc_up"],
                     "down": _scaled_images["elucidate_idle_female_faithful_citizen_npc_down"],
                     "left": _scaled_images["elucidate_idle_female_faithful_citizen_npc_left"],
                     "right": _scaled_images["elucidate_idle_female_faithful_citizen_npc_right"], }, "walk": {
                "up": [_scaled_images["elucidate_idle_female_faithful_citizen_npc_up"],
                       _scaled_images["elucidate_idle_female_faithful_citizen_npc_up"]],
                "down": [_scaled_images["elucidate_idle_female_faithful_citizen_npc_down"],
                         _scaled_images["elucidate_idle_female_faithful_citizen_npc_down"]],
                "left": [_scaled_images["elucidate_idle_female_faithful_citizen_npc_left"],
                         _scaled_images["elucidate_idle_female_faithful_citizen_npc_left"]],
                "right": [_scaled_images["elucidate_idle_female_faithful_citizen_npc_right"],
                          _scaled_images["elucidate_idle_female_faithful_citizen_npc_right"]],
                "down": [_scaled_images["elucidate_no_sprite_walk_2_1"],
                         _scaled_images["elucidate_no_sprite_walk_2_2"]],
                "left": [_scaled_images["elucidate_no_sprite_walk_3_1"],
                         _scaled_images["elucidate_no_sprite_walk_3_2"]],
                "right": [_scaled_images["elucidate_no_sprite_walk_4_1"],
                          _scaled_images["elucidate_no_sprite_walk_4_2"]], }, "attack": {
                "up": [_scaled_images["elucidate_no_sprite_attack_1_1"],
                       _scaled_images["elucidate_no_sprite_attack_1_2"]],
                "down": [_scaled_images["elucidate_no_sprite_attack_2_1"],
                         _scaled_images["elucidate_no_sprite_attack_2_2"]],
                "left": [_scaled_images["elucidate_no_sprite_attack_3_1"],
                         _scaled_images["elucidate_no_sprite_attack_3_2"]],
                "right": [_scaled_images["elucidate_no_sprite_attack_4_1"],
                          _scaled_images["elucidate_no_sprite_attack_4_2"]], }, }, "chuAttendants": {
            "idle": {"up": _scaled_images["elucidate_idle_sprite_chuAttendants_up"],
                     "down": _scaled_images["elucidate_idle_sprite_chuAttendants_down"],
                     "left": _scaled_images["elucidate_idle_sprite_chuAttendants_left"],
                     "right": _scaled_images["elucidate_idle_sprite_chuAttendants_right"], }, "walk": {
                "up": [_scaled_images["elucidate_idle_sprite_chuAttendants_up"],
                       _scaled_images["elucidate_idle_sprite_chuAttendants_up"]],
                "down": [_scaled_images["elucidate_idle_sprite_chuAttendants_down"],
                         _scaled_images["elucidate_idle_sprite_chuAttendants_down"]],
                "left": [_scaled_images["elucidate_idle_sprite_chuAttendants_left"],
                         _scaled_images["elucidate_idle_sprite_chuAttendants_left"]],
                "right": [_scaled_images["elucidate_idle_sprite_chuAttendants_right"],
                          _scaled_images["elucidate_idle_sprite_chuAttendants_right"]],
                "down": [_scaled_images["elucidate_no_sprite_walk_2_1"],
                         _scaled_images["elucidate_no_sprite_walk_2_2"]],
                "left": [_scaled_images["elucidate_no_sprite_walk_3_1"],
                         _scaled_images["elucidate_no_sprite_walk_3_2"]],
                "right": [_scaled_images["elucidate_no_sprite_walk_4_1"],
                          _scaled_images["elucidate_no_sprite_walk_4_2"]], }, "attack": {
                "up": [_scaled_images["elucidate_no_sprite_attack_1_1"],
                       _scaled_images["elucidate_no_sprite_attack_1_2"]],
                "down": [_scaled_images["elucidate_no_sprite_attack_2_1"],
                         _scaled_images["elucidate_no_sprite_attack_2_2"]],
                "left": [_scaled_images["elucidate_no_sprite_attack_3_1"],
                         _scaled_images["elucidate_no_sprite_attack_3_2"]],
                "right": [_scaled_images["elucidate_no_sprite_attack_4_1"],
                          _scaled_images["elucidate_no_sprite_attack_4_2"]], }, }, "tribe_warrior": {
            "idle": {"up": _scaled_images["elucidate_idle_tribe_warrior_npc_up"],
                     "down": _scaled_images["elucidate_idle_tribe_warrior_npc_down"],
                     "left": _scaled_images["elucidate_idle_tribe_warrior_npc_left"],
                     "right": _scaled_images["elucidate_idle_tribe_warrior_npc_right"], }, "walk": {
                "up": _scaled_images["elucidate_idle_tribe_warrior_npc_up"],
                "down": _scaled_images["elucidate_idle_tribe_warrior_npc_down"],
                "left": _scaled_images["elucidate_idle_tribe_warrior_npc_left"],
                "right": _scaled_images["elucidate_idle_tribe_warrior_npc_right"], }, "attack": {
                "up": _scaled_images["elucidate_idle_tribe_warrior_npc_up"],
                "down": _scaled_images["elucidate_idle_tribe_warrior_npc_down"],
                "left": _scaled_images["elucidate_idle_tribe_warrior_npc_left"],
                "right": _scaled_images["elucidate_idle_tribe_warrior_npc_right"], }, }, "tribe_elder": {
            "idle": {"up": _scaled_images["elucidate_idle_tribe_elder_npc_up"],
                     "down": _scaled_images["elucidate_idle_tribe_elder_npc_down"],
                     "left": _scaled_images["elucidate_idle_tribe_elder_npc_left"],
                     "right": _scaled_images["elucidate_idle_tribe_elder_npc_right"], }, "walk": {
                "up": [_scaled_images["elucidate_no_sprite_walk_1_1"], _scaled_images["elucidate_no_sprite_walk_1_2"]],
                "up": _scaled_images["elucidate_idle_tribe_elder_npc_up"],
                "down": _scaled_images["elucidate_idle_tribe_elder_npc_down"],
                "left": _scaled_images["elucidate_idle_tribe_elder_npc_left"],
                "right": _scaled_images["elucidate_idle_tribe_elder_npc_right"], }, "walk": {
                "up": [_scaled_images["elucidate_no_sprite_walk_1_1"],
                       _scaled_images["elucidate_no_sprite_walk_1_2"]], }, "attack": {
                "up": [_scaled_images["elucidate_no_sprite_attack_1_1"],
                       _scaled_images["elucidate_no_sprite_attack_1_2"]],
                "down": [_scaled_images["elucidate_no_sprite_attack_2_1"],
                         _scaled_images["elucidate_no_sprite_attack_2_2"]],
                "left": [_scaled_images["elucidate_no_sprite_attack_3_1"],
                         _scaled_images["elucidate_no_sprite_attack_3_2"]],
                "right": [_scaled_images["elucidate_no_sprite_attack_4_1"],
                          _scaled_images["elucidate_no_sprite_attack_4_2"]], }, }, "tribe_chief": {
            "idle": {"up": _scaled_images["elucidate_idle_tribe_chief_npc_up"],
                     "down": _scaled_images["elucidate_idle_tribe_chief_npc_down"],
                     "left": _scaled_images["elucidate_idle_tribe_chief_npc_left"],
                     "right": _scaled_images["elucidate_idle_tribe_chief_npc_right"], }, "walk": {
                "up": [_scaled_images["elucidate_no_sprite_walk_1_1"], _scaled_images["elucidate_no_sprite_walk_1_2"]],
                "down": [_scaled_images["elucidate_no_sprite_walk_2_1"],
                         _scaled_images["elucidate_no_sprite_walk_2_2"]],
                "left": [_scaled_images["elucidate_no_sprite_walk_3_1"],
                         _scaled_images["elucidate_no_sprite_walk_3_2"]],
                "right": [_scaled_images["elucidate_no_sprite_walk_4_1"],
                          _scaled_images["elucidate_no_sprite_walk_4_2"]], }, "attack": {
                "up": [_scaled_images["elucidate_no_sprite_attack_1_1"],
                       _scaled_images["elucidate_no_sprite_attack_1_2"]],
                "down": [_scaled_images["elucidate_no_sprite_attack_2_1"],
                         _scaled_images["elucidate_no_sprite_attack_2_2"]],
                "left": [_scaled_images["elucidate_no_sprite_attack_3_1"],
                         _scaled_images["elucidate_no_sprite_attack_3_2"]],
                "right": [_scaled_images["elucidate_no_sprite_attack_4_1"],
                          _scaled_images["elucidate_no_sprite_attack_4_2"]], }, }, "supply_merchant": {
            "idle": {"up": _scaled_images["elucidate_idle_supply_merchant_npc_up"],
                     "down": _scaled_images["elucidate_idle_supply_merchant_npc_down"],
                     "left": _scaled_images["elucidate_idle_supply_merchant_npc_left"],
                     "right": _scaled_images["elucidate_idle_supply_merchant_npc_right"], }, "walk": {
                "up": [_scaled_images["elucidate_no_sprite_walk_1_1"], _scaled_images["elucidate_no_sprite_walk_1_2"]],
                "down": [_scaled_images["elucidate_no_sprite_walk_2_1"],
                         _scaled_images["elucidate_no_sprite_walk_2_2"]],
                "left": [_scaled_images["elucidate_no_sprite_walk_3_1"],
                         _scaled_images["elucidate_no_sprite_walk_3_2"]],
                "right": [_scaled_images["elucidate_no_sprite_walk_4_1"],
                          _scaled_images["elucidate_no_sprite_walk_4_2"]], }, "attack": {
                "up": [_scaled_images["elucidate_no_sprite_attack_1_1"],
                       _scaled_images["elucidate_no_sprite_attack_1_2"]],
                "down": [_scaled_images["elucidate_no_sprite_attack_2_1"],
                         _scaled_images["elucidate_no_sprite_attack_2_2"]],
                "left": [_scaled_images["elucidate_no_sprite_attack_3_1"],
                         _scaled_images["elucidate_no_sprite_attack_3_2"]],
                "right": [_scaled_images["elucidate_no_sprite_attack_4_1"],
                          _scaled_images["elucidate_no_sprite_attack_4_2"]], }, }, "merchant_guild_member": {
            "idle": {"up": _scaled_images["elucidate_idle_merchant_guild_npc_up"],
                     "down": _scaled_images["elucidate_idle_merchant_guild_npc_down"],
                     "left": _scaled_images["elucidate_idle_merchant_guild_npc_left"],
                     "right": _scaled_images["elucidate_idle_merchant_guild_npc_right"], }, "walk": {
                "up": [_scaled_images["elucidate_no_sprite_walk_1_1"], _scaled_images["elucidate_no_sprite_walk_1_2"]],
                "down": [_scaled_images["elucidate_no_sprite_walk_2_1"],
                         _scaled_images["elucidate_no_sprite_walk_2_2"]],
                "left": [_scaled_images["elucidate_no_sprite_walk_3_1"],
                         _scaled_images["elucidate_no_sprite_walk_3_2"]],
                "right": [_scaled_images["elucidate_no_sprite_walk_4_1"],
                          _scaled_images["elucidate_no_sprite_walk_4_2"]], }, "attack": {
                "up": [_scaled_images["elucidate_no_sprite_attack_1_1"],
                       _scaled_images["elucidate_no_sprite_attack_1_2"]],
                "down": [_scaled_images["elucidate_no_sprite_attack_2_1"],
                         _scaled_images["elucidate_no_sprite_attack_2_2"]],
                "left": [_scaled_images["elucidate_no_sprite_attack_3_1"],
                         _scaled_images["elucidate_no_sprite_attack_3_2"]],
                "right": [_scaled_images["elucidate_no_sprite_attack_4_1"],
                          _scaled_images["elucidate_no_sprite_attack_4_2"]], }, }, "merchant_guild_master": {
            "idle": {"up": _scaled_images["elucidate_idle_merchant_guild_master_npc_up"],
                     "down": _scaled_images["elucidate_idle_merchant_guild_master_npc_down"],
                     "left": _scaled_images["elucidate_idle_merchant_guild_master_npc_left"],
                     "right": _scaled_images["elucidate_idle_merchant_guild_master_npc_right"], }, "walk": {
                "up": [_scaled_images["elucidate_no_sprite_walk_1_1"], _scaled_images["elucidate_no_sprite_walk_1_2"]],
                "down": [_scaled_images["elucidate_no_sprite_walk_2_1"],
                         _scaled_images["elucidate_no_sprite_walk_2_2"]],
                "left": [_scaled_images["elucidate_no_sprite_walk_3_1"],
                         _scaled_images["elucidate_no_sprite_walk_3_2"]],
                "right": [_scaled_images["elucidate_no_sprite_walk_4_1"],
                          _scaled_images["elucidate_no_sprite_walk_4_2"]], }, "attack": {
                "up": [_scaled_images["elucidate_no_sprite_attack_1_1"],
                       _scaled_images["elucidate_no_sprite_attack_1_2"]],
                "down": [_scaled_images["elucidate_no_sprite_attack_2_1"],
                         _scaled_images["elucidate_no_sprite_attack_2_2"]],
                "left": [_scaled_images["elucidate_no_sprite_attack_3_1"],
                         _scaled_images["elucidate_no_sprite_attack_3_2"]],
                "right": [_scaled_images["elucidate_no_sprite_attack_4_1"],
                          _scaled_images["elucidate_no_sprite_attack_4_2"]], }, }, "harbor_captain": {
            "idle": {"up": _scaled_images["elucidate_idle_harbor_captain_npc_up"],
                     "down": _scaled_images["elucidate_idle_harbor_captain_npc_down"],
                     "left": _scaled_images["elucidate_idle_harbor_captain_npc_left"],
                     "right": _scaled_images["elucidate_idle_harbor_captain_npc_right"], }, "walk": {
                "up": [_scaled_images["elucidate_no_sprite_walk_1_1"], _scaled_images["elucidate_no_sprite_walk_1_2"]],
                "down": [_scaled_images["elucidate_no_sprite_walk_2_1"],
                         _scaled_images["elucidate_no_sprite_walk_2_2"]],
                "left": [_scaled_images["elucidate_no_sprite_walk_3_1"],
                         _scaled_images["elucidate_no_sprite_walk_3_2"]],
                "right": [_scaled_images["elucidate_no_sprite_walk_4_1"],
                          _scaled_images["elucidate_no_sprite_walk_4_2"]], }, "attack": {
                "up": [_scaled_images["elucidate_no_sprite_attack_1_1"],
                       _scaled_images["elucidate_no_sprite_attack_1_2"]],
                "down": [_scaled_images["elucidate_no_sprite_attack_2_1"],
                         _scaled_images["elucidate_no_sprite_attack_2_2"]],
                "left": [_scaled_images["elucidate_no_sprite_attack_3_1"],
                         _scaled_images["elucidate_no_sprite_attack_3_2"]],
                "right": [_scaled_images["elucidate_no_sprite_attack_4_1"],
                          _scaled_images["elucidate_no_sprite_attack_4_2"]], }, }, "male_villager_variant": {
            "idle": {"up": _scaled_images["elucidate_idle_male_villager_variant_npc_up"],
                     "down": _scaled_images["elucidate_idle_male_villager_variant_npc_down"],
                     "left": _scaled_images["elucidate_idle_male_villager_variant_npc_left"],
                     "right": _scaled_images["elucidate_idle_male_villager_variant_npc_right"], }, "walk": {
                "up": [_scaled_images["elucidate_no_sprite_walk_1_1"], _scaled_images["elucidate_no_sprite_walk_1_2"]],
                "down": [_scaled_images["elucidate_no_sprite_walk_2_1"],
                         _scaled_images["elucidate_no_sprite_walk_2_2"]],
                "left": [_scaled_images["elucidate_no_sprite_walk_3_1"],
                         _scaled_images["elucidate_no_sprite_walk_3_2"]],
                "right": [_scaled_images["elucidate_no_sprite_walk_4_1"],
                          _scaled_images["elucidate_no_sprite_walk_4_2"]], }, "attack": {
                "up": [_scaled_images["elucidate_no_sprite_attack_1_1"],
                       _scaled_images["elucidate_no_sprite_attack_1_2"]],
                "down": [_scaled_images["elucidate_no_sprite_attack_2_1"],
                         _scaled_images["elucidate_no_sprite_attack_2_2"]],
                "left": [_scaled_images["elucidate_no_sprite_attack_3_1"],
                         _scaled_images["elucidate_no_sprite_attack_3_2"]],
                "right": [_scaled_images["elucidate_no_sprite_attack_4_1"],
                          _scaled_images["elucidate_no_sprite_attack_4_2"]], }, }, "male_villager": {
            "idle": {"up": _scaled_images["elucidate_idle_male_villager_npc_up"],
                     "down": _scaled_images["elucidate_idle_male_villager_npc_down"],
                     "left": _scaled_images["elucidate_idle_male_villager_npc_left"],
                     "right": _scaled_images["elucidate_idle_male_villager_npc_right"], }, "walk": {
                "up": [_scaled_images["elucidate_no_sprite_walk_1_1"], _scaled_images["elucidate_no_sprite_walk_1_2"]],
                "down": [_scaled_images["elucidate_no_sprite_walk_2_1"],
                         _scaled_images["elucidate_no_sprite_walk_2_2"]],
                "left": [_scaled_images["elucidate_no_sprite_walk_3_1"],
                         _scaled_images["elucidate_no_sprite_walk_3_2"]],
                "right": [_scaled_images["elucidate_no_sprite_walk_4_1"],
                          _scaled_images["elucidate_no_sprite_walk_4_2"]], }, "attack": {
                "up": [_scaled_images["elucidate_no_sprite_attack_1_1"],
                       _scaled_images["elucidate_no_sprite_attack_1_2"]],
                "down": [_scaled_images["elucidate_no_sprite_attack_2_1"],
                         _scaled_images["elucidate_no_sprite_attack_2_2"]],
                "left": [_scaled_images["elucidate_no_sprite_attack_3_1"],
                         _scaled_images["elucidate_no_sprite_attack_3_2"]],
                "right": [_scaled_images["elucidate_no_sprite_attack_4_1"],
                          _scaled_images["elucidate_no_sprite_attack_4_2"]], }, }, "female_villager_variant": {
            "idle": {"up": _scaled_images["elucidate_idle_female_villager_variant_npc_up"],
                     "down": _scaled_images["elucidate_idle_female_villager_variant_npc_down"],
                     "left": _scaled_images["elucidate_idle_female_villager_variant_npc_left"],
                     "right": _scaled_images["elucidate_idle_female_villager_variant_npc_right"], }, "walk": {
                "up": [_scaled_images["elucidate_no_sprite_walk_1_1"], _scaled_images["elucidate_no_sprite_walk_1_2"]],
                "down": [_scaled_images["elucidate_no_sprite_walk_2_1"],
                         _scaled_images["elucidate_no_sprite_walk_2_2"]],
                "left": [_scaled_images["elucidate_no_sprite_walk_3_1"],
                         _scaled_images["elucidate_no_sprite_walk_3_2"]],
                "right": [_scaled_images["elucidate_no_sprite_walk_4_1"],
                          _scaled_images["elucidate_no_sprite_walk_4_2"]], }, "attack": {
                "up": [_scaled_images["elucidate_no_sprite_attack_1_1"],
                       _scaled_images["elucidate_no_sprite_attack_1_2"]],
                "down": [_scaled_images["elucidate_no_sprite_attack_2_1"],
                         _scaled_images["elucidate_no_sprite_attack_2_2"]],
                "left": [_scaled_images["elucidate_no_sprite_attack_3_1"],
                         _scaled_images["elucidate_no_sprite_attack_3_2"]],
                "right": [_scaled_images["elucidate_no_sprite_attack_4_1"],
                          _scaled_images["elucidate_no_sprite_attack_4_2"]], }, }, "female_villager": {
            "idle": {"up": _scaled_images["elucidate_idle_female_villager_npc_up"],
                     "down": _scaled_images["elucidate_idle_female_villager_npc_down"],
                     "left": _scaled_images["elucidate_idle_female_villager_npc_left"],
                     "right": _scaled_images["elucidate_idle_female_villager_npc_right"], }, "walk": {
                "up": [_scaled_images["elucidate_no_sprite_walk_1_1"], _scaled_images["elucidate_no_sprite_walk_1_2"]],
                "down": [_scaled_images["elucidate_no_sprite_walk_2_1"],
                         _scaled_images["elucidate_no_sprite_walk_2_2"]],
                "left": [_scaled_images["elucidate_no_sprite_walk_3_1"],
                         _scaled_images["elucidate_no_sprite_walk_3_2"]],
                "right": [_scaled_images["elucidate_no_sprite_walk_4_1"],
                          _scaled_images["elucidate_no_sprite_walk_4_2"]], }, "attack": {
                "up": [_scaled_images["elucidate_no_sprite_attack_1_1"],
                       _scaled_images["elucidate_no_sprite_attack_1_2"]],
                "down": [_scaled_images["elucidate_no_sprite_attack_2_1"],
                         _scaled_images["elucidate_no_sprite_attack_2_2"]],
                "left": [_scaled_images["elucidate_no_sprite_attack_3_1"],
                         _scaled_images["elucidate_no_sprite_attack_3_2"]],
                "right": [_scaled_images["elucidate_no_sprite_attack_4_1"],
                          _scaled_images["elucidate_no_sprite_attack_4_2"]], }, }, "guards": {
            "idle": {"up": _scaled_images["elucidate_idle_guards_npc_up"],
                     "down": _scaled_images["elucidate_idle_guards_npc_down"],
                     "left": _scaled_images["elucidate_idle_guards_npc_left"],
                     "right": _scaled_images["elucidate_idle_guards_npc_right"], }, "walk": {
                "up": [_scaled_images["elucidate_no_sprite_walk_1_1"], _scaled_images["elucidate_no_sprite_walk_1_2"]],
                "down": [_scaled_images["elucidate_no_sprite_walk_2_1"],
                         _scaled_images["elucidate_no_sprite_walk_2_2"]],
                "left": [_scaled_images["elucidate_no_sprite_walk_3_1"],
                         _scaled_images["elucidate_no_sprite_walk_3_2"]],
                "right": [_scaled_images["elucidate_no_sprite_walk_4_1"],
                          _scaled_images["elucidate_no_sprite_walk_4_2"]], }, "attack": {
                "up": [_scaled_images["elucidate_no_sprite_attack_1_1"],
                       _scaled_images["elucidate_no_sprite_attack_1_2"]],
                "down": [_scaled_images["elucidate_no_sprite_attack_2_1"],
                         _scaled_images["elucidate_no_sprite_attack_2_2"]],
                "left": [_scaled_images["elucidate_no_sprite_attack_3_1"],
                         _scaled_images["elucidate_no_sprite_attack_3_2"]],
                "right": [_scaled_images["elucidate_no_sprite_attack_4_1"],
                          _scaled_images["elucidate_no_sprite_attack_4_2"]], }, }, "guard_captain": {
            "idle": {"up": _scaled_images["elucidate_idle_guard_captain_npc_up"],
                     "down": _scaled_images["elucidate_idle_guard_captain_npc_down"],
                     "left": _scaled_images["elucidate_idle_guard_captain_npc_left"],
                     "right": _scaled_images["elucidate_idle_guard_captain_npc_right"], }, "walk": {
                "up": [_scaled_images["elucidate_no_sprite_walk_1_1"], _scaled_images["elucidate_no_sprite_walk_1_2"]],
                "down": [_scaled_images["elucidate_no_sprite_walk_2_1"],
                         _scaled_images["elucidate_no_sprite_walk_2_2"]],
                "left": [_scaled_images["elucidate_no_sprite_walk_3_1"],
                         _scaled_images["elucidate_no_sprite_walk_3_2"]],
                "right": [_scaled_images["elucidate_no_sprite_walk_4_1"],
                          _scaled_images["elucidate_no_sprite_walk_4_2"]], }, "attack": {
                "up": [_scaled_images["elucidate_no_sprite_attack_1_1"],
                       _scaled_images["elucidate_no_sprite_attack_1_2"]],
                "down": [_scaled_images["elucidate_no_sprite_attack_2_1"],
                         _scaled_images["elucidate_no_sprite_attack_2_2"]],
                "left": [_scaled_images["elucidate_no_sprite_attack_3_1"],
                         _scaled_images["elucidate_no_sprite_attack_3_2"]],
                "right": [_scaled_images["elucidate_no_sprite_attack_4_1"],
                          _scaled_images["elucidate_no_sprite_attack_4_2"]], }, }, "draft_officer": {
            "idle": {"up": _scaled_images["elucidate_idle_draft_officer_npc_up"],
                     "down": _scaled_images["elucidate_idle_draft_officer_npc_down"],
                     "left": _scaled_images["elucidate_idle_draft_officer_npc_left"],
                     "right": _scaled_images["elucidate_idle_draft_officer_npc_right"], }, "walk": {
                "up": [_scaled_images["elucidate_no_sprite_walk_1_1"], _scaled_images["elucidate_no_sprite_walk_1_2"]],
                "down": [_scaled_images["elucidate_no_sprite_walk_2_1"],
                         _scaled_images["elucidate_no_sprite_walk_2_2"]],
                "left": [_scaled_images["elucidate_no_sprite_walk_3_1"],
                         _scaled_images["elucidate_no_sprite_walk_3_2"]],
                "right": [_scaled_images["elucidate_no_sprite_walk_4_1"],
                          _scaled_images["elucidate_no_sprite_walk_4_2"]], }, "attack": {
                "up": [_scaled_images["elucidate_no_sprite_attack_1_1"],
                       _scaled_images["elucidate_no_sprite_attack_1_2"]],
                "down": [_scaled_images["elucidate_no_sprite_attack_2_1"],
                         _scaled_images["elucidate_no_sprite_attack_2_2"]],
                "left": [_scaled_images["elucidate_no_sprite_attack_3_1"],
                         _scaled_images["elucidate_no_sprite_attack_3_2"]],
                "right": [_scaled_images["elucidate_no_sprite_attack_4_1"],
                          _scaled_images["elucidate_no_sprite_attack_4_2"]], }, }, "male_civilian": {
            "idle": {"up": _scaled_images["elucidate_idle_male_civilian_npc_up"],
                     "down": _scaled_images["elucidate_idle_male_civilian_npc_down"],
                     "left": _scaled_images["elucidate_idle_male_civilian_npc_left"],
                     "right": _scaled_images["elucidate_idle_male_civilian_npc_right"], }, "walk": {
                "up": [_scaled_images["elucidate_no_sprite_walk_1_1"], _scaled_images["elucidate_no_sprite_walk_1_2"]],
                "down": [_scaled_images["elucidate_no_sprite_walk_2_1"],
                         _scaled_images["elucidate_no_sprite_walk_2_2"]],
                "left": [_scaled_images["elucidate_no_sprite_walk_3_1"],
                         _scaled_images["elucidate_no_sprite_walk_3_2"]],
                "right": [_scaled_images["elucidate_no_sprite_walk_4_1"],
                          _scaled_images["elucidate_no_sprite_walk_4_2"]], }, "attack": {
                "up": [_scaled_images["elucidate_no_sprite_attack_1_1"],
                       _scaled_images["elucidate_no_sprite_attack_1_2"]],
                "down": [_scaled_images["elucidate_no_sprite_attack_2_1"],
                         _scaled_images["elucidate_no_sprite_attack_2_2"]],
                "left": [_scaled_images["elucidate_no_sprite_attack_3_1"],
                         _scaled_images["elucidate_no_sprite_attack_3_2"]],
                "right": [_scaled_images["elucidate_no_sprite_attack_4_1"],
                          _scaled_images["elucidate_no_sprite_attack_4_2"]], }, }, "female_civilian": {
            "idle": {"up": _scaled_images["elucidate_idle_female_civilian_npc_up"],
                     "down": _scaled_images["elucidate_idle_female_civilian_npc_down"],
                     "left": _scaled_images["elucidate_idle_female_civilian_npc_left"],
                     "right": _scaled_images["elucidate_idle_female_civilian_npc_right"], }, "walk": {
                "up": [_scaled_images["elucidate_no_sprite_walk_1_1"], _scaled_images["elucidate_no_sprite_walk_1_2"]],
                "down": [_scaled_images["elucidate_no_sprite_walk_2_1"],
                         _scaled_images["elucidate_no_sprite_walk_2_2"]],
                "left": [_scaled_images["elucidate_no_sprite_walk_3_1"],
                         _scaled_images["elucidate_no_sprite_walk_3_2"]],
                "right": [_scaled_images["elucidate_no_sprite_walk_4_1"],
                          _scaled_images["elucidate_no_sprite_walk_4_2"]], }, "attack": {
                "up": [_scaled_images["elucidate_no_sprite_attack_1_1"],
                       _scaled_images["elucidate_no_sprite_attack_1_2"]],
                "down": [_scaled_images["elucidate_no_sprite_attack_2_1"],
                         _scaled_images["elucidate_no_sprite_attack_2_2"]],
                "left": [_scaled_images["elucidate_no_sprite_attack_3_1"],
                         _scaled_images["elucidate_no_sprite_attack_3_2"]],
                "right": [_scaled_images["elucidate_no_sprite_attack_4_1"],
                          _scaled_images["elucidate_no_sprite_attack_4_2"]], }, }, "male_civilian_variant": {
            "idle": {"up": _scaled_images["elucidate_idle_male_civilian_variant_npc_up"],
                     "down": _scaled_images["elucidate_idle_male_civilian_variant_npc_down"],
                     "left": _scaled_images["elucidate_idle_male_civilian_variant_npc_left"],
                     "right": _scaled_images["elucidate_idle_male_civilian_variant_npc_right"], }, "walk": {
                "up": [_scaled_images["elucidate_no_sprite_walk_1_1"], _scaled_images["elucidate_no_sprite_walk_1_2"]],
                "down": [_scaled_images["elucidate_no_sprite_walk_2_1"],
                         _scaled_images["elucidate_no_sprite_walk_2_2"]],
                "left": [_scaled_images["elucidate_no_sprite_walk_3_1"],
                         _scaled_images["elucidate_no_sprite_walk_3_2"]],
                "right": [_scaled_images["elucidate_no_sprite_walk_4_1"],
                          _scaled_images["elucidate_no_sprite_walk_4_2"]], }, "attack": {
                "up": [_scaled_images["elucidate_no_sprite_attack_1_1"],
                       _scaled_images["elucidate_no_sprite_attack_1_2"]],
                "down": [_scaled_images["elucidate_no_sprite_attack_2_1"],
                         _scaled_images["elucidate_no_sprite_attack_2_2"]],
                "left": [_scaled_images["elucidate_no_sprite_attack_3_1"],
                         _scaled_images["elucidate_no_sprite_attack_3_2"]],
                "right": [_scaled_images["elucidate_no_sprite_attack_4_1"],
                          _scaled_images["elucidate_no_sprite_attack_4_2"]], }, }, "female_civilian_variant": {
            "idle": {"up": _scaled_images["elucidate_idle_female_civilian_variant_npc_up"],
                     "down": _scaled_images["elucidate_idle_female_civilian_variant_npc_down"],
                     "left": _scaled_images["elucidate_idle_female_civilian_variant_npc_left"],
                     "right": _scaled_images["elucidate_idle_female_civilian_variant_npc_right"], }, "walk": {
                "up": [_scaled_images["elucidate_no_sprite_walk_1_1"], _scaled_images["elucidate_no_sprite_walk_1_2"]],
                "down": [_scaled_images["elucidate_no_sprite_walk_2_1"],
                         _scaled_images["elucidate_no_sprite_walk_2_2"]],
                "left": [_scaled_images["elucidate_no_sprite_walk_3_1"],
                         _scaled_images["elucidate_no_sprite_walk_3_2"]],
                "right": [_scaled_images["elucidate_no_sprite_walk_4_1"],
                          _scaled_images["elucidate_no_sprite_walk_4_2"]], }, "attack": {
                "up": [_scaled_images["elucidate_no_sprite_attack_1_1"],
                       _scaled_images["elucidate_no_sprite_attack_1_2"]],
                "down": [_scaled_images["elucidate_no_sprite_attack_2_1"],
                         _scaled_images["elucidate_no_sprite_attack_2_2"]],
                "left": [_scaled_images["elucidate_no_sprite_attack_3_1"],
                         _scaled_images["elucidate_no_sprite_attack_3_2"]],
                "right": [_scaled_images["elucidate_no_sprite_attack_4_1"],
                          _scaled_images["elucidate_no_sprite_attack_4_2"]], }, }, "blacksmith": {
            "idle": {"up": _scaled_images["elucidate_idle_blacksmith_npc_up"],
                     "down": _scaled_images["elucidate_idle_blacksmith_npc_down"],
                     "left": _scaled_images["elucidate_idle_blacksmith_npc_left"],
                     "right": _scaled_images["elucidate_idle_blacksmith_npc_right"], }, "walk": {
                "up": [_scaled_images["elucidate_no_sprite_walk_1_1"], _scaled_images["elucidate_no_sprite_walk_1_2"]],
                "down": [_scaled_images["elucidate_no_sprite_walk_2_1"],
                         _scaled_images["elucidate_no_sprite_walk_2_2"]],
                "left": [_scaled_images["elucidate_no_sprite_walk_3_1"],
                         _scaled_images["elucidate_no_sprite_walk_3_2"]],
                "right": [_scaled_images["elucidate_no_sprite_walk_4_1"],
                          _scaled_images["elucidate_no_sprite_walk_4_2"]], }, "attack": {
                "up": [_scaled_images["elucidate_no_sprite_attack_1_1"],
                       _scaled_images["elucidate_no_sprite_attack_1_2"]],
                "down": [_scaled_images["elucidate_no_sprite_attack_2_1"],
                         _scaled_images["elucidate_no_sprite_attack_2_2"]],
                "left": [_scaled_images["elucidate_no_sprite_attack_3_1"],
                         _scaled_images["elucidate_no_sprite_attack_3_2"]],
                "right": [_scaled_images["elucidate_no_sprite_attack_4_1"],
                          _scaled_images["elucidate_no_sprite_attack_4_2"]], }, }, "caligo_manifestation": {
            "idle": {"up": _scaled_images["elucidate_idle_caligo_manifestation"],
                     "down": _scaled_images["elucidate_idle_caligo_manifestation"],
                     "left": _scaled_images["elucidate_idle_caligo_manifestation"],
                     "right": _scaled_images["elucidate_idle_caligo_manifestation"]}, "walk": {
                "up": [_scaled_images["elucidate_idle_caligo_manifestation"],
                       _scaled_images["elucidate_idle_caligo_manifestation"]],
                "down": [_scaled_images["elucidate_idle_caligo_manifestation"],
                         _scaled_images["elucidate_idle_caligo_manifestation"]],
                "left": [_scaled_images["elucidate_idle_caligo_manifestation"],
                         _scaled_images["elucidate_idle_caligo_manifestation"]],
                "right": [_scaled_images["elucidate_idle_caligo_manifestation"],
                          _scaled_images["elucidate_idle_caligo_manifestation"]]}, "attack": {
                "up": [_scaled_images["elucidate_no_sprite_attack_1_1"],
                       _scaled_images["elucidate_no_sprite_attack_1_2"]],
                "down": [_scaled_images["elucidate_no_sprite_attack_2_1"],
                         _scaled_images["elucidate_no_sprite_attack_2_2"]],
                "left": [_scaled_images["elucidate_no_sprite_attack_3_1"],
                         _scaled_images["elucidate_no_sprite_attack_3_2"]],
                "right": [_scaled_images["elucidate_no_sprite_attack_4_1"],
                          _scaled_images["elucidate_no_sprite_attack_4_2"]], }, }, "imprisoned_experiment_1": {
            "idle": {"up": _scaled_images["elucidate_idle_imprisoned_experiment_1_npc_down"],
                     "down": _scaled_images["elucidate_idle_imprisoned_experiment_1_npc_down"],
                     "left": _scaled_images["elucidate_idle_imprisoned_experiment_1_npc_down"],
                     "right": _scaled_images["elucidate_idle_imprisoned_experiment_1_npc_down"], }, "walk": {
                "up": [_scaled_images["elucidate_idle_imprisoned_experiment_1_npc_down"],
                       _scaled_images["elucidate_idle_imprisoned_experiment_1_npc_down"]],
                "down": [_scaled_images["elucidate_idle_imprisoned_experiment_1_npc_down"],
                         _scaled_images["elucidate_idle_imprisoned_experiment_1_npc_down"]],
                "left": [_scaled_images["elucidate_idle_imprisoned_experiment_1_npc_down"],
                         _scaled_images["elucidate_idle_imprisoned_experiment_1_npc_down"]],
                "right": [_scaled_images["elucidate_idle_imprisoned_experiment_1_npc_down"],
                          _scaled_images["elucidate_idle_imprisoned_experiment_1_npc_down"]], }, "attack": {
                "up": [_scaled_images["elucidate_no_sprite_attack_1_1"],
                       _scaled_images["elucidate_no_sprite_attack_1_2"]],
                "down": [_scaled_images["elucidate_no_sprite_attack_2_1"],
                         _scaled_images["elucidate_no_sprite_attack_2_2"]],
                "left": [_scaled_images["elucidate_no_sprite_attack_3_1"],
                         _scaled_images["elucidate_no_sprite_attack_3_2"]],
                "right": [_scaled_images["elucidate_no_sprite_attack_4_1"],
                          _scaled_images["elucidate_no_sprite_attack_4_2"]], }, }, "imprisoned_experiment_2": {
            "idle": {"up": _scaled_images["elucidate_idle_imprisoned_experiment_2_npc_down"],
                     "down": _scaled_images["elucidate_idle_imprisoned_experiment_2_npc_down"],
                     "left": _scaled_images["elucidate_idle_imprisoned_experiment_2_npc_down"],
                     "right": _scaled_images["elucidate_idle_imprisoned_experiment_2_npc_down"], }, "walk": {
                "up": [_scaled_images["elucidate_idle_imprisoned_experiment_2_npc_down"],
                       _scaled_images["elucidate_idle_imprisoned_experiment_2_npc_down"]],
                "down": [_scaled_images["elucidate_idle_imprisoned_experiment_2_npc_down"],
                         _scaled_images["elucidate_idle_imprisoned_experiment_2_npc_down"]],
                "left": [_scaled_images["elucidate_idle_imprisoned_experiment_2_npc_down"],
                         _scaled_images["elucidate_idle_imprisoned_experiment_2_npc_down"]],
                "right": [_scaled_images["elucidate_idle_imprisoned_experiment_2_npc_down"],
                          _scaled_images["elucidate_idle_imprisoned_experiment_2_npc_down"]], }, "attack": {
                "up": [_scaled_images["elucidate_no_sprite_attack_1_1"],
                       _scaled_images["elucidate_no_sprite_attack_1_2"]],
                "down": [_scaled_images["elucidate_no_sprite_attack_2_1"],
                         _scaled_images["elucidate_no_sprite_attack_2_2"]],
                "left": [_scaled_images["elucidate_no_sprite_attack_3_1"],
                         _scaled_images["elucidate_no_sprite_attack_3_2"]],
                "right": [_scaled_images["elucidate_no_sprite_attack_4_1"],
                          _scaled_images["elucidate_no_sprite_attack_4_2"]], }, }, "imprisoned_experiment_hostile": {
            "idle": {"up": _scaled_images["elucidate_idle_imprisoned_experiment_hostile_npc_down"],
                     "down": _scaled_images["elucidate_idle_imprisoned_experiment_hostile_npc_down"],
                     "left": _scaled_images["elucidate_idle_imprisoned_experiment_hostile_npc_down"],
                     "right": _scaled_images["elucidate_idle_imprisoned_experiment_hostile_npc_down"], }, "walk": {
                "up": [_scaled_images["elucidate_idle_imprisoned_experiment_hostile_npc_down"],
                       _scaled_images["elucidate_idle_imprisoned_experiment_hostile_npc_down"]],
                "down": [_scaled_images["elucidate_idle_imprisoned_experiment_hostile_npc_down"],
                         _scaled_images["elucidate_idle_imprisoned_experiment_hostile_npc_down"]],
                "left": [_scaled_images["elucidate_idle_imprisoned_experiment_hostile_npc_down"],
                         _scaled_images["elucidate_idle_imprisoned_experiment_hostile_npc_down"]],
                "right": [_scaled_images["elucidate_idle_imprisoned_experiment_hostile_npc_down"],
                          _scaled_images["elucidate_idle_imprisoned_experiment_hostile_npc_down"]], }, "attack": {
                "up": [_scaled_images["elucidate_no_sprite_attack_1_1"],
                       _scaled_images["elucidate_no_sprite_attack_1_2"]],
                "down": [_scaled_images["elucidate_no_sprite_attack_2_1"],
                         _scaled_images["elucidate_no_sprite_attack_2_2"]],
                "left": [_scaled_images["elucidate_no_sprite_attack_3_1"],
                         _scaled_images["elucidate_no_sprite_attack_3_2"]],
                "right": [_scaled_images["elucidate_no_sprite_attack_4_1"],
                          _scaled_images["elucidate_no_sprite_attack_4_2"]], }, }, "church_medical_staff": {
            "idle": {"up": _scaled_images["elucidate_idle_church_medical_staff_npc_up"],
                     "down": _scaled_images["elucidate_idle_church_medical_staff_npc_down"],
                     "left": _scaled_images["elucidate_idle_church_medical_staff_npc_left"],
                     "right": _scaled_images["elucidate_idle_church_medical_staff_npc_right"], }, "walk": {
                "up": [_scaled_images["elucidate_no_sprite_walk_1_1"], _scaled_images["elucidate_no_sprite_walk_1_2"]],
                "down": [_scaled_images["elucidate_no_sprite_walk_2_1"],
                         _scaled_images["elucidate_no_sprite_walk_2_2"]],
                "left": [_scaled_images["elucidate_no_sprite_walk_3_1"],
                         _scaled_images["elucidate_no_sprite_walk_3_2"]],
                "right": [_scaled_images["elucidate_no_sprite_walk_4_1"],
                          _scaled_images["elucidate_no_sprite_walk_4_2"]], }, "attack": {
                "up": [_scaled_images["elucidate_no_sprite_attack_1_1"],
                       _scaled_images["elucidate_no_sprite_attack_1_2"]],
                "down": [_scaled_images["elucidate_no_sprite_attack_2_1"],
                         _scaled_images["elucidate_no_sprite_attack_2_2"]],
                "left": [_scaled_images["elucidate_no_sprite_attack_3_1"],
                         _scaled_images["elucidate_no_sprite_attack_3_2"]],
                "right": [_scaled_images["elucidate_no_sprite_attack_4_1"],
                          _scaled_images["elucidate_no_sprite_attack_4_2"]], }, }, "female_market_merchant": {
            "idle": {"up": _scaled_images["elucidate_idle_female_market_merchant_npc_up"],
                     "down": _scaled_images["elucidate_idle_female_market_merchant_npc_down"],
                     "left": _scaled_images["elucidate_idle_female_market_merchant_npc_left"],
                     "right": _scaled_images["elucidate_idle_female_market_merchant_npc_right"], }, "walk": {
                "up": [_scaled_images["elucidate_no_sprite_walk_1_1"], _scaled_images["elucidate_no_sprite_walk_1_2"]],
                "down": [_scaled_images["elucidate_no_sprite_walk_2_1"],
                         _scaled_images["elucidate_no_sprite_walk_2_2"]],
                "left": [_scaled_images["elucidate_no_sprite_walk_3_1"],
                         _scaled_images["elucidate_no_sprite_walk_3_2"]],
                "right": [_scaled_images["elucidate_no_sprite_walk_4_1"],
                          _scaled_images["elucidate_no_sprite_walk_4_2"]], }, "attack": {
                "up": [_scaled_images["elucidate_no_sprite_attack_1_1"],
                       _scaled_images["elucidate_no_sprite_attack_1_2"]],
                "down": [_scaled_images["elucidate_no_sprite_attack_2_1"],
                         _scaled_images["elucidate_no_sprite_attack_2_2"]],
                "left": [_scaled_images["elucidate_no_sprite_attack_3_1"],
                         _scaled_images["elucidate_no_sprite_attack_3_2"]],
                "right": [_scaled_images["elucidate_no_sprite_attack_4_1"],
                          _scaled_images["elucidate_no_sprite_attack_4_2"]], }, }, "male_market_merchant": {
            "idle": {"up": _scaled_images["elucidate_idle_male_market_merchant_npc_up"],
                     "down": _scaled_images["elucidate_idle_male_market_merchant_npc_down"],
                     "left": _scaled_images["elucidate_idle_male_market_merchant_npc_left"],
                     "right": _scaled_images["elucidate_idle_male_market_merchant_npc_right"], }, "walk": {
                "up": [_scaled_images["elucidate_no_sprite_walk_1_1"], _scaled_images["elucidate_no_sprite_walk_1_2"]],
                "down": [_scaled_images["elucidate_no_sprite_walk_2_1"],
                         _scaled_images["elucidate_no_sprite_walk_2_2"]],
                "left": [_scaled_images["elucidate_no_sprite_walk_3_1"],
                         _scaled_images["elucidate_no_sprite_walk_3_2"]],
                "right": [_scaled_images["elucidate_no_sprite_walk_4_1"],
                          _scaled_images["elucidate_no_sprite_walk_4_2"]], }, "attack": {
                "up": [_scaled_images["elucidate_no_sprite_attack_1_1"],
                       _scaled_images["elucidate_no_sprite_attack_1_2"]],
                "down": [_scaled_images["elucidate_no_sprite_attack_2_1"],
                         _scaled_images["elucidate_no_sprite_attack_2_2"]],
                "left": [_scaled_images["elucidate_no_sprite_attack_3_1"],
                         _scaled_images["elucidate_no_sprite_attack_3_2"]],
                "right": [_scaled_images["elucidate_no_sprite_attack_4_1"],
                          _scaled_images["elucidate_no_sprite_attack_4_2"]], }, }, "ghost_memory1": {
            "idle": {"up": _scaled_images["elucidate_idle_ghost_memory1_npc_right"],
                     "down": _scaled_images["elucidate_idle_ghost_memory1_npc_right"],
                     "left": _scaled_images["elucidate_idle_ghost_memory1_npc_left"],
                     "right": _scaled_images["elucidate_idle_ghost_memory1_npc_right"], }, "walk": {
                "up": [_scaled_images["elucidate_idle_ghost_memory1_npc_right"],
                       _scaled_images["elucidate_idle_ghost_memory1_npc_right"]],
                "down": [_scaled_images["elucidate_idle_ghost_memory1_npc_right"],
                         _scaled_images["elucidate_idle_ghost_memory1_npc_right"]],
                "left": [_scaled_images["elucidate_idle_ghost_memory1_npc_left"],
                         _scaled_images["elucidate_idle_ghost_memory1_npc_left"]],
                "right": [_scaled_images["elucidate_idle_ghost_memory1_npc_right"],
                          _scaled_images["elucidate_idle_ghost_memory1_npc_right"]], }, "attack": {
                "up": [_scaled_images["elucidate_no_sprite_attack_1_1"],
                       _scaled_images["elucidate_no_sprite_attack_1_2"]],
                "down": [_scaled_images["elucidate_no_sprite_attack_2_1"],
                         _scaled_images["elucidate_no_sprite_attack_2_2"]],
                "left": [_scaled_images["elucidate_no_sprite_attack_3_1"],
                         _scaled_images["elucidate_no_sprite_attack_3_2"]],
                "right": [_scaled_images["elucidate_no_sprite_attack_4_1"],
                          _scaled_images["elucidate_no_sprite_attack_4_2"]], }, }, "ghost_memory2": {
            "idle": {"up": _scaled_images["elucidate_idle_ghost_memory2_npc_right"],
                     "down": _scaled_images["elucidate_idle_ghost_memory2_npc_right"],
                     "left": _scaled_images["elucidate_idle_ghost_memory2_npc_left"],
                     "right": _scaled_images["elucidate_idle_ghost_memory2_npc_right"], }, "walk": {
                "up": [_scaled_images["elucidate_idle_ghost_memory2_npc_right"],
                       _scaled_images["elucidate_idle_ghost_memory2_npc_right"]],
                "down": [_scaled_images["elucidate_idle_ghost_memory2_npc_right"],
                         _scaled_images["elucidate_idle_ghost_memory2_npc_right"]],
                "left": [_scaled_images["elucidate_idle_ghost_memory2_npc_left"],
                         _scaled_images["elucidate_idle_ghost_memory2_npc_left"]],
                "right": [_scaled_images["elucidate_idle_ghost_memory2_npc_right"],
                          _scaled_images["elucidate_idle_ghost_memory2_npc_right"]], }, "attack": {
                "up": [_scaled_images["elucidate_no_sprite_attack_1_1"],
                       _scaled_images["elucidate_no_sprite_attack_1_2"]],
                "down": [_scaled_images["elucidate_no_sprite_attack_2_1"],
                         _scaled_images["elucidate_no_sprite_attack_2_2"]],
                "left": [_scaled_images["elucidate_no_sprite_attack_3_1"],
                         _scaled_images["elucidate_no_sprite_attack_3_2"]],
                "right": [_scaled_images["elucidate_no_sprite_attack_4_1"],
                          _scaled_images["elucidate_no_sprite_attack_4_2"]], }, }, "female_tribal_warrior": {
            "idle": {"up": _scaled_images["elucidate_idle_female_tribal_warrior_npc_up"],
                     "down": _scaled_images["elucidate_idle_female_tribal_warrior_npc_down"],
                     "left": _scaled_images["elucidate_idle_female_tribal_warrior_npc_left"],
                     "right": _scaled_images["elucidate_idle_female_tribal_warrior_npc_right"], }, "walk": {
                "up": [_scaled_images["elucidate_no_sprite_walk_1_1"], _scaled_images["elucidate_no_sprite_walk_1_2"]],
                "down": [_scaled_images["elucidate_no_sprite_walk_2_1"],
                         _scaled_images["elucidate_no_sprite_walk_2_2"]],
                "left": [_scaled_images["elucidate_no_sprite_walk_3_1"],
                         _scaled_images["elucidate_no_sprite_walk_3_2"]],
                "right": [_scaled_images["elucidate_no_sprite_walk_4_1"],
                          _scaled_images["elucidate_no_sprite_walk_4_2"]], }, "attack": {
                "up": [_scaled_images["elucidate_no_sprite_attack_1_1"],
                       _scaled_images["elucidate_no_sprite_attack_1_2"]],
                "down": [_scaled_images["elucidate_no_sprite_attack_2_1"],
                         _scaled_images["elucidate_no_sprite_attack_2_2"]],
                "left": [_scaled_images["elucidate_no_sprite_attack_3_1"],
                         _scaled_images["elucidate_no_sprite_attack_3_2"]],
                "right": [_scaled_images["elucidate_no_sprite_attack_4_1"],
                          _scaled_images["elucidate_no_sprite_attack_4_2"]], }, }, "travelling_bard": {
            "idle": {"up": _scaled_images["elucidate_idle_travelling_bard_npc_up"],
                     "down": _scaled_images["elucidate_idle_travelling_bard_npc_down"],
                     "left": _scaled_images["elucidate_idle_travelling_bard_npc_left"],
                     "right": _scaled_images["elucidate_idle_travelling_bard_npc_right"]},
            "walk": {
                "up": [_scaled_images["elucidate_idle_travelling_bard_npc_up"],
                       _scaled_images["elucidate_idle_travelling_bard_npc_up"]],
                "down": [_scaled_images["elucidate_idle_travelling_bard_npc_down"],
                         _scaled_images["elucidate_idle_travelling_bard_npc_down"]],
                "left": [_scaled_images["elucidate_idle_travelling_bard_npc_left"],
                         _scaled_images["elucidate_idle_travelling_bard_npc_left"]],
                "right": [_scaled_images["elucidate_idle_travelling_bard_npc_right"],
                          _scaled_images["elucidate_idle_travelling_bard_npc_right"]]},
            "attack": {
                "up": [_scaled_images["elucidate_no_sprite_attack_1_1"],
                       _scaled_images["elucidate_no_sprite_attack_1_2"]],
                "down": [_scaled_images["elucidate_no_sprite_attack_2_1"],
                         _scaled_images["elucidate_no_sprite_attack_2_2"]],
                "left": [_scaled_images["elucidate_no_sprite_attack_3_1"],
                         _scaled_images["elucidate_no_sprite_attack_3_2"]],
                "right": [_scaled_images["elucidate_no_sprite_attack_4_1"],
                          _scaled_images["elucidate_no_sprite_attack_4_2"]]}},
        "travelling_merchant": {
            "idle": {"up": _scaled_images["elucidate_idle_supply_merchant_npc_up"],
                     "down": _scaled_images["elucidate_idle_supply_merchant_npc_down"],
                     "left": _scaled_images["elucidate_idle_supply_merchant_npc_left"],
                     "right": _scaled_images["elucidate_idle_supply_merchant_npc_right"]}, "walk": {
                "up": [_scaled_images["elucidate_idle_supply_merchant_npc_up"],
                       _scaled_images["elucidate_idle_supply_merchant_npc_up"]],
                "down": [_scaled_images["elucidate_idle_supply_merchant_npc_down"],
                         _scaled_images["elucidate_idle_supply_merchant_npc_down"]],
                "left": [_scaled_images["elucidate_idle_supply_merchant_npc_left"],
                         _scaled_images["elucidate_idle_supply_merchant_npc_left"]],
                "right": [_scaled_images["elucidate_idle_supply_merchant_npc_right"],
                          _scaled_images["elucidate_idle_supply_merchant_npc_right"]], }, "attack": {
                "up": [_scaled_images["elucidate_no_sprite_attack_1_1"],
                       _scaled_images["elucidate_no_sprite_attack_1_2"]],
                "down": [_scaled_images["elucidate_no_sprite_attack_2_1"],
                         _scaled_images["elucidate_no_sprite_attack_2_2"]],
                "left": [_scaled_images["elucidate_no_sprite_attack_3_1"],
                         _scaled_images["elucidate_no_sprite_attack_3_2"]],
                "right": [_scaled_images["elucidate_no_sprite_attack_4_1"],
                          _scaled_images["elucidate_no_sprite_attack_4_2"]], }, }, "cultist_priest": {
            "idle": {"up": _scaled_images["elucidate_idle_cultist_priest_npc_up"],
                     "down": _scaled_images["elucidate_idle_cultist_priest_npc_down"],
                     "left": _scaled_images["elucidate_idle_cultist_priest_npc_left"],
                     "right": _scaled_images["elucidate_idle_cultist_priest_npc_right"], }, "walk": {
                "up": [_scaled_images["elucidate_no_sprite_walk_1_1"], _scaled_images["elucidate_no_sprite_walk_1_2"]],
                "down": [_scaled_images["elucidate_no_sprite_walk_2_1"],
                         _scaled_images["elucidate_no_sprite_walk_2_2"]],
                "left": [_scaled_images["elucidate_no_sprite_walk_3_1"],
                         _scaled_images["elucidate_no_sprite_walk_3_2"]],
                "right": [_scaled_images["elucidate_no_sprite_walk_4_1"],
                          _scaled_images["elucidate_no_sprite_walk_4_2"]], }, "attack": {
                "up": [_scaled_images["elucidate_no_sprite_attack_1_1"],
                       _scaled_images["elucidate_no_sprite_attack_1_2"]],
                "down": [_scaled_images["elucidate_no_sprite_attack_2_1"],
                         _scaled_images["elucidate_no_sprite_attack_2_2"]],
                "left": [_scaled_images["elucidate_no_sprite_attack_3_1"],
                         _scaled_images["elucidate_no_sprite_attack_3_2"]],
                "right": [_scaled_images["elucidate_no_sprite_attack_4_1"],
                          _scaled_images["elucidate_no_sprite_attack_4_2"]], }, }, "tavern_keeper": {
            "idle": {"up": _scaled_images["elucidate_idle_tavern_keeper_npc_up"],
                     "down": _scaled_images["elucidate_idle_tavern_keeper_npc_down"],
                     "left": _scaled_images["elucidate_idle_tavern_keeper_npc_left"],
                     "right": _scaled_images["elucidate_idle_tavern_keeper_npc_right"], }, "walk": {
                "up": [_scaled_images["elucidate_no_sprite_walk_1_1"], _scaled_images["elucidate_no_sprite_walk_1_2"]],
                "down": [_scaled_images["elucidate_no_sprite_walk_2_1"],
                         _scaled_images["elucidate_no_sprite_walk_2_2"]],
                "left": [_scaled_images["elucidate_no_sprite_walk_3_1"],
                         _scaled_images["elucidate_no_sprite_walk_3_2"]],
                "right": [_scaled_images["elucidate_no_sprite_walk_4_1"],
                          _scaled_images["elucidate_no_sprite_walk_4_2"]], }, "attack": {
                "up": [_scaled_images["elucidate_no_sprite_attack_1_1"],
                       _scaled_images["elucidate_no_sprite_attack_1_2"]],
                "down": [_scaled_images["elucidate_no_sprite_attack_2_1"],
                         _scaled_images["elucidate_no_sprite_attack_2_2"]],
                "left": [_scaled_images["elucidate_no_sprite_attack_3_1"],
                         _scaled_images["elucidate_no_sprite_attack_3_2"]],
                "right": [_scaled_images["elucidate_no_sprite_attack_4_1"],
                          _scaled_images["elucidate_no_sprite_attack_4_2"]], }, }, };

    screen.fill((0, 0, 0))
    try:
        _title_img = pygame.image.load("images/elucidate_full_text_portait_001.png")
        _title_resized = pygame.transform.scale(_title_img, (screen_x // 2, screen_y // 2))
        screen.blit(_title_resized, (screen_x // 4, screen_y // 4))
        _sel_img = pygame.image.load("images/elucidate_select_full.png")
        _sel_resized = pygame.transform.scale(_sel_img, (screen_x // 2, 30))
        screen.blit(_sel_resized, (screen_x // 4, screen_y - 115))
    except Exception:
        pass
    _load_font_a = pygame.font.SysFont("Times New Roman", 25)
    _load_font_b = pygame.font.SysFont("Times New Roman", 20)
    _load_surf_a = _load_font_a.render("Loading Functions", True, (0, 0, 0))
    _load_rect_a = _load_surf_a.get_rect(center=(screen_x // 2, screen_y - 100))
    screen.blit(_load_surf_a, _load_rect_a)
    _load_surf_b = _load_font_b.render("Loading...", True, (255, 255, 255))
    _load_rect_b = _load_surf_b.get_rect(center=(screen_x // 2, screen_y - 20))
    screen.blit(_load_surf_b, _load_rect_b)
    pygame.draw.rect(screen, (160, 0, 0), (0, 0, screen_x, screen_y), 1)
    pygame.display.flip()
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    sys_bg_color = (0, 0, 0)
    sys_bd_color_sc_area = (180, 180, 180)
    sys_audio_volume = 1.0
    ui_white = (245, 245, 245)
    ui_crimson = (160, 0, 0)
    ui_dark_crimson = (120, 0, 0)
    ui_gray = (180, 180, 180)
    sys_audio_muted = False
    sys_controls_mode = "keyboard"

    controls = {"move_left": pygame.K_a, "move_right": pygame.K_d, "move_up": pygame.K_w, "move_down": pygame.K_s,
                "attack": pygame.K_SPACE, "interact": pygame.K_e, "inventory": pygame.K_i, }

    SAVE_DIR = "saves"
    CONTROLS_FILE = os.path.join(SAVE_DIR, "controls.json")
    os.makedirs(SAVE_DIR, exist_ok=True)

    text_home_001 = "PLAY"
    text_home_002 = "SETTINGS"
    text_home_003 = "EXIT"

    _sfx_cache = {}

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

    def load_controls():
        nonlocal controls
        try:
            if os.path.exists(CONTROLS_FILE):
                with open(CONTROLS_FILE, "r") as f:
                    data = json.load(f)
                    for k in controls:
                        if k in data:
                            controls[k] = data[k]
        except Exception:
            pass

    def save_controls():
        try:
            with open(CONTROLS_FILE, "w") as f:
                json.dump(controls, f)
        except Exception:
            pass

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

    def ambient(rel_path, loop):
        try:
            pygame.mixer.music.load(rel_path)
            pygame.mixer.music.play(loop)
            sys_apply_audio_settings()
        except Exception:
            pass

    def _sfx(file, sfx_volume):
        try:
            if file not in _sfx_cache:
                _sfx_cache[file] = pygame.mixer.Sound(file)
            sound = _sfx_cache[file]
            if sys_audio_muted:
                sound.set_volume(0.0)
            else:
                sound.set_volume(sfx_volume * sys_audio_volume)
            sound.play()
        except Exception:
            pass

    def sys_apply_audio_settings():
        try:
            if sys_audio_muted:
                pygame.mixer.music.set_volume(0.0)
            else:
                pygame.mixer.music.set_volume(sys_audio_volume)
        except Exception:
            pass

    def mouse():
        pygame.draw.rect(screen, (160, 0, 0), (0, 0, screen_x, screen_y), 1)
        mx, my = pygame.mouse.get_pos()
        pygame.draw.rect(screen, (0, 255, 0), (mx - 10, my, 20, 1))
        pygame.draw.rect(screen, (0, 255, 0), (mx, my - 10, 1, 20))
        tuple_static_text(mx, my, color=(0, 255, 0), position=(mx + 10, my), size=15)
        tuple_static_text(py_clock.get_fps(), color=(0, 255, 0), position=(mx + 10, my + 15), size=15)
        
    saved_pos = [None, None]

    def mouse_dev():
        pygame.draw.rect(screen, (160, 0, 0), (0, 0, screen_x, screen_y), 1)

        mx, my = pygame.mouse.get_pos()
        offset_x, offset_y = mx - 200, my - 200

        pygame.draw.rect(screen, (0, 255, 0), (offset_x, offset_y, 20, 1))
        pygame.draw.rect(screen, (0, 255, 0), (offset_x, offset_y, 1, 20))

        tuple_static_text((offset_x, offset_y), color=(0, 255, 0), position=(offset_x, offset_y), size=15)
        tuple_static_text(py_clock.get_fps(), color=(0, 255, 0), position=(offset_x, offset_y + 15), size=15)

        events = pygame.event.get()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                saved_pos[0], saved_pos[1] = mx, my
            if event.type == pygame.QUIT:
                elucidate_sys_exit()

        if saved_pos[0] is not None:
            sx, sy = saved_pos
            pygame.draw.rect(screen, (0, 255, 0), (sx - 200, sy - 200, 20, 1))
            pygame.draw.rect(screen, (0, 255, 0), (sx - 200, sy - 200, 1, 20))
            tuple_static_text((sx - 200, sy - 200, mx - sx, my - sy), color=(0, 255, 0), position=(sx - 200, sy - 200 - 15), size=15)
            pygame.draw.rect(screen, (0, 255, 0), (sx - 200, sy - 200, offset_x - (sx - 200), offset_y - (sy - 200)), 1)
    
    def sys_gen_loading(n):
        ambient("music/elucidate_the_wait.wav", -1)
        screen.fill(sys_bg_color)
        screen.blit(_scaled_images["elucidate_title_1"], (screen_x // 4, screen_y // 4))
        screen.blit(_scaled_images["elucidate_select_load"], (screen_x // 4, screen_y - 115))
        static_text_raw_center("Welcome to Elucidate RPG", color=(0, 0, 0), position=(screen_x // 2, screen_y - 100),
                               size=25)
        static_text_raw_center("Loading...", color=(255, 255, 255), position=(screen_x // 2, screen_y - 20), size=20)
        pygame.draw.rect(screen, (160, 0, 0), (0, 0, screen_x, screen_y), 1)
        display()
        pygame.time.delay(n * 1000)
        screen.fill(sys_bg_color)
        screen.blit(_scaled_images["elucidate_title_1"], (screen_x // 4, screen_y // 4))
        screen.blit(_scaled_images["elucidate_select_load"], (screen_x // 4, screen_y - 115))
        static_text_raw_center("Welcome to Elucidate RPG", color=(0, 0, 0), position=(screen_x // 2, screen_y - 100),
                               size=25)
        static_text_raw_center("Done", color=(255, 255, 255), position=(screen_x // 2, screen_y - 20), size=20)
        pygame.draw.rect(screen, (160, 0, 0), (0, 0, screen_x, screen_y), 1)
        display()
        pygame.time.delay(1000)

    def Asys_gen_update_error():
        nonlocal sys_audio_muted, sys_audio_volume
        loop_cytsuwjw = True
        colide_yes = pygame.Rect((screen_x // 2) - 100, (screen_y // 2) + 134, 200, 30)
        colide_no = pygame.Rect((screen_x // 2) - 100, (screen_y // 2) + 174, 200, 30)
        while loop_cytsuwjw:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    elucidate_sys_exit()
            mx, my = pygame.mouse.get_pos()
            screen.fill(sys_bg_color)
            screen.blit(_preloaded_images["elucidate_select_bg_002"], (0, 0))
            static_text_raw_center("Built for future update.", color=(255, 255, 255),
                                   position=(screen_x // 2, (screen_y // 2) - 40), size=40)
            static_text_raw_center("Unavailable state.", color=(255, 255, 255),
                                   position=(screen_x // 2, (screen_y // 2)), size=40)
            static_text_raw_center("BACK", color=(255, 255, 255), position=(screen_x // 2, (screen_y // 2) + 150),
                                   size=30)
            static_text_raw_center("CLOSE GAME", color=(255, 255, 255), position=(screen_x // 2, (screen_y // 2) + 190),
                                   size=30)
            if colide_yes.collidepoint(mx, my):
                screen.blit(_scaled_images["elucidate_select_exit"], ((screen_x // 2) - 100, (screen_y // 2) + 134))
                static_text_raw_center("BACK", color=(0, 0, 0), position=(screen_x // 2, (screen_y // 2) + 150),
                                       size=30)
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        loop_cytsuwjw = False
            elif colide_no.collidepoint(mx, my):
                screen.blit(_scaled_images["elucidate_select_exit"], ((screen_x // 2) - 100, (screen_y // 2) + 174))
                static_text_raw_center("CLOSE GAME", color=(0, 0, 0), position=(screen_x // 2, (screen_y // 2) + 190),
                                       size=30)
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        elucidate_sys_exit()
            mouse()
            display()

    def get_entity_walls(npcs, player):
        entity_walls = []
        for npc in npcs:
            if npc.state != "hostile":
                entity_walls.append(npc.get_rect())
        return entity_walls

    class Player:
        def __init__(self, class_name, x, y, pw, ph):
            self.class_name = class_name
            self.x = float(x)
            self.y = float(y)
            self.pw = pw
            self.ph = ph
            self.size = 40
            self.dx = 0
            self.dy = 0
            self.speed = PLAYER_CLASSES.get(class_name, user_add_speed)
            self.facing = "down"
            self.state = "idle"
            self.is_attacking = False
            self.sprite_type = PLAYER_SPRITES.get(class_name, "no")
            self.anim_frame = 0
            self.anim_timer = 0

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
            if self.dx != 0 and self.dy != 0:
                self.dx *= 0.7071
                self.dy *= 0.7071

        def move(self, walls):
            new_x = self.x + self.dx
            test_rect = pygame.Rect(int(new_x), int(self.y), self.size, self.size)
            for wall in walls:
                if test_rect.colliderect(wall):
                    if self.dx > 0:
                        new_x = wall.left - self.size
                    elif self.dx < 0:
                        new_x = wall.right
                    break
            self.x = new_x
            new_y = self.y + self.dy
            test_rect = pygame.Rect(int(self.x), int(new_y), self.size, self.size)
            for wall in walls:
                if test_rect.colliderect(wall):
                    if self.dy > 0:
                        new_y = wall.top - self.size
                    elif self.dy < 0:
                        new_y = wall.bottom
                    break
            self.y = new_y

        def border(self):
            if self.x < 0:
                self.x = self.pw - self.size
            if self.x > self.pw - self.size:
                self.x = 0
            if self.y < 0:
                self.y = self.ph - self.size
            if self.y > self.ph - self.size:
                self.y = 0

        def attack(self):
            self.is_attacking = True
            self.state = "attack"

        def get_rect(self):
            return pygame.Rect(int(self.x), int(self.y), self.size, self.size)

        def interact_rect(self):
            size = 40
            if self.facing == "up":
                return pygame.Rect(self.x, self.y - size, size, size)
            elif self.facing == "down":
                return pygame.Rect(self.x, self.y + self.size, size, size)
            elif self.facing == "left":
                return pygame.Rect(self.x - size, self.y, size, size)
            elif self.facing == "right":
                return pygame.Rect(self.x + self.size, self.y, size, size)

        def draw(self, screen, world_x, world_y):
            sprite_set = SPRITES[self.sprite_type]
            if self.state == "idle":
                sprite = sprite_set["idle"][self.facing]
            elif self.state == "walk":
                frames = sprite_set["walk"][self.facing]
                self.anim_timer += delta
                if self.anim_timer > 0.15:
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
            draw_x = screen_x // 2 - self.size // 2
            draw_y = screen_y // 2 - self.size // 2
            screen.blit(sprite, (draw_x - 18, draw_y - 41))

    class NPC:
        def __init__(self, allowed_states, state, x, y, pw, ph, sprite_key):
            self.allowed_states = allowed_states
            self.state = state
            self.x = x
            self.y = y
            self.pw = pw
            self.ph = ph
            self.sprite_key = sprite_key
            self.sprites = SPRITES.get(sprite_key, SPRITES["no"])
            self.action = "idle"
            self.frame = 0
            self.anim_timer = 0
            self.anim_speed = 10
            self.direction = random.choice(["up", "down", "left", "right"])
            self.speed = 4
            self.move_timer = random.randint(10, 120)
            self.move_time = 120
            self.stunned = False
            self.stun_timer = 0
            self.stun_time = 60
            self.rect = pygame.Rect(self.x, self.y, 72, 72)
            self.last_pos = (self.x, self.y)
            self.stuck_timer = 0
            self.stuck_time = 10
            self.maneuvering = False
            self.maneuver_timer = 0
            self.maneuver_time = 45
            self.moving = False

        def get_rect(self):
            return pygame.Rect(self.x, self.y, 72, 72)

        def spawn_safe(self, walls):
            for _ in range(1000):
                x = random.randint(0, self.pw - 72)
                y = random.randint(0, self.ph - 72)
                test_rect = pygame.Rect(x, y, 72, 72)
                collide = False
                for w in walls:
                    if test_rect.colliderect(w):
                        collide = True
                        break
                if not collide:
                    self.x = x
                    self.y = y
                    self.rect.topleft = (x, y)
                    return

        def update(self, player, walls, entities):
            self.moving = False
            if self.stunned:
                self.stun_timer -= 1
                if self.stun_timer <= 0:
                    self.stunned = False
                return
            if (self.x, self.y) == self.last_pos:
                self.stuck_timer += 1
            else:
                self.stuck_timer = 0
                self.last_pos = (self.x, self.y)
            if self.state == "hostile":
                if "hostile" not in self.allowed_states:
                    return
                if self.stuck_timer >= self.stuck_time:
                    self.maneuvering = True
                    self.maneuver_timer = self.maneuver_time
                    self.direction = random.choice(["up", "down", "left", "right"])
                    self.stuck_timer = 0
                if self.maneuvering:
                    self.maneuver_timer -= 1
                    self.move_direction(walls, entities, player)
                    if self.maneuver_timer <= 0:
                        self.maneuvering = False
                else:
                    self.follow_player(player, walls, entities)
                if self.rect.colliderect(player.get_rect()):
                    self.interact(player)
            elif self.state == "roaming":
                if "roaming" in self.allowed_states:
                    self.move_timer -= 1
                    if self.move_timer <= 0:
                        self.direction = random.choice(["up", "down", "left", "right"])
                        self.move_timer = random.randint(10, 120)
                    self.move_direction(walls, entities, player)
            self.animate()

        def animate(self):
            if self.moving:
                self.action = "walk"
            else:
                self.action = "idle"
            self.anim_timer += delta
            if self.anim_timer >= 0.12:
                self.anim_timer = 0
                self.frame += 1

        def move_direction(self, walls, entities, player):
            dx = 0
            dy = 0
            if self.direction == "up":
                dy = -self.speed
            elif self.direction == "down":
                dy = self.speed
            elif self.direction == "left":
                dx = -self.speed
            elif self.direction == "right":
                dx = self.speed
            self.try_move(dx, dy, walls, entities, player)

        def follow_player(self, player, walls, entities):
            dx = player.x - self.x
            dy = player.y - self.y
            move_x = 0
            move_y = 0
            if abs(dx) > 0:
                move_x = max(-self.speed, min(self.speed, dx))
                self.direction = "right" if dx > 0 else "left"
            if abs(dy) > 0:
                move_y = max(-self.speed, min(self.speed, dy))
                self.direction = "down" if dy > 0 else "up"
            self.try_move(move_x, move_y, walls, entities, player)

        def try_move(self, dx, dy, walls, entities, player):
            new_rect = self.rect.move(dx, dy)
            for w in walls:
                if new_rect.colliderect(w):
                    self.moving = False
                    return
            if self.state != "hostile":
                for e in entities:
                    if e != self.rect and new_rect.colliderect(e):
                        self.moving = False
                        return
                if new_rect.colliderect(player.get_rect()):
                    self.moving = False
                    return
            self.x += dx
            self.y += dy
            self.rect.topleft = (self.x, self.y)
            self.moving = True

        def interact(self, player):
            self.stunned = True
            self.stun_timer = self.stun_time

        def draw(self, screen, world_x, world_y):
            action_set = self.sprites.get(self.action, SPRITES["no"]["idle"])
            dir_set = action_set.get(self.direction, SPRITES["no"]["idle"]["down"])
            if isinstance(dir_set, list):
                sprite = dir_set[self.frame % len(dir_set)]
            else:
                sprite = dir_set
            draw_x = self.x - world_x
            draw_y = self.y - world_y
            screen.blit(sprite, (draw_x, draw_y))

    def player(class_name, x, y, pw, ph):
        return Player(class_name, x, y, pw, ph)

    class inventory:
        def __init__(self, img, text, rect):
            self.img = img
            self.text = text
            self.rect = rect
            self._font = pygame.font.SysFont("Times New Roman", 14)

        def _format_text(self):
            if isinstance(self.text, int):
                return "999+" if self.text > 999 else str(self.text)
            return str(self.text)

        def draw(self, surface):
            img_scaled = pygame.transform.scale(
                self.img, (self.rect.width, self.rect.height)
            )

            surface.blit(img_scaled, self.rect.topleft)
            text_str = self._format_text()
            if text_str != "0":
                text_surf = self._font.render(text_str, True, (255, 255, 255))

                text_rect = text_surf.get_rect()
                text_rect.bottomleft = (
                    self.rect.left + 2,
                    self.rect.bottom - 2
                )

                surface.blit(text_surf, text_rect)

    load_controls()
    home_random_bg = random.randint(1, 10)
    home_bg_ran = _preloaded_images[f"elucidate_menu_bg_{home_random_bg:03d}"]

    colide_play = pygame.Rect(5, 561, 250, 35)
    colide_settings = pygame.Rect(5, 596, 250, 35)
    colide_exit = pygame.Rect(5, 631, 250, 35)
    colide_yes = pygame.Rect((screen_x // 2) - 100, (screen_y // 2) + 134, 200, 30)
    colide_no = pygame.Rect((screen_x // 2) - 100, (screen_y // 2) + 174, 200, 30)
    colide_graphics = pygame.Rect((screen_x // 2) - 100, 185, 200, 30)
    colide_audio = pygame.Rect((screen_x // 2) - 100, 220, 200, 30)
    colide_controls = pygame.Rect((screen_x // 2) - 100, 255, 200, 30)
    colide_authors = pygame.Rect((screen_x // 2) - 100, 290, 200, 30)
    colide_back = pygame.Rect((screen_x // 2) - 100, 635, 200, 30)
    colide_up = pygame.Rect((screen_x // 2) - 150, 185, 300, 30)
    colide_down = pygame.Rect((screen_x // 2) - 150, 225, 300, 30)
    colide_left = pygame.Rect((screen_x // 2) - 150, 265, 300, 30)
    colide_right = pygame.Rect((screen_x // 2) - 150, 305, 300, 30)
    colide_attack = pygame.Rect((screen_x // 2) - 150, 345, 300, 30)
    colide_interact = pygame.Rect((screen_x // 2) - 150, 385, 300, 30)
    colide_inventory = pygame.Rect((screen_x // 2) - 150, 425, 300, 30)

    elucidate_main_run_home_play_newgame = pygame.Rect(5, 202, 250, 35)
    elucidate_main_run_home_play_more = pygame.Rect(5, 237, 250, 35)
    elucidate_main_run_home_play_back = pygame.Rect(5, 272, 250, 35)
    elucidate_main_run_home_play_back_select = pygame.Rect((screen_x // 2) - 100, 655, 200, 30)

    select_mercenary = pygame.Rect(180, 160, 150, 400)
    select_cultist = pygame.Rect(360, 160, 150, 400)
    select_priest = pygame.Rect(560, 160, 150, 400)
    select_shaman = pygame.Rect(760, 160, 150, 400)
    select_merchant = pygame.Rect(940, 160, 150, 400)

    back_playselect_col = pygame.Rect(680, 671, 200, 30)
    ok_playselect_col = pygame.Rect(680, 631, 200, 30)

    colide_inventory_stats = pygame.Rect(5, 22, 300, 35)
    colide_inventory_bag = pygame.Rect(5, 58, 300, 35)
    colide_inventory_equipment = pygame.Rect(5, 95, 300, 35)
    colide_inventory_continue = pygame.Rect(5, 132, 300, 35)
    colide_inventory_saves = pygame.Rect(5, 169, 300, 35)
    colide_inventory_exit = pygame.Rect(5, 206, 300, 35)

    interact_rect = pygame.Rect(601, 60, 40, 40)

    slider_x = (screen_x // 2) - 200
    slider_y = 300
    slider_w = 400
    slider_h = 10
    knob_r = 12
    dragging_slider = False
    mute_rect = pygame.Rect((screen_x // 2) - 60, 360, 120, 35)

    gfx_fps_slider_x = (screen_x // 2) - 200
    gfx_fps_slider_y = 260
    gfx_fps_slider_w = 400
    gfx_cpu_slider_x = (screen_x // 2) - 200
    gfx_cpu_slider_y = 380
    gfx_cpu_slider_w = 400
    gfx_ram_slider_x = (screen_x // 2) - 200
    gfx_ram_slider_y = 500
    gfx_ram_slider_w = 400

    waiting_for_key = None
    p = None
    test_area_npc_idle = NPC(["hostile"], "hostile", 400, 300, 1275, 710, "no")
    test_area_npc_idle1 = NPC(["idle"], "idle", 601, 60, 1275, 710, "no")
    test_area_npc_idle2 = NPC(["roaming"], "roaming", 400, 300, 1275, 710, "no")
    npcs = [test_area_npc_idle, test_area_npc_idle1, test_area_npc_idle2]

    area_walls = {
        "cutscene_01":
            [

            ],
        "map_01":
            [
                pygame.Rect(125, 72, 725, 139),
                pygame.Rect(748, 199, 90, 140),
                pygame.Rect(697, 212, 70, 134),
                pygame.Rect(642, 214, 52, 119),
                pygame.Rect(546, 377, 60, 39),
                pygame.Rect(611, 351, 61, 51),
                pygame.Rect(779, 342, 57, 144),
                pygame.Rect(834, 198, 32, 324),
                pygame.Rect(569, 483, 271, 76),
                pygame.Rect(137, 478, 309, 82),
                pygame.Rect(342, 230, 86, 144),
                pygame.Rect(123, 200, 43, 276),
                pygame.Rect(165, 265, 64, 131),
                pygame.Rect(171, 396, 47, 57),
                pygame.Rect(451, 210, 114, 45),
            ],
        "map_02":
            [
                pygame.Rect(0, 2, 160, 441),
                pygame.Rect(-3, 443, 108, 44),
                pygame.Rect(146, -18, 306, 42),
                pygame.Rect(557, 28, 217, 94),
                pygame.Rect(450, 34, 113, 148),
                pygame.Rect(556, 123, 102, 76),
                pygame.Rect(456, 181, 115, 34),
                pygame.Rect(851, 1, 171, 318),
                pygame.Rect(737, 163, 69, 93),
                pygame.Rect(451, -7, 1777, 22),
                pygame.Rect(1020, 9, 1196, 145),
                pygame.Rect(2213, 23, 11, 141),
                pygame.Rect(2160, 251, 64, 175),
                pygame.Rect(2145, 292, 18, 42),
                pygame.Rect(2144, 374, 26, 40),
                pygame.Rect(1190, 325, 51, 119),
                pygame.Rect(1213, 449, 94, 38),
                pygame.Rect(1236, 304, 122, 145),
                pygame.Rect(1398, 308, 113, 143),
                pygame.Rect(1379, 399, 28, 25),
                pygame.Rect(1550, 305, 117, 143),
                pygame.Rect(1530, 409, 18, 39),
                pygame.Rect(1530, 442, 73, 37),
                pygame.Rect(1713, 301, 132, 144),
                pygame.Rect(1674, 394, 40, 30),
                pygame.Rect(1688, 426, 43, 37),
                pygame.Rect(1734, 448, 33, 31),
                pygame.Rect(1785, 459, 75, 22),
                pygame.Rect(1846, 384, 16, 52),
                pygame.Rect(1886, 303, 118, 126),
                pygame.Rect(1911, 428, 69, 29),
                pygame.Rect(1988, 448, 50, 33),
                pygame.Rect(2014, 313, 30, 52),
                pygame.Rect(2008, 359, 36, 39),
                pygame.Rect(1994, 397, 45, 40),
                pygame.Rect(1017, 159, 84, 162),
                pygame.Rect(1099, 159, 83, 76),
                pygame.Rect(1253, 163, 116, 61),
                pygame.Rect(1253, 213, 40, 27),
                pygame.Rect(1313, 216, 41, 22),
                pygame.Rect(1437, 167, 102, 47),
                pygame.Rect(1580, 172, 122, 57),
                pygame.Rect(1757, 166, 105, 42),
                pygame.Rect(1801, 148, 41, 22),
                pygame.Rect(1789, 191, 84, 30),
                pygame.Rect(1810, 214, 39, 18),
                pygame.Rect(1892, 150, 119, 60),
                pygame.Rect(2126, 162, 54, 47),
                pygame.Rect(2198, 150, 28, 55),
                pygame.Rect(2212, 154, 7, 353),
                pygame.Rect(2169, 426, 39, 30),
                pygame.Rect(2183, 455, 8, 77),
                pygame.Rect(989, 450, 104, 109),
                pygame.Rect(1015, 311, 87, 149),
                pygame.Rect(1096, 388, 33, 50),
                pygame.Rect(1085, 439, 38, 47),
                pygame.Rect(840, 682, 237, 560),
                pygame.Rect(577, 308, 306, 182),
                pygame.Rect(597, 462, 172, 51),
                pygame.Rect(465, 340, 37, 74),
                pygame.Rect(454, 414, 119, 122),
                pygame.Rect(528, 336, 36, 94),
                pygame.Rect(600, 488, 8, 60),
                pygame.Rect(782, 471, 18, 56),
                pygame.Rect(803, 463, 101, 83),
                pygame.Rect(878, 313, 147, 161),
                pygame.Rect(432, 716, 166, 71),
                pygame.Rect(549, 679, 72, 48),
                pygame.Rect(573, 698, 134, 191),
                pygame.Rect(597, 880, 90, 36),
                pygame.Rect(547, 797, 36, 69),
                pygame.Rect(493, 786, 31, 74),
                pygame.Rect(-27, 755, 150, 474),
                pygame.Rect(116, 850, 25, 396),
                pygame.Rect(388, 1088, 107, 147),
                pygame.Rect(686, 1006, 150, 105),
                pygame.Rect(747, 1124, 82, 109),
                pygame.Rect(619, 1138, 64, 47),
                pygame.Rect(582, 1182, 161, 64),
                pygame.Rect(388, 1225, 460, 19),
                pygame.Rect(126, 1210, 262, 34),
                pygame.Rect(706, 798, 129, 80),
                pygame.Rect(804, 748, 46, 54),
                pygame.Rect(824, 725, 24, 36),
                pygame.Rect(658, 911, 38, 24),
                pygame.Rect(713, 870, 51, 82),
                pygame.Rect(1077, 766, 55, 75),
                pygame.Rect(1078, 857, 49, 30),
                pygame.Rect(1067, 864, 149, 126),
                pygame.Rect(1068, 981, 213, 134),
                pygame.Rect(1299, 960, 89, 39),
                pygame.Rect(1240, 813, 187, 82),
                pygame.Rect(1428, 942, 44, 109),
                pygame.Rect(1306, 1037, 107, 78),
                pygame.Rect(1074, 1130, 1153, 116),
                pygame.Rect(2135, 785, 88, 112),
                pygame.Rect(2141, 886, 83, 97),
                pygame.Rect(2057, 928, 45, 120),
                pygame.Rect(2119, 1076, 97, 55),
                pygame.Rect(2207, 971, 19, 161),
                pygame.Rect(1887, 802, 169, 97),
                pygame.Rect(1871, 834, 35, 42),
                pygame.Rect(1934, 938, 43, 23),
                pygame.Rect(1962, 960, 62, 40),
                pygame.Rect(1885, 968, 32, 42),
                pygame.Rect(1930, 1028, 130, 88),
                pygame.Rect(1828, 1029, 92, 59),
                pygame.Rect(1793, 1067, 102, 56),
                pygame.Rect(1747, 1079, 77, 47),
                pygame.Rect(1729, 944, 43, 121),
                pygame.Rect(1624, 1034, 102, 83),
                pygame.Rect(1510, 1050, 91, 62),
                pygame.Rect(1556, 966, 41, 54),
                pygame.Rect(1630, 954, 57, 35),
                pygame.Rect(1606, 941, 47, 27),
                pygame.Rect(1582, 818, 159, 75),
                pygame.Rect(1544, 865, 45, 28),
                pygame.Rect(1534, 894, 29, 13),
                pygame.Rect(2212, 722, 8, 67),
                pygame.Rect(815, 887, 49, 47),
                pygame.Rect(763, 476, 26, 43),
                pygame.Rect(1064, 668, 27, 83),
                pygame.Rect(1076, 748, 16, 28),
                pygame.Rect(1401, 443, 47, 33),
                pygame.Rect(1242, 175, 10, 60),
                pygame.Rect(2178, 177, 11, 49),
                pygame.Rect(1003, 638, 25, 58),
                pygame.Rect(1029, 654, 37, 35),
                pygame.Rect(997, 626, 13, 64),
            ],
        "map_03":
            [
                pygame.Rect(0, 0, 232, 622),
                pygame.Rect(232, 458, 51, 175),
                pygame.Rect(0, 620, 118, 665),
                pygame.Rect(120, 925, 74, 177),
                pygame.Rect(380, 892, 60, 79),
                pygame.Rect(1, 1280, 1933, 180),
                pygame.Rect(453, 509, 16, 608),
                pygame.Rect(441, 0, 478, 282),
                pygame.Rect(920, 1, 1689, 196),
                pygame.Rect(926, 195, 91, 178),
                pygame.Rect(1076, 197, 197, 150),
                pygame.Rect(1332, 200, 274, 133),
                pygame.Rect(1669, 202, 150, 111),
                pygame.Rect(1715, 304, 137, 73),
                pygame.Rect(1935, 196, 676, 163),
                pygame.Rect(1837, 195, 98, 56),
                pygame.Rect(2365, 366, 245, 274),
                pygame.Rect(475, 506, 796, 175),
                pygame.Rect(477, 685, 148, 327),
                pygame.Rect(1244, 679, 29, 344),
                pygame.Rect(1244, 679, 29, 344),
                pygame.Rect(1269, 490, 90, 137),
                pygame.Rect(1183, 819, 58, 82),
                pygame.Rect(1281, 858, 90, 241),
                pygame.Rect(939, 1015, 334, 127),
                pygame.Rect(1521, 495, 302, 144),
                pygame.Rect(1864, 506, 189, 133),
                pygame.Rect(1880, 653, 105, 142),
                pygame.Rect(1729, 1240, 160, 42),
                pygame.Rect(1625, 986, 312, 173),
                pygame.Rect(1579, 791, 373, 186),
                pygame.Rect(2193, 964, 411, 489),
                pygame.Rect(2106, 1061, 69, 136),
                pygame.Rect(2147, 958, 45, 105),
                pygame.Rect(473, 1013, 321, 127),
                pygame.Rect(1281, 858, 90, 241),
                pygame.Rect(939, 1015, 334, 127),
                pygame.Rect(1281, 858, 90, 241),
                pygame.Rect(926, 195, 91, 178),
                pygame.Rect(1076, 197, 197, 150),
                pygame.Rect(1332, 200, 274, 133),
                pygame.Rect(1669, 202, 150, 111),
                pygame.Rect(1715, 304, 137, 73)
            ],
        "map_04":
            [
                pygame.Rect(0, 0, 689, 183),
                pygame.Rect(0, 257, 136, 837),
                pygame.Rect(0, 184, 28, 257),
                pygame.Rect(253, 262, 143, 401),
                pygame.Rect(664, 426, 177, 137),
                pygame.Rect(690, 0, 92, 93),
                pygame.Rect(136, 825, 1359, 836),
                pygame.Rect(791, 0, 476, 194),
                pygame.Rect(1267, 0, 231, 91),
                pygame.Rect(1129, 332, 146, 117),
                pygame.Rect(1050, 478, 215, 179),
                pygame.Rect(1329, 90, 164, 826),
            ],
        "map_05":
            [
                pygame.Rect(975, 0, 593, 452),
                pygame.Rect(1568, 0, 98, 165),
                pygame.Rect(1666, 0, 49, 602),
                pygame.Rect(1424, 590, 270, 900),
                pygame.Rect(0, 589, 265, 135),
                pygame.Rect(989, 723, 483, 904),
                pygame.Rect(0, 0, 201, 387),
                pygame.Rect(0, 504, 50, 572),
                pygame.Rect(201, 0, 665, 110),
                pygame.Rect(292, 110, 136, 281),
                pygame.Rect(427, 110, 190, 351),
                pygame.Rect(604, 110, 216, 280),
                pygame.Rect(673, 390, 142, 82),
                pygame.Rect(283, 534, 136, 209),
                pygame.Rect(566, 765, 137, 906),
                pygame.Rect(711, 594, 35, 905),
                pygame.Rect(530, 840, 29, 908),
                pygame.Rect(674, 720, 41, 772),
                pygame.Rect(491, 567, 217, 89),
                pygame.Rect(759, 49, 110, 115),
                pygame.Rect(61, 718, 40, 46),
                pygame.Rect(65, 767, 144, 137),
                pygame.Rect(214, 839, 39, 67),
                pygame.Rect(254, 900, 322, 26),
            ],
        "map_06":
            [
                pygame.Rect(350, 207, 218, 120),
                pygame.Rect(0, 0, 605, 165),
                pygame.Rect(674, 0, 601, 165),
                pygame.Rect(718, 207, 205, 120),
                pygame.Rect(604, 0, 125, 81),
                pygame.Rect(0, 0, 16, 703),
                pygame.Rect(25, 589, 41, 113),
                pygame.Rect(71, 611, 40, 700),
                pygame.Rect(116, 649, 84, 48),
                pygame.Rect(714, 383, 230, 598),
                pygame.Rect(0, 700, 1274, 714),
                pygame.Rect(944, 472, 306, 632),
                pygame.Rect(1265, 0, 15, 714),
                pygame.Rect(940, 70, 331, 242),
                pygame.Rect(351, 432, 212, 608),
                pygame.Rect(460, 573, 362, 703),
                pygame.Rect(476, 384, 90, 579),
                pygame.Rect(20, 323, 72, 91),
            ],
        "map_07":
            [
                pygame.Rect(292, 170, 479, 378),
                pygame.Rect(297, 682, 479, 347),
                pygame.Rect(754, 112, 228, 242),
                pygame.Rect(1371, 110, 233, 161),
                pygame.Rect(1442, 403, 72, 109),
                pygame.Rect(841, 412, 72, 111),
                pygame.Rect(826, 689, 81, 110),
                pygame.Rect(1451, 705, 54, 88),
                pygame.Rect(1410, 276, 175, 48),
                pygame.Rect(1579, 173, 483, 373),
                pygame.Rect(1579, 680, 485, 347),
                pygame.Rect(1432, 844, 57, 84),
                pygame.Rect(1256, 818, 128, 396),
                pygame.Rect(970, 824, 129, 391),
                pygame.Rect(865, 856, 50, 87),
                pygame.Rect(867, 1099, 53, 85),
                pygame.Rect(1445, 1100, 37, 81),
                pygame.Rect(2273, 104, 77, 453),
                pygame.Rect(2271, 646, 86, 596),
                pygame.Rect(1552, 1173, 722, 71),
                pygame.Rect(1622, 1144, 651, 28),
                pygame.Rect(2192, 709, 76, 428),
                pygame.Rect(2048, 109, 218, 94),
                pygame.Rect(2183, 199, 86, 326),
                pygame.Rect(0, 109, 139, 443),
                pygame.Rect(129, 114, 170, 115),
                pygame.Rect(0, 658, 130, 588),
                pygame.Rect(117, 1117, 693, 125),
                pygame.Rect(134, 292, 52, 141),
                pygame.Rect(1076, 406, 211, 282),
                pygame.Rect(0, 0, 1087, 101),
                pygame.Rect(1084, 0, 184, 30),
                pygame.Rect(1268, 0, 1084, 112),
            ],
        "map_08":
            [
                pygame.Rect(5, -6, 1192, 112),
                pygame.Rect(392, 100, 29, 176),
                pygame.Rect(821, 104, 23, 198),
                pygame.Rect(381, 373, 22, 276),
                pygame.Rect(823, 371, 22, 281),
                pygame.Rect(1065, 102, 128, 180),
                pygame.Rect(890, 105, 173, 202),
                pygame.Rect(888, 356, 123, 172),
                pygame.Rect(921, 311, 106, 62),
                pygame.Rect(1085, 347, 102, 156),
                pygame.Rect(1116, 499, 68, 84),
                pygame.Rect(1123, 581, 64, 86),
                pygame.Rect(1183, 278, 18, 394),
                pygame.Rect(3, 109, 10, 564),
                pygame.Rect(13, 656, 548, 15),
                pygame.Rect(640, 660, 552, 13),
                pygame.Rect(100, 388, 242, 60),
                pygame.Rect(99, 226, 245, 58),
                pygame.Rect(235, 595, 108, 53),
                pygame.Rect(103, 488, 240, 58),
                pygame.Rect(257, 312, 81, 43),
                pygame.Rect(124, 313, 90, 44),
                pygame.Rect(248, 159, 93, 39),
                pygame.Rect(121, 159, 92, 40),
                pygame.Rect(483, 118, 32, 87),
                pygame.Rect(700, 114, 30, 87),
                pygame.Rect(529, 124, 159, 113),
                pygame.Rect(26, 524, 72, 128),
                pygame.Rect(107, 615, 42, 42),
                pygame.Rect(18, 292, 34, 78),
                pygame.Rect(20, 119, 48, 58),
                pygame.Rect(1146, 281, 30, 43),
            ],
        "map_09":
            [
                pygame.Rect(-4, -2, 1334, 164),
                pygame.Rect(1318, 163, 18, 582),
                pygame.Rect(4, 168, 11, 574),
                pygame.Rect(523, 146, 45, 90),
                pygame.Rect(791, 142, 37, 95),
                pygame.Rect(574, 181, 26, 103),
                pygame.Rect(755, 176, 23, 115),
                pygame.Rect(601, 260, 33, 48),
                pygame.Rect(722, 261, 35, 47),
                pygame.Rect(340, 327, 286, 214),
                pygame.Rect(736, 327, 186, 208),
                pygame.Rect(743, 657, 383, 73),
                pygame.Rect(708, 730, 625, 15),
                pygame.Rect(1174, 249, 145, 97),
                pygame.Rect(1174, 428, 143, 132),
                pygame.Rect(1235, 569, 81, 62),
                pygame.Rect(1252, 649, 62, 69),
                pygame.Rect(1179, 695, 66, 31),
                pygame.Rect(248, 647, 348, 84),
                pygame.Rect(8, 731, 618, 17),
                pygame.Rect(29, 568, 32, 160),
                pygame.Rect(71, 641, 37, 78),
                pygame.Rect(23, 238, 179, 103),
                pygame.Rect(23, 460, 185, 95),
                pygame.Rect(73, 559, 89, 37),
                pygame.Rect(217, 425, 44, 101),
                pygame.Rect(360, 161, 82, 75),
                pygame.Rect(995, 225, 106, 52),
                pygame.Rect(938, 152, 244, 44),
                pygame.Rect(914, 258, 58, 31),
                pygame.Rect(1004, 297, 134, 92),
                pygame.Rect(1001, 444, 119, 134),
                pygame.Rect(937, 418, 33, 93),
                pygame.Rect(472, 174, 22, 40),
                pygame.Rect(870, 180, 28, 33),
                pygame.Rect(574, 157, 17, 31),
                pygame.Rect(762, 153, 13, 26),
                pygame.Rect(205, 162, 121, 30),
                pygame.Rect(23, 151, 74, 48),
                pygame.Rect(24, 427, 31, 31),
                pygame.Rect(16, 334, 37, 43),
            ],
        "map_10":
            [
                pygame.Rect(0, 0, 232, 622),
                pygame.Rect(232, 458, 51, 175),
                pygame.Rect(0, 620, 118, 665),
                pygame.Rect(120, 925, 74, 177),
                pygame.Rect(380, 892, 60, 79),
                pygame.Rect(1, 1280, 1933, 180),
                pygame.Rect(453, 509, 16, 608),
                pygame.Rect(441, 0, 478, 282),
                pygame.Rect(920, 1, 1689, 196),
                pygame.Rect(926, 195, 91, 178),
                pygame.Rect(1076, 197, 197, 150),
                pygame.Rect(1332, 200, 274, 133),
                pygame.Rect(1669, 202, 150, 111),
                pygame.Rect(1715, 304, 137, 73),
                pygame.Rect(1935, 196, 676, 163),
                pygame.Rect(1837, 195, 98, 56),
                pygame.Rect(2365, 366, 245, 274),
                pygame.Rect(475, 506, 796, 175),
                pygame.Rect(477, 685, 148, 327),
                pygame.Rect(1244, 679, 29, 344),
                pygame.Rect(1244, 679, 29, 344),
                pygame.Rect(1269, 490, 90, 137),
                pygame.Rect(1183, 819, 58, 82),
                pygame.Rect(1281, 858, 90, 241),
                pygame.Rect(939, 1015, 334, 127),
                pygame.Rect(1521, 495, 302, 144),
                pygame.Rect(1864, 506, 189, 133),
                pygame.Rect(1880, 653, 105, 142),
                pygame.Rect(1729, 1240, 160, 42),
                pygame.Rect(1625, 986, 312, 173),
                pygame.Rect(1579, 791, 373, 186),
                pygame.Rect(2193, 964, 411, 489),
                pygame.Rect(2106, 1061, 69, 136),
                pygame.Rect(2147, 958, 45, 105),
                pygame.Rect(473, 1013, 321, 127),
                pygame.Rect(1281, 858, 90, 241),
                pygame.Rect(939, 1015, 334, 127),
                pygame.Rect(1281, 858, 90, 241),
                pygame.Rect(926, 195, 91, 178),
                pygame.Rect(1076, 197, 197, 150),
                pygame.Rect(1332, 200, 274, 133),
                pygame.Rect(1669, 202, 150, 111),
                pygame.Rect(1715, 304, 137, 73)
            ],
        "map_11":
            [
                pygame.Rect(-7, 0, 83, 567),
                pygame.Rect(421, 3, 510, 98),
                pygame.Rect(566, 96, 174, 225),
                pygame.Rect(546, 317, 18, 237),
                pygame.Rect(329, 481, 226, 58),
                pygame.Rect(552, 376, 237, 178),
                pygame.Rect(819, 168, 98, 228),
                pygame.Rect(856, 96, 242, 219),
                pygame.Rect(980, 314, 109, 90),
                pygame.Rect(929, -1, 1440, 72),
                pygame.Rect(1733, 65, 120, 164),
                pygame.Rect(1467, 120, 125, 149),
                pygame.Rect(1119, 76, 133, 153),
                pygame.Rect(1848, 76, 514, 183),
                pygame.Rect(1933, 261, 102, 175),
                pygame.Rect(2026, 267, 341, 91),
                pygame.Rect(2091, 357, 271, 90),
                pygame.Rect(2140, 645, 152, 174),
                pygame.Rect(2304, 717, 70, 281),
                pygame.Rect(1950, 985, 114, 134),
                pygame.Rect(1961, 859, 274, 175),
                pygame.Rect(1993, 807, 186, 61),
                pygame.Rect(2059, 772, 77, 39),
                pygame.Rect(2119, 1036, 97, 86),
                pygame.Rect(2345, 996, 24, 9),
                pygame.Rect(2347, 998, 18, 191),
                pygame.Rect(2292, 1123, 49, 66),
                pygame.Rect(389, 1162, 1921, 17),
                pygame.Rect(825, 801, 417, 360),
                pygame.Rect(580, 732, 251, 94),
                pygame.Rect(636, 830, 80, 47),
                pygame.Rect(321, 790, 160, 78),
                pygame.Rect(464, 865, 40, 288),
                pygame.Rect(10, 739, 182, 102),
                pygame.Rect(23, 850, 78, 319),
                pygame.Rect(-2, 738, 25, 131),
                pygame.Rect(97, 920, 54, 262),
                pygame.Rect(358, 127, 208, 75),
                pygame.Rect(87, 151, 126, 52),
                pygame.Rect(63, 13, 106, 132),
                pygame.Rect(65, 469, 105, 91),
                pygame.Rect(1718, 483, 87, 57),
                pygame.Rect(2280, 440, 93, 80),
                pygame.Rect(508, 771, 77, 42),
            ],
        "map_12":
            [
                pygame.Rect(85, 233, 145, 82),
                pygame.Rect(3, 0, 854, 86),
                pygame.Rect(3, 84, 13, 401),
                pygame.Rect(852, 85, 19, 392),
                pygame.Rect(364, 120, 341, 95),
                pygame.Rect(251, 353, 139, 71),
                pygame.Rect(387, 400, 158, 57),
                pygame.Rect(723, 390, 127, 70),
                pygame.Rect(381, 461, 472, 15),
                pygame.Rect(807, 185, 46, 130),
                pygame.Rect(774, 243, 34, 46),
                pygame.Rect(20, 185, 44, 73),
                pygame.Rect(14, 324, 10, 146),
                pygame.Rect(768, 113, 89, 33),
                pygame.Rect(24, 446, 104, 30),
                pygame.Rect(251, 429, 133, 48),
            ],
        "map_13":
            [
                pygame.Rect(1, 130, 4, 249),
                pygame.Rect(4, 126, 127, 40),
                pygame.Rect(160, 1, 330, 105),
                pygame.Rect(575, 3, 54, 103),
                pygame.Rect(631, -1, 121, 169),
                pygame.Rect(654, 164, 104, 33),
                pygame.Rect(684, 199, 64, 31),
                pygame.Rect(717, 233, 34, 127),
                pygame.Rect(6, 168, 103, 18),
                pygame.Rect(8, 184, 90, 27),
                pygame.Rect(4, 213, 45, 23),
                pygame.Rect(232, 151, 100, 87),
                pygame.Rect(199, 242, 289, 114),
                pygame.Rect(335, 95, 106, 44),
                pygame.Rect(94, 418, 590, 22),
                pygame.Rect(686, 371, 72, 59),
                pygame.Rect(720, 362, 33, 12),
                pygame.Rect(3, 378, 95, 65),
                pygame.Rect(566, 2, 11, 103),
            ],
        "map_14":
            [
                pygame.Rect(-6, -6, 357, 330),
                pygame.Rect(217, 330, 140, 62),
                pygame.Rect(0, 325, 106, 70),
                pygame.Rect(298, 317, 58, 16),
                pygame.Rect(347, -5, 1124, 160),
                pygame.Rect(350, 155, 193, 48),
                pygame.Rect(379, 284, 156, 93),
                pygame.Rect(451, 256, 50, 29),
                pygame.Rect(562, 219, 124, 110),
                pygame.Rect(883, 182, 119, 65),
                pygame.Rect(689, 440, 111, 146),
                pygame.Rect(356, 506, 145, 138),
                pygame.Rect(1207, 165, 58, 98),
                pygame.Rect(1208, 150, 54, 30),
                pygame.Rect(1285, 153, 194, 211),
                pygame.Rect(1414, 364, 63, 81),
                pygame.Rect(1129, 513, 340, 321),
                pygame.Rect(999, 538, 118, 205),
                pygame.Rect(833, 687, 145, 96),
                pygame.Rect(505, 693, 174, 100),
                pygame.Rect(409, 657, 96, 69),
                pygame.Rect(-13, 504, 367, 320),
                pygame.Rect(356, 810, 778, 28),
                pygame.Rect(653, 146, 49, 36),
            ],
        "map_15":
            [
                pygame.Rect(5, -2, 520, 169),
                pygame.Rect(865, 12, 1009, 185),
                pygame.Rect(671, 253, 180, 78),
                pygame.Rect(551, 98, 24, 124),
                pygame.Rect(572, 365, 96, 74),
                pygame.Rect(669, 332, 17, 167),
                pygame.Rect(618, 471, 51, 29),
                pygame.Rect(615, 598, 53, 26),
                pygame.Rect(1053, 204, 245, 164),
                pygame.Rect(930, 198, 124, 43),
                pygame.Rect(858, 238, 280, 213),
                pygame.Rect(855, 439, 41, 64),
                pygame.Rect(980, 449, 47, 54),
                pygame.Rect(1065, 451, 38, 50),
                pygame.Rect(1208, 382, 71, 73),
                pygame.Rect(1139, 362, 138, 27),
                pygame.Rect(1265, 457, 14, 305),
                pygame.Rect(1067, 574, 197, 186),
                pygame.Rect(669, 601, 12, 226),
                pygame.Rect(686, 771, 194, 55),
                pygame.Rect(678, 773, 10, 51),
                pygame.Rect(854, 625, 35, 153),
                pygame.Rect(894, 650, 128, 100),
                pygame.Rect(890, 745, 177, 30),
                pygame.Rect(463, 395, 42, 54),
                pygame.Rect(396, 171, 98, 136),
                pygame.Rect(-3, 168, 123, 768),
                pygame.Rect(111, 173, 151, 149),
                pygame.Rect(301, 254, 25, 42),
                pygame.Rect(339, 264, 34, 54),
                pygame.Rect(355, 359, 39, 51),
                pygame.Rect(188, 478, 103, 62),
                pygame.Rect(109, 583, 56, 102),
                pygame.Rect(128, 702, 181, 233),
                pygame.Rect(316, 913, 13, 6),
                pygame.Rect(305, 889, 5, 5),
                pygame.Rect(300, 880, 318, 55),
                pygame.Rect(487, 800, 86, 82),
                pygame.Rect(456, 686, 59, 65),
                pygame.Rect(341, 748, 117, 48),
                pygame.Rect(420, 586, 54, 80),
                pygame.Rect(633, 924, 474, 20),
                pygame.Rect(1276, 929, 600, 5),
                pygame.Rect(1455, 887, 47, 40),
                pygame.Rect(1751, 191, 134, 742),
                pygame.Rect(1307, 229, 265, 134),
                pygame.Rect(1388, 352, 176, 120),
                pygame.Rect(1345, 191, 306, 83),
                pygame.Rect(1669, 355, 72, 226),
                pygame.Rect(1740, 360, 15, 571),
                pygame.Rect(1631, 785, 117, 146),
                pygame.Rect(1489, 618, 33, 59),
                pygame.Rect(1552, 648, 26, 48),
                pygame.Rect(1683, 681, 38, 97),
                pygame.Rect(1387, 592, 46, 56),
                pygame.Rect(1669, 196, 46, 109),
                pygame.Rect(848, 0, 1028, 12),
                pygame.Rect(506, 183, 18, 103),
            ],
        "map_16":
            [
                pygame.Rect(-1, -2, 614, 102),
                pygame.Rect(592, -52, 118, 50),
                pygame.Rect(699, -1, 897, 105),
                pygame.Rect(1057, 105, 11, 164),
                pygame.Rect(-3, 102, 14, 636),
                pygame.Rect(165, 107, 351, 197),
                pygame.Rect(2, 351, 208, 134),
                pygame.Rect(2, 309, 186, 41),
                pygame.Rect(282, 312, 144, 95),
                pygame.Rect(510, 97, 30, 134),
                pygame.Rect(739, 102, 22, 76),
                pygame.Rect(1294, 101, 176, 134),
                pygame.Rect(1081, 91, 177, 100),
                pygame.Rect(1585, 103, 19, 637),
                pygame.Rect(1068, 309, 81, 89),
                pygame.Rect(649, 275, 229, 368),
                pygame.Rect(597, 408, 43, 75),
                pygame.Rect(550, 450, 39, 61),
                pygame.Rect(477, 474, 69, 58),
                pygame.Rect(592, 441, 3, 41),
                pygame.Rect(9, 733, 1595, 21),
                pygame.Rect(1214, 345, 274, 213),
                pygame.Rect(1149, 424, 65, 112),
                pygame.Rect(872, 456, 125, 276),
                pygame.Rect(1003, 573, 186, 141),
                pygame.Rect(1249, 548, 162, 97),
                pygame.Rect(1364, 240, 172, 85),
                pygame.Rect(9, 567, 77, 78),
            ],
        "map_17":
            [
                pygame.Rect(-12, 0, 78, 416),
                pygame.Rect(63, 0, 60, 151),
                pygame.Rect(117, -3, 294, 128),
                pygame.Rect(95, 350, 139, 76),
                pygame.Rect(375, 355, 176, 100),
                pygame.Rect(532, 35, 32, 142),
                pygame.Rect(562, 160, 131, 43),
                pygame.Rect(579, 0, 31, 40),
                pygame.Rect(615, 3, 272, 97),
                pygame.Rect(3, 568, 73, 253),
                pygame.Rect(-4, 821, 421, 202),
                pygame.Rect(164, 769, 83, 50),
                pygame.Rect(121, 606, 117, 70),
                pygame.Rect(685, 376, 45, 90),
                pygame.Rect(723, 272, 169, 198),
                pygame.Rect(900, 378, 36, 73),
                pygame.Rect(1021, 281, 155, 158),
                pygame.Rect(922, 115, 106, 73),
                pygame.Rect(920, -2, 61, 91),
                pygame.Rect(988, 2, 7, 30),
                pygame.Rect(1178, 340, 51, 85),
                pygame.Rect(998, 441, 79, 36),
                pygame.Rect(1119, 447, 96, 35),
                pygame.Rect(993, 361, 22, 69),
                pygame.Rect(1275, 272, 154, 181),
                pygame.Rect(1473, 277, 12, 195),
                pygame.Rect(1471, 281, 167, 69),
                pygame.Rect(1500, 349, 96, 66),
                pygame.Rect(1570, 413, 43, 53),
                pygame.Rect(1614, 352, 14, 114),
                pygame.Rect(1632, 370, 51, 95),
                pygame.Rect(981, -1, 21, 102),
                pygame.Rect(1000, 0, 202, 106),
                pygame.Rect(808, 147, 86, 53),
                pygame.Rect(893, 116, 29, 61),
                pygame.Rect(573, 67, 46, 39),
                pygame.Rect(1146, 99, 66, 56),
                pygame.Rect(1222, 4, 30, 172),
                pygame.Rect(1241, 169, 116, 31),
                pygame.Rect(1265, 6, 42, 72),
                pygame.Rect(1316, 102, 51, 44),
                pygame.Rect(1315, -4, 259, 109),
                pygame.Rect(1444, 101, 121, 39),
                pygame.Rect(1455, 167, 153, 38),
                pygame.Rect(1642, 57, 55, 89),
                pygame.Rect(1695, 2, 126, 156),
                pygame.Rect(1579, 0, 72, 110),
                pygame.Rect(1769, 373, 69, 90),
                pygame.Rect(1745, 606, 74, 258),
                pygame.Rect(1804, 574, 17, 34),
                pygame.Rect(521, 865, 1298, 155),
                pygame.Rect(275, 780, 115, 46),
                pygame.Rect(520, 790, 140, 73),
                pygame.Rect(740, 604, 166, 164),
                pygame.Rect(664, 681, 72, 41),
                pygame.Rect(647, 731, 80, 44),
                pygame.Rect(912, 687, 74, 109),
                pygame.Rect(937, 664, 37, 30),
                pygame.Rect(1015, 604, 162, 181),
                pygame.Rect(1187, 696, 31, 79),
                pygame.Rect(1818, 284, 14, 227),
                pygame.Rect(1292, 607, 164, 191),
                pygame.Rect(1243, 705, 54, 75),
                pygame.Rect(1464, 632, 76, 99),
                pygame.Rect(1471, 726, 50, 78),
                pygame.Rect(1465, 810, 225, 59),
                pygame.Rect(1280, 838, 117, 23),
                pygame.Rect(1215, 770, 36, 22),
                pygame.Rect(987, 771, 38, 29),
                pygame.Rect(633, 778, 17, 14),
                pygame.Rect(498, -7, 83, 17),
                pygame.Rect(237, 221, 58, 44),
                pygame.Rect(274, 128, 127, 47),
            ],
        "map_18":
            [
                pygame.Rect(681, 13, 94, 96),
                pygame.Rect(424, 126, 58, 204),
                pygame.Rect(276, 184, 83, 128),
                pygame.Rect(320, 164, 96, 59),
                pygame.Rect(193, 280, 81, 144),
                pygame.Rect(22, 453, 107, 90),
                pygame.Rect(466, 423, 202, 309),
                pygame.Rect(423, 517, 46, 174),
                pygame.Rect(796, 365, 222, 201),
                pygame.Rect(1045, 160, 275, 167),
                pygame.Rect(1369, 96, 37, 103),
                pygame.Rect(1487, 136, 61, 78),
                pygame.Rect(1560, 126, 50, 97),
                pygame.Rect(1476, 401, 42, 68),
                pygame.Rect(1409, 491, 51, 57),
                pygame.Rect(1803, 16, 17, 552),
                pygame.Rect(1803, 663, 16, 353),
                pygame.Rect(-3, 1007, 1807, 9),
                pygame.Rect(0, 7, 9, 552),
                pygame.Rect(-4, 722, 12, 290),
                pygame.Rect(247, 729, 69, 93),
                pygame.Rect(136, 726, 40, 90),
                pygame.Rect(548, 826, 91, 94),
                pygame.Rect(683, 828, 50, 68),
                pygame.Rect(283, 903, 80, 56),
                pygame.Rect(432, 892, 49, 81),
                pygame.Rect(100, 911, 47, 82),
                pygame.Rect(1619, 446, 75, 60),
                pygame.Rect(1153, 627, 190, 172),
                pygame.Rect(1593, 752, 50, 97),
                pygame.Rect(599, 30, 59, 67),
                pygame.Rect(1581, 552, 19, 78),
                pygame.Rect(1742, 437, 60, 72),
            ],
        "map_19":
            [
                pygame.Rect(-4, -1, 1339, 180),
                pygame.Rect(1431, 232, 236, 448),
                pygame.Rect(1662, 674, 18, 51),
                pygame.Rect(-2, 720, 1681, 68),
                pygame.Rect(1422, -1, 262, 225),
                pygame.Rect(1598, 222, 85, 31),
                pygame.Rect(1335, 176, 40, 178),
                pygame.Rect(0, 183, 740, 538),
                pygame.Rect(731, 178, 587, 127),
                pygame.Rect(1158, 310, 175, 87),
                pygame.Rect(1295, 450, 26, 119),
                pygame.Rect(1251, 633, 124, 31),
                pygame.Rect(1119, 655, 272, 24),
                pygame.Rect(736, 578, 465, 144),
                pygame.Rect(922, 304, 236, 279),
                pygame.Rect(1155, 406, 97, 211),
                pygame.Rect(1274, 614, 99, 22),
                pygame.Rect(1309, 178, 24, 131),
            ],
        "map_20":
            [
                pygame.Rect(-6, 473, 114, 264),
                pygame.Rect(0, 433, 236, 25),
                pygame.Rect(217, 450, 17, 341),
                pygame.Rect(171, 513, 44, 50),
                pygame.Rect(350, 436, 17, 356),
                pygame.Rect(-2, 146, 214, 268),
                pygame.Rect(-1, 0, 1820, 121),
                pygame.Rect(221, 191, 13, 204),
                pygame.Rect(353, 253, 13, 139),
                pygame.Rect(235, 131, 117, 159),
                pygame.Rect(370, 251, 219, 24),
                pygame.Rect(350, 126, 1468, 126),
                pygame.Rect(475, 271, 82, 49),
                pygame.Rect(460, 292, 14, 29),
                pygame.Rect(427, 313, 151, 57),
                pygame.Rect(381, 455, 88, 64),
                pygame.Rect(497, 399, 76, 71),
                pygame.Rect(549, 476, 29, 89),
                pygame.Rect(526, 573, 53, 58),
                pygame.Rect(-1, 884, 35, 129),
                pygame.Rect(30, 903, 98, 111),
                pygame.Rect(126, 958, 66, 64),
                pygame.Rect(586, 256, 647, 372),
                pygame.Rect(590, 629, 281, 87),
                pygame.Rect(944, 633, 287, 94),
                pygame.Rect(1230, 643, 150, 96),
                pygame.Rect(1294, 615, 25, 187),
                pygame.Rect(355, 962, 479, 50),
                pygame.Rect(577, 938, 134, 27),
                pygame.Rect(611, 902, 63, 34),
                pygame.Rect(994, 971, 12, 40),
                pygame.Rect(1036, 954, 24, 58),
                pygame.Rect(994, 1009, 828, 14),
                pygame.Rect(1059, 963, 757, 45),
                pygame.Rect(1135, 923, 132, 39),
                pygame.Rect(1175, 895, 45, 28),
                pygame.Rect(1374, 672, 127, 36),
                pygame.Rect(1426, 710, 63, 248),
                pygame.Rect(1227, 260, 597, 420),
                pygame.Rect(1479, 671, 337, 303),
                pygame.Rect(582, 717, 186, 81),
                pygame.Rect(775, 705, 58, 46),
                pygame.Rect(190, 1014, 175, 13),
                pygame.Rect(-3, 399, 31, 79),
                pygame.Rect(189, 150, 68, 48),
            ],
        "map_21":
            [
                pygame.Rect(4, 547, 295, 14),
                pygame.Rect(418, 550, 583, 8),
                pygame.Rect(697, 452, 24, 101),
                pygame.Rect(-1, 11, 10, 546),
                pygame.Rect(3, 6, 698, 114),
                pygame.Rect(11, 137, 53, 78),
                pygame.Rect(10, 114, 156, 60),
                pygame.Rect(223, 115, 186, 25),
                pygame.Rect(495, 118, 104, 37),
                pygame.Rect(642, 190, 52, 110),
                pygame.Rect(655, 307, 37, 43),
                pygame.Rect(603, 113, 93, 55),
                pygame.Rect(699, 121, 28, 223),
                pygame.Rect(723, 322, 107, 22),
                pygame.Rect(895, 324, 89, 21),
                pygame.Rect(721, 75, 264, 19),
                pygame.Rect(967, 95, 19, 235),
                pygame.Rect(723, 83, 6, 67),
                pygame.Rect(813, 75, 88, 18),
                pygame.Rect(986, 318, 17, 234),
                pygame.Rect(723, 509, 151, 41),
                pygame.Rect(225, 305, 247, 109),
                pygame.Rect(235, 406, 218, 47),
                pygame.Rect(473, 331, 42, 43),
                pygame.Rect(189, 325, 38, 50),
                pygame.Rect(242, 247, 209, 53),
            ],
        "map_22":
            [
                pygame.Rect(-22, -4, 447, 244),
                pygame.Rect(-5, 239, 110, 28),
                pygame.Rect(196, 240, 518, 28),
                pygame.Rect(707, 225, 186, 21),
                pygame.Rect(901, 242, 228, 29),
                pygame.Rect(893, 234, 12, 26),
                pygame.Rect(1132, 248, 77, 16),
                pygame.Rect(1121, 246, 22, 9),
                pygame.Rect(0, 393, 238, 274),
                pygame.Rect(243, 450, 961, 222),
                pygame.Rect(231, 398, 21, 76),
                pygame.Rect(444, 415, 761, 35),
                pygame.Rect(712, 385, 159, 31),
                pygame.Rect(1087, 405, 117, 14),
                pygame.Rect(872, 406, 22, 10),
                pygame.Rect(865, 401, 22, 13),
                pygame.Rect(495, 398, 219, 39),
                pygame.Rect(422, 439, 24, 20),
                pygame.Rect(890, 402, 114, 15),
                pygame.Rect(915, 369, 91, 38),
                pygame.Rect(937, 353, 32, 18),
                pygame.Rect(997, 397, 27, 19),
                pygame.Rect(1144, 394, 59, 22),
                pygame.Rect(982, 263, 98, 21),
                pygame.Rect(709, 241, 22, 12),
            ],
        "map_23":
            [
                pygame.Rect(-1, -2, 154, 314),
                pygame.Rect(139, -3, 258, 168),
                pygame.Rect(147, 155, 47, 161),
                pygame.Rect(381, 7, 314, 303),
                pygame.Rect(342, 167, 40, 145),
                pygame.Rect(362, 309, 283, 14),
                pygame.Rect(694, 58, 171, 186),
                pygame.Rect(718, 230, 85, 84),
                pygame.Rect(691, -12, 798, 20),
                pygame.Rect(702, 2, 323, 68),
                pygame.Rect(846, 67, 169, 51),
                pygame.Rect(849, 122, 160, 30),
                pygame.Rect(851, 155, 130, 25),
                pygame.Rect(850, 187, 110, 15),
                pygame.Rect(1094, 9, 391, 105),
                pygame.Rect(1095, 109, 394, 40),
                pygame.Rect(1200, 132, 284, 37),
                pygame.Rect(1325, 163, 168, 111),
                pygame.Rect(1167, 178, 67, 41),
                pygame.Rect(-10, 496, 105, 245),
                pygame.Rect(100, 520, 171, 228),
                pygame.Rect(268, 539, 81, 214),
                pygame.Rect(354, 527, 1132, 213),
                pygame.Rect(1068, 273, 416, 249),
                pygame.Rect(890, 310, 82, 225),
                pygame.Rect(925, 291, 53, 26),
                pygame.Rect(885, 340, 13, 186),
                pygame.Rect(865, 393, 21, 134),
                pygame.Rect(664, 432, 104, 106),
                pygame.Rect(488, 431, 46, 105),
                pygame.Rect(524, 439, 44, 93),
                pygame.Rect(563, 445, 23, 88),
                pygame.Rect(581, 481, 39, 61),
                pygame.Rect(426, 446, 58, 96),
                pygame.Rect(395, 457, 31, 86),
                pygame.Rect(359, 487, 30, 61),
                pygame.Rect(384, 482, 14, 70),
                pygame.Rect(344, 547, 16, 208),
                pygame.Rect(972, 324, 18, 147),
                pygame.Rect(852, 421, 17, 105),
                pygame.Rect(8, 317, 178, 8),
                pygame.Rect(3, 310, 146, 7),
                pygame.Rect(193, 254, 12, 48),
            ],
        "map_24":
            [
                pygame.Rect(-4, -5, 341, 478),
                pygame.Rect(37, 478, 132, 51),
                pygame.Rect(338, 0, 1941, 108),
                pygame.Rect(335, 110, 223, 177),
                pygame.Rect(343, 291, 192, 59),
                pygame.Rect(335, 349, 135, 37),
                pygame.Rect(280, 468, 169, 49),
                pygame.Rect(465, 379, 15, 91),
                pygame.Rect(566, 293, 26, 105),
                pygame.Rect(549, 96, 694, 71),
                pygame.Rect(509, 136, 74, 122),
                pygame.Rect(574, 119, 38, 114),
                pygame.Rect(599, 85, 37, 120),
                pygame.Rect(627, 152, 23, 38),
                pygame.Rect(703, 146, 184, 57),
                pygame.Rect(643, 245, 266, 62),
                pygame.Rect(739, 499, 138, 29),
                pygame.Rect(697, 520, 17, 40),
                pygame.Rect(607, 587, 46, 22),
                pygame.Rect(622, 573, 51, 13),
                pygame.Rect(653, 549, 41, 26),
                pygame.Rect(674, 534, 20, 12),
                pygame.Rect(610, 733, 43, 46),
                pygame.Rect(639, 755, 34, 48),
                pygame.Rect(660, 777, 43, 44),
                pygame.Rect(727, 797, 144, 39),
                pygame.Rect(908, 778, 44, 40),
                pygame.Rect(960, 749, 38, 33),
                pygame.Rect(956, 571, 51, 31),
                pygame.Rect(911, 534, 48, 28),
                pygame.Rect(990, 619, 29, 89),
                pygame.Rect(737, 627, 137, 79),
                pygame.Rect(0, 787, 331, 291),
                pygame.Rect(331, 844, 55, 234),
                pygame.Rect(386, 900, 43, 186),
                pygame.Rect(432, 939, 40, 149),
                pygame.Rect(399, 846, 85, 47),
                pygame.Rect(468, 915, 59, 44),
                pygame.Rect(470, 1032, 1810, 39),
                pygame.Rect(1251, 106, 127, 180),
                pygame.Rect(1180, 104, 98, 92),
                pygame.Rect(978, 212, 199, 107),
                pygame.Rect(975, 307, 69, 105),
                pygame.Rect(1108, 306, 77, 107),
                pygame.Rect(1167, 211, 62, 144),
                pygame.Rect(1013, 159, 158, 58),
                pygame.Rect(1295, 365, 63, 100),
                pygame.Rect(1263, 381, 27, 110),
                pygame.Rect(1243, 410, 17, 63),
                pygame.Rect(1283, 460, 70, 32),
                pygame.Rect(1334, 286, 57, 142),
                pygame.Rect(1311, 287, 28, 74),
                pygame.Rect(1366, 97, 911, 140),
                pygame.Rect(1361, 225, 77, 63),
                pygame.Rect(1391, 295, 91, 90),
                pygame.Rect(1580, 235, 693, 52),
                pygame.Rect(1603, 289, 674, 50),
                pygame.Rect(1617, 341, 661, 484),
                pygame.Rect(1723, 832, 553, 200),
                pygame.Rect(1225, 832, 281, 215),
                pygame.Rect(1491, 906, 233, 138),
                pygame.Rect(1583, 470, 41, 232),
                pygame.Rect(1533, 524, 60, 82),
                pygame.Rect(1538, 601, 41, 163),
                pygame.Rect(1504, 657, 42, 71),
                pygame.Rect(1581, 703, 36, 53),
                pygame.Rect(1144, 844, 105, 187),
                pygame.Rect(1115, 901, 42, 143),
                pygame.Rect(1072, 955, 39, 93),
                pygame.Rect(1037, 996, 43, 44),
                pygame.Rect(1105, 956, 12, 82),
                pygame.Rect(521, 974, 51, 36),
                pygame.Rect(306, 670, 23, 114),
                pygame.Rect(321, 679, 34, 41),
                pygame.Rect(405, 718, 44, 115),
                pygame.Rect(355, 700, 55, 30),
            ],
        "map_25":
            [
                pygame.Rect(40, 32, 725, 232),
                pygame.Rect(765, 232, 703, 570),
                pygame.Rect(0, 0, 148, 597),
                pygame.Rect(703, 570, 643, 612),
                pygame.Rect(472, 596, 684, 678),
            ],
        "map_26":
            [
                pygame.Rect(-19, 9, 1690, 95),
                pygame.Rect(842, 109, 139, 142),
                pygame.Rect(-11, 102, 853, 27),
                pygame.Rect(690, 137, 89, 101),
                pygame.Rect(703, 126, 155, 19),
                pygame.Rect(767, 134, 17, 32),
                pygame.Rect(-9, 122, 702, 112),
                pygame.Rect(-7, 231, 347, 23),
                pygame.Rect(1, 251, 97, 635),
                pygame.Rect(83, 255, 223, 25),
                pygame.Rect(93, 275, 117, 21),
                pygame.Rect(96, 293, 96, 24),
                pygame.Rect(97, 319, 74, 12),
                pygame.Rect(93, 333, 68, 25),
                pygame.Rect(94, 354, 41, 28),
                pygame.Rect(94, 380, 12, 51),
                pygame.Rect(80, 461, 60, 50),
                pygame.Rect(96, 516, 40, 78),
                pygame.Rect(96, 593, 17, 60),
                pygame.Rect(176, 585, 79, 99),
                pygame.Rect(87, 732, 88, 154),
                pygame.Rect(106, 704, 37, 36),
                pygame.Rect(85, 702, 27, 29),
                pygame.Rect(94, 683, 13, 29),
                pygame.Rect(172, 791, 1502, 94),
                pygame.Rect(1365, 558, 309, 235),
                pygame.Rect(976, 102, 698, 208),
                pygame.Rect(870, 249, 77, 40),
                pygame.Rect(949, 266, 55, 42),
                pygame.Rect(940, 254, 50, 14),
                pygame.Rect(1213, 287, 364, 149),
                pygame.Rect(1570, 282, 39, 51),
                pygame.Rect(1652, 299, 28, 47),
                pygame.Rect(1666, 334, 10, 232),
                pygame.Rect(327, 391, 55, 253),
                pygame.Rect(379, 470, 16, 184),
                pygame.Rect(391, 521, 29, 168),
                pygame.Rect(311, 393, 24, 237),
                pygame.Rect(255, 488, 59, 80),
                pygame.Rect(285, 555, 23, 41),
                pygame.Rect(294, 592, 23, 34),
                pygame.Rect(285, 468, 39, 27),
                pygame.Rect(394, 487, 61, 127),
                pygame.Rect(444, 530, 51, 71),
                pygame.Rect(221, 745, 48, 52),
                pygame.Rect(159, 728, 48, 64),
                pygame.Rect(576, 760, 212, 50),
                pygame.Rect(592, 477, 204, 122),
                pygame.Rect(884, 474, 210, 128),
                pygame.Rect(969, 444, 55, 35),
                pygame.Rect(907, 595, 69, 34),
                pygame.Rect(989, 598, 66, 44),
                pygame.Rect(722, 595, 44, 30),
                pygame.Rect(518, 234, 239, 66),
                pygame.Rect(586, 298, 158, 47),
                pygame.Rect(606, 337, 90, 52),
                pygame.Rect(744, 267, 45, 41),
                pygame.Rect(736, 320, 48, 27),
                pygame.Rect(684, 352, 43, 46),
                pygame.Rect(877, 293, 60, 44),
                pygame.Rect(942, 312, 53, 63),
                pygame.Rect(1021, 320, 92, 96),
                pygame.Rect(1024, 300, 201, 37),
                pygame.Rect(1118, 330, 109, 41),
                pygame.Rect(1098, 377, 135, 18),
                pygame.Rect(1130, 387, 55, 59),
                pygame.Rect(1221, 413, 74, 38),
                pygame.Rect(1276, 606, 61, 40),
                pygame.Rect(1332, 569, 38, 239),
                pygame.Rect(1295, 652, 43, 155),
                pygame.Rect(1270, 684, 35, 144),
                pygame.Rect(1208, 705, 66, 109),
                pygame.Rect(1173, 695, 97, 97),
                pygame.Rect(1202, 684, 67, 17),
                pygame.Rect(1047, 727, 105, 68),
                pygame.Rect(984, 763, 62, 31),
                pygame.Rect(726, 733, 55, 25),
                pygame.Rect(772, 770, 27, 26),
                pygame.Rect(1088, 525, 28, 28),
            ],
        "map_27":
            [
                pygame.Rect(-1, 5, 1675, 41),
                pygame.Rect(-5, 36, 1674, 134),
                pygame.Rect(-5, 241, 426, 91),
                pygame.Rect(418, 251, 39, 56),
                pygame.Rect(421, 305, 37, 74),
                pygame.Rect(459, 344, 24, 38),
                pygame.Rect(-13, 338, 419, 93),
                pygame.Rect(393, 341, 34, 77),
                pygame.Rect(425, 375, 32, 35),
                pygame.Rect(-12, 422, 173, 43),
                pygame.Rect(158, 429, 33, 25),
                pygame.Rect(-4, 465, 112, 36),
                pygame.Rect(110, 465, 18, 16),
                pygame.Rect(105, 478, 18, 11),
                pygame.Rect(-23, 495, 118, 32),
                pygame.Rect(1, 534, 68, 39),
                pygame.Rect(-14, 529, 77, 8),
                pygame.Rect(-11, 557, 77, 321),
                pygame.Rect(485, 165, 190, 28),
                pygame.Rect(509, 192, 188, 13),
                pygame.Rect(516, 202, 203, 22),
                pygame.Rect(546, 217, 137, 26),
                pygame.Rect(568, 236, 137, 26),
                pygame.Rect(588, 261, 109, 227),
                pygame.Rect(555, 428, 36, 121),
                pygame.Rect(528, 468, 29, 134),
                pygame.Rect(63, 741, 39, 145),
                pygame.Rect(58, 678, 27, 67),
                pygame.Rect(78, 681, 29, 46),
                pygame.Rect(110, 788, 64, 114),
                pygame.Rect(97, 754, 77, 40),
                pygame.Rect(161, 817, 1512, 83),
                pygame.Rect(1652, 495, 25, 339),
                pygame.Rect(1605, 565, 58, 113),
                pygame.Rect(1521, 640, 71, 25),
                pygame.Rect(1101, 485, 290, 414),
                pygame.Rect(1381, 479, 84, 239),
                pygame.Rect(1484, 736, 79, 42),
                pygame.Rect(1617, 749, 55, 79),
                pygame.Rect(1535, 794, 91, 30),
                pygame.Rect(1111, 173, 355, 189),
                pygame.Rect(1592, 161, 95, 87),
                pygame.Rect(1552, 248, 27, 18),
                pygame.Rect(672, 159, 467, 87),
                pygame.Rect(671, 223, 365, 77),
                pygame.Rect(677, 287, 254, 49),
                pygame.Rect(924, 293, 77, 24),
                pygame.Rect(696, 326, 203, 48),
                pygame.Rect(891, 332, 41, 24),
                pygame.Rect(933, 317, 25, 22),
                pygame.Rect(693, 358, 139, 47),
                pygame.Rect(684, 402, 112, 58),
                pygame.Rect(911, 540, 85, 283),
                pygame.Rect(994, 575, 64, 249),
                pygame.Rect(864, 570, 60, 257),
                pygame.Rect(820, 635, 50, 199),
                pygame.Rect(792, 679, 37, 157),
                pygame.Rect(742, 707, 55, 127),
                pygame.Rect(702, 738, 61, 77),
                pygame.Rect(669, 751, 35, 75),
                pygame.Rect(597, 783, 66, 52),
                pygame.Rect(657, 777, 31, 51),
                pygame.Rect(237, 510, 295, 118),
                pygame.Rect(206, 524, 40, 78),
                pygame.Rect(198, 581, 82, 122),
                pygame.Rect(270, 608, 352, 92),
                pygame.Rect(247, 693, 291, 18),
                pygame.Rect(567, 478, 94, 178),
                pygame.Rect(645, 479, 48, 144),
                pygame.Rect(677, 467, 47, 128),
                pygame.Rect(689, 434, 51, 124),
                pygame.Rect(737, 453, 25, 54),
                pygame.Rect(1097, 260, 23, 96),
                pygame.Rect(1551, 626, 35, 21),
            ],
        "map_28":
            [
                pygame.Rect(-1, 0, 2895, 83),
                pygame.Rect(-4, 78, 180, 609),
                pygame.Rect(168, 83, 51, 497),
                pygame.Rect(222, 81, 326, 170),
                pygame.Rect(547, 374, 100, 165),
                pygame.Rect(432, 473, 125, 197),
                pygame.Rect(769, 275, 66, 185),
                pygame.Rect(577, 544, 206, 144),
                pygame.Rect(552, 546, 31, 144),
                pygame.Rect(697, 474, 136, 77),
                pygame.Rect(647, 502, 51, 41),
                pygame.Rect(832, 443, 39, 59),
                pygame.Rect(771, 555, 29, 118),
                pygame.Rect(454, 837, 217, 221),
                pygame.Rect(681, 876, 154, 146),
                pygame.Rect(667, 882, 95, 246),
                pygame.Rect(0, 841, 188, 251),
                pygame.Rect(-1, 1084, 116, 112),
                pygame.Rect(-2, 1195, 40, 328),
                pygame.Rect(32, 1483, 2852, 44),
                pygame.Rect(2751, 76, 138, 943),
                pygame.Rect(857, 421, 87, 168),
                pygame.Rect(880, 374, 69, 51),
                pygame.Rect(929, 320, 329, 49),
                pygame.Rect(1013, 286, 207, 33),
                pygame.Rect(1047, 257, 136, 30),
                pygame.Rect(1017, 379, 153, 236),
                pygame.Rect(1156, 399, 156, 235),
                pygame.Rect(992, 603, 85, 110),
                pygame.Rect(823, 776, 48, 352),
                pygame.Rect(874, 807, 39, 221),
                pygame.Rect(736, 1122, 129, 136),
                pygame.Rect(862, 1019, 203, 107),
                pygame.Rect(499, 1080, 72, 64),
                pygame.Rect(139, 1117, 236, 272),
                pygame.Rect(196, 931, 120, 163),
                pygame.Rect(1218, 78, 279, 98),
                pygame.Rect(1770, 57, 58, 90),
                pygame.Rect(1856, 99, 237, 89),
                pygame.Rect(1810, 95, 61, 84),
                pygame.Rect(1881, 166, 60, 54),
                pygame.Rect(1917, 189, 206, 90),
                pygame.Rect(2073, 81, 96, 107),
                pygame.Rect(2119, 176, 49, 77),
                pygame.Rect(2164, 76, 105, 104),
                pygame.Rect(2270, 72, 46, 68),
                pygame.Rect(1612, 447, 127, 223),
                pygame.Rect(1519, 339, 87, 125),
                pygame.Rect(1660, 204, 41, 199),
                pygame.Rect(1583, 258, 81, 77),
                pygame.Rect(1561, 289, 39, 50),
                pygame.Rect(1605, 333, 28, 117),
                pygame.Rect(1493, 741, 60, 57),
                pygame.Rect(1071, 799, 155, 73),
                pygame.Rect(1124, 864, 76, 108),
                pygame.Rect(1413, 962, 106, 101),
                pygame.Rect(1446, 1060, 42, 97),
                pygame.Rect(1485, 1110, 6, 3),
                pygame.Rect(1481, 1107, 42, 103),
                pygame.Rect(1376, 1067, 62, 86),
                pygame.Rect(1420, 1149, 71, 51),
                pygame.Rect(1563, 1228, 151, 139),
                pygame.Rect(1832, 1156, 59, 86),
                pygame.Rect(1856, 1224, 200, 83),
                pygame.Rect(1886, 1195, 68, 37),
                pygame.Rect(1987, 1188, 77, 40),
                pygame.Rect(1883, 1291, 95, 44),
                pygame.Rect(1914, 1325, 114, 49),
                pygame.Rect(1956, 1293, 94, 41),
                pygame.Rect(2042, 1227, 56, 40),
                pygame.Rect(1148, 1200, 39, 287),
                pygame.Rect(1083, 1342, 76, 138),
                pygame.Rect(1056, 1412, 43, 71),
                pygame.Rect(986, 1452, 80, 35),
                pygame.Rect(829, 1456, 85, 37),
                pygame.Rect(1229, 1345, 110, 147),
                pygame.Rect(1179, 1376, 73, 123),
                pygame.Rect(1570, 1348, 152, 48),
                pygame.Rect(2232, 372, 93, 71),
                pygame.Rect(2140, 433, 243, 60),
                pygame.Rect(2183, 485, 192, 63),
                pygame.Rect(2311, 531, 83, 41),
                pygame.Rect(2338, 568, 116, 86),
                pygame.Rect(2391, 549, 50, 23),
                pygame.Rect(2459, 623, 64, 111),
                pygame.Rect(2521, 690, 43, 150),
                pygame.Rect(2040, 666, 84, 206),
                pygame.Rect(1899, 507, 57, 161),
                pygame.Rect(2317, 862, 55, 96),
                pygame.Rect(2367, 880, 47, 89),
                pygame.Rect(2410, 901, 26, 85),
                pygame.Rect(2435, 911, 35, 50),
                pygame.Rect(2284, 896, 46, 34),
                pygame.Rect(1782, 922, 61, 79),
                pygame.Rect(613, 84, 150, 26),
                pygame.Rect(847, 79, 205, 33),
                pygame.Rect(948, 366, 70, 75),
                pygame.Rect(2809, 1207, 71, 286),
                pygame.Rect(2877, 1206, 8, 57),
                pygame.Rect(2338, 1414, 130, 90),
            ],
        "map_29":
            [
                pygame.Rect(1, 0, 2670, 342),
                pygame.Rect(2472, 446, 188, 252),
                pygame.Rect(2506, 351, 165, 110),
                pygame.Rect(2507, 335, 170, 26),
                pygame.Rect(2656, 450, 7, 722),
                pygame.Rect(2661, 704, 10, 471),
                pygame.Rect(2657, 1363, 13, 159),
                pygame.Rect(1, 342, 385, 503),
                pygame.Rect(-8, 838, 146, 692),
                pygame.Rect(141, 1151, 247, 379),
                pygame.Rect(487, 440, 392, 291),
                pygame.Rect(974, 444, 338, 286),
                pygame.Rect(1298, 453, 21, 273),
                pygame.Rect(531, 852, 332, 114),
                pygame.Rect(937, 860, 283, 133),
                pygame.Rect(1194, 999, 30, 317),
                pygame.Rect(962, 1201, 234, 121),
                pygame.Rect(530, 1394, 428, 129),
                pygame.Rect(943, 1421, 288, 98),
                pygame.Rect(1210, 1283, 51, 69),
                pygame.Rect(1145, 1321, 65, 38),
                pygame.Rect(1257, 1311, 15, 33),
                pygame.Rect(1324, 1447, 334, 77),
                pygame.Rect(1656, 1400, 111, 122),
                pygame.Rect(1748, 732, 153, 792),
                pygame.Rect(1898, 1354, 25, 180),
                pygame.Rect(1923, 1378, 22, 150),
                pygame.Rect(1940, 1397, 26, 128),
                pygame.Rect(1962, 1418, 29, 103),
                pygame.Rect(1988, 1418, 303, 105),
                pygame.Rect(2074, 1339, 183, 83),
                pygame.Rect(2042, 1396, 46, 24),
                pygame.Rect(2358, 1352, 220, 163),
                pygame.Rect(2573, 1417, 26, 108),
                pygame.Rect(2596, 1482, 20, 43),
                pygame.Rect(2362, 1504, 213, 17),
                pygame.Rect(1897, 909, 39, 189),
                pygame.Rect(1926, 921, 56, 179),
                pygame.Rect(1981, 950, 59, 155),
                pygame.Rect(2031, 998, 44, 93),
                pygame.Rect(1968, 812, 132, 80),
                pygame.Rect(2045, 773, 25, 52),
                pygame.Rect(2066, 795, 31, 21),
                pygame.Rect(2033, 778, 21, 29),
                pygame.Rect(2018, 797, 18, 8),
                pygame.Rect(1963, 884, 130, 32),
                pygame.Rect(2099, 884, 30, 41),
                pygame.Rect(2048, 915, 65, 22),
                pygame.Rect(2005, 919, 94, 34),
                pygame.Rect(2029, 949, 43, 27),
                pygame.Rect(2104, 744, 136, 122),
                pygame.Rect(2164, 859, 58, 40),
                pygame.Rect(2333, 761, 122, 125),
                pygame.Rect(2308, 819, 28, 63),
                pygame.Rect(2463, 798, 108, 119),
                pygame.Rect(2544, 776, 22, 27),
                pygame.Rect(2417, 885, 43, 40),
                pygame.Rect(2466, 933, 93, 307),
                pygame.Rect(2553, 1031, 28, 109),
                pygame.Rect(2186, 954, 188, 114),
                pygame.Rect(2164, 979, 24, 182),
                pygame.Rect(2151, 992, 19, 60),
                pygame.Rect(2133, 1005, 18, 45),
                pygame.Rect(2147, 1072, 15, 82),
                pygame.Rect(2146, 1147, 44, 17),
                pygame.Rect(1918, 1183, 113, 170),
                pygame.Rect(2035, 1223, 32, 86),
                pygame.Rect(2189, 1126, 185, 100),
                pygame.Rect(2190, 1225, 82, 19),
                pygame.Rect(2281, 1223, 48, 35),
                pygame.Rect(2369, 1132, 35, 86),
                pygame.Rect(2330, 1060, 43, 82),
                pygame.Rect(1686, 782, 58, 85),
                pygame.Rect(1328, 1157, 56, 173),
                pygame.Rect(1386, 1165, 28, 51),
                pygame.Rect(1394, 1217, 48, 130),
                pygame.Rect(1421, 1180, 21, 36),
                pygame.Rect(1572, 1175, 40, 177),
                pygame.Rect(476, 1201, 62, 64),
                pygame.Rect(527, 1204, 264, 130),
                pygame.Rect(472, 971, 62, 54),
                pygame.Rect(495, 1021, 43, 45),
                pygame.Rect(479, 1064, 45, 43),
                pygame.Rect(530, 955, 86, 255),
                pygame.Rect(604, 954, 73, 104),
                pygame.Rect(740, 994, 134, 66),
                pygame.Rect(705, 1034, 96, 75),
                pygame.Rect(824, 1085, 133, 98),
                pygame.Rect(947, 982, 143, 70),
                pygame.Rect(1152, 1000, 45, 217),
                pygame.Rect(1130, 1040, 41, 162),
                pygame.Rect(1095, 1107, 31, 96),
                pygame.Rect(1074, 1176, 95, 22),
                pygame.Rect(975, 817, 151, 43),
                pygame.Rect(582, 727, 174, 39),
                pygame.Rect(631, 760, 132, 42),
                pygame.Rect(776, 744, 69, 52),
                pygame.Rect(495, 747, 20, 42),
                pygame.Rect(510, 741, 62, 39),
                pygame.Rect(267, 847, 55, 41),
                pygame.Rect(139, 1010, 68, 102),
                pygame.Rect(233, 1062, 47, 42),
                pygame.Rect(439, 515, 47, 56),
                pygame.Rect(931, 458, 37, 65),
                pygame.Rect(1070, 332, 132, 109),
                pygame.Rect(1412, 380, 51, 94),
                pygame.Rect(1330, 659, 72, 105),
                pygame.Rect(1419, 618, 45, 95),
                pygame.Rect(1565, 480, 117, 116),
                pygame.Rect(1574, 332, 493, 158),
                pygame.Rect(1679, 491, 139, 146),
                pygame.Rect(1797, 484, 633, 35),
                pygame.Rect(1901, 517, 222, 85),
                pygame.Rect(2114, 529, 97, 154),
                pygame.Rect(2034, 603, 81, 58),
                pygame.Rect(1993, 593, 50, 30),
                pygame.Rect(2204, 531, 180, 55),
                pygame.Rect(2392, 574, 45, 58),
                pygame.Rect(2433, 602, 40, 70),
                pygame.Rect(2370, 514, 57, 57),
                pygame.Rect(2281, 585, 111, 101),
                pygame.Rect(1914, 720, 42, 118),
                pygame.Rect(1737, 699, 171, 31),
                pygame.Rect(1900, 721, 19, 13),
                pygame.Rect(1497, 807, 34, 231),
                pygame.Rect(1528, 814, 31, 232),
                pygame.Rect(1626, 1191, 37, 165),
                pygame.Rect(1603, 1193, 23, 149),
                pygame.Rect(1660, 1198, 31, 136),
                pygame.Rect(1555, 838, 37, 212),
                pygame.Rect(1375, 1059, 289, 43),
                pygame.Rect(1628, 1107, 23, 64),
                pygame.Rect(1375, 1105, 23, 47),
                pygame.Rect(1336, 910, 55, 209),
                pygame.Rect(1443, 842, 65, 215),
                pygame.Rect(1392, 864, 88, 210),
                pygame.Rect(1364, 886, 50, 25),
                pygame.Rect(1468, 826, 43, 29),
                pygame.Rect(1564, 881, 93, 187),
                pygame.Rect(1589, 854, 27, 30),
                pygame.Rect(1609, 867, 29, 16),
                pygame.Rect(1655, 948, 26, 65),
                pygame.Rect(1651, 1012, 40, 80),
                pygame.Rect(384, 339, 56, 57),
                pygame.Rect(434, 336, 47, 37),
                pygame.Rect(1042, 730, 223, 32),
                pygame.Rect(1227, 752, 40, 33),
                pygame.Rect(973, 724, 66, 38),
                pygame.Rect(1523, 397, 47, 71),
                pygame.Rect(1531, 511, 33, 57),
                pygame.Rect(1537, 589, 28, 33),
                pygame.Rect(1886, 1170, 46, 19),
                pygame.Rect(2139, 1177, 46, 50),
                pygame.Rect(2158, 1228, 31, 20),
            ],
        "map_30":
            [
                pygame.Rect(-9, 10, 18, 922),
                pygame.Rect(1, 9, 404, 106),
                pygame.Rect(12, 107, 312, 27),
                pygame.Rect(626, 7, 1039, 96),
                pygame.Rect(725, 103, 315, 27),
                pygame.Rect(1319, 179, 269, 79),
                pygame.Rect(1429, 122, 69, 60),
                pygame.Rect(392, 336, 124, 539),
                pygame.Rect(508, 723, 74, 76),
                pygame.Rect(628, 320, 27, 387),
                pygame.Rect(631, 269, 21, 50),
                pygame.Rect(648, 266, 460, 46),
                pygame.Rect(1096, 301, 14, 430),
                pygame.Rect(1093, 842, 25, 89),
                pygame.Rect(633, 821, 21, 107),
                pygame.Rect(1039, 315, 72, 416),
                pygame.Rect(645, 321, 77, 379),
                pygame.Rect(643, 816, 73, 118),
                pygame.Rect(1038, 863, 72, 61),
                pygame.Rect(825, 801, 104, 116),
                pygame.Rect(957, 421, 76, 68),
                pygame.Rect(950, 505, 77, 58),
                pygame.Rect(958, 579, 71, 62),
                pygame.Rect(946, 657, 84, 73),
                pygame.Rect(729, 413, 74, 59),
                pygame.Rect(723, 311, 149, 63),
                pygame.Rect(879, 307, 158, 60),
                pygame.Rect(728, 510, 65, 44),
                pygame.Rect(720, 589, 74, 47),
                pygame.Rect(730, 668, 84, 73),
                pygame.Rect(665, 702, 59, 31),
                pygame.Rect(130, 338, 108, 529),
                pygame.Rect(35, 746, 71, 56),
                pygame.Rect(241, 608, 48, 62),
                pygame.Rect(91, 556, 63, 43),
                pygame.Rect(1406, 712, 70, 53),
                pygame.Rect(1332, 759, 223, 72),
                pygame.Rect(1399, 836, 75, 63),
                pygame.Rect(1479, 830, 76, 26),
                pygame.Rect(1653, 1, 12, 925),
                pygame.Rect(1106, 921, 563, 10),
                pygame.Rect(705, 923, 393, 10),
                pygame.Rect(-1, 920, 647, 8),
                pygame.Rect(1584, 99, 33, 40),
                pygame.Rect(1603, 125, 11, 23),
                pygame.Rect(1345, 826, 15, 32),
            ],
        "map_31":
            [
                pygame.Rect(461, 1, 7, 683),
                pygame.Rect(140, 681, 326, 31),
                pygame.Rect(174, 643, 114, 42),
                pygame.Rect(287, 651, 67, 29),
                pygame.Rect(308, 642, 23, 12),
                pygame.Rect(355, 645, 106, 30),
                pygame.Rect(-1, 679, 45, 32),
                pygame.Rect(-6, 3, 5, 712),
                pygame.Rect(-4, -7, 467, 85),
                pygame.Rect(5, 68, 41, 30),
                pygame.Rect(43, 71, 68, 28),
                pygame.Rect(110, 75, 191, 22),
                pygame.Rect(-8, 131, 320, 57),
                pygame.Rect(352, 152, 112, 41),
                pygame.Rect(336, 59, 87, 34),
                pygame.Rect(417, 299, 53, 276),
                pygame.Rect(352, 280, 69, 94),
                pygame.Rect(262, 366, 89, 29),
                pygame.Rect(286, 320, 24, 47),
                pygame.Rect(310, 319, 40, 49),
                pygame.Rect(252, 346, 34, 28),
                pygame.Rect(258, 374, 51, 197),
                pygame.Rect(301, 526, 87, 47),
                pygame.Rect(392, 523, 24, 44),
                pygame.Rect(312, 563, 30, 28),
                pygame.Rect(226, 520, 29, 33),
                pygame.Rect(226, 400, 31, 29),
                pygame.Rect(250, 109, 27, 26),
                pygame.Rect(102, 106, 26, 25),
                pygame.Rect(2, 107, 13, 20),
                pygame.Rect(302, 396, 30, 36),
            ],
        "map_32":
            [
                pygame.Rect(-5, -15, 249, 121),
                pygame.Rect(0, 107, 74, 223),
                pygame.Rect(72, 179, 62, 26),
                pygame.Rect(147, 125, 63, 51),
                pygame.Rect(196, 183, 65, 13),
                pygame.Rect(204, 101, 51, 23),
                pygame.Rect(70, 103, 35, 35),
                pygame.Rect(71, 136, 18, 18),
                pygame.Rect(117, 252, 152, 91),
                pygame.Rect(110, 335, 46, 106),
                pygame.Rect(4, 321, 70, 274),
                pygame.Rect(70, 302, 27, 118),
                pygame.Rect(23, 505, 93, 128),
                pygame.Rect(107, 558, 52, 51),
                pygame.Rect(143, 509, 142, 132),
                pygame.Rect(-1, 604, 275, 238),
                pygame.Rect(281, 650, 93, 196),
                pygame.Rect(374, 679, 65, 163),
                pygame.Rect(369, 671, 26, 21),
                pygame.Rect(521, 529, 75, 83),
                pygame.Rect(462, 587, 58, 91),
                pygame.Rect(442, 617, 27, 62),
                pygame.Rect(611, 498, 77, 62),
                pygame.Rect(591, 542, 28, 79),
                pygame.Rect(615, 563, 70, 52),
                pygame.Rect(452, 712, 49, 65),
                pygame.Rect(581, 667, 136, 121),
                pygame.Rect(431, 820, 596, 27),
                pygame.Rect(794, 670, 82, 125),
                pygame.Rect(781, 698, 29, 84),
                pygame.Rect(710, 727, 27, 30),
                pygame.Rect(563, 723, 34, 46),
                pygame.Rect(784, 502, 83, 107),
                pygame.Rect(830, 613, 32, 14),
                pygame.Rect(883, 505, 9, 103),
                pygame.Rect(899, 557, 30, 47),
                pygame.Rect(886, 503, 33, 40),
                pygame.Rect(917, 570, 48, 102),
                pygame.Rect(950, 584, 39, 79),
                pygame.Rect(892, 612, 35, 41),
                pygame.Rect(949, 658, 38, 57),
                pygame.Rect(978, 664, 44, 111),
                pygame.Rect(957, 712, 27, 59),
                pygame.Rect(936, 674, 20, 46),
                pygame.Rect(241, -12, 59, 16),
                pygame.Rect(371, -16, 68, 18),
                pygame.Rect(426, -20, 1078, 164),
                pygame.Rect(411, 15, 26, 95),
                pygame.Rect(412, 134, 16, 69),
                pygame.Rect(463, 138, 50, 30),
                pygame.Rect(505, 139, 12, 94),
                pygame.Rect(488, 125, 110, 74),
                pygame.Rect(565, 198, 35, 25),
                pygame.Rect(423, 196, 14, 141),
                pygame.Rect(392, 199, 23, 45),
                pygame.Rect(407, 202, 20, 12),
                pygame.Rect(430, 122, 6, 79),
                pygame.Rect(433, 282, 168, 18),
                pygame.Rect(594, 282, 9, 82),
                pygame.Rect(600, 336, 98, 21),
                pygame.Rect(676, 328, 22, 30),
                pygame.Rect(671, 347, 27, 44),
                pygame.Rect(592, 347, 91, 44),
                pygame.Rect(435, 293, 164, 56),
                pygame.Rect(461, 344, 29, 19),
                pygame.Rect(490, 347, 69, 31),
                pygame.Rect(559, 340, 35, 33),
                pygame.Rect(798, 333, 27, 46),
                pygame.Rect(815, 335, 83, 19),
                pygame.Rect(892, 284, 14, 59),
                pygame.Rect(904, 284, 116, 64),
                pygame.Rect(914, 341, 76, 22),
                pygame.Rect(801, 350, 105, 39),
                pygame.Rect(840, 390, 26, 22),
                pygame.Rect(604, 389, 70, 21),
                pygame.Rect(601, 143, 116, 98),
                pygame.Rect(662, 234, 40, 26),
                pygame.Rect(775, 140, 85, 95),
                pygame.Rect(263, 319, 23, 95),
                pygame.Rect(291, 379, 19, 99),
                pygame.Rect(310, 384, 16, 41),
                pygame.Rect(248, 27, 25, 36),
                pygame.Rect(168, 199, 19, 24),
                pygame.Rect(282, 554, 18, 30),
                pygame.Rect(844, 202, 10, 69),
                pygame.Rect(862, 194, 33, 53),
                pygame.Rect(964, 131, 15, 107),
                pygame.Rect(974, 139, 48, 38),
                pygame.Rect(861, 140, 107, 66),
                pygame.Rect(927, 200, 30, 23),
                pygame.Rect(1008, 157, 10, 137),
                pygame.Rect(785, 224, 42, 30),
                pygame.Rect(1016, 157, 68, 69),
                pygame.Rect(1081, 144, 40, 81),
                pygame.Rect(1109, 148, 67, 79),
                pygame.Rect(1159, 149, 342, 109),
                pygame.Rect(1141, 230, 158, 81),
                pygame.Rect(1118, 296, 33, 76),
                pygame.Rect(1150, 310, 12, 123),
                pygame.Rect(1174, 352, 71, 33),
                pygame.Rect(1162, 311, 50, 22),
                pygame.Rect(1276, 339, 22, 43),
                pygame.Rect(1166, 404, 89, 59),
                pygame.Rect(1148, 517, 12, 44),
                pygame.Rect(1157, 520, 143, 37),
                pygame.Rect(1210, 501, 62, 20),
                pygame.Rect(1159, 550, 82, 34),
                pygame.Rect(1128, 619, 77, 60),
                pygame.Rect(1302, 621, 78, 55),
                pygame.Rect(1308, 701, 62, 30),
                pygame.Rect(1143, 701, 56, 25),
                pygame.Rect(1403, 582, 103, 253),
                pygame.Rect(1390, 747, 32, 69),
                pygame.Rect(1378, 675, 31, 42),
                pygame.Rect(1468, 530, 38, 64),
                pygame.Rect(1430, 548, 65, 47),
                pygame.Rect(1424, 252, 72, 271),
                pygame.Rect(1373, 518, 96, 43),
                pygame.Rect(1397, 452, 16, 59),
                pygame.Rect(1297, 300, 81, 109),
                pygame.Rect(1299, 248, 134, 60),
                pygame.Rect(1372, 301, 55, 50),
                pygame.Rect(1318, 406, 46, 22),
                pygame.Rect(1101, 819, 312, 18),
                pygame.Rect(1117, 522, 19, 26),
                pygame.Rect(414, 210, 13, 73),
                pygame.Rect(263, 628, 30, 34),
                pygame.Rect(417, 644, 26, 36),
                pygame.Rect(629, 779, 43, 28),
            ],
        "map_33":
            [
                pygame.Rect(0, 0, 1064, 87),
                pygame.Rect(1064, 0, 280, 168),
                pygame.Rect(1344, 0, 273, 124),
                pygame.Rect(1300, 227, 161, 130),
                pygame.Rect(760, 141, 140, 77),
                pygame.Rect(1516, 227, 105, 47),
                pygame.Rect(1621, 396, 36, 905),
                pygame.Rect(0, 0, 43, 906),
                pygame.Rect(210, 274, 386, 109),
                pygame.Rect(151, 507, 540, 142),
                pygame.Rect(631, 693, 83, 63),
                pygame.Rect(68, 816, 705, 906),
                pygame.Rect(883, 810, 728, 903),
                pygame.Rect(1455, 540, 80, 104),
                pygame.Rect(1455, 540, 80, 104),
            ],
        "map_34":
            [
                pygame.Rect(0, 12, 1539, 110),
                pygame.Rect(908, 102, 53, 180),
                pygame.Rect(375, 101, 65, 181),
                pygame.Rect(435, 203, 474, 78),
                pygame.Rect(387, 268, 46, 33),
                pygame.Rect(457, 274, 37, 27),
                pygame.Rect(526, 274, 31, 27),
                pygame.Rect(588, 270, 31, 34),
                pygame.Rect(655, 275, 33, 30),
                pygame.Rect(713, 272, 36, 25),
                pygame.Rect(785, 273, 36, 29),
                pygame.Rect(846, 267, 37, 38),
                pygame.Rect(905, 271, 40, 26),
                pygame.Rect(978, 140, 30, 36),
                pygame.Rect(976, 177, 34, 36),
                pygame.Rect(968, 221, 40, 32),
                pygame.Rect(331, 145, 29, 27),
                pygame.Rect(337, 183, 24, 36),
                pygame.Rect(328, 231, 37, 23),
                pygame.Rect(10, 132, 51, 39),
                pygame.Rect(117, 199, 99, 85),
                pygame.Rect(76, 223, 38, 46),
                pygame.Rect(153, 164, 35, 35),
                pygame.Rect(217, 226, 29, 42),
                pygame.Rect(149, 283, 45, 38),
                pygame.Rect(3, 284, 63, 86),
                pygame.Rect(70, 346, 49, 35),
                pygame.Rect(1, 115, 9, 749),
                pygame.Rect(10, 525, 110, 113),
                pygame.Rect(123, 566, 44, 46),
                pygame.Rect(316, 538, 447, 95),
                pygame.Rect(424, 502, 29, 40),
                pygame.Rect(617, 503, 35, 43),
                pygame.Rect(415, 632, 46, 41),
                pygame.Rect(620, 637, 38, 40),
                pygame.Rect(769, 391, 176, 88),
                pygame.Rect(858, 363, 37, 32),
                pygame.Rect(741, 420, 33, 38),
                pygame.Rect(952, 427, 43, 35),
                pygame.Rect(841, 482, 40, 37),
                pygame.Rect(1173, 189, 49, 45),
                pygame.Rect(1274, 158, 43, 28),
                pygame.Rect(1223, 179, 128, 70),
                pygame.Rect(1361, 206, 42, 29),
                pygame.Rect(1270, 254, 44, 40),
                pygame.Rect(1362, 280, 123, 78),
                pygame.Rect(1434, 244, 35, 37),
                pygame.Rect(1528, 122, 11, 733),
                pygame.Rect(1028, 844, 506, 10),
                pygame.Rect(7, 789, 55, 53),
                pygame.Rect(11, 848, 896, 12),
                pygame.Rect(124, 673, 113, 85),
                pygame.Rect(163, 632, 39, 41),
                pygame.Rect(71, 715, 50, 36),
                pygame.Rect(235, 719, 51, 28),
                pygame.Rect(158, 767, 43, 38),
                pygame.Rect(409, 744, 54, 27),
                pygame.Rect(382, 765, 191, 74),
                pygame.Rect(573, 794, 46, 31),
                pygame.Rect(701, 771, 68, 65),
                pygame.Rect(708, 726, 52, 48),
                pygame.Rect(774, 792, 61, 36),
                pygame.Rect(656, 788, 46, 40),
                pygame.Rect(331, 790, 45, 41),
                pygame.Rect(574, 400, 86, 87),
                pygame.Rect(658, 434, 34, 43),
                pygame.Rect(539, 435, 38, 43),
                pygame.Rect(527, 423, 14, 40),
                pygame.Rect(460, 360, 30, 31),
                pygame.Rect(424, 403, 87, 77),
                pygame.Rect(390, 439, 41, 27),
                pygame.Rect(1037, 526, 130, 43),
                pygame.Rect(1178, 543, 40, 28),
                pygame.Rect(1311, 522, 26, 40),
                pygame.Rect(1364, 530, 116, 33),
                pygame.Rect(1440, 133, 44, 55),
                pygame.Rect(1235, 110, 50, 35),
                pygame.Rect(1297, 115, 62, 29),
                pygame.Rect(1366, 120, 50, 24),
                pygame.Rect(1035, 565, 51, 81),
                pygame.Rect(979, 648, 48, 50),
                pygame.Rect(984, 697, 51, 46),
                pygame.Rect(1032, 645, 57, 97),
                pygame.Rect(1027, 575, 10, 65),
                pygame.Rect(1082, 577, 450, 119),
                pygame.Rect(1307, 681, 49, 38),
                pygame.Rect(1233, 684, 47, 41),
                pygame.Rect(1394, 714, 31, 28),
                pygame.Rect(1436, 720, 40, 41),
                pygame.Rect(1482, 694, 49, 152),
                pygame.Rect(1098, 801, 182, 32),
                pygame.Rect(1304, 799, 57, 42),
                pygame.Rect(1370, 789, 58, 53),
                pygame.Rect(1435, 776, 49, 67),
                pygame.Rect(71, 809, 43, 33),
            ],
        "map_35":
            [
                pygame.Rect(-1, -5, 174, 843),
                pygame.Rect(171, -6, 1417, 9),
                pygame.Rect(1431, -2, 163, 841),
                pygame.Rect(176, 825, 1034, 12),
                pygame.Rect(393, 237, 16, 230),
                pygame.Rect(1183, 228, 17, 238),
                pygame.Rect(649, 29, 309, 44),
                pygame.Rect(960, 43, 75, 56),
                pygame.Rect(1030, 69, 45, 41),
                pygame.Rect(1068, 89, 37, 48),
                pygame.Rect(1105, 110, 25, 52),
                pygame.Rect(1125, 129, 26, 59),
                pygame.Rect(1150, 150, 14, 58),
                pygame.Rect(1162, 177, 23, 48),
                pygame.Rect(622, 35, 30, 58),
                pygame.Rect(571, 43, 53, 61),
                pygame.Rect(536, 55, 38, 50),
                pygame.Rect(665, 75, 33, 29),
                pygame.Rect(774, 70, 41, 44),
                pygame.Rect(519, 66, 15, 60),
                pygame.Rect(490, 75, 27, 64),
                pygame.Rect(476, 93, 14, 69),
                pygame.Rect(451, 116, 29, 71),
                pygame.Rect(425, 142, 24, 72),
                pygame.Rect(404, 182, 33, 54),
                pygame.Rect(475, 157, 45, 35),
                pygame.Rect(734, 160, 123, 87),
                pygame.Rect(893, 70, 94, 36),
                pygame.Rect(697, 180, 29, 23),
                pygame.Rect(866, 180, 29, 30),
                pygame.Rect(434, 205, 76, 46),
                pygame.Rect(416, 257, 141, 128),
                pygame.Rect(560, 279, 15, 50),
                pygame.Rect(416, 384, 98, 44),
                pygame.Rect(415, 428, 62, 30),
                pygame.Rect(1075, 162, 46, 31),
                pygame.Rect(1072, 205, 100, 47),
                pygame.Rect(1031, 200, 25, 53),
                pygame.Rect(1043, 252, 129, 115),
                pygame.Rect(1012, 320, 47, 49),
                pygame.Rect(1071, 379, 103, 60),
                pygame.Rect(1105, 432, 70, 32),
                pygame.Rect(390, 541, 15, 286),
                pygame.Rect(401, 538, 354, 10),
                pygame.Rect(837, 537, 359, 14),
                pygame.Rect(1178, 551, 21, 277),
                pygame.Rect(917, 550, 71, 69),
                pygame.Rect(916, 606, 39, 29),
                pygame.Rect(1040, 553, 139, 49),
                pygame.Rect(1140, 600, 37, 91),
                pygame.Rect(1107, 600, 36, 24),
                pygame.Rect(1069, 600, 33, 21),
                pygame.Rect(1049, 602, 15, 20),
                pygame.Rect(1090, 715, 81, 90),
                pygame.Rect(1035, 754, 53, 45),
                pygame.Rect(924, 743, 106, 60),
                pygame.Rect(409, 806, 778, 25),
                pygame.Rect(899, 716, 16, 92),
                pygame.Rect(901, 546, 13, 104),
                pygame.Rect(414, 560, 205, 36),
                pygame.Rect(415, 612, 125, 37),
                pygame.Rect(416, 654, 37, 35),
                pygame.Rect(407, 692, 50, 111),
                pygame.Rect(462, 704, 45, 94),
                pygame.Rect(518, 755, 324, 50),
                pygame.Rect(858, 762, 42, 43),
                pygame.Rect(587, 705, 98, 41),
                pygame.Rect(690, 716, 45, 34),
                pygame.Rect(840, 533, 61, 77),
                pygame.Rect(620, 547, 131, 58),
                pygame.Rect(1185, -7, 17, 244),
                pygame.Rect(395, -1, 15, 240),
            ],
        "map_36":
            [
                pygame.Rect(1147, -2, 915, 105),
                pygame.Rect(2031, 22, 31, 1177),
                pygame.Rect(0, 1188, 2037, 17),
                pygame.Rect(3, 23, 10, 1168),
                pygame.Rect(12, 23, 982, 88),
                pygame.Rect(981, -8, 13, 38),
                pygame.Rect(841, 324, 72, 92),
                pygame.Rect(852, 410, 54, 65),
                pygame.Rect(922, 28, 29, 517),
                pygame.Rect(854, 480, 52, 59),
                pygame.Rect(361, 331, 377, 135),
                pygame.Rect(572, 480, 179, 56),
                pygame.Rect(354, 459, 215, 37),
                pygame.Rect(685, 132, 226, 58),
                pygame.Rect(814, 185, 64, 53),
                pygame.Rect(693, 102, 209, 31),
                pygame.Rect(369, 110, 177, 73),
                pygame.Rect(312, 28, 37, 519),
                pygame.Rect(8, 127, 57, 86),
                pygame.Rect(62, 118, 67, 65),
                pygame.Rect(143, 103, 34, 44),
                pygame.Rect(275, 111, 25, 60),
                pygame.Rect(9, 281, 51, 221),
                pygame.Rect(72, 336, 47, 128),
                pygame.Rect(117, 385, 30, 152),
                pygame.Rect(90, 469, 29, 66),
                pygame.Rect(169, 423, 41, 69),
                pygame.Rect(9, 693, 50, 205),
                pygame.Rect(68, 705, 56, 199),
                pygame.Rect(129, 731, 45, 125),
                pygame.Rect(230, 1047, 208, 141),
                pygame.Rect(168, 1123, 58, 60),
                pygame.Rect(443, 1084, 43, 92),
                pygame.Rect(502, 1128, 366, 58),
                pygame.Rect(507, 1075, 167, 39),
                pygame.Rect(759, 1066, 101, 54),
                pygame.Rect(879, 670, 39, 517),
                pygame.Rect(344, 704, 325, 211),
                pygame.Rect(685, 760, 48, 111),
                pygame.Rect(830, 701, 42, 241),
                pygame.Rect(814, 770, 16, 172),
                pygame.Rect(257, 788, 53, 133),
                pygame.Rect(316, 761, 41, 152),
                pygame.Rect(662, 697, 26, 175),
                pygame.Rect(1218, 21, 38, 445),
                pygame.Rect(1164, 302, 50, 115),
                pygame.Rect(1168, 96, 40, 132),
                pygame.Rect(1252, 395, 122, 70),
                pygame.Rect(1259, 278, 106, 110),
                pygame.Rect(1491, 322, 154, 66),
                pygame.Rect(1493, 393, 314, 77),
                pygame.Rect(1644, 18, 49, 372),
                pygame.Rect(1914, 397, 145, 67),
                pygame.Rect(1924, 452, 95, 51),
                pygame.Rect(1690, 234, 63, 119),
                pygame.Rect(1928, 347, 99, 40),
                pygame.Rect(1958, 151, 61, 156),
                pygame.Rect(1698, 100, 59, 52),
                pygame.Rect(1781, 120, 44, 37),
                pygame.Rect(1849, 84, 38, 70),
                pygame.Rect(1927, 100, 54, 51),
                pygame.Rect(1912, 169, 29, 55),
                pygame.Rect(1257, 106, 191, 43),
                pygame.Rect(1265, 145, 45, 62),
                pygame.Rect(1458, 105, 187, 55),
                pygame.Rect(1467, 166, 56, 19),
                pygame.Rect(1523, 160, 119, 67),
                pygame.Rect(1148, 803, 69, 93),
                pygame.Rect(1159, 900, 56, 68),
                pygame.Rect(1215, 776, 42, 420),
                pygame.Rect(924, 986, 58, 198),
                pygame.Rect(979, 1063, 14, 124),
                pygame.Rect(1164, 1061, 53, 123),
                pygame.Rect(928, 812, 51, 129),
                pygame.Rect(943, 777, 19, 40),
                pygame.Rect(950, 940, 17, 31),
                pygame.Rect(1246, 775, 125, 149),
                pygame.Rect(1362, 779, 543, 67),
                pygame.Rect(2016, 789, 23, 405),
                pygame.Rect(1730, 779, 41, 413),
                pygame.Rect(1824, 941, 61, 55),
                pygame.Rect(1770, 866, 111, 312),
                pygame.Rect(1868, 1105, 50, 87),
                pygame.Rect(1878, 975, 35, 67),
                pygame.Rect(1868, 849, 38, 100),
                pygame.Rect(1977, 851, 48, 58),
                pygame.Rect(474, 1130, 26, 52),
                pygame.Rect(65, 464, 21, 40),
                pygame.Rect(80, 503, 9, 41),
                pygame.Rect(560, 99, 122, 28),
                pygame.Rect(1581, 299, 27, 30),
            ],
        "map_37":
            [
                pygame.Rect(-25, -10, 573, 575),
                pygame.Rect(0, 665, 532, 430),
                pygame.Rect(-9, 565, 518, 105),
                pygame.Rect(526, 676, 65, 421),
                pygame.Rect(586, 796, 28, 178),
                pygame.Rect(550, -1, 170, 123),
                pygame.Rect(556, 121, 173, 139),
                pygame.Rect(718, 149, 49, 176),
                pygame.Rect(760, 178, 21, 109),
                pygame.Rect(539, 239, 169, 144),
                pygame.Rect(709, 254, 36, 88),
                pygame.Rect(701, 337, 22, 25),
                pygame.Rect(535, 376, 151, 35),
                pygame.Rect(534, 408, 43, 24),
                pygame.Rect(741, 418, 146, 94),
                pygame.Rect(832, 373, 87, 48),
                pygame.Rect(881, 320, 76, 54),
                pygame.Rect(928, 278, 62, 46),
                pygame.Rect(938, 232, 99, 48),
                pygame.Rect(945, 153, 108, 83),
                pygame.Rect(830, 1, 216, 88),
                pygame.Rect(879, 91, 158, 65),
                pygame.Rect(713, 0, 1228, 19),
                pygame.Rect(1031, 8, 632, 105),
                pygame.Rect(1646, 15, 99, 171),
                pygame.Rect(1712, 126, 72, 126),
                pygame.Rect(1770, 156, 63, 153),
                pygame.Rect(1633, 379, 158, 61),
                pygame.Rect(1711, 356, 150, 67),
                pygame.Rect(1787, 307, 76, 67),
                pygame.Rect(1724, 427, 168, 75),
                pygame.Rect(1862, 447, 71, 89),
                pygame.Rect(1890, 523, 47, 55),
                pygame.Rect(1904, 568, 30, 191),
                pygame.Rect(1879, 654, 20, 108),
                pygame.Rect(1845, 681, 33, 108),
                pygame.Rect(1813, 710, 35, 218),
                pygame.Rect(1773, 915, 41, 149),
                pygame.Rect(1728, 1019, 47, 61),
                pygame.Rect(1354, 179, 72, 110),
                pygame.Rect(1406, 217, 76, 145),
                pygame.Rect(1474, 299, 56, 164),
                pygame.Rect(1518, 423, 72, 115),
                pygame.Rect(1496, 462, 36, 35),
                pygame.Rect(752, 701, 109, 77),
                pygame.Rect(840, 726, 65, 92),
                pygame.Rect(827, 778, 105, 91),
                pygame.Rect(886, 850, 78, 234),
                pygame.Rect(851, 990, 45, 95),
                pygame.Rect(589, 1076, 1180, 7),
                pygame.Rect(952, 915, 96, 169),
                pygame.Rect(917, 790, 46, 57),
                pygame.Rect(909, 734, 33, 48),
                pygame.Rect(1033, 898, 51, 60),
                pygame.Rect(1036, 1014, 72, 64),
                pygame.Rect(1094, 1049, 68, 33),
                pygame.Rect(1511, 685, 68, 104),
                pygame.Rect(1483, 744, 66, 68),
                pygame.Rect(1453, 784, 69, 63),
                pygame.Rect(1436, 886, 47, 58),
                pygame.Rect(1404, 908, 63, 60),
                pygame.Rect(1370, 923, 62, 53),
                pygame.Rect(1326, 942, 95, 52),
                pygame.Rect(1307, 996, 66, 33),
                pygame.Rect(1282, 1017, 52, 61),
                pygame.Rect(1257, 1039, 31, 38),
                pygame.Rect(1598, 838, 69, 33),
                pygame.Rect(1616, 866, 102, 68),
                pygame.Rect(1668, 847, 30, 38),
                pygame.Rect(1706, 876, 39, 85),
                pygame.Rect(1688, 928, 21, 24),
                pygame.Rect(1737, 888, 42, 89),
                pygame.Rect(1589, 904, 69, 62),
            ],
        "map_38":
            [
                pygame.Rect(44, 2, 2961, 115),
                pygame.Rect(1946, 685, 157, 140),
                pygame.Rect(1920, 723, 30, 80),
                pygame.Rect(1945, 811, 154, 44),
                pygame.Rect(2095, 719, 30, 104),
                pygame.Rect(2010, 662, 27, 33),
                pygame.Rect(1704, 249, 189, 107),
                pygame.Rect(1647, 109, 697, 225),
                pygame.Rect(2329, 111, 721, 355),
                pygame.Rect(2434, 459, 585, 198),
                pygame.Rect(2446, 655, 556, 42),
                pygame.Rect(2343, 947, 33, 48),
                pygame.Rect(2353, 990, 43, 23),
                pygame.Rect(2381, 1018, 42, 29),
                pygame.Rect(2372, 1016, 15, 15),
                pygame.Rect(2365, 1009, 17, 13),
                pygame.Rect(2387, 977, 329, 67),
                pygame.Rect(2703, 1015, 62, 79),
                pygame.Rect(2750, 1065, 77, 82),
                pygame.Rect(2823, 1104, 78, 90),
                pygame.Rect(2904, 964, 115, 737),
                pygame.Rect(2459, 831, 18, 143),
                pygame.Rect(2396, 906, 33, 63),
                pygame.Rect(2567, 851, 9, 138),
                pygame.Rect(2596, 894, 11, 98),
                pygame.Rect(2632, 853, 13, 145),
                pygame.Rect(2758, 903, 14, 153),
                pygame.Rect(2650, 915, 104, 86),
                pygame.Rect(2484, 858, 84, 116),
                pygame.Rect(2839, 1427, 70, 276),
                pygame.Rect(2639, 1599, 249, 104),
                pygame.Rect(2781, 1501, 69, 121),
                pygame.Rect(2807, 1484, 57, 38),
                pygame.Rect(1959, 1345, 148, 362),
                pygame.Rect(2088, 1508, 176, 194),
                pygame.Rect(2244, 1550, 40, 150),
                pygame.Rect(2278, 1593, 189, 88),
                pygame.Rect(2276, 1554, 39, 40),
                pygame.Rect(2090, 1235, 55, 106),
                pygame.Rect(2124, 1181, 126, 45),
                pygame.Rect(2113, 1221, 84, 46),
                pygame.Rect(2103, 1355, 81, 158),
                pygame.Rect(2189, 1441, 84, 68),
                pygame.Rect(2154, 1065, 31, 116),
                pygame.Rect(2193, 1114, 39, 69),
                pygame.Rect(2137, 1280, 32, 72),
                pygame.Rect(2169, 1272, 51, 13),
                pygame.Rect(2167, 333, 164, 90),
                pygame.Rect(1278, 118, 339, 492),
                pygame.Rect(1605, 247, 109, 164),
                pygame.Rect(1616, 406, 87, 25),
                pygame.Rect(1616, 429, 43, 33),
                pygame.Rect(1777, 350, 79, 23),
                pygame.Rect(1637, 471, 22, 103),
                pygame.Rect(1460, 604, 144, 27),
                pygame.Rect(1489, 636, 74, 19),
                pygame.Rect(1158, 474, 118, 122),
                pygame.Rect(1192, 590, 264, 58),
                pygame.Rect(1321, 638, 162, 68),
                pygame.Rect(1461, 632, 41, 24),
                pygame.Rect(1199, 373, 68, 77),
                pygame.Rect(1052, 124, 110, 109),
                pygame.Rect(1167, 163, 73, 89),
                pygame.Rect(1246, 191, 87, 70),
                pygame.Rect(891, 142, 95, 85),
                pygame.Rect(839, 219, 84, 51),
                pygame.Rect(863, 283, 84, 64),
                pygame.Rect(926, 235, 49, 62),
                pygame.Rect(994, 229, 38, 49),
                pygame.Rect(984, 157, 69, 63),
                pygame.Rect(1051, 238, 45, 30),
                pygame.Rect(928, 356, 59, 74),
                pygame.Rect(925, 447, 124, 152),
                pygame.Rect(920, 421, 37, 35),
                pygame.Rect(638, 108, 291, 386),
                pygame.Rect(1256, 310, 65, 60),
                pygame.Rect(751, 499, 135, 190),
                pygame.Rect(820, 450, 104, 167),
                pygame.Rect(873, 612, 33, 37),
                pygame.Rect(515, 169, 166, 178),
                pygame.Rect(482, 220, 195, 112),
                pygame.Rect(232, 109, 189, 185),
                pygame.Rect(76, 209, 196, 166),
                pygame.Rect(75, 372, 133, 46),
                pygame.Rect(89, 100, 172, 125),
                pygame.Rect(569, 124, 87, 64),
                pygame.Rect(580, 416, 159, 87),
                pygame.Rect(614, 493, 95, 55),
                pygame.Rect(600, 367, 55, 47),
                pygame.Rect(704, 498, 42, 36),
                pygame.Rect(905, 623, 14, 92),
                pygame.Rect(914, 629, 41, 42),
                pygame.Rect(26, 1, 58, 1267),
                pygame.Rect(-23, 1247, 121, 186),
                pygame.Rect(94, 1646, 1334, 29),
                pygame.Rect(593, 1309, 205, 370),
                pygame.Rect(670, 1241, 57, 98),
                pygame.Rect(634, 1283, 51, 33),
                pygame.Rect(723, 1273, 53, 62),
                pygame.Rect(930, 1295, 41, 371),
                pygame.Rect(893, 1331, 57, 329),
                pygame.Rect(764, 1481, 629, 208),
                pygame.Rect(963, 1331, 44, 162),
                pygame.Rect(982, 1377, 62, 108),
                pygame.Rect(810, 1378, 87, 99),
                pygame.Rect(832, 1364, 70, 23),
                pygame.Rect(870, 1336, 29, 41),
                pygame.Rect(237, 1585, 360, 63),
                pygame.Rect(294, 1533, 302, 52),
                pygame.Rect(389, 1438, 205, 94),
                pygame.Rect(486, 1337, 105, 99),
                pygame.Rect(431, 1363, 69, 74),
                pygame.Rect(348, 1508, 52, 19),
                pygame.Rect(347, 1520, 44, 19),
                pygame.Rect(192, 934, 193, 198),
                pygame.Rect(376, 870, 195, 140),
                pygame.Rect(438, 995, 94, 53),
                pygame.Rect(524, 985, 74, 68),
                pygame.Rect(96, 478, 176, 193),
                pygame.Rect(86, 394, 57, 58),
                pygame.Rect(166, 435, 81, 39),
                pygame.Rect(223, 614, 224, 329),
                pygame.Rect(364, 543, 58, 79),
                pygame.Rect(344, 590, 33, 30),
                pygame.Rect(316, 586, 47, 41),
                pygame.Rect(408, 667, 207, 238),
                pygame.Rect(499, 646, 51, 26),
                pygame.Rect(395, 1003, 40, 26),
                pygame.Rect(88, 1199, 145, 121),
                pygame.Rect(131, 1116, 146, 79),
                pygame.Rect(256, 1124, 58, 49),
                pygame.Rect(273, 1169, 30, 19),
                pygame.Rect(307, 1125, 55, 30),
                pygame.Rect(307, 1154, 30, 11),
                pygame.Rect(130, 1190, 45, 17),
                pygame.Rect(85, 1303, 55, 35),
                pygame.Rect(93, 1374, 39, 49),
                pygame.Rect(79, 454, 40, 28),
                pygame.Rect(898, 880, 642, 215),
                pygame.Rect(1297, 803, 36, 97),
                pygame.Rect(1321, 845, 115, 76),
                pygame.Rect(1430, 811, 26, 87),
                pygame.Rect(1459, 855, 58, 37),
                pygame.Rect(1177, 825, 57, 111),
                pygame.Rect(1218, 852, 47, 89),
                pygame.Rect(1251, 867, 38, 35),
                pygame.Rect(1145, 850, 52, 58),
                pygame.Rect(1135, 862, 40, 73),
                pygame.Rect(1161, 839, 39, 41),
                pygame.Rect(953, 855, 96, 104),
                pygame.Rect(991, 822, 34, 136),
                pygame.Rect(1019, 843, 29, 35),
                pygame.Rect(833, 968, 175, 204),
                pygame.Rect(795, 1040, 165, 26),
                pygame.Rect(817, 1010, 77, 39),
                pygame.Rect(800, 1067, 51, 32),
                pygame.Rect(815, 1092, 24, 72),
                pygame.Rect(845, 1158, 107, 44),
                pygame.Rect(1213, 1103, 154, 103),
                pygame.Rect(1382, 1111, 62, 70),
                pygame.Rect(1450, 1156, 48, 58),
                pygame.Rect(1411, 1645, 560, 39),
                pygame.Rect(1539, 910, 45, 178),
                pygame.Rect(1573, 931, 42, 126),
                pygame.Rect(1632, 901, 16, 140),
                pygame.Rect(1599, 971, 40, 73),
                pygame.Rect(1122, 1398, 121, 93),
                pygame.Rect(1019, 1414, 65, 57),
                pygame.Rect(1623, 1472, 340, 206),
                pygame.Rect(1745, 1434, 204, 58),
                pygame.Rect(1747, 1160, 192, 168),
                pygame.Rect(1850, 1315, 90, 75),
                pygame.Rect(1928, 1256, 50, 122),
                pygame.Rect(1716, 1193, 50, 116),
                pygame.Rect(1817, 1108, 101, 73),
                pygame.Rect(1851, 1068, 56, 52),
                pygame.Rect(1754, 1119, 68, 49),
                pygame.Rect(2812, 689, 196, 89),
                pygame.Rect(73, 484, 43, 160),
            ],
        "map_39":
            [
                pygame.Rect(0, 0, 136, 417),
                pygame.Rect(0, 605, 136, 1014),
                pygame.Rect(136, 0, 1688, 47),
                pygame.Rect(1726, 46, 1187, 1018),
                pygame.Rect(136, 966, 1684, 1018),
                pygame.Rect(869, 47, 411, 313),
                pygame.Rect(1105, 313, 217, 378),
            ],
        "map_40":
            [
                pygame.Rect(-10, -11, 1888, 81),
                pygame.Rect(972, 71, 189, 94),
                pygame.Rect(1094, 151, 56, 43),
                pygame.Rect(1158, 59, 150, 161),
                pygame.Rect(1140, 183, 37, 37),
                pygame.Rect(1130, 207, 24, 15),
                pygame.Rect(1174, 214, 33, 39),
                pygame.Rect(1239, 184, 77, 71),
                pygame.Rect(1208, 218, 29, 31),
                pygame.Rect(1296, 72, 49, 182),
                pygame.Rect(1341, 64, 539, 96),
                pygame.Rect(1354, 158, 152, 25),
                pygame.Rect(1580, 161, 65, 24),
                pygame.Rect(1712, 157, 62, 25),
                pygame.Rect(1814, 161, 66, 903),
                pygame.Rect(1799, 177, 24, 83),
                pygame.Rect(1354, 309, 157, 63),
                pygame.Rect(1603, 317, 72, 62),
                pygame.Rect(1604, 301, 69, 39),
                pygame.Rect(1714, 307, 64, 67),
                pygame.Rect(1801, 377, 21, 75),
                pygame.Rect(1773, 411, 28, 49),
                pygame.Rect(1663, 433, 96, 27),
                pygame.Rect(1381, 422, 85, 33),
                pygame.Rect(1245, 355, 71, 415),
                pygame.Rect(1306, 437, 48, 151),
                pygame.Rect(1344, 459, 196, 108),
                pygame.Rect(1313, 588, 83, 28),
                pygame.Rect(1436, 561, 34, 53),
                pygame.Rect(1599, 454, 215, 123),
                pygame.Rect(1655, 569, 33, 35),
                pygame.Rect(1778, 589, 33, 34),
                pygame.Rect(1202, 884, 123, 167),
                pygame.Rect(1323, 986, 496, 73),
                pygame.Rect(1635, 579, 13, 93),
                pygame.Rect(1648, 877, 16, 107),
                pygame.Rect(1430, 886, 13, 98),
                pygame.Rect(1422, 587, 20, 97),
                pygame.Rect(1758, 905, 56, 81),
                pygame.Rect(1321, 947, 44, 37),
                pygame.Rect(1190, 440, 56, 151),
                pygame.Rect(1014, 338, 111, 52),
                pygame.Rect(1081, 322, 37, 27),
                pygame.Rect(1218, 388, 22, 27),
                pygame.Rect(1179, 700, 61, 74),
                pygame.Rect(988, 988, 232, 64),
                pygame.Rect(1110, 949, 100, 45),
                pygame.Rect(1181, 900, 25, 53),
                pygame.Rect(1144, 920, 42, 25),
                pygame.Rect(1066, 911, 50, 59),
                pygame.Rect(1037, 947, 23, 36),
                pygame.Rect(820, 942, 25, 32),
                pygame.Rect(760, 923, 45, 50),
                pygame.Rect(0, 988, 877, 53),
                pygame.Rect(860, 981, 32, 65),
                pygame.Rect(-1, 952, 774, 31),
                pygame.Rect(-8, -1, 64, 954),
                pygame.Rect(52, 896, 38, 65),
                pygame.Rect(87, 914, 27, 47),
                pygame.Rect(50, 662, 34, 150),
                pygame.Rect(76, 680, 29, 131),
                pygame.Rect(102, 710, 23, 82),
                pygame.Rect(52, 705, 16, 143),
                pygame.Rect(40, 709, 199, 92),
                pygame.Rect(79, 797, 55, 60),
                pygame.Rect(58, 846, 35, 34),
                pygame.Rect(70, 876, 29, 27),
                pygame.Rect(142, 803, 30, 33),
                pygame.Rect(183, 795, 38, 32),
                pygame.Rect(305, 716, 326, 85),
                pygame.Rect(560, 558, 72, 241),
                pygame.Rect(530, 677, 36, 64),
                pygame.Rect(510, 689, 28, 43),
                pygame.Rect(503, 804, 53, 32),
                pygame.Rect(640, 735, 55, 60),
                pygame.Rect(634, 604, 41, 99),
                pygame.Rect(642, 572, 16, 38),
                pygame.Rect(745, 624, 119, 61),
                pygame.Rect(1008, 617, 113, 70),
                pygame.Rect(744, 330, 125, 69),
                pygame.Rect(524, 60, 382, 100),
                pygame.Rect(900, 60, 85, 20),
                pygame.Rect(548, 148, 85, 291),
                pygame.Rect(613, 132, 108, 44),
                pygame.Rect(621, 159, 87, 29),
                pygame.Rect(615, 179, 79, 43),
                pygame.Rect(620, 214, 46, 38),
                pygame.Rect(717, 145, 54, 45),
                pygame.Rect(667, 203, 46, 39),
                pygame.Rect(632, 242, 49, 36),
                pygame.Rect(35, 59, 496, 103),
                pygame.Rect(350, 147, 65, 32),
                pygame.Rect(163, 146, 73, 31),
                pygame.Rect(96, 135, 48, 59),
                pygame.Rect(45, 154, 62, 56),
                pygame.Rect(460, 146, 27, 41),
                pygame.Rect(457, 158, 74, 22),
                pygame.Rect(468, 174, 36, 41),
                pygame.Rect(519, 208, 31, 38),
                pygame.Rect(65, 275, 17, 158),
                pygame.Rect(91, 562, 94, 58),
                pygame.Rect(435, 605, 35, 33),
                pygame.Rect(341, 652, 63, 49),
                pygame.Rect(467, 592, 46, 40),
                pygame.Rect(449, 625, 77, 47),
                pygame.Rect(516, 613, 29, 34),
                pygame.Rect(437, 627, 26, 26),
                pygame.Rect(685, 777, 24, 31),
                pygame.Rect(336, 296, 71, 28),
                pygame.Rect(340, 360, 63, 30),
                pygame.Rect(337, 426, 72, 33),
                pygame.Rect(455, 297, 71, 33),
                pygame.Rect(523, 356, 28, 66),
                pygame.Rect(460, 364, 62, 28),
                pygame.Rect(453, 423, 70, 37),
                pygame.Rect(370, 195, 36, 68),
                pygame.Rect(274, 203, 41, 59),
                pygame.Rect(92, 200, 20, 23),
                pygame.Rect(180, 201, 43, 59),
                pygame.Rect(92, 294, 57, 35),
                pygame.Rect(180, 298, 69, 33),
                pygame.Rect(87, 361, 68, 32),
                pygame.Rect(184, 363, 63, 28),
                pygame.Rect(88, 429, 66, 29),
                pygame.Rect(186, 431, 61, 26),
                pygame.Rect(904, 75, 15, 17),
                pygame.Rect(1052, 962, 82, 29),
                pygame.Rect(1501, 808, 22, 27),
                pygame.Rect(1569, 720, 12, 22),
                pygame.Rect(1313, 615, 40, 37),
                pygame.Rect(1794, 622, 21, 21),
                pygame.Rect(1787, 622, 12, 17),
                pygame.Rect(1692, 960, 16, 35),
                pygame.Rect(630, 381, 34, 41),
                pygame.Rect(851, 155, 25, 29),
                pygame.Rect(1003, 149, 27, 37),
                pygame.Rect(58, 506, 12, 28),
                pygame.Rect(555, 422, 75, 28),
            ],
        "map_41":
            [
                pygame.Rect(2, -14, 33, 454),
                pygame.Rect(1, 600, 31, 451),
                pygame.Rect(18, 980, 140, 73),
                pygame.Rect(149, 1038, 105, 15),
                pygame.Rect(248, 983, 871, 72),
                pygame.Rect(360, 630, 135, 354),
                pygame.Rect(493, 662, 444, 327),
                pygame.Rect(817, 626, 124, 39),
                pygame.Rect(938, 726, 14, 257),
                pygame.Rect(947, 753, 27, 234),
                pygame.Rect(973, 767, 16, 223),
                pygame.Rect(989, 779, 15, 206),
                pygame.Rect(1002, 796, 19, 190),
                pygame.Rect(1021, 821, 20, 164),
                pygame.Rect(1043, 834, 78, 222),
                pygame.Rect(32, 674, 98, 79),
                pygame.Rect(122, 685, 16, 72),
                pygame.Rect(134, 724, 24, 37),
                pygame.Rect(64, 730, 31, 60),
                pygame.Rect(246, 672, 112, 83),
                pygame.Rect(228, 618, 75, 33),
                pygame.Rect(74, 611, 81, 45),
                pygame.Rect(68, 381, 89, 37),
                pygame.Rect(226, 376, 82, 45),
                pygame.Rect(34, -10, 118, 130),
                pygame.Rect(227, -5, 782, 130),
                pygame.Rect(131, -20, 118, 33),
                pygame.Rect(354, 117, 581, 282),
                pygame.Rect(933, 117, 75, 160),
                pygame.Rect(931, 271, 53, 42),
                pygame.Rect(920, 298, 45, 61),
                pygame.Rect(987, -9, 32, 256),
                pygame.Rect(1010, -4, 875, 144),
                pygame.Rect(1003, 130, 101, 45),
                pygame.Rect(993, 170, 73, 31),
                pygame.Rect(1000, 203, 53, 17),
                pygame.Rect(997, 217, 31, 17),
                pygame.Rect(1255, 127, 63, 70),
                pygame.Rect(1226, 159, 58, 44),
                pygame.Rect(1247, 193, 62, 22),
                pygame.Rect(1300, 124, 586, 90),
                pygame.Rect(1342, 202, 537, 68),
                pygame.Rect(1324, 232, 44, 41),
                pygame.Rect(1391, 266, 489, 47),
                pygame.Rect(1469, 259, 61, 189),
                pygame.Rect(1402, 311, 69, 52),
                pygame.Rect(1421, 360, 48, 48),
                pygame.Rect(1425, 404, 51, 32),
                pygame.Rect(1520, 272, 334, 114),
                pygame.Rect(1829, 269, 29, 117),
                pygame.Rect(1846, 380, 35, 672),
                pygame.Rect(1309, 828, 571, 220),
                pygame.Rect(1463, 624, 64, 213),
                pygame.Rect(1445, 730, 18, 113),
                pygame.Rect(1421, 762, 25, 85),
                pygame.Rect(1428, 749, 17, 17),
                pygame.Rect(1408, 777, 21, 65),
                pygame.Rect(1380, 805, 31, 31),
                pygame.Rect(1395, 790, 16, 18),
                pygame.Rect(1368, 818, 14, 17),
                pygame.Rect(1521, 730, 335, 113),
                pygame.Rect(1114, 435, 146, 142),
                pygame.Rect(753, 551, 37, 96),
                pygame.Rect(867, 361, 33, 86),
                pygame.Rect(787, 370, 35, 86),
                pygame.Rect(462, 359, 33, 90),
                pygame.Rect(500, 555, 30, 90),
                pygame.Rect(376, 549, 38, 70),
                pygame.Rect(378, 387, 31, 100),
                pygame.Rect(44, 137, 64, 25),
                pygame.Rect(86, 117, 19, 24),
                pygame.Rect(41, 149, 29, 31),
                pygame.Rect(47, 231, 26, 87),
                pygame.Rect(182, 228, 52, 43),
                pygame.Rect(233, 240, 27, 42),
                pygame.Rect(260, 254, 38, 48),
                pygame.Rect(264, 323, 80, 25),
                pygame.Rect(42, 871, 24, 58),
                pygame.Rect(50, 911, 55, 48),
                pygame.Rect(274, 932, 58, 35),
                pygame.Rect(309, 915, 47, 35),
                pygame.Rect(703, 419, 47, 55),
                pygame.Rect(1638, 466, 104, 98),
                pygame.Rect(1799, 647, 51, 83),
                pygame.Rect(1767, 703, 58, 30),
                pygame.Rect(1537, 681, 49, 55),
                pygame.Rect(1525, 664, 32, 33),
                pygame.Rect(1587, 707, 33, 35),
                pygame.Rect(1530, 697, 31, 40),
                pygame.Rect(1621, 717, 22, 21),
                pygame.Rect(292, 121, 46, 66),
                pygame.Rect(260, 136, 50, 37),
                pygame.Rect(321, 150, 33, 22),
                pygame.Rect(314, 755, 39, 64),
                pygame.Rect(295, 800, 31, 34),
                pygame.Rect(294, 772, 26, 30),
                pygame.Rect(303, 828, 38, 32),
                pygame.Rect(255, 754, 30, 39),
                pygame.Rect(132, 769, 40, 23),
                pygame.Rect(247, 781, 43, 38),
                pygame.Rect(82, 867, 45, 30),
                pygame.Rect(38, 783, 26, 29),
            ],
        "map_42":
            [
                pygame.Rect(0, -4, 1627, 4),
                pygame.Rect(1615, 0, 36, 905),
                pygame.Rect(0, 904, 1635, 15),
                pygame.Rect(-6, -4, 64, 401),
                pygame.Rect(53, 329, 34, 73),
                pygame.Rect(54, 305, 72, 39),
                pygame.Rect(-6, 590, 11, 329),
                pygame.Rect(440, 570, 87, 115),
                pygame.Rect(370, 621, 24, 57),
                pygame.Rect(416, 561, 18, 78),
                pygame.Rect(433, 561, 18, 66),
                pygame.Rect(604, 655, 21, 91),
                pygame.Rect(349, 115, 85, 38),
                pygame.Rect(338, 146, 12, 52),
                pygame.Rect(337, 233, 19, 81),
                pygame.Rect(353, 275, 24, 41),
                pygame.Rect(395, 264, 26, 43),
                pygame.Rect(411, 283, 58, 27),
                pygame.Rect(477, 118, 55, 35),
                pygame.Rect(602, 133, 20, 78),
                pygame.Rect(1043, 760, 107, 16),
                pygame.Rect(1092, 691, 12, 52),
                pygame.Rect(1061, 546, 145, 39),
                pygame.Rect(1086, 535, 33, 12),
                pygame.Rect(1245, 632, 20, 57),
                pygame.Rect(1196, 573, 9, 72),
                pygame.Rect(1139, 605, 29, 48),
                pygame.Rect(1191, 703, 14, 60),
                pygame.Rect(1018, 73, 20, 80),
                pygame.Rect(1076, 94, 14, 36),
                pygame.Rect(1094, 94, 150, 18),
                pygame.Rect(1259, 133, 28, 112),
                pygame.Rect(1523, 334, 92, 72),
                pygame.Rect(1496, 278, 34, 69),
                pygame.Rect(1478, 203, 28, 25),
                pygame.Rect(1500, 221, 13, 48),
                pygame.Rect(1507, 264, 8, 15),
            ],
        "map_43":
            [
                pygame.Rect(0, -4, 1627, 4),
                pygame.Rect(1615, 0, 36, 905),
                pygame.Rect(0, 904, 1635, 15),
                pygame.Rect(-6, -4, 64, 401),
                pygame.Rect(53, 329, 34, 73),
                pygame.Rect(54, 305, 72, 39),
                pygame.Rect(-6, 590, 11, 329),
                pygame.Rect(440, 570, 87, 115),
                pygame.Rect(370, 621, 24, 57),
                pygame.Rect(416, 561, 18, 78),
                pygame.Rect(433, 561, 18, 66),
                pygame.Rect(604, 655, 21, 91),
                pygame.Rect(349, 115, 85, 38),
                pygame.Rect(338, 146, 12, 52),
                pygame.Rect(337, 233, 19, 81),
                pygame.Rect(353, 275, 24, 41),
                pygame.Rect(395, 264, 26, 43),
                pygame.Rect(411, 283, 58, 27),
                pygame.Rect(477, 118, 55, 35),
                pygame.Rect(602, 133, 20, 78),
                pygame.Rect(1043, 760, 107, 16),
                pygame.Rect(1092, 691, 12, 52),
                pygame.Rect(1061, 546, 145, 39),
                pygame.Rect(1086, 535, 33, 12),
                pygame.Rect(1245, 632, 20, 57),
                pygame.Rect(1196, 573, 9, 72),
                pygame.Rect(1139, 605, 29, 48),
                pygame.Rect(1191, 703, 14, 60),
                pygame.Rect(1018, 73, 20, 80),
                pygame.Rect(1076, 94, 14, 36),
                pygame.Rect(1094, 94, 150, 18),
                pygame.Rect(1259, 133, 28, 112),
                pygame.Rect(1523, 334, 92, 72),
                pygame.Rect(1496, 278, 34, 69),
                pygame.Rect(1478, 203, 28, 25),
                pygame.Rect(1500, 221, 13, 48),
                pygame.Rect(1507, 264, 8, 15),
            ],
        "map_44":
            [
                pygame.Rect(0, 0, 467, 177),
                pygame.Rect(0, 175, 20, 249),
                pygame.Rect(133, 515, 47, 39),
                pygame.Rect(456, 6, 1209, 245),
                pygame.Rect(1557, 250, 104, 674),
                pygame.Rect(1273, 685, 382, 78),
                pygame.Rect(1425, 877, 227, 34),
                pygame.Rect(968, 803, 393, 102),
                pygame.Rect(0, 913, 1659, 17),
                pygame.Rect(0, 570, 23, 350),
                pygame.Rect(234, 556, 35, 222),
                pygame.Rect(230, 851, 41, 64),
                pygame.Rect(236, 275, 38, 147),
                pygame.Rect(28, 273, 51, 138),
                pygame.Rect(35, 532, 36, 155),
                pygame.Rect(908, 722, 35, 192),
                pygame.Rect(303, 795, 521, 119),
                pygame.Rect(273, 609, 38, 89),
                pygame.Rect(325, 595, 95, 70),
                pygame.Rect(447, 285, 611, 130),
                pygame.Rect(576, 565, 123, 69),
                pygame.Rect(719, 610, 20, 112),
                pygame.Rect(969, 603, 28, 106),
                pygame.Rect(869, 481, 144, 70),
                pygame.Rect(753, 532, 108, 42),
                pygame.Rect(1175, 548, 56, 74),
                pygame.Rect(1266, 259, 283, 11),
                pygame.Rect(1308, 326, 251, 278),
                pygame.Rect(16, 788, 60, 126),
                pygame.Rect(80, 857, 121, 53),
                pygame.Rect(745, 598, 20, 98),
                pygame.Rect(17, 178, 74, 79),
                pygame.Rect(293, 234, 36, 53),
                pygame.Rect(234, 165, 217, 83),
                pygame.Rect(1256, 250, 297, 29),
                pygame.Rect(139, 482, 36, 39),
                pygame.Rect(20, 404, 37, 45),
            ], }

    area_w001 = pygame.Rect(screen_x - 10, 260, 10, 190)

    tick_counter = 0

    user_class = "null_"
    user_name = "null_"
    user_body = 0
    user_str = 0
    user_def = 0
    user_agi = 0
    user_mind_resistance = 0
    user_mind_state = 0
    
    user_item_headware = ''
    user_item_bodyware = ''
    user_item_weapon = ''
    user_item_shield = ''
    user_item_accessories = ''
    
    user_status_bleeding = 0
    user_status_infection = 0
    user_status_brokenbones = 0
    user_status_stun = 0
    user_status_confusion = 0
    user_status_blindness = 0
    user_status_critical = 0
    user_status_infected = 0

    user_item_coif = 1
    user_item_bascinet = 1
    user_item_iron_helmet = 1
    user_item_cloth_hood = 1
    user_item_arming_cap = 1
    user_item_chainmail_hood = 1
    user_item_plate_helmet = 1
    user_item_iron_mask = 1
    user_item_guard_bascinet = 1
    user_item_red_scarf = 1
    user_item_leather_vest = 1
    user_item_loincloth = 1
    user_item_priests_robe = 1
    user_item_dark_priests_robe = 1
    user_item_hard_leather_armor = 1
    user_item_plated_mail = 1
    user_item_black_dress = 1
    user_item_iron_cuirass = 1
    user_item_plate_armour = 1
    user_item_trench_coat = 1
    user_item_wooden_buckler = 1
    user_item_scutum = 1
    user_item_iron_shield = 1
    user_item_short_sword = 1
    user_item_cleaver = 1
    user_item_dagger = 1
    user_item_longsword = 1
    user_item_iron_axe = 1
    user_item_mace = 1
    user_item_corsairs_saber = 1
    user_item_knife = 1
    user_item_improvised_shiv = 1
    user_item_steel_hammer = 1
    user_item_stiletto = 1
    user_item_dirk =1
    user_item_scimitar = 1
    user_item_greatsword = 1
    user_item_makeshift_spear = 1
    user_item_maul = 1
    user_item_claymore = 1
    user_item_spear = 1
    user_item_short_bow = 1
    user_item_longbow = 1
    user_item_blunderbuss = 1
    user_item_heavy_crossbow = 1
    user_item_flintlock = 1
    user_item_musket = 1
    user_item_blue_amulet = 1
    user_item_swift_boots = 1
    user_item_black_dressed_doll = 1
    user_item_red_amulet = 1
    user_item_arm_guard = 1
    user_item_ring = 1
    user_item_book_of_crafsmanship = 1
    user_item_book_of_marksmanship = 1
    user_item_book_of_trade_i = 1
    user_item_book_of_trade_ii = 1
    user_item_book_of_trade_iii = 1
    user_item_book_of_rapid_fire = 1
    user_item_book_of_agility = 1
    user_item_book_of_healing = 1
    user_item_book_of_instincts = 1
    user_item_book_of_stars = 1
    user_item_book_of_cowardice_i = 1
    user_item_book_of_cowardice_ii = 1
    user_item_book_of_pestilence_i = 1
    user_item_book_of_pestilence_ii = 1
    user_item_book_of_pestilence_iii = 1
    user_item_book_of_pestilence_iv = 1
    user_item_book_of_pestilence_v = 1
    user_item_book_of_pestilence_vi = 1
    user_item_book_of_pestilence_vii = 1
    user_item_book_of_pestilence_viii = 1
    user_item_book_of_the_secrets = 1
    user_item_book_of_enlightenment = 1
    user_item_paper = 1
    user_item_leather_scraps = 1
    user_item_iron_ingot = 1
    user_item_raw_iron = 1
    user_item_wooden_plank = 1
    user_item_blue_gem = 1
    user_item_red_gem = 1
    user_item_silver_wire = 1
    user_item_bowstring = 1
    user_item_green_herb = 1
    user_item_blue_herb = 1
    user_item_stick = 1
    user_item_empty_vial = 1
    user_item_ale = 1
    user_item_rum = 1
    user_item_wine = 1
    user_item_betadine = 1
    user_item_antibiotics = 1
    user_item_red_vial = 1
    user_item_ancient_paper = 1

    inv1 = pygame.Rect(486, 111, 83, 42)
    inv2 = pygame.Rect(469, 147, 89, 42)
    inv3 = pygame.Rect(470, 195, 86, 38)
    inv4 = pygame.Rect(472, 242, 79, 42)
    inv5 = pygame.Rect(471, 299, 81, 43)
    inv6 = pygame.Rect(471, 353, 82, 45)
    inv7 = pygame.Rect(470, 405, 86, 41)
    inv8 = pygame.Rect(470, 458, 82, 39)
    inv9 = pygame.Rect(468, 508, 85, 43)
    inv10 = pygame.Rect(467, 560, 89, 43)
    inv11 = pygame.Rect(613, 93, 89, 39)
    inv12 = pygame.Rect(614, 143, 88, 39)
    inv13 = pygame.Rect(619, 194, 80, 42)
    inv14 = pygame.Rect(616, 249, 83, 39)
    inv15 = pygame.Rect(616, 299, 83, 41)
    inv16 = pygame.Rect(617, 354, 85, 42)
    inv17 = pygame.Rect(615, 404, 85, 44)
    inv18 = pygame.Rect(614, 458, 87, 43)
    inv19 = pygame.Rect(615, 508, 89, 43)
    inv20 = pygame.Rect(618, 561, 83, 42)
    inv21 = pygame.Rect(762, 92, 88, 44)
    inv22 = pygame.Rect(763, 145, 84, 42)
    inv23 = pygame.Rect(767, 197, 79, 42)
    inv24 = pygame.Rect(765, 250, 81, 36)
    inv25 = pygame.Rect(765, 302, 85, 43)
    inv26 = pygame.Rect(763, 352, 85, 44)
    inv27 = pygame.Rect(764, 405, 84, 41)
    inv28 = pygame.Rect(764, 455, 83, 45)
    inv29 = pygame.Rect(763, 509, 84, 46)
    inv30 = pygame.Rect(763, 562, 84, 42)
    inv31 = pygame.Rect(910, 92, 86, 44)
    inv32 = pygame.Rect(910, 144, 83, 41)
    inv33 = pygame.Rect(912, 198, 82, 39)
    inv34 = pygame.Rect(911, 248, 84, 45)
    inv35 = pygame.Rect(911, 299, 82, 41)
    inv36 = pygame.Rect(911, 353, 83, 40)
    inv37 = pygame.Rect(911, 405, 83, 37)
    inv38 = pygame.Rect(912, 455, 83, 39)
    inv39 = pygame.Rect(911, 508, 90, 42)
    inv40 = pygame.Rect(911, 557, 88, 45)
    inv41 = pygame.Rect(1049, 93, 85, 46)
    inv42 = pygame.Rect(1050, 145, 82, 41)
    inv43 = pygame.Rect(1053, 195, 81, 41)
    inv44 = pygame.Rect(1050, 248, 81, 44)
    inv45 = pygame.Rect(1050, 303, 79, 39)
    inv46 = pygame.Rect(1051, 352, 80, 45)
    inv47 = pygame.Rect(1050, 400, 81, 49)
    inv48 = pygame.Rect(1049, 455, 83, 44)
    inv49 = pygame.Rect(1053, 508, 76, 44)
    inv50 = pygame.Rect(1049, 558, 83, 45)
    inv_back = pygame.Rect(472, 646, 134, 135)
    inv_next = pygame.Rect(1004, 637, 134, 135)
    world_x = 0.0
    world_y = 0.0
    p = player("mercenary", (screen_x / 2) - 36, (screen_y / 2) - 36, 6375, 3550)
    entity_walls = []
    logic_accumulator = 0.0
    main_game_loop = True
    last_time = time.time()
    state = "home"
    pre_state = None
    sys_gen_loading(1)

    if process is not None:
        try:
            process.cpu_affinity(list(range(min(13, _sys_max_cores))))
        except Exception:
            pass
    ambient("music/elucidate_calm.wav", -1)
    while main_game_loop:
        now = time.time()
        delta = now - last_time
        last_time = now
        logic_accumulator += delta
        world_x = p.x - screen_x // 2 + p.size // 2
        world_y = p.y - screen_y // 2 + p.size // 2
        if process is not None:
            try:
                if process.memory_info().rss > limit:
                    break
            except Exception:
                pass
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                elucidate_sys_exit()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        screen.fill(sys_bg_color)

        if state == "version_check":
            screen.blit(_preloaded_images["elucidate_menu_bg_011"], (0, 0))
            static_text_raw_center("The version you currently have is an outdated test version,", color=(255, 255, 255),
                                   position=(screen_x // 2, (screen_y // 2) - 40), size=40)
            static_text_raw_center("would you like to continue?", color=(255, 255, 255),
                                   position=(screen_x // 2, (screen_y // 2)), size=40)
            static_text_raw_center("Alpha 1.0.83", color=(255, 255, 255),
                                   position=(screen_x // 2, (screen_y // 2) + 60), size=20)
            static_text_raw_center("YES", color=(255, 255, 255), position=(screen_x // 2, (screen_y // 2) + 150),
                                   size=30)
            static_text_raw_center("NO", color=(255, 255, 255), position=(screen_x // 2, (screen_y // 2) + 190),
                                   size=30)
            if colide_yes.collidepoint(mouse_x, mouse_y):
                screen.blit(_scaled_images["elucidate_select_exit"], ((screen_x // 2) - 100, (screen_y // 2) + 134))
                static_text_raw_center("YES", color=(0, 0, 0), position=(screen_x // 2, (screen_y // 2) + 150), size=30)
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        state = "home"
            elif colide_no.collidepoint(mouse_x, mouse_y):
                screen.blit(_scaled_images["elucidate_select_exit"], ((screen_x // 2) - 100, (screen_y // 2) + 174))
                static_text_raw_center("NO", color=(0, 0, 0), position=(screen_x // 2, (screen_y // 2) + 190), size=30)
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        elucidate_sys_exit()

        elif state == "home":
            screen.blit(home_bg_ran, (0, 0))
            static_text_raw(text_home_001, color=(255, 255, 255), position=(5, 560), size=35)
            static_text_raw(text_home_002, color=(255, 255, 255), position=(5, 595), size=35)
            static_text_raw(text_home_003, color=(255, 255, 255), position=(5, 630), size=35)
            if colide_play.collidepoint(mouse_x, mouse_y):
                screen.blit(_scaled_images["elucidate_select_home"], (5, 561))
                static_text_raw(text_home_001, color=(0, 0, 0), position=(25, 560), size=35)
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        state = "play"
            elif colide_settings.collidepoint(mouse_x, mouse_y):
                screen.blit(_scaled_images["elucidate_select_home"], (5, 596))
                static_text_raw(text_home_002, color=(0, 0, 0), position=(25, 595), size=35)
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        state = "settings"
            elif colide_exit.collidepoint(mouse_x, mouse_y):
                screen.blit(_scaled_images["elucidate_select_home"], (5, 631))
                static_text_raw(text_home_003, color=(0, 0, 0), position=(25, 630), size=35)
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        state = "exit_confirm"

        elif state == "settings":
            screen.blit(_preloaded_images["elucidate_menu_bg_011"], (0, 0))
            static_text_raw_center(text_home_002, color=(255, 255, 255), position=(screen_x // 2, 80), size=50)
            static_text_raw_center("GRAPHICS", color=(255, 255, 255), position=(screen_x // 2, 200), size=30)
            static_text_raw_center("AUDIO", color=(255, 255, 255), position=(screen_x // 2, 235), size=30)
            static_text_raw_center("CONTROLS", color=(255, 255, 255), position=(screen_x // 2, 270), size=30)
            static_text_raw_center("CREDITS", color=(255, 255, 255), position=(screen_x // 2, 305), size=30)
            static_text_raw_center("BACK", color=(255, 255, 255), position=(screen_x // 2, 650), size=30)
            if colide_back.collidepoint(mouse_x, mouse_y):
                screen.blit(_scaled_images["elucidate_select_exit"], ((screen_x // 2) - 100, 635))
                static_text_raw_center("BACK", color=(0, 0, 0), position=(screen_x // 2, 650), size=30)
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        state = "home"
            elif colide_authors.collidepoint(mouse_x, mouse_y):
                screen.blit(_scaled_images["elucidate_select_exit"], ((screen_x // 2) - 100, 290))
                static_text_raw_center("CREDITS", color=(0, 0, 0), position=(screen_x // 2, 305), size=30)
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        p = player(user_class, (screen_x / 2) - 36, (screen_y / 2) - 36, 6375, 3550)
                        state = "settings_credits"
            elif colide_controls.collidepoint(mouse_x, mouse_y):
                screen.blit(_scaled_images["elucidate_select_exit"], ((screen_x // 2) - 100, 255))
                static_text_raw_center("CONTROLS", color=(0, 0, 0), position=(screen_x // 2, 270), size=30)
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        waiting_for_key = None
                        state = "settings_controls"
            elif colide_audio.collidepoint(mouse_x, mouse_y):
                screen.blit(_scaled_images["elucidate_select_exit"], ((screen_x // 2) - 100, 220))
                static_text_raw_center("AUDIO", color=(0, 0, 0), position=(screen_x // 2, 235), size=30)
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        dragging_slider = False
                        state = "settings_audio"
            elif colide_graphics.collidepoint(mouse_x, mouse_y):
                screen.blit(_scaled_images["elucidate_select_exit"], ((screen_x // 2) - 100, 185))
                static_text_raw_center("GRAPHICS", color=(0, 0, 0), position=(screen_x // 2, 200), size=30)
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        fps_slider_dragging = False
                        cpu_slider_dragging = False
                        ram_slider_dragging = False
                        state = "settings_graphics"

        elif state == "settings_credits":
            screen.blit(_preloaded_images["elucidate_menu_bg_011"], (0, 0))
            while logic_accumulator >= 1.0 / logic_tick:
                p.update_input()
                p.move(walls)
                p.border()
                logic_accumulator -= 1.0 / logic_tick
            p.draw(screen, world_x, world_y)
            static_text_raw_center("CREDITS", color=(255, 255, 255), position=(screen_x // 2, 80), size=50)
            static_text_raw_center("Baterbonia, Jose Gabriel", color=(255, 255, 255), position=(screen_x // 2, 200),
                                   size=30)
            static_text_raw_center("Capulong, Ivan Rafael", color=(255, 255, 255), position=(screen_x // 2, 235),
                                   size=30)
            static_text_raw_center("De Leon, Maximilian Kurt", color=(255, 255, 255), position=(screen_x // 2, 270),
                                   size=30)
            static_text_raw_center("Famero, Marc Roden", color=(255, 255, 255), position=(screen_x // 2, 305), size=30)
            static_text_raw_center("Tinoko, Gabrielle Keira", color=(255, 255, 255), position=(screen_x // 2, 340),
                                   size=30)
            static_text_raw_center("Vallite, John Alwyn", color=(255, 255, 255), position=(screen_x // 2, 375), size=30)
            static_text_raw_center("BACK", color=(255, 255, 255), position=(screen_x // 2, 650), size=30)
            if colide_back.collidepoint(mouse_x, mouse_y):
                screen.blit(_scaled_images["elucidate_select_exit"], ((screen_x // 2) - 100, 635))
                static_text_raw_center("BACK", color=(0, 0, 0), position=(screen_x // 2, 650), size=30)
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        state = "settings"

        elif state == "settings_controls":
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
                    elif colide_interact.collidepoint(event.pos):
                        waiting_for_key = "interact"
                    elif colide_inventory.collidepoint(event.pos):
                        waiting_for_key = "inventory"
                    elif colide_back.collidepoint(event.pos):
                        state = "settings"
            screen.fill(sys_bg_color)
            screen.blit(_preloaded_images["elucidate_menu_bg_011"], (0, 0))
            static_text_raw_center("CONTROLS", color=(255, 255, 255), position=(screen_x // 2, 80), size=50)
            static_text_raw_center(f"MOVE UP : {pygame.key.name(controls['move_up'])}", (255, 255, 255),
                                   (screen_x // 2, 200), 30)
            static_text_raw_center(f"MOVE DOWN : {pygame.key.name(controls['move_down'])}", (255, 255, 255),
                                   (screen_x // 2, 240), 30)
            static_text_raw_center(f"MOVE LEFT : {pygame.key.name(controls['move_left'])}", (255, 255, 255),
                                   (screen_x // 2, 280), 30)
            static_text_raw_center(f"MOVE RIGHT : {pygame.key.name(controls['move_right'])}", (255, 255, 255),
                                   (screen_x // 2, 320), 30)
            static_text_raw_center(f"ATTACK : {pygame.key.name(controls['attack'])}", (255, 255, 255),
                                   (screen_x // 2, 360), 30)
            static_text_raw_center(f"INTERACT : {pygame.key.name(controls['interact'])}", (255, 255, 255),
                                   (screen_x // 2, 400), 30)
            static_text_raw_center(f"INVENTORY : {pygame.key.name(controls['inventory'])}", (255, 255, 255),
                                   (screen_x // 2, 440), 30)
            static_text_raw_center("BACK", color=(255, 255, 255), position=(screen_x // 2, 650), size=30)
            if colide_back.collidepoint(mouse_x, mouse_y):
                screen.blit(_scaled_images["elucidate_select_exit"], ((screen_x // 2) - 100, 635))
                static_text_raw_center("BACK", color=(0, 0, 0), position=(screen_x // 2, 650), size=30)

        elif state == "settings_audio":
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if mute_rect.collidepoint(event.pos):
                        sys_audio_muted = not sys_audio_muted
                        sys_apply_audio_settings()
                    if pygame.Rect(slider_x, slider_y - 10, slider_w, 20).collidepoint(event.pos):
                        dragging_slider = True
                if event.type == pygame.MOUSEBUTTONUP:
                    dragging_slider = False
                if dragging_slider and event.type == pygame.MOUSEMOTION:
                    value = max(0.0, min(1.0, (event.pos[0] - slider_x) / slider_w))
                    sys_audio_volume = value
                    sys_apply_audio_settings()
            if dragging_slider:
                value = max(0.0, min(1.0, (mouse_x - slider_x) / slider_w))
                sys_audio_volume = value
                sys_apply_audio_settings()
            screen.blit(_preloaded_images["elucidate_menu_bg_011"], (0, 0))
            static_text_raw_center("AUDIO", color=(255, 255, 255), position=(screen_x // 2, 80), size=50)
            static_text_raw_center("BACK", color=(255, 255, 255), position=(screen_x // 2, 650), size=30)
            pygame.draw.rect(screen, ui_gray, (slider_x, slider_y, slider_w, slider_h))
            knob_x = slider_x + (sys_audio_volume * slider_w)
            pygame.draw.circle(screen, ui_crimson, (int(knob_x), slider_y + 5), knob_r)
            static_text_raw_center(f"VOLUME : {int(sys_audio_volume * 100)}%", ui_white, (screen_x // 2, 260), 30)
            pygame.draw.rect(screen, ui_crimson, mute_rect)
            if sys_audio_muted:
                static_text_raw_center("UNMUTE", ui_white, mute_rect.center, 25)
            else:
                static_text_raw_center("MUTE", ui_white, mute_rect.center, 25)
            if colide_back.collidepoint(mouse_x, mouse_y):
                screen.blit(_scaled_images["elucidate_select_exit"], ((screen_x // 2) - 100, 635))
                static_text_raw_center("BACK", color=(0, 0, 0), position=(screen_x // 2, 650), size=30)
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        state = "settings"

        elif state == "settings_graphics":
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.Rect(gfx_fps_slider_x, gfx_fps_slider_y - 10, gfx_fps_slider_w, 20).collidepoint(
                            event.pos):
                        fps_slider_dragging = True
                    if pygame.Rect(gfx_cpu_slider_x, gfx_cpu_slider_y - 10, gfx_cpu_slider_w, 20).collidepoint(
                            event.pos):
                        cpu_slider_dragging = True
                    if pygame.Rect(gfx_ram_slider_x, gfx_ram_slider_y - 10, gfx_ram_slider_w, 20).collidepoint(
                            event.pos):
                        ram_slider_dragging = True
                if event.type == pygame.MOUSEBUTTONUP:
                    fps_slider_dragging = False
                    cpu_slider_dragging = False
                    ram_slider_dragging = False
                if event.type == pygame.MOUSEMOTION:
                    if fps_slider_dragging:
                        ratio = max(0.0, min(1.0, (event.pos[0] - gfx_fps_slider_x) / gfx_fps_slider_w))
                        render_fps_index = int(round(ratio * (len(render_fps_options) - 1)))
                        render_fps = render_fps_options[render_fps_index]
                    if cpu_slider_dragging:
                        ratio = max(0.0, min(1.0, (event.pos[0] - gfx_cpu_slider_x) / gfx_cpu_slider_w))
                        cpu_core_limit = max(1, min(_sys_max_cores, int(round(ratio * (_sys_max_cores - 1))) + 1))
                        try:
                            if _HAS_PSUTIL:
                                _psutil.Process(os.getpid()).cpu_affinity(list(range(cpu_core_limit)))
                        except Exception:
                            pass
                    if ram_slider_dragging:
                        ratio = max(0.0, min(1.0, (event.pos[0] - gfx_ram_slider_x) / gfx_ram_slider_w))
                        ram_limit_gb = max(1, min(_sys_total_ram_gb, int(round(ratio * (_sys_total_ram_gb - 1))) + 1))
                        limit = ram_limit_gb * 1024 * 1024 * 1024
            if fps_slider_dragging:
                ratio = max(0.0, min(1.0, (mouse_x - gfx_fps_slider_x) / gfx_fps_slider_w))
                render_fps_index = int(round(ratio * (len(render_fps_options) - 1)))
                render_fps = render_fps_options[render_fps_index]
            if cpu_slider_dragging:
                ratio = max(0.0, min(1.0, (mouse_x - gfx_cpu_slider_x) / gfx_cpu_slider_w))
                cpu_core_limit = max(1, min(_sys_max_cores, int(round(ratio * (_sys_max_cores - 1))) + 1))
                try:
                    if _HAS_PSUTIL:
                        _psutil.Process(os.getpid()).cpu_affinity(list(range(cpu_core_limit)))
                except Exception:
                    pass
            if ram_slider_dragging:
                ratio = max(0.0, min(1.0, (mouse_x - gfx_ram_slider_x) / gfx_ram_slider_w))
                ram_limit_gb = max(1, min(_sys_total_ram_gb, int(round(ratio * (_sys_total_ram_gb - 1))) + 1))
                limit = ram_limit_gb * 1024 * 1024 * 1024
            screen.blit(_preloaded_images["elucidate_menu_bg_011"], (0, 0))
            static_text_raw_center("GRAPHICS", color=(255, 255, 255), position=(screen_x // 2, 80), size=50)
            static_text_raw_center("BACK", color=(255, 255, 255), position=(screen_x // 2, 650), size=30)
            fps_label = "UNLIMITED" if render_fps == 0 else str(render_fps)
            static_text_raw_center(f"FPS LIMIT : {fps_label}", ui_white, (screen_x // 2, 220), 30)
            pygame.draw.rect(screen, ui_gray, (gfx_fps_slider_x, gfx_fps_slider_y, gfx_fps_slider_w, slider_h))
            fps_knob_ratio = render_fps_index / (len(render_fps_options) - 1)
            fps_knob_x = int(gfx_fps_slider_x + fps_knob_ratio * gfx_fps_slider_w)
            pygame.draw.circle(screen, ui_crimson, (fps_knob_x, gfx_fps_slider_y + 5), knob_r)
            for i, opt in enumerate(render_fps_options):
                tick_x = int(gfx_fps_slider_x + (i / (len(render_fps_options) - 1)) * gfx_fps_slider_w)
                pygame.draw.rect(screen, ui_gray, (tick_x - 1, gfx_fps_slider_y - 6, 2, 6))
                tick_label = "UNL" if opt == 0 else str(opt)
                static_text_raw_center(tick_label, ui_white, (tick_x, gfx_fps_slider_y + 22), 15)
            static_text_raw_center(f"CPU CORES : {cpu_core_limit}", ui_white, (screen_x // 2, 340), 30)
            pygame.draw.rect(screen, ui_gray, (gfx_cpu_slider_x, gfx_cpu_slider_y, gfx_cpu_slider_w, slider_h))
            cpu_knob_ratio = (cpu_core_limit - 1) / max(1, (_sys_max_cores - 1))
            cpu_knob_x = int(gfx_cpu_slider_x + cpu_knob_ratio * gfx_cpu_slider_w)
            pygame.draw.circle(screen, ui_crimson, (cpu_knob_x, gfx_cpu_slider_y + 5), knob_r)
            for i in range(_sys_max_cores):
                tick_x = int(gfx_cpu_slider_x + (i / max(1, (_sys_max_cores - 1))) * gfx_cpu_slider_w)
                pygame.draw.rect(screen, ui_gray, (tick_x - 1, gfx_cpu_slider_y - 6, 2, 6))
                static_text_raw_center(str(i + 1), ui_white, (tick_x, gfx_cpu_slider_y + 22), 15)
            static_text_raw_center(f"RAM LIMIT : {ram_limit_gb} GB", ui_white, (screen_x // 2, 460), 30)
            pygame.draw.rect(screen, ui_gray, (gfx_ram_slider_x, gfx_ram_slider_y, gfx_ram_slider_w, slider_h))
            ram_knob_ratio = (ram_limit_gb - 1) / max(1, (_sys_total_ram_gb - 1))
            ram_knob_x = int(gfx_ram_slider_x + ram_knob_ratio * gfx_ram_slider_w)
            pygame.draw.circle(screen, ui_crimson, (ram_knob_x, gfx_ram_slider_y + 5), knob_r)
            for i in range(_sys_total_ram_gb):
                tick_x = int(gfx_ram_slider_x + (i / max(1, (_sys_total_ram_gb - 1))) * gfx_ram_slider_w)
                pygame.draw.rect(screen, ui_gray, (tick_x - 1, gfx_ram_slider_y - 6, 2, 6))
                static_text_raw_center(f"{i + 1}G", ui_white, (tick_x, gfx_ram_slider_y + 22), 15)
            if colide_back.collidepoint(mouse_x, mouse_y):
                screen.blit(_scaled_images["elucidate_select_exit"], ((screen_x // 2) - 100, 635))
                static_text_raw_center("BACK", color=(0, 0, 0), position=(screen_x // 2, 650), size=30)
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        state = "settings"

        elif state == "exit_confirm":
            screen.blit(_preloaded_images["elucidate_menu_bg_011"], (0, 0))
            static_text_raw_center("ARE YOU SURE YOU WANT TO EXIT THE GAME?", color=(255, 255, 255),
                                   position=(screen_x // 2, (screen_y // 2) - 40), size=40)
            static_text_raw_center("YES", color=(255, 255, 255), position=(screen_x // 2, (screen_y // 2) + 150),
                                   size=30)
            static_text_raw_center("NO", color=(255, 255, 255), position=(screen_x // 2, (screen_y // 2) + 190),
                                   size=30)
            if colide_yes.collidepoint(mouse_x, mouse_y):
                screen.blit(_scaled_images["elucidate_select_exit"], ((screen_x // 2) - 100, (screen_y // 2) + 134))
                static_text_raw_center("YES", color=(0, 0, 0), position=(screen_x // 2, (screen_y // 2) + 150), size=30)
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        elucidate_sys_exit()
            elif colide_no.collidepoint(mouse_x, mouse_y):
                screen.blit(_scaled_images["elucidate_select_exit"], ((screen_x // 2) - 100, (screen_y // 2) + 174))
                static_text_raw_center("NO", color=(0, 0, 0), position=(screen_x // 2, (screen_y // 2) + 190), size=30)
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        state = "home"

        elif state == "play":
            screen.blit(_preloaded_images["elucidate_menu_bg_010"], (0, 0))
            static_text_raw("NEW GAME", color=(255, 255, 255), position=(5, 200), size=35)
            static_text_raw("MORE", color=(255, 255, 255), position=(5, 235), size=35)
            static_text_raw("BACK", color=(255, 255, 255), position=(5, 270), size=35)
            if elucidate_main_run_home_play_newgame.collidepoint(mouse_x, mouse_y):
                screen.blit(_scaled_images["elucidate_select_home"], (5, 202))
                static_text_raw("NEW GAME", color=(0, 0, 0), position=(5, 200), size=35)
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        state = "play_select"
            if elucidate_main_run_home_play_more.collidepoint(mouse_x, mouse_y):
                screen.blit(_scaled_images["elucidate_select_home"], (5, 237))
                static_text_raw("MORE", color=(0, 0, 0), position=(5, 235), size=35)
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        sys_gen_update_error()
            if elucidate_main_run_home_play_back.collidepoint(mouse_x, mouse_y):
                screen.blit(_scaled_images["elucidate_select_home"], (5, 272))
                static_text_raw("BACK", color=(0, 0, 0), position=(5, 270), size=35)
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        state = "home"
        elif state == "play_select":
            screen.blit(_preloaded_images["elucidate_dlc_user_selection_bg_001"], (0, 0))
            if elucidate_main_run_home_play_back_select.collidepoint(mouse_x, mouse_y):
                screen.blit(_scaled_images["elucidate_select_exit"], ((screen_x // 2) - 100, 655))
                static_text_raw_center("BACK", color=(0, 0, 0), position=(screen_x // 2, 670), size=30)
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        state = "play"
            if dlc == True:
                if select_mercenary.collidepoint(mouse_x, mouse_y):
                    screen.blit(_preloaded_images["elucidate_dlc_user_selection_bg_001"], (0, 0))
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            user_body = 100
                            user_str = 30
                            user_def = 0
                            user_agi = 12
                            user_mind_resistance = 2
                            user_mind_state = 20
                            user_add_speed = 7
                            user_class = "mercenary"
                            user_name = "Lucidus"
                            state = "play_select_1"
                elif select_cultist.collidepoint(mouse_x, mouse_y):
                    screen.blit(_preloaded_images["elucidate_dlc_user_selection_bg_003"], (0, 0))
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            user_body = 100
                            user_str = 18
                            user_def = 0
                            user_agi = 8
                            user_mind_resistance = 3
                            user_mind_state = 10
                            user_add_speed = 6
                            user_class = "cultist"
                            user_name = "Funeris"
                            state = "play_select_1"
                elif select_priest.collidepoint(mouse_x, mouse_y):
                    screen.blit(_preloaded_images["elucidate_dlc_user_selection_bg_004"], (0, 0))
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            user_body = 100
                            user_str = 40
                            user_def = 10
                            user_agi = 8
                            user_mind_resistance = 1
                            user_mind_state = 0
                            user_add_speed = 6
                            user_class = "priest"
                            user_name = "Father Calum"
                            state = "play_select_1"
                elif select_shaman.collidepoint(mouse_x, mouse_y):
                    screen.blit(_preloaded_images["elucidate_dlc_user_selection_bg_005"], (0, 0))
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            user_body = 80
                            user_str = 15
                            user_def = 0
                            user_agi = 8
                            user_mind_resistance = 2
                            user_mind_state = 20
                            user_add_speed = 5
                            user_class = "shaman"
                            user_name = "Pluvia"
                            state = "play_select_1"
                elif select_merchant.collidepoint(mouse_x, mouse_y):
                    screen.blit(_preloaded_images["elucidate_dlc_user_selection_bg_006"], (0, 0))
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            user_body = 70
                            user_str = 10
                            user_def = 0
                            user_agi = 10
                            user_mind_resistance = 3
                            user_mind_state = 30
                            user_add_speed = 5
                            user_class = "merchant"
                            user_name = "Konrad"
                            state = "play_select_1"
            else:
                select_mercenary = pygame.Rect(356, 110, 258, 477)
                select_cultist = pygame.Rect(624, 110, 258, 477)
                if select_mercenary.collidepoint(mouse_x, mouse_y):
                    screen.blit(_preloaded_images["elucidate_user_selection_bg_002"], (0, 0))
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            user_body = 100
                            user_str = 30
                            user_def = 0
                            user_agi = 12
                            user_mind_resistance = 2
                            user_mind_state = 20
                            user_class = "mercenary"
                            user_name = "Lucidus"
                            state = "play_select_1"
                elif select_cultist.collidepoint(mouse_x, mouse_y):
                    screen.blit(_preloaded_images["elucidate_user_selection_bg_003"], (0, 0))
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            user_body = 100
                            user_str = 18
                            user_def = 0
                            user_agi = 8
                            user_mind_resistance = 3
                            user_mind_state = 10
                            user_class = "cultist"
                            user_name = "Funeris"
                            state = "play_select_1"
                else:
                    screen.blit(_preloaded_images["elucidate_user_selection_bg_001"], (0, 0))
            static_text_raw_center("BACK", color=(255, 255, 255), position=(screen_x // 2, 670), size=30)
            static_text_raw_center("SELECT CHARACTER", color=(255, 255, 255), position=(screen_x // 2, 80), size=40)

        elif state == "play_select_1":
            if user_class == "mercenary":
                screen.blit(_preloaded_images["elucidate_user_selected_play_001"], (0, 0))
            elif user_class == "cultist":
                screen.blit(_preloaded_images["elucidate_user_selected_play_002"], (0, 0))
            elif user_class == "priest":
                screen.blit(_preloaded_images["elucidate_dlc_user_selected_play_001"], (0, 0))
            elif user_class == "shaman":
                screen.blit(_preloaded_images["elucidate_dlc_user_selected_play_002"], (0, 0))
            elif user_class == "merchant":
                screen.blit(_preloaded_images["elucidate_dlc_user_selected_play_003"], (0, 0))
            else:
                state = "play_select"
            static_text_raw("BACK", color=(255, 255, 255), position=(680, 670), size=30)
            static_text_raw("OK", color=(255, 255, 255), position=(680, 630), size=30)
            if back_playselect_col.collidepoint(mouse_x, mouse_y):
                screen.blit(_scaled_images["elucidate_select_home_1"], (680, 671))
                static_text_raw("BACK", color=(0, 0, 0), position=(700, 670), size=30)
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        state = "play_select"
            elif ok_playselect_col.collidepoint(mouse_x, mouse_y):
                screen.blit(_scaled_images["elucidate_select_home_1"], (680, 631))
                static_text_raw("OK", color=(0, 0, 0), position=(700, 630), size=30)
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        p = player(user_class, (screen_x / 2) - 36, (screen_y / 2) - 36, 1275, 710)
                        world_x = p.x - screen_x // 2 + p.size // 2
                        world_y = p.y - screen_y // 2 + p.size // 2
                        state = "play_intro_001"

        elif state == "play_intro_001":
            if user_class == "mercenary":
                static_text_raw_center("Before there was a soldier", color=(255, 255, 255),
                                       position=(screen_x // 2, 100), size=20)
                static_text_raw_center("there was a child.", color=(255, 255, 255), position=(screen_x // 2, 120),
                                       size=20)
                static_text_raw_center("A child with no name the world remembered,", color=(255, 255, 255),
                                       position=(screen_x // 2, 140), size=20)
                static_text_raw_center("taken from an orphanage at approximately nine years of age,",
                                       color=(255, 255, 255), position=(screen_x // 2, 160), size=20)
                static_text_raw_center("loaded into a Church carriage that smelled of incense and iron,",
                                       color=(255, 255, 255), position=(screen_x // 2, 180), size=20)
                static_text_raw_center("and driven toward a facility beneath the Theocratic Capital where the",
                                       color=(255, 255, 255), position=(screen_x // 2, 200), size=20)
                static_text_raw_center("Church of Lumen conducted its most classified operations.",
                                       color=(255, 255, 255), position=(screen_x // 2, 220), size=20)
                static_text_raw_center("He was not told where he was going. He was told he was special.",
                                       color=(255, 255, 255), position=(screen_x // 2, 240), size=20)
                static_text_raw_center("He believed it...", color=(255, 255, 255), position=(screen_x // 2, 260),
                                       size=20)
                static_text_raw_center("Because he was nine years old and had no one.", color=(255, 255, 255),
                                       position=(screen_x // 2, 280), size=20)
                static_text_raw_center("And being chosen felt better than being nothing.", color=(255, 255, 255),
                                       position=(screen_x // 2, 300), size=20)
            elif user_class == "cultist":
                static_text_raw_center("The Church took her away from the orphanage.", color=(255, 255, 255),
                                       position=(screen_x // 2, 100), size=20)
                static_text_raw_center("The promise that she was special...", color=(255, 255, 255),
                                       position=(screen_x // 2, 120), size=20)
                static_text_raw_center("She was only seven when it  happened.", color=(255, 255, 255),
                                       position=(screen_x // 2, 140), size=20)
                static_text_raw_center("She was enrolled in the Vindication Lumen program", color=(255, 255, 255),
                                       position=(screen_x // 2, 160), size=20)
                static_text_raw_center("alongside the child who would become Ignis,", color=(255, 255, 255),
                                       position=(screen_x // 2, 180), size=20)
                static_text_raw_center("alongside the child who would become Father Calum a generation earlier,",
                                       color=(255, 255, 255), position=(screen_x // 2, 200), size=20)
                static_text_raw_center("alongside the others whose names the program assigned and the world forgot.",
                                       color=(255, 255, 255), position=(screen_x // 2, 220), size=20)
                static_text_raw_center("The procedure worked differently in her.", color=(255, 255, 255),
                                       position=(screen_x // 2, 240), size=20)
                static_text_raw_center("She could feel the horrors,", color=(255, 255, 255),
                                       position=(screen_x // 2, 260), size=20)
                static_text_raw_center("and see them in the shadows.", color=(255, 255, 255),
                                       position=(screen_x // 2, 280), size=20)
                static_text_raw_center("", color=(255, 255, 255), position=(screen_x // 2, 300), size=20)
            elif user_class == "priest":
                static_text_raw_center("He was told he was special.", color=(255, 255, 255),
                                       position=(screen_x // 2, 100), size=20)
                static_text_raw_center("He believed it, because he was nine and he needed to.", color=(255, 255, 255),
                                       position=(screen_x // 2, 120), size=20)
                static_text_raw_center("He survived what the others did not.", color=(255, 255, 255),
                                       position=(screen_x // 2, 140), size=20)
                static_text_raw_center("The Church called his survival proof of the program.", color=(255, 255, 255),
                                       position=(screen_x // 2, 160), size=20)
                static_text_raw_center("They promoted him,", color=(255, 255, 255), position=(screen_x // 2, 180),
                                       size=20)
                static_text_raw_center("And he began to tell the next group of children...", color=(255, 255, 255),
                                       position=(screen_x // 2, 200), size=20)
                static_text_raw_center("That they were special, too...", color=(255, 255, 255),
                                       position=(screen_x // 2, 220), size=20)
                static_text_raw_center("", color=(255, 255, 255), position=(screen_x // 2, 240), size=20)
                static_text_raw_center("", color=(255, 255, 255), position=(screen_x // 2, 260), size=20)
                static_text_raw_center("", color=(255, 255, 255), position=(screen_x // 2, 280), size=20)
                static_text_raw_center("", color=(255, 255, 255), position=(screen_x // 2, 300), size=20)
            elif user_class == "shaman":
                static_text_raw_center("Pluvia traces to the same orphanage as the others,", color=(255, 255, 255),
                                       position=(screen_x // 2, 100), size=20)
                static_text_raw_center("Though her connection to it is different in nature.", color=(255, 255, 255),
                                       position=(screen_x // 2, 120), size=20)
                static_text_raw_center("Where Ignis was taken into the program,", color=(255, 255, 255),
                                       position=(screen_x // 2, 140), size=20)
                static_text_raw_center("And Funeris was expelled from it,", color=(255, 255, 255),
                                       position=(screen_x // 2, 160), size=20)
                static_text_raw_center("Pluvia’s sensitivity developed differently.", color=(255, 255, 255),
                                       position=(screen_x // 2, 180), size=20)
                static_text_raw_center("It was not a mechanical enhancement,", color=(255, 255, 255),
                                       position=(screen_x // 2, 200), size=20)
                static_text_raw_center("But a gift the Church classified as Foresight.", color=(255, 255, 255),
                                       position=(screen_x // 2, 220), size=20)
                static_text_raw_center("The program could not contain her.", color=(255, 255, 255),
                                       position=(screen_x // 2, 240), size=20)
                static_text_raw_center("She found her way to the Tribe", color=(255, 255, 255),
                                       position=(screen_x // 2, 260), size=20)
                static_text_raw_center("Where her power was a responsibility, not a weapon.", color=(255, 255, 255),
                                       position=(screen_x // 2, 280), size=20)
                static_text_raw_center("She stayed for thirty years...", color=(255, 255, 255),
                                       position=(screen_x // 2, 300), size=20)
            elif user_class == "merchant":
                static_text_raw_center("Konrad investigates the Church’s procurement,", color=(255, 255, 255),
                                       position=(screen_x // 2, 100), size=20)
                static_text_raw_center("A study of how corruption hides in plain language.", color=(255, 255, 255),
                                       position=(screen_x // 2, 120), size=20)
                static_text_raw_center("He reviews documents of ''subject acquisition''", color=(255, 255, 255),
                                       position=(screen_x // 2, 140), size=20)
                static_text_raw_center("Handled through ''charitable partnerships.''", color=(255, 255, 255),
                                       position=(screen_x // 2, 160), size=20)
                static_text_raw_center("He finds children described in the language of logistics.",
                                       color=(255, 255, 255), position=(screen_x // 2, 180), size=20)
                static_text_raw_center("In the Merchant Guild Hall, the cost of reading is high.",
                                       color=(255, 255, 255), position=(screen_x // 2, 200), size=20)
                static_text_raw_center("The administrative framing of atrocity is the true horror,",
                                       color=(255, 255, 255), position=(screen_x // 2, 220), size=20)
                static_text_raw_center("Because someone sat down,", color=(255, 255, 255),
                                       position=(screen_x // 2, 240), size=20)
                static_text_raw_center("And chose those words deliberately.", color=(255, 255, 255),
                                       position=(screen_x // 2, 260), size=20)
                static_text_raw_center("", color=(255, 255, 255), position=(screen_x // 2, 280), size=20)
                static_text_raw_center("", color=(255, 255, 255), position=(screen_x // 2, 300), size=20)
            static_text_raw_center("[ click anywhere to continue ]", color=(255, 255, 255),
                                   position=(screen_x // 2, 695), size=15)
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    npcs = []
                    entity_walls = []
                    p = player(user_class, (screen_x / 2) - 36, (screen_y / 2) - 36, 6375, 3550)
                    world_x = p.x - screen_x // 2 + p.size // 2
                    world_y = p.y - screen_y // 2 + p.size // 2
                    if user_class == "mercenary":
                        state = "map_01"
                    elif user_class == "cultist":
                        state = "map_39"
                    elif user_class == "priest":
                        state = "map_2"
                    elif user_class == "shaman":
                        state = "map_25"
                    elif user_class == "merchant":
                        state = "map_33"


        elif state == "map_01":

            screen.blit(_scaled_images["l_i_inside_the_wall"], (-world_x, -world_y))

            walls = area_walls["map_01"].copy()

            # entity_walls = get_entity_walls(npcs, p)

            while logic_accumulator >= 1.0 / logic_tick:
                p.update_input()

                p.move(walls + entity_walls)

                p.border()

                logic_accumulator -= 1.0 / logic_tick

            world_x = p.x - screen_x // 2 + p.size // 2

            world_y = p.y - screen_y // 2 + p.size // 2

            p.draw(screen, world_x, world_y)
            exit = pygame.Rect(447, 541, 122, 16)
            if p.get_rect().colliderect(exit):
                p.x = 921
                p.y = 590
                state = "map_02"
            keys = pygame.key.get_pressed()
            if keys[controls["interact"]]:

                interact_box = p.interact_rect()

                interact_box_draw = pygame.Rect(

                    interact_box.x - world_x,

                    interact_box.y - world_y,

                    interact_box.w,

                    interact_box.h,

                )

                if interact_box.colliderect(interact_rect):
                    pre_state = state

                    state = "interact_test_npc1"

            if keys[controls["inventory"]]:
                pre_state = state

                state = "inventory"

            rect = p.get_rect()

            pygame.draw.rect(screen, (0, 255, 0), (rect.x - world_x, rect.y - world_y, rect.width, rect.height), 1)

        elif state == "map_02":

            screen.blit(_scaled_images["l_o_outer_gate_district"], (-world_x, -world_y))

            walls = area_walls["map_02"].copy()

            # entity_walls = get_entity_walls(npcs, p)

            while logic_accumulator >= 1.0 / logic_tick:
                p.update_input()

                p.move(walls + entity_walls)

                p.border()

                logic_accumulator -= 1.0 / logic_tick

            world_x = p.x - screen_x // 2 + p.size // 2

            world_y = p.y - screen_y // 2 + p.size // 2

            p.draw(screen, world_x, world_y)

            draft_officer_interact_rect = pygame.Rect(2121, 530, 40, 40)
            pygame.draw.rect(screen, (0, 255, 0), (draft_officer_interact_rect), 1)
            screen.blit(_scaled_images["elucidate_idle_draft_officer_npc_left"],
                        ((draft_officer_interact_rect.x - 18) - world_x,
                         (draft_officer_interact_rect.y - 36) - world_y))
            keys = pygame.key.get_pressed()
            p.draw(screen, world_x, world_y)
            exit = pygame.Rect(905, 513, 86, 20)
            if p.get_rect().colliderect(exit):
                p.x = 475
                p.y = 464
                state = "map_01"
            if keys[controls["interact"]]:

                interact_box = p.interact_rect()

                interact_box_draw = pygame.Rect(

                    interact_box.x - world_x,

                    interact_box.y - world_y,

                    interact_box.w,

                    interact_box.h,

                )

                pygame.draw.rect(screen, (255, 255, 0), interact_box_draw)

                if interact_box.colliderect(interact_rect):
                    pre_state = state

                    state = "interact_test_npc1"

            if keys[controls["inventory"]]:
                pre_state = state

                state = "inventory"

            rect = p.get_rect()

            pygame.draw.rect(screen, (0, 255, 0), (rect.x - world_x, rect.y - world_y, rect.width, rect.height), 1)

        elif state == "map_03":

            screen.blit(_scaled_images["l_o_inner_military_district"], (-world_x, -world_y))

            walls = area_walls["map_03"].copy()

            # entity_walls = get_entity_walls(npcs, p)

            while logic_accumulator >= 1.0 / logic_tick:
                p.update_input()

                p.move(walls + entity_walls)

                p.border()

                logic_accumulator -= 1.0 / logic_tick

            world_x = p.x - screen_x // 2 + p.size // 2

            world_y = p.y - screen_y // 2 + p.size // 2

            p.draw(screen, world_x, world_y)

            keys = pygame.key.get_pressed()

            if keys[controls["interact"]]:

                interact_box = p.interact_rect()

                interact_box_draw = pygame.Rect(

                    interact_box.x - world_x,

                    interact_box.y - world_y,

                    interact_box.w,

                    interact_box.h,

                )

                pygame.draw.rect(screen, (255, 255, 0), interact_box_draw)

                if interact_box.colliderect(interact_rect):
                    pre_state = state

                    state = "interact_test_npc1"

            if keys[controls["inventory"]]:
                pre_state = state

                state = "inventory"

            rect = p.get_rect()

            pygame.draw.rect(screen, (0, 255, 0), (rect.x - world_x, rect.y - world_y, rect.width, rect.height), 1)

        elif state == "map_04":

            screen.blit(_scaled_images["l_i_barracks_hall"], (-world_x, -world_y))

            walls = area_walls["map_04"].copy()

            # entity_walls = get_entity_walls(npcs, p)

            while logic_accumulator >= 1.0 / logic_tick:
                p.update_input()

                p.move(walls + entity_walls)

                p.border()

                logic_accumulator -= 1.0 / logic_tick

            world_x = p.x - screen_x // 2 + p.size // 2

            world_y = p.y - screen_y // 2 + p.size // 2

            p.draw(screen, world_x, world_y)

            keys = pygame.key.get_pressed()

            if keys[controls["interact"]]:

                interact_box = p.interact_rect()

                interact_box_draw = pygame.Rect(

                    interact_box.x - world_x,

                    interact_box.y - world_y,

                    interact_box.w,

                    interact_box.h,

                )

                pygame.draw.rect(screen, (255, 255, 0), interact_box_draw)

                if interact_box.colliderect(interact_rect):
                    pre_state = state

                    state = "interact_test_npc1"

            if keys[controls["inventory"]]:
                pre_state = state

                state = "inventory"

            rect = p.get_rect()

            pygame.draw.rect(screen, (0, 255, 0), (rect.x - world_x, rect.y - world_y, rect.width, rect.height), 1)

        elif state == "map_05":

            screen.blit(_scaled_images["l_o_church_outpost"], (-world_x, -world_y))

            walls = area_walls["map_05"].copy()

            # entity_walls = get_entity_walls(npcs, p)

            while logic_accumulator >= 1.0 / logic_tick:
                p.update_input()

                p.move(walls + entity_walls)

                p.border()

                logic_accumulator -= 1.0 / logic_tick

            world_x = p.x - screen_x // 2 + p.size // 2

            world_y = p.y - screen_y // 2 + p.size // 2

            p.draw(screen, world_x, world_y)

            keys = pygame.key.get_pressed()

            if keys[controls["interact"]]:

                interact_box = p.interact_rect()

                interact_box_draw = pygame.Rect(

                    interact_box.x - world_x,

                    interact_box.y - world_y,

                    interact_box.w,

                    interact_box.h,

                )

                pygame.draw.rect(screen, (255, 255, 0), interact_box_draw)

                if interact_box.colliderect(interact_rect):
                    pre_state = state

                    state = "interact_test_npc1"

            if keys[controls["inventory"]]:
                pre_state = state

                state = "inventory"

            rect = p.get_rect()

            pygame.draw.rect(screen, (0, 255, 0), (rect.x - world_x, rect.y - world_y, rect.width, rect.height), 1)

        elif state == "map_06":

            screen.blit(_scaled_images["l_i_church_chapel"], (-world_x, -world_y))

            walls = area_walls["map_06"].copy()

            # entity_walls = get_entity_walls(npcs, p)

            while logic_accumulator >= 1.0 / logic_tick:
                p.update_input()

                p.move(walls + entity_walls)

                p.border()

                logic_accumulator -= 1.0 / logic_tick

            world_x = p.x - screen_x // 2 + p.size // 2

            world_y = p.y - screen_y // 2 + p.size // 2

            p.draw(screen, world_x, world_y)

            keys = pygame.key.get_pressed()

            if keys[controls["interact"]]:

                interact_box = p.interact_rect()

                interact_box_draw = pygame.Rect(

                    interact_box.x - world_x,

                    interact_box.y - world_y,

                    interact_box.w,

                    interact_box.h,

                )

                pygame.draw.rect(screen, (255, 255, 0), interact_box_draw)

                if interact_box.colliderect(interact_rect):
                    pre_state = state

                    state = "interact_test_npc1"

            if keys[controls["inventory"]]:
                pre_state = state

                state = "inventory"

            rect = p.get_rect()

            pygame.draw.rect(screen, (0, 255, 0), (rect.x - world_x, rect.y - world_y, rect.width, rect.height), 1)

        elif state == "map_07":

            screen.blit(_scaled_images["l_o_cathedral_plaza"], (-world_x, -world_y))

            walls = area_walls["map_07"].copy()

            # entity_walls = get_entity_walls(npcs, p)

            while logic_accumulator >= 1.0 / logic_tick:
                p.update_input()

                p.move(walls + entity_walls)

                p.border()

                logic_accumulator -= 1.0 / logic_tick

            world_x = p.x - screen_x // 2 + p.size // 2

            world_y = p.y - screen_y // 2 + p.size // 2

            p.draw(screen, world_x, world_y)

            keys = pygame.key.get_pressed()

            if keys[controls["interact"]]:

                interact_box = p.interact_rect()

                interact_box_draw = pygame.Rect(

                    interact_box.x - world_x,

                    interact_box.y - world_y,

                    interact_box.w,

                    interact_box.h,

                )

                pygame.draw.rect(screen, (255, 255, 0), interact_box_draw)

                if interact_box.colliderect(interact_rect):
                    pre_state = state

                    state = "interact_test_npc1"

            if keys[controls["inventory"]]:
                pre_state = state

                state = "inventory"

            rect = p.get_rect()

            pygame.draw.rect(screen, (0, 255, 0), (rect.x - world_x, rect.y - world_y, rect.width, rect.height), 1)

        elif state == "map_08":

            screen.blit(_scaled_images["l_i_church_administrative_wing"], (-world_x, -world_y))

            walls = area_walls["map_08"].copy()

            # entity_walls = get_entity_walls(npcs, p)

            while logic_accumulator >= 1.0 / logic_tick:
                p.update_input()

                p.move(walls + entity_walls)

                p.border()

                logic_accumulator -= 1.0 / logic_tick

            world_x = p.x - screen_x // 2 + p.size // 2

            world_y = p.y - screen_y // 2 + p.size // 2

            p.draw(screen, world_x, world_y)

            keys = pygame.key.get_pressed()

            if keys[controls["interact"]]:

                interact_box = p.interact_rect()

                interact_box_draw = pygame.Rect(

                    interact_box.x - world_x,

                    interact_box.y - world_y,

                    interact_box.w,

                    interact_box.h,

                )

                pygame.draw.rect(screen, (255, 255, 0), interact_box_draw)

                if interact_box.colliderect(interact_rect):
                    pre_state = state

                    state = "interact_test_npc1"

            if keys[controls["inventory"]]:
                pre_state = state

                state = "inventory"

            rect = p.get_rect()

            pygame.draw.rect(screen, (0, 255, 0), (rect.x - world_x, rect.y - world_y, rect.width, rect.height), 1)

        elif state == "map_09":

            screen.blit(_scaled_images["l_i_main_cathedral"], (-world_x, -world_y))

            walls = area_walls["map_09"].copy()

            # entity_walls = get_entity_walls(npcs, p)

            while logic_accumulator >= 1.0 / logic_tick:
                p.update_input()

                p.move(walls + entity_walls)

                p.border()

                logic_accumulator -= 1.0 / logic_tick

            world_x = p.x - screen_x // 2 + p.size // 2

            world_y = p.y - screen_y // 2 + p.size // 2

            p.draw(screen, world_x, world_y)

            keys = pygame.key.get_pressed()

            if keys[controls["interact"]]:

                interact_box = p.interact_rect()

                interact_box_draw = pygame.Rect(

                    interact_box.x - world_x,

                    interact_box.y - world_y,

                    interact_box.w,

                    interact_box.h,

                )

                pygame.draw.rect(screen, (255, 255, 0), interact_box_draw)

                if interact_box.colliderect(interact_rect):
                    pre_state = state

                    state = "interact_test_npc1"

            if keys[controls["inventory"]]:
                pre_state = state

                state = "inventory"

            rect = p.get_rect()

            pygame.draw.rect(screen, (0, 255, 0), (rect.x - world_x, rect.y - world_y, rect.width, rect.height), 1)

        elif state == "map_10":

            screen.blit(_scaled_images["l_o_inner_military_district"], (-world_x, -world_y))

            walls = area_walls["map_10"].copy()

            # entity_walls = get_entity_walls(npcs, p)

            while logic_accumulator >= 1.0 / logic_tick:
                p.update_input()

                p.move(walls + entity_walls)

                p.border()

                logic_accumulator -= 1.0 / logic_tick

            world_x = p.x - screen_x // 2 + p.size // 2

            world_y = p.y - screen_y // 2 + p.size // 2

            p.draw(screen, world_x, world_y)

            keys = pygame.key.get_pressed()

            if keys[controls["interact"]]:

                interact_box = p.interact_rect()

                interact_box_draw = pygame.Rect(

                    interact_box.x - world_x,

                    interact_box.y - world_y,

                    interact_box.w,

                    interact_box.h,

                )

                pygame.draw.rect(screen, (255, 255, 0), interact_box_draw)

                if interact_box.colliderect(interact_rect):
                    pre_state = state

                    state = "interact_test_npc1"

            if keys[controls["inventory"]]:
                pre_state = state

                state = "inventory"

            rect = p.get_rect()

            pygame.draw.rect(screen, (0, 255, 0), (rect.x - world_x, rect.y - world_y, rect.width, rect.height), 1)

        elif state == "map_11":

            screen.blit(_scaled_images["l_o_home_village_entry"], (-world_x, -world_y))

            walls = area_walls["map_11"].copy()

            # entity_walls = get_entity_walls(npcs, p)

            while logic_accumulator >= 1.0 / logic_tick:
                p.update_input()

                p.move(walls + entity_walls)

                p.border()

                logic_accumulator -= 1.0 / logic_tick

            world_x = p.x - screen_x // 2 + p.size // 2

            world_y = p.y - screen_y // 2 + p.size // 2

            p.draw(screen, world_x, world_y)

            keys = pygame.key.get_pressed()

            if keys[controls["interact"]]:

                interact_box = p.interact_rect()

                interact_box_draw = pygame.Rect(

                    interact_box.x - world_x,

                    interact_box.y - world_y,

                    interact_box.w,

                    interact_box.h,

                )

                pygame.draw.rect(screen, (255, 255, 0), interact_box_draw)

                if interact_box.colliderect(interact_rect):
                    pre_state = state

                    state = "interact_test_npc1"

            if keys[controls["inventory"]]:
                pre_state = state

                state = "inventory"

            rect = p.get_rect()

            pygame.draw.rect(screen, (0, 255, 0), (rect.x - world_x, rect.y - world_y, rect.width, rect.height), 1)

        elif state == "map_12":

            screen.blit(_scaled_images["l_i_chief_home"], (-world_x, -world_y))

            walls = area_walls["map_12"].copy()

            # entity_walls = get_entity_walls(npcs, p)

            while logic_accumulator >= 1.0 / logic_tick:
                p.update_input()

                p.move(walls + entity_walls)

                p.border()

                logic_accumulator -= 1.0 / logic_tick

            world_x = p.x - screen_x // 2 + p.size // 2

            world_y = p.y - screen_y // 2 + p.size // 2

            p.draw(screen, world_x, world_y)

            keys = pygame.key.get_pressed()

            if keys[controls["interact"]]:

                interact_box = p.interact_rect()

                interact_box_draw = pygame.Rect(

                    interact_box.x - world_x,

                    interact_box.y - world_y,

                    interact_box.w,

                    interact_box.h,

                )

                pygame.draw.rect(screen, (255, 255, 0), interact_box_draw)

                if interact_box.colliderect(interact_rect):
                    pre_state = state

                    state = "interact_test_npc1"

            if keys[controls["inventory"]]:
                pre_state = state

                state = "inventory"

            rect = p.get_rect()

            pygame.draw.rect(screen, (0, 255, 0), (rect.x - world_x, rect.y - world_y, rect.width, rect.height), 1)

        elif state == "map_13":

            screen.blit(_scaled_images["l_i_headmaster_office"], (-world_x, -world_y))

            walls = area_walls["map_13"].copy()

            # entity_walls = get_entity_walls(npcs, p)

            while logic_accumulator >= 1.0 / logic_tick:
                p.update_input()

                p.move(walls + entity_walls)

                p.border()

                logic_accumulator -= 1.0 / logic_tick

            world_x = p.x - screen_x // 2 + p.size // 2

            world_y = p.y - screen_y // 2 + p.size // 2

            p.draw(screen, world_x, world_y)

            keys = pygame.key.get_pressed()

            if keys[controls["interact"]]:

                interact_box = p.interact_rect()

                interact_box_draw = pygame.Rect(

                    interact_box.x - world_x,

                    interact_box.y - world_y,

                    interact_box.w,

                    interact_box.h,

                )

                pygame.draw.rect(screen, (255, 255, 0), interact_box_draw)

                if interact_box.colliderect(interact_rect):
                    pre_state = state

                    state = "interact_test_npc1"

            if keys[controls["inventory"]]:
                pre_state = state

                state = "inventory"

            rect = p.get_rect()

            pygame.draw.rect(screen, (0, 255, 0), (rect.x - world_x, rect.y - world_y, rect.width, rect.height), 1)

        elif state == "map_14":

            screen.blit(_scaled_images["l_o_home_village_center"], (-world_x, -world_y))

            walls = area_walls["map_14"].copy()

            # entity_walls = get_entity_walls(npcs, p)

            while logic_accumulator >= 1.0 / logic_tick:
                p.update_input()

                p.move(walls + entity_walls)

                p.border()

                logic_accumulator -= 1.0 / logic_tick

            world_x = p.x - screen_x // 2 + p.size // 2

            world_y = p.y - screen_y // 2 + p.size // 2

            p.draw(screen, world_x, world_y)

            keys = pygame.key.get_pressed()

            if keys[controls["interact"]]:

                interact_box = p.interact_rect()

                interact_box_draw = pygame.Rect(

                    interact_box.x - world_x,

                    interact_box.y - world_y,

                    interact_box.w,

                    interact_box.h,

                )

                pygame.draw.rect(screen, (255, 255, 0), interact_box_draw)

                if interact_box.colliderect(interact_rect):
                    pre_state = state

                    state = "interact_test_npc1"

            if keys[controls["inventory"]]:
                pre_state = state

                state = "inventory"

            rect = p.get_rect()

            pygame.draw.rect(screen, (0, 255, 0), (rect.x - world_x, rect.y - world_y, rect.width, rect.height), 1)

        elif state == "map_15":

            screen.blit(_scaled_images["l_o_the_old_orphanage"], (-world_x, -world_y))

            walls = area_walls["map_15"].copy()

            # entity_walls = get_entity_walls(npcs, p)

            while logic_accumulator >= 1.0 / logic_tick:
                p.update_input()

                p.move(walls + entity_walls)

                p.border()

                logic_accumulator -= 1.0 / logic_tick

            world_x = p.x - screen_x // 2 + p.size // 2

            world_y = p.y - screen_y // 2 + p.size // 2

            p.draw(screen, world_x, world_y)

            keys = pygame.key.get_pressed()

            if keys[controls["interact"]]:

                interact_box = p.interact_rect()

                interact_box_draw = pygame.Rect(

                    interact_box.x - world_x,

                    interact_box.y - world_y,

                    interact_box.w,

                    interact_box.h,

                )

                pygame.draw.rect(screen, (255, 255, 0), interact_box_draw)

                if interact_box.colliderect(interact_rect):
                    pre_state = state

                    state = "interact_test_npc1"

            if keys[controls["inventory"]]:
                pre_state = state

                state = "inventory"

            rect = p.get_rect()

            pygame.draw.rect(screen, (0, 255, 0), (rect.x - world_x, rect.y - world_y, rect.width, rect.height), 1)

        elif state == "map_16":

            screen.blit(_scaled_images["l_i_the_play_room"], (-world_x, -world_y))

            walls = area_walls["map_16"].copy()

            # entity_walls = get_entity_walls(npcs, p)

            while logic_accumulator >= 1.0 / logic_tick:
                p.update_input()

                p.move(walls + entity_walls)

                p.border()

                logic_accumulator -= 1.0 / logic_tick

            world_x = p.x - screen_x // 2 + p.size // 2

            world_y = p.y - screen_y // 2 + p.size // 2

            p.draw(screen, world_x, world_y)

            keys = pygame.key.get_pressed()

            if keys[controls["interact"]]:

                interact_box = p.interact_rect()

                interact_box_draw = pygame.Rect(

                    interact_box.x - world_x,

                    interact_box.y - world_y,

                    interact_box.w,

                    interact_box.h,

                )

                pygame.draw.rect(screen, (255, 255, 0), interact_box_draw)

                if interact_box.colliderect(interact_rect):
                    pre_state = state

                    state = "interact_test_npc1"

            if keys[controls["inventory"]]:
                pre_state = state

                state = "inventory"

            rect = p.get_rect()

            pygame.draw.rect(screen, (0, 255, 0), (rect.x - world_x, rect.y - world_y, rect.width, rect.height), 1)

        elif state == "map_17":

            screen.blit(_scaled_images["f_o_village_market"], (-world_x, -world_y))

            walls = area_walls["map_17"].copy()

            # entity_walls = get_entity_walls(npcs, p)

            while logic_accumulator >= 1.0 / logic_tick:
                p.update_input()

                p.move(walls + entity_walls)

                p.border()

                logic_accumulator -= 1.0 / logic_tick

            world_x = p.x - screen_x // 2 + p.size // 2

            world_y = p.y - screen_y // 2 + p.size // 2

            p.draw(screen, world_x, world_y)

            keys = pygame.key.get_pressed()

            if keys[controls["interact"]]:

                interact_box = p.interact_rect()

                interact_box_draw = pygame.Rect(

                    interact_box.x - world_x,

                    interact_box.y - world_y,

                    interact_box.w,

                    interact_box.h,

                )

                pygame.draw.rect(screen, (255, 255, 0), interact_box_draw)

                if interact_box.colliderect(interact_rect):
                    pre_state = state

                    state = "interact_test_npc1"

            if keys[controls["inventory"]]:
                pre_state = state

                state = "inventory"

            rect = p.get_rect()

            pygame.draw.rect(screen, (0, 255, 0), (rect.x - world_x, rect.y - world_y, rect.width, rect.height), 1)

        elif state == "map_18":

            screen.blit(_scaled_images["f_o_deep_terror_zone"], (-world_x, -world_y))

            walls = area_walls["map_18"].copy()

            # entity_walls = get_entity_walls(npcs, p)

            while logic_accumulator >= 1.0 / logic_tick:
                p.update_input()

                p.move(walls + entity_walls)

                p.border()

                logic_accumulator -= 1.0 / logic_tick

            world_x = p.x - screen_x // 2 + p.size // 2

            world_y = p.y - screen_y // 2 + p.size // 2

            p.draw(screen, world_x, world_y)

            keys = pygame.key.get_pressed()

            if keys[controls["interact"]]:

                interact_box = p.interact_rect()

                interact_box_draw = pygame.Rect(

                    interact_box.x - world_x,

                    interact_box.y - world_y,

                    interact_box.w,

                    interact_box.h,

                )

                pygame.draw.rect(screen, (255, 255, 0), interact_box_draw)

                if interact_box.colliderect(interact_rect):
                    pre_state = state

                    state = "interact_test_npc1"

            if keys[controls["inventory"]]:
                pre_state = state

                state = "inventory"

            rect = p.get_rect()

            pygame.draw.rect(screen, (0, 255, 0), (rect.x - world_x, rect.y - world_y, rect.width, rect.height), 1)

        elif state == "map_19":

            screen.blit(_scaled_images["t_o_anomaly_forest"], (-world_x, -world_y))

            walls = area_walls["map_19"].copy()

            # entity_walls = get_entity_walls(npcs, p)

            while logic_accumulator >= 1.0 / logic_tick:
                p.update_input()

                p.move(walls + entity_walls)

                p.border()

                logic_accumulator -= 1.0 / logic_tick

            world_x = p.x - screen_x // 2 + p.size // 2

            world_y = p.y - screen_y // 2 + p.size // 2

            p.draw(screen, world_x, world_y)

            keys = pygame.key.get_pressed()

            if keys[controls["interact"]]:

                interact_box = p.interact_rect()

                interact_box_draw = pygame.Rect(

                    interact_box.x - world_x,

                    interact_box.y - world_y,

                    interact_box.w,

                    interact_box.h,

                )

                pygame.draw.rect(screen, (255, 255, 0), interact_box_draw)

                if interact_box.colliderect(interact_rect):
                    pre_state = state

                    state = "interact_test_npc1"

            if keys[controls["inventory"]]:
                pre_state = state

                state = "inventory"

            rect = p.get_rect()

            pygame.draw.rect(screen, (0, 255, 0), (rect.x - world_x, rect.y - world_y, rect.width, rect.height), 1)

        elif state == "map_20":

            screen.blit(_scaled_images["f_o_outside_chief_home"], (-world_x, -world_y))

            walls = area_walls["map_20"].copy()

            # entity_walls = get_entity_walls(npcs, p)

            while logic_accumulator >= 1.0 / logic_tick:
                p.update_input()

                p.move(walls + entity_walls)

                p.border()

                logic_accumulator -= 1.0 / logic_tick

            world_x = p.x - screen_x // 2 + p.size // 2

            world_y = p.y - screen_y // 2 + p.size // 2

            p.draw(screen, world_x, world_y)

            keys = pygame.key.get_pressed()

            if keys[controls["interact"]]:

                interact_box = p.interact_rect()

                interact_box_draw = pygame.Rect(

                    interact_box.x - world_x,

                    interact_box.y - world_y,

                    interact_box.w,

                    interact_box.h,

                )

                pygame.draw.rect(screen, (255, 255, 0), interact_box_draw)

                if interact_box.colliderect(interact_rect):
                    pre_state = state

                    state = "interact_test_npc1"

            if keys[controls["inventory"]]:
                pre_state = state

                state = "inventory"

            rect = p.get_rect()

            pygame.draw.rect(screen, (0, 255, 0), (rect.x - world_x, rect.y - world_y, rect.width, rect.height), 1)

        elif state == "map_21":

            screen.blit(_scaled_images["f_i_inside_chief_home"], (-world_x, -world_y))

            walls = area_walls["map_21"].copy()

            # entity_walls = get_entity_walls(npcs, p)

            while logic_accumulator >= 1.0 / logic_tick:
                p.update_input()

                p.move(walls + entity_walls)

                p.border()

                logic_accumulator -= 1.0 / logic_tick

            world_x = p.x - screen_x // 2 + p.size // 2

            world_y = p.y - screen_y // 2 + p.size // 2

            p.draw(screen, world_x, world_y)

            keys = pygame.key.get_pressed()

            if keys[controls["interact"]]:

                interact_box = p.interact_rect()

                interact_box_draw = pygame.Rect(

                    interact_box.x - world_x,

                    interact_box.y - world_y,

                    interact_box.w,

                    interact_box.h,

                )

                pygame.draw.rect(screen, (255, 255, 0), interact_box_draw)

                if interact_box.colliderect(interact_rect):
                    pre_state = state

                    state = "interact_test_npc1"

            if keys[controls["inventory"]]:
                pre_state = state

                state = "inventory"

            rect = p.get_rect()

            pygame.draw.rect(screen, (0, 255, 0), (rect.x - world_x, rect.y - world_y, rect.width, rect.height), 1)

        elif state == "map_22":

            screen.blit(_scaled_images["f_i_tunnel_passage_to_tribe"], (-world_x, -world_y))

            walls = area_walls["l_i_merchant_tavern"].copy()

            entity_walls = get_entity_walls(npcs, p)

            while logic_accumulator >= 1.0 / logic_tick:
                p.update_input()

                p.move(walls + entity_walls)

                p.border()

                logic_accumulator -= 1.0 / logic_tick

            world_x = p.x - screen_x // 2 + p.size // 2

            world_y = p.y - screen_y // 2 + p.size // 2

            p.draw(screen, world_x, world_y)

            keys = pygame.key.get_pressed()

            if keys[controls["interact"]]:

                interact_box = p.interact_rect()

                interact_box_draw = pygame.Rect(

                    interact_box.x - world_x,

                    interact_box.y - world_y,

                    interact_box.w,

                    interact_box.h,

                )

                pygame.draw.rect(screen, (255, 255, 0), interact_box_draw)

                if interact_box.colliderect(interact_rect):
                    pre_state = state

                    state = "interact_test_npc1"

            if keys[controls["inventory"]]:
                pre_state = state

                state = "inventory"

            rect = p.get_rect()

            pygame.draw.rect(screen, (0, 255, 0), (rect.x - world_x, rect.y - world_y, rect.width, rect.height), 1)

        elif state == "map_23":

            screen.blit(_scaled_images["t_o_tribe_perimeter"], (-world_x, -world_y))

            walls = area_walls["l_i_merchant_tavern"].copy()

            entity_walls = get_entity_walls(npcs, p)

            while logic_accumulator >= 1.0 / logic_tick:
                p.update_input()

                p.move(walls + entity_walls)

                p.border()

                logic_accumulator -= 1.0 / logic_tick

            world_x = p.x - screen_x // 2 + p.size // 2

            world_y = p.y - screen_y // 2 + p.size // 2

            p.draw(screen, world_x, world_y)

            keys = pygame.key.get_pressed()

            if keys[controls["interact"]]:

                interact_box = p.interact_rect()

                interact_box_draw = pygame.Rect(

                    interact_box.x - world_x,

                    interact_box.y - world_y,

                    interact_box.w,

                    interact_box.h,

                )

                pygame.draw.rect(screen, (255, 255, 0), interact_box_draw)

                if interact_box.colliderect(interact_rect):
                    pre_state = state

                    state = "interact_test_npc1"

            if keys[controls["inventory"]]:
                pre_state = state

                state = "inventory"

            rect = p.get_rect()

            pygame.draw.rect(screen, (0, 255, 0), (rect.x - world_x, rect.y - world_y, rect.width, rect.height), 1)

        elif state == "map_24":

            screen.blit(_scaled_images["t_o_tribe_settlement"], (-world_x, -world_y))

            walls = area_walls["map_24"].copy()

            # entity_walls = get_entity_walls(npcs, p)

            while logic_accumulator >= 1.0 / logic_tick:
                p.update_input()

                p.move(walls + entity_walls)

                p.border()

                logic_accumulator -= 1.0 / logic_tick

            world_x = p.x - screen_x // 2 + p.size // 2

            world_y = p.y - screen_y // 2 + p.size // 2

            p.draw(screen, world_x, world_y)

            keys = pygame.key.get_pressed()

            if keys[controls["interact"]]:

                interact_box = p.interact_rect()

                interact_box_draw = pygame.Rect(

                    interact_box.x - world_x,

                    interact_box.y - world_y,

                    interact_box.w,

                    interact_box.h,

                )

                pygame.draw.rect(screen, (255, 255, 0), interact_box_draw)

                if interact_box.colliderect(interact_rect):
                    pre_state = state

                    state = "interact_test_npc1"

            if keys[controls["inventory"]]:
                pre_state = state

                state = "inventory"

            rect = p.get_rect()

            pygame.draw.rect(screen, (0, 255, 0), (rect.x - world_x, rect.y - world_y, rect.width, rect.height), 1)

        elif state == "map_25":

            screen.blit(_scaled_images["t_i_healing_hut"], (-world_x, -world_y))

            walls = area_walls["map_25"].copy()

            # entity_walls = get_entity_walls(npcs, p)

            while logic_accumulator >= 1.0 / logic_tick:
                p.update_input()

                p.move(walls + entity_walls)

                p.border()

                logic_accumulator -= 1.0 / logic_tick

            world_x = p.x - screen_x // 2 + p.size // 2

            world_y = p.y - screen_y // 2 + p.size // 2

            p.draw(screen, world_x, world_y)

            keys = pygame.key.get_pressed()

            if keys[controls["interact"]]:

                interact_box = p.interact_rect()

                interact_box_draw = pygame.Rect(

                    interact_box.x - world_x,

                    interact_box.y - world_y,

                    interact_box.w,

                    interact_box.h,

                )

                pygame.draw.rect(screen, (255, 255, 0), interact_box_draw)

                if interact_box.colliderect(interact_rect):
                    pre_state = state

                    state = "interact_test_npc1"

            if keys[controls["inventory"]]:
                pre_state = state

                state = "inventory"

            rect = p.get_rect()

            pygame.draw.rect(screen, (0, 255, 0), (rect.x - world_x, rect.y - world_y, rect.width, rect.height), 1)

        elif state == "map_26":

            screen.blit(_scaled_images["t_i_storage_cave"], (-world_x, -world_y))

            walls = area_walls["map_26"].copy()

            # entity_walls = get_entity_walls(npcs, p)

            while logic_accumulator >= 1.0 / logic_tick:
                p.update_input()

                p.move(walls + entity_walls)

                p.border()

                logic_accumulator -= 1.0 / logic_tick

            world_x = p.x - screen_x // 2 + p.size // 2

            world_y = p.y - screen_y // 2 + p.size // 2

            p.draw(screen, world_x, world_y)

            keys = pygame.key.get_pressed()

            if keys[controls["interact"]]:

                interact_box = p.interact_rect()

                interact_box_draw = pygame.Rect(

                    interact_box.x - world_x,

                    interact_box.y - world_y,

                    interact_box.w,

                    interact_box.h,

                )

                pygame.draw.rect(screen, (255, 255, 0), interact_box_draw)

                if interact_box.colliderect(interact_rect):
                    pre_state = state

                    state = "interact_test_npc1"

            if keys[controls["inventory"]]:
                pre_state = state

                state = "inventory"

            rect = p.get_rect()

            pygame.draw.rect(screen, (0, 255, 0), (rect.x - world_x, rect.y - world_y, rect.width, rect.height), 1)

        elif state == "map_27":

            screen.blit(_scaled_images["t_i_escape_route"], (-world_x, -world_y))

            walls = area_walls["map_27"].copy()

            # entity_walls = get_entity_walls(npcs, p)

            while logic_accumulator >= 1.0 / logic_tick:
                p.update_input()

                p.move(walls + entity_walls)

                p.border()

                logic_accumulator -= 1.0 / logic_tick

            world_x = p.x - screen_x // 2 + p.size // 2

            world_y = p.y - screen_y // 2 + p.size // 2

            p.draw(screen, world_x, world_y)

            keys = pygame.key.get_pressed()

            if keys[controls["interact"]]:

                interact_box = p.interact_rect()

                interact_box_draw = pygame.Rect(

                    interact_box.x - world_x,

                    interact_box.y - world_y,

                    interact_box.w,

                    interact_box.h,

                )

                pygame.draw.rect(screen, (255, 255, 0), interact_box_draw)

                if interact_box.colliderect(interact_rect):
                    pre_state = state

                    state = "interact_test_npc1"

            if keys[controls["inventory"]]:
                pre_state = state

                state = "inventory"

            rect = p.get_rect()

            pygame.draw.rect(screen, (0, 255, 0), (rect.x - world_x, rect.y - world_y, rect.width, rect.height), 1)

        elif state == "map_28":

            screen.blit(_scaled_images["l_o_corrupted_frontier"], (-world_x, -world_y))

            walls = area_walls["map_28"].copy()

            # entity_walls = get_entity_walls(npcs, p)

            while logic_accumulator >= 1.0 / logic_tick:
                p.update_input()

                p.move(walls + entity_walls)

                p.border()

                logic_accumulator -= 1.0 / logic_tick

            world_x = p.x - screen_x // 2 + p.size // 2

            world_y = p.y - screen_y // 2 + p.size // 2

            p.draw(screen, world_x, world_y)

            keys = pygame.key.get_pressed()

            if keys[controls["interact"]]:

                interact_box = p.interact_rect()

                interact_box_draw = pygame.Rect(

                    interact_box.x - world_x,

                    interact_box.y - world_y,

                    interact_box.w,

                    interact_box.h,

                )

                pygame.draw.rect(screen, (255, 255, 0), interact_box_draw)

                if interact_box.colliderect(interact_rect):
                    pre_state = state

                    state = "interact_test_npc1"

            if keys[controls["inventory"]]:
                pre_state = state

                state = "inventory"

            rect = p.get_rect()

            pygame.draw.rect(screen, (0, 255, 0), (rect.x - world_x, rect.y - world_y, rect.width, rect.height), 1)

        elif state == "map_29":

            screen.blit(_scaled_images["l_o_harbor_district"], (-world_x, -world_y))

            walls = area_walls["map_29"].copy()

            # entity_walls = get_entity_walls(npcs, p)

            while logic_accumulator >= 1.0 / logic_tick:
                p.update_input()

                p.move(walls + entity_walls)

                p.border()

                logic_accumulator -= 1.0 / logic_tick

            world_x = p.x - screen_x // 2 + p.size // 2

            world_y = p.y - screen_y // 2 + p.size // 2

            p.draw(screen, world_x, world_y)

            keys = pygame.key.get_pressed()

            if keys[controls["interact"]]:

                interact_box = p.interact_rect()

                interact_box_draw = pygame.Rect(

                    interact_box.x - world_x,

                    interact_box.y - world_y,

                    interact_box.w,

                    interact_box.h,

                )

                pygame.draw.rect(screen, (255, 255, 0), interact_box_draw)

                if interact_box.colliderect(interact_rect):
                    pre_state = state

                    state = "interact_test_npc1"

            if keys[controls["inventory"]]:
                pre_state = state

                state = "inventory"

            rect = p.get_rect()

            pygame.draw.rect(screen, (0, 255, 0), (rect.x - world_x, rect.y - world_y, rect.width, rect.height), 1)

        elif state == "map_30":

            screen.blit(_scaled_images["l_i_customs_office"], (-world_x, -world_y))

            walls = area_walls["map_30"].copy()

            # entity_walls = get_entity_walls(npcs, p)

            while logic_accumulator >= 1.0 / logic_tick:
                p.update_input()

                p.move(walls + entity_walls)

                p.border()

                logic_accumulator -= 1.0 / logic_tick

            world_x = p.x - screen_x // 2 + p.size // 2

            world_y = p.y - screen_y // 2 + p.size // 2

            p.draw(screen, world_x, world_y)

            keys = pygame.key.get_pressed()

            if keys[controls["interact"]]:

                interact_box = p.interact_rect()

                interact_box_draw = pygame.Rect(

                    interact_box.x - world_x,

                    interact_box.y - world_y,

                    interact_box.w,

                    interact_box.h,

                )

                pygame.draw.rect(screen, (255, 255, 0), interact_box_draw)

                if interact_box.colliderect(interact_rect):
                    pre_state = state

                    state = "interact_test_npc1"

            if keys[controls["inventory"]]:
                pre_state = state

                state = "inventory"

            rect = p.get_rect()

            pygame.draw.rect(screen, (0, 255, 0), (rect.x - world_x, rect.y - world_y, rect.width, rect.height), 1)

        elif state == "map_31":

            screen.blit(_scaled_images["l_i_clearance_office"], (-world_x, -world_y))

            walls = area_walls["map_31"].copy()

            # entity_walls = get_entity_walls(npcs, p)

            while logic_accumulator >= 1.0 / logic_tick:
                p.update_input()

                p.move(walls + entity_walls)

                p.border()

                logic_accumulator -= 1.0 / logic_tick

            world_x = p.x - screen_x // 2 + p.size // 2

            world_y = p.y - screen_y // 2 + p.size // 2

            p.draw(screen, world_x, world_y)

            keys = pygame.key.get_pressed()

            if keys[controls["interact"]]:

                interact_box = p.interact_rect()

                interact_box_draw = pygame.Rect(

                    interact_box.x - world_x,

                    interact_box.y - world_y,

                    interact_box.w,

                    interact_box.h,

                )

                pygame.draw.rect(screen, (255, 255, 0), interact_box_draw)

                if interact_box.colliderect(interact_rect):
                    pre_state = state

                    state = "interact_test_npc1"

            if keys[controls["inventory"]]:
                pre_state = state

                state = "inventory"

            rect = p.get_rect()

            pygame.draw.rect(screen, (0, 255, 0), (rect.x - world_x, rect.y - world_y, rect.width, rect.height), 1)

        elif state == "map_32":

            screen.blit(_scaled_images["l_o_merchant_quarter"], (-world_x, -world_y))

            walls = area_walls["map_32"].copy()

            # entity_walls = get_entity_walls(npcs, p)

            while logic_accumulator >= 1.0 / logic_tick:
                p.update_input()

                p.move(walls + entity_walls)

                p.border()

                logic_accumulator -= 1.0 / logic_tick

            world_x = p.x - screen_x // 2 + p.size // 2

            world_y = p.y - screen_y // 2 + p.size // 2

            p.draw(screen, world_x, world_y)

            keys = pygame.key.get_pressed()

            if keys[controls["interact"]]:

                interact_box = p.interact_rect()

                interact_box_draw = pygame.Rect(

                    interact_box.x - world_x,

                    interact_box.y - world_y,

                    interact_box.w,

                    interact_box.h,

                )

                pygame.draw.rect(screen, (255, 255, 0), interact_box_draw)

                if interact_box.colliderect(interact_rect):
                    pre_state = state

                    state = "interact_test_npc1"

            if keys[controls["inventory"]]:
                pre_state = state

                state = "inventory"

            rect = p.get_rect()

            pygame.draw.rect(screen, (0, 255, 0), (rect.x - world_x, rect.y - world_y, rect.width, rect.height), 1)

        elif state == "map_33":

            screen.blit(_scaled_images["l_i_merchant_guild_hall"], (-world_x, -world_y))

            walls = area_walls["map_33"].copy()

            # entity_walls = get_entity_walls(npcs, p)

            while logic_accumulator >= 1.0 / logic_tick:
                p.update_input()

                p.move(walls + entity_walls)

                p.border()

                logic_accumulator -= 1.0 / logic_tick

            world_x = p.x - screen_x // 2 + p.size // 2

            world_y = p.y - screen_y // 2 + p.size // 2

            p.draw(screen, world_x, world_y)

            keys = pygame.key.get_pressed()

            if keys[controls["interact"]]:

                interact_box = p.interact_rect()

                interact_box_draw = pygame.Rect(

                    interact_box.x - world_x,

                    interact_box.y - world_y,

                    interact_box.w,

                    interact_box.h,

                )

                pygame.draw.rect(screen, (255, 255, 0), interact_box_draw)

                if interact_box.colliderect(interact_rect):
                    pre_state = state

                    state = "interact_test_npc1"

            if keys[controls["inventory"]]:
                pre_state = state

                state = "inventory"

            rect = p.get_rect()

            pygame.draw.rect(screen, (0, 255, 0), (rect.x - world_x, rect.y - world_y, rect.width, rect.height), 1)

        elif state == "map_34":

            screen.blit(_scaled_images["l_i_merchant_tavern"], (-world_x, -world_y))

            walls = area_walls["map_34"].copy()

            # entity_walls = get_entity_walls(npcs, p)

            while logic_accumulator >= 1.0 / logic_tick:
                p.update_input()

                p.move(walls + entity_walls)

                p.border()

                logic_accumulator -= 1.0 / logic_tick

            world_x = p.x - screen_x // 2 + p.size // 2

            world_y = p.y - screen_y // 2 + p.size // 2

            p.draw(screen, world_x, world_y)

            keys = pygame.key.get_pressed()

            if keys[controls["interact"]]:

                interact_box = p.interact_rect()

                interact_box_draw = pygame.Rect(

                    interact_box.x - world_x,

                    interact_box.y - world_y,

                    interact_box.w,

                    interact_box.h,

                )

                pygame.draw.rect(screen, (255, 255, 0), interact_box_draw)

                if interact_box.colliderect(interact_rect):
                    pre_state = state

                    state = "interact_test_npc1"

            if keys[controls["inventory"]]:
                pre_state = state

                state = "inventory"

            rect = p.get_rect()

            pygame.draw.rect(screen, (0, 255, 0), (rect.x - world_x, rect.y - world_y, rect.width, rect.height), 1)

        elif state == "map_35":

            screen.blit(_scaled_images["l_i_the_ship"], (-world_x, -world_y))

            walls = area_walls["l_i_merchant_tavern"].copy()

            entity_walls = get_entity_walls(npcs, p)

            while logic_accumulator >= 1.0 / logic_tick:
                p.update_input()

                p.move(walls + entity_walls)

                p.border()

                logic_accumulator -= 1.0 / logic_tick

            world_x = p.x - screen_x // 2 + p.size // 2

            world_y = p.y - screen_y // 2 + p.size // 2

            p.draw(screen, world_x, world_y)

            keys = pygame.key.get_pressed()

            if keys[controls["interact"]]:

                interact_box = p.interact_rect()

                interact_box_draw = pygame.Rect(

                    interact_box.x - world_x,

                    interact_box.y - world_y,

                    interact_box.w,

                    interact_box.h,

                )

                pygame.draw.rect(screen, (255, 255, 0), interact_box_draw)

                if interact_box.colliderect(interact_rect):
                    pre_state = state

                    state = "interact_test_npc1"

            if keys[controls["inventory"]]:
                pre_state = state

                state = "inventory"

            rect = p.get_rect()

            pygame.draw.rect(screen, (0, 255, 0), (rect.x - world_x, rect.y - world_y, rect.width, rect.height), 1)

        elif state == "map_36":

            screen.blit(_scaled_images["l_i_ship_lower_part"], (-world_x, -world_y))

            walls = area_walls["map_36"].copy()

            # entity_walls = get_entity_walls(npcs, p)

            while logic_accumulator >= 1.0 / logic_tick:
                p.update_input()

                p.move(walls + entity_walls)

                p.border()

                logic_accumulator -= 1.0 / logic_tick

            world_x = p.x - screen_x // 2 + p.size // 2

            world_y = p.y - screen_y // 2 + p.size // 2

            p.draw(screen, world_x, world_y)

            keys = pygame.key.get_pressed()

            if keys[controls["interact"]]:

                interact_box = p.interact_rect()

                interact_box_draw = pygame.Rect(

                    interact_box.x - world_x,

                    interact_box.y - world_y,

                    interact_box.w,

                    interact_box.h,

                )

                pygame.draw.rect(screen, (255, 255, 0), interact_box_draw)

                if interact_box.colliderect(interact_rect):
                    pre_state = state

                    state = "interact_test_npc1"

            if keys[controls["inventory"]]:
                pre_state = state
                state = "inventory"
            rect = p.get_rect()
            pygame.draw.rect(screen, (0, 255, 0), (rect.x - world_x, rect.y - world_y, rect.width, rect.height), 1)
        elif state == "map_37":
            screen.blit(_scaled_images["c_o_coastal_landing"], (-world_x, -world_y))
            walls = area_walls["map_37"].copy()
            # entity_walls = get_entity_walls(npcs, p)
            while logic_accumulator >= 1.0 / logic_tick:
                p.update_input()
                p.move(walls + entity_walls)
                p.border()
                logic_accumulator -= 1.0 / logic_tick
            world_x = p.x - screen_x // 2 + p.size // 2
            world_y = p.y - screen_y // 2 + p.size // 2
            p.draw(screen, world_x, world_y)
            keys = pygame.key.get_pressed()
            if keys[controls["interact"]]:
                interact_box = p.interact_rect()
                interact_box_draw = pygame.Rect(interact_box.x - world_x, interact_box.y - world_y, interact_box.w,
                                                interact_box.h)
                pygame.draw.rect(screen, (255, 255, 0), interact_box_draw)
                if interact_box.colliderect(interact_rect):
                    pre_state = state
                    state = "interact_test_npc1"
            if keys[controls["inventory"]]:
                pre_state = state
                state = "inventory"
            rect = p.get_rect()
            pygame.draw.rect(screen, (0, 255, 0), (rect.x - world_x, rect.y - world_y, rect.width, rect.height), 1)
        elif state == "map_38":
            screen.blit(_scaled_images["c_o_cult_village"], (-world_x, -world_y))
            walls = area_walls["map_38"].copy()
            # entity_walls = get_entity_walls(npcs, p)
            while logic_accumulator >= 1.0 / logic_tick:
                p.update_input()
                p.move(walls + entity_walls)
                p.border()
                logic_accumulator -= 1.0 / logic_tick
            world_x = p.x - screen_x // 2 + p.size // 2
            world_y = p.y - screen_y // 2 + p.size // 2
            p.draw(screen, world_x, world_y)
            keys = pygame.key.get_pressed()
            if keys[controls["interact"]]:
                interact_box = p.interact_rect()
                interact_box_draw = pygame.Rect(interact_box.x - world_x, interact_box.y - world_y, interact_box.w,
                                                interact_box.h)
                pygame.draw.rect(screen, (255, 255, 0), interact_box_draw)
                if interact_box.colliderect(interact_rect):
                    pre_state = state
                    state = "interact_test_npc1"
            if keys[controls["inventory"]]:
                pre_state = state
                state = "inventory"
            rect = p.get_rect()
            pygame.draw.rect(screen, (0, 255, 0), (rect.x - world_x, rect.y - world_y, rect.width, rect.height), 1)
        elif state == "map_39":
            screen.blit(_scaled_images["c_o_cult_funeris_encounter"], (-world_x, -world_y))
            walls = area_walls["map_39"].copy()
            # entity_walls = get_entity_walls(npcs, p)
            while logic_accumulator >= 1.0 / logic_tick:
                p.update_input()
                p.move(walls + entity_walls)
                p.border()
                logic_accumulator -= 1.0 / logic_tick
            world_x = p.x - screen_x // 2 + p.size // 2
            world_y = p.y - screen_y // 2 + p.size // 2
            p.draw(screen, world_x, world_y)

            cult_leader_interact_rect1 = pygame.Rect(940, 390, 40, 40)
            cult_leader_interact_rect = pygame.Rect((cult_leader_interact_rect1.x - 18) - world_x,
                                                    (cult_leader_interact_rect1.y - 36) - world_y, 40, 40)
            pygame.draw.rect(screen, (0, 255, 0), (cult_leader_interact_rect), 1)
            screen.blit(_scaled_images["elucidate_idle_cult_leader_npc_left"],
                        (cult_leader_interact_rect1.x - world_x,
                         cult_leader_interact_rect1.x - world_y))
            if cult_leader_interact_rect.colliderect(interact_rect):
                pre_state = state

                state = "interact_cult_leader1"
            keys = pygame.key.get_pressed()
            if keys[controls["interact"]]:
                interact_box = p.interact_rect()
                interact_box_draw = pygame.Rect(interact_box.x - world_x, interact_box.y - world_y, interact_box.w,
                                                interact_box.h)
                pygame.draw.rect(screen, (255, 255, 0), interact_box_draw)
                if interact_box.colliderect(interact_rect):
                    pre_state = state
                    state = "interact_test_npc1"
            if keys[controls["inventory"]]:
                pre_state = state
                state = "inventory"
            rect = p.get_rect()
            pygame.draw.rect(screen, (0, 255, 0), (rect.x - world_x, rect.y - world_y, rect.width, rect.height), 1)
        elif state == "map_40":
            screen.blit(_scaled_images["c_i_inner_sanctum"], (-world_x, -world_y))
            walls = area_walls["map_40"].copy()
            # entity_walls = get_entity_walls(npcs, p)
            while logic_accumulator >= 1.0 / logic_tick:
                p.update_input()
                p.move(walls + entity_walls)
                p.border()
                logic_accumulator -= 1.0 / logic_tick
            world_x = p.x - screen_x // 2 + p.size // 2
            world_y = p.y - screen_y // 2 + p.size // 2
            p.draw(screen, world_x, world_y)
            keys = pygame.key.get_pressed()
            if keys[controls["interact"]]:
                interact_box = p.interact_rect()
                interact_box_draw = pygame.Rect(interact_box.x - world_x, interact_box.y - world_y, interact_box.w,
                                                interact_box.h)
                pygame.draw.rect(screen, (255, 255, 0), interact_box_draw)
                if interact_box.colliderect(interact_rect):
                    pre_state = state
                    state = "interact_test_npc1"
            if keys[controls["inventory"]]:
                pre_state = state
                state = "inventory"
            rect = p.get_rect()
            pygame.draw.rect(screen, (0, 255, 0), (rect.x - world_x, rect.y - world_y, rect.width, rect.height), 1)
        elif state == "map_41":
            screen.blit(_scaled_images["c_i_cult_leader_fortress"], (-world_x, -world_y))
            walls = area_walls["map_41"].copy()
            # entity_walls = get_entity_walls(npcs, p)
            while logic_accumulator >= 1.0 / logic_tick:
                p.update_input()
                p.move(walls + entity_walls)
                p.border()
                logic_accumulator -= 1.0 / logic_tick
            world_x = p.x - screen_x // 2 + p.size // 2
            world_y = p.y - screen_y // 2 + p.size // 2
            p.draw(screen, world_x, world_y)
            keys = pygame.key.get_pressed()
            if keys[controls["interact"]]:
                interact_box = p.interact_rect()
                interact_box_draw = pygame.Rect(interact_box.x - world_x, interact_box.y - world_y, interact_box.w,
                                                interact_box.h, )
                pygame.draw.rect(screen, (255, 255, 0), interact_box_draw)
                if interact_box.colliderect(interact_rect):
                    pre_state = state
                    state = "interact_test_npc1"
            if keys[controls["inventory"]]:
                pre_state = state
                state = "inventory"
            rect = p.get_rect()
            pygame.draw.rect(screen, (0, 255, 0), (rect.x - world_x, rect.y - world_y, rect.width, rect.height), 1)
        elif state == "map_42":
            screen.blit(_scaled_images["c_o_cultist_battleground"], (-world_x, -world_y))
            walls = area_walls["map_42"].copy()
            # entity_walls = get_entity_walls(npcs, p)
            while logic_accumulator >= 1.0 / logic_tick:
                p.update_input()
                p.move(walls + entity_walls)
                p.border()
                logic_accumulator -= 1.0 / logic_tick
            world_x = p.x - screen_x // 2 + p.size // 2
            world_y = p.y - screen_y // 2 + p.size // 2
            p.draw(screen, world_x, world_y)
            keys = pygame.key.get_pressed()
            if keys[controls["interact"]]:
                interact_box = p.interact_rect()
                interact_box_draw = pygame.Rect(interact_box.x - world_x, interact_box.y - world_y, interact_box.w,
                                                interact_box.h, )
                pygame.draw.rect(screen, (255, 255, 0), interact_box_draw)
                if interact_box.colliderect(interact_rect):
                    pre_state = state
                    state = "interact_test_npc1"
            if keys[controls["inventory"]]:
                pre_state = state
                state = "inventory"
            rect = p.get_rect()
            pygame.draw.rect(screen, (0, 255, 0), (rect.x - world_x, rect.y - world_y, rect.width, rect.height), 1)
        elif state == "map_43":
            screen.blit(_scaled_images["c_o_lowms_cultist_battleground"], (-world_x, -world_y))
            walls = area_walls["map_43"].copy()
            # entity_walls = get_entity_walls(npcs, p)
            while logic_accumulator >= 1.0 / logic_tick:
                p.update_input()
                p.move(walls + entity_walls)
                p.border()
                logic_accumulator -= 1.0 / logic_tick
            world_x = p.x - screen_x // 2 + p.size // 2
            world_y = p.y - screen_y // 2 + p.size // 2
            p.draw(screen, world_x, world_y)
            keys = pygame.key.get_pressed()
            if keys[controls["interact"]]:
                interact_box = p.interact_rect()
                interact_box_draw = pygame.Rect(interact_box.x - world_x, interact_box.y - world_y, interact_box.w,
                                                interact_box.h)
                pygame.draw.rect(screen, (255, 255, 0), interact_box_draw)
                if interact_box.colliderect(interact_rect):
                    pre_state = state
                    state = "interact_test_npc1"
            if keys[controls["inventory"]]:
                pre_state = state
                state = "inventory"
            rect = p.get_rect()
            pygame.draw.rect(screen, (0, 255, 0), (rect.x - world_x, rect.y - world_y, rect.width, rect.height), 1)
        elif state == "map_44":

            screen.blit(_scaled_images["l_i_theocratic_battleground_endingb"], (-world_x, -world_y))

            walls = area_walls["map_44"].copy()

            # entity_walls = get_entity_walls(npcs, p)

            while logic_accumulator >= 1.0 / logic_tick:
                p.update_input()

                p.move(walls + entity_walls)

                p.border()

                logic_accumulator -= 1.0 / logic_tick

            world_x = p.x - screen_x // 2 + p.size // 2

            world_y = p.y - screen_y // 2 + p.size // 2

            p.draw(screen, world_x, world_y)

            keys = pygame.key.get_pressed()

            if keys[controls["interact"]]:

                interact_box = p.interact_rect()

                interact_box_draw = pygame.Rect(

                    interact_box.x - world_x,

                    interact_box.y - world_y,

                    interact_box.w,

                    interact_box.h,

                )

                pygame.draw.rect(screen, (255, 255, 0), interact_box_draw)

                if interact_box.colliderect(interact_rect):
                    pre_state = state

                    state = "interact_test_npc1"

            if keys[controls["inventory"]]:
                pre_state = state

                state = "inventory"

            rect = p.get_rect()

            pygame.draw.rect(screen, (0, 255, 0), (rect.x - world_x, rect.y - world_y, rect.width, rect.height), 1)
        elif state == "cutscene_01":
            screen.blit(_scaled_images["l_i_orphanage_access"], (-world_x, -world_y))
            walls = area_walls["cutscene_01"].copy()
            # entity_walls = get_entity_walls(npcs, p)
            while logic_accumulator >= 1.0 / logic_tick:
                p.update_input()
                p.move(walls + entity_walls)
                p.border()
                logic_accumulator -= 1.0 / logic_tick
            world_x = p.x - screen_x // 2 + p.size // 2
            world_y = p.y - screen_y // 2 + p.size // 2
            p.draw(screen, world_x, world_y)
            keys = pygame.key.get_pressed()
            if keys[controls["interact"]]:
                interact_box = p.interact_rect()
                interact_box_draw = pygame.Rect(interact_box.x - world_x, interact_box.y - world_y, interact_box.w,
                                                interact_box.h)
                pygame.draw.rect(screen, (255, 255, 0), interact_box_draw)
                if interact_box.colliderect(interact_rect):
                    pre_state = state
                    state = "interact_test_npc1"
            if keys[controls["inventory"]]:
                pre_state = state
                state = "inventory"
            rect = p.get_rect()
            pygame.draw.rect(screen, (0, 255, 0), (rect.x - world_x, rect.y - world_y, rect.width, rect.height), 1)

        elif state == "interact_test_npc1":
            screen.blit(_scaled_images["l_i_merchant_guild_hall"], (-world_x, -world_y))
            screen.blit(_scaled_images["elucidate_idle_blacksmith_npc_down"],
                        ((interact_rect.x - 18) - world_x, (interact_rect.y - 36) - world_y))
            p.draw(screen, world_x, world_y)
            screen.blit(_preloaded_images["walled_merchant_with_blacksmith_001"], (0, 0))
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    state = "interact_test_npc2"
        elif state == "interact_test_npc2":
            screen.blit(_scaled_images["l_i_merchant_guild_hall"], (-world_x, -world_y))
            screen.blit(_scaled_images["elucidate_idle_blacksmith_npc_down"],
                        ((interact_rect.x - 18) - world_x, (interact_rect.y - 36) - world_y))
            p.draw(screen, world_x, world_y)
            screen.blit(_preloaded_images["walled_merchant_with_blacksmith_002"], (0, 0))
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    state = "interact_test_npc3"
        elif state == "interact_test_npc3":
            screen.blit(_scaled_images["l_i_merchant_guild_hall"], (-world_x, -world_y))
            screen.blit(_scaled_images["elucidate_idle_blacksmith_npc_down"],
                        ((interact_rect.x - 18) - world_x, (interact_rect.y - 36) - world_y))
            p.draw(screen, world_x, world_y)
            screen.blit(_preloaded_images["walled_merchant_with_blacksmith_003"], (0, 0))
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    state = "interact_test_npc4"
        elif state == "interact_test_npc4":
            screen.blit(_scaled_images["l_i_merchant_guild_hall"], (-world_x, -world_y))
            screen.blit(_scaled_images["elucidate_idle_blacksmith_npc_down"],
                        ((interact_rect.x - 18) - world_x, (interact_rect.y - 36) - world_y))
            p.draw(screen, world_x, world_y)
            screen.blit(_preloaded_images["walled_merchant_with_blacksmith_004"], (0, 0))
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    state = "interact_test_npc5"
        elif state == "interact_test_npc5":
            screen.blit(_scaled_images["l_i_merchant_guild_hall"], (-world_x, -world_y))
            screen.blit(_scaled_images["elucidate_idle_blacksmith_npc_down"],
                        ((interact_rect.x - 18) - world_x, (interact_rect.y - 36) - world_y))
            p.draw(screen, world_x, world_y)
            screen.blit(_preloaded_images["walled_merchant_with_blacksmith_005"], (0, 0))
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    state = pre_state
        elif state == "interact_cult_leader1":
            screen.blit(_scaled_images["map_39"], (-world_x, -world_y))
            screen.blit(_scaled_images["elucidate_idle_cult_leader_npc_left"],
                        ((cult_leader_interact_rect.x - 18) - world_x, (cult_leader_interact_rect.y - 36) - world_y))
            p.draw(screen, world_x, world_y)
            screen.blit(_preloaded_images["cultist_island_funeris_with_cult_leader_001"], (0, 0))
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    state = "interact_cult_leader2"
        elif state == "interact_cult_leader2":
            screen.blit(_scaled_images["map_39"], (-world_x, -world_y))
            screen.blit(_scaled_images["elucidate_idle_cult_leader_npc_left"],
                        ((cult_leader_interact_rect.x - 18) - world_x, (cult_leader_interact_rect.y - 36) - world_y))
            p.draw(screen, world_x, world_y)
            screen.blit(_preloaded_images["cultist_island_funeris_with_cult_leader_002"], (0, 0))
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    state = "interact_cult_leader3"
        elif state == "interact_cult_leader3":
            screen.blit(_scaled_images["map_39"], (-world_x, -world_y))
            screen.blit(_scaled_images["elucidate_idle_cult_leader_npc_left"],
                        ((cult_leader_interact_rect.x - 18) - world_x, (cult_leader_interact_rect.y - 36) - world_y))
            p.draw(screen, world_x, world_y)
            screen.blit(_preloaded_images["cultist_island_funeris_with_cult_leader_003"], (0, 0))
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    state = "interact_cult_leader4"
        elif state == "interact_cult_leader4":
            screen.blit(_scaled_images["map_39"], (-world_x, -world_y))
            screen.blit(_scaled_images["elucidate_idle_merchant_cult_leader_npc_left"],
                        ((cult_leader_interact_rect.x - 18) - world_x, (cult_leader_interact_rect.y - 36) - world_y))
            p.draw(screen, world_x, world_y)
            screen.blit(_preloaded_images["cultist_island_funeris_with_cult_leader_004"], (0, 0))
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    state = "interact_cult_leader5"
        elif state == "interact_cult_leader5":
            screen.blit(_scaled_images["map_39"], (-world_x, -world_y))
            screen.blit(_scaled_images["elucidate_idle_cult_leader_npc_left"],
                        ((cult_leader_interact_rect.x - 18) - world_x, (cult_leader_interact_rect.y - 36) - world_y))
            p.draw(screen, world_x, world_y)
            screen.blit(_preloaded_images["cultist_island_funeris_with_cult_leader_005"], (0, 0))
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    state = "interact_cult_leader6"
        elif state == "interact_cult_leader6":
            screen.blit(_scaled_images["map_39"], (-world_x, -world_y))
            screen.blit(_scaled_images["elucidate_idle_cult_leader_npc_left"],
                        ((cult_leader_interact_rect.x - 18) - world_x, (cult_leader_interact_rect.y - 36) - world_y))
            p.draw(screen, world_x, world_y)
            screen.blit(_preloaded_images["cultist_island_funeris_with_cult_leader_006"], (0, 0))
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    state = "interact_cult_leader7"
        elif state == "interact_cult_leader7":
            screen.blit(_scaled_images["map_39"], (-world_x, -world_y))
            screen.blit(_scaled_images["elucidate_idle_cult_leader_npc_left"],
                        ((cult_leader_interact_rect.x - 18) - world_x, (cult_leader_interact_rect.y - 36) - world_y))
            p.draw(screen, world_x, world_y)
            screen.blit(_preloaded_images["cultist_island_funeris_with_cult_leader_007"], (0, 0))
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    state = "interact_cult_leader8"
        elif state == "interact_cult_leader8":
            screen.blit(_scaled_images["map_39"], (-world_x, -world_y))
            screen.blit(_scaled_images["elucidate_idle_cult_leader_npc_left"],
                        ((cult_leader_interact_rect.x - 18) - world_x, (cult_leader_interact_rect.y - 36) - world_y))
            p.draw(screen, world_x, world_y)
            screen.blit(_preloaded_images["cultist_island_funeris_with_cult_leader_008"], (0, 0))
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    state = "interact_cult_leader9"
        elif state == "interact_cult_leader9":
            screen.blit(_scaled_images["map_39"], (-world_x, -world_y))
            screen.blit(_scaled_images["elucidate_idle_cult_leader_npc_left"],
                        ((cult_leader_interact_rect.x - 18) - world_x, (cult_leader_interact_rect.y - 36) - world_y))
            p.draw(screen, world_x, world_y)
            screen.blit(_preloaded_images["cultist_island_funeris_with_cult_leader_009"], (0, 0))
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    state = "interact_cult_leader10"
        elif state == "interact_cult_leader10":
            screen.blit(_scaled_images["map_39"], (-world_x, -world_y))
            screen.blit(_scaled_images["elucidate_idle_cult_leader_npc_left"],
                        ((cult_leader_interact_rect.x - 18) - world_x, (cult_leader_interact_rect.y - 36) - world_y))
            p.draw(screen, world_x, world_y)
            screen.blit(_preloaded_images["cultist_island_funeris_with_cult_leader_010"], (0, 0))
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    state = "interact_cult_leader11"
        elif state == "interact_cult_leader11":
            screen.blit(_scaled_images["map_39"], (-world_x, -world_y))
            screen.blit(_scaled_images["elucidate_idle_cult_leader_npc_left"],
                        ((cult_leader_interact_rect.x - 18) - world_x, (cult_leader_interact_rect.y - 36) - world_y))
            p.draw(screen, world_x, world_y)
            screen.blit(_preloaded_images["cultist_island_funeris_with_cult_leader_011"], (0, 0))
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    state = "interact_cult_leader12"
        elif state == "interact_cult_leader12":
            screen.blit(_scaled_images["map_39"], (-world_x, -world_y))
            screen.blit(_scaled_images["elucidate_idle_cult_leader_npc_left"],
                        ((cult_leader_interact_rect.x - 18) - world_x, (cult_leader_interact_rect.y - 36) - world_y))
            p.draw(screen, world_x, world_y)
            screen.blit(_preloaded_images["cultist_island_funeris_with_cult_leader_012"], (0, 0))
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    state = "interact_cult_leader13"
        elif state == "interact_cult_leader13":
            screen.blit(_scaled_images["map_39"], (-world_x, -world_y))
            screen.blit(_scaled_images["elucidate_idle_cult_leader_npc_left"],
                        ((cult_leader_interact_rect.x - 18) - world_x, (cult_leader_interact_rect.y - 36) - world_y))
            p.draw(screen, world_x, world_y)
            screen.blit(_preloaded_images["cultist_island_funeris_with_cult_leader_013"], (0, 0))
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    state = "interact_cult_leader14"
        elif state == "interact_cult_leader14":
            screen.blit(_scaled_images["map_39"], (-world_x, -world_y))
            screen.blit(_scaled_images["elucidate_idle_cult_leader_npc_left"],
                        ((cult_leader_interact_rect.x - 18) - world_x, (cult_leader_interact_rect.y - 36) - world_y))
            p.draw(screen, world_x, world_y)
            screen.blit(_preloaded_images["cultist_island_funeris_with_cult_leader_014"], (0, 0))
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    state = "interact_cult_leader15"
        elif state == "interact_cult_leader15":
            screen.blit(_scaled_images["map_39"], (-world_x, -world_y))
            screen.blit(_scaled_images["elucidate_idle_cult_leader_npc_left"],
                        ((cult_leader_interact_rect.x - 18) - world_x, (cult_leader_interact_rect.y - 36) - world_y))
            p.draw(screen, world_x, world_y)
            screen.blit(_preloaded_images["cultist_island_funeris_with_cult_leader_015"], (0, 0))
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    state = pre_state
            rect = p.get_rect()
            pygame.draw.rect(screen, (0, 255, 0), (rect.x - world_x, rect.y - world_y, rect.width, rect.height), 1)
        elif state == "interact_draft_officer1":
            screen.blit(_scaled_images["l_o_outer_gate_district"], (-world_x, -world_y))
            screen.blit(_scaled_images["elucidate_idle_draft_officer_npc_left"],
                        ((draft_officer_interact_rect.x - 18) - world_x,
                         (draft_officer_interact_rect.y - 36) - world_y))
            p.draw(screen, world_x, world_y)
            screen.blit(_preloaded_images["walled_mercenary_with_draft_officer_001"], (0, 0))
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    state = "interact_draft_officer2"
        elif state == "interact_draft_officer2":
            screen.blit(_scaled_images["l_o_outer_gate_district"], (-world_x, -world_y))
            screen.blit(_scaled_images["elucidate_idle_draft_officer_npc_left"],
                        ((draft_officer_interact_rect.x - 18) - world_x,
                         (draft_officer_interact_rect.y - 36) - world_y))
            p.draw(screen, world_x, world_y)
            screen.blit(_preloaded_images["walled_mercenary_with_draft_officer_002"], (0, 0))
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    state = "interact_draft_officer3"
        elif state == "interact_draft_officer3":
            screen.blit(_scaled_images["l_o_outer_gate_district"], (-world_x, -world_y))
            screen.blit(_scaled_images["elucidate_idle_draft_officer_npc_left"],
                        ((draft_officer_interact_rect.x - 18) - world_x,
                         (draft_officer_interact_rect.y - 36) - world_y))
            p.draw(screen, world_x, world_y)
            screen.blit(_preloaded_images["walled_mercenary_with_draft_officer_003"], (0, 0))
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    state = "interact_draft_officer4"
        elif state == "interact_draft_officer4":
            screen.blit(_scaled_images["l_o_outer_gate_district"], (-world_x, -world_y))
            screen.blit(_scaled_images["elucidate_idle_draft_officer_npc_left"],
                        ((draft_officer_interact_rect.x - 18) - world_x,
                         (draft_officer_interact_rect.y - 36) - world_y))
            p.draw(screen, world_x, world_y)
            screen.blit(_preloaded_images["walled_mercenary_with_draft_officer_004"], (0, 0))
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    state = "interact_draft_officer5"
        elif state == "interact_draft_officer5":
            screen.blit(_scaled_images["l_o_outer_gate_district"], (-world_x, -world_y))
            screen.blit(_scaled_images["elucidate_idle_draft_officer_npc_left"],
                        ((draft_officer_interact_rect.x - 18) - world_x,
                         (draft_officer_interact_rect.y - 36) - world_y))
            p.draw(screen, world_x, world_y)
            screen.blit(_preloaded_images["walled_mercenary_with_draft_officer_005"], (0, 0))
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    state = "interact_draft_officer6"
        elif state == "interact_draft_officer6":
            screen.blit(_scaled_images["l_o_outer_gate_district"], (-world_x, -world_y))
            screen.blit(_scaled_images["elucidate_idle_draft_officer_npc_left"],
                        ((draft_officer_interact_rect.x - 18) - world_x,
                         (draft_officer_interact_rect.y - 36) - world_y))
            p.draw(screen, world_x, world_y)
            screen.blit(_preloaded_images["walled_mercenary_with_draft_officer_006"], (0, 0))
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    state = "interact_draft_officer7"
        elif state == "interact_draft_officer7":
            screen.blit(_scaled_images["l_o_outer_gate_district"], (-world_x, -world_y))
            screen.blit(_scaled_images["elucidate_idle_draft_officer_npc_left"],
                        ((draft_officer_interact_rect.x - 18) - world_x,
                         (draft_officer_interact_rect.y - 36) - world_y))
            p.draw(screen, world_x, world_y)
            screen.blit(_preloaded_images["walled_mercenary_with_draft_officer_007"], (0, 0))
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    state = "interact_draft_officer8"
        elif state == "interact_draft_officer8":
            screen.blit(_scaled_images["l_o_outer_gate_district"], (-world_x, -world_y))
            screen.blit(_scaled_images["elucidate_idle_draft_officer_npc_left"],
                        ((draft_officer_interact_rect.x - 18) - world_x,
                         (draft_officer_interact_rect.y - 36) - world_y))
            p.draw(screen, world_x, world_y)
            screen.blit(_preloaded_images["walled_mercenary_with_draft_officer_008"], (0, 0))
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    state = pre_state

        elif state == "inventory":
            state = "inventory1"
        elif state == "inventory1":
            if user_class == "mercenary":
                screen.blit(_preloaded_images["elucidate_inventory_001"], (0, 0))
            elif user_class == "cultist":
                screen.blit(_preloaded_images["elucidate_inventory_002"], (0, 0))
            elif user_class == "priest":
                screen.blit(_preloaded_images["elucidate_dlc_inventory_001"], (0, 0))
            elif user_class == "shaman":
                screen.blit(_preloaded_images["elucidate_dlc_inventory_002"], (0, 0))
            elif user_class == "merchant":
                screen.blit(_preloaded_images["elucidate_dlc_inventory_003"], (0, 0))
            static_text_raw("STATS", color=(255, 255, 255), position=(5, 20), size=35)
            static_text_raw("BAG", color=(255, 255, 255), position=(5, 55), size=35)
            static_text_raw("EQUIPMENT", color=(255, 255, 255), position=(5, 90), size=35)
            static_text_raw("CONTINUE", color=(255, 255, 255), position=(5, 125), size=35)
            static_text_raw("SAVES", color=(255, 255, 255), position=(5, 160), size=35)
            static_text_raw("EXIT", color=(255, 255, 255), position=(5, 195), size=35)
            static_text_raw("Class: ", color=(255, 255, 255), position=(360, 5), size=30)
            static_text_raw(user_class, color=(255, 255, 255), position=(470, 5), size=30)
            static_text_raw("Name:", color=(255, 255, 255), position=(360, 35), size=30)
            static_text_raw(user_name, color=(255, 255, 255), position=(470, 35), size=30)
            static_text_raw("Body ", color=(255, 255, 255), position=(360, 130), size=20)
            static_text_raw(str(user_body), color=(255, 255, 255), position=(430, 130), size=20)
            static_text_raw("STR ", color=(255, 255, 255), position=(360, 150), size=20)
            static_text_raw(str(user_str), color=(255, 255, 255), position=(430, 150), size=20)
            static_text_raw("DEF ", color=(255, 255, 255), position=(360, 170), size=20)
            static_text_raw(str(user_def), color=(255, 255, 255), position=(430, 170), size=20)
            static_text_raw("AGI ", color=(255, 255, 255), position=(360, 190), size=20)
            static_text_raw(str(user_agi), color=(255, 255, 255), position=(430, 190), size=20)
            static_text_raw("Mind ", color=(255, 255, 255), position=(360, 210), size=20)
            static_text_raw(str(user_mind_state), color=(255, 255, 255), position=(430, 210), size=20)
            if user_status_bleeding != 0:
                static_text_raw("Bleeding", color=(255, 255, 255), position=(360, 250), size=20)
            else:
                static_text_raw("///", color=(255, 255, 255), position=(360, 250), size=20)
            if user_status_infection != 0:
                static_text_raw("Infection", color=(255, 255, 255), position=(360, 270), size=20)
            else:
                static_text_raw("///", color=(255, 255, 255), position=(360, 270), size=20)
            if user_status_brokenbones != 0:
                static_text_raw("Broken Bones", color=(255, 255, 255), position=(360, 290), size=20)
            else:
                static_text_raw("///", color=(255, 255, 255), position=(360, 290), size=20)
            if user_status_stun != 0:
                static_text_raw("Stunned", color=(255, 255, 255), position=(360, 310), size=20)
            else:
                static_text_raw("///", color=(255, 255, 255), position=(360, 310), size=20)
            if user_status_confusion != 0:
                static_text_raw("Confusion", color=(255, 255, 255), position=(360, 330), size=20)
            else:
                static_text_raw("///", color=(255, 255, 255), position=(360, 330), size=20)
            if user_status_blindness != 0:
                static_text_raw("Blindness", color=(255, 255, 255), position=(360, 350), size=20)
            else:
                static_text_raw("///", color=(255, 255, 255), position=(360, 350), size=20)
            if user_status_critical != 0:
                static_text_raw("Critical", color=(255, 255, 255), position=(360, 370), size=20)
            else:
                static_text_raw("///", color=(255, 255, 255), position=(360, 370), size=20)
            if user_status_infected != 0:
                static_text_raw("Infected", color=(255, 255, 255), position=(360, 390), size=20)
            else:
                static_text_raw("///", color=(255, 255, 255), position=(360, 390), size=20)
            if colide_inventory_stats.collidepoint(mouse_x, mouse_y):
                screen.blit(_scaled_images["elucidate_select_inv"], (5, 22))
                static_text_raw("STATS", color=(0, 0, 0), position=(15, 20), size=35)
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        state = "inventory1"
            elif colide_inventory_bag.collidepoint(mouse_x, mouse_y):
                screen.blit(_scaled_images["elucidate_select_inv"], (5, 58))
                static_text_raw("BAG", color=(0, 0, 0), position=(15, 55), size=35)
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        state = "inventory_bag"
            elif colide_inventory_equipment.collidepoint(mouse_x, mouse_y):
                screen.blit(_scaled_images["elucidate_select_inv"], (5, 95))
                static_text_raw("EQUIPMENT", color=(0, 0, 0), position=(15, 90), size=35)
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:

                        state = "home"
            elif colide_inventory_continue.collidepoint(mouse_x, mouse_y):
                screen.blit(_scaled_images["elucidate_select_inv"], (5, 130))
                static_text_raw("CONTINUE", color=(0, 0, 0), position=(15, 125), size=35)
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        state = pre_state
            elif colide_inventory_saves.collidepoint(mouse_x, mouse_y):
                screen.blit(_scaled_images["elucidate_select_inv"], (5, 162))
                static_text_raw("SAVES", color=(0, 0, 0), position=(15, 160), size=35)
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        state = pre_state
            elif colide_inventory_exit.collidepoint(mouse_x, mouse_y):
                screen.blit(_scaled_images["elucidate_select_inv"], (5, 194))
                static_text_raw("EXIT", color=(0, 0, 0), position=(15, 195), size=35)
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        state = "home"  # elucidate_sys_exit()
        elif state == "inventory_bag":
            screen.blit(_preloaded_images["elucidate_bag_inventory_001"], (0, 0))
            static_text_raw("STATS", color=(255, 255, 255), position=(5, 20), size=35)
            static_text_raw("BAG", color=(255, 255, 255), position=(5, 55), size=35)
            static_text_raw("EQUIPMENT", color=(255, 255, 255), position=(5, 90), size=35)
            static_text_raw("CONTINUE", color=(255, 255, 255), position=(5, 125), size=35)
            static_text_raw("SAVES", color=(255, 255, 255), position=(5, 160), size=35)
            static_text_raw("EXIT", color=(255, 255, 255), position=(5, 195), size=35)
            if colide_inventory_stats.collidepoint(mouse_x, mouse_y):
                screen.blit(_scaled_images["elucidate_select_inv"], (5, 22))
                static_text_raw("STATS", color=(0, 0, 0), position=(15, 20), size=35)
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        state = "inventory1"
            elif colide_inventory_bag.collidepoint(mouse_x, mouse_y):
                screen.blit(_scaled_images["elucidate_select_inv"], (5, 58))
                static_text_raw("BAG", color=(0, 0, 0), position=(15, 55), size=35)
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        state = "inventory_bag"
            elif colide_inventory_equipment.collidepoint(mouse_x, mouse_y):
                screen.blit(_scaled_images["elucidate_select_inv"], (5, 95))
                static_text_raw("EQUIPMENT", color=(0, 0, 0), position=(15, 90), size=35)
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        state = "home"
            elif colide_inventory_continue.collidepoint(mouse_x, mouse_y):
                screen.blit(_scaled_images["elucidate_select_inv"], (5, 130))
                static_text_raw("CONTINUE", color=(0, 0, 0), position=(15, 125), size=35)
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        state = pre_state
            elif colide_inventory_saves.collidepoint(mouse_x, mouse_y):
                screen.blit(_scaled_images["elucidate_select_inv"], (5, 162))
                static_text_raw("SAVES", color=(0, 0, 0), position=(15, 160), size=35)
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        state = pre_state
            elif colide_inventory_exit.collidepoint(mouse_x, mouse_y):
                screen.blit(_scaled_images["elucidate_select_inv"], (5, 194))
                static_text_raw("EXIT", color=(0, 0, 0), position=(15, 195), size=35)
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        state = "home"  # elucidate_sys_exit()
            if user_item_book_of_crafsmanship > 0:
                screen.blit(_scaled_images["materials_skill_book_of_crafsmanship"], (470, 93))
                tuple_static_text(user_item_book_of_crafsmanship, color=(240, 240, 240), position=(470 + 72, 93 + 30), size=15)
                if inv1.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_book_of_agility > 0:
                screen.blit(_scaled_images["materials_skill_book_of_agility"], (465, 145))
                tuple_static_text(user_item_book_of_agility, color=(240, 240, 240), position=(465 + 72, 145 + 30),
                                  size=15)
                if inv2.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_book_of_healing > 0:
                screen.blit(_scaled_images["materials_skill_book_of_healing"], (469, 198))
                tuple_static_text(user_item_book_of_healing, color=(240, 240, 240), position=(469 + 72, 198 + 30),
                                  size=15)
                if inv3.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_book_of_instincts > 0:
                screen.blit(_scaled_images["materials_skill_book_of_instincts"], (472, 248))
                tuple_static_text(user_item_book_of_instincts, color=(240, 240, 240), position=(472 + 72, 248 + 30),
                                  size=15)
                if inv4.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_book_of_stars > 0:
                screen.blit(_scaled_images["materials_skill_book_of_stars"], (471, 299))
                tuple_static_text(user_item_book_of_stars, color=(240, 240, 240), position=(471 + 72, 299 + 30),
                                  size=15)
                if inv5.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_book_of_the_secrets > 0:
                screen.blit(_scaled_images["materials_skill_book_of_the_secrets"], (471, 353))
                tuple_static_text(user_item_book_of_the_secrets, color=(240, 240, 240), position=(471 + 72, 353 + 30),
                                  size=15)
                if inv6.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_book_of_enlightenment > 0:
                screen.blit(_scaled_images["materials_save_book_of_enlightenment"], (470, 405))
                tuple_static_text(user_item_book_of_enlightenment, color=(240, 240, 240), position=(470 + 72, 405 + 30),
                                  size=15)
                if inv7.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_book_of_cowardice_i > 0:
                screen.blit(_scaled_images["materials_skill_book_of_cowardice_i"], (470, 458))
                tuple_static_text(user_item_book_of_cowardice_i, color=(240, 240, 240), position=(470 + 72, 458 + 30),
                                  size=15)
                if inv8.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_book_of_cowardice_ii > 0:
                screen.blit(_scaled_images["materials_skill_book_of_cowardice_ii"], (468, 508))
                tuple_static_text(user_item_book_of_cowardice_ii, color=(240, 240, 240), position=(468 + 72, 508 + 30),
                                  size=15)
                if inv9.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_book_of_pestilence_i > 0:
                screen.blit(_scaled_images["materials_skill_book_of_pestilence_i"], (467, 560))
                tuple_static_text(user_item_book_of_pestilence_i, color=(240, 240, 240), position=(467 + 72, 560 + 30),
                                  size=15)
                if inv10.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            user_item_book_of_pestilence_i -=1
                            user_status_bleeding = 1
            if user_item_book_of_pestilence_ii > 0:
                screen.blit(_scaled_images["materials_skill_book_of_pestilence_ii"], (613, 93))
                tuple_static_text(user_item_book_of_pestilence_ii, color=(240, 240, 240), position=(613 + 72, 93 + 30),
                                  size=15)
                if inv11.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            user_item_book_of_pestilence_ii -= 1
                            user_status_infection = 1
            if user_item_book_of_pestilence_iii > 0:
                screen.blit(_scaled_images["materials_skill_book_of_pestilence_iii"], (614, 143))
                tuple_static_text(user_item_book_of_pestilence_iii, color=(240, 240, 240),
                                  position=(614 + 72, 143 + 30), size=15)
                if inv12.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            user_item_book_of_pestilence_iii -= 1
                            user_status_brokenbones = 1
            if user_item_book_of_pestilence_iv > 0:
                screen.blit(_scaled_images["materials_skill_book_of_pestilence_iv"], (619, 194))
                tuple_static_text(user_item_book_of_pestilence_iv, color=(240, 240, 240), position=(619 + 72, 194 + 30),
                                  size=15)
                if inv13.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            user_item_book_of_pestilence_iv -= 1
                            user_status_stun = 1
            if user_item_book_of_pestilence_v > 0:
                screen.blit(_scaled_images["materials_skill_book_of_pestilence_v"], (616, 249))
                tuple_static_text(user_item_book_of_pestilence_v, color=(240, 240, 240), position=(616 + 72, 249 + 30),
                                  size=15)
                if inv14.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            user_item_book_of_pestilence_v -= 1
                            user_status_confusion = 1
            if user_item_book_of_pestilence_vi > 0:
                screen.blit(_scaled_images["materials_skill_book_of_pestilence_vi"], (616, 299))
                tuple_static_text(user_item_book_of_pestilence_vi, color=(240, 240, 240), position=(616 + 72, 299 + 30),
                                  size=15)
                if inv15.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            user_item_book_of_pestilence_vi -= 1
                            user_status_blindness = 1
            if user_item_book_of_pestilence_vii > 0:
                screen.blit(_scaled_images["materials_skill_book_of_pestilence_vii"], (617, 354))
                tuple_static_text(user_item_book_of_pestilence_vii, color=(240, 240, 240),
                                  position=(617 + 72, 354 + 30), size=15)
                if inv16.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            user_item_book_of_pestilence_vii -= 1
                            user_status_critical = 1
            if user_item_book_of_pestilence_viii > 0:
                screen.blit(_scaled_images["materials_skill_book_of_pestilence_viii"], (615, 404))
                tuple_static_text(user_item_book_of_pestilence_viii, color=(240, 240, 240),
                                  position=(615 + 72, 404 + 30), size=15)
                if inv17.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            user_item_book_of_pestilence_viii -= 1
                            user_status_infected = 1
            if user_item_book_of_trade_i > 0:
                screen.blit(_scaled_images["materials_skill_book_of_trade_i"], (614, 458))
                tuple_static_text(user_item_book_of_trade_i, color=(240, 240, 240), position=(614 + 72, 458 + 30),
                                  size=15)
                if inv18.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_book_of_trade_ii > 0:
                screen.blit(_scaled_images["materials_skill_book_of_trade_ii"], (615, 508))
                tuple_static_text(user_item_book_of_trade_ii, color=(240, 240, 240), position=(615 + 72, 508 + 30),
                                  size=15)
                if inv19.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_book_of_trade_iii > 0:
                screen.blit(_scaled_images["materials_skill_book_of_trade_iii"], (618, 561))
                tuple_static_text(user_item_book_of_trade_iii, color=(240, 240, 240), position=(618 + 72, 561 + 30),
                                  size=15)
                if inv20.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_red_gem > 0:
                screen.blit(_scaled_images["materials_gem_red_gem"], (777, 100))
                tuple_static_text(user_item_red_gem, color=(240, 240, 240), position=(762 + 77, 92 + 30), size=15)
                if inv21.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_blue_gem > 0:
                screen.blit(_scaled_images["materials_gem_blue_gem"], (777, 157))
                tuple_static_text(user_item_blue_gem, color=(240, 240, 240), position=(763 + 77, 145 + 30), size=15)
                if inv22.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_ale > 0:
                screen.blit(_scaled_images["materials_beverage_ale"], (777, 203))
                tuple_static_text(user_item_ale, color=(240, 240, 240), position=(767 + 77, 197 + 35), size=15)
                if inv23.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_wine > 0:
                screen.blit(_scaled_images["materials_beverage_wine"], (777, 262))
                tuple_static_text(user_item_wine, color=(240, 240, 240), position=(765 + 77, 250 + 35), size=15)
                if inv24.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_rum > 0:
                screen.blit(_scaled_images["materials_beverage_rum"], (777, 317))
                tuple_static_text(user_item_rum, color=(240, 240, 240), position=(765 + 72, 302 + 30), size=15)
                if inv25.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_iron_ingot > 0:
                screen.blit(_scaled_images["materials_bar_iron_ingot"], (777, 370))
                tuple_static_text(user_item_iron_ingot, color=(240, 240, 240), position=(763 + 72, 352 + 30), size=15)
                if inv26.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_raw_iron > 0:
                screen.blit(_scaled_images["materials_ore_raw_iron"], (777, 435))
                tuple_static_text(user_item_raw_iron, color=(240, 240, 240), position=(764 + 72, 405 + 30), size=15)
                if inv27.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_green_herb > 0:
                screen.blit(_scaled_images["materials_foliage_green_herb"], (777, 465))
                tuple_static_text(user_item_green_herb, color=(240, 240, 240), position=(764 + 72, 455 + 30), size=15)
                if inv28.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_blue_herb > 0:
                screen.blit(_scaled_images["materials_foliage_blue_herb-1"], (777, 519))
                tuple_static_text(user_item_blue_herb, color=(240, 240, 240), position=(763 + 72, 509 + 30), size=15)
                if inv29.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_paper > 0:
                screen.blit(_scaled_images["materials_sheet_paper"], (777, 574))
                tuple_static_text(user_item_paper, color=(240, 240, 240), position=(763 + 72, 562 + 30), size=15)
                if inv30.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_ancient_paper > 0:
                screen.blit(_scaled_images["materials_sheet_ancient_paper"], (928, 102))
                tuple_static_text(user_item_ancient_paper, color=(240, 240, 240), position=(910 + 72, 92 + 30), size=15)
                if inv31.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_antibiotics > 0:
                screen.blit(_scaled_images["materials_potion_antibiotics"], (928, 160))
                tuple_static_text(user_item_antibiotics, color=(240, 240, 240), position=(910 + 72, 144 + 30), size=15)
                if inv32.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_betadine > 0:
                screen.blit(_scaled_images["materials_potion_betadine"], (928, 216))
                tuple_static_text(user_item_betadine, color=(240, 240, 240), position=(912 + 72, 198 + 30), size=15)
                if inv33.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_red_vial > 0:
                screen.blit(_scaled_images["materials_potion_red_vial"], (928, 256))
                tuple_static_text(user_item_red_vial, color=(240, 240, 240), position=(911 + 72, 242 + 30), size=15)
                if inv34.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_empty_vial > 0:
                screen.blit(_scaled_images["materials_container_empty_vial"], (928, 311))
                tuple_static_text(user_item_empty_vial, color=(240, 240, 240), position=(911 + 72, 299 + 30), size=15)
                if inv35.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_book_of_marksmanship > 0:
                screen.blit(_scaled_images["materials_skill_book_of_marksmanship"], (911, 353))
                tuple_static_text(user_item_book_of_marksmanship, color=(240, 240, 240), position=(911 + 72, 353 + 30), size=15)
                if inv36.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_book_of_rapid_fire > 0:
                screen.blit(_scaled_images["materials_skill_book_of_rapid_fire"], (911, 405))
                tuple_static_text(user_item_book_of_rapid_fire, color=(240, 240, 240), position=(911 + 72, 405 + 30), size=15)
                if inv37.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_leather_scraps > 0:
                screen.blit(_scaled_images["materials_scrap_leather_scraps"], (922, 465))
                tuple_static_text(user_item_leather_scraps, color=(240, 240, 240), position=(911 + 72, 455 + 30), size=15)
                if inv38.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_wooden_plank > 0:
                screen.blit(_scaled_images["materials_plank_wooden_plank"], (934, 530))
                tuple_static_text(user_item_wooden_plank, color=(240, 240, 240), position=(911 + 72, 508 + 30), size=15)
                if inv39.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_silver_wire > 0:
                screen.blit(_scaled_images["materials_component_silver_wire"], (936, 570))
                tuple_static_text(user_item_silver_wire, color=(240, 240, 240), position=(911 + 72, 557 + 30), size=15)
                if inv40.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_bowstring > 0:
                screen.blit(_scaled_images["materials_component_bow_string"], (1049, 93))
                tuple_static_text(user_item_bowstring, color=(240, 240, 240), position=(1049 + 72, 98 + 30), size=15)
                if inv41.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_coif > 0:
                screen.blit(_scaled_images["armour_headware_guard_coif"], (1068, 164))
                tuple_static_text(user_item_coif, color=(240, 240, 240), position=(1050 + 72, 145 + 30), size=15)
                if inv42.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_red_amulet > 0:
                screen.blit(_scaled_images["armour_accessories_red_amulet"], (1058, 217))
                tuple_static_text(user_item_red_amulet, color=(240, 240, 240), position=(1053 + 72, 195 + 30), size=15)
                if inv43.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_arm_guard > 0:
                screen.blit(_scaled_images["armour_armwear_arm_guard"], (1060, 255))
                tuple_static_text(user_item_arm_guard, color=(240, 240, 240), position=(1050 + 72, 248 + 30), size=15)
                if inv44.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_ring > 0:
                screen.blit(_scaled_images["armour_accessories_ring"], (1076, 307))
                tuple_static_text(user_item_ring, color=(240, 240, 240), position=(1050 + 72, 303 + 30), size=15)
                if inv45.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if inv_back.collidepoint(mouse_x, mouse_y):
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        state = "inventory_bag2"
            if inv_next.collidepoint(mouse_x, mouse_y):
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        state = "inventory_bag2"
        elif state == "inventory_bag2":
            screen.blit(_preloaded_images["elucidate_bag_inventory_001"], (0, 0))
            static_text_raw("STATS", color=(255, 255, 255), position=(5, 20), size=35)
            static_text_raw("BAG", color=(255, 255, 255), position=(5, 55), size=35)
            static_text_raw("EQUIPMENT", color=(255, 255, 255), position=(5, 90), size=35)
            static_text_raw("CONTINUE", color=(255, 255, 255), position=(5, 125), size=35)
            static_text_raw("SAVES", color=(255, 255, 255), position=(5, 160), size=35)
            static_text_raw("EXIT", color=(255, 255, 255), position=(5, 195), size=35)
            if colide_inventory_stats.collidepoint(mouse_x, mouse_y):
                screen.blit(_scaled_images["elucidate_select_inv"], (5, 22))
                static_text_raw("STATS", color=(0, 0, 0), position=(15, 20), size=35)
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        state = "inventory1"
            elif colide_inventory_bag.collidepoint(mouse_x, mouse_y):
                screen.blit(_scaled_images["elucidate_select_inv"], (5, 58))
                static_text_raw("BAG", color=(0, 0, 0), position=(15, 55), size=35)
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        state = "inventory_bag2"
            elif colide_inventory_equipment.collidepoint(mouse_x, mouse_y):
                screen.blit(_scaled_images["elucidate_select_inv"], (5, 95))
                static_text_raw("EQUIPMENT", color=(0, 0, 0), position=(15, 90), size=35)
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        state = "home"
            elif colide_inventory_continue.collidepoint(mouse_x, mouse_y):
                screen.blit(_scaled_images["elucidate_select_inv"], (5, 130))
                static_text_raw("CONTINUE", color=(0, 0, 0), position=(15, 125), size=35)
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        state = pre_state
            elif colide_inventory_saves.collidepoint(mouse_x, mouse_y):
                screen.blit(_scaled_images["elucidate_select_inv"], (5, 162))
                static_text_raw("SAVES", color=(0, 0, 0), position=(15, 160), size=35)
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        state = pre_state
            elif colide_inventory_exit.collidepoint(mouse_x, mouse_y):
                screen.blit(_scaled_images["elucidate_select_inv"], (5, 194))
                static_text_raw("EXIT", color=(0, 0, 0), position=(15, 195), size=35)
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        state = "home"  # elucidate_sys_exit()
            if user_item_stick > 0:
                screen.blit(_scaled_images["materials_bar_iron_ingot"], (470, 93))
                tuple_static_text(user_item_stick, color=(240, 240, 240), position=(470 + 72, 93 + 30), size=15)
                if inv1.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_bascinet > 0:
                screen.blit(_scaled_images["materials_bar_iron_ingot"], (465, 145))
                tuple_static_text(user_item_bascinet, color=(240, 240, 240), position=(465 + 72, 145 + 30),
                                  size=15)
                if inv2.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_iron_helmet > 0:
                screen.blit(_scaled_images["materials_bar_iron_ingot"], (469, 198))
                tuple_static_text(user_item_iron_helmet, color=(240, 240, 240), position=(469 + 72, 198 + 30),
                                  size=15)
                if inv3.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_cloth_hood > 0:
                screen.blit(_scaled_images["materials_skill_book_of_instincts"], (472, 248))
                tuple_static_text(user_item_cloth_hood, color=(240, 240, 240), position=(472 + 72, 248 + 30),
                                  size=15)
                if inv4.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_arming_cap > 0:
                screen.blit(_scaled_images["materials_skill_book_of_stars"], (471, 299))
                tuple_static_text(user_item_arming_cap, color=(240, 240, 240), position=(471 + 72, 299 + 30),
                                  size=15)
                if inv5.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_chainmail_hood > 0:
                screen.blit(_scaled_images["materials_skill_book_of_the_secrets"], (471, 353))
                tuple_static_text(user_item_chainmail_hood, color=(240, 240, 240), position=(471 + 72, 353 + 30),
                                  size=15)
                if inv6.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_plate_helmet > 0:
                screen.blit(_scaled_images["materials_save_book_of_enlightenment"], (470, 405))
                tuple_static_text(user_item_plate_helmet, color=(240, 240, 240), position=(470 + 72, 405 + 30),
                                  size=15)
                if inv7.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_iron_mask > 0:
                screen.blit(_scaled_images["materials_skill_book_of_cowardice_i"], (470, 458))
                tuple_static_text(user_item_iron_mask, color=(240, 240, 240), position=(470 + 72, 458 + 30),
                                  size=15)
                if inv8.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_guard_bascinet > 0:
                screen.blit(_scaled_images["materials_skill_book_of_cowardice_ii"], (468, 508))
                tuple_static_text(user_item_guard_bascinet, color=(240, 240, 240), position=(468 + 72, 508 + 30),
                                  size=15)
                if inv9.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_red_scarf > 0:
                screen.blit(_scaled_images["materials_skill_book_of_pestilence_i"], (467, 560))
                tuple_static_text(user_item_red_scarf, color=(240, 240, 240), position=(467 + 72, 560 + 30),
                                  size=15)
                if inv10.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            user_item_book_of_pestilence_i -=1
                            user_status_bleeding = 1
            if user_item_leather_vest > 0:
                screen.blit(_scaled_images["materials_skill_book_of_pestilence_ii"], (613, 93))
                tuple_static_text(user_item_leather_vest, color=(240, 240, 240), position=(613 + 72, 93 + 30),
                                  size=15)
                if inv11.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            user_item_book_of_pestilence_ii -= 1
                            user_status_infection = 1
            if user_item_loincloth > 0:
                screen.blit(_scaled_images["materials_skill_book_of_pestilence_iii"], (614, 143))
                tuple_static_text(user_item_loincloth, color=(240, 240, 240),
                                  position=(614 + 72, 143 + 30), size=15)
                if inv12.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            user_item_book_of_pestilence_iii -= 1
                            user_status_brokenbones = 1
            if user_item_priests_robe > 0:
                screen.blit(_scaled_images["materials_skill_book_of_pestilence_iv"], (619, 194))
                tuple_static_text(user_item_priests_robe, color=(240, 240, 240), position=(619 + 72, 194 + 30),
                                  size=15)
                if inv13.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            user_item_book_of_pestilence_iv -= 1
                            user_status_stun = 1
            if user_item_dark_priests_robe > 0:
                screen.blit(_scaled_images["materials_skill_book_of_pestilence_v"], (616, 249))
                tuple_static_text(user_item_dark_priests_robe, color=(240, 240, 240), position=(616 + 72, 249 + 30),
                                  size=15)
                if inv14.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            user_item_book_of_pestilence_v -= 1
                            user_status_confusion = 1
            if user_item_hard_leather_armor > 0:
                screen.blit(_scaled_images["materials_skill_book_of_pestilence_vi"], (616, 299))
                tuple_static_text(user_item_hard_leather_armor, color=(240, 240, 240), position=(616 + 72, 299 + 30),
                                  size=15)
                if inv15.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            user_item_book_of_pestilence_vi -= 1
                            user_status_blindness = 1
            if user_item_plated_mail > 0:
                screen.blit(_scaled_images["materials_skill_book_of_pestilence_vii"], (617, 354))
                tuple_static_text(user_item_plated_mail, color=(240, 240, 240),
                                  position=(617 + 72, 354 + 30), size=15)
                if inv16.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            user_item_book_of_pestilence_vii -= 1
                            user_status_critical = 1
            if user_item_black_dress > 0:
                screen.blit(_scaled_images["materials_skill_book_of_pestilence_viii"], (615, 404))
                tuple_static_text(user_item_black_dress, color=(240, 240, 240),
                                  position=(615 + 72, 404 + 30), size=15)
                if inv17.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            user_item_book_of_pestilence_viii -= 1
                            user_status_infected = 1
            if user_item_iron_cuirass > 0:
                screen.blit(_scaled_images["materials_skill_book_of_trade_i"], (614, 458))
                tuple_static_text(user_item_iron_cuirass, color=(240, 240, 240), position=(614 + 72, 458 + 30),
                                  size=15)
                if inv18.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_plate_armour > 0:
                screen.blit(_scaled_images["materials_skill_book_of_trade_ii"], (615, 508))
                tuple_static_text(user_item_plate_armour, color=(240, 240, 240), position=(615 + 72, 508 + 30),
                                  size=15)
                if inv19.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_trench_coat > 0:
                screen.blit(_scaled_images["materials_skill_book_of_trade_iii"], (618, 561))
                tuple_static_text(user_item_trench_coat, color=(240, 240, 240), position=(618 + 72, 561 + 30),
                                  size=15)
                if inv20.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_wooden_buckler > 0:
                screen.blit(_scaled_images["materials_gem_red_gem"], (777, 100))
                tuple_static_text(user_item_wooden_buckler, color=(240, 240, 240), position=(762 + 77, 92 + 30), size=15)
                if inv21.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_scutum > 0:
                screen.blit(_scaled_images["materials_gem_blue_gem"], (777, 157))
                tuple_static_text(user_item_scutum, color=(240, 240, 240), position=(763 + 77, 145 + 30), size=15)
                if inv22.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_iron_shield > 0:
                screen.blit(_scaled_images["materials_beverage_ale"], (777, 203))
                tuple_static_text(user_item_iron_shield, color=(240, 240, 240), position=(767 + 77, 197 + 35), size=15)
                if inv23.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_short_sword > 0:
                screen.blit(_scaled_images["materials_beverage_wine"], (777, 262))
                tuple_static_text(user_item_short_sword, color=(240, 240, 240), position=(765 + 77, 250 + 35), size=15)
                if inv24.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_cleaver > 0:
                screen.blit(_scaled_images["materials_beverage_rum"], (777, 317))
                tuple_static_text(user_item_cleaver, color=(240, 240, 240), position=(765 + 72, 302 + 30), size=15)
                if inv25.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_dagger > 0:
                screen.blit(_scaled_images["materials_bar_iron_ingot"], (777, 370))
                tuple_static_text(user_item_dagger, color=(240, 240, 240), position=(763 + 72, 352 + 30), size=15)
                if inv26.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_longsword > 0:
                screen.blit(_scaled_images["materials_ore_raw_iron"], (777, 435))
                tuple_static_text(user_item_longsword, color=(240, 240, 240), position=(764 + 72, 405 + 30), size=15)
                if inv27.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_iron_axe > 0:
                screen.blit(_scaled_images["materials_foliage_green_herb"], (777, 465))
                tuple_static_text(user_item_iron_axe, color=(240, 240, 240), position=(764 + 72, 455 + 30), size=15)
                if inv28.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_mace > 0:
                screen.blit(_scaled_images["materials_foliage_blue_herb-1"], (777, 519))
                tuple_static_text(user_item_mace, color=(240, 240, 240), position=(763 + 72, 509 + 30), size=15)
                if inv29.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_corsairs_saber > 0:
                screen.blit(_scaled_images["materials_sheet_paper"], (777, 574))
                tuple_static_text(user_item_corsairs_saber, color=(240, 240, 240), position=(763 + 72, 562 + 30), size=15)
                if inv30.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_knife > 0:
                screen.blit(_scaled_images["materials_sheet_ancient_paper"], (928, 102))
                tuple_static_text(user_item_knife, color=(240, 240, 240), position=(910 + 72, 92 + 30), size=15)
                if inv31.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_improvised_shiv > 0:
                screen.blit(_scaled_images["materials_potion_antibiotics"], (928, 160))
                tuple_static_text(user_item_improvised_shiv, color=(240, 240, 240), position=(910 + 72, 144 + 30), size=15)
                if inv32.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_steel_hammer > 0:
                screen.blit(_scaled_images["materials_potion_betadine"], (928, 216))
                tuple_static_text(user_item_steel_hammer, color=(240, 240, 240), position=(912 + 72, 198 + 30), size=15)
                if inv33.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_stiletto > 0:
                screen.blit(_scaled_images["materials_potion_red_vial"], (928, 256))
                tuple_static_text(user_item_stiletto, color=(240, 240, 240), position=(911 + 72, 242 + 30), size=15)
                if inv34.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_dirk > 0:
                screen.blit(_scaled_images["materials_container_empty_vial"], (928, 311))
                tuple_static_text(user_item_dirk, color=(240, 240, 240), position=(911 + 72, 299 + 30), size=15)
                if inv35.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_scimitar > 0:
                screen.blit(_scaled_images["materials_skill_book_of_marksmanship"], (911, 353))
                tuple_static_text(user_item_scimitar, color=(240, 240, 240), position=(911 + 72, 353 + 30), size=15)
                if inv36.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_greatsword > 0:
                screen.blit(_scaled_images["materials_skill_book_of_rapid_fire"], (911, 405))
                tuple_static_text(user_item_greatsword, color=(240, 240, 240), position=(911 + 72, 405 + 30), size=15)
                if inv37.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_makeshift_spear > 0:
                screen.blit(_scaled_images["materials_scrap_leather_scraps"], (922, 465))
                tuple_static_text(user_item_makeshift_spear, color=(240, 240, 240), position=(911 + 72, 455 + 30), size=15)
                if inv38.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_maul > 0:
                screen.blit(_scaled_images["materials_plank_wooden_plank"], (934, 530))
                tuple_static_text(user_item_maul, color=(240, 240, 240), position=(911 + 72, 508 + 30), size=15)
                if inv39.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_claymore > 0:
                screen.blit(_scaled_images["materials_component_silver_wire"], (936, 570))
                tuple_static_text(user_item_claymore, color=(240, 240, 240), position=(911 + 72, 557 + 30), size=15)
                if inv40.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_spear > 0:
                screen.blit(_scaled_images["materials_component_bow_string"], (1049, 93))
                tuple_static_text(user_item_spear, color=(240, 240, 240), position=(1049 + 72, 98 + 30), size=15)
                if inv41.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_short_bow > 0:
                screen.blit(_scaled_images["armour_headware_guard_coif"], (1068, 164))
                tuple_static_text(user_item_short_bow, color=(240, 240, 240), position=(1050 + 72, 145 + 30), size=15)
                if inv42.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_longbow > 0:
                screen.blit(_scaled_images["armour_headware_guard_coif"], (1053, 195))
                tuple_static_text(user_item_longbow, color=(240, 240, 240), position=(1053 + 72, 195 + 30), size=15)
                if inv43.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_blunderbuss > 0:
                screen.blit(_scaled_images["armour_headware_guard_coif"], (1050, 248))
                tuple_static_text(user_item_blunderbuss, color=(240, 240, 240), position=(1050 + 72, 248 + 30), size=15)
                if inv44.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_heavy_crossbow > 0:
                screen.blit(_scaled_images["armour_headware_guard_coif"], (1050, 303))
                tuple_static_text(user_item_heavy_crossbow, color=(240, 240, 240), position=(1050 + 72, 303 + 30), size=15)
                if inv45.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_flintlock > 0:
                screen.blit(_scaled_images["armour_headware_guard_coif"], (1051, 352))
                tuple_static_text(user_item_flintlock, color=(240, 240, 240), position=(1051 + 72, 352 + 30), size=15)
                if inv46.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_musket > 0:
                screen.blit(_scaled_images["armour_headware_guard_coif"], (1050, 400))
                tuple_static_text(user_item_musket, color=(240, 240, 240), position=(1050 + 72, 400 + 30), size=15)
                if inv47.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_blue_amulet > 0:
                screen.blit(_scaled_images["armour_headware_guard_coif"], (1049, 455))
                tuple_static_text(user_item_blue_amulet, color=(240, 240, 240), position=(1049 + 72, 455 + 30), size=15)
                if inv48.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_swift_boots > 0:
                screen.blit(_scaled_images["armour_headware_guard_coif"], (1053, 508))
                tuple_static_text(user_item_swift_boots, color=(240, 240, 240), position=(1053 + 72, 508 + 30), size=15)
                if inv49.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if user_item_black_dressed_doll > 0:
                screen.blit(_scaled_images["armour_headware_guard_coif"], (1049, 558))
                tuple_static_text(user_item_black_dressed_doll, color=(240, 240, 240), position=(1049 + 72, 558 + 30), size=15)
                if inv50.collidepoint(mouse_x, mouse_y):
                    for event in events:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            print('1')
            if inv_back.collidepoint(mouse_x, mouse_y):
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        state = "inventory_bag"
            if inv_next.collidepoint(mouse_x, mouse_y):
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        state = "inventory_bag"
        else:
            state = "home"
        tuple_static_text((mouse_x + int(world_x), mouse_y + int(world_y)), color=(255, 255, 255),
                          position=(mouse_x + 5, mouse_y - 20), size=15)
        
        #user_status_bleeding = 0
#        user_status_infection = 0
#    user_status_brokenbones = 0
#    user_status_stun = 0
#    user_status_confusion = 0
#    user_status_blindness = 0
#    user_status_critical = 0
#    user_status_infected = 0
#        
#        user_body = 0
#    user_str = 0
#    user_def = 0
#    user_agi = 0
#    user_mind_resistance
        tick_counter += 1
        if tick_counter >= 500:
            if user_status_bleeding >= 1:
                user_body -= 1
            if user_status_infection >= 1:
                user_body -= 1
                user_status_infection += 1
                if user_status_infection >= 10:
                    user_body -= 1
                    if user_status_infection >= 30:
                        user_body -= 4
                        if user_status_infection >= 40:
                            user_body -= 4
            if user_status_brokenbones >= 1:
                user_agi = user_agi / 2
            if user_status_confusion >= 1:
                user_agi = user_agi / 4
            if user_status_critical >= 1:
                user_def = user_def / 8
            if user_status_infected >= 1:
                user_body -= user_body / 4

            tick_counter = 0
        if user_status_blindness >= 1:
            screen.blit(_preloaded_images["elucidate_middle_gradient_001"], (-638, 0))
            screen.blit(_preloaded_images["elucidate_middle_gradient_001"], (637, 0))
            screen.blit(_rotated_images["elucidate_middle_gradient_001_r"], (0, 355))
            screen.blit(_rotated_images["elucidate_middle_gradient_001_r"], (0, -355))
        mouse()
        display()


elucidate()
