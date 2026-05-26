import importlib, subprocess, sys

libs = ["pygame", "os", "requests", "zipfile", "gdown", "shutil", "random", "time", "json", "psutil"]

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

pygame.init()
screen_x, screen_y = 1275, 710
screen = pygame.display.set_mode((screen_x, screen_y))
pygame.display.set_caption("Elucidate RPG Launcher")
font = pygame.font.SysFont("Times New Roman", 20)

def draw_text(text, x, y):
	surf = font.render(text, True, (255, 255, 255))
	screen.blit(surf, (x, y))
def handle_quit():
	for ev in pygame.event.get():
		if ev.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
def zip_download(url):
	screen.fill((0, 0, 0))
	y_offset = 25
	handle_quit()
	temp_zip = "temp_download.zip"
	temp_extract = "temp_extract"
	draw_text("ZIP package", 5, y_offset)
	draw_text(" | checking files...", 5, y_offset + 20)
	pygame.draw.rect(screen, (160, 0, 0), (0, 0, screen_x, screen_y), 1)
	pygame.display.flip()
	try:
		if os.path.exists(temp_zip):
			os.remove(temp_zip)
		if os.path.exists(temp_extract):
			shutil.rmtree(temp_extract)
		draw_text(" | downloading...", 5, y_offset + 40)
		pygame.display.flip()
		gdown.download(url, temp_zip, quiet=False)
		if not os.path.exists(temp_zip) or os.path.getsize(temp_zip) < 10000:
			draw_text(" | invalid zip file.", 5, y_offset + 60)
			pygame.display.flip()
			return False
		draw_text(" | extracting...", 5, y_offset + 60)
		pygame.display.flip()
		with zipfile.ZipFile(temp_zip, 'r') as zip_ref:
			zip_ref.extractall(temp_extract)
		draw_text(" | replacing files...", 5, y_offset + 80)
		pygame.display.flip()
		for item in os.listdir(temp_extract):
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
			draw_text(f" | replaced: {item}", 5, y_offset + 100)
			pygame.display.flip()
		os.remove(temp_zip)
		shutil.rmtree(temp_extract)
		draw_text(" | done!", 5, y_offset + 120)
		pygame.display.flip()
		return True
	except Exception as e:
		draw_text(" | error occurred.", 5, y_offset + 120)
		draw_text(str(e), 5, y_offset + 140)
		pygame.display.flip()
		return False
def verify(filename, url):
	screen.fill((0, 0, 0))
	headers = {
		"User-Agent": "Mozilla/5.0",
		"Accept": "image/png,image/*;q=0.8,*/*;q=0.5",
		"Connection": "keep-alive"
	}
	y_offset = 25
	handle_quit()
	dirname = os.path.dirname(filename)
	if dirname != "":
		os.makedirs(dirname, exist_ok=True)
	if os.path.exists(filename):
		draw_text(filename, 5, y_offset)
		draw_text(" | file verified.", 5, y_offset + 20)
		pygame.draw.rect(screen, (160, 0, 0), (0, 0, screen_x, screen_y), 1)
	else:
		draw_text(filename, 5, y_offset)
		draw_text(" | file not found...", 5, y_offset + 20)
		draw_text(" | downloading...", 5, y_offset + 40)
		pygame.draw.rect(screen, (160, 0, 0), (0, 0, screen_x, screen_y), 1)
		pygame.display.flip()
		tries = 0
		for attempt in range(30):
			handle_quit()
			try:
				with requests.get(url, headers=headers, stream=True, timeout=10) as r:
					r.raise_for_status()
					with open(filename, "wb") as f:
						for chunk in r.iter_content(1024):
							if chunk:
								f.write(chunk)
				full_path = os.path.abspath(filename)
				draw_text(" | Download successful", 5, y_offset + 60 + (tries * 20))
				draw_text(" | saved at: " + full_path, 5, y_offset + 80 + (tries * 20))
				break
			except Exception:
				tries += 1
				draw_text(" | Download failed... Retrying...", 5, y_offset + 40 + (tries * 20))
			pygame.draw.rect(screen, (160, 0, 0), (0, 0, screen_x, screen_y), 1)
			pygame.display.flip()
			pygame.time.delay(100)
		else:
			draw_text(" | Download Failed...", 5, y_offset + 60 + (tries * 20))
	pygame.draw.rect(screen, (160, 0, 0), (0, 0, screen_x, screen_y), 1)
	pygame.display.flip()

screen.fill((0, 0, 0))
draw_text("Loading...", 5, 5)
pygame.draw.rect(screen, (160, 0, 0), (0, 0, screen_x, screen_y), 1)
pygame.display.flip()

for i in range(1):
	verify("items/materials_special_small_caligo_fragment_tribe.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_special_small_caligo_fragment_tribe.png");
	verify("items/materials_special_small_caligo_fragment_port.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_special_small_caligo_fragment_port.png");
	verify("items/materials_special_big_caligo_fragment.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_special_big_caligo_fragmrnt.png");
	verify("items/weapon_1handed_short_sword.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/weapon_1handed_short_sword.png");
	verify("items/weapon_1handed_cleaver.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/weapon_1handed_cleaver.png");
	verify("items/weapon_1handed_knife.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/weapon_1handed_knife.png");
	verify("items/materials_sheet_ancient_paper.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_sheet_ancient_paper.png");
	verify("items/armour_headware_iron_mask.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/armour_headware_iron_mask.png");
	verify("items/armour_body_armour_dark_priests_robe.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/armour_body_armour_dark_priests_robe.png");
	verify("items/armour_body_armour_priests_robe.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/armour_body_armour_priests_robe.png");
	verify("items/armour_headware_plate_helmet.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/armour_headware_plate_helmet.png");
	verify("items/armour_headware_padded_cap.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/armour_headware_padded_cap.png");
	verify("items/armour_body_armour_iron_cuirass.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/armour_body_armour_iron_cuirass.png");
	verify("items/armour_body_armour_loincloth.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/armour_body_armour_loincloth.png");
	verify("items/armour_accessories_red_scarf.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/armour_accessories_red_scarf.png");
	verify("items/armour_headware_iron_helmet.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/armour_headware_iron_helmet.png");
	verify("items/armour_headware_guard_bascinet.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/armour_headware_guard_bascinet.png");
	verify("items/armour_headware_guard_coif.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/armour_headware_guard_coif.png");
	verify("items/armour_headware_chainmail_hood.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/armour_headware_chainmail_hood.png");
	verify("items/armour_body_armour_black_dress.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/armour_body_armour_black_dress.png");
	verify("items/armour_body_armour_trench_coat.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/armour_body_armour_trench_coat.png");
	verify("items/weapon_1handed_corsairs_saber.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/weapon_1handed_corsairs_saber.png");
	verify("items/weapon_1handed_cloth_hood.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/weapon_1handed_cloth_hood.png");
	verify("items/armour_body_armour_leather_coat.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/armour_body_armour_leather_coat.png");
	verify("items/armour_body_armour_leather_vest.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/armour_body_armour_leather_jvest.png");
	verify("items/armour_body_armour_plated_mail.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/armour_body_armour_plated_mail.png");
	verify("items/armour_shield_scutum.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/armour_shield_scutum.png");
	verify("items/weapon_longrange_musket.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/weapon_longrange_musket.png");
	verify("items/weapon_2handed_spear.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/weapon_2handed_spear.png");
	verify("items/armour_body_armour_hard_leather_armor.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/armour_body_armour_hard_leather_armor.png");
	verify("items/armour_body_armour_iron_plate.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/armour_body_armour_iron_plate.png");
	verify("items/weapon_1handed_stiletto.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/weapon_1handed_stiletto.png");
	verify("items/armour_armwear_arm_guard.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/armour_armwear_arm_guard.png");
	verify("items/weapon_1handed_iron_axe.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/weapon_1handed_iron_axe.png");
	verify("items/weapon_longrange_short_bow.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/weapon_longrange_short_bow.png");
	verify("items/materials_scrap_leather_scraps.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_scrap_leather_scraps.png");
	verify("items/materials_skill_book_of_rapid_fire.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_skill_book_of_rapid_fire.png");
	verify("items/materials_skill_book_of_instincts.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_skill_book_of_instincts.png");
	verify("items/armour_accessories_swift_boots.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/armour_accessories_swift_boots.png");
	verify("items/weapon_longrange_heavy_crossbow.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/weapon_longrange_heavy_crossbow.png");
	verify("items/weapon_longrange_longbow.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/weapon_longrange_longbow.png");
	verify("items/weapon_2handed_maul.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/weapon_2handed_maul.png");
	verify("items/weapon_2handed_claymore.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/weapon_2handed_claymore.png");
	verify("items/weapon_1handed_scimitar.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/weapon_1handed_scimitar.png");
	verify("items/weapon_1handed_improvised_shiv.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/weapon_1handed_improvised_shiv.png");
	verify("items/weapon_1handed_steel_hammer.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/weapon_1handed_steel_hammer.png");
	verify("items/material_toy_black_dressed_doll.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/material_toy_black_dressed_doll.png");
	verify("items/weapon_1handed_dirk.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/weapon_1handed_dirk.png");
	verify("items/materials_plank_wooden_plank.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_plank_wooden_plank.png");
	verify("items/weapon_1handed_dagger.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/weapon_1handed_dagger.png");
	verify("items/materials_component_silver_wire.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_component_silver_wire.png");
	verify("items/armour_accessories_red_amulet.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/armour_accessories_red_amulet.png");
	verify("items/armour_accessories_blue_amulet.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/armour_accessories_blue_amulet.png");
	verify("items/materials_component_stick.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_component_stick.png");
	verify("items/armour_accessories_ring.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/armour_accessories_ring.png");
	verify("items/materials_skill_book_of_marksmanship.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_skill_book_of_marksmanship.png");
	verify("items/materials_skill_book_of_stars.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_skill_book_of_stars.png");
	verify("items/materials_skill_book_of_crafsmanship.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_skill_book_of_crafsmanship.png");
	verify("items/materials_skill_book_of_agility.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_skill_book_of_agility.png");
	verify("items/materials_skill_book_of_healing.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_skill_book_of_healing.png");
	verify("items/materials_skill_book_of_the_secrets.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_skill_book_of_the_secrets.png");
	verify("items/materials_save_book_of_enlightenment.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_save_book_of_enlightenment.png");
	verify("items/materials_skill_book_of_cowardice_i.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_skill_book_of_cowardice_i.png");
	verify("items/materials_skill_book_of_cowardice_ii.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_skill_book_of_cowardice_ii.png");
	verify("items/materials_skill_book_of_pestilence_i.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_skill_book_of_pestilence_i.png");
	verify("items/materials_skill_book_of_pestilence_ii.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_skill_book_of_pestilence_ii.png");
	verify("items/materials_skill_book_of_pestilence_iii.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_skill_book_of_pestilence_iii.png");
	verify("items/materials_skill_book_of_pestilence_iv.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_skill_book_of_pestilence_iv.png");
	verify("items/materials_skill_book_of_pestilence_v.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_skill_book_of_pestilence_v.png");
	verify("items/materials_skill_book_of_pestilence_vi.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_skill_book_of_pestilence_vi.png");
	verify("items/materials_skill_book_of_pestilence_vii.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_skill_book_of_pestilence_vii.png");
	verify("items/materials_skill_book_of_pestilence_viii.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_skill_book_of_pestilence_viii.png");
	verify("items/materials_skill_book_of_trade_i.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_skill_book_of_trade_i.png");
	verify("items/materials_skill_book_of_trade_ii.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_skill_book_of_trade_ii.png");
	verify("items/materials_skill_book_of_trade_iii.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_skill_book_of_trade_iii.png");
	verify("items/materials_gem_red_gem.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_gem_red_gem.png");
	verify("items/materials_gem_blue_gem.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_gem_blue_gem.png");
	verify("items/materials_beverage_ale.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_beverage_ale.png");
	verify("items/materials_beverage_wine.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_beverage_wine.png");
	verify("items/materials_beverage_rum.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_beverage_rum.png");
	verify("items/materials_bar_iron_ingot.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_bar_iron_ingot.png");
	verify("items/materials_ore_raw_iron.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_ore_raw_iron.png");
	verify("items/materials_foliage_blue_herb-1.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_foliage_blue_herb-1.png");
	verify("items/materials_foliage_green_herb.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_foliage_green_herb.png");
	verify("items/materials_sheet_paper.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_sheet_paper.png");
	verify("items/materials_potion_antibiotics.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_potion_antibiotics.png");
	verify("items/materials_potion_betadine.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_potion_betadine.png");
	verify("items/materials_potion_red_vial.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_potion_red_vial.png");
	verify("items/materials_container_empty_vial.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_container_empty_vial.png");
	verify("items/weapon_2handed_longsword.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/weapon_2handed_longsword.png");
	verify("items/armour_shield_wooden_buckler.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/armour_shield_wooden_buckler.png");
	verify("items/weapon_1handed_cultist_dagger.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/weapon_1handed_cultist_dagger.png");
	verify("items/weapon_longrange_flintlock.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/weapon_longrange_flintlock.png");
	verify("items/weapon_2handed_makeshift_spear.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/weapon_2handed_makeshift_spear.png");
	verify("items/weapon_longrange_blunderbuss.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/weapon_longrange_blunderbuss.png");
	verify("items/weapon_1handed_shaman_dagger.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/weapon_1handed_shaman_dagger.png");
	verify("items/weapon_2handed_priest_staff.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/weapon_2handed_priest_staff.png");
	verify("items/weapon_longrange_cultist_crossbow.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/weapon_longrange_cultist_crossbow.png");
	verify("items/materials_component_bow_string.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/materials_component_bow_string.png");
	verify("maps/l_o_outer_gate_district.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Outer-Gate-District.png");
	verify("maps/l_i_inside_the_wall.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Inside-The-Wall.png");
	verify("maps/l_o_inner_military_district.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Inner-Military-Disctrict.png");
	verify("maps/l_i_church_chapel.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/CHURCH-CHAPEL.png");
	verify("maps/l_i_barracks_hall.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/BARRACKS-HALL.png");
	verify("maps/l_o_church_outpost.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Church-Outpost.png");
	verify("maps/l_i_orphanage_access.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Orphanage-Access-1.png");
	verify("maps/l_i_theocratic_battleground_endingb.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Theocratic-Battleground-Ending-B.png");
	verify("maps/l_i_main_cathedral.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Main-Cathedral.png");
	verify("maps/l_o_destroy_theocracy.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Destroy-Theoracy.png");
	verify("maps/l_i_church_administrative_wing.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Church-Administrative-Wing.png");
	verify("maps/l_o_cathedral_plaza.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Cathedral-Plaza.png");
	verify("maps/l_o_rare_nexus_points.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Rare-Nexus-Points-Zone-of-Terror.png");
	verify("maps/f_o_deep_terror_zone.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Deep-Terror-Zone.png");
	verify("maps/l_o_corrupted_frontier.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Corrupted-Frontier.png");
	verify("maps/t_o_anomaly_forest.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Anomaly-Forest.png");
	verify("maps/l_i_lab_office_under_administrative_wing.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Lab-Office-Under-Church-Administrative-WIng.png");
	verify("maps/l_i_active_laboratory_under_administrative_wing.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Active-Laboratory-Under-Church-Administrative-WIng.png");
	verify("maps/l_i_subterranean_labyrinth_exit.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Subterranean-Labyrithn-Exit.png");
	verify("maps/l_i_subterranean_labyrinth.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Subterranean-Labyrithn-Slowed-Movements-Connected-to-New-Laboratory-Theocratic-Capital.png");
	verify("maps/l_i_old_laboratory.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Old-Laboratory.png");
	verify("maps/l_i_tutorial_ground.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Tutorial-Ground.png");
	verify("maps/t_o_tutorial_ground_shaman.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Tutorial-Ground-Shaman-DLC.png");
	verify("maps/l_i_tutorial_ground_dlc.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Tutorial-Ground-DLC.png");
	verify("maps/l_i_tutorial_ground_first_version.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/First-Version.png");
	verify("maps/t_i_escape_route.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Excape-Route.png");
	verify("maps/t_o_destroyed_tribe_settlement.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Destroyed-Tribe-Settlement.png");
	verify("maps/t_o_tribe_settlement.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Tribe-Settlement.png");
	verify("maps/t_o_tribe_perimeter.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Tribe-Perimeter.png");
	verify("maps/t_i_storage_cave.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Storage-Cave.png");
	verify("maps/t_i_healing_hut.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Healing-Hut.png");
	verify("maps/l_i_headmaster_office.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Headmaster-Office.png");
	verify("maps/l_i_the_play_room.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/The-Play-Room.png");
	verify("maps/l_o_the_old_orphanage.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/The-Old-Orphanage.png");
	verify("maps/l_o_home_village_entry.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Home-Village-Entry.png");
	verify("maps/l_o_home_village_center.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Home-Village-Center.png");
	verify("maps/l_i_chief_home.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Chief_s-Home.png");
	verify("maps/f_o_village_market.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Village-Market-Village-Outskirts.png");
	verify("maps/f_i_tunnel_passage_to_tribe.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Tunnel-Passage-to-Tribe.png");
	verify("maps/f_o_residential_area.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Residential-Area-Village-Outskirts.png");
	verify("maps/f_i_inside_chief_home.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Int.-Chief_s-Home.png");
	verify("maps/f_o_outside_chief_home.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Ext.-Chief_s-Home.png");
	verify("maps/f_i_inside_elder_house.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Elder-House-Int.png");
	verify("maps/c_o_lowms_cultist_battleground.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Low-MS-Cultist-Battleground.png");
	verify("maps/c_i_inner_sanctum.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Inner-Sanctum-Cult.png");
	verify("maps/c_o_cultist_battleground.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Cultist-Battleground.png");
	verify("maps/c_o_cult_village.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Cult-VIllage.png");
	verify("maps/c_i_cult_leader_fortress.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Cult-Leader-Fortress.png");
	verify("maps/c_o_cult_funeris_encounter.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Cult-Funeris-Encounter-CULTIST-SPAWN.png");
	verify("maps/c_o_coastal_landing.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Coastal-Landing.png");
	verify("maps/l_i_merchant_bank.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Merchant-Bank.png");
	verify("maps/l_i_the_ship.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/The-Ship-Transitioning.png");
	verify("maps/l_i_ship_lower_part.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Ship-Lower-Part-DLC-EXCLUSIVE.png");
	verify("maps/l_i_merchant_tavern.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Merchant-Tavern.png");
	verify("maps/l_o_merchant_quarter.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Merchant-Quarter.png");
	verify("maps/l_i_merchant_guild_hall.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Merchant-Guild-Hall.png");
	verify("maps/l_i_lumen_spy_merchant_guild.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Lumen-Spy-Merchant-Guild-DLC-EXCLUSIVE-.png");
	verify("maps/l_o_harbor_district.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Harbor-District.png");
	verify("maps/l_i_clearance_office.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/2-Clearance-Office.png");
	verify("maps/l_i_customs_office.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/1-Customs-Office.png");
	verify("sprites/npc_e_cult_leader/elucidate_idle_cult_leader_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_cult_leader_npc_down.png")
	verify("sprites/npc_e_cult_leader/elucidate_idle_cult_leader_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_cult_leader_npc_up.png")
	verify("sprites/npc_e_cult_leader/elucidate_idle_cult_leader_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_cult_leader_npc_left.png")
	verify("sprites/npc_e_cult_leader/elucidate_idle_cult_leader_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_cult_leader_npc_right.png")
	verify("sprites/npc_e_cult_soldier/elucidate_idle_cultist_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_cultist_npc_up.png")
	verify("sprites/npc_e_cult_soldier/elucidate_idle_cultist_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_cultist_npc_right.png")
	verify("sprites/npc_e_cult_soldier/elucidate_idle_cultist_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_cultist_npc_left.png")
	verify("sprites/npc_e_cult_soldier/elucidate_idle_cultist_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_cultist_npc_down.png")
	verify("sprites/npc_e_s1_corrupted_cultist/elucidate_idle_corrupted1_cultist_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_corrupted1_cultist_npc_right.png")
	verify("sprites/npc_e_s1_corrupted_cultist/elucidate_idle_corrupted1_cultist_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_corrupted1_cultist_npc_left.png")
	verify("sprites/npc_e_s1_corrupted_cultist/elucidate_idle_corrupted1_cultist_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_corrupted1_cultist_npc_down.png")
	verify("sprites/npc_e_s1_corrupted_cultist/elucidate_idle_corrupted1_cultist_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_corrupted1_cultist_npc_up.png")
	verify("sprites/npc_e_amalgamated_villagers/elucidate_idle_amalgamated_villagers_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_amalgamated_villagers_npc_right.png")
	verify("sprites/npc_e_amalgamated_villagers/elucidate_idle_amalgamated_villagers_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_amalgamated_villagers_npc_left.png")
	verify("sprites/npc_e_amalgamated_knights/elucidate_idle_amalgamated_knights_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_amalgamated_knights_npc_right.png")
	verify("sprites/npc_e_amalgamated_knights/elucidate_idle_amalgamated_knights_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_amalgamated_knights_npc_left.png")
	verify("sprites/npc_e_amalgamated_civilians/elucidate_idle_amalgamated_civillians_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_amalgamated_civillians_npc_right.png")
	verify("sprites/npc_e_amalgamated_civilians/elucidate_idle_amalgamated_civillians_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_amalgamated_civillians_npc_left.png")
	verify("sprites/npc_e_melted_villager_male/elucidate_idle_melted_male_villager_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_melted_male_villager_npc_right.png")
	verify("sprites/npc_e_melted_villager_male/elucidate_idle_melted_male_villager_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_melted_male_villager_npc_left.png")
	verify("sprites/npc_e_melted_villager_male/elucidate_idle_melted_male_villager_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_melted_male_villager_npc_up.png")
	verify("sprites/npc_e_melted_villager_male/elucidate_idle_melted_male_villager_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_melted_male_villager_npc_down.png")
	verify("sprites/npc_e_melted_villager_female/elucidate_idle_melted_female_villager_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_melted_female_villager_npc_up.png")
	verify("sprites/npc_e_melted_villager_female/elucidate_idle_melted_female_villager_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_melted_female_villager_npc_right.png")
	verify("sprites/npc_e_melted_villager_female/elucidate_idle_melted_female_villager_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_melted_female_villager_npc_left.png")
	verify("sprites/npc_e_melted_villager_female/elucidate_idle_melted_female_villager_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_melted_female_villager_npc_down.png")
	verify("sprites/npc_e_s3_corrupted_cultist/elucidate_idle_corrupted3_cultist_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_corrupted3_cultist_npc_up.png")
	verify("sprites/npc_e_s3_corrupted_cultist/elucidate_idle_corrupted3_cultist_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_corrupted3_cultist_npc_right.png")
	verify("sprites/npc_e_s3_corrupted_cultist/elucidate_idle_corrupted3_cultist_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_corrupted3_cultist_npc_left.png")
	verify("sprites/npc_e_s3_corrupted_cultist/elucidate_idle_corrupted3_cultist_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_corrupted3_cultist_npc_down.png")
	verify("sprites/npc_e_s2_corrupted_cultist/elucidate_idle_corrupted2_cultist_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_corrupted3_cultist_npc_up.png")
	verify("sprites/npc_e_s2_corrupted_cultist/elucidate_idle_corrupted2_cultist_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_corrupted3_cultist_npc_right.png")
	verify("sprites/npc_e_s2_corrupted_cultist/elucidate_idle_corrupted2_cultist_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_corrupted3_cultist_npc_left.png")
	verify("sprites/npc_e_s2_corrupted_cultist/elucidate_idle_corrupted2_cultist_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_corrupted3_cultist_npc_down.png")
	verify("sprites/npc_n_librarian_scholar/elucidate_idle_librarian_scholar_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_librarian_scholar_npc_up.png")
	verify("sprites/npc_n_librarian_scholar/elucidate_idle_librarian_scholar_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_librarian_scholar_npc_right.png")
	verify("sprites/npc_n_librarian_scholar/elucidate_idle_librarian_scholar_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_librarian_scholar_npc_left.png")
	verify("sprites/npc_n_librarian_scholar/elucidate_idle_librarian_scholar_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_librarian_scholar_npc_down.png")
	verify("sprites/npc_e_luminarian_knight/elucidate_idle_holyknight_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_holyknight_npc_up.png")
	verify("sprites/npc_e_luminarian_knight/elucidate_idle_holyknight_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_holyknight_npc_right.png")
	verify("sprites/npc_e_luminarian_knight/elucidate_idle_holyknight_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_holyknight_npc_left.png")
	verify("sprites/npc_e_luminarian_knight/elucidate_idle_holyknight_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_holyknight_npc_down.png")
	verify("sprites/npc_n_faithful_luminarian/elucidate_idle_male_faithful_citizen_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_male_faithful_citizen_npc_up.png")
	verify("sprites/npc_n_faithful_luminarian/elucidate_idle_male_faithful_citizen_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_male_faithful_citizen_npc_right.png")
	verify("sprites/npc_n_faithful_luminarian/elucidate_idle_male_faithful_citizen_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_male_faithful_citizen_npc_left.png")
	verify("sprites/npc_n_faithful_luminarian/elucidate_idle_male_faithful_citizen_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_male_faithful_citizen_npc_down.png")
	verify("sprites/npc_n_faithful_luminarie/elucidate_idle_female_faithful_citizen_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_female_faithful_citizen_npc_up.png")
	verify("sprites/npc_n_faithful_luminarie/elucidate_idle_female_faithful_citizen_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_female_faithful_citizen_npc_right.png")
	verify("sprites/npc_n_faithful_luminarie/elucidate_idle_female_faithful_citizen_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_female_faithful_citizen_npc_left.png")
	verify("sprites/npc_n_faithful_luminarie/elucidate_idle_female_faithful_citizen_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_female_faithful_citizen_npc_down.png")
	verify("sprites/npc_n_luminarian_priest/elucidate_idle_sprite_chuAttendants_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_sprite_chuAttendants_up.png")
	verify("sprites/npc_n_luminarian_priest/elucidate_idle_sprite_chuAttendants_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_sprite_chuAttendants_right.png")
	verify("sprites/npc_n_luminarian_priest/elucidate_idle_sprite_chuAttendants_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_sprite_chuAttendants_left.png")
	verify("sprites/npc_n_luminarian_priest/elucidate_idle_sprite_chuAttendants_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_sprite_chuAttendants_down.png")
	verify("sprites/npc_e_lunar_assasin/elucidate_idle_assassin_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_assassin_npc_up.png")
	verify("sprites/npc_e_lunar_assasin/elucidate_idle_assassin_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_assassin_npc_right.png")
	verify("sprites/npc_e_lunar_assasin/elucidate_idle_assassin_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_assassin_npc_left.png")
	verify("sprites/npc_e_lunar_assasin/elucidate_idle_assassin_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_assassin_npc_down.png")
	verify("sprites/npc_n_seekers_warrior_male/elucidate_idle_tribe_warrior_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_tribe_warrior_npc_up.png")
	verify("sprites/npc_n_seekers_warrior_male/elucidate_idle_tribe_warrior_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_tribe_warrior_npc_right.png")
	verify("sprites/npc_n_seekers_warrior_male/elucidate_idle_tribe_warrior_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_tribe_warrior_npc_left.png")
	verify("sprites/npc_n_seekers_warrior_male/elucidate_idle_tribe_warrior_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_tribe_warrior_npc_down.png")
	verify("sprites/npc_n_seekers_elder/elucidate_idle_tribe_elder_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_tribe_elder_npc_up.png")
	verify("sprites/npc_n_seekers_elder/elucidate_idle_tribe_elder_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_tribe_elder_npc_right.png")
	verify("sprites/npc_n_seekers_elder/elucidate_idle_tribe_elder_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_tribe_elder_npc_left.png")
	verify("sprites/npc_n_seekers_elder/elucidate_idle_tribe_elder_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_tribe_elder_npc_down.png")
	verify("sprites/npc_n_seekers_chieftain/elucidate_idle_tribe_chief_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_tribe_chief_npc_up.png")
	verify("sprites/npc_n_seekers_chieftain/elucidate_idle_tribe_chief_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_tribe_chief_npc_right.png")
	verify("sprites/npc_n_seekers_chieftain/elucidate_idle_tribe_chief_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_tribe_chief_npc_left.png")
	verify("sprites/npc_n_seekers_chieftain/elucidate_idle_tribe_chief_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_tribe_chief_npc_down.png")
	verify("sprites/npc_n_traveling_merchant/elucidate_idle_supply_merchant_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_supply_merchant_npc_down.png")
	verify("sprites/npc_n_traveling_merchant/elucidate_idle_supply_merchant_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_supply_merchant_npc_up.png")
	verify("sprites/npc_n_traveling_merchant/elucidate_idle_supply_merchant_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_supply_merchant_npc_right.png")
	verify("sprites/npc_n_traveling_merchant/elucidate_idle_supply_merchant_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_supply_merchant_npc_left.png")
	verify("sprites/npc_n_merchant_guild_member/elucidate_idle_merchant_guild_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_merchant_guild_npc_up.png")
	verify("sprites/npc_n_merchant_guild_member/elucidate_idle_merchant_guild_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_merchant_guild_npc_right.png")
	verify("sprites/npc_n_merchant_guild_member/elucidate_idle_merchant_guild_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_merchant_guild_npc_left.png")
	verify("sprites/npc_n_merchant_guild_member/elucidate_idle_merchant_guild_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_merchant_guild_npc_down.png")
	verify("sprites/npc_n_merchant_guild_director/elucidate_idle_merchant_guild_master_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_merchant_guild_master_npc_up.png")
	verify("sprites/npc_n_merchant_guild_director/elucidate_idle_merchant_guild_master_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_merchant_guild_master_npc_right.png")
	verify("sprites/npc_n_merchant_guild_director/elucidate_idle_merchant_guild_master_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_merchant_guild_master_npc_left.png")
	verify("sprites/npc_n_merchant_guild_director/elucidate_idle_merchant_guild_master_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_merchant_guild_master_npc_down.png")
	verify("sprites/npc_n_harbor_captain/elucidate_idle_harbor_captain_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_harbor_captain_npc_up.png")
	verify("sprites/npc_n_harbor_captain/elucidate_idle_harbor_captain_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_harbor_captain_npc_right.png")
	verify("sprites/npc_n_harbor_captain/elucidate_idle_harbor_captain_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_harbor_captain_npc_left.png")
	verify("sprites/npc_n_harbor_captain/elucidate_idle_harbor_captain_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_harbor_captain_npc_down.png")
	verify("sprites/npc_n_s2_outskirts_villagers/elucidate_idle_male_villager_variant_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_male_villager_variant_npc_up.png")
	verify("sprites/npc_n_s2_outskirts_villagers/elucidate_idle_male_villager_variant_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_male_villager_variant_npc_right.png")
	verify("sprites/npc_n_s2_outskirts_villagers/elucidate_idle_male_villager_variant_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_male_villager_variant_npc_left.png")
	verify("sprites/npc_n_s2_outskirts_villagers/elucidate_idle_male_villager_variant_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_male_villager_variant_npc_down.png")
	verify("sprites/npc_n_s1_outskirts_villagers/elucidate_idle_male_villager_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_male_villager_npc_up.png")
	verify("sprites/npc_n_s1_outskirts_villagers/elucidate_idle_male_villager_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_male_villager_npc_right.png")
	verify("sprites/npc_n_s1_outskirts_villagers/elucidate_idle_male_villager_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_male_villager_npc_left.png")
	verify("sprites/npc_n_s1_outskirts_villagers/elucidate_idle_male_villager_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_male_villager_npc_down.png")
	verify("sprites/npc_n_s2_outskirts_villagers/elucidate_idle_female_villager_variant_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_female_villager_variant_npc_up.png")
	verify("sprites/npc_n_s2_outskirts_villagers/elucidate_idle_female_villager_variant_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_female_villager_variant_npc_right.png")
	verify("sprites/npc_n_s2_outskirts_villagers/elucidate_idle_female_villager_variant_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_female_villager_variant_npc_left.png")
	verify("sprites/npc_n_s2_outskirts_villagers/elucidate_idle_female_villager_variant_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_female_villager_variant_npc_down.png")
	verify("sprites/npc_n_s1_outskirts_villagers/elucidate_idle_female_villager_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_female_villager_npc_up.png")
	verify("sprites/npc_n_s1_outskirts_villagers/elucidate_idle_female_villager_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_female_villager_npc_right.png")
	verify("sprites/npc_n_s1_outskirts_villagers/elucidate_idle_female_villager_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_female_villager_npc_left.png")
	verify("sprites/npc_n_s1_outskirts_villagers/elucidate_idle_female_villager_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_female_villager_npc_down.png")
	verify("sprites/npc_n_guards/elucidate_idle_guards_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_guards_npc_up.png")
	verify("sprites/npc_n_guards/elucidate_idle_guards_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_guards_npc_right.png")
	verify("sprites/npc_n_guards/elucidate_idle_guards_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_guards_npc_left.png")
	verify("sprites/npc_n_guards/elucidate_idle_guards_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_guards_npc_down.png")
	verify("sprites/npc_n_guard_captain/elucidate_idle_guard_captain_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_guard_captain_npc_up.png")
	verify("sprites/npc_n_guard_captain/elucidate_idle_guard_captain_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_guard_captain_npc_right.png")
	verify("sprites/npc_n_guard_captain/elucidate_idle_guard_captain_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_guard_captain_npc_left.png")
	verify("sprites/npc_n_guard_captain/elucidate_idle_guard_captain_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_guard_captain_npc_down.png")
	verify("sprites/npc_n_draft_officer/elucidate_idle_draft_officer_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_draft_officer_npc_up.png")
	verify("sprites/npc_n_draft_officer/elucidate_idle_draft_officer_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_draft_officer_npc_right.png")
	verify("sprites/npc_n_draft_officer/elucidate_idle_draft_officer_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_draft_officer_npc_left.png")
	verify("sprites/npc_n_draft_officer/elucidate_idle_draft_officer_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_draft_officer_npc_down.png")
	verify("sprites/npc_n_s1_walled_city_civilians_male/elucidate_idle_male_civilian_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_male_civilian_npc_up.png")
	verify("sprites/npc_n_s1_walled_city_civilians_male/elucidate_idle_male_civilian_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_male_civilian_npc_right.png")
	verify("sprites/npc_n_s1_walled_city_civilians_male/elucidate_idle_male_civilian_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_male_civilian_npc_left.png")
	verify("sprites/npc_n_s1_walled_city_civilians_male/elucidate_idle_male_civilian_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_male_civilian_npc_down.png")
	verify("sprites/npc_n_s1_walled_city_civilians_female/elucidate_idle_female_civilian_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_female_civilian_npc_up.png")
	verify("sprites/npc_n_s1_walled_city_civilians_female/elucidate_idle_female_civilian_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_female_civilian_npc_right.png")
	verify("sprites/npc_n_s1_walled_city_civilians_female/elucidate_idle_female_civilian_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_female_civilian_npc_left.png")
	verify("sprites/npc_n_s1_walled_city_civilians_female/elucidate_idle_female_civilian_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_female_civilian_npc_down.png")
	verify("sprites/npc_n_blacksmith_conrad/elucidate_idle_blacksmith_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_blacksmith_npc_up.png")
	verify("sprites/npc_n_blacksmith_conrad/elucidate_idle_blacksmith_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_blacksmith_npc_right.png")
	verify("sprites/npc_n_blacksmith_conrad/elucidate_idle_blacksmith_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_blacksmith_npc_left.png")
	verify("sprites/npc_n_blacksmith_conrad/elucidate_idle_blacksmith_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_blacksmith_npc_down.png")
	verify("sprites/player_shaman/elucidate_sprite_shaman_left_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_shaman_left_001.png")
	verify("sprites/player_shaman/elucidate_sprite_shaman_left_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_shaman_left_002.png")
	verify("sprites/player_shaman/elucidate_sprite_shaman_left_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_shaman_left_003.png")
	verify("sprites/player_shaman/elucidate_attack_shaman_left_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_attack_shaman_left_001.png")
	verify("sprites/player_shaman/elucidate_attack_shaman_left_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_attack_shaman_left_002.png")
	verify("sprites/player_shaman/elucidate_sprite_shaman_down_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_shaman_down_002-1.png")
	verify("sprites/player_shaman/elucidate_sprite_shaman_down_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_shaman_down_001.png")
	verify("sprites/player_shaman/elucidate_sprite_shaman_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_shaman_down_002.png")
	verify("sprites/player_shaman/elucidate_attack_shaman_down_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_attack_shaman_down_001.png")
	verify("sprites/player_shaman/elucidate_attack_shaman_down_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_attack_shaman_down_002.png")
	verify("sprites/player_shaman/elucidate_sprite_shaman_up_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_shaman_up_002.png")
	verify("sprites/player_shaman/elucidate_sprite_shaman_up_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_shaman_up_001-1.png")
	verify("sprites/player_shaman/elucidate_sprite_shaman_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_shaman_up_001.png")
	verify("sprites/player_shaman/elucidate_attack_shaman_up_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_attack_shaman_up_001.png")
	verify("sprites/player_shaman/elucidate_attack_shaman_up_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_attack_shaman_up_002.png")
	verify("sprites/player_shaman/elucidate_sprite_shaman_right_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_shaman_right_002.png")
	verify("sprites/player_shaman/elucidate_sprite_shaman_right_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_shaman_right_001.png")
	verify("sprites/player_shaman/elucidate_sprite_shaman_right_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_shaman_right_004.png")
	verify("sprites/player_shaman/elucidate_attack_shaman_right_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_attack_shaman_right_001.png")
	verify("sprites/player_shaman/elucidate_attack_shaman_right_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_attack_shaman_right_002.png")
	verify("sprites/player_merchant/elucidate_sprite_merchant_up_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_merchant_up_002.png")
	verify("sprites/player_merchant/elucidate_sprite_merchant_up_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_merchant_up_001-1.png")
	verify("sprites/player_merchant/elucidate_sprite_merchant_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_merchant_up_001.png")
	verify("sprites/player_merchant/elucidate_attack_merchant_up_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_attack_merchant_up_001.png")
	verify("sprites/player_merchant/elucidate_attack_merchant_up_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_attack_merchant_up_002.png")
	verify("sprites/player_merchant/elucidate_sprite_merchant_right_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_merchant_right_002.png")
	verify("sprites/player_merchant/elucidate_sprite_merchant_right_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_merchant_right_001.png")
	verify("sprites/player_merchant/elucidate_sprite_merchant_right_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_merchant_right_004.png")
	verify("sprites/player_merchant/elucidate_attack_merchant_right_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_attack_merchant_right_001.png")
	verify("sprites/player_merchant/elucidate_attack_merchant_right_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_attack_merchant_right_002.png")
	verify("sprites/player_merchant/elucidate_sprite_merchant_left_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_merchant_left_002.png")
	verify("sprites/player_merchant/elucidate_sprite_merchant_left_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_merchant_left_001.png")
	verify("sprites/player_merchant/elucidate_sprite_merchant_left_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_merchant_left_003.png")
	verify("sprites/player_merchant/elucidate_attack_merchant_left_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_attack_merchant_left_001.png")
	verify("sprites/player_merchant/elucidate_attack_merchant_left_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_attack_merchant_left_002.png")
	verify("sprites/player_merchant/elucidate_sprite_merchant_down_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_merchant_down_002.png")
	verify("sprites/player_merchant/elucidate_sprite_merchant_down_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_merchant_down_001.png")
	verify("sprites/player_merchant/elucidate_sprite_merchant_down_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_merchant_down_002.png")
	verify("sprites/player_merchant/elucidate_attack_merchant_down_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_attack_merchant_down_001.png")
	verify("sprites/player_merchant/elucidate_attack_merchant_down_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_attack_merchant_down_002.png")
	verify("sprites/player_priest/elucidate_sprite_priest_left_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_priest_left_002.png")
	verify("sprites/player_priest/elucidate_sprite_priest_left_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_priest_left_001.png")
	verify("sprites/player_priest/elucidate_sprite_priest_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_priest_left.png")
	verify("sprites/player_priest/elucidate_attack_priest_left_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_attack_priest_left_001.png")
	verify("sprites/player_priest/elucidate_attack_priest_left_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_attack_priest_left_002.png")
	verify("sprites/player_priest/elucidate_sprite_priest_down_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_priest_down_002.png")
	verify("sprites/player_priest/elucidate_sprite_priest_down_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_priest_down_001-1.png")
	verify("sprites/player_priest/elucidate_sprite_priest_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_priest_down.png")
	verify("sprites/player_priest/elucidate_attack_priest_down_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_attack_priest_down_001.png")
	verify("sprites/player_priest/elucidate_attack_priest_down_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_attack_priest_down_002.png")
	verify("sprites/player_priest/elucidate_sprite_priest_up_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_priest_up_002.png")
	verify("sprites/player_priest/elucidate_sprite_priest_up_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_priest_up_001-1.png")
	verify("sprites/player_priest/elucidate_sprite_priest_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_priest_up.png")
	verify("sprites/player_priest/elucidate_attack_priest_up_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_attack_priest_up_001.png")
	verify("sprites/player_priest/elucidate_attack_priest_up_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_attack_priest_up_002.png")
	verify("sprites/player_priest/elucidate_sprite_priest_right_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_priest_right_002.png")
	verify("sprites/player_priest/elucidate_sprite_priest_right_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_priest_right_001.png")
	verify("sprites/player_priest/elucidate_sprite_priest_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_priest_right.png")
	verify("sprites/player_priest/elucidate_attack_priest_right_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_attack_priest_right_001.png")
	verify("sprites/player_priest/elucidate_attack_priest_right_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_attack_priest_right_002.png")
	verify("sprites/player_cultist/elucidate_walking_sprite_cultist_down_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walking_sprite_cultist_down_002.png")
	verify("sprites/player_cultist/elucidate_walking_sprite_cultist_down_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walking_sprite_cultist_down_001.png")
	verify("sprites/player_cultist/elucidate_sprite_cultist_down_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_sprite_cultist_down_002.png")
	verify("sprites/player_cultist/elucidate_attack_cultist_down_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_attack_cultist_down_001.png")
	verify("sprites/player_cultist/elucidate_attack_cultist_down_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_attack_cultist_down_002.png")
	verify("sprites/player_cultist/elucidate_walking_sprite_cultist_up_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walking_sprite_cultist_up_002.png")
	verify("sprites/player_cultist/elucidate_walking_sprite_cultist_up_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walking_sprite_cultist_up_001.png")
	verify("sprites/player_cultist/elucidate_sprite_cultist_up_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_sprite_cultist_up_001.png")
	verify("sprites/player_cultist/elucidate_attack_cultist_up_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_attack_cultist_up_001.png")
	verify("sprites/player_cultist/elucidate_attack_cultist_up_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_attack_cultist_up_002.png")
	verify("sprites/player_cultist/elucidate_walking_sprite_cultist_right_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walking_sprite_cultist_right_002.png")
	verify("sprites/player_cultist/elucidate_walking_sprite_cultist_right_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walking_sprite_cultist_right_001.png")
	verify("sprites/player_cultist/elucidate_sprite_cultist_right_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_cultist_right_004.png")
	verify("sprites/player_cultist/elucidate_attack_cultist_right_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_attack_cultist_right_001.png")
	verify("sprites/player_cultist/elucidate_attack_cultist_right_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_attack_cultist_right_002.png")
	verify("sprites/player_cultist/elucidate_walking_sprite_cultist_left_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walking_sprite_cultist_left_002.png")
	verify("sprites/player_cultist/elucidate_walking_sprite_cultist_left_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walking_sprite_cultist_left_001.png")
	verify("sprites/player_cultist/elucidate_sprite_cultist_left_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_cultist_left_003.png")
	verify("sprites/player_cultist/elucidate_attack_cultist_left_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_attack_cultist_left_001.png")
	verify("sprites/player_cultist/elucidate_attack_cultist_left_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_attack_cultist_left_002.png")
	verify("sprites/npc_e_caligo_manifestation/elucidate_idle_caligo_manifestation.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_caligo_manifestationenemy.png")
	verify("sprites/npc_e_caligo_manifestation/elucidate_idle_caligo_manifestation_black_bg.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_caligo_manifestation_black_bg.png")
	verify("sprites/npc_n_imprisoned_experiment/elucidate_idle_imprisoned_experiment_1_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_imprisoned_experiment_1_npc_down.png")
	verify("sprites/npc_n_imprisoned_experiment/elucidate_idle_imprisoned_experiment_2_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_imprisoned_experiment_2_npc_down.png")
	verify("sprites/npc_e_imprisoned_experiment/elucidate_idle_imprisoned_experiment_hostile_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_imprisoned_experiment_hostile_npc_down.png")
	verify("sprites/npc_n_luminarian_scientist/elucidate_idle_church_medical_staff_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_church_medical_staff_npc_down.png")
	verify("sprites/npc_n_luminarian_scientist/elucidate_idle_church_medical_staff_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_church_medical_staff_npc_right.png")
	verify("sprites/npc_n_luminarian_scientist/elucidate_idle_church_medical_staff_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_church_medical_staff_npc_up.png")
	verify("sprites/npc_n_luminarian_scientist/elucidate_idle_church_medical_staff_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_church_medical_staff_npc_left.png")
	verify("sprites/npc_e_luminarian_spy/elucidate_idle_church_spy_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_church_spy_npc_down.png")
	verify("sprites/npc_e_luminarian_spy/elucidate_walk_church_spy_npc_down_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walk_church_spy_npc_down_001.png")
	verify("sprites/npc_e_luminarian_spy/elucidate_walk_church_spy_npc_down_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walk_church_spy_npc_down_002.png")
	verify("sprites/npc_e_luminarian_spy/elucidate_idle_church_spy_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_church_spy_npc_left.png")
	verify("sprites/npc_e_luminarian_spy/elucidate_walk_church_spy_npc_left_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walk_church_spy_npc_left_001.png")
	verify("sprites/npc_e_luminarian_spy/elucidate_walk_church_spy_npc_left_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walk_church_spy_npc_left_002.png")
	verify("sprites/npc_e_luminarian_spy/elucidate_idle_church_spy_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_church_spy_npc_right.png")
	verify("sprites/npc_e_luminarian_spy/elucidate_walk_church_spy_npc_right_001", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walk_church_spy_npc_right_001.png")
	verify("sprites/npc_e_luminarian_spy/elucidate_walk_church_spy_npc_right_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walk_church_spy_npc_right_002.png")
	verify("sprites/npc_e_luminarian_spy/elucidate_idle_church_spy_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_church_spy_npc_up.png")
	verify("sprites/npc_e_luminarian_spy/elucidate_walk_church_spy_npc_up_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walk_church_spy_npc_up_001.png")
	verify("sprites/npc_e_luminarian_spy/elucidate_walk_church_spy_npc_up_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walk_church_spy_npc_up_002.png")
	verify("sprites/npc_n_market_merchant_female/elucidate_idle_female_market_merchant_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_female_market_merchant_npc_down.png")
	verify("sprites/npc_n_market_merchant_female/elucidate_idle_female_market_merchant_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_female_market_merchant_npc_left.png")
	verify("sprites/npc_n_market_merchant_female/elucidate_idle_female_market_merchant_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_female_market_merchant_npc_right.png")
	verify("sprites/npc_n_market_merchant_female/elucidate_idle_female_market_merchant_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_female_market_merchant_npc_up.png")
	verify("sprites/npc_n_market_merchant_male/elucidate_idle_male_market_merchant_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_male_market_merchant_npc_down.png")
	verify("sprites/npc_n_market_merchant_male/elucidate_idle_male_market_merchant_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_male_market_merchant_npc_left.png")
	verify("sprites/npc_n_market_merchant_male/elucidate_idle_male_market_merchant_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_male_market_merchant_npc_right.png")
	verify("sprites/npc_n_market_merchant_male/elucidate_idle_male_market_merchant_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_male_market_merchant_npc_up.png")
	verify("sprites/npc_n_ghost_memories/elucidate_idle_ghost_memory1_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_ghost_memory1_npc_left.png")
	verify("sprites/npc_n_ghost_memories/elucidate_idle_ghost_memory1_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_ghost_memory1_npc_right.png")
	verify("sprites/npc_n_ghost_memories/elucidate_idle_ghost_memory2_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_ghost_memory2_npc_left1.png.png")
	verify("sprites/npc_n_ghost_memories/elucidate_idle_ghost_memory2_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_ghost_memory2_npc_right.png")
	verify("sprites/npc_n_seekers_warrior_female/elucidate_idle_female_tribal_warrior_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_female_tribal_warrior_npc_down.png")
	verify("sprites/npc_n_seekers_warrior_female/elucidate_idle_female_tribal_warrior_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_female_tribal_warrior_npc_left.png")
	verify("sprites/npc_n_seekers_warrior_female/elucidate_idle_female_tribal_warrior_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_female_tribal_warrior_npc_right.png")
	verify("sprites/npc_n_seekers_warrior_female/elucidate_idle_female_tribal_warrior_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_female_tribal_warrior_npc_up.png")
	verify("sprites/npc_n_travelling_bard/elucidate_idle_travelling_merchant_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_travelling_merchant_npc_down.png")
	verify("sprites/npc_n_travelling_bard/elucidate_idle_travelling_merchant_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_travelling_merchant_npc_left.png")
	verify("sprites/npc_n_travelling_bard/elucidate_idle_travelling_merchant_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_travelling_merchant_npc_right.png")
	verify("sprites/npc_n_travelling_bard/elucidate_idle_travelling_merchant_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_travelling_merchant_npc_up.png")
	verify("sprites/npc_n_cult_priest/elucidate_idle_cultist_priest_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_cultist_priest_npc_down.png")
	verify("sprites/npc_n_cult_priest/elucidate_idle_cultist_priest_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_cultist_priest_npc_left.png")
	verify("sprites/npc_n_cult_priest/elucidate_idle_cultist_priest_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_cultist_priest_npc_right.png")
	verify("sprites/npc_n_cult_priest/elucidate_idle_cultist_priest_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_cultist_priest_npc_up.png")
	verify("sprites/npc_n_tavern_keeper/elucidate_idle_tavern_keeper_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_tavern_keeper_npc_down.png")
	verify("sprites/npc_n_tavern_keeper/elucidate_idle_tavern_keeper_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_tavern_keeper_npc_left.png")
	verify("sprites/npc_n_tavern_keeper/elucidate_idle_tavern_keeper_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_tavern_keeper_npc_right.png")
	verify("sprites/npc_n_tavern_keeper/elucidate_idle_tavern_keeper_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_tavern_keeper_npc_up.png")
	verify("sprites/npc_e_cult_archers/elucidate_idle_cultist_archer_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_cultist_archer_npc_down.png")
	verify("sprites/npc_e_cult_archers/elucidate_walk_cultist_archer_npc_down_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walk_cultist_archer_npc_down_001.png")
	verify("sprites/npc_e_cult_archers/elucidate_walk_cultist_archer_npc_down_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walk_cultist_archer_npc_down_002.png")
	verify("sprites/npc_e_cult_archers/elucidate_idle_cultist_archer_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_cultist_archer_npc_left.png")
	verify("sprites/npc_e_cult_archers/elucidate_walk_cultist_archer_npc_left_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walk_cultist_archer_npc_left_001.png")
	verify("sprites/npc_e_cult_archers/elucidate_walk_cultist_archer_npc_left_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walk_cultist_archer_npc_left_002.png")
	verify("sprites/npc_e_cult_archers/elucidate_idle_cultist_archer_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_cultist_archer_npc_right.png")
	verify("sprites/npc_e_cult_archers/elucidate_walk_cultist_archer_npc_right_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walk_cultist_archer_npc_right_001.png")
	verify("sprites/npc_e_cult_archers/elucidate_walk_cultist_archer_npc_right_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walk_cultist_archer_npc_right_002.png")
	verify("sprites/npc_e_cult_archers/elucidate_idle_cultist_archer_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_cultist_archer_npc_up.png")
	verify("sprites/npc_e_cult_archers/elucidate_walk_cultist_archer_npc_up_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walk_cultist_archer_npc_up_001.png")
	verify("sprites/npc_e_cult_archers/elucidate_walk_cultist_archer_npc_up_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walk_cultist_archer_npc_up_002.png")
	verify("sprites/npc_e_cult_eldritch_channelers/elucidate_idle_cultist_channeler_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_cultist_channeler_npc_down.png")
	verify("sprites/npc_e_cult_eldritch_channelers/elucidate_walk_cultist_chaneller_npc_down_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walk_cultist_chaneller_npc_down_002.png")
	verify("sprites/npc_e_cult_eldritch_channelers/elucidate_walk_cultist_chaneller_npc_down_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walk_cultist_chaneller_npc_down_001.png")
	verify("sprites/npc_e_cult_eldritch_channelers/elucidate_idle_cultist_channeler_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_cultist_channeler_npc_right.png")
	verify("sprites/npc_e_cult_eldritch_channelers/elucidate_walk_cultist_chaneller_npc_right_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walk_cultist_chaneller_npc_right_002.png")
	verify("sprites/npc_e_cult_eldritch_channelers/elucidate_walk_cultist_chaneller_npc_right_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walk_cultist_chaneller_npc_right_001.png")
	verify("sprites/npc_e_cult_eldritch_channelers/elucidate_idle_cultist_channeler_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_cultist_channeler_npc_left.png")
	verify("sprites/npc_e_cult_eldritch_channelers/elucidate_walk_cultist_chaneller_npc_left_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walk_cultist_chaneller_npc_left_002.png")
	verify("sprites/npc_e_cult_eldritch_channelers/elucidate_walk_cultist_chaneller_npc_left_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walk_cultist_chaneller_npc_left_001.png")
	verify("sprites/npc_e_cult_eldritch_channelers/elucidate_idle_cultist_channeler_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_idle_cultist_channeler_npc_up.png")
	verify("sprites/npc_e_cult_eldritch_channelers/elucidate_walk_cultist_chaneller_npc_up_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walk_cultist_chaneller_npc_up_002.png")
	verify("sprites/npc_e_cult_eldritch_channelers/elucidate_walk_cultist_chaneller_npc_up_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walk_cultist_chaneller_npc_up_001.png")
	verify("sprites/npc_e_lunar_assasin/elucidate_idle_assassin_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_assassin_npc_down.png")
	verify("sprites/npc_e_lunar_assasin/elucidate_walk_church_assassin_npc_down_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walk_church_assassin_npc_down_001.png")
	verify("sprites/npc_e_lunar_assasin/elucidate_walk_church_assassin_npc_down_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walk_church_assassin_npc_down_002.png")
	verify("sprites/npc_e_lunar_assasin/elucidate_idle_assassin_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_assassin_npc_left.png")
	verify("sprites/npc_e_lunar_assasin/elucidate_walk_church_assassin_npc_left_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walk_church_assassin_npc_left_001.png")
	verify("sprites/npc_e_lunar_assasin/elucidate_walk_church_assassin_npc_left_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walk_church_assassin_npc_left_002.png")
	verify("sprites/npc_e_lunar_assasin/elucidate_idle_assassin_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_assassin_npc_right.png")
	verify("sprites/npc_e_lunar_assasin/elucidate_walk_church_assassin_npc_right_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walk_church_assassin_npc_right_001.png")
	verify("sprites/npc_e_lunar_assasin/elucidate_walk_church_assassin_npc_right_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walk_church_assassin_npc_right_002.png")
	verify("sprites/npc_e_lunar_assasin/elucidate_idle_assassin_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_assassin_npc_up.png")
	verify("sprites/npc_e_lunar_assasin/elucidate_walk_church_assassin_npc_up_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walk_church_assassin_npc_up_001.png")
	verify("sprites/npc_e_lunar_assasin/elucidate_walk_church_assassin_npc_up_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_walk_church_assassin_npc_up_002.png")
	verify("sprites/elucidate_player_sprite_idle_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_player_sprite_idle_down.png")
	verify("sprites/elucidate_player_sprite_walking_down_1.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_player_sprite_walking_down_1.png")
	verify("sprites/elucidate_player_sprite_walking_down_2.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_player_sprite_walking_down_2.png")
	verify("sprites/elucidate_player_sprite_attack_down_1.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_player_sprite_attack_down_1.png")
	verify("sprites/elucidate_player_sprite_attack_down_2.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_player_sprite_attack_down_2.png")
	verify("sprites/elucidate_player_sprite_idle_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_player_sprite_idle_right.png")
	verify("sprites/elucidate_player_sprite_walking_right_1.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_player_sprite_walking_right_1.png")
	verify("sprites/elucidate_player_sprite_walking_right_2.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_player_sprite_walking_right_2.png")
	verify("sprites/elucidate_player_sprite_attack_right_1.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_player_sprite_attack_right_1.png")
	verify("sprites/elucidate_player_sprite_attack_right_2.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_player_sprite_attack_right_2.png")
	verify("sprites/elucidate_player_sprite_idle_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_player_sprite_idle_left.png")
	verify("sprites/elucidate_player_sprite_walking_left_1.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_player_sprite_walking_left_1.png")
	verify("sprites/elucidate_player_sprite_walking_left_2.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_player_sprite_walking_left_2.png")
	verify("sprites/elucidate_player_sprite_attack_left_1.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_player_sprite_attack_left_1.png")
	verify("sprites/elucidate_player_sprite_attack_left_2.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_player_sprite_attack_left_2.png")
	verify("sprites/elucidate_player_sprite_idle_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_player_sprite_idle_up.png")
	verify("sprites/elucidate_player_sprite_walking_up_1.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_player_sprite_walking_up_1.png")
	verify("sprites/elucidate_player_sprite_walking_up_2.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_player_sprite_walking_up_2.png")
	verify("sprites/elucidate_player_sprite_attack_up_1.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_player_sprite_attack_up_1.png")
	verify("sprites/elucidate_player_sprite_attack_up_2.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_player_sprite_attack_up_2.png")
	verify("images/elucidate_empty_bg_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_empty_bg_001.jpg")
	verify("images/elucidate_floor_bg_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_floor_bg_001.png")
	verify("images/elucidate_inventory.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_inventory.png")
	verify("images/elucidate_map_long1.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_map_long1.png")
	verify("images/elucidate_mcguy_portrait_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_mcguy_portrait_001.png")
	verify("images/elucidate_bg_launcher_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_bg_launcher_001-2.png")
	verify("images/elucidate_no_texture.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_no_texture.png")
	verify("images/elucidate_play_bg.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_play_bg.png")
	verify("images/elucidate_select.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_select.png")
	verify("images/elucidate_select_background.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_select_background.png")
	verify("images/elucidate_select_full.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_select_full.png")
	verify("images/elucidate_show_selection.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_show_selection.png")
	verify("images/elucidate_show_selection_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_show_selection_001.png")
	verify("images/elucidate_show_selection_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_show_selection_002.png")
	verify("images/elucidate_title.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_title.png")
	verify("images/elucidate_user_elected_play.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_user_elected_play.png")
	verify("images/elucidate_user_selection_bg.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_user_selection_bg.png")
	verify("images/mercenary_portrait_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/mercenary_portrait_001.png")
	verify("images/mercenary_portrait_001_full.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/mercenary_portrait_001_full.png")
	verify("images/elucidate_bg_empty_room_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_bg_empty_room_001.png")
	verify("images/elucidate_dungeon_grounds_bg_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_dungeon_grounds_bg_001.png")
	verify("images/elucidate_silver_chest_closed_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_silver_chest_closed_001.png")
	verify("images/elucidate_silver_chest_opened_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_silver_chest_opened_002.png")
	verify("images/elucidate_gold_chest_closed_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_gold_chest_closed_003.png")
	verify("images/elucidate_gold_chest_opened_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_gold_chest_opened_004.png")
	verify("images/elucidate_bag_craft_inventory_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_bag_craft_inventory_001.png");
	verify("images/elucidate_bag_craft_inventory_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_bag_craft_inventory_002.png");
	verify("images/elucidate_bag_craft_inventory_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_bag_craft_inventory_003.png");
	verify("images/elucidate_bag_craft_inventory_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_bag_craft_inventory_004.png");
	verify("images/elucidate_bag_inventory_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_bag_inventory_001.png");
	verify("images/elucidate_bag_inventory_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_bag_inventory_002.png");
	verify("images/elucidate_bag_inventory_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_bag_inventory_003.png");
	verify("images/elucidate_craft_only_inventory_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_craft_only_inventory_001.png");
	verify("images/elucidate_craft_only_inventory_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_craft_only_inventory_002.png");
	verify("images/elucidate_craft_only_inventory_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_craft_only_inventory_003.png");
	verify("images/elucidate_craft_only_inventory_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_craft_only_inventory_004.png");
	verify("images/elucidate_craft_only_inventory_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_craft_only_inventory_005.png");
	verify("images/elucidate_dlc_inventory_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_dlc_inventory_001.png");
	verify("images/elucidate_dlc_inventory_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_dlc_inventory_002.png");
	verify("images/elucidate_dlc_inventory_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_dlc_inventory_003.png");
	verify("images/elucidate_dlc_user_selected_play_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_dlc_user_selected_play_001.png");
	verify("images/elucidate_dlc_user_selected_play_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_dlc_user_selected_play_002.png");
	verify("images/elucidate_dlc_user_selected_play_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_dlc_user_selected_play_003.png");
	verify("images/elucidate_dlc_user_selection_bg_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_dlc_user_selection_bg_001.png");
	verify("images/elucidate_dlc_user_selection_bg_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_dlc_user_selection_bg_002.png");
	verify("images/elucidate_dlc_user_selection_bg_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_dlc_user_selection_bg_003.png");
	verify("images/elucidate_dlc_user_selection_bg_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_dlc_user_selection_bg_004.png");
	verify("images/elucidate_dlc_user_selection_bg_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_dlc_user_selection_bg_005.png");
	verify("images/elucidate_dlc_user_selection_bg_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_dlc_user_selection_bg_006.png");
	verify("images/elucidate_enemy_attack_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_enemy_attack_001.png");
	verify("images/elucidate_enemy_escape_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_enemy_escape_001.png");
	verify("images/elucidate_enemy_escape_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_enemy_escape_002.png");
	verify("images/elucidate_enemy_escape_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_enemy_escape_003.png");
	verify("images/elucidate_enemy_interaction_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_enemy_interaction_001.png");
	verify("images/elucidate_enemy_interaction_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_enemy_interaction_002.png");
	verify("images/elucidate_enemy_interaction_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_enemy_interaction_003.png");
	verify("images/elucidate_enemy_interaction_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_enemy_interaction_004.png");
	verify("images/elucidate_enemy_interaction_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_enemy_interaction_005.png");
	verify("images/elucidate_enemy_inventory_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_enemy_inventory_001.png");
	verify("images/elucidate_enemy_skill_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_enemy_skill_001.png");
	verify("images/elucidate_enemy_skill_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_enemy_skill_002.png");
	verify("images/elucidate_enemy_skill_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_enemy_skill_003.png");
	verify("images/elucidate_equipment_inventory_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_equipment_inventory_001.png");
	verify("images/elucidate_equipment_inventory_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_equipment_inventory_002.png");
	verify("images/elucidate_equipment_inventory_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_equipment_inventory_003.png");
	verify("images/elucidate_full_text_portait_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_full_text_portait_001.png");
	verify("images/elucidate_inventory_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_inventory_001.png");
	verify("images/elucidate_inventory_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_inventory_002.png");
	verify("images/elucidate_map_portait_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_map_portait_001.png");
	verify("images/elucidate_map_portait_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_map_portait_002.png");
	verify("images/elucidate_map_portait_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_map_portait_003.png");
	verify("images/elucidate_map_portait_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_map_portait_004.png");
	verify("images/elucidate_map_portait_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_map_portait_005.png");
	verify("images/elucidate_map_portait_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_map_portait_006.png");
	verify("images/elucidate_map_portait_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_map_portait_007.png");
	verify("images/elucidate_map_portait_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_map_portait_008.png");
	verify("images/elucidate_menu_bg_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_menu_bg_001-1.png");
	verify("images/elucidate_menu_bg_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_menu_bg_002-1.png");
	verify("images/elucidate_menu_bg_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_menu_bg_003-1.png");
	verify("images/elucidate_menu_bg_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_menu_bg_004-1.png");
	verify("images/elucidate_menu_bg_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_menu_bg_005-1.png");
	verify("images/elucidate_menu_bg_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_menu_bg_006-1.png");
	verify("images/elucidate_menu_bg_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_menu_bg_007-1.png");
	verify("images/elucidate_menu_bg_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_menu_bg_008-1.png");
	verify("images/elucidate_menu_bg_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_menu_bg_009-1.png");
	verify("images/elucidate_menu_bg_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_menu_bg_010.png");
	verify("images/elucidate_menu_bg_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_menu_bg_011.png");
	verify("images/elucidate_mini_games_select_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_mini_games_select_001.png");
	verify("images/elucidate_mini_games_select_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_mini_games_select_002.png");
	verify("images/elucidate_mini_games_select_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_mini_games_select_003.png");
	verify("images/elucidate_mini_games_select_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_mini_games_select_004.png");
	verify("images/elucidate_mini_games_select_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_mini_games_select_005.png");
	verify("images/elucidate_mini_games_select_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_mini_games_select_006.png");
	verify("images/elucidate_mini_games_select_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_mini_games_select_007.png");
	verify("images/elucidate_mini_games_select_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_mini_games_select_008.png");
	verify("images/elucidate_mini_games_select_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_mini_games_select_009.png");
	verify("images/elucidate_mini_games_select_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_mini_games_select_010.png");
	verify("images/elucidate_mini_games_select_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_mini_games_select_011.png");
	verify("images/elucidate_mini_games_select_012.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_mini_games_select_012.png");
	verify("images/elucidate_mini_games_select_013.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_mini_games_select_013.png");
	verify("images/elucidate_mini_games_select_014.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_mini_games_select_014.png");
	verify("images/elucidate_mini_games_select_015.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_mini_games_select_015.png");
	verify("images/elucidate_mini_games_select_016.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_mini_games_select_016.png");
	verify("images/elucidate_no_texture_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_no_texture_001.png");
	verify("images/elucidate_play_bg.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_play_bg.png");
	verify("images/elucidate_select_background.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_select_background.png");
	verify("images/elucidate_show_selection_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_show_selection_001.png");
	verify("images/elucidate_show_selection_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_show_selection_002.png");
	verify("images/elucidate_user_selected_play_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_user_selected_play_001.png");
	verify("images/elucidate_user_selected_play_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_user_selected_play_002.png");
	verify("images/elucidate_user_selection_bg_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_user_selection_bg_001.png");
	verify("images/elucidate_user_selection_bg_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_user_selection_bg_002.png");
	verify("images/elucidate_user_selection_bg_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_user_selection_bg_003.png");
	verify("images/elucidate_version_select_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_version_select_001.png");
	verify("images/elucidate_version_select_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_version_select_002.png");
	verify("images/elucidate_version_select_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_version_select_003.png");
	verify("images/elucidate_version_select_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_version_select_004.png");
	verify("images/elucidate_version_select_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_version_select_005.png");
	verify("images/elucidate_left_gradient_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_left_gradient_001.png");
	verify("images/elucidate_left_purple_gradient_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_left_purple_gradient_001.png");
	verify("images/elucidate_middle_gradient_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_middle_gradient_001.png");
	verify("images/elucidate_middle_purple_gradient_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_middle_purple_gradient_001.png");
	verify("images/elucidate_middle_purple_gradient_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_middle_purple_gradient_002.png");
	verify("images/elucidate_right_gradient_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_right_gradient_001.png");
	verify("images/elucidate_right_purple_gradient_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_right_purple_gradient_001.png");
	verify("images/walled_mercenary_with_draft_officer_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_mercenary_with_draft_officer_001.png");
	verify("images/walled_mercenary_with_draft_officer_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_mercenary_with_draft_officer_002.png");
	verify("images/walled_mercenary_with_draft_officer_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_mercenary_with_draft_officer_003.png");
	verify("images/walled_mercenary_with_draft_officer_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_mercenary_with_draft_officer_004.png");
	verify("images/walled_mercenary_with_draft_officer_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_mercenary_with_draft_officer_005.png");
	verify("images/walled_mercenary_with_draft_officer_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_mercenary_with_draft_officer_006.png");
	verify("images/walled_mercenary_with_draft_officer_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_mercenary_with_draft_officer_007.png");
	verify("images/walled_mercenary_with_draft_officer_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_mercenary_with_draft_officer_008.png");
	verify("images/walled_mercenary_with_blacksmith_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_mercenary_with_blacksmith_001.png");
	verify("images/walled_mercenary_with_blacksmith_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_mercenary_with_blacksmith_002.png");
	verify("images/walled_mercenary_with_blacksmith_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_mercenary_with_blacksmith_003.png");
	verify("images/walled_mercenary_with_blacksmith_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_mercenary_with_blacksmith_004.png");
	verify("images/walled_mercenary_with_blacksmith_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_mercenary_with_blacksmith_005.png");
	verify("images/walled_mercenary_with_blacksmith_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_mercenary_with_blacksmith_006.png");
	verify("images/walled_mercenary_with_blacksmith_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_mercenary_with_blacksmith_007.png");
	verify("images/walled_mercenary_with_blacksmith_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_mercenary_with_blacksmith_008.png");
	verify("images/walled_mercenary_with_blacksmith_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_mercenary_with_blacksmith_009.png");
	verify("images/walled_mercenary_with_blacksmith_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_mercenary_with_blacksmith_010.png");
	verify("images/walled_mercenary_with_blacksmith_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_mercenary_with_blacksmith_011.png");
	verify("images/walled_mercenary_with_blacksmith_012.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_mercenary_with_blacksmith_012.png");
	verify("images/walled_mercenary_with_blacksmith_013.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_mercenary_with_blacksmith_013.png");
	verify("images/walled_mercenary_with_blacksmith_014.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_mercenary_with_blacksmith_014.png");
	verify("images/walled_mercenary_poster_interact_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_mercenary_poster_interact_001.png");
	verify("images/walled_mercenary_poster_interact_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_mercenary_poster_interact_002.png");
	verify("images/walled_mercenary_poster_interact_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_mercenary_poster_interact_003.png");
	verify("images/theocratic_mercenary_with_priest_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_priest_001.png");
	verify("images/theocratic_mercenary_with_priest_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_priest_002.png");
	verify("images/theocratic_mercenary_with_priest_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_priest_003.png");
	verify("images/theocratic_mercenary_with_priest_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_priest_004.png");
	verify("images/theocratic_mercenary_with_priest_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_priest_005.png");
	verify("images/theocratic_mercenary_with_priest_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_priest_006.png");
	verify("images/theocratic_mercenary_with_priest_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_priest_007.png");
	verify("images/theocratic_mercenary_with_priest_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_priest_008.png");
	verify("images/theocratic_mercenary_with_priest_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_priest_009.png");
	verify("images/theocratic_mercenary_with_priest_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_priest_010.png");
	verify("images/theocratic_mercenary_with_priest_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_priest_011.png");
	verify("images/theocratic_mercenary_with_priest_012.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_priest_012.png");
	verify("images/theocratic_mercenary_with_priest_013.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_priest_013.png");
	verify("images/theocratic_mercenary_with_priest_014.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_priest_014.png");
	verify("images/theocratic_mercenary_with_priest_015.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_priest_015.png");
	verify("images/theocratic_mercenary_with_priest_016.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_priest_016.png");
	verify("images/theocratic_mercenary_with_priest_017.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_priest_017.png");
	verify("images/theocratic_mercenary_with_priest_018.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_priest_018.png");
	verify("images/theocratic_mercenary_with_priest_019.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_priest_019.png");
	verify("images/theocratic_mercenary_with_priest_020.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_priest_020.png");
	verify("images/theocratic_mercenary_with_priest_021.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_priest_021.png");
	verify("images/theocratic_mercenary_with_priest_022.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_priest_022.png");
	verify("images/theocratic_mercenary_with_priest_023.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_priest_023.png");
	verify("images/theocratic_mercenary_with_priest_024.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_priest_024.png");
	verify("images/theocratic_mercenary_with_priest_025.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_priest_025.png");
	verify("images/theocratic_mercenary_with_priest_026.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_priest_026.png");
	verify("images/theocratic_mercenary_with_priest_027.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_priest_027.png");
	verify("images/theocratic_mercenary_with_priest_028.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_priest_028.png");
	verify("images/theocratic_mercenary_with_librarian_scholar_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_librarian_scholar_001.png");
	verify("images/theocratic_mercenary_with_librarian_scholar_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_librarian_scholar_002.png");
	verify("images/theocratic_mercenary_with_librarian_scholar_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_librarian_scholar_003.png");
	verify("images/theocratic_mercenary_with_librarian_scholar_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_librarian_scholar_004.png");
	verify("images/theocratic_mercenary_with_librarian_scholar_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_librarian_scholar_005.png");
	verify("images/theocratic_mercenary_with_librarian_scholar_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_librarian_scholar_006.png");
	verify("images/theocratic_mercenary_with_librarian_scholar_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_librarian_scholar_007.png");
	verify("images/theocratic_mercenary_with_librarian_scholar_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_librarian_scholar_008.png");
	verify("images/theocratic_mercenary_with_librarian_scholar_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_librarian_scholar_009.png");
	verify("images/theocratic_mercenary_with_librarian_scholar_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_librarian_scholar_010.png");
	verify("images/theocratic_mercenary_with_librarian_scholar_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_librarian_scholar_011.png");
	verify("images/theocratic_mercenary_with_librarian_scholar_012.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_librarian_scholar_012.png");
	verify("images/theocratic_mercenary_with_librarian_scholar_013.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_librarian_scholar_013.png");
	verify("images/theocratic_mercenary_with_librarian_scholar_014.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_librarian_scholar_014.png");
	verify("images/theocratic_mercenary_with_librarian_scholar_015.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_librarian_scholar_015.png");
	verify("images/theocratic_mercenary_with_librarian_scholar_016.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_librarian_scholar_016.png");
	verify("images/theocratic_mercenary_with_confession_booth_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_confession_booth_001.png");
	verify("images/theocratic_mercenary_with_confession_booth_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_confession_booth_002.png");
	verify("images/theocratic_mercenary_with_confession_booth_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_confession_booth_003.png");
	verify("images/theocratic_mercenary_with_confession_booth_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_confession_booth_004.png");
	verify("images/theocratic_mercenary_with_confession_booth_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_confession_booth_005.png");
	verify("images/theocratic_mercenary_with_confession_booth_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_mercenary_with_confession_booth_006.png");
	verify("images/theocratic_battle_mercenary_with_priest_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_mercenary_with_priest_001.png");
	verify("images/theocratic_battle_mercenary_with_priest_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_mercenary_with_priest_002.png");
	verify("images/theocratic_battle_mercenary_with_priest_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_mercenary_with_priest_003.png");
	verify("images/theocratic_battle_mercenary_with_priest_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_mercenary_with_priest_004.png");
	verify("images/theocratic_battle_mercenary_with_priest_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_mercenary_with_priest_005.png");
	verify("images/theocratic_battle_mercenary_with_priest_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_mercenary_with_priest_006.png");
	verify("images/theocratic_battle_mercenary_with_priest_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_mercenary_with_priest_007.png");
	verify("images/theocratic_battle_mercenary_with_priest_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_mercenary_with_priest_008.png");
	verify("images/theocratic_battle_mercenary_with_priest_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_mercenary_with_priest_009.png");
	verify("images/theocratic_battle_mercenary_with_priest_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_mercenary_with_priest_010.png");
	verify("images/theocratic_battle_mercenary_with_priest_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_mercenary_with_priest_011.png");
	verify("images/theocratic_battle_mercenary_with_priest_012.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_mercenary_with_priest_012.png");
	verify("images/theocratic_battle_mercenary_with_priest_013.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_mercenary_with_priest_013.png");
	verify("images/theocratic_battle_mercenary_with_priest_014.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_mercenary_with_priest_014.png");
	verify("images/theocratic_battle_mercenary_with_priest_015.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_mercenary_with_priest_015.png");
	verify("images/theocratic_battle_mercenary_with_priest_016.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_mercenary_with_priest_016.png");
	verify("images/theocratic_battle_mercenary_with_priest_017.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_mercenary_with_priest_017.png");
	verify("images/theocratic_battle_mercenary_with_priest_018.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_mercenary_with_priest_018.png");
	verify("images/theocratic_battle_mercenary_with_priest_019.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_mercenary_with_priest_019.png");
	verify("images/theocratic_battle_mercenary_with_priest_020.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_mercenary_with_priest_020.png");
	verify("images/theocratic_battle_mercenary_with_priest_021.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_mercenary_with_priest_021.png");
	verify("images/theocratic_battle_mercenary_with_priest_022.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_mercenary_with_priest_022.png");
	verify("images/theocratic_battle_mercenary_with_priest_023.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_mercenary_with_priest_023.png");
	verify("images/theocratic_battle_mercenary_with_priest_024.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_mercenary_with_priest_024.png");
	verify("images/theocratic_battle_mercenary_with_priest_025.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_mercenary_with_priest_025.png");
	verify("images/theocratic_battle_mercenary_with_priest_026.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_mercenary_with_priest_026.png");
	verify("images/theocratic_battle_mercenary_with_priest_027.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_mercenary_with_priest_027.png");
	verify("images/theocratic_battle_mercenary_with_priest_028.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_mercenary_with_priest_028.png");
	verify("images/theocratic_battle_mercenary_with_priest_029.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_mercenary_with_priest_029.png");
	verify("images/theocratic_battle_mercenary_with_priest_030.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_mercenary_with_priest_030.png");
	verify("images/home_village_mercenary_with_memory_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_mercenary_with_memory_001.png");
	verify("images/home_village_mercenary_with_memory_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_mercenary_with_memory_002.png");
	verify("images/home_village_mercenary_with_memory_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_mercenary_with_memory_003.png");
	verify("images/home_village_mercenary_with_memory_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_mercenary_with_memory_004.png");
	verify("images/home_village_mercenary_with_memory_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_mercenary_with_memory_005.png");
	verify("images/home_village_mercenary_with_memory_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_mercenary_with_memory_006.png");
	verify("images/home_village_mercenary_with_memory_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_mercenary_with_memory_007.png");
	verify("images/home_village_mercenary_with_memory_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_mercenary_with_memory_008.png");
	verify("images/home_village_mercenary_with_memory_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_mercenary_with_memory_009.png");
	verify("images/home_village_mercenary_with_memory_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_mercenary_with_memory_010.png");
	verify("images/home_village_mercenary_with_memory_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_mercenary_with_memory_011.png");
	verify("images/home_village_mercenary_with_memory_012.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_mercenary_with_memory_012.png");
	verify("images/home_village_mercenary_with_memory_013.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_mercenary_with_memory_013.png");
	verify("images/home_village_mercenary_with_memory_014.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_mercenary_with_memory_014.png");
	verify("images/home_village_mercenary_with_memory_015.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_mercenary_with_memory_015.png");
	verify("images/home_village_mercenary_with_memory_016.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_mercenary_with_memory_016.png");
	verify("images/home_village_mercenary_with_memory_017.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_mercenary_with_memory_017.png");
	verify("images/home_village_mercenary_with_memory_018.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_mercenary_with_memory_018.png");
	verify("images/home_village_mercenary_with_memory_019.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_mercenary_with_memory_019.png");
	verify("images/home_village_mercenary_with_memory_020.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_mercenary_with_memory_020.png");
	verify("images/home_village_mercenary_with_memory_021.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_mercenary_with_memory_021.png");
	verify("images/home_village_mercenary_with_memory_022.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_mercenary_with_memory_022.png");
	verify("images/home_village_mercenary_with_memory_023.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_mercenary_with_memory_023.png");
	verify("images/home_village_mercenary_with_memory_024.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_mercenary_with_memory_024.png");
	verify("images/home_village_mercenary_with_memory_025.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_mercenary_with_memory_025.png");
	verify("images/home_village_mercenary_with_memory_026.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_mercenary_with_memory_026.png");
	verify("images/home_village_mercenary_with_memory_027.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_mercenary_with_memory_027.png");
	verify("images/outskirts_village_mercenary_with_village_chief_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_village_chief_001.png");
	verify("images/outskirts_village_mercenary_with_village_chief_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_village_chief_002.png");
	verify("images/outskirts_village_mercenary_with_village_chief_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_village_chief_003.png");
	verify("images/outskirts_village_mercenary_with_village_chief_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_village_chief_004.png");
	verify("images/outskirts_village_mercenary_with_village_chief_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_village_chief_005.png");
	verify("images/outskirts_village_mercenary_with_village_chief_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_village_chief_006.png");
	verify("images/outskirts_village_mercenary_with_village_chief_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_village_chief_007.png");
	verify("images/outskirts_village_mercenary_with_village_chief_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_village_chief_008.png");
	verify("images/outskirts_village_mercenary_with_village_chief_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_village_chief_009.png");
	verify("images/outskirts_village_mercenary_with_village_chief_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_village_chief_010.png");
	verify("images/outskirts_village_mercenary_with_village_chief_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_village_chief_011.png");
	verify("images/outskirts_market_mercenary_with_village_market_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_market_mercenary_with_village_market_001.png");
	verify("images/outskirts_market_mercenary_with_village_market_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_market_mercenary_with_village_market_002.png");
	verify("images/outskirts_market_mercenary_with_village_market_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_market_mercenary_with_village_market_003.png");
	verify("images/outskirts_market_mercenary_with_village_market_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_market_mercenary_with_village_market_004.png");
	verify("images/outskirts_market_mercenary_with_village_market_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_market_mercenary_with_village_market_005.png");
	verify("images/outskirts_market_mercenary_with_village_market_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_market_mercenary_with_village_market_006.png");
	verify("images/outskirts_market_mercenary_with_village_market_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_market_mercenary_with_village_market_007.png");
	verify("images/outskirts_market_mercenary_with_village_market_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_market_mercenary_with_village_market_008.png");
	verify("images/outskirts_village_mercenary_with_villagers_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_villagers_001.png");
	verify("images/outskirts_village_mercenary_with_villagers_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_villagers_002.png");
	verify("images/outskirts_village_mercenary_with_villagers_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_villagers_003.png");
	verify("images/outskirts_village_mercenary_with_villagers_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_villagers_004.png");
	verify("images/outskirts_village_mercenary_with_villagers_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_villagers_005.png");
	verify("images/outskirts_village_mercenary_with_villagers_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_villagers_006.png");
	verify("images/outskirts_village_mercenary_with_travelling_bard_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_travelling_bard_001.png");
	verify("images/outskirts_village_mercenary_with_travelling_bard_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_travelling_bard_002.png");
	verify("images/outskirts_village_mercenary_with_travelling_bard_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_travelling_bard_003.png");
	verify("images/outskirts_village_mercenary_with_travelling_bard_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_travelling_bard_004.png");
	verify("images/outskirts_village_mercenary_with_travelling_bard_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_travelling_bard_005.png");
	verify("images/outskirts_village_mercenary_with_travelling_bard_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_travelling_bard_006.png");
	verify("images/outskirts_village_mercenary_with_travelling_bard_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_travelling_bard_007.png");
	verify("images/outskirts_village_mercenary_with_travelling_bard_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_travelling_bard_008.png");
	verify("images/outskirts_village_mercenary_with_travelling_bard_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_travelling_bard_009.png");
	verify("images/outskirts_village_mercenary_with_travelling_bard_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_travelling_bard_010.png");
	verify("images/outskirts_village_mercenary_with_travelling_bard_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_travelling_bard_011.png");
	verify("images/outskirts_village_mercenary_with_travelling_bard_012.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_travelling_bard_012.png");
	verify("images/outskirts_village_mercenary_with_travelling_bard_013.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_travelling_bard_013.png");
	verify("images/outskirts_village_mercenary_with_travelling_bard_014.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_travelling_bard_014.png");
	verify("images/outskirts_village_mercenary_with_travelling_bard_015.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_travelling_bard_015.png");
	verify("images/outskirts_village_mercenary_with_travelling_bard_016.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_travelling_bard_016.png");
	verify("images/outskirts_village_mercenary_with_travelling_bard_017.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_travelling_bard_017.png");
	verify("images/outskirts_village_mercenary_with_travelling_bard_018.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_travelling_bard_018.png");
	verify("images/outskirts_village_mercenary_with_travelling_bard_019.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_travelling_bard_019.png");
	verify("images/outskirts_village_mercenary_with_travelling_bard_020.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_travelling_bard_020.png");
	verify("images/outskirts_village_mercenary_with_travelling_bard_021.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_mercenary_with_travelling_bard_021.png");
	verify("images/zone_terror_mercenary_to_himself_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_mercenary_to_himself_001.png");
	verify("images/zone_terror_mercenary_to_himself_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_mercenary_to_himself_002.png");
	verify("images/zone_terror_mercenary_to_himself_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_mercenary_to_himself_003.png");
	verify("images/zone_terror_mercenary_to_himself_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_mercenary_to_himself_004.png");
	verify("images/zone_terror_mercenary_to_himself_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_mercenary_to_himself_005.png");
	verify("images/tribe_perimeter_mercenary_with_tribe_elder_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_perimeter_mercenary_with_tribe_elder_001.png");
	verify("images/tribe_perimeter_mercenary_with_tribe_elder_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_perimeter_mercenary_with_tribe_elder_002.png");
	verify("images/tribe_perimeter_mercenary_with_tribe_elder_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_perimeter_mercenary_with_tribe_elder_003.png");
	verify("images/tribe_perimeter_mercenary_with_tribe_elder_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_perimeter_mercenary_with_tribe_elder_004.png");
	verify("images/tribe_perimeter_mercenary_with_tribe_elder_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_perimeter_mercenary_with_tribe_elder_005.png");
	verify("images/tribe_perimeter_mercenary_with_tribe_elder_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_perimeter_mercenary_with_tribe_elder_006.png");
	verify("images/tribe_perimeter_mercenary_with_tribe_elder_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_perimeter_mercenary_with_tribe_elder_007.png");
	verify("images/tribe_perimeter_mercenary_with_tribe_elder_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_perimeter_mercenary_with_tribe_elder_008.png");
	verify("images/tribe_perimeter_mercenary_with_tribe_elder_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_perimeter_mercenary_with_tribe_elder_009.png");
	verify("images/tribe_perimeter_mercenary_with_tribe_elder_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_perimeter_mercenary_with_tribe_elder_010.png");
	verify("images/tribe_perimeter_mercenary_with_tribe_elder_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_perimeter_mercenary_with_tribe_elder_011.png");
	verify("images/tribe_perimeter_mercenary_with_tribe_elder_012.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_perimeter_mercenary_with_tribe_elder_012.png");
	verify("images/tribe_perimeter_warrior_with_assassin_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_perimeter_warrior_with_assassin_001.png");
	verify("images/tribe_perimeter_warrior_with_assassin_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_perimeter_warrior_with_assassin_002.png");
	verify("images/tribe_perimeter_warrior_with_assassin_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_perimeter_warrior_with_assassin_003.png");
	verify("images/tribe_perimeter_warrior_with_assassin_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_perimeter_warrior_with_assassin_004.png");
	verify("images/tribe_perimeter_warrior_with_assassin_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_perimeter_warrior_with_assassin_005.png");
	verify("images/tribe_storage_mercenary_with_shaman_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_mercenary_with_shaman_001.png");
	verify("images/tribe_storage_mercenary_with_shaman_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_mercenary_with_shaman_002.png");
	verify("images/tribe_storage_mercenary_with_shaman_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_mercenary_with_shaman_003.png");
	verify("images/tribe_storage_mercenary_with_shaman_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_mercenary_with_shaman_004.png");
	verify("images/tribe_storage_mercenary_with_shaman_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_mercenary_with_shaman_005.png");
	verify("images/tribe_storage_mercenary_with_shaman_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_mercenary_with_shaman_006.png");
	verify("images/tribe_storage_mercenary_with_shaman_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_mercenary_with_shaman_007.png");
	verify("images/tribe_storage_mercenary_with_shaman_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_mercenary_with_shaman_008.png");
	verify("images/tribe_storage_mercenary_with_shaman_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_mercenary_with_shaman_009.png");
	verify("images/tribe_storage_mercenary_with_shaman_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_mercenary_with_shaman_010.png");
	verify("images/tribe_storage_mercenary_with_shaman_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_mercenary_with_shaman_011.png");
	verify("images/tribe_storage_mercenary_with_shaman_012.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_mercenary_with_shaman_012.png");
	verify("images/tribe_storage_mercenary_with_shaman_013.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_mercenary_with_shaman_013.png");
	verify("images/tribe_storage_mercenary_with_shaman_014.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_mercenary_with_shaman_014.png");
	verify("images/tribe_storage_mercenary_with_shaman_015.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_mercenary_with_shaman_015.png");
	verify("images/tribe_storage_mercenary_with_shaman_016.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_mercenary_with_shaman_016.png");
	verify("images/tribe_storage_mercenary_with_shaman_017.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_mercenary_with_shaman_017.png");
	verify("images/tribe_storage_mercenary_with_shaman_018.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_mercenary_with_shaman_018.png");
	verify("images/tribe_storage_mercenary_with_shaman_019.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_mercenary_with_shaman_019.png");
	verify("images/tribe_storage_mercenary_with_shaman_020.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_mercenary_with_shaman_020.png");
	verify("images/tribe_storage_mercenary_with_shaman_021.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_mercenary_with_shaman_021.png");
	verify("images/tribe_storage_mercenary_with_shaman_022.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_mercenary_with_shaman_022.png");
	verify("images/tribe_tunnel_mercenary_with_tibe_chief_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_tunnel_mercenary_with_tibe_chief_001.png");
	verify("images/tribe_tunnel_mercenary_with_tibe_chief_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_tunnel_mercenary_with_tibe_chief_002.png");
	verify("images/tribe_tunnel_mercenary_with_tibe_chief_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_tunnel_mercenary_with_tibe_chief_003.png");
	verify("images/tribe_tunnel_mercenary_with_tibe_chief_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_tunnel_mercenary_with_tibe_chief_004.png");
	verify("images/tribe_tunnel_mercenary_with_tibe_chief_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_tunnel_mercenary_with_tibe_chief_005.png");
	verify("images/zone_terror_mercenary_with_shaman_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_mercenary_with_shaman_001.png");
	verify("images/zone_terror_mercenary_with_shaman_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_mercenary_with_shaman_002.png");
	verify("images/zone_terror_mercenary_with_shaman_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_mercenary_with_shaman_003.png");
	verify("images/zone_terror_mercenary_with_shaman_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_mercenary_with_shaman_004.png");
	verify("images/zone_terror_mercenary_with_shaman_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_mercenary_with_shaman_005.png");
	verify("images/zone_terror_mercenary_with_shaman_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_mercenary_with_shaman_006.png");
	verify("images/zone_terror_mercenary_with_shaman_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_mercenary_with_shaman_007.png");
	verify("images/zone_terror_mercenary_with_shaman_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_mercenary_with_shaman_008.png");
	verify("images/zone_terror_mercenary_with_shaman_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_mercenary_with_shaman_009.png");
	verify("images/zone_terror_mercenary_with_shaman_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_mercenary_with_shaman_010.png");
	verify("images/zone_terror_mercenary_with_shaman_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_mercenary_with_shaman_011.png");
	verify("images/zone_terror_mercenary_with_shaman_012.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_mercenary_with_shaman_012.png");
	verify("images/zone_terror_mercenary_with_shaman_013.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_mercenary_with_shaman_013.png");
	verify("images/zone_terror_mercenary_with_shaman_014.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_mercenary_with_shaman_014.png");
	verify("images/zone_terror_mercenary_with_shaman_015.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_mercenary_with_shaman_015.png");
	verify("images/zone_terror_mercenary_with_shaman_016.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_mercenary_with_shaman_016.png");
	verify("images/zone_terror_mercenary_with_shaman_017.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_mercenary_with_shaman_017.png");
	verify("images/port_city_mercenary_with_merchant_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_001.png");
	verify("images/port_city_mercenary_with_merchant_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_002.png");
	verify("images/port_city_mercenary_with_merchant_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_003.png");
	verify("images/port_city_mercenary_with_merchant_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_004.png");
	verify("images/port_city_mercenary_with_merchant_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_005.png");
	verify("images/port_city_mercenary_with_merchant_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_006.png");
	verify("images/port_city_mercenary_with_merchant_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_007.png");
	verify("images/port_city_mercenary_with_merchant_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_008.png");
	verify("images/port_city_mercenary_with_merchant_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_009.png");
	verify("images/port_city_mercenary_with_merchant_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_010.png");
	verify("images/port_city_mercenary_with_merchant_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_011.png");
	verify("images/port_city_mercenary_with_merchant_012.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_012.png");
	verify("images/port_city_mercenary_with_merchant_013.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_013.png");
	verify("images/port_city_mercenary_with_merchant_014.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_014.png");
	verify("images/port_city_mercenary_with_merchant_015.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_015.png");
	verify("images/port_city_mercenary_with_merchant_016.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_016.png");
	verify("images/port_city_mercenary_with_merchant_017.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_017.png");
	verify("images/port_city_mercenary_with_merchant_018.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_018.png");
	verify("images/port_city_mercenary_with_merchant_019.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_019.png");
	verify("images/port_city_mercenary_with_merchant_020.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_020.png");
	verify("images/port_city_mercenary_with_merchant_021.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_021.png");
	verify("images/port_city_mercenary_with_merchant_022.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_022.png");
	verify("images/port_city_mercenary_with_merchant_023.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_023.png");
	verify("images/port_city_mercenary_with_merchant_024.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_024.png");
	verify("images/port_city_mercenary_with_merchant_025.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_025.png");
	verify("images/port_city_mercenary_with_merchant_026.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_026.png");
	verify("images/port_city_mercenary_with_merchant_027.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_027.png");
	verify("images/port_city_mercenary_with_merchant_028.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_028.png");
	verify("images/port_city_mercenary_with_merchant_029.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_029.png");
	verify("images/port_city_mercenary_with_merchant_030.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_030.png");
	verify("images/port_city_mercenary_with_merchant_031.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_031.png");
	verify("images/port_city_mercenary_with_merchant_032.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_032.png");
	verify("images/port_city_mercenary_with_merchant_033.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_033.png");
	verify("images/port_city_mercenary_with_merchant_034.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_034.png");
	verify("images/port_city_mercenary_with_merchant_035.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_035.png");
	verify("images/port_city_mercenary_with_merchant_036.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_036.png");
	verify("images/port_city_mercenary_with_merchant_037.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_merchant_037.png");
	verify("images/port_city_mercenary_decision_node_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_decision_node_001.png");
	verify("images/port_city_mercenary_decision_node_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_decision_node_002.png");
	verify("images/port_city_mercenary_decision_node_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_decision_node_003.png");
	verify("images/port_city_mercenary_response_node_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_response_node_001.png");
	verify("images/port_city_mercenary_response_node_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_response_node_002.png");
	verify("images/port_city_mercenary_response_node_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_response_node_003.png");
	verify("images/port_city_mercenary_with_tavern_keeper_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_tavern_keeper_001.png");
	verify("images/port_city_mercenary_with_tavern_keeper_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_tavern_keeper_002.png");
	verify("images/port_city_mercenary_with_tavern_keeper_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_tavern_keeper_003.png");
	verify("images/port_city_mercenary_with_tavern_keeper_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_tavern_keeper_004.png");
	verify("images/port_city_mercenary_with_tavern_keeper_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_tavern_keeper_005.png");
	verify("images/port_city_mercenary_with_tavern_keeper_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_tavern_keeper_006.png");
	verify("images/port_city_mercenary_with_tavern_keeper_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_tavern_keeper_007.png");
	verify("images/port_city_mercenary_with_tavern_keeper_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_tavern_keeper_008.png");
	verify("images/port_city_mercenary_with_tavern_keeper_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_tavern_keeper_009.png");
	verify("images/port_city_mercenary_with_tavern_keeper_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_tavern_keeper_010.png");
	verify("images/port_city_mercenary_with_tavern_keeper_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_tavern_keeper_011.png");
	verify("images/port_city_mercenary_with_tavern_keeper_012.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_tavern_keeper_012.png");
	verify("images/port_city_mercenary_with_tavern_keeper_013.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_tavern_keeper_013.png");
	verify("images/port_city_mercenary_with_tavern_keeper_014.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_tavern_keeper_014.png");
	verify("images/port_city_mercenary_with_tavern_keeper_015.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_tavern_keeper_015.png");
	verify("images/port_city_mercenary_with_tavern_keeper_016.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_tavern_keeper_016.png");
	verify("images/port_city_mercenary_with_tavern_keeper_017.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_tavern_keeper_017.png");
	verify("images/port_city_mercenary_with_harbor_captain_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_harbor_captain_001.png");
	verify("images/port_city_mercenary_with_harbor_captain_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_harbor_captain_002.png");
	verify("images/port_city_mercenary_with_harbor_captain_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_harbor_captain_003.png");
	verify("images/port_city_mercenary_with_harbor_captain_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_harbor_captain_004.png");
	verify("images/port_city_mercenary_with_harbor_captain_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_harbor_captain_005.png");
	verify("images/port_city_mercenary_with_harbor_captain_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_harbor_captain_006.png");
	verify("images/port_city_mercenary_with_harbor_captain_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_harbor_captain_007.png");
	verify("images/port_city_mercenary_with_harbor_captain_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_mercenary_with_harbor_captain_008.png");
	verify("images/cultist_island_mercenary_with_cultist_soldier_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_cultist_soldier_001.png");
	verify("images/cultist_island_mercenary_with_cultist_soldier_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_cultist_soldier_002.png");
	verify("images/cultist_island_mercenary_with_cultist_soldier_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_cultist_soldier_003.png");
	verify("images/cultist_island_mercenary_with_cultist_soldier_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_cultist_soldier_004.png");
	verify("images/cultist_island_mercenary_with_cultist_priest_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_cultist_priest_001.png");
	verify("images/cultist_island_mercenary_with_cultist_priest_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_cultist_priest_002.png");
	verify("images/cultist_island_mercenary_with_cultist_priest_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_cultist_priest_003.png");
	verify("images/cultist_island_mercenary_with_cultist_priest_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_cultist_priest_004.png");
	verify("images/cultist_island_mercenary_with_experiments_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_experiments_001.png");
	verify("images/cultist_island_mercenary_with_experiments_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_experiments_002.png");
	verify("images/cultist_island_mercenary_with_experiments_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_experiments_003.png");
	verify("images/cultist_island_mercenary_with_experiments_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_experiments_004.png");
	verify("images/cultist_island_mercenary_with_experiments_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_experiments_005.png");
	verify("images/cultist_island_mercenary_with_experiments_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_experiments_006.png");
	verify("images/cultist_island_mercenary_with_experiments_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_experiments_007.png");
	verify("images/cultist_island_mercenary_with_experiments_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_experiments_008.png");
	verify("images/cultist_island_mercenary_with_funeris_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_funeris_001.png");
	verify("images/cultist_island_mercenary_with_funeris_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_funeris_002.png");
	verify("images/cultist_island_mercenary_with_funeris_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_funeris_003.png");
	verify("images/cultist_island_mercenary_with_funeris_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_funeris_004.png");
	verify("images/cultist_island_mercenary_with_funeris_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_funeris_005.png");
	verify("images/cultist_island_mercenary_with_funeris_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_funeris_006.png");
	verify("images/cultist_island_mercenary_with_funeris_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_funeris_007.png");
	verify("images/cultist_island_mercenary_with_funeris_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_funeris_008.png");
	verify("images/cultist_island_mercenary_with_funeris_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_funeris_009.png");
	verify("images/cultist_island_mercenary_with_funeris_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_funeris_010.png");
	verify("images/cultist_island_mercenary_with_funeris_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_funeris_011.png");
	verify("images/cultist_island_mercenary_with_funeris_012.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_funeris_012.png");
	verify("images/cultist_island_mercenary_with_funeris_013.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_funeris_013.png");
	verify("images/cultist_island_mercenary_with_funeris_014.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_funeris_014.png");
	verify("images/cultist_island_mercenary_with_funeris_015.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_funeris_015.png");
	verify("images/cultist_island_mercenary_with_funeris_016.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_funeris_016.png");
	verify("images/cultist_island_mercenary_with_funeris_017.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_funeris_017.png");
	verify("images/cultist_island_mercenary_with_funeris_018.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_funeris_018.png");
	verify("images/cultist_island_mercenary_with_funeris_019.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_funeris_019.png");
	verify("images/cultist_island_mercenary_with_funeris_020.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_funeris_020.png");
	verify("images/cultist_island_mercenary_with_funeris_021.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_funeris_021.png");
	verify("images/cultist_island_mercenary_with_funeris_022.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_funeris_022.png");
	verify("images/cultist_island_mercenary_with_funeris_023.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_funeris_023.png");
	verify("images/cultist_island_mercenary_with_funeris_024.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_funeris_024.png");
	verify("images/cultist_island_mercenary_with_funeris_025.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_funeris_025.png");
	verify("images/cultist_island_mercenary_with_funeris_026.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_funeris_026.png");
	verify("images/cultist_island_mercenary_with_funeris_027.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_funeris_027.png");
	verify("images/cultist_island_mercenary_with_funeris_028.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_funeris_028.png");
	verify("images/cultist_island_mercenary_with_funeris_029.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_funeris_029.png");
	verify("images/cultist_island_mercenary_with_funeris_030.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_funeris_030.png");
	verify("images/cultist_island_mercenary_with_cult_leader_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_cult_leader_001.png");
	verify("images/cultist_island_mercenary_with_cult_leader_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_cult_leader_002.png");
	verify("images/cultist_island_mercenary_with_cult_leader_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_cult_leader_003.png");
	verify("images/cultist_island_mercenary_with_cult_leader_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_cult_leader_004.png");
	verify("images/cultist_island_mercenary_with_cult_leader_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_cult_leader_005.png");
	verify("images/cultist_island_mercenary_with_cult_leader_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_cult_leader_006.png");
	verify("images/cultist_island_mercenary_with_cult_leader_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_cult_leader_007.png");
	verify("images/cultist_island_mercenary_with_cult_leader_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_cult_leader_008.png");
	verify("images/cultist_island_mercenary_with_cult_leader_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_cult_leader_009.png");
	verify("images/cultist_island_mercenary_with_cult_leader_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_cult_leader_010.png");
	verify("images/cultist_island_mercenary_with_cult_leader_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_cult_leader_011.png");
	verify("images/cultist_island_mercenary_with_cult_leader_012.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_cult_leader_012.png");
	verify("images/cultist_island_mercenary_with_cult_leader_013.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_cult_leader_013.png");
	verify("images/cultist_island_mercenary_with_cult_leader_014.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_cult_leader_014.png");
	verify("images/cultist_island_mercenary_with_cult_leader_015.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_cult_leader_015.png");
	verify("images/cultist_island_mercenary_with_cult_leader_016.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_cult_leader_016.png");
	verify("images/cultist_island_mercenary_with_cult_leader_017.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_cult_leader_017.png");
	verify("images/cultist_island_mercenary_with_cult_leader_018.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_cult_leader_018.png");
	verify("images/cultist_island_mercenary_with_cult_leader_019.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_cult_leader_019.png");
	verify("images/cultist_island_mercenary_with_cult_leader_020.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_mercenary_with_cult_leader_020.png");
	verify("images/cultist_island_funeris_with_cult_leader_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_funeris_with_cult_leader_001.png");
	verify("images/cultist_island_funeris_with_cult_leader_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_funeris_with_cult_leader_002.png");
	verify("images/cultist_island_funeris_with_cult_leader_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_funeris_with_cult_leader_003.png");
	verify("images/cultist_island_funeris_with_cult_leader_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_funeris_with_cult_leader_004.png");
	verify("images/cultist_island_funeris_with_cult_leader_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_funeris_with_cult_leader_005.png");
	verify("images/cultist_island_funeris_with_cult_leader_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_funeris_with_cult_leader_006.png");
	verify("images/cultist_island_funeris_with_cult_leader_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_funeris_with_cult_leader_007.png");
	verify("images/cultist_island_funeris_with_cult_leader_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_funeris_with_cult_leader_008.png");
	verify("images/cultist_island_funeris_with_cult_leader_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_funeris_with_cult_leader_009.png");
	verify("images/cultist_island_funeris_with_cult_leader_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_funeris_with_cult_leader_010.png");
	verify("images/cultist_island_funeris_with_cult_leader_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_funeris_with_cult_leader_011.png");
	verify("images/cultist_island_funeris_with_cult_leader_012.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_funeris_with_cult_leader_012.png");
	verify("images/cultist_island_funeris_with_cult_leader_013.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_funeris_with_cult_leader_013.png");
	verify("images/cultist_island_funeris_with_cult_leader_014.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_funeris_with_cult_leader_014.png");
	verify("images/cultist_island_funeris_with_cult_leader_015.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_funeris_with_cult_leader_015.png");
	verify("images/cultist_island_funeris_with_cult_soldiers_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_funeris_with_cult_soldiers_001.png");
	verify("images/cultist_island_funeris_with_cult_soldiers_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_funeris_with_cult_soldiers_002.png");
	verify("images/cultist_island_funeris_with_cult_soldiers_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_funeris_with_cult_soldiers_003.png");
	verify("images/cultist_island_funeris_with_cult_soldiers_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_funeris_with_cult_soldiers_004.png");
	verify("images/cultist_island_funeris_with_cult_soldiers_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_funeris_with_cult_soldiers_005.png");
	verify("images/cultist_island_funeris_with_cult_soldiers_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_funeris_with_cult_soldiers_006.png");
	verify("images/zone_terrors_funeris_to_herself_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terrors_funeris_to_herself_001.png");
	verify("images/zone_terrors_funeris_to_herself_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terrors_funeris_to_herself_002.png");
	verify("images/zone_terrors_funeris_to_herself_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terrors_funeris_to_herself_003.png");
	verify("images/zone_terrors_funeris_to_herself_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terrors_funeris_to_herself_004.png");
	verify("images/zone_terrors_funeris_to_herself_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terrors_funeris_to_herself_005.png");
	verify("images/zone_terrors_funeris_to_herself_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terrors_funeris_to_herself_006.png");
	verify("images/zone_terrors_funeris_to_herself_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terrors_funeris_to_herself_007.png");
	verify("images/zone_terrors_funeris_to_herself_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terrors_funeris_to_herself_008.png");
	verify("images/zone_terrors_funeris_to_herself_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terrors_funeris_to_herself_009.png");
	verify("images/zone_terrors_funeris_to_herself_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terrors_funeris_to_herself_010.png");
	verify("images/zone_terrors_funeris_to_herself_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terrors_funeris_to_herself_011.png");
	verify("images/zone_terrors_funeris_to_herself_012.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terrors_funeris_to_herself_012.png");
	verify("images/zone_terrors_funeris_to_herself_013.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terrors_funeris_to_herself_013.png");
	verify("images/zone_terrors_funeris_to_herself_014.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terrors_funeris_to_herself_014.png");
	verify("images/home_village_funeris_to_memory_fragment_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_funeris_to_memory_fragment_001.png");
	verify("images/home_village_funeris_to_memory_fragment_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_funeris_to_memory_fragment_002.png");
	verify("images/home_village_funeris_to_memory_fragment_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_funeris_to_memory_fragment_003.png");
	verify("images/home_village_funeris_to_memory_fragment_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_funeris_to_memory_fragment_004.png");
	verify("images/home_village_funeris_to_memory_fragment_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_funeris_to_memory_fragment_005.png");
	verify("images/home_village_funeris_to_memory_fragment_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_funeris_to_memory_fragment_006.png");
	verify("images/home_village_funeris_to_memory_fragment_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_funeris_to_memory_fragment_007.png");
	verify("images/home_village_funeris_to_memory_fragment_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_funeris_to_memory_fragment_008.png");
	verify("images/home_village_funeris_to_memory_fragment_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_funeris_to_memory_fragment_009.png");
	verify("images/home_village_funeris_to_memory_fragment_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_funeris_to_memory_fragment_010.png");
	verify("images/home_village_funeris_to_memory_fragment_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_funeris_to_memory_fragment_011.png");
	verify("images/home_village_funeris_to_memory_fragment_012.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_funeris_to_memory_fragment_012.png");
	verify("images/home_village_funeris_to_memory_fragment_013.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_funeris_to_memory_fragment_013.png");
	verify("images/home_village_funeris_to_memory_fragment_014.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_funeris_to_memory_fragment_014.png");
	verify("images/home_village_funeris_to_memory_fragment_015.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_funeris_to_memory_fragment_015.png");
	verify("images/home_village_funeris_to_memory_fragment_016.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_funeris_to_memory_fragment_016.png");
	verify("images/home_village_funeris_to_memory_fragment_017.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_funeris_to_memory_fragment_017.png");
	verify("images/home_village_funeris_to_memory_fragment_018.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_funeris_to_memory_fragment_018.png");
	verify("images/home_village_funeris_to_memory_fragment_019.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_funeris_to_memory_fragment_019.png");
	verify("images/home_village_funeris_to_memory_fragment_020.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_funeris_to_memory_fragment_020.png");
	verify("images/home_village_funeris_decision_node_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_funeris_decision_node_001.png");
	verify("images/home_village_funeris_decision_node_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_funeris_decision_node_002.png");
	verify("images/home_village_funeris_decision_node_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_funeris_decision_node_003.png");
	verify("images/home_village_funeris_response_node_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_funeris_response_node_001.png");
	verify("images/home_village_funeris_response_node_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_funeris_response_node_002.png");
	verify("images/home_village_funeris_response_node_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_funeris_response_node_003.png");
	verify("images/laboratory_funeris_with_priest_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_priest_001.png");
	verify("images/laboratory_funeris_with_priest_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_priest_002.png");
	verify("images/laboratory_funeris_with_priest_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_priest_003.png");
	verify("images/laboratory_funeris_with_priest_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_priest_004.png");
	verify("images/laboratory_funeris_with_priest_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_priest_005.png");
	verify("images/laboratory_funeris_with_priest_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_priest_006.png");
	verify("images/laboratory_funeris_with_priest_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_priest_007.png");
	verify("images/laboratory_funeris_with_priest_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_priest_008.png");
	verify("images/laboratory_funeris_with_priest_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_priest_009.png");
	verify("images/laboratory_funeris_with_priest_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_priest_010.png");
	verify("images/laboratory_funeris_with_priest_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_priest_011.png");
	verify("images/laboratory_funeris_with_priest_012.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_priest_012.png");
	verify("images/laboratory_funeris_with_priest_013.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_priest_013.png");
	verify("images/laboratory_funeris_with_priest_014.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_priest_014.png");
	verify("images/laboratory_funeris_with_priest_015.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_priest_015.png");
	verify("images/laboratory_funeris_with_priest_016.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_priest_016.png");
	verify("images/laboratory_funeris_with_priest_017.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_priest_017.png");
	verify("images/laboratory_funeris_with_priest_018.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_priest_018.png");
	verify("images/laboratory_funeris_with_priest_019.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_priest_019.png");
	verify("images/laboratory_funeris_with_priest_020.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_priest_020.png");
	verify("images/laboratory_funeris_with_priest_021.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_priest_021.png");
	verify("images/laboratory_funeris_with_priest_022.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_priest_022.png");
	verify("images/laboratory_funeris_with_priest_023.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_priest_023.png");
	verify("images/laboratory_funeris_with_priest_024.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_priest_024.png");
	verify("images/laboratory_funeris_with_priest_025.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_priest_025.png");
	verify("images/laboratory_funeris_with_priest_026.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_priest_026.png");
	verify("images/laboratory_funeris_with_priest_027.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_priest_027.png");
	verify("images/laboratory_funeris_with_priest_028.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_priest_028.png");
	verify("images/laboratory_funeris_with_priest_029.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_priest_029.png");
	verify("images/laboratory_funeris_with_priest_030.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_priest_030.png");
	verify("images/laboratory_funeris_with_priest_031.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_priest_031.png");
	verify("images/laboratory_funeris_with_priest_032.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_priest_032.png");
	verify("images/laboratory_funeris_with_priest_033.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_priest_033.png");
	verify("images/laboratory_funeris_with_priest_034.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_priest_034.png");
	verify("images/laboratory_funeris_with_assassin_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_funeris_with_assassin_001.png");
	verify("images/walled_priest_with_draft_officer_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_priest_with_draft_officer_001.png");
	verify("images/walled_priest_with_draft_officer_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_priest_with_draft_officer_002.png");
	verify("images/walled_priest_with_draft_officer_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_priest_with_draft_officer_003.png");
	verify("images/walled_priest_with_draft_officer_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_priest_with_draft_officer_004.png");
	verify("images/walled_chapel_priest_with_guard_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_chapel_priest_with_guard_001.png");
	verify("images/walled_chapel_priest_with_guard_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_chapel_priest_with_guard_002.png");
	verify("images/walled_chapel_priest_with_guard_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_chapel_priest_with_guard_003.png");
	verify("images/walled_chapel_priest_with_guard_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_chapel_priest_with_guard_004.png");
	verify("images/walled_chapel_priest_with_guard_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_chapel_priest_with_guard_005.png");
	verify("images/walled_chapel_priest_with_guard_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_chapel_priest_with_guard_006.png");
	verify("images/theocratic_priest_with_church_attendance_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_attendance_001.png");
	verify("images/theocratic_priest_with_church_attendance_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_attendance_002.png");
	verify("images/theocratic_priest_with_church_attendance_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_attendance_003.png");
	verify("images/theocratic_priest_with_church_attendance_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_attendance_004.png");
	verify("images/theocratic_priest_with_church_attendance_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_attendance_005.png");
	verify("images/theocratic_priest_with_church_attendance_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_attendance_006.png");
	verify("images/theocratic_priest_with_church_attendance_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_attendance_007.png");
	verify("images/theocratic_priest_with_church_attendance_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_attendance_008.png");
	verify("images/theocratic_priest_with_church_attendance_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_attendance_009.png");
	verify("images/theocratic_priest_with_church_attendance_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_attendance_010.png");
	verify("images/theocratic_priest_with_church_attendance_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_attendance_011.png");
	verify("images/theocratic_priest_with_church_attendance_012.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_attendance_012.png");
	verify("images/theocratic_priest_with_church_attendance_013.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_attendance_013.png");
	verify("images/theocratic_priest_with_church_attendance_014.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_attendance_014.png");
	verify("images/theocratic_priest_with_church_attendance_015.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_attendance_015.png");
	verify("images/theocratic_priest_with_church_attendance_016.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_attendance_016.png");
	verify("images/theocratic_priest_with_church_attendance_017.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_attendance_017.png");
	verify("images/theocratic_priest_with_church_attendance_018.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_attendance_018.png");
	verify("images/theocratic_priest_with_church_attendance_019.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_attendance_019.png");
	verify("images/theocratic_priest_with_church_attendance_020.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_attendance_020.png");
	verify("images/theocratic_priest_with_church_official_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_official_001.png");
	verify("images/theocratic_priest_with_church_official_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_official_002.png");
	verify("images/theocratic_priest_with_church_official_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_official_003.png");
	verify("images/theocratic_priest_with_church_official_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_official_004.png");
	verify("images/theocratic_priest_with_church_official_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_official_005.png");
	verify("images/theocratic_priest_with_church_official_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_official_006.png");
	verify("images/theocratic_priest_with_church_official_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_official_007.png");
	verify("images/theocratic_priest_with_church_official_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_official_008.png");
	verify("images/theocratic_priest_with_church_official_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_official_009.png");
	verify("images/theocratic_priest_with_church_official_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_official_010.png");
	verify("images/theocratic_priest_with_church_official_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_official_011.png");
	verify("images/theocratic_priest_with_church_official_012.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_official_012.png");
	verify("images/theocratic_priest_with_church_official_013.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_official_013.png");
	verify("images/theocratic_priest_with_church_official_014.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_official_014.png");
	verify("images/theocratic_priest_with_church_official_015.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_official_015.png");
	verify("images/theocratic_priest_with_church_official_016.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_official_016.png");
	verify("images/theocratic_priest_with_church_official_017.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_official_017.png");
	verify("images/theocratic_priest_with_church_official_018.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_priest_with_church_official_018.png");
	verify("images/laboratory_priest_to_himself_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_to_himself_001.png");
	verify("images/laboratory_priest_to_himself_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_to_himself_002.png");
	verify("images/laboratory_priest_to_himself_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_to_himself_003.png");
	verify("images/laboratory_priest_to_himself_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_to_himself_004.png");
	verify("images/laboratory_priest_to_himself_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_to_himself_005.png");
	verify("images/laboratory_priest_to_himself_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_to_himself_006.png");
	verify("images/laboratory_priest_to_himself_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_to_himself_007.png");
	verify("images/laboratory_priest_to_himself_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_to_himself_008.png");
	verify("images/laboratory_priest_to_himself_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_to_himself_009.png");
	verify("images/laboratory_priest_decision_node_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_decision_node_001.png");
	verify("images/laboratory_priest_decision_node_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_decision_node_002.png");
	verify("images/laboratory_priest_decision_node_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_decision_node_003.png");
	verify("images/laboratory_priest_response_node_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_response_node_001.png");
	verify("images/laboratory_priest_response_node_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_response_node_002.png");
	verify("images/laboratory_priest_response_node_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_response_node_003.png");
	verify("images/zone_terror_priest_with_medical_staff_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_priest_with_medical_staff_001.png");
	verify("images/zone_terror_priest_with_medical_staff_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_priest_with_medical_staff_002.png");
	verify("images/zone_terror_priest_with_medical_staff_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_priest_with_medical_staff_003.png");
	verify("images/zone_terror_priest_with_medical_staff_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_priest_with_medical_staff_004.png");
	verify("images/zone_terror_priest_with_medical_staff_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_priest_with_medical_staff_005.png");
	verify("images/zone_terror_priest_with_church_knight_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_priest_with_church_knight_001.png");
	verify("images/zone_terror_priest_with_church_knight_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_priest_with_church_knight_002.png");
	verify("images/zone_terror_priest_with_church_knight_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_priest_with_church_knight_003.png");
	verify("images/zone_terror_priest_with_church_knight_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_priest_with_church_knight_004.png");
	verify("images/zone_terror_priest_with_church_knight_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_priest_with_church_knight_005.png");
	verify("images/zone_terror_priest_with_church_knight_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_priest_with_church_knight_006.png");
	verify("images/zone_terror_priest_with_church_knight_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_priest_with_church_knight_007.png");
	verify("images/zone_terror_priest_with_church_knight_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_priest_with_church_knight_008.png");
	verify("images/laboratory_priest_to_medical_staff_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_to_medical_staff_001.png");
	verify("images/laboratory_priest_to_medical_staff_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_to_medical_staff_002.png");
	verify("images/laboratory_priest_to_medical_staff_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_to_medical_staff_003.png");
	verify("images/laboratory_priest_to_medical_staff_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_to_medical_staff_004.png");
	verify("images/laboratory_priest_to_medical_staff_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_to_medical_staff_005.png");
	verify("images/laboratory_priest_to_medical_staff_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_to_medical_staff_006.png");
	verify("images/laboratory_priest_to_medical_staff_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_to_medical_staff_007.png");
	verify("images/laboratory_priest_to_medical_staff_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_to_medical_staff_008.png");
	verify("images/laboratory_priest_to_medical_staff_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_to_medical_staff_009.png");
	verify("images/laboratory_priest_to_medical_staff_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_to_medical_staff_010.png");
	verify("images/laboratory_priest_to_medical_staff_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_to_medical_staff_011.png");
	verify("images/laboratory_priest_to_medical_staff_012.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_to_medical_staff_012.png");
	verify("images/laboratory_priest_to_medical_staff_013.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_to_medical_staff_013.png");
	verify("images/laboratory_priest_to_medical_staff_014.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_to_medical_staff_014.png");
	verify("images/laboratory_priest_to_medical_staff_015.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_to_medical_staff_015.png");
	verify("images/laboratory_priest_to_medical_staff_016.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_to_medical_staff_016.png");
	verify("images/laboratory_priest_to_medical_staff_017.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_to_medical_staff_017.png");
	verify("images/laboratory_priest_to_medical_staff_018.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_to_medical_staff_018.png");
	verify("images/laboratory_priest_to_medical_staff_019.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_to_medical_staff_019.png");
	verify("images/laboratory_priest_to_medical_staff_020.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_to_medical_staff_020.png");
	verify("images/laboratory_priest_to_medical_staff_021.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_to_medical_staff_021.png");
	verify("images/laboratory_priest_to_medical_staff_022.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_to_medical_staff_022.png");
	verify("images/laboratory_priest_to_medical_staff_023.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/laboratory_priest_to_medical_staff_023.png");
	verify("images/theocratic_battle_priest_with_lucidus_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_priest_with_lucidus_001.png");
	verify("images/theocratic_battle_priest_with_lucidus_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_priest_with_lucidus_002.png");
	verify("images/theocratic_battle_priest_with_lucidus_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_priest_with_lucidus_003.png");
	verify("images/theocratic_battle_priest_with_lucidus_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_priest_with_lucidus_004.png");
	verify("images/theocratic_battle_priest_with_lucidus_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_priest_with_lucidus_005.png");
	verify("images/theocratic_battle_priest_with_lucidus_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_battle_priest_with_lucidus_006.png");
	verify("images/tribe_storage_shaman_with_mercenary_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_shaman_with_mercenary_001.png");
	verify("images/tribe_storage_shaman_with_mercenary_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_shaman_with_mercenary_002.png");
	verify("images/tribe_storage_shaman_with_mercenary_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_shaman_with_mercenary_003.png");
	verify("images/tribe_storage_shaman_with_mercenary_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_shaman_with_mercenary_004.png");
	verify("images/tribe_storage_shaman_with_mercenary_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_shaman_with_mercenary_005.png");
	verify("images/tribe_storage_shaman_with_mercenary_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_shaman_with_mercenary_006.png");
	verify("images/tribe_storage_shaman_with_mercenary_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_shaman_with_mercenary_007.png");
	verify("images/tribe_storage_shaman_with_mercenary_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_shaman_with_mercenary_008.png");
	verify("images/tribe_storage_shaman_with_mercenary_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_shaman_with_mercenary_009.png");
	verify("images/tribe_storage_shaman_with_mercenary_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_shaman_with_mercenary_010.png");
	verify("images/tribe_storage_shaman_with_mercenary_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_shaman_with_mercenary_011.png");
	verify("images/tribe_storage_shaman_with_mercenary_012.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_shaman_with_mercenary_012.png");
	verify("images/tribe_storage_shaman_with_mercenary_013.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_shaman_with_mercenary_013.png");
	verify("images/tribe_storage_shaman_with_mercenary_014.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_shaman_with_mercenary_014.png");
	verify("images/tribe_storage_shaman_with_mercenary_015.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_shaman_with_mercenary_015.png");
	verify("images/tribe_storage_shaman_with_mercenary_016.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_shaman_with_mercenary_016.png");
	verify("images/tribe_storage_shaman_with_mercenary_017.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_shaman_with_mercenary_017.png");
	verify("images/tribe_storage_shaman_with_mercenary_018.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_shaman_with_mercenary_018.png");
	verify("images/tribe_storage_shaman_with_mercenary_019.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_shaman_with_mercenary_019.png");
	verify("images/tribe_storage_shaman_with_mercenary_020.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_shaman_with_mercenary_020.png");
	verify("images/tribe_storage_shaman_with_mercenary_021.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_shaman_with_mercenary_021.png");
	verify("images/tribe_storage_shaman_with_mercenary_022.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_storage_shaman_with_mercenary_022.png");
	verify("images/tribe_tunnel_shaman_with_tribe_chief_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_tunnel_shaman_with_tribe_chief_001.png");
	verify("images/tribe_tunnel_shaman_with_tribe_chief_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_tunnel_shaman_with_tribe_chief_002.png");
	verify("images/tribe_tunnel_shaman_with_tribe_chief_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_tunnel_shaman_with_tribe_chief_003.png");
	verify("images/tribe_tunnel_shaman_with_tribe_chief_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_tunnel_shaman_with_tribe_chief_004.png");
	verify("images/tribe_tunnel_shaman_with_mercenary_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_tunnel_shaman_with_mercenary_001.png");
	verify("images/tribe_tunnel_shaman_with_mercenary_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_tunnel_shaman_with_mercenary_002.png");
	verify("images/tribe_tunnel_shaman_with_mercenary_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_tunnel_shaman_with_mercenary_003.png");
	verify("images/tribe_tunnel_shaman_with_mercenary_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_tunnel_shaman_with_mercenary_004.png");
	verify("images/tribe_tunnel_shaman_with_mercenary_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_tunnel_shaman_with_mercenary_005.png");
	verify("images/tribe_tunnel_shaman_with_mercenary_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_tunnel_shaman_with_mercenary_006.png");
	verify("images/tribe_tunnel_shaman_with_mercenary_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_tunnel_shaman_with_mercenary_007.png");
	verify("images/tribe_tunnel_shaman_with_mercenary_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_tunnel_shaman_with_mercenary_008.png");
	verify("images/tribe_tunnel_shaman_with_mercenary_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_tunnel_shaman_with_mercenary_009.png");
	verify("images/tribe_tunnel_shaman_with_mercenary_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_tunnel_shaman_with_mercenary_010.png");
	verify("images/tribe_tunnel_shaman_with_mercenary_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_tunnel_shaman_with_mercenary_011.png");
	verify("images/tribe_tunnel_shaman_with_mercenary_012.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_tunnel_shaman_with_mercenary_012.png");
	verify("images/tribe_shaman_foresight_low_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_shaman_foresight_low_001.png");
	verify("images/tribe_shaman_foresight_low_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_shaman_foresight_low_002.png");
	verify("images/tribe_shaman_foresight_low_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_shaman_foresight_low_003.png");
	verify("images/tribe_shaman_foresight_mid_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_shaman_foresight_mid_001.png");
	verify("images/tribe_shaman_foresight_mid_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_shaman_foresight_mid_002.png");
	verify("images/tribe_shaman_foresight_mid_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_shaman_foresight_mid_003.png");
	verify("images/tribe_shaman_foresight_high_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_shaman_foresight_high_001.png");
	verify("images/tribe_shaman_foresight_high_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_shaman_foresight_high_002.png");
	verify("images/tribe_shaman_foresight_high_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_shaman_foresight_high_003.png");
	verify("images/tribe_shaman_foresight_high_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_shaman_foresight_high_004.png");
	verify("images/tribe_shaman_foresight_high_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_shaman_foresight_high_005.png");
	verify("images/zone_terror_shaman_with_mercenary_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_shaman_with_mercenary_001.png");
	verify("images/zone_terror_shaman_with_mercenary_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_shaman_with_mercenary_002.png");
	verify("images/zone_terror_shaman_with_mercenary_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_shaman_with_mercenary_003.png");
	verify("images/zone_terror_shaman_with_mercenary_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_shaman_with_mercenary_004.png");
	verify("images/zone_terror_shaman_with_mercenary_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_shaman_with_mercenary_005.png");
	verify("images/zone_terror_shaman_with_mercenary_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_shaman_with_mercenary_006.png");
	verify("images/zone_terror_shaman_with_mercenary_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_shaman_with_mercenary_007.png");
	verify("images/zone_terror_shaman_with_mercenary_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_shaman_with_mercenary_008.png");
	verify("images/zone_terror_shaman_with_mercenary_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_shaman_with_mercenary_009.png");
	verify("images/zone_terror_shaman_with_mercenary_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_shaman_with_mercenary_010.png");
	verify("images/zone_terror_shaman_with_mercenary_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_shaman_with_mercenary_011.png");
	verify("images/zone_terror_shaman_with_mercenary_012.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_shaman_with_mercenary_012.png");
	verify("images/zone_terror_shaman_with_mercenary_013.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_shaman_with_mercenary_013.png");
	verify("images/zone_terror_shaman_with_mercenary_014.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_shaman_with_mercenary_014.png");
	verify("images/zone_terror_shaman_with_mercenary_015.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_shaman_with_mercenary_015.png");
	verify("images/zone_terror_shaman_with_mercenary_016.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_shaman_with_mercenary_016.png");
	verify("images/zone_terror_shaman_with_mercenary_017.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_shaman_with_mercenary_017.png");
	verify("images/zone_terror_shaman_with_mercenary_018.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_shaman_with_mercenary_018.png");
	verify("images/zone_terror_shaman_with_mercenary_019.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_shaman_with_mercenary_019.png");
	verify("images/zone_terror_shaman_with_mercenary_020.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_shaman_with_mercenary_020.png");
	verify("images/zone_terror_shaman_with_mercenary_021.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_shaman_with_mercenary_021.png");
	verify("images/zone_terror_shaman_with_mercenary_022.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_shaman_with_mercenary_022.png");
	verify("images/zone_terror_shaman_with_mercenary_023.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_shaman_with_mercenary_023.png");
	verify("images/zone_terror_shaman_with_mercenary_024.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_shaman_with_mercenary_024.png");
	verify("images/zone_terror_shaman_with_mercenary_025.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_shaman_with_mercenary_025.png");
	verify("images/zone_terror_shaman_with_mercenary_026.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_shaman_with_mercenary_026.png");
	verify("images/zone_terror_shaman_with_mercenary_027.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_shaman_with_mercenary_027.png");
	verify("images/zone_terror_shaman_with_mercenary_028.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_shaman_with_mercenary_028.png");
	verify("images/zone_terror_shaman_with_mercenary_029.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terror_shaman_with_mercenary_029.png");
	verify("images/port_city_shaman_with_mercenary_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_shaman_with_mercenary_001.png");
	verify("images/port_city_shaman_with_mercenary_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_shaman_with_mercenary_002.png");
	verify("images/port_city_shaman_with_mercenary_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_shaman_with_mercenary_003.png");
	verify("images/port_city_shaman_with_mercenary_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_shaman_with_mercenary_004.png");
	verify("images/port_city_shaman_with_mercenary_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_shaman_with_mercenary_005.png");
	verify("images/port_city_shaman_with_mercenary_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_shaman_with_mercenary_006.png");
	verify("images/port_city_shaman_with_mercenary_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_shaman_with_mercenary_007.png");
	verify("images/port_city_shaman_with_mercenary_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_shaman_with_mercenary_008.png");
	verify("images/port_city_shaman_with_mercenary_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_shaman_with_mercenary_009.png");
	verify("images/port_city_shaman_with_mercenary_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_shaman_with_mercenary_010.png");
	verify("images/port_city_shaman_with_mercenary_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_shaman_with_mercenary_011.png");
	verify("images/port_city_shaman_with_mercenary_012.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_shaman_with_mercenary_012.png");
	verify("images/port_city_shaman_with_mercenary_013.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_shaman_with_mercenary_013.png");
	verify("images/port_city_shaman_with_mercenary_014.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_shaman_with_mercenary_014.png");
	verify("images/port_city_shaman_with_mercenary_015.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_shaman_with_mercenary_015.png");
	verify("images/port_city_shaman_with_mercenary_016.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_shaman_with_mercenary_016.png");
	verify("images/port_city_shaman_with_mercenary_017.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_shaman_with_mercenary_017.png");
	verify("images/cultist_island_shaman_with_mercenary_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_shaman_with_mercenary_001.png");
	verify("images/cultist_island_shaman_with_mercenary_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_shaman_with_mercenary_002.png");
	verify("images/cultist_island_shaman_with_mercenary_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_shaman_with_mercenary_003.png");
	verify("images/cultist_island_shaman_with_mercenary_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_shaman_with_mercenary_004.png");
	verify("images/cultist_island_shaman_with_mercenary_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_shaman_with_mercenary_005.png");
	verify("images/cultist_island_shaman_with_mercenary_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_shaman_with_mercenary_006.png");
	verify("images/cultist_island_shaman_with_mercenary_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_shaman_with_mercenary_007.png");
	verify("images/cultist_island_shaman_with_mercenary_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_shaman_with_mercenary_008.png");
	verify("images/cultist_island_shaman_with_mercenary_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_shaman_with_mercenary_009.png");
	verify("images/cultist_island_shaman_with_mercenary_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_shaman_with_mercenary_010.png");
	verify("images/cultist_island_shaman_with_mercenary_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_shaman_with_mercenary_011.png");
	verify("images/cultist_island_shaman_with_mercenary_012.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_shaman_with_mercenary_012.png");
	verify("images/cultist_island_shaman_with_mercenary_013.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_shaman_with_mercenary_013.png");
	verify("images/cultist_island_shaman_with_mercenary_014.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_shaman_with_mercenary_014.png");
	verify("images/cultist_island_shaman_with_mercenary_015.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_shaman_with_mercenary_015.png");
	verify("images/cultist_island_shaman_with_mercenary_016.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_shaman_with_mercenary_016.png");
	verify("images/cultist_island_shaman_with_mercenary_017.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_shaman_with_mercenary_017.png");
	verify("images/cultist_island_shaman_with_mercenary_018.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_shaman_with_mercenary_018.png");
	verify("images/cultist_island_shaman_with_mercenary_019.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_shaman_with_mercenary_019.png");
	verify("images/cultist_island_shaman_with_mercenary_020.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/cultist_island_shaman_with_mercenary_020.png");
	verify("images/outskirts_village_shaman_with_village_chief_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_shaman_with_village_chief_001.png");
	verify("images/outskirts_village_shaman_with_village_chief_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_shaman_with_village_chief_002.png");
	verify("images/outskirts_village_shaman_with_village_chief_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_shaman_with_village_chief_003.png");
	verify("images/outskirts_village_shaman_with_village_chief_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_shaman_with_village_chief_004.png");
	verify("images/outskirts_village_shaman_with_village_chief_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_shaman_with_village_chief_005.png");
	verify("images/outskirts_village_shaman_with_villager_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_shaman_with_villager_001.png");
	verify("images/outskirts_village_shaman_with_villager_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_shaman_with_villager_002.png");
	verify("images/outskirts_village_shaman_with_villager_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_shaman_with_villager_003.png");
	verify("images/outskirts_village_shaman_with_villager_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_shaman_with_villager_004.png");
	verify("images/outskirts_village_shaman_with_villager_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_shaman_with_villager_005.png");
	verify("images/outskirts_village_shaman_with_travelling_bard_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_shaman_with_travelling_bard_001.png");
	verify("images/outskirts_village_shaman_with_travelling_bard_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_shaman_with_travelling_bard_002.png");
	verify("images/outskirts_village_shaman_with_travelling_bard_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_shaman_with_travelling_bard_003.png");
	verify("images/outskirts_village_shaman_with_travelling_bard_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_shaman_with_travelling_bard_004.png");
	verify("images/outskirts_village_shaman_with_travelling_bard_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_shaman_with_travelling_bard_005.png");
	verify("images/tribe_destroyed_shaman_to_herself_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_destroyed_shaman_to_herself_001.png");
	verify("images/tribe_destroyed_shaman_to_herself_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_destroyed_shaman_to_herself_002.png");
	verify("images/tribe_destroyed_shaman_to_herself_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_destroyed_shaman_to_herself_003.png");
	verify("images/tribe_destroyed_shaman_to_herself_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_destroyed_shaman_to_herself_004.png");
	verify("images/tribe_destroyed_shaman_to_herself_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_destroyed_shaman_to_herself_005.png");
	verify("images/tribe_destroyed_shaman_to_herself_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_destroyed_shaman_to_herself_006.png");
	verify("images/tribe_destroyed_shaman_to_herself_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_destroyed_shaman_to_herself_007.png");
	verify("images/tribe_destroyed_shaman_to_herself_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_destroyed_shaman_to_herself_008.png");
	verify("images/tribe_destroyed_shaman_to_herself_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/tribe_destroyed_shaman_to_herself_009.png");
	verify("images/port_city_merchant_with_guild_master_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_guild_master_001.png");
	verify("images/port_city_merchant_with_guild_master_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_guild_master_002.png");
	verify("images/port_city_merchant_with_guild_master_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_guild_master_003.png");
	verify("images/port_city_merchant_with_guild_master_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_guild_master_004.png");
	verify("images/port_city_merchant_with_guild_master_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_guild_master_005.png");
	verify("images/port_city_merchant_with_guild_master_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_guild_master_006.png");
	verify("images/port_city_merchant_with_guild_master_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_guild_master_007.png");
	verify("images/port_city_merchant_with_guild_master_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_guild_master_008.png");
	verify("images/port_city_merchant_with_guild_master_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_guild_master_009.png");
	verify("images/port_city_merchant_with_guild_master_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_guild_master_010.png");
	verify("images/port_city_merchant_with_guild_master_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_guild_master_011.png");
	verify("images/port_city_merchant_with_guild_master_012.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_guild_master_012.png");
	verify("images/port_city_merchant_with_guild_master_013.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_guild_master_013.png");
	verify("images/port_city_merchant_with_guild_master_014.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_guild_master_014.png");
	verify("images/port_city_merchant_with_guild_master_015.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_guild_master_015.png");
	verify("images/port_city_merchant_with_guild_master_016.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_guild_master_016.png");
	verify("images/port_city_merchant_with_guild_master_017.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_guild_master_017.png");
	verify("images/port_city_merchant_with_guild_master_018.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_guild_master_018.png");
	verify("images/port_city_merchant_with_guild_master_019.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_guild_master_019.png");
	verify("images/port_city_merchant_with_guild_master_020.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_guild_master_020.png");
	verify("images/port_city_merchant_with_guild_master_021.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_guild_master_021.png");
	verify("images/port_city_merchant_with_guild_master_022.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_guild_master_022.png");
	verify("images/port_city_merchant_with_guild_master_023.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_guild_master_023.png");
	verify("images/port_city_merchant_with_guild_master_024.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_guild_master_024.png");
	verify("images/port_city_merchant_with_guild_master_025.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_guild_master_025.png");
	verify("images/port_city_merchant_with_guild_master_026.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_guild_master_026.png");
	verify("images/port_city_merchant_with_guild_master_027.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_guild_master_027.png");
	verify("images/port_city_merchant_with_tavern_keeper_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_tavern_keeper_001.png");
	verify("images/port_city_merchant_with_tavern_keeper_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_tavern_keeper_002.png");
	verify("images/port_city_merchant_with_tavern_keeper_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_tavern_keeper_003.png");
	verify("images/port_city_merchant_with_tavern_keeper_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_tavern_keeper_004.png");
	verify("images/port_city_merchant_with_tavern_keeper_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_tavern_keeper_005.png");
	verify("images/port_city_merchant_with_tavern_keeper_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_tavern_keeper_006.png");
	verify("images/port_city_merchant_with_tavern_keeper_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_tavern_keeper_007.png");
	verify("images/port_city_merchant_with_tavern_keeper_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_tavern_keeper_008.png");
	verify("images/port_city_merchant_with_tavern_keeper_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_tavern_keeper_009.png");
	verify("images/port_city_merchant_with_tavern_keeper_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_tavern_keeper_010.png");
	verify("images/port_city_merchant_decision_node_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_decision_node_001.png");
	verify("images/port_city_merchant_decision_node_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_decision_node_002.png");
	verify("images/port_city_merchant_decision_node_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_decision_node_003.png");
	verify("images/port_city_merchant_response_node_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_response_node_001.png");
	verify("images/port_city_merchant_response_node_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_response_node_002.png");
	verify("images/port_city_merchant_response_node_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_response_node_003.png");
	verify("images/walled_merchant_with_blacksmith_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_merchant_with_blacksmith_001.png");
	verify("images/walled_merchant_with_blacksmith_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_merchant_with_blacksmith_002.png");
	verify("images/walled_merchant_with_blacksmith_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_merchant_with_blacksmith_003.png");
	verify("images/walled_merchant_with_blacksmith_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_merchant_with_blacksmith_004.png");
	verify("images/walled_merchant_with_blacksmith_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_merchant_with_blacksmith_005.png");
	verify("images/walled_merchant_with_blacksmith_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_merchant_with_blacksmith_006.png");
	verify("images/walled_merchant_with_blacksmith_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_merchant_with_blacksmith_007.png");
	verify("images/walled_merchant_with_blacksmith_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_merchant_with_blacksmith_008.png");
	verify("images/walled_merchant_with_blacksmith_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_merchant_with_blacksmith_009.png");
	verify("images/walled_merchant_with_blacksmith_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_merchant_with_blacksmith_010.png");
	verify("images/walled_merchant_with_blacksmith_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/walled_merchant_with_blacksmith_011.png");
	verify("images/outskirts_village_merchant_with_village_chief_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_merchant_with_village_chief_001.png");
	verify("images/outskirts_village_merchant_with_village_chief_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_merchant_with_village_chief_002.png");
	verify("images/outskirts_village_merchant_with_village_chief_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_merchant_with_village_chief_003.png");
	verify("images/outskirts_village_merchant_with_village_chief_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_merchant_with_village_chief_004.png");
	verify("images/outskirts_village_merchant_with_village_chief_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_merchant_with_village_chief_005.png");
	verify("images/outskirts_village_merchant_with_village_chief_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_merchant_with_village_chief_006.png");
	verify("images/outskirts_village_merchant_with_village_chief_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/outskirts_village_merchant_with_village_chief_007.png");
	verify("images/zone_terrors_merchant_to_himself_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terrors_merchant_to_himself_001.png");
	verify("images/zone_terrors_merchant_to_himself_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/zone_terrors_merchant_to_himself_002.png");
	verify("images/port_city_merchant_with_harbor_captain_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_harbor_captain_001.png");
	verify("images/port_city_merchant_with_harbor_captain_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_harbor_captain_002.png");
	verify("images/port_city_merchant_with_harbor_captain_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_harbor_captain_003.png");
	verify("images/port_city_merchant_with_harbor_captain_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_harbor_captain_004.png");
	verify("images/home_village_merchant_to_himself_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_merchant_to_himself_001.png");
	verify("images/home_village_merchant_to_himself_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_merchant_to_himself_002.png");
	verify("images/home_village_merchant_to_himself_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_merchant_to_himself_003.png");
	verify("images/home_village_merchant_to_himself_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/home_village_merchant_to_himself_004.png");
	verify("images/port_outpost_mechant_with_church_spy_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_outpost_mechant_with_church_spy_001.png");
	verify("images/port_outpost_mechant_with_church_spy_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_outpost_mechant_with_church_spy_002.png");
	verify("images/port_outpost_mechant_with_church_spy_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_outpost_mechant_with_church_spy_003.png");
	verify("images/port_outpost_mechant_with_church_spy_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_outpost_mechant_with_church_spy_004.png");
	verify("images/port_outpost_mechant_with_church_spy_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_outpost_mechant_with_church_spy_005.png");
	verify("images/port_outpost_mechant_with_church_spy_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_outpost_mechant_with_church_spy_006.png");
	verify("images/port_outpost_mechant_with_church_spy_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_outpost_mechant_with_church_spy_007.png");
	verify("images/port_outpost_mechant_with_church_spy_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_outpost_mechant_with_church_spy_008.png");
	verify("images/port_outpost_mechant_with_church_spy_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_outpost_mechant_with_church_spy_009.png");
	verify("images/port_outpost_mechant_with_church_spy_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_outpost_mechant_with_church_spy_010.png");
	verify("images/port_outpost_mechant_with_church_spy_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_outpost_mechant_with_church_spy_011.png");
	verify("images/port_outpost_mechant_with_church_spy_012.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_outpost_mechant_with_church_spy_012.png");
	verify("images/port_outpost_mechant_with_church_spy_013.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_outpost_mechant_with_church_spy_013.png");
	verify("images/port_outpost_mechant_with_church_spy_014.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_outpost_mechant_with_church_spy_014.png");
	verify("images/port_outpost_mechant_with_church_spy_015.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_outpost_mechant_with_church_spy_015.png");
	verify("images/port_outpost_mechant_with_church_spy_016.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_outpost_mechant_with_church_spy_016.png");
	verify("images/port_outpost_mechant_with_church_spy_017.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_outpost_mechant_with_church_spy_017.png");
	verify("images/port_outpost_mechant_with_church_spy_018.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_outpost_mechant_with_church_spy_018.png");
	verify("images/port_city_merchant_with_captain_and_spy_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_captain_and_spy_001.png");
	verify("images/port_city_merchant_with_captain_and_spy_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_captain_and_spy_002.png");
	verify("images/port_city_merchant_with_captain_and_spy_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_captain_and_spy_003.png");
	verify("images/port_city_merchant_with_captain_and_spy_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_captain_and_spy_004.png");
	verify("images/port_city_merchant_with_captain_and_spy_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_captain_and_spy_005.png");
	verify("images/port_city_merchant_with_captain_and_spy_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_captain_and_spy_006.png");
	verify("images/port_city_merchant_with_captain_and_spy_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_captain_and_spy_007.png");
	verify("images/port_city_merchant_with_captain_and_spy_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_captain_and_spy_008.png");
	verify("images/port_city_merchant_with_captain_and_spy_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_captain_and_spy_009.png");
	verify("images/port_city_merchant_with_captain_and_spy_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_captain_and_spy_010.png");
	verify("images/port_city_merchant_with_captain_and_spy_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_captain_and_spy_011.png");
	verify("images/port_city_merchant_with_captain_and_spy_012.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_captain_and_spy_012.png");
	verify("images/port_city_merchant_with_captain_and_spy_013.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_captain_and_spy_013.png");
	verify("images/port_city_merchant_with_captain_and_spy_014.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_captain_and_spy_014.png");
	verify("images/port_city_merchant_with_captain_and_spy_015.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_captain_and_spy_015.png");
	verify("images/port_city_merchant_with_captain_and_spy_016.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_captain_and_spy_016.png");
	verify("images/port_city_merchant_with_captain_and_spy_017.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_captain_and_spy_017.png");
	verify("images/port_city_merchant_with_captain_and_spy_018.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_captain_and_spy_018.png");
	verify("images/port_city_merchant_with_captain_and_spy_019.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_captain_and_spy_019.png");
	verify("images/port_city_merchant_with_captain_and_spy_020.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_captain_and_spy_020.png");
	verify("images/port_city_merchant_with_mercenary_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_mercenary_001.png");
	verify("images/port_city_merchant_with_mercenary_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_mercenary_002.png");
	verify("images/port_city_merchant_with_mercenary_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_mercenary_003.png");
	verify("images/port_city_merchant_with_mercenary_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_mercenary_004.png");
	verify("images/port_city_merchant_with_mercenary_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_mercenary_005.png");
	verify("images/port_city_merchant_with_mercenary_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_mercenary_006.png");
	verify("images/port_city_merchant_with_mercenary_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_mercenary_007.png");
	verify("images/port_city_merchant_with_mercenary_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_mercenary_008.png");
	verify("images/port_city_merchant_with_mercenary_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_mercenary_009.png");
	verify("images/port_city_merchant_with_mercenary_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_mercenary_010.png");
	verify("images/port_city_merchant_with_mercenary_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_mercenary_011.png");
	verify("images/port_city_merchant_with_mercenary_012.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_mercenary_012.png");
	verify("images/port_city_merchant_with_mercenary_013.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_mercenary_013.png");
	verify("images/port_city_merchant_with_mercenary_014.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_mercenary_014.png");
	verify("images/port_city_merchant_with_mercenary_015.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_mercenary_015.png");
	verify("images/port_city_merchant_with_mercenary_016.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_mercenary_016.png");
	verify("images/port_city_merchant_with_mercenary_017.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_mercenary_017.png");
	verify("images/port_city_merchant_with_mercenary_018.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_mercenary_018.png");
	verify("images/port_city_merchant_with_mercenary_019.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_mercenary_019.png");
	verify("images/port_city_merchant_with_mercenary_020.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/port_city_merchant_with_mercenary_020.png");
	verify("images/theocratic_merchant_with_archive_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_archive_001.png");
	verify("images/theocratic_merchant_with_archive_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_archive_002.png");
	verify("images/theocratic_merchant_with_archive_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_archive_003.png");
	verify("images/theocratic_merchant_with_archive_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_archive_004.png");
	verify("images/theocratic_merchant_with_archive_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_archive_005.png");
	verify("images/theocratic_merchant_with_archive_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_archive_006.png");
	verify("images/theocratic_merchant_with_archive_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_archive_007.png");
	verify("images/theocratic_merchant_with_archive_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_archive_008.png");
	verify("images/theocratic_merchant_with_archive_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_archive_009.png");
	verify("images/theocratic_merchant_with_church_knight_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_church_knight_001.png");
	verify("images/theocratic_merchant_with_church_knight_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_church_knight_002.png");
	verify("images/theocratic_merchant_with_church_knight_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_church_knight_003.png");
	verify("images/theocratic_merchant_with_church_knight_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_church_knight_004.png");
	verify("images/theocratic_merchant_with_church_knight_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_church_knight_005.png");
	verify("images/theocratic_merchant_with_church_knight_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_church_knight_006.png");
	verify("images/theocratic_merchant_with_church_knight_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_church_knight_007.png");
	verify("images/theocratic_merchant_with_church_knight_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_church_knight_008.png");
	verify("images/theocratic_merchant_with_church_knight_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_church_knight_009.png");
	verify("images/theocratic_merchant_with_church_knight_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_church_knight_010.png");
	verify("images/theocratic_merchant_with_church_knight_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_church_knight_011.png");
	verify("images/theocratic_merchant_with_church_knight_012.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_church_knight_012.png");
	verify("images/theocratic_merchant_with_church_knight_013.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_church_knight_013.png");
	verify("images/theocratic_merchant_with_church_knight_014.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_church_knight_014.png");
	verify("images/theocratic_merchant_with_church_knight_015.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_church_knight_015.png");
	verify("images/theocratic_merchant_with_priest_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_001.png");
	verify("images/theocratic_merchant_with_priest_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_002.png");
	verify("images/theocratic_merchant_with_priest_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_003.png");
	verify("images/theocratic_merchant_with_priest_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_004.png");
	verify("images/theocratic_merchant_with_priest_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_005.png");
	verify("images/theocratic_merchant_with_priest_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_006.png");
	verify("images/theocratic_merchant_with_priest_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_007.png");
	verify("images/theocratic_merchant_with_priest_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_008.png");
	verify("images/theocratic_merchant_with_priest_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_009.png");
	verify("images/theocratic_merchant_with_priest_010.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_010.png");
	verify("images/theocratic_merchant_with_priest_011.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_011.png");
	verify("images/theocratic_merchant_with_priest_012.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_012.png");
	verify("images/theocratic_merchant_with_priest_013.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_013.png");
	verify("images/theocratic_merchant_with_priest_014.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_014.png");
	verify("images/theocratic_merchant_with_priest_015.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_015.png");
	verify("images/theocratic_merchant_with_priest_016.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_016.png");
	verify("images/theocratic_merchant_with_priest_017.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_017.png");
	verify("images/theocratic_merchant_with_priest_018.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_018.png");
	verify("images/theocratic_merchant_with_priest_019.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_019.png");
	verify("images/theocratic_merchant_with_priest_020.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_020.png");
	verify("images/theocratic_merchant_with_priest_021.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_021.png");
	verify("images/theocratic_merchant_with_priest_022.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_022.png");
	verify("images/theocratic_merchant_with_priest_023.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_023.png");
	verify("images/theocratic_merchant_with_priest_024.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_024.png");
	verify("images/theocratic_merchant_with_priest_025.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_025.png");
	verify("images/theocratic_merchant_with_priest_026.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_026.png");
	verify("images/theocratic_merchant_with_priest_027.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_027.png");
	verify("images/theocratic_merchant_with_priest_028.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_028.png");
	verify("images/theocratic_merchant_with_priest_029.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_029.png");
	verify("images/theocratic_merchant_with_priest_030.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_030.png");
	verify("images/theocratic_merchant_with_priest_031.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_031.png");
	verify("images/theocratic_merchant_with_priest_032.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_032.png");
	verify("images/theocratic_merchant_with_priest_033.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_033.png");
	verify("images/theocratic_merchant_with_priest_034.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_034.png");
	verify("images/theocratic_merchant_with_priest_035.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_035.png");
	verify("images/theocratic_merchant_with_priest_036.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_036.png");
	verify("images/theocratic_merchant_with_priest_037.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_037.png");
	verify("images/theocratic_merchant_with_priest_038.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_038.png");
	verify("images/theocratic_merchant_with_priest_039.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_039.png");
	verify("images/theocratic_merchant_with_priest_040.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_040.png");
	verify("images/theocratic_merchant_with_priest_041.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_041.png");
	verify("images/theocratic_merchant_with_priest_042.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_042.png");
	verify("images/theocratic_merchant_with_priest_043.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/theocratic_merchant_with_priest_043.png");
	verify("sprites/npc_n_s2_walled_city_civilians_male/elucidate_idle_male_civilian_variant_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_male_civilian_variant_npc_up.png")
	verify("sprites/npc_n_s2_walled_city_civilians_male/elucidate_idle_male_civilian_variant_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_male_civilian_variant_npc_right.png")
	verify("sprites/npc_n_s2_walled_city_civilians_male/elucidate_idle_male_civilian_variant_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_male_civilian_variant_npc_left.png")
	verify("sprites/npc_n_s2_walled_city_civilians_male/elucidate_idle_male_civilian_variant_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_male_civilian_variant_npc_down.png")
	verify("sprites/npc_n_s2_walled_city_civilians_female/elucidate_idle_female_civilian_variant_npc_up.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_female_civilian_variant_npc_up.png")
	verify("sprites/npc_n_s2_walled_city_civilians_female/elucidate_idle_female_civilian_variant_npc_right.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_female_civilian_variant_npc_right.png")
	verify("sprites/npc_n_s2_walled_city_civilians_female/elucidate_idle_female_civilian_variant_npc_left.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_female_civilian_variant_npc_left.png")
	verify("sprites/npc_n_s2_walled_city_civilians_female/elucidate_idle_female_civilian_variant_npc_down.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_idle_female_civilian_variant_npc_down.png")
	verify("sprites/player_mercenary/elucidate_mercenary_sprite_idle_up.png",
		   "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_mercenary_up_001.png")
	verify("sprites/player_mercenary/elucidate_mercenary_move_up_001.png",
		   "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_mercenary_move_up_001.png")
	verify("sprites/player_mercenary/elucidate_mercenary_move_up_002.png",
		   "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_mercenary_move_up_002.png")
	verify("sprites/player_mercenary/elucidate_mercenary_sprite_idle_right.png",
		   "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_mercenary_right_004.png")
	verify("sprites/player_mercenary/elucidate_mercenary_move_right_001.png",
		   "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_mercenary_move_right_001.png")
	verify("sprites/player_mercenary/elucidate_mercenary_move_right_002.png",
		   "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_mercenary_move_right_002.png")
	verify("sprites/player_mercenary/elucidate_mercenary_sprite_idle_left.png",
		   "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_mercenary_left_003.png")
	verify("sprites/player_mercenary/elucidate_mercenary_move_left_001.png",
		   "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_mercenary_move_left_001.png")
	verify("sprites/player_mercenary/elucidate_mercenary_move_left_002.png",
		   "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_mercenary_move_left_002.png")
	verify("sprites/player_mercenary/elucidate_mercenary_sprite_idle_down.png",
		   "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_mercenary_down_002.png")
	verify("sprites/player_mercenary/elucidate_mercenary_move_down_001.png",
		   "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_mercenary_move_down_001.png")
	verify("sprites/player_mercenary/elucidate_mercenary_move_down_002.png",
		   "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_sprite_mercenary_move_down_002.png")
	y_offset = 25
	if os.path.exists("music/elucidate_calm.wav"):
		screen.fill((0, 0, 0))
		draw_text("music/elucidate_calm.wav", 5, y_offset)
		draw_text(" | file verified.", 5, y_offset + 20)
		pygame.draw.rect(screen, (160, 0, 0), (0, 0, screen_x, screen_y), 1)
		pygame.display.flip()
	else:
		zip_download("https://drive.google.com/uc?id=1N2qbV-6Xw5gGJPIjCVD-q_AvE-wy56el")
	if os.path.exists("music/elucidate_depths.wav"):
		screen.fill((0, 0, 0))
		draw_text("music/elucidate_depths.wav", 5, y_offset)
		draw_text(" | file verified.", 5, y_offset + 20)
		pygame.draw.rect(screen, (160, 0, 0), (0, 0, screen_x, screen_y), 1)
		pygame.display.flip()
	else:
		zip_download("https://drive.google.com/uc?id=1N2qbV-6Xw5gGJPIjCVD-q_AvE-wy56el")
	if os.path.exists("music/elucidate_end.wav"):
		screen.fill((0, 0, 0))
		draw_text("music/elucidate_end.wav", 5, y_offset)
		draw_text(" | file verified.", 5, y_offset + 20)
		pygame.draw.rect(screen, (160, 0, 0), (0, 0, screen_x, screen_y), 1)
		pygame.display.flip()
	else:
		zip_download("https://drive.google.com/uc?id=1N2qbV-6Xw5gGJPIjCVD-q_AvE-wy56el")
	if os.path.exists("music/elucidate_last_battle.wav"):
		screen.fill((0, 0, 0))
		draw_text("music/elucidate_last_battle.wav", 5, y_offset)
		draw_text(" | file verified.", 5, y_offset + 20)
		pygame.draw.rect(screen, (160, 0, 0), (0, 0, screen_x, screen_y), 1)
		pygame.display.flip()
	else:
		zip_download("https://drive.google.com/uc?id=1N2qbV-6Xw5gGJPIjCVD-q_AvE-wy56el")
	if os.path.exists("music/elucidate_losing_it.wav"):
		screen.fill((0, 0, 0))
		draw_text("music/elucidate_losing_it.wav", 5, y_offset)
		draw_text(" | file verified.", 5, y_offset + 20)
		pygame.draw.rect(screen, (160, 0, 0), (0, 0, screen_x, screen_y), 1)
		pygame.display.flip()
	else:
		zip_download("https://drive.google.com/uc?id=1N2qbV-6Xw5gGJPIjCVD-q_AvE-wy56el")
	if os.path.exists("music/elucidate_menu.wav"):
		screen.fill((0, 0, 0))
		draw_text("music/elucidate_menu.wav", 5, y_offset)
		draw_text(" | file verified.", 5, y_offset + 20)
		pygame.draw.rect(screen, (160, 0, 0), (0, 0, screen_x, screen_y), 1)
		pygame.display.flip()
	else:
		zip_download("https://drive.google.com/uc?id=1N2qbV-6Xw5gGJPIjCVD-q_AvE-wy56el")
	if os.path.exists("music/elucidate_tense.wav"):
		screen.fill((0, 0, 0))
		draw_text("music/elucidate_tense.wav", 5, y_offset)
		draw_text(" | file verified.", 5, y_offset + 20)
		pygame.draw.rect(screen, (160, 0, 0), (0, 0, screen_x, screen_y), 1)
		pygame.display.flip()
	else:
		zip_download("https://drive.google.com/uc?id=1N2qbV-6Xw5gGJPIjCVD-q_AvE-wy56el")
	if os.path.exists("music/elucidate_the_dark.wav"):
		screen.fill((0, 0, 0))
		draw_text("music/elucidate_the_dark.wav", 5, y_offset)
		draw_text(" | file verified.", 5, y_offset + 20)
		pygame.draw.rect(screen, (160, 0, 0), (0, 0, screen_x, screen_y), 1)
		pygame.display.flip()
	else:
		zip_download("https://drive.google.com/uc?id=1N2qbV-6Xw5gGJPIjCVD-q_AvE-wy56el")
	if os.path.exists("music/elucidate_the_wait.wav"):
		screen.fill((0, 0, 0))
		draw_text("music/elucidate_the_wait.wav", 5, y_offset)
		draw_text(" | file verified.", 5, y_offset + 20)
		pygame.draw.rect(screen, (160, 0, 0), (0, 0, screen_x, screen_y), 1)
		pygame.display.flip()
	else:
		zip_download("https://drive.google.com/uc?id=1N2qbV-6Xw5gGJPIjCVD-q_AvE-wy56el")

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
	"elucidate_title":       _load("images/elucidate_title.png"),
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
	"elucidate_middle_gradient_001":  _sc(_preloaded_images["elucidate_middle_gradient_001"], (200, 30)),
	"elucidate_middle_gradient_002":  _sc(_preloaded_images["elucidate_middle_gradient_001"], (300, 30)),
}

sys_bg_color         = (0,   0,   0  )
sys_bd_color_sc_area = (180, 180, 180)
sys_audio_volume     = 1.0
ui_white       = (245, 245, 245)
ui_crimson     = (160, 0,   0  )
ui_dark_crimson= (120, 0,   0  )
ui_gray        = (180, 180, 180)
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

def mouse():
	pygame.draw.rect(screen, (160, 0, 0), (0, 0, screen_x, screen_y), 1)
	mx, my = pygame.mouse.get_pos()
	pygame.draw.rect(screen, (0, 255, 0), (mx - 10, my, 20, 1))
	pygame.draw.rect(screen, (0, 255, 0), (mx, my - 10, 1, 20))
	tuple_static_text(mx, my, color=(0, 255, 0), position=(mx + 10, my), size=15)
	tuple_static_text(py_clock.get_fps(), color=(0, 255, 0), position=(mx + 10, my + 15), size=15)

state = "main_hub"
play = pygame.Rect((screen_x/2)-50, (screen_y/2)-35, 100, 30)
jhvb = pygame.Rect((screen_x/2)-50, (screen_y / 2) + 5, 300, 30)
while True:
	events = pygame.event.get()
	for event in events:
		if event.type == pygame.QUIT:
			elucidate_sys_exit()
	mouse_x, mouse_y = pygame.mouse.get_pos()
	screen.fill((0, 0, 0))
	screen.blit(_preloaded_images["elucidate_launcher_bg"], (0, 0))
	
	pygame.draw.rect(screen, (160, 0, 0), (0, 0, screen_x, screen_y), 1)
	static_text_raw_center("PLAY", color=(255, 255, 255), position=(screen_x/2, int((screen_y/2))-20), size=30)
	static_text_raw_center("SELECT VERSION", color=(255, 255, 255), position=(screen_x/2, int((screen_y/2))+20), size=30)
	static_text_raw_center("2026 All Rights Reserved. Powered By FGC Productions", color=(180, 180, 180), position=(screen_x / 2, screen_y - 30), size=15)
	if play.collidepoint(mouse_x, mouse_y):
		screen.blit(_scaled_images["elucidate_middle_gradient_001"], ((screen_x // 2) - 100, (screen_y/2)-35))
		static_text_raw_center("PLAY", color=(0, 0, 0), position=(screen_x / 2, int((screen_y / 2)) - 20), size=30)
		for event in events:
			if event.type == pygame.MOUSEBUTTONDOWN:
				from main import *
	if jhvb.collidepoint(mouse_x, mouse_y):
		screen.blit(_scaled_images["elucidate_middle_gradient_002"], ((screen_x // 2) - 150, (screen_y/2) + 5))
		static_text_raw_center("SELECT VERSION", color=(0, 0, 0), position=(screen_x/2, int((screen_y/2))+20), size=30)
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
					if log2.collidepoint(mouse_x, mouse_y):
						bg = 2
					if log3.collidepoint(mouse_x, mouse_y):
						bg = 3
					if log4.collidepoint(mouse_x, mouse_y):
						bg = 4
					mouse()
					display()
	mouse()
	display()