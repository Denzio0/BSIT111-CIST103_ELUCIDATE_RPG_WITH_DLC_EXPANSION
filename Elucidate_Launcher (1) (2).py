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
	verify("sprites/player_mercenary/elucidate_atk_sprite_mercenary_up_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_atk_sprite_mercenary_up_001.png")
	verify("sprites/player_mercenary/elucidate_atk_sprite_mercenary_up_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_atk_sprite_mercenary_up_002.png")
	verify("sprites/player_mercenary/elucidate_atk_sprite_mercenary_right_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_atk_sprite_mercenary_right_001.png")
	verify("sprites/player_mercenary/elucidate_atk_sprite_mercenary_right_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_atk_sprite_mercenary_right_002.png")
	verify("sprites/player_mercenary/elucidate_atk_sprite_mercenary_left_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_atk_sprite_mercenary_left_001.png")
	verify("sprites/player_mercenary/elucidate_atk_sprite_mercenary_left_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_atk_sprite_mercenary_left_002.png")
	verify("sprites/player_mercenary/elucidate_atk_sprite_mercenary_down_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_atk_sprite_mercenary_down_001.png")
	verify("sprites/player_mercenary/elucidate_atk_sprite_mercenary_down_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/Copy-of-elucidate_atk_sprite_mercenary_down_002.png")
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
	verify("images/elucidate_bg_launcher_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_bg_launcher_001-1.png")
	verify("images/elucidate_menu_bg_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_menu_bg_001.png")
	verify("images/elucidate_menu_bg_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_menu_bg_002.png")
	verify("images/elucidate_menu_bg_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_menu_bg_003.png")
	verify("images/elucidate_menu_bg_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_menu_bg_004.png")
	verify("images/elucidate_menu_bg_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_menu_bg_005.png")
	verify("images/elucidate_menu_bg_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_menu_bg_006.png")
	verify("images/elucidate_menu_bg_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_menu_bg_007.png")
	verify("images/elucidate_menu_bg_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_menu_bg_008.png")
	verify("images/elucidate_menu_bg_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_menu_bg_009.png")
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
	verify("images/elucidate_bg_launcher_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_bg_launcher_001-2.png");
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
	verify("images/elucidate_menu_bg_001.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_menu_bg_001.png");
	verify("images/elucidate_menu_bg_002.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_menu_bg_002.png");
	verify("images/elucidate_menu_bg_003.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_menu_bg_003.png");
	verify("images/elucidate_menu_bg_004.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_menu_bg_004.png");
	verify("images/elucidate_menu_bg_005.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_menu_bg_005.png");
	verify("images/elucidate_menu_bg_006.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_menu_bg_006.png");
	verify("images/elucidate_menu_bg_007.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_menu_bg_007.png");
	verify("images/elucidate_menu_bg_008.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_menu_bg_008.png");
	verify("images/elucidate_menu_bg_009.png", "http://elucidatewebstorage.unaux.com/wp-content/uploads/2026/04/elucidate_menu_bg_009.png");
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
	"elucidate_menu_bg_001": _load("images/elucidate_menu_bg_001.png"),
	"elucidate_menu_bg_002": _load("images/elucidate_menu_bg_002.png"),
	"elucidate_menu_bg_003": _load("images/elucidate_menu_bg_003.png"),
	"elucidate_menu_bg_004": _load("images/elucidate_menu_bg_004.png"),
	"elucidate_menu_bg_005": _load("images/elucidate_menu_bg_005.png"),
	"elucidate_menu_bg_006": _load("images/elucidate_menu_bg_006.png"),
	"elucidate_menu_bg_007": _load("images/elucidate_menu_bg_007.png"),
	"elucidate_menu_bg_008": _load("images/elucidate_menu_bg_008.png"),
	"elucidate_menu_bg_009": _load("images/elucidate_menu_bg_009.png"),
	"elucidate_select":      _load("images/elucidate_select.png"),
	"elucidate_select_full": _load("images/elucidate_select_full.png"),
	"elucidate_play_bg":     _load("images/elucidate_play_bg.png"),
	"elucidate_no_texture":  _load("images/elucidate_no_texture.png"),
	"elucidate_no_sprite_idle_1":     _load("sprites/elucidate_player_sprite_idle_up.png",    True),
	"elucidate_no_sprite_idle_2":     _load("sprites/elucidate_player_sprite_idle_down.png",  True),
	"elucidate_no_sprite_idle_3":     _load("sprites/elucidate_player_sprite_idle_left.png",  True),
	"elucidate_no_sprite_idle_4":     _load("sprites/elucidate_player_sprite_idle_right.png", True),
	"elucidate_no_sprite_walk_1_1":   _load("sprites/elucidate_player_sprite_walking_up_1.png",    True),
	"elucidate_no_sprite_walk_1_2":   _load("sprites/elucidate_player_sprite_walking_up_2.png",    True),
	"elucidate_no_sprite_walk_2_1":   _load("sprites/elucidate_player_sprite_walking_down_1.png",  True),
	"elucidate_no_sprite_walk_2_2":   _load("sprites/elucidate_player_sprite_walking_down_2.png",  True),
	"elucidate_no_sprite_walk_3_1":   _load("sprites/elucidate_player_sprite_walking_left_1.png",  True),
	"elucidate_no_sprite_walk_3_2":   _load("sprites/elucidate_player_sprite_walking_left_2.png",  True),
	"elucidate_no_sprite_walk_4_1":   _load("sprites/elucidate_player_sprite_walking_right_1.png", True),
	"elucidate_no_sprite_walk_4_2":   _load("sprites/elucidate_player_sprite_walking_right_2.png", True),
	"elucidate_no_sprite_attack_1_1": _load("sprites/elucidate_player_sprite_attack_up_1.png",    True),
	"elucidate_no_sprite_attack_1_2": _load("sprites/elucidate_player_sprite_attack_up_2.png",    True),
	"elucidate_no_sprite_attack_2_1": _load("sprites/elucidate_player_sprite_attack_down_1.png",  True),
	"elucidate_no_sprite_attack_2_2": _load("sprites/elucidate_player_sprite_attack_down_2.png",  True),
	"elucidate_no_sprite_attack_3_1": _load("sprites/elucidate_player_sprite_attack_left_1.png",  True),
	"elucidate_no_sprite_attack_3_2": _load("sprites/elucidate_player_sprite_attack_left_2.png",  True),
	"elucidate_no_sprite_attack_4_1": _load("sprites/elucidate_player_sprite_attack_right_1.png", True),
	"elucidate_no_sprite_attack_4_2": _load("sprites/elucidate_player_sprite_attack_right_2.png", True),
	"elucidate_mercenary_sprite_idle_1": _load("sprites/mercenary/elucidate_mercenary_sprite_idle_up.png",    True),
	"elucidate_mercenary_sprite_idle_2": _load("sprites/mercenary/elucidate_mercenary_sprite_idle_down.png",  True),
	"elucidate_mercenary_sprite_idle_3": _load("sprites/mercenary/elucidate_mercenary_sprite_idle_left.png",  True),
	"elucidate_mercenary_sprite_idle_4": _load("sprites/mercenary/elucidate_mercenary_sprite_idle_right.png", True),
	"elucidate_mercenary_sprite_walk_1_1": _load("sprites/mercenary/elucidate_sprite_mercenary_move_up_001.png",    True),
	"elucidate_mercenary_sprite_walk_1_2": _load("sprites/mercenary/elucidate_sprite_mercenary_move_up_002.png",    True),
	"elucidate_mercenary_sprite_walk_2_1": _load("sprites/mercenary/elucidate_sprite_mercenary_move_down_001.png",  True),
	"elucidate_mercenary_sprite_walk_2_2": _load("sprites/mercenary/elucidate_sprite_mercenary_move_down_002.png",  True),
	"elucidate_mercenary_sprite_walk_3_1": _load("sprites/mercenary/elucidate_sprite_mercenary_move_left_001.png",  True),
	"elucidate_mercenary_sprite_walk_3_2": _load("sprites/mercenary/elucidate_sprite_mercenary_move_left_002.png",  True),
	"elucidate_mercenary_sprite_walk_4_1": _load("sprites/mercenary/elucidate_sprite_mercenary_move_right_001.png", True),
	"elucidate_mercenary_sprite_walk_4_2": _load("sprites/mercenary/elucidate_sprite_mercenary_move_right_002.png", True),
	"elucidate_mercenary_sprite_attack_1_1": _load("sprites/elucidate_player_sprite_attack_up_1.png",    True),
	"elucidate_mercenary_sprite_attack_1_2": _load("sprites/elucidate_player_sprite_attack_up_2.png",    True),
	"elucidate_mercenary_sprite_attack_2_1": _load("sprites/elucidate_player_sprite_attack_down_1.png",  True),
	"elucidate_mercenary_sprite_attack_2_2": _load("sprites/elucidate_player_sprite_attack_down_2.png",  True),
	"elucidate_mercenary_sprite_attack_3_1": _load("sprites/elucidate_player_sprite_attack_left_1.png",  True),
	"elucidate_mercenary_sprite_attack_3_2": _load("sprites/elucidate_player_sprite_attack_left_2.png",  True),
	"elucidate_mercenary_sprite_attack_4_1": _load("sprites/elucidate_player_sprite_attack_right_1.png", True),
	"elucidate_mercenary_sprite_attack_4_2": _load("sprites/elucidate_player_sprite_attack_right_2.png", True),
	"elucidate_select_bg_001":     _load("images/elucidate_select_background.png"),
	"elucidate_select_bg_002":     _load("images/elucidate_empty_bg_001.png"),
	"elucidate_select_ui_001":     _load("images/elucidate_show_selection_002.png"),
	"elucidate_select_ui_002":     _load("images/elucidate_show_selection_001.png", True),
	"elucidate_mcguy_001":         _load("images/elucidate_mcguy_portrait_001.png", True),
	"elucidate_select_player_001": _load("images/elucidate_user_selection_bg.png"),
	"elucidate_select_player_002": _load("images/elucidate_user_elected_play.png"),
	"elucidate_area_empty_room":   _load("images/elucidate_bg_empty_room_001.png"),
	"elucidate_dungeon_area_001":  _load("images/elucidate_dungeon_grounds_bg_001.png"),
	"elucidate_dungeon_area_002":  _load("images/elucidate_dungeon_grounds_bg_002.png"),
	"elucidate_full_scale_test":   _load("images/elucidate_map_long1.png"),
	"elucidate_inventory":         _load("images/elucidate_inventory.png"),
	"elucidate_launcher_bg":        _load("images/elucidate_bg_launcher_001.png"),
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
	"l_i_lab_office_under_administrative_wing": _load("maps/l_i_lab_office_under_administrative_wing.png"),
	"l_i_active_laboratory_under_administrative_wing": _load("maps/l_i_active_laboratory_under_administrative_wing.png"),
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
	"f_o_village_market": _load("maps/f_o_village_market.png"),
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
	"l_i_customs_office": _load("maps/l_i_customs_office.png"),
	#GUI AND BACKGROUNDS
	"elucidate_bag_craft_inventory_001":        _load("images/elucidate_bag_craft_inventory_001.png"),
	"elucidate_bag_craft_inventory_002":        _load("images/elucidate_bag_craft_inventory_002.png"),
	"elucidate_bag_craft_inventory_003":        _load("images/elucidate_bag_craft_inventory_003.png"),
	"elucidate_bag_craft_inventory_004":        _load("images/elucidate_bag_craft_inventory_004.png"),
	"elucidate_bag_inventory_001":        _load("images/elucidate_bag_inventory_001.png"),
	"elucidate_bag_inventory_002":        _load("images/elucidate_bag_inventory_002.png"),
	"elucidate_bag_inventory_003":        _load("images/elucidate_bag_inventory_003.png"),
	"elucidate_bg_launcher_001":        _load("images/elucidate_bg_launcher_001.png"),
	"elucidate_craft_only_inventory_001":        _load("images/elucidate_craft_only_inventory_001.png"),
	"elucidate_craft_only_inventory_002":        _load("images/elucidate_craft_only_inventory_002.png"),
	"elucidate_craft_only_inventory_003":        _load("images/elucidate_craft_only_inventory_003.png"),
	"elucidate_craft_only_inventory_004":        _load("images/elucidate_craft_only_inventory_004.png"),
	"elucidate_craft_only_inventory_005":        _load("images/elucidate_craft_only_inventory_005.png"),
	"elucidate_dlc_inventory_001":        _load("images/elucidate_dlc_inventory_001.png"),
	"elucidate_dlc_inventory_002":        _load("images/elucidate_dlc_inventory_002.png"),
	"elucidate_dlc_inventory_003":        _load("images/elucidate_dlc_inventory_003.png"),
	"elucidate_dlc_user_selected_play_001":        _load("images/elucidate_dlc_user_selected_play_001.png"),
	"elucidate_dlc_user_selected_play_002":        _load("images/elucidate_dlc_user_selected_play_002.png"),
	"elucidate_dlc_user_selected_play_003":        _load("images/elucidate_dlc_user_selected_play_003.png"),
	"elucidate_dlc_user_selection_bg_001":        _load("images/elucidate_dlc_user_selection_bg_001.png"),
	"elucidate_dlc_user_selection_bg_002":        _load("images/elucidate_dlc_user_selection_bg_002.png"),
	"elucidate_dlc_user_selection_bg_003":        _load("images/elucidate_dlc_user_selection_bg_003.png"),
	"elucidate_dlc_user_selection_bg_004":        _load("images/elucidate_dlc_user_selection_bg_004.png"),
	"elucidate_dlc_user_selection_bg_005":        _load("images/elucidate_dlc_user_selection_bg_005.png"),
	"elucidate_dlc_user_selection_bg_006":        _load("images/elucidate_dlc_user_selection_bg_006.png"),
	"elucidate_enemy_attack_001":        _load("images/elucidate_enemy_attack_001.png"),
	"elucidate_enemy_escape_001":        _load("images/elucidate_enemy_escape_001.png"),
	"elucidate_enemy_escape_002":        _load("images/elucidate_enemy_escape_002.png"),
	"elucidate_enemy_escape_003":        _load("images/elucidate_enemy_escape_003.png"),
	"elucidate_enemy_interaction_001":        _load("images/elucidate_enemy_interaction_001.png"),
	"elucidate_enemy_interaction_002":        _load("images/elucidate_enemy_interaction_002.png"),
	"elucidate_enemy_interaction_003":        _load("images/elucidate_enemy_interaction_003.png"),
	"elucidate_enemy_interaction_004":        _load("images/elucidate_enemy_interaction_004.png"),
	"elucidate_enemy_interaction_005":        _load("images/elucidate_enemy_interaction_005.png"),
	"elucidate_enemy_inventory_001":        _load("images/elucidate_enemy_inventory_001.png"),
	"elucidate_enemy_skill_001":        _load("images/elucidate_enemy_skill_001.png"),
	"elucidate_enemy_skill_002":        _load("images/elucidate_enemy_skill_002.png"),
	"elucidate_enemy_skill_003":        _load("images/elucidate_enemy_skill_003.png"),
	"elucidate_equipment_inventory_001":        _load("images/elucidate_equipment_inventory_001.png"),
	"elucidate_equipment_inventory_002":        _load("images/elucidate_equipment_inventory_002.png"),
	"elucidate_equipment_inventory_003":        _load("images/elucidate_equipment_inventory_003.png"),
	"elucidate_full_text_portait_001":        _load("images/elucidate_full_text_portait_001.png"),
	"elucidate_inventory_001":        _load("images/elucidate_inventory_001.png"),
	"elucidate_inventory_002":        _load("images/elucidate_inventory_002.png"),
	"elucidate_map_portait_001":        _load("images/elucidate_map_portait_001.png"),
	"elucidate_map_portait_002":        _load("images/elucidate_map_portait_002.png"),
	"elucidate_map_portait_003":        _load("images/elucidate_map_portait_003.png"),
	"elucidate_map_portait_004":        _load("images/elucidate_map_portait_004.png"),
	"elucidate_map_portait_005":        _load("images/elucidate_map_portait_005.png"),
	"elucidate_map_portait_006":        _load("images/elucidate_map_portait_006.png"),
	"elucidate_map_portait_007":        _load("images/elucidate_map_portait_007.png"),
	"elucidate_map_portait_008":        _load("images/elucidate_map_portait_008.png"),
	"elucidate_menu_bg_001":        _load("images/elucidate_menu_bg_001.png"),
	"elucidate_menu_bg_002":        _load("images/elucidate_menu_bg_002.png"),
	"elucidate_menu_bg_003":        _load("images/elucidate_menu_bg_003.png"),
	"elucidate_menu_bg_004":        _load("images/elucidate_menu_bg_004.png"),
	"elucidate_menu_bg_005":        _load("images/elucidate_menu_bg_005.png"),
	"elucidate_menu_bg_006":        _load("images/elucidate_menu_bg_006.png"),
	"elucidate_menu_bg_007":        _load("images/elucidate_menu_bg_007.png"),
	"elucidate_menu_bg_008":        _load("images/elucidate_menu_bg_008.png"),
	"elucidate_menu_bg_009":        _load("images/elucidate_menu_bg_009.png"),
	"elucidate_menu_bg_010":        _load("images/elucidate_menu_bg_010.png"),
	"elucidate_menu_bg_011":        _load("images/elucidate_menu_bg_011.png"),
	"elucidate_mini_games_select_001":        _load("images/elucidate_mini_games_select_001.png"),
	"elucidate_mini_games_select_002":        _load("images/elucidate_mini_games_select_002.png"),
	"elucidate_mini_games_select_003":        _load("images/elucidate_mini_games_select_003.png"),
	"elucidate_mini_games_select_004":        _load("images/elucidate_mini_games_select_004.png"),
	"elucidate_mini_games_select_005":        _load("images/elucidate_mini_games_select_005.png"),
	"elucidate_mini_games_select_006":        _load("images/elucidate_mini_games_select_006.png"),
	"elucidate_mini_games_select_007":        _load("images/elucidate_mini_games_select_007.png"),
	"elucidate_mini_games_select_008":        _load("images/elucidate_mini_games_select_008.png"),
	"elucidate_mini_games_select_009":        _load("images/elucidate_mini_games_select_009.png"),
	"elucidate_mini_games_select_010":        _load("images/elucidate_mini_games_select_010.png"),
	"elucidate_mini_games_select_011":        _load("images/elucidate_mini_games_select_011.png"),
	"elucidate_mini_games_select_012":        _load("images/elucidate_mini_games_select_012.png"),
	"elucidate_mini_games_select_013":        _load("images/elucidate_mini_games_select_013.png"),
	"elucidate_mini_games_select_014":        _load("images/elucidate_mini_games_select_014.png"),
	"elucidate_mini_games_select_015":        _load("images/elucidate_mini_games_select_015.png"),
	"elucidate_mini_games_select_016":        _load("images/elucidate_mini_games_select_016.png"),
	"elucidate_no_texture_001":        _load("images/elucidate_no_texture_001.png"),
	"elucidate_play_bg":        _load("images/elucidate_play_bg.png"),
	"elucidate_select_background":        _load("images/elucidate_select_background.png"),
	"elucidate_show_selection_001":        _load("images/elucidate_show_selection_001.png"),
	"elucidate_show_selection_002":        _load("images/elucidate_show_selection_002.png"),
	"elucidate_user_selected_play_001":        _load("images/elucidate_user_selected_play_001.png"),
	"elucidate_user_selected_play_002":        _load("images/elucidate_user_selected_play_002.png"),
	"elucidate_user_selection_bg_001":        _load("images/elucidate_user_selection_bg_001.png"),
	"elucidate_user_selection_bg_002":        _load("images/elucidate_user_selection_bg_002.png"),
	"elucidate_user_selection_bg_003":        _load("images/elucidate_user_selection_bg_003.png"),
	"elucidate_version_select_001":        _load("images/elucidate_version_select_001.png"),
	"elucidate_version_select_002":        _load("images/elucidate_version_select_002.png"),
	"elucidate_version_select_003":        _load("images/elucidate_version_select_003.png"),
	"elucidate_version_select_004":        _load("images/elucidate_version_select_004.png"),
	"elucidate_version_select_005":        _load("images/elucidate_version_select_005.png"),
	"elucidate_left_gradient_001":        _load("images/elucidate_left_gradient_001.png", True),
	"elucidate_left_purple_gradient_001":        _load("images/elucidate_left_purple_gradient_001.png", True),
	"elucidate_middle_gradient_001":        _load("images/elucidate_middle_gradient_001.png", True),
	"elucidate_middle_purple_gradient_001":        _load("images/elucidate_middle_purple_gradient_001.png", True),
	"elucidate_middle_purple_gradient_002":        _load("images/elucidate_middle_purple_gradient_002.png", True),
	"elucidate_right_gradient_001":        _load("images/elucidate_right_gradient_001.png", True),
	"elucidate_right_purple_gradient_001":        _load("images/elucidate_right_purple_gradient_001.png", True),
	
	#MERCENARY DIALOGUE
	"walled_mercenary_with_draft_officer_001":        _load("images/walled_mercenary_with_draft_officer_001.png", True),
	"walled_mercenary_with_draft_officer_002":        _load("images/walled_mercenary_with_draft_officer_002.png", True),
	"walled_mercenary_with_draft_officer_003":        _load("images/walled_mercenary_with_draft_officer_003.png", True),
	"walled_mercenary_with_draft_officer_004":        _load("images/walled_mercenary_with_draft_officer_004.png", True),
	"walled_mercenary_with_draft_officer_005":        _load("images/walled_mercenary_with_draft_officer_005.png", True),
	"walled_mercenary_with_draft_officer_006":        _load("images/walled_mercenary_with_draft_officer_006.png", True),
	"walled_mercenary_with_draft_officer_007":        _load("images/walled_mercenary_with_draft_officer_007.png", True),
	"walled_mercenary_with_draft_officer_008":        _load("images/walled_mercenary_with_draft_officer_008.png", True),
	"walled_mercenary_with_blacksmith_001":        _load("images/walled_mercenary_with_blacksmith_001.png", True),
	"walled_mercenary_with_blacksmith_002":        _load("images/walled_mercenary_with_blacksmith_002.png", True),
	"walled_mercenary_with_blacksmith_003":        _load("images/walled_mercenary_with_blacksmith_003.png", True),
	"walled_mercenary_with_blacksmith_004":        _load("images/walled_mercenary_with_blacksmith_004.png", True),
	"walled_mercenary_with_blacksmith_005":        _load("images/walled_mercenary_with_blacksmith_005.png", True),
	"walled_mercenary_with_blacksmith_006":        _load("images/walled_mercenary_with_blacksmith_006.png", True),
	"walled_mercenary_with_blacksmith_007":        _load("images/walled_mercenary_with_blacksmith_007.png", True),
	"walled_mercenary_with_blacksmith_008":        _load("images/walled_mercenary_with_blacksmith_008.png", True),
	"walled_mercenary_with_blacksmith_009":        _load("images/walled_mercenary_with_blacksmith_009.png", True),
	"walled_mercenary_with_blacksmith_010":        _load("images/walled_mercenary_with_blacksmith_010.png", True),
	"walled_mercenary_with_blacksmith_011":        _load("images/walled_mercenary_with_blacksmith_011.png", True),
	"walled_mercenary_with_blacksmith_012":        _load("images/walled_mercenary_with_blacksmith_012.png", True),
	"walled_mercenary_with_blacksmith_013":        _load("images/walled_mercenary_with_blacksmith_013.png", True),
	"walled_mercenary_with_blacksmith_014":        _load("images/walled_mercenary_with_blacksmith_014.png", True),
	"walled_mercenary_poster_interact_001":        _load("images/walled_mercenary_poster_interact_001.png", True),
	"walled_mercenary_poster_interact_002":        _load("images/walled_mercenary_poster_interact_002.png", True),
	"walled_mercenary_poster_interact_003":        _load("images/walled_mercenary_poster_interact_003.png", True),
	"theocratic_mercenary_with_priest_001":        _load("images/theocratic_mercenary_with_priest_001.png", True),
	"theocratic_mercenary_with_priest_002":        _load("images/theocratic_mercenary_with_priest_002.png", True),
	"theocratic_mercenary_with_priest_003":        _load("images/theocratic_mercenary_with_priest_003.png", True),
	"theocratic_mercenary_with_priest_004":        _load("images/theocratic_mercenary_with_priest_004.png", True),
	"theocratic_mercenary_with_priest_005":        _load("images/theocratic_mercenary_with_priest_005.png", True),
	"theocratic_mercenary_with_priest_006":        _load("images/theocratic_mercenary_with_priest_006.png", True),
	"theocratic_mercenary_with_priest_007":        _load("images/theocratic_mercenary_with_priest_007.png", True),
	"theocratic_mercenary_with_priest_008":        _load("images/theocratic_mercenary_with_priest_008.png", True),
	"theocratic_mercenary_with_priest_009":        _load("images/theocratic_mercenary_with_priest_009.png", True),
	"theocratic_mercenary_with_priest_010":        _load("images/theocratic_mercenary_with_priest_010.png", True),
	"theocratic_mercenary_with_priest_011":        _load("images/theocratic_mercenary_with_priest_011.png", True),
	"theocratic_mercenary_with_priest_012":        _load("images/theocratic_mercenary_with_priest_012.png", True),
	"theocratic_mercenary_with_priest_013":        _load("images/theocratic_mercenary_with_priest_013.png", True),
	"theocratic_mercenary_with_priest_014":        _load("images/theocratic_mercenary_with_priest_014.png", True),
	"theocratic_mercenary_with_priest_015":        _load("images/theocratic_mercenary_with_priest_015.png", True),
	"theocratic_mercenary_with_priest_016":        _load("images/theocratic_mercenary_with_priest_016.png", True),
	"theocratic_mercenary_with_priest_017":        _load("images/theocratic_mercenary_with_priest_017.png", True),
	"theocratic_mercenary_with_priest_018":        _load("images/theocratic_mercenary_with_priest_018.png", True),
	"theocratic_mercenary_with_priest_019":        _load("images/theocratic_mercenary_with_priest_019.png", True),
	"theocratic_mercenary_with_priest_020":        _load("images/theocratic_mercenary_with_priest_020.png", True),
	"theocratic_mercenary_with_priest_021":        _load("images/theocratic_mercenary_with_priest_021.png", True),
	"theocratic_mercenary_with_priest_022":        _load("images/theocratic_mercenary_with_priest_022.png", True),
	"theocratic_mercenary_with_priest_023":        _load("images/theocratic_mercenary_with_priest_023.png", True),
	"theocratic_mercenary_with_priest_024":        _load("images/theocratic_mercenary_with_priest_024.png", True),
	"theocratic_mercenary_with_priest_025":        _load("images/theocratic_mercenary_with_priest_025.png", True),
	"theocratic_mercenary_with_priest_026":        _load("images/theocratic_mercenary_with_priest_026.png", True),
	"theocratic_mercenary_with_priest_027":        _load("images/theocratic_mercenary_with_priest_027.png", True),
	"theocratic_mercenary_with_priest_028":        _load("images/theocratic_mercenary_with_priest_028.png", True),
	"theocratic_mercenary_with_librarian_scholar_001":        _load("images/theocratic_mercenary_with_librarian_scholar_001.png", True),
	"theocratic_mercenary_with_librarian_scholar_002":        _load("images/theocratic_mercenary_with_librarian_scholar_002.png", True),
	"theocratic_mercenary_with_librarian_scholar_003":        _load("images/theocratic_mercenary_with_librarian_scholar_003.png", True),
	"theocratic_mercenary_with_librarian_scholar_004":        _load("images/theocratic_mercenary_with_librarian_scholar_004.png", True),
	"theocratic_mercenary_with_librarian_scholar_005":        _load("images/theocratic_mercenary_with_librarian_scholar_005.png", True),
	"theocratic_mercenary_with_librarian_scholar_006":        _load("images/theocratic_mercenary_with_librarian_scholar_006.png", True),
	"theocratic_mercenary_with_librarian_scholar_007":        _load("images/theocratic_mercenary_with_librarian_scholar_007.png", True),
	"theocratic_mercenary_with_librarian_scholar_008":        _load("images/theocratic_mercenary_with_librarian_scholar_008.png", True),
	"theocratic_mercenary_with_librarian_scholar_009":        _load("images/theocratic_mercenary_with_librarian_scholar_009.png", True),
	"theocratic_mercenary_with_librarian_scholar_010":        _load("images/theocratic_mercenary_with_librarian_scholar_010.png", True),
	"theocratic_mercenary_with_librarian_scholar_011":        _load("images/theocratic_mercenary_with_librarian_scholar_011.png", True),
	"theocratic_mercenary_with_librarian_scholar_012":        _load("images/theocratic_mercenary_with_librarian_scholar_012.png", True),
	"theocratic_mercenary_with_librarian_scholar_013":        _load("images/theocratic_mercenary_with_librarian_scholar_013.png", True),
	"theocratic_mercenary_with_librarian_scholar_014":        _load("images/theocratic_mercenary_with_librarian_scholar_014.png", True),
	"theocratic_mercenary_with_librarian_scholar_015":        _load("images/theocratic_mercenary_with_librarian_scholar_015.png", True),
	"theocratic_mercenary_with_librarian_scholar_016":        _load("images/theocratic_mercenary_with_librarian_scholar_016.png", True),
	"theocratic_mercenary_with_confession_booth_001":        _load("images/theocratic_mercenary_with_confession_booth_001.png", True),
	"theocratic_mercenary_with_confession_booth_002":        _load("images/theocratic_mercenary_with_confession_booth_002.png", True),
	"theocratic_mercenary_with_confession_booth_003":        _load("images/theocratic_mercenary_with_confession_booth_003.png", True),
	"theocratic_mercenary_with_confession_booth_004":        _load("images/theocratic_mercenary_with_confession_booth_004.png", True),
	"theocratic_mercenary_with_confession_booth_005":        _load("images/theocratic_mercenary_with_confession_booth_005.png", True),
	"theocratic_mercenary_with_confession_booth_006":        _load("images/theocratic_mercenary_with_confession_booth_006.png", True),
	"theocratic_battle_mercenary_with_priest_001":        _load("images/theocratic_battle_mercenary_with_priest_001.png", True),
	"theocratic_battle_mercenary_with_priest_002":        _load("images/theocratic_battle_mercenary_with_priest_002.png", True),
	"theocratic_battle_mercenary_with_priest_003":        _load("images/theocratic_battle_mercenary_with_priest_003.png", True),
	"theocratic_battle_mercenary_with_priest_004":        _load("images/theocratic_battle_mercenary_with_priest_004.png", True),
	"theocratic_battle_mercenary_with_priest_005":        _load("images/theocratic_battle_mercenary_with_priest_005.png", True),
	"theocratic_battle_mercenary_with_priest_006":        _load("images/theocratic_battle_mercenary_with_priest_006.png", True),
	"theocratic_battle_mercenary_with_priest_007":        _load("images/theocratic_battle_mercenary_with_priest_007.png", True),
	"theocratic_battle_mercenary_with_priest_008":        _load("images/theocratic_battle_mercenary_with_priest_008.png", True),
	"theocratic_battle_mercenary_with_priest_009":        _load("images/theocratic_battle_mercenary_with_priest_009.png", True),
	"theocratic_battle_mercenary_with_priest_010":        _load("images/theocratic_battle_mercenary_with_priest_010.png", True),
	"theocratic_battle_mercenary_with_priest_011":        _load("images/theocratic_battle_mercenary_with_priest_011.png", True),
	"theocratic_battle_mercenary_with_priest_012":        _load("images/theocratic_battle_mercenary_with_priest_012.png", True),
	"theocratic_battle_mercenary_with_priest_013":        _load("images/theocratic_battle_mercenary_with_priest_013.png", True),
	"theocratic_battle_mercenary_with_priest_014":        _load("images/theocratic_battle_mercenary_with_priest_014.png", True),
	"theocratic_battle_mercenary_with_priest_015":        _load("images/theocratic_battle_mercenary_with_priest_015.png", True),
	"theocratic_battle_mercenary_with_priest_016":        _load("images/theocratic_battle_mercenary_with_priest_016.png", True),
	"theocratic_battle_mercenary_with_priest_017":        _load("images/theocratic_battle_mercenary_with_priest_017.png", True),
	"theocratic_battle_mercenary_with_priest_018":        _load("images/theocratic_battle_mercenary_with_priest_018.png", True),
	"theocratic_battle_mercenary_with_priest_019":        _load("images/theocratic_battle_mercenary_with_priest_019.png", True),
	"theocratic_battle_mercenary_with_priest_020":        _load("images/theocratic_battle_mercenary_with_priest_020.png", True),
	"theocratic_battle_mercenary_with_priest_021":        _load("images/theocratic_battle_mercenary_with_priest_021.png", True),
	"theocratic_battle_mercenary_with_priest_022":        _load("images/theocratic_battle_mercenary_with_priest_022.png", True),
	"theocratic_battle_mercenary_with_priest_023":        _load("images/theocratic_battle_mercenary_with_priest_023.png", True),
	"theocratic_battle_mercenary_with_priest_024":        _load("images/theocratic_battle_mercenary_with_priest_024.png", True),
	"theocratic_battle_mercenary_with_priest_025":        _load("images/theocratic_battle_mercenary_with_priest_025.png", True),
	"theocratic_battle_mercenary_with_priest_026":        _load("images/theocratic_battle_mercenary_with_priest_026.png", True),
	"theocratic_battle_mercenary_with_priest_027":        _load("images/theocratic_battle_mercenary_with_priest_027.png", True),
	"theocratic_battle_mercenary_with_priest_028":        _load("images/theocratic_battle_mercenary_with_priest_028.png", True),
	"theocratic_battle_mercenary_with_priest_029":        _load("images/theocratic_battle_mercenary_with_priest_029.png", True),
	"theocratic_battle_mercenary_with_priest_030":        _load("images/theocratic_battle_mercenary_with_priest_030.png", True),
	"home_village_mercenary_with_memory_001":        _load("images/home_village_mercenary_with_memory_001.png", True),
	"home_village_mercenary_with_memory_002":        _load("images/home_village_mercenary_with_memory_002.png", True),
	"home_village_mercenary_with_memory_003":        _load("images/home_village_mercenary_with_memory_003.png", True),
	"home_village_mercenary_with_memory_004":        _load("images/home_village_mercenary_with_memory_004.png", True),
	"home_village_mercenary_with_memory_005":        _load("images/home_village_mercenary_with_memory_005.png", True),
	"home_village_mercenary_with_memory_006":        _load("images/home_village_mercenary_with_memory_006.png", True),
	"home_village_mercenary_with_memory_007":        _load("images/home_village_mercenary_with_memory_007.png", True),
	"home_village_mercenary_with_memory_008":        _load("images/home_village_mercenary_with_memory_008.png", True),
	"home_village_mercenary_with_memory_009":        _load("images/home_village_mercenary_with_memory_009.png", True),
	"home_village_mercenary_with_memory_010":        _load("images/home_village_mercenary_with_memory_010.png", True),
	"home_village_mercenary_with_memory_011":        _load("images/home_village_mercenary_with_memory_011.png", True),
	"home_village_mercenary_with_memory_012":        _load("images/home_village_mercenary_with_memory_012.png", True),
	"home_village_mercenary_with_memory_013":        _load("images/home_village_mercenary_with_memory_013.png", True),
	"home_village_mercenary_with_memory_014":        _load("images/home_village_mercenary_with_memory_014.png", True),
	"home_village_mercenary_with_memory_015":        _load("images/home_village_mercenary_with_memory_015.png", True),
	"home_village_mercenary_with_memory_016":        _load("images/home_village_mercenary_with_memory_016.png", True),
	"home_village_mercenary_with_memory_017":        _load("images/home_village_mercenary_with_memory_017.png", True),
	"home_village_mercenary_with_memory_018":        _load("images/home_village_mercenary_with_memory_018.png", True),
	"home_village_mercenary_with_memory_019":        _load("images/home_village_mercenary_with_memory_019.png", True),
	"home_village_mercenary_with_memory_020":        _load("images/home_village_mercenary_with_memory_020.png", True),
	"home_village_mercenary_with_memory_021":        _load("images/home_village_mercenary_with_memory_021.png", True),
	"home_village_mercenary_with_memory_022":        _load("images/home_village_mercenary_with_memory_022.png", True),
	"home_village_mercenary_with_memory_023":        _load("images/home_village_mercenary_with_memory_023.png", True),
	"home_village_mercenary_with_memory_024":        _load("images/home_village_mercenary_with_memory_024.png", True),
	"home_village_mercenary_with_memory_025":        _load("images/home_village_mercenary_with_memory_025.png", True),
	"home_village_mercenary_with_memory_026":        _load("images/home_village_mercenary_with_memory_026.png", True),
	"home_village_mercenary_with_memory_027":        _load("images/home_village_mercenary_with_memory_027.png", True),
	"outskirts_village_mercenary_with_village_chief_001":        _load("images/outskirts_village_mercenary_with_village_chief_001.png", True),
	"outskirts_village_mercenary_with_village_chief_002":        _load("images/outskirts_village_mercenary_with_village_chief_002.png", True),
	"outskirts_village_mercenary_with_village_chief_003":        _load("images/outskirts_village_mercenary_with_village_chief_003.png", True),
	"outskirts_village_mercenary_with_village_chief_004":        _load("images/outskirts_village_mercenary_with_village_chief_004.png", True),
	"outskirts_village_mercenary_with_village_chief_005":        _load("images/outskirts_village_mercenary_with_village_chief_005.png", True),
	"outskirts_village_mercenary_with_village_chief_006":        _load("images/outskirts_village_mercenary_with_village_chief_006.png", True),
	"outskirts_village_mercenary_with_village_chief_007":        _load("images/outskirts_village_mercenary_with_village_chief_007.png", True),
	"outskirts_village_mercenary_with_village_chief_008":        _load("images/outskirts_village_mercenary_with_village_chief_008.png", True),
	"outskirts_village_mercenary_with_village_chief_009":        _load("images/outskirts_village_mercenary_with_village_chief_009.png", True),
	"outskirts_village_mercenary_with_village_chief_010":        _load("images/outskirts_village_mercenary_with_village_chief_010.png", True),
	"outskirts_village_mercenary_with_village_chief_011":        _load("images/outskirts_village_mercenary_with_village_chief_011.png", True),
	"outskirts_market_mercenary_with_village_market_001":        _load("images/outskirts_market_mercenary_with_village_market_001.png", True),
	"outskirts_market_mercenary_with_village_market_002":        _load("images/outskirts_market_mercenary_with_village_market_002.png", True),
	"outskirts_market_mercenary_with_village_market_003":        _load("images/outskirts_market_mercenary_with_village_market_003.png", True),
	"outskirts_market_mercenary_with_village_market_004":        _load("images/outskirts_market_mercenary_with_village_market_004.png", True),
	"outskirts_market_mercenary_with_village_market_005":        _load("images/outskirts_market_mercenary_with_village_market_005.png", True),
	"outskirts_market_mercenary_with_village_market_006":        _load("images/outskirts_market_mercenary_with_village_market_006.png", True),
	"outskirts_market_mercenary_with_village_market_007":        _load("images/outskirts_market_mercenary_with_village_market_007.png", True),
	"outskirts_market_mercenary_with_village_market_008":        _load("images/outskirts_market_mercenary_with_village_market_008.png", True),
	"outskirts_village_mercenary_with_villagers_001":        _load("images/outskirts_village_mercenary_with_villagers_001.png", True),
	"outskirts_village_mercenary_with_villagers_002":        _load("images/outskirts_village_mercenary_with_villagers_002.png", True),
	"outskirts_village_mercenary_with_villagers_003":        _load("images/outskirts_village_mercenary_with_villagers_003.png", True),
	"outskirts_village_mercenary_with_villagers_004":        _load("images/outskirts_village_mercenary_with_villagers_004.png", True),
	"outskirts_village_mercenary_with_villagers_005":        _load("images/outskirts_village_mercenary_with_villagers_005.png", True),
	"outskirts_village_mercenary_with_villagers_006":        _load("images/outskirts_village_mercenary_with_villagers_006.png", True),
	"outskirts_village_mercenary_with_travelling_bard_001":        _load("images/outskirts_village_mercenary_with_travelling_bard_001.png", True),
	"outskirts_village_mercenary_with_travelling_bard_002":        _load("images/outskirts_village_mercenary_with_travelling_bard_002.png", True),
	"outskirts_village_mercenary_with_travelling_bard_003":        _load("images/outskirts_village_mercenary_with_travelling_bard_003.png", True),
	"outskirts_village_mercenary_with_travelling_bard_004":        _load("images/outskirts_village_mercenary_with_travelling_bard_004.png", True),
	"outskirts_village_mercenary_with_travelling_bard_005":        _load("images/outskirts_village_mercenary_with_travelling_bard_005.png", True),
	"outskirts_village_mercenary_with_travelling_bard_006":        _load("images/outskirts_village_mercenary_with_travelling_bard_006.png", True),
	"outskirts_village_mercenary_with_travelling_bard_007":        _load("images/outskirts_village_mercenary_with_travelling_bard_007.png", True),
	"outskirts_village_mercenary_with_travelling_bard_008":        _load("images/outskirts_village_mercenary_with_travelling_bard_008.png", True),
	"outskirts_village_mercenary_with_travelling_bard_009":        _load("images/outskirts_village_mercenary_with_travelling_bard_009.png", True),
	"outskirts_village_mercenary_with_travelling_bard_010":        _load("images/outskirts_village_mercenary_with_travelling_bard_010.png", True),
	"outskirts_village_mercenary_with_travelling_bard_011":        _load("images/outskirts_village_mercenary_with_travelling_bard_011.png", True),
	"outskirts_village_mercenary_with_travelling_bard_012":        _load("images/outskirts_village_mercenary_with_travelling_bard_012.png", True),
	"outskirts_village_mercenary_with_travelling_bard_013":        _load("images/outskirts_village_mercenary_with_travelling_bard_013.png", True),
	"outskirts_village_mercenary_with_travelling_bard_014":        _load("images/outskirts_village_mercenary_with_travelling_bard_014.png", True),
	"outskirts_village_mercenary_with_travelling_bard_015":        _load("images/outskirts_village_mercenary_with_travelling_bard_015.png", True),
	"outskirts_village_mercenary_with_travelling_bard_016":        _load("images/outskirts_village_mercenary_with_travelling_bard_016.png", True),
	"outskirts_village_mercenary_with_travelling_bard_017":        _load("images/outskirts_village_mercenary_with_travelling_bard_017.png", True),
	"outskirts_village_mercenary_with_travelling_bard_018":        _load("images/outskirts_village_mercenary_with_travelling_bard_018.png", True),
	"outskirts_village_mercenary_with_travelling_bard_019":        _load("images/outskirts_village_mercenary_with_travelling_bard_019.png", True),
	"outskirts_village_mercenary_with_travelling_bard_020":        _load("images/outskirts_village_mercenary_with_travelling_bard_020.png", True),
	"outskirts_village_mercenary_with_travelling_bard_021":        _load("images/outskirts_village_mercenary_with_travelling_bard_021.png", True),
	"zone_terror_mercenary_to_himself_001":        _load("images/zone_terror_mercenary_to_himself_001.png", True),
	"zone_terror_mercenary_to_himself_002":        _load("images/zone_terror_mercenary_to_himself_002.png", True),
	"zone_terror_mercenary_to_himself_003":        _load("images/zone_terror_mercenary_to_himself_003.png", True),
	"zone_terror_mercenary_to_himself_004":        _load("images/zone_terror_mercenary_to_himself_004.png", True),
	"zone_terror_mercenary_to_himself_005":        _load("images/zone_terror_mercenary_to_himself_005.png", True),
	"tribe_perimeter_mercenary_with_tribe_elder_001":        _load("images/tribe_perimeter_mercenary_with_tribe_elder_001.png", True),
	"tribe_perimeter_mercenary_with_tribe_elder_002":        _load("images/tribe_perimeter_mercenary_with_tribe_elder_002.png", True),
	"tribe_perimeter_mercenary_with_tribe_elder_003":        _load("images/tribe_perimeter_mercenary_with_tribe_elder_003.png", True),
	"tribe_perimeter_mercenary_with_tribe_elder_004":        _load("images/tribe_perimeter_mercenary_with_tribe_elder_004.png", True),
	"tribe_perimeter_mercenary_with_tribe_elder_005":        _load("images/tribe_perimeter_mercenary_with_tribe_elder_005.png", True),
	"tribe_perimeter_mercenary_with_tribe_elder_006":        _load("images/tribe_perimeter_mercenary_with_tribe_elder_006.png", True),
	"tribe_perimeter_mercenary_with_tribe_elder_007":        _load("images/tribe_perimeter_mercenary_with_tribe_elder_007.png", True),
	"tribe_perimeter_mercenary_with_tribe_elder_008":        _load("images/tribe_perimeter_mercenary_with_tribe_elder_008.png", True),
	"tribe_perimeter_mercenary_with_tribe_elder_009":        _load("images/tribe_perimeter_mercenary_with_tribe_elder_009.png", True),
	"tribe_perimeter_mercenary_with_tribe_elder_010":        _load("images/tribe_perimeter_mercenary_with_tribe_elder_010.png", True),
	"tribe_perimeter_mercenary_with_tribe_elder_011":        _load("images/tribe_perimeter_mercenary_with_tribe_elder_011.png", True),
	"tribe_perimeter_mercenary_with_tribe_elder_012":        _load("images/tribe_perimeter_mercenary_with_tribe_elder_012.png", True),
	"tribe_perimeter_warrior_with_assassin_001":        _load("images/tribe_perimeter_warrior_with_assassin_001.png", True),
	"tribe_perimeter_warrior_with_assassin_002":        _load("images/tribe_perimeter_warrior_with_assassin_002.png", True),
	"tribe_perimeter_warrior_with_assassin_003":        _load("images/tribe_perimeter_warrior_with_assassin_003.png", True),
	"tribe_perimeter_warrior_with_assassin_004":        _load("images/tribe_perimeter_warrior_with_assassin_004.png", True),
	"tribe_perimeter_warrior_with_assassin_005":        _load("images/tribe_perimeter_warrior_with_assassin_005.png", True),
	"tribe_storage_mercenary_with_shaman_001":        _load("images/tribe_storage_mercenary_with_shaman_001.png", True),
	"tribe_storage_mercenary_with_shaman_002":        _load("images/tribe_storage_mercenary_with_shaman_002.png", True),
	"tribe_storage_mercenary_with_shaman_003":        _load("images/tribe_storage_mercenary_with_shaman_003.png", True),
	"tribe_storage_mercenary_with_shaman_004":        _load("images/tribe_storage_mercenary_with_shaman_004.png", True),
	"tribe_storage_mercenary_with_shaman_005":        _load("images/tribe_storage_mercenary_with_shaman_005.png", True),
	"tribe_storage_mercenary_with_shaman_006":        _load("images/tribe_storage_mercenary_with_shaman_006.png", True),
	"tribe_storage_mercenary_with_shaman_007":        _load("images/tribe_storage_mercenary_with_shaman_007.png", True),
	"tribe_storage_mercenary_with_shaman_008":        _load("images/tribe_storage_mercenary_with_shaman_008.png", True),
	"tribe_storage_mercenary_with_shaman_009":        _load("images/tribe_storage_mercenary_with_shaman_009.png", True),
	"tribe_storage_mercenary_with_shaman_010":        _load("images/tribe_storage_mercenary_with_shaman_010.png", True),
	"tribe_storage_mercenary_with_shaman_011":        _load("images/tribe_storage_mercenary_with_shaman_011.png", True),
	"tribe_storage_mercenary_with_shaman_012":        _load("images/tribe_storage_mercenary_with_shaman_012.png", True),
	"tribe_storage_mercenary_with_shaman_013":        _load("images/tribe_storage_mercenary_with_shaman_013.png", True),
	"tribe_storage_mercenary_with_shaman_014":        _load("images/tribe_storage_mercenary_with_shaman_014.png", True),
	"tribe_storage_mercenary_with_shaman_015":        _load("images/tribe_storage_mercenary_with_shaman_015.png", True),
	"tribe_storage_mercenary_with_shaman_016":        _load("images/tribe_storage_mercenary_with_shaman_016.png", True),
	"tribe_storage_mercenary_with_shaman_017":        _load("images/tribe_storage_mercenary_with_shaman_017.png", True),
	"tribe_storage_mercenary_with_shaman_018":        _load("images/tribe_storage_mercenary_with_shaman_018.png", True),
	"tribe_storage_mercenary_with_shaman_019":        _load("images/tribe_storage_mercenary_with_shaman_019.png", True),
	"tribe_storage_mercenary_with_shaman_020":        _load("images/tribe_storage_mercenary_with_shaman_020.png", True),
	"tribe_storage_mercenary_with_shaman_021":        _load("images/tribe_storage_mercenary_with_shaman_021.png", True),
	"tribe_storage_mercenary_with_shaman_022":        _load("images/tribe_storage_mercenary_with_shaman_022.png", True),
	"tribe_tunnel_mercenary_with_tibe_chief_001":        _load("images/tribe_tunnel_mercenary_with_tibe_chief_001.png", True),
	"tribe_tunnel_mercenary_with_tibe_chief_002":        _load("images/tribe_tunnel_mercenary_with_tibe_chief_002.png", True),
	"tribe_tunnel_mercenary_with_tibe_chief_003":        _load("images/tribe_tunnel_mercenary_with_tibe_chief_003.png", True),
	"tribe_tunnel_mercenary_with_tibe_chief_004":        _load("images/tribe_tunnel_mercenary_with_tibe_chief_004.png", True),
	"tribe_tunnel_mercenary_with_tibe_chief_005":        _load("images/tribe_tunnel_mercenary_with_tibe_chief_005.png", True),
	"zone_terror_mercenary_with_shaman_001":        _load("images/zone_terror_mercenary_with_shaman_001.png", True),
	"zone_terror_mercenary_with_shaman_002":        _load("images/zone_terror_mercenary_with_shaman_002.png", True),
	"zone_terror_mercenary_with_shaman_003":        _load("images/zone_terror_mercenary_with_shaman_003.png", True),
	"zone_terror_mercenary_with_shaman_004":        _load("images/zone_terror_mercenary_with_shaman_004.png", True),
	"zone_terror_mercenary_with_shaman_005":        _load("images/zone_terror_mercenary_with_shaman_005.png", True),
	"zone_terror_mercenary_with_shaman_006":        _load("images/zone_terror_mercenary_with_shaman_006.png", True),
	"zone_terror_mercenary_with_shaman_007":        _load("images/zone_terror_mercenary_with_shaman_007.png", True),
	"zone_terror_mercenary_with_shaman_008":        _load("images/zone_terror_mercenary_with_shaman_008.png", True),
	"zone_terror_mercenary_with_shaman_009":        _load("images/zone_terror_mercenary_with_shaman_009.png", True),
	"zone_terror_mercenary_with_shaman_010":        _load("images/zone_terror_mercenary_with_shaman_010.png", True),
	"zone_terror_mercenary_with_shaman_011":        _load("images/zone_terror_mercenary_with_shaman_011.png", True),
	"zone_terror_mercenary_with_shaman_012":        _load("images/zone_terror_mercenary_with_shaman_012.png", True),
	"zone_terror_mercenary_with_shaman_013":        _load("images/zone_terror_mercenary_with_shaman_013.png", True),
	"zone_terror_mercenary_with_shaman_014":        _load("images/zone_terror_mercenary_with_shaman_014.png", True),
	"zone_terror_mercenary_with_shaman_015":        _load("images/zone_terror_mercenary_with_shaman_015.png", True),
	"zone_terror_mercenary_with_shaman_016":        _load("images/zone_terror_mercenary_with_shaman_016.png", True),
	"zone_terror_mercenary_with_shaman_017":        _load("images/zone_terror_mercenary_with_shaman_017.png", True),
	"port_city_mercenary_with_merchant_001":        _load("images/port_city_mercenary_with_merchant_001.png", True),
	"port_city_mercenary_with_merchant_002":        _load("images/port_city_mercenary_with_merchant_002.png", True),
	"port_city_mercenary_with_merchant_003":        _load("images/port_city_mercenary_with_merchant_003.png", True),
	"port_city_mercenary_with_merchant_004":        _load("images/port_city_mercenary_with_merchant_004.png", True),
	"port_city_mercenary_with_merchant_005":        _load("images/port_city_mercenary_with_merchant_005.png", True),
	"port_city_mercenary_with_merchant_006":        _load("images/port_city_mercenary_with_merchant_006.png", True),
	"port_city_mercenary_with_merchant_007":        _load("images/port_city_mercenary_with_merchant_007.png", True),
	"port_city_mercenary_with_merchant_008":        _load("images/port_city_mercenary_with_merchant_008.png", True),
	"port_city_mercenary_with_merchant_009":        _load("images/port_city_mercenary_with_merchant_009.png", True),
	"port_city_mercenary_with_merchant_010":        _load("images/port_city_mercenary_with_merchant_010.png", True),
	"port_city_mercenary_with_merchant_011":        _load("images/port_city_mercenary_with_merchant_011.png", True),
	"port_city_mercenary_with_merchant_012":        _load("images/port_city_mercenary_with_merchant_012.png", True),
	"port_city_mercenary_with_merchant_013":        _load("images/port_city_mercenary_with_merchant_013.png", True),
	"port_city_mercenary_with_merchant_014":        _load("images/port_city_mercenary_with_merchant_014.png", True),
	"port_city_mercenary_with_merchant_015":        _load("images/port_city_mercenary_with_merchant_015.png", True),
	"port_city_mercenary_with_merchant_016":        _load("images/port_city_mercenary_with_merchant_016.png", True),
	"port_city_mercenary_with_merchant_017":        _load("images/port_city_mercenary_with_merchant_017.png", True),
	"port_city_mercenary_with_merchant_018":        _load("images/port_city_mercenary_with_merchant_018.png", True),
	"port_city_mercenary_with_merchant_019":        _load("images/port_city_mercenary_with_merchant_019.png", True),
	"port_city_mercenary_with_merchant_020":        _load("images/port_city_mercenary_with_merchant_020.png", True),
	"port_city_mercenary_with_merchant_021":        _load("images/port_city_mercenary_with_merchant_021.png", True),
	"port_city_mercenary_with_merchant_022":        _load("images/port_city_mercenary_with_merchant_022.png", True),
	"port_city_mercenary_with_merchant_023":        _load("images/port_city_mercenary_with_merchant_023.png", True),
	"port_city_mercenary_with_merchant_024":        _load("images/port_city_mercenary_with_merchant_024.png", True),
	"port_city_mercenary_with_merchant_025":        _load("images/port_city_mercenary_with_merchant_025.png", True),
	"port_city_mercenary_with_merchant_026":        _load("images/port_city_mercenary_with_merchant_026.png", True),
	"port_city_mercenary_with_merchant_027":        _load("images/port_city_mercenary_with_merchant_027.png", True),
	"port_city_mercenary_with_merchant_028":        _load("images/port_city_mercenary_with_merchant_028.png", True),
	"port_city_mercenary_with_merchant_029":        _load("images/port_city_mercenary_with_merchant_029.png", True),
	"port_city_mercenary_with_merchant_030":        _load("images/port_city_mercenary_with_merchant_030.png", True),
	"port_city_mercenary_with_merchant_031":        _load("images/port_city_mercenary_with_merchant_031.png", True),
	"port_city_mercenary_with_merchant_032":        _load("images/port_city_mercenary_with_merchant_032.png", True),
	"port_city_mercenary_with_merchant_033":        _load("images/port_city_mercenary_with_merchant_033.png", True),
	"port_city_mercenary_with_merchant_034":        _load("images/port_city_mercenary_with_merchant_034.png", True),
	"port_city_mercenary_with_merchant_035":        _load("images/port_city_mercenary_with_merchant_035.png", True),
	"port_city_mercenary_with_merchant_036":        _load("images/port_city_mercenary_with_merchant_036.png", True),
	"port_city_mercenary_with_merchant_037":        _load("images/port_city_mercenary_with_merchant_037.png", True),
	"port_city_mercenary_decision_node_001":        _load("images/port_city_mercenary_decision_node_001.png", True),
	"port_city_mercenary_decision_node_002":        _load("images/port_city_mercenary_decision_node_002.png", True),
	"port_city_mercenary_decision_node_003":        _load("images/port_city_mercenary_decision_node_003.png", True),
	"port_city_mercenary_response_node_001":        _load("images/port_city_mercenary_response_node_001.png", True),
	"port_city_mercenary_response_node_002":        _load("images/port_city_mercenary_response_node_002.png", True),
	"port_city_mercenary_response_node_003":        _load("images/port_city_mercenary_response_node_003.png", True),
	"port_city_mercenary_with_tavern_keeper_001":        _load("images/port_city_mercenary_with_tavern_keeper_001.png", True),
	"port_city_mercenary_with_tavern_keeper_002":        _load("images/port_city_mercenary_with_tavern_keeper_002.png", True),
	"port_city_mercenary_with_tavern_keeper_003":        _load("images/port_city_mercenary_with_tavern_keeper_003.png", True),
	"port_city_mercenary_with_tavern_keeper_004":        _load("images/port_city_mercenary_with_tavern_keeper_004.png", True),
	"port_city_mercenary_with_tavern_keeper_005":        _load("images/port_city_mercenary_with_tavern_keeper_005.png", True),
	"port_city_mercenary_with_tavern_keeper_006":        _load("images/port_city_mercenary_with_tavern_keeper_006.png", True),
	"port_city_mercenary_with_tavern_keeper_007":        _load("images/port_city_mercenary_with_tavern_keeper_007.png", True),
	"port_city_mercenary_with_tavern_keeper_008":        _load("images/port_city_mercenary_with_tavern_keeper_008.png", True),
	"port_city_mercenary_with_tavern_keeper_009":        _load("images/port_city_mercenary_with_tavern_keeper_009.png", True),
	"port_city_mercenary_with_tavern_keeper_010":        _load("images/port_city_mercenary_with_tavern_keeper_010.png", True),
	"port_city_mercenary_with_tavern_keeper_011":        _load("images/port_city_mercenary_with_tavern_keeper_011.png", True),
	"port_city_mercenary_with_tavern_keeper_012":        _load("images/port_city_mercenary_with_tavern_keeper_012.png", True),
	"port_city_mercenary_with_tavern_keeper_013":        _load("images/port_city_mercenary_with_tavern_keeper_013.png", True),
	"port_city_mercenary_with_tavern_keeper_014":        _load("images/port_city_mercenary_with_tavern_keeper_014.png", True),
	"port_city_mercenary_with_tavern_keeper_015":        _load("images/port_city_mercenary_with_tavern_keeper_015.png", True),
	"port_city_mercenary_with_tavern_keeper_016":        _load("images/port_city_mercenary_with_tavern_keeper_016.png", True),
	"port_city_mercenary_with_tavern_keeper_017":        _load("images/port_city_mercenary_with_tavern_keeper_017.png", True),
	"port_city_mercenary_with_harbor_captain_001":        _load("images/port_city_mercenary_with_harbor_captain_001.png", True),
	"port_city_mercenary_with_harbor_captain_002":        _load("images/port_city_mercenary_with_harbor_captain_002.png", True),
	"port_city_mercenary_with_harbor_captain_003":        _load("images/port_city_mercenary_with_harbor_captain_003.png", True),
	"port_city_mercenary_with_harbor_captain_004":        _load("images/port_city_mercenary_with_harbor_captain_004.png", True),
	"port_city_mercenary_with_harbor_captain_005":        _load("images/port_city_mercenary_with_harbor_captain_005.png", True),
	"port_city_mercenary_with_harbor_captain_006":        _load("images/port_city_mercenary_with_harbor_captain_006.png", True),
	"port_city_mercenary_with_harbor_captain_007":        _load("images/port_city_mercenary_with_harbor_captain_007.png", True),
	"port_city_mercenary_with_harbor_captain_008":        _load("images/port_city_mercenary_with_harbor_captain_008.png", True),
	"cultist_island_mercenary_with_cultist_soldier_001":        _load("images/cultist_island_mercenary_with_cultist_soldier_001.png", True),
	"cultist_island_mercenary_with_cultist_soldier_002":        _load("images/cultist_island_mercenary_with_cultist_soldier_002.png", True),
	"cultist_island_mercenary_with_cultist_soldier_003":        _load("images/cultist_island_mercenary_with_cultist_soldier_003.png", True),
	"cultist_island_mercenary_with_cultist_soldier_004":        _load("images/cultist_island_mercenary_with_cultist_soldier_004.png", True),
	"cultist_island_mercenary_with_cultist_priest_001":        _load("images/cultist_island_mercenary_with_cultist_priest_001.png", True),
	"cultist_island_mercenary_with_cultist_priest_002":        _load("images/cultist_island_mercenary_with_cultist_priest_002.png", True),
	"cultist_island_mercenary_with_cultist_priest_003":        _load("images/cultist_island_mercenary_with_cultist_priest_003.png", True),
	"cultist_island_mercenary_with_cultist_priest_004":        _load("images/cultist_island_mercenary_with_cultist_priest_004.png", True),
	"cultist_island_mercenary_with_experiments_001":        _load("images/cultist_island_mercenary_with_experiments_001.png", True),
	"cultist_island_mercenary_with_experiments_002":        _load("images/cultist_island_mercenary_with_experiments_002.png", True),
	"cultist_island_mercenary_with_experiments_003":        _load("images/cultist_island_mercenary_with_experiments_003.png", True),
	"cultist_island_mercenary_with_experiments_004":        _load("images/cultist_island_mercenary_with_experiments_004.png", True),
	"cultist_island_mercenary_with_experiments_005":        _load("images/cultist_island_mercenary_with_experiments_005.png", True),
	"cultist_island_mercenary_with_experiments_006":        _load("images/cultist_island_mercenary_with_experiments_006.png", True),
	"cultist_island_mercenary_with_experiments_007":        _load("images/cultist_island_mercenary_with_experiments_007.png", True),
	"cultist_island_mercenary_with_experiments_008":        _load("images/cultist_island_mercenary_with_experiments_008.png", True),
	"cultist_island_mercenary_with_funeris_001":        _load("images/cultist_island_mercenary_with_funeris_001.png", True),
	"cultist_island_mercenary_with_funeris_002":        _load("images/cultist_island_mercenary_with_funeris_002.png", True),
	"cultist_island_mercenary_with_funeris_003":        _load("images/cultist_island_mercenary_with_funeris_003.png", True),
	"cultist_island_mercenary_with_funeris_004":        _load("images/cultist_island_mercenary_with_funeris_004.png", True),
	"cultist_island_mercenary_with_funeris_005":        _load("images/cultist_island_mercenary_with_funeris_005.png", True),
	"cultist_island_mercenary_with_funeris_006":        _load("images/cultist_island_mercenary_with_funeris_006.png", True),
	"cultist_island_mercenary_with_funeris_007":        _load("images/cultist_island_mercenary_with_funeris_007.png", True),
	"cultist_island_mercenary_with_funeris_008":        _load("images/cultist_island_mercenary_with_funeris_008.png", True),
	"cultist_island_mercenary_with_funeris_009":        _load("images/cultist_island_mercenary_with_funeris_009.png", True),
	"cultist_island_mercenary_with_funeris_010":        _load("images/cultist_island_mercenary_with_funeris_010.png", True),
	"cultist_island_mercenary_with_funeris_011":        _load("images/cultist_island_mercenary_with_funeris_011.png", True),
	"cultist_island_mercenary_with_funeris_012":        _load("images/cultist_island_mercenary_with_funeris_012.png", True),
	"cultist_island_mercenary_with_funeris_013":        _load("images/cultist_island_mercenary_with_funeris_013.png", True),
	"cultist_island_mercenary_with_funeris_014":        _load("images/cultist_island_mercenary_with_funeris_014.png", True),
	"cultist_island_mercenary_with_funeris_015":        _load("images/cultist_island_mercenary_with_funeris_015.png", True),
	"cultist_island_mercenary_with_funeris_016":        _load("images/cultist_island_mercenary_with_funeris_016.png", True),
	"cultist_island_mercenary_with_funeris_017":        _load("images/cultist_island_mercenary_with_funeris_017.png", True),
	"cultist_island_mercenary_with_funeris_018":        _load("images/cultist_island_mercenary_with_funeris_018.png", True),
	"cultist_island_mercenary_with_funeris_019":        _load("images/cultist_island_mercenary_with_funeris_019.png", True),
	"cultist_island_mercenary_with_funeris_020":        _load("images/cultist_island_mercenary_with_funeris_020.png", True),
	"cultist_island_mercenary_with_funeris_021":        _load("images/cultist_island_mercenary_with_funeris_021.png", True),
	"cultist_island_mercenary_with_funeris_022":        _load("images/cultist_island_mercenary_with_funeris_022.png", True),
	"cultist_island_mercenary_with_funeris_023":        _load("images/cultist_island_mercenary_with_funeris_023.png", True),
	"cultist_island_mercenary_with_funeris_024":        _load("images/cultist_island_mercenary_with_funeris_024.png", True),
	"cultist_island_mercenary_with_funeris_025":        _load("images/cultist_island_mercenary_with_funeris_025.png", True),
	"cultist_island_mercenary_with_funeris_026":        _load("images/cultist_island_mercenary_with_funeris_026.png", True),
	"cultist_island_mercenary_with_funeris_027":        _load("images/cultist_island_mercenary_with_funeris_027.png", True),
	"cultist_island_mercenary_with_funeris_028":        _load("images/cultist_island_mercenary_with_funeris_028.png", True),
	"cultist_island_mercenary_with_funeris_029":        _load("images/cultist_island_mercenary_with_funeris_029.png", True),
	"cultist_island_mercenary_with_funeris_030":        _load("images/cultist_island_mercenary_with_funeris_030.png", True),
	"cultist_island_mercenary_with_cult_leader_001":        _load("images/cultist_island_mercenary_with_cult_leader_001.png", True),
	"cultist_island_mercenary_with_cult_leader_002":        _load("images/cultist_island_mercenary_with_cult_leader_002.png", True),
	"cultist_island_mercenary_with_cult_leader_003":        _load("images/cultist_island_mercenary_with_cult_leader_003.png", True),
	"cultist_island_mercenary_with_cult_leader_004":        _load("images/cultist_island_mercenary_with_cult_leader_004.png", True),
	"cultist_island_mercenary_with_cult_leader_005":        _load("images/cultist_island_mercenary_with_cult_leader_005.png", True),
	"cultist_island_mercenary_with_cult_leader_006":        _load("images/cultist_island_mercenary_with_cult_leader_006.png", True),
	"cultist_island_mercenary_with_cult_leader_007":        _load("images/cultist_island_mercenary_with_cult_leader_007.png", True),
	"cultist_island_mercenary_with_cult_leader_008":        _load("images/cultist_island_mercenary_with_cult_leader_008.png", True),
	"cultist_island_mercenary_with_cult_leader_009":        _load("images/cultist_island_mercenary_with_cult_leader_009.png", True),
	"cultist_island_mercenary_with_cult_leader_010":        _load("images/cultist_island_mercenary_with_cult_leader_010.png", True),
	"cultist_island_mercenary_with_cult_leader_011":        _load("images/cultist_island_mercenary_with_cult_leader_011.png", True),
	"cultist_island_mercenary_with_cult_leader_012":        _load("images/cultist_island_mercenary_with_cult_leader_012.png", True),
	"cultist_island_mercenary_with_cult_leader_013":        _load("images/cultist_island_mercenary_with_cult_leader_013.png", True),
	"cultist_island_mercenary_with_cult_leader_014":        _load("images/cultist_island_mercenary_with_cult_leader_014.png", True),
	"cultist_island_mercenary_with_cult_leader_015":        _load("images/cultist_island_mercenary_with_cult_leader_015.png", True),
	"cultist_island_mercenary_with_cult_leader_016":        _load("images/cultist_island_mercenary_with_cult_leader_016.png", True),
	"cultist_island_mercenary_with_cult_leader_017":        _load("images/cultist_island_mercenary_with_cult_leader_017.png", True),
	"cultist_island_mercenary_with_cult_leader_018":        _load("images/cultist_island_mercenary_with_cult_leader_018.png", True),
	"cultist_island_mercenary_with_cult_leader_019":        _load("images/cultist_island_mercenary_with_cult_leader_019.png", True),
	"cultist_island_mercenary_with_cult_leader_020":        _load("images/cultist_island_mercenary_with_cult_leader_020.png", True),
	
	#CULTIST DIALOGUE
	"cultist_island_funeris_with_cult_leader_001":        _load("images/cultist_island_funeris_with_cult_leader_001.png", True),
	"cultist_island_funeris_with_cult_leader_002":        _load("images/cultist_island_funeris_with_cult_leader_002.png", True),
	"cultist_island_funeris_with_cult_leader_003":        _load("images/cultist_island_funeris_with_cult_leader_003.png", True),
	"cultist_island_funeris_with_cult_leader_004":        _load("images/cultist_island_funeris_with_cult_leader_004.png", True),
	"cultist_island_funeris_with_cult_leader_005":        _load("images/cultist_island_funeris_with_cult_leader_005.png", True),
	"cultist_island_funeris_with_cult_leader_006":        _load("images/cultist_island_funeris_with_cult_leader_006.png", True),
	"cultist_island_funeris_with_cult_leader_007":        _load("images/cultist_island_funeris_with_cult_leader_007.png", True),
	"cultist_island_funeris_with_cult_leader_008":        _load("images/cultist_island_funeris_with_cult_leader_008.png", True),
	"cultist_island_funeris_with_cult_leader_009":        _load("images/cultist_island_funeris_with_cult_leader_009.png", True),
	"cultist_island_funeris_with_cult_leader_010":        _load("images/cultist_island_funeris_with_cult_leader_010.png", True),
	"cultist_island_funeris_with_cult_leader_011":        _load("images/cultist_island_funeris_with_cult_leader_011.png", True),
	"cultist_island_funeris_with_cult_leader_012":        _load("images/cultist_island_funeris_with_cult_leader_012.png", True),
	"cultist_island_funeris_with_cult_leader_013":        _load("images/cultist_island_funeris_with_cult_leader_013.png", True),
	"cultist_island_funeris_with_cult_leader_014":        _load("images/cultist_island_funeris_with_cult_leader_014.png", True),
	"cultist_island_funeris_with_cult_leader_015":        _load("images/cultist_island_funeris_with_cult_leader_015.png", True),
	"cultist_island_funeris_with_cult_soldiers_001":        _load("images/cultist_island_funeris_with_cult_soldiers_001.png", True),
	"cultist_island_funeris_with_cult_soldiers_002":        _load("images/cultist_island_funeris_with_cult_soldiers_002.png", True),
	"cultist_island_funeris_with_cult_soldiers_003":        _load("images/cultist_island_funeris_with_cult_soldiers_003.png", True),
	"cultist_island_funeris_with_cult_soldiers_004":        _load("images/cultist_island_funeris_with_cult_soldiers_004.png", True),
	"cultist_island_funeris_with_cult_soldiers_005":        _load("images/cultist_island_funeris_with_cult_soldiers_005.png", True),
	"cultist_island_funeris_with_cult_soldiers_006":        _load("images/cultist_island_funeris_with_cult_soldiers_006.png", True),
	"zone_terrors_funeris_to_herself_001":        _load("images/zone_terrors_funeris_to_herself_001.png", True),
	"zone_terrors_funeris_to_herself_002":        _load("images/zone_terrors_funeris_to_herself_002.png", True),
	"zone_terrors_funeris_to_herself_003":        _load("images/zone_terrors_funeris_to_herself_003.png", True),
	"zone_terrors_funeris_to_herself_004":        _load("images/zone_terrors_funeris_to_herself_004.png", True),
	"zone_terrors_funeris_to_herself_005":        _load("images/zone_terrors_funeris_to_herself_005.png", True),
	"zone_terrors_funeris_to_herself_006":        _load("images/zone_terrors_funeris_to_herself_006.png", True),
	"zone_terrors_funeris_to_herself_007":        _load("images/zone_terrors_funeris_to_herself_007.png", True),
	"zone_terrors_funeris_to_herself_008":        _load("images/zone_terrors_funeris_to_herself_008.png", True),
	"zone_terrors_funeris_to_herself_009":        _load("images/zone_terrors_funeris_to_herself_009.png", True),
	"zone_terrors_funeris_to_herself_010":        _load("images/zone_terrors_funeris_to_herself_010.png", True),
	"zone_terrors_funeris_to_herself_011":        _load("images/zone_terrors_funeris_to_herself_011.png", True),
	"zone_terrors_funeris_to_herself_012":        _load("images/zone_terrors_funeris_to_herself_012.png", True),
	"zone_terrors_funeris_to_herself_013":        _load("images/zone_terrors_funeris_to_herself_013.png", True),
	"zone_terrors_funeris_to_herself_014":        _load("images/zone_terrors_funeris_to_herself_014.png", True),
	"home_village_funeris_to_memory_fragment_001":        _load("images/home_village_funeris_to_memory_fragment_001.png", True),
	"home_village_funeris_to_memory_fragment_002":        _load("images/home_village_funeris_to_memory_fragment_002.png", True),
	"home_village_funeris_to_memory_fragment_003":        _load("images/home_village_funeris_to_memory_fragment_003.png", True),
	"home_village_funeris_to_memory_fragment_004":        _load("images/home_village_funeris_to_memory_fragment_004.png", True),
	"home_village_funeris_to_memory_fragment_005":        _load("images/home_village_funeris_to_memory_fragment_005.png", True),
	"home_village_funeris_to_memory_fragment_006":        _load("images/home_village_funeris_to_memory_fragment_006.png", True),
	"home_village_funeris_to_memory_fragment_007":        _load("images/home_village_funeris_to_memory_fragment_007.png", True),
	"home_village_funeris_to_memory_fragment_008":        _load("images/home_village_funeris_to_memory_fragment_008.png", True),
	"home_village_funeris_to_memory_fragment_009":        _load("images/home_village_funeris_to_memory_fragment_009.png", True),
	"home_village_funeris_to_memory_fragment_010":        _load("images/home_village_funeris_to_memory_fragment_010.png", True),
	"home_village_funeris_to_memory_fragment_011":        _load("images/home_village_funeris_to_memory_fragment_011.png", True),
	"home_village_funeris_to_memory_fragment_012":        _load("images/home_village_funeris_to_memory_fragment_012.png", True),
	"home_village_funeris_to_memory_fragment_013":        _load("images/home_village_funeris_to_memory_fragment_013.png", True),
	"home_village_funeris_to_memory_fragment_014":        _load("images/home_village_funeris_to_memory_fragment_014.png", True),
	"home_village_funeris_to_memory_fragment_015":        _load("images/home_village_funeris_to_memory_fragment_015.png", True),
	"home_village_funeris_to_memory_fragment_016":        _load("images/home_village_funeris_to_memory_fragment_016.png", True),
	"home_village_funeris_to_memory_fragment_017":        _load("images/home_village_funeris_to_memory_fragment_017.png", True),
	"home_village_funeris_to_memory_fragment_018":        _load("images/home_village_funeris_to_memory_fragment_018.png", True),
	"home_village_funeris_to_memory_fragment_019":        _load("images/home_village_funeris_to_memory_fragment_019.png", True),
	"home_village_funeris_to_memory_fragment_020":        _load("images/home_village_funeris_to_memory_fragment_020.png", True),
	"home_village_funeris_decision_node_001":        _load("images/home_village_funeris_decision_node_001.png", True),
	"home_village_funeris_decision_node_002":        _load("images/home_village_funeris_decision_node_002.png", True),
	"home_village_funeris_decision_node_003":        _load("images/home_village_funeris_decision_node_003.png", True),
	"home_village_funeris_response_node_001":        _load("images/home_village_funeris_response_node_001.png", True),
	"home_village_funeris_response_node_002":        _load("images/home_village_funeris_response_node_002.png", True),
	"home_village_funeris_response_node_003":        _load("images/home_village_funeris_response_node_003.png", True),
	"laboratory_funeris_with_priest_001":        _load("images/laboratory_funeris_with_priest_001.png", True),
	"laboratory_funeris_with_priest_002":        _load("images/laboratory_funeris_with_priest_002.png", True),
	"laboratory_funeris_with_priest_003":        _load("images/laboratory_funeris_with_priest_003.png", True),
	"laboratory_funeris_with_priest_004":        _load("images/laboratory_funeris_with_priest_004.png", True),
	"laboratory_funeris_with_priest_005":        _load("images/laboratory_funeris_with_priest_005.png", True),
	"laboratory_funeris_with_priest_006":        _load("images/laboratory_funeris_with_priest_006.png", True),
	"laboratory_funeris_with_priest_007":        _load("images/laboratory_funeris_with_priest_007.png", True),
	"laboratory_funeris_with_priest_008":        _load("images/laboratory_funeris_with_priest_008.png", True),
	"laboratory_funeris_with_priest_009":        _load("images/laboratory_funeris_with_priest_009.png", True),
	"laboratory_funeris_with_priest_010":        _load("images/laboratory_funeris_with_priest_010.png", True),
	"laboratory_funeris_with_priest_011":        _load("images/laboratory_funeris_with_priest_011.png", True),
	"laboratory_funeris_with_priest_012":        _load("images/laboratory_funeris_with_priest_012.png", True),
	"laboratory_funeris_with_priest_013":        _load("images/laboratory_funeris_with_priest_013.png", True),
	"laboratory_funeris_with_priest_014":        _load("images/laboratory_funeris_with_priest_014.png", True),
	"laboratory_funeris_with_priest_015":        _load("images/laboratory_funeris_with_priest_015.png", True),
	"laboratory_funeris_with_priest_016":        _load("images/laboratory_funeris_with_priest_016.png", True),
	"laboratory_funeris_with_priest_017":        _load("images/laboratory_funeris_with_priest_017.png", True),
	"laboratory_funeris_with_priest_018":        _load("images/laboratory_funeris_with_priest_018.png", True),
	"laboratory_funeris_with_priest_019":        _load("images/laboratory_funeris_with_priest_019.png", True),
	"laboratory_funeris_with_priest_020":        _load("images/laboratory_funeris_with_priest_020.png", True),
	"laboratory_funeris_with_priest_021":        _load("images/laboratory_funeris_with_priest_021.png", True),
	"laboratory_funeris_with_priest_022":        _load("images/laboratory_funeris_with_priest_022.png", True),
	"laboratory_funeris_with_priest_023":        _load("images/laboratory_funeris_with_priest_023.png", True),
	"laboratory_funeris_with_priest_024":        _load("images/laboratory_funeris_with_priest_024.png", True),
	"laboratory_funeris_with_priest_025":        _load("images/laboratory_funeris_with_priest_025.png", True),
	"laboratory_funeris_with_priest_026":        _load("images/laboratory_funeris_with_priest_026.png", True),
	"laboratory_funeris_with_priest_027":        _load("images/laboratory_funeris_with_priest_027.png", True),
	"laboratory_funeris_with_priest_028":        _load("images/laboratory_funeris_with_priest_028.png", True),
	"laboratory_funeris_with_priest_029":        _load("images/laboratory_funeris_with_priest_029.png", True),
	"laboratory_funeris_with_priest_030":        _load("images/laboratory_funeris_with_priest_030.png", True),
	"laboratory_funeris_with_priest_031":        _load("images/laboratory_funeris_with_priest_031.png", True),
	"laboratory_funeris_with_priest_032":        _load("images/laboratory_funeris_with_priest_032.png", True),
	"laboratory_funeris_with_priest_033":        _load("images/laboratory_funeris_with_priest_033.png", True),
	"laboratory_funeris_with_priest_034":        _load("images/laboratory_funeris_with_priest_034.png", True),
	"laboratory_funeris_with_assassin_001":        _load("images/laboratory_funeris_with_assassin_001.png", True),
	
	#PRIEST DIALOGUE
	"walled_priest_with_draft_officer_001":        _load("images/walled_priest_with_draft_officer_001.png", True),
	"walled_priest_with_draft_officer_002":        _load("images/walled_priest_with_draft_officer_002.png", True),
	"walled_priest_with_draft_officer_003":        _load("images/walled_priest_with_draft_officer_003.png", True),
	"walled_priest_with_draft_officer_004":        _load("images/walled_priest_with_draft_officer_004.png", True),
	"walled_chapel_priest_with_guard_001":        _load("images/walled_chapel_priest_with_guard_001.png", True),
	"walled_chapel_priest_with_guard_002":        _load("images/walled_chapel_priest_with_guard_002.png", True),
	"walled_chapel_priest_with_guard_003":        _load("images/walled_chapel_priest_with_guard_003.png", True),
	"walled_chapel_priest_with_guard_004":        _load("images/walled_chapel_priest_with_guard_004.png", True),
	"walled_chapel_priest_with_guard_005":        _load("images/walled_chapel_priest_with_guard_005.png", True),
	"walled_chapel_priest_with_guard_006":        _load("images/walled_chapel_priest_with_guard_006.png", True),
	"theocratic_priest_with_church_attendance_001":        _load("images/theocratic_priest_with_church_attendance_001.png", True),
	"theocratic_priest_with_church_attendance_002":        _load("images/theocratic_priest_with_church_attendance_002.png", True),
	"theocratic_priest_with_church_attendance_003":        _load("images/theocratic_priest_with_church_attendance_003.png", True),
	"theocratic_priest_with_church_attendance_004":        _load("images/theocratic_priest_with_church_attendance_004.png", True),
	"theocratic_priest_with_church_attendance_005":        _load("images/theocratic_priest_with_church_attendance_005.png", True),
	"theocratic_priest_with_church_attendance_006":        _load("images/theocratic_priest_with_church_attendance_006.png", True),
	"theocratic_priest_with_church_attendance_007":        _load("images/theocratic_priest_with_church_attendance_007.png", True),
	"theocratic_priest_with_church_attendance_008":        _load("images/theocratic_priest_with_church_attendance_008.png", True),
	"theocratic_priest_with_church_attendance_009":        _load("images/theocratic_priest_with_church_attendance_009.png", True),
	"theocratic_priest_with_church_attendance_010":        _load("images/theocratic_priest_with_church_attendance_010.png", True),
	"theocratic_priest_with_church_attendance_011":        _load("images/theocratic_priest_with_church_attendance_011.png", True),
	"theocratic_priest_with_church_attendance_012":        _load("images/theocratic_priest_with_church_attendance_012.png", True),
	"theocratic_priest_with_church_attendance_013":        _load("images/theocratic_priest_with_church_attendance_013.png", True),
	"theocratic_priest_with_church_attendance_014":        _load("images/theocratic_priest_with_church_attendance_014.png", True),
	"theocratic_priest_with_church_attendance_015":        _load("images/theocratic_priest_with_church_attendance_015.png", True),
	"theocratic_priest_with_church_attendance_016":        _load("images/theocratic_priest_with_church_attendance_016.png", True),
	"theocratic_priest_with_church_attendance_017":        _load("images/theocratic_priest_with_church_attendance_017.png", True),
	"theocratic_priest_with_church_attendance_018":        _load("images/theocratic_priest_with_church_attendance_018.png", True),
	"theocratic_priest_with_church_attendance_019":        _load("images/theocratic_priest_with_church_attendance_019.png", True),
	"theocratic_priest_with_church_attendance_020":        _load("images/theocratic_priest_with_church_attendance_020.png", True),
	"theocratic_priest_with_church_official_001":        _load("images/theocratic_priest_with_church_official_001.png", True),
	"theocratic_priest_with_church_official_002":        _load("images/theocratic_priest_with_church_official_002.png", True),
	"theocratic_priest_with_church_official_003":        _load("images/theocratic_priest_with_church_official_003.png", True),
	"theocratic_priest_with_church_official_004":        _load("images/theocratic_priest_with_church_official_004.png", True),
	"theocratic_priest_with_church_official_005":        _load("images/theocratic_priest_with_church_official_005.png", True),
	"theocratic_priest_with_church_official_006":        _load("images/theocratic_priest_with_church_official_006.png", True),
	"theocratic_priest_with_church_official_007":        _load("images/theocratic_priest_with_church_official_007.png", True),
	"theocratic_priest_with_church_official_008":        _load("images/theocratic_priest_with_church_official_008.png", True),
	"theocratic_priest_with_church_official_009":        _load("images/theocratic_priest_with_church_official_009.png", True),
	"theocratic_priest_with_church_official_010":        _load("images/theocratic_priest_with_church_official_010.png", True),
	"theocratic_priest_with_church_official_011":        _load("images/theocratic_priest_with_church_official_011.png", True),
	"theocratic_priest_with_church_official_012":        _load("images/theocratic_priest_with_church_official_012.png", True),
	"theocratic_priest_with_church_official_013":        _load("images/theocratic_priest_with_church_official_013.png", True),
	"theocratic_priest_with_church_official_014":        _load("images/theocratic_priest_with_church_official_014.png", True),
	"theocratic_priest_with_church_official_015":        _load("images/theocratic_priest_with_church_official_015.png", True),
	"theocratic_priest_with_church_official_016":        _load("images/theocratic_priest_with_church_official_016.png", True),
	"theocratic_priest_with_church_official_017":        _load("images/theocratic_priest_with_church_official_017.png", True),
	"theocratic_priest_with_church_official_018":        _load("images/theocratic_priest_with_church_official_018.png", True),
	"laboratory_priest_to_himself_001":        _load("images/laboratory_priest_to_himself_001.png", True),
	"laboratory_priest_to_himself_002":        _load("images/laboratory_priest_to_himself_002.png", True),
	"laboratory_priest_to_himself_003":        _load("images/laboratory_priest_to_himself_003.png", True),
	"laboratory_priest_to_himself_004":        _load("images/laboratory_priest_to_himself_004.png", True),
	"laboratory_priest_to_himself_005":        _load("images/laboratory_priest_to_himself_005.png", True),
	"laboratory_priest_to_himself_006":        _load("images/laboratory_priest_to_himself_006.png", True),
	"laboratory_priest_to_himself_007":        _load("images/laboratory_priest_to_himself_007.png", True),
	"laboratory_priest_to_himself_008":        _load("images/laboratory_priest_to_himself_008.png", True),
	"laboratory_priest_to_himself_009":        _load("images/laboratory_priest_to_himself_009.png", True),
	"laboratory_priest_decision_node_001":        _load("images/laboratory_priest_decision_node_001.png", True),
	"laboratory_priest_decision_node_002":        _load("images/laboratory_priest_decision_node_002.png", True),
	"laboratory_priest_decision_node_003":        _load("images/laboratory_priest_decision_node_003.png", True),
	"laboratory_priest_response_node_001":        _load("images/laboratory_priest_response_node_001.png", True),
	"laboratory_priest_response_node_002":        _load("images/laboratory_priest_response_node_002.png", True),
	"laboratory_priest_response_node_003":        _load("images/laboratory_priest_response_node_003.png", True),
	"zone_terror_priest_with_medical_staff_001":        _load("images/zone_terror_priest_with_medical_staff_001.png", True),
	"zone_terror_priest_with_medical_staff_002":        _load("images/zone_terror_priest_with_medical_staff_002.png", True),
	"zone_terror_priest_with_medical_staff_003":        _load("images/zone_terror_priest_with_medical_staff_003.png", True),
	"zone_terror_priest_with_medical_staff_004":        _load("images/zone_terror_priest_with_medical_staff_004.png", True),
	"zone_terror_priest_with_medical_staff_005":        _load("images/zone_terror_priest_with_medical_staff_005.png", True),
	"zone_terror_priest_with_church_knight_001":        _load("images/zone_terror_priest_with_church_knight_001.png", True),
	"zone_terror_priest_with_church_knight_002":        _load("images/zone_terror_priest_with_church_knight_002.png", True),
	"zone_terror_priest_with_church_knight_003":        _load("images/zone_terror_priest_with_church_knight_003.png", True),
	"zone_terror_priest_with_church_knight_004":        _load("images/zone_terror_priest_with_church_knight_004.png", True),
	"zone_terror_priest_with_church_knight_005":        _load("images/zone_terror_priest_with_church_knight_005.png", True),
	"zone_terror_priest_with_church_knight_006":        _load("images/zone_terror_priest_with_church_knight_006.png", True),
	"zone_terror_priest_with_church_knight_007":        _load("images/zone_terror_priest_with_church_knight_007.png", True),
	"zone_terror_priest_with_church_knight_008":        _load("images/zone_terror_priest_with_church_knight_008.png", True),
	"laboratory_priest_to_medical_staff_001":        _load("images/laboratory_priest_to_medical_staff_001.png", True),
	"laboratory_priest_to_medical_staff_002":        _load("images/laboratory_priest_to_medical_staff_002.png", True),
	"laboratory_priest_to_medical_staff_003":        _load("images/laboratory_priest_to_medical_staff_003.png", True),
	"laboratory_priest_to_medical_staff_004":        _load("images/laboratory_priest_to_medical_staff_004.png", True),
	"laboratory_priest_to_medical_staff_005":        _load("images/laboratory_priest_to_medical_staff_005.png", True),
	"laboratory_priest_to_medical_staff_006":        _load("images/laboratory_priest_to_medical_staff_006.png", True),
	"laboratory_priest_to_medical_staff_007":        _load("images/laboratory_priest_to_medical_staff_007.png", True),
	"laboratory_priest_to_medical_staff_008":        _load("images/laboratory_priest_to_medical_staff_008.png", True),
	"laboratory_priest_to_medical_staff_009":        _load("images/laboratory_priest_to_medical_staff_009.png", True),
	"laboratory_priest_to_medical_staff_010":        _load("images/laboratory_priest_to_medical_staff_010.png", True),
	"laboratory_priest_to_medical_staff_011":        _load("images/laboratory_priest_to_medical_staff_011.png", True),
	"laboratory_priest_to_medical_staff_012":        _load("images/laboratory_priest_to_medical_staff_012.png", True),
	"laboratory_priest_to_medical_staff_013":        _load("images/laboratory_priest_to_medical_staff_013.png", True),
	"laboratory_priest_to_medical_staff_014":        _load("images/laboratory_priest_to_medical_staff_014.png", True),
	"laboratory_priest_to_medical_staff_015":        _load("images/laboratory_priest_to_medical_staff_015.png", True),
	"laboratory_priest_to_medical_staff_016":        _load("images/laboratory_priest_to_medical_staff_016.png", True),
	"laboratory_priest_to_medical_staff_017":        _load("images/laboratory_priest_to_medical_staff_017.png", True),
	"laboratory_priest_to_medical_staff_018":        _load("images/laboratory_priest_to_medical_staff_018.png", True),
	"laboratory_priest_to_medical_staff_019":        _load("images/laboratory_priest_to_medical_staff_019.png", True),
	"laboratory_priest_to_medical_staff_020":        _load("images/laboratory_priest_to_medical_staff_020.png", True),
	"laboratory_priest_to_medical_staff_021":        _load("images/laboratory_priest_to_medical_staff_021.png", True),
	"laboratory_priest_to_medical_staff_022":        _load("images/laboratory_priest_to_medical_staff_022.png", True),
	"laboratory_priest_to_medical_staff_023":        _load("images/laboratory_priest_to_medical_staff_023.png", True),
	"theocratic_battle_priest_with_lucidus_001":        _load("images/theocratic_battle_priest_with_lucidus_001.png", True),
	"theocratic_battle_priest_with_lucidus_002":        _load("images/theocratic_battle_priest_with_lucidus_002.png", True),
	"theocratic_battle_priest_with_lucidus_003":        _load("images/theocratic_battle_priest_with_lucidus_003.png", True),
	"theocratic_battle_priest_with_lucidus_004":        _load("images/theocratic_battle_priest_with_lucidus_004.png", True),
	"theocratic_battle_priest_with_lucidus_005":        _load("images/theocratic_battle_priest_with_lucidus_005.png", True),
	"theocratic_battle_priest_with_lucidus_006":        _load("images/theocratic_battle_priest_with_lucidus_006.png", True),
	
	#SHAMAN DIALOGUE
	"tribe_storage_shaman_with_mercenary_001":        _load("images/tribe_storage_shaman_with_mercenary_001.png", True),
	"tribe_storage_shaman_with_mercenary_002":        _load("images/tribe_storage_shaman_with_mercenary_002.png", True),
	"tribe_storage_shaman_with_mercenary_003":        _load("images/tribe_storage_shaman_with_mercenary_003.png", True),
	"tribe_storage_shaman_with_mercenary_004":        _load("images/tribe_storage_shaman_with_mercenary_004.png", True),
	"tribe_storage_shaman_with_mercenary_005":        _load("images/tribe_storage_shaman_with_mercenary_005.png", True),
	"tribe_storage_shaman_with_mercenary_006":        _load("images/tribe_storage_shaman_with_mercenary_006.png", True),
	"tribe_storage_shaman_with_mercenary_007":        _load("images/tribe_storage_shaman_with_mercenary_007.png", True),
	"tribe_storage_shaman_with_mercenary_008":        _load("images/tribe_storage_shaman_with_mercenary_008.png", True),
	"tribe_storage_shaman_with_mercenary_009":        _load("images/tribe_storage_shaman_with_mercenary_009.png", True),
	"tribe_storage_shaman_with_mercenary_010":        _load("images/tribe_storage_shaman_with_mercenary_010.png", True),
	"tribe_storage_shaman_with_mercenary_011":        _load("images/tribe_storage_shaman_with_mercenary_011.png", True),
	"tribe_storage_shaman_with_mercenary_012":        _load("images/tribe_storage_shaman_with_mercenary_012.png", True),
	"tribe_storage_shaman_with_mercenary_013":        _load("images/tribe_storage_shaman_with_mercenary_013.png", True),
	"tribe_storage_shaman_with_mercenary_014":        _load("images/tribe_storage_shaman_with_mercenary_014.png", True),
	"tribe_storage_shaman_with_mercenary_015":        _load("images/tribe_storage_shaman_with_mercenary_015.png", True),
	"tribe_storage_shaman_with_mercenary_016":        _load("images/tribe_storage_shaman_with_mercenary_016.png", True),
	"tribe_storage_shaman_with_mercenary_017":        _load("images/tribe_storage_shaman_with_mercenary_017.png", True),
	"tribe_storage_shaman_with_mercenary_018":        _load("images/tribe_storage_shaman_with_mercenary_018.png", True),
	"tribe_storage_shaman_with_mercenary_019":        _load("images/tribe_storage_shaman_with_mercenary_019.png", True),
	"tribe_storage_shaman_with_mercenary_020":        _load("images/tribe_storage_shaman_with_mercenary_020.png", True),
	"tribe_storage_shaman_with_mercenary_021":        _load("images/tribe_storage_shaman_with_mercenary_021.png", True),
	"tribe_storage_shaman_with_mercenary_022":        _load("images/tribe_storage_shaman_with_mercenary_022.png", True),
	"tribe_tunnel_shaman_with_tribe_chief_001":        _load("images/tribe_tunnel_shaman_with_tribe_chief_001.png", True),
	"tribe_tunnel_shaman_with_tribe_chief_002":        _load("images/tribe_tunnel_shaman_with_tribe_chief_002.png", True),
	"tribe_tunnel_shaman_with_tribe_chief_003":        _load("images/tribe_tunnel_shaman_with_tribe_chief_003.png", True),
	"tribe_tunnel_shaman_with_tribe_chief_004":        _load("images/tribe_tunnel_shaman_with_tribe_chief_004.png", True),
	"tribe_tunnel_shaman_with_mercenary_001":        _load("images/tribe_tunnel_shaman_with_mercenary_001.png", True),
	"tribe_tunnel_shaman_with_mercenary_002":        _load("images/tribe_tunnel_shaman_with_mercenary_002.png", True),
	"tribe_tunnel_shaman_with_mercenary_003":        _load("images/tribe_tunnel_shaman_with_mercenary_003.png", True),
	"tribe_tunnel_shaman_with_mercenary_004":        _load("images/tribe_tunnel_shaman_with_mercenary_004.png", True),
	"tribe_tunnel_shaman_with_mercenary_005":        _load("images/tribe_tunnel_shaman_with_mercenary_005.png", True),
	"tribe_tunnel_shaman_with_mercenary_006":        _load("images/tribe_tunnel_shaman_with_mercenary_006.png", True),
	"tribe_tunnel_shaman_with_mercenary_007":        _load("images/tribe_tunnel_shaman_with_mercenary_007.png", True),
	"tribe_tunnel_shaman_with_mercenary_008":        _load("images/tribe_tunnel_shaman_with_mercenary_008.png", True),
	"tribe_tunnel_shaman_with_mercenary_009":        _load("images/tribe_tunnel_shaman_with_mercenary_009.png", True),
	"tribe_tunnel_shaman_with_mercenary_010":        _load("images/tribe_tunnel_shaman_with_mercenary_010.png", True),
	"tribe_tunnel_shaman_with_mercenary_011":        _load("images/tribe_tunnel_shaman_with_mercenary_011.png", True),
	"tribe_tunnel_shaman_with_mercenary_012":        _load("images/tribe_tunnel_shaman_with_mercenary_012.png", True),
	"tribe_shaman_foresight_low_001":        _load("images/tribe_shaman_foresight_low_001.png", True),
	"tribe_shaman_foresight_low_002":        _load("images/tribe_shaman_foresight_low_002.png", True),
	"tribe_shaman_foresight_low_003":        _load("images/tribe_shaman_foresight_low_003.png", True),
	"tribe_shaman_foresight_mid_001":        _load("images/tribe_shaman_foresight_mid_001.png", True),
	"tribe_shaman_foresight_mid_002":        _load("images/tribe_shaman_foresight_mid_002.png", True),
	"tribe_shaman_foresight_mid_003":        _load("images/tribe_shaman_foresight_mid_003.png", True),
	"tribe_shaman_foresight_high_001":        _load("images/tribe_shaman_foresight_high_001.png", True),
	"tribe_shaman_foresight_high_002":        _load("images/tribe_shaman_foresight_high_002.png", True),
	"tribe_shaman_foresight_high_003":        _load("images/tribe_shaman_foresight_high_003.png", True),
	"tribe_shaman_foresight_high_004":        _load("images/tribe_shaman_foresight_high_004.png", True),
	"tribe_shaman_foresight_high_005":        _load("images/tribe_shaman_foresight_high_005.png", True),
	"zone_terror_shaman_with_mercenary_001":        _load("images/zone_terror_shaman_with_mercenary_001.png", True),
	"zone_terror_shaman_with_mercenary_002":        _load("images/zone_terror_shaman_with_mercenary_002.png", True),
	"zone_terror_shaman_with_mercenary_003":        _load("images/zone_terror_shaman_with_mercenary_003.png", True),
	"zone_terror_shaman_with_mercenary_004":        _load("images/zone_terror_shaman_with_mercenary_004.png", True),
	"zone_terror_shaman_with_mercenary_005":        _load("images/zone_terror_shaman_with_mercenary_005.png", True),
	"zone_terror_shaman_with_mercenary_006":        _load("images/zone_terror_shaman_with_mercenary_006.png", True),
	"zone_terror_shaman_with_mercenary_007":        _load("images/zone_terror_shaman_with_mercenary_007.png", True),
	"zone_terror_shaman_with_mercenary_008":        _load("images/zone_terror_shaman_with_mercenary_008.png", True),
	"zone_terror_shaman_with_mercenary_009":        _load("images/zone_terror_shaman_with_mercenary_009.png", True),
	"zone_terror_shaman_with_mercenary_010":        _load("images/zone_terror_shaman_with_mercenary_010.png", True),
	"zone_terror_shaman_with_mercenary_011":        _load("images/zone_terror_shaman_with_mercenary_011.png", True),
	"zone_terror_shaman_with_mercenary_012":        _load("images/zone_terror_shaman_with_mercenary_012.png", True),
	"zone_terror_shaman_with_mercenary_013":        _load("images/zone_terror_shaman_with_mercenary_013.png", True),
	"zone_terror_shaman_with_mercenary_014":        _load("images/zone_terror_shaman_with_mercenary_014.png", True),
	"zone_terror_shaman_with_mercenary_015":        _load("images/zone_terror_shaman_with_mercenary_015.png", True),
	"zone_terror_shaman_with_mercenary_016":        _load("images/zone_terror_shaman_with_mercenary_016.png", True),
	"zone_terror_shaman_with_mercenary_017":        _load("images/zone_terror_shaman_with_mercenary_017.png", True),
	"zone_terror_shaman_with_mercenary_018":        _load("images/zone_terror_shaman_with_mercenary_018.png", True),
	"zone_terror_shaman_with_mercenary_019":        _load("images/zone_terror_shaman_with_mercenary_019.png", True),
	"zone_terror_shaman_with_mercenary_020":        _load("images/zone_terror_shaman_with_mercenary_020.png", True),
	"zone_terror_shaman_with_mercenary_021":        _load("images/zone_terror_shaman_with_mercenary_021.png", True),
	"zone_terror_shaman_with_mercenary_022":        _load("images/zone_terror_shaman_with_mercenary_022.png", True),
	"zone_terror_shaman_with_mercenary_023":        _load("images/zone_terror_shaman_with_mercenary_023.png", True),
	"zone_terror_shaman_with_mercenary_024":        _load("images/zone_terror_shaman_with_mercenary_024.png", True),
	"zone_terror_shaman_with_mercenary_025":        _load("images/zone_terror_shaman_with_mercenary_025.png", True),
	"zone_terror_shaman_with_mercenary_026":        _load("images/zone_terror_shaman_with_mercenary_026.png", True),
	"zone_terror_shaman_with_mercenary_027":        _load("images/zone_terror_shaman_with_mercenary_027.png", True),
	"zone_terror_shaman_with_mercenary_028":        _load("images/zone_terror_shaman_with_mercenary_028.png", True),
	"zone_terror_shaman_with_mercenary_029":        _load("images/zone_terror_shaman_with_mercenary_029.png", True),
	"port_city_shaman_with_mercenary_001":        _load("images/port_city_shaman_with_mercenary_001.png", True),
	"port_city_shaman_with_mercenary_002":        _load("images/port_city_shaman_with_mercenary_002.png", True),
	"port_city_shaman_with_mercenary_003":        _load("images/port_city_shaman_with_mercenary_003.png", True),
	"port_city_shaman_with_mercenary_004":        _load("images/port_city_shaman_with_mercenary_004.png", True),
	"port_city_shaman_with_mercenary_005":        _load("images/port_city_shaman_with_mercenary_005.png", True),
	"port_city_shaman_with_mercenary_006":        _load("images/port_city_shaman_with_mercenary_006.png", True),
	"port_city_shaman_with_mercenary_007":        _load("images/port_city_shaman_with_mercenary_007.png", True),
	"port_city_shaman_with_mercenary_008":        _load("images/port_city_shaman_with_mercenary_008.png", True),
	"port_city_shaman_with_mercenary_009":        _load("images/port_city_shaman_with_mercenary_009.png", True),
	"port_city_shaman_with_mercenary_010":        _load("images/port_city_shaman_with_mercenary_010.png", True),
	"port_city_shaman_with_mercenary_011":        _load("images/port_city_shaman_with_mercenary_011.png", True),
	"port_city_shaman_with_mercenary_012":        _load("images/port_city_shaman_with_mercenary_012.png", True),
	"port_city_shaman_with_mercenary_013":        _load("images/port_city_shaman_with_mercenary_013.png", True),
	"port_city_shaman_with_mercenary_014":        _load("images/port_city_shaman_with_mercenary_014.png", True),
	"port_city_shaman_with_mercenary_015":        _load("images/port_city_shaman_with_mercenary_015.png", True),
	"port_city_shaman_with_mercenary_016":        _load("images/port_city_shaman_with_mercenary_016.png", True),
	"port_city_shaman_with_mercenary_017":        _load("images/port_city_shaman_with_mercenary_017.png", True),
	"cultist_island_shaman_with_mercenary_001":        _load("images/cultist_island_shaman_with_mercenary_001.png", True),
	"cultist_island_shaman_with_mercenary_002":        _load("images/cultist_island_shaman_with_mercenary_002.png", True),
	"cultist_island_shaman_with_mercenary_003":        _load("images/cultist_island_shaman_with_mercenary_003.png", True),
	"cultist_island_shaman_with_mercenary_004":        _load("images/cultist_island_shaman_with_mercenary_004.png", True),
	"cultist_island_shaman_with_mercenary_005":        _load("images/cultist_island_shaman_with_mercenary_005.png", True),
	"cultist_island_shaman_with_mercenary_006":        _load("images/cultist_island_shaman_with_mercenary_006.png", True),
	"cultist_island_shaman_with_mercenary_007":        _load("images/cultist_island_shaman_with_mercenary_007.png", True),
	"cultist_island_shaman_with_mercenary_008":        _load("images/cultist_island_shaman_with_mercenary_008.png", True),
	"cultist_island_shaman_with_mercenary_009":        _load("images/cultist_island_shaman_with_mercenary_009.png", True),
	"cultist_island_shaman_with_mercenary_010":        _load("images/cultist_island_shaman_with_mercenary_010.png", True),
	"cultist_island_shaman_with_mercenary_011":        _load("images/cultist_island_shaman_with_mercenary_011.png", True),
	"cultist_island_shaman_with_mercenary_012":        _load("images/cultist_island_shaman_with_mercenary_012.png", True),
	"cultist_island_shaman_with_mercenary_013":        _load("images/cultist_island_shaman_with_mercenary_013.png", True),
	"cultist_island_shaman_with_mercenary_014":        _load("images/cultist_island_shaman_with_mercenary_014.png", True),
	"cultist_island_shaman_with_mercenary_015":        _load("images/cultist_island_shaman_with_mercenary_015.png", True),
	"cultist_island_shaman_with_mercenary_016":        _load("images/cultist_island_shaman_with_mercenary_016.png", True),
	"cultist_island_shaman_with_mercenary_017":        _load("images/cultist_island_shaman_with_mercenary_017.png", True),
	"cultist_island_shaman_with_mercenary_018":        _load("images/cultist_island_shaman_with_mercenary_018.png", True),
	"cultist_island_shaman_with_mercenary_019":        _load("images/cultist_island_shaman_with_mercenary_019.png", True),
	"cultist_island_shaman_with_mercenary_020":        _load("images/cultist_island_shaman_with_mercenary_020.png", True),
	"outskirts_village_shaman_with_village_chief_001":        _load("images/outskirts_village_shaman_with_village_chief_001.png", True),
	"outskirts_village_shaman_with_village_chief_002":        _load("images/outskirts_village_shaman_with_village_chief_002.png", True),
	"outskirts_village_shaman_with_village_chief_003":        _load("images/outskirts_village_shaman_with_village_chief_003.png", True),
	"outskirts_village_shaman_with_village_chief_004":        _load("images/outskirts_village_shaman_with_village_chief_004.png", True),
	"outskirts_village_shaman_with_village_chief_005":        _load("images/outskirts_village_shaman_with_village_chief_005.png", True),
	"outskirts_village_shaman_with_villager_001":        _load("images/outskirts_village_shaman_with_villager_001.png", True),
	"outskirts_village_shaman_with_villager_002":        _load("images/outskirts_village_shaman_with_villager_002.png", True),
	"outskirts_village_shaman_with_villager_003":        _load("images/outskirts_village_shaman_with_villager_003.png", True),
	"outskirts_village_shaman_with_villager_004":        _load("images/outskirts_village_shaman_with_villager_004.png", True),
	"outskirts_village_shaman_with_villager_005":        _load("images/outskirts_village_shaman_with_villager_005.png", True),
	"outskirts_village_shaman_with_travelling_bard_001":        _load("images/outskirts_village_shaman_with_travelling_bard_001.png", True),
	"outskirts_village_shaman_with_travelling_bard_002":        _load("images/outskirts_village_shaman_with_travelling_bard_002.png", True),
	"outskirts_village_shaman_with_travelling_bard_003":        _load("images/outskirts_village_shaman_with_travelling_bard_003.png", True),
	"outskirts_village_shaman_with_travelling_bard_004":        _load("images/outskirts_village_shaman_with_travelling_bard_004.png", True),
	"outskirts_village_shaman_with_travelling_bard_005":        _load("images/outskirts_village_shaman_with_travelling_bard_005.png", True),
	"tribe_destroyed_shaman_to_herself_001":        _load("images/tribe_destroyed_shaman_to_herself_001.png", True),
	"tribe_destroyed_shaman_to_herself_002":        _load("images/tribe_destroyed_shaman_to_herself_002.png", True),
	"tribe_destroyed_shaman_to_herself_003":        _load("images/tribe_destroyed_shaman_to_herself_003.png", True),
	"tribe_destroyed_shaman_to_herself_004":        _load("images/tribe_destroyed_shaman_to_herself_004.png", True),
	"tribe_destroyed_shaman_to_herself_005":        _load("images/tribe_destroyed_shaman_to_herself_005.png", True),
	"tribe_destroyed_shaman_to_herself_006":        _load("images/tribe_destroyed_shaman_to_herself_006.png", True),
	"tribe_destroyed_shaman_to_herself_007":        _load("images/tribe_destroyed_shaman_to_herself_007.png", True),
	"tribe_destroyed_shaman_to_herself_008":        _load("images/tribe_destroyed_shaman_to_herself_008.png", True),
	"tribe_destroyed_shaman_to_herself_009":        _load("images/tribe_destroyed_shaman_to_herself_009.png", True),
	
	#MERCHANT DIALOGUE
	"port_city_merchant_with_guild_master_001":        _load("images/port_city_merchant_with_guild_master_001.png", True),
	"port_city_merchant_with_guild_master_002":        _load("images/port_city_merchant_with_guild_master_002.png", True),
	"port_city_merchant_with_guild_master_003":        _load("images/port_city_merchant_with_guild_master_003.png", True),
	"port_city_merchant_with_guild_master_004":        _load("images/port_city_merchant_with_guild_master_004.png", True),
	"port_city_merchant_with_guild_master_005":        _load("images/port_city_merchant_with_guild_master_005.png", True),
	"port_city_merchant_with_guild_master_006":        _load("images/port_city_merchant_with_guild_master_006.png", True),
	"port_city_merchant_with_guild_master_007":        _load("images/port_city_merchant_with_guild_master_007.png", True),
	"port_city_merchant_with_guild_master_008":        _load("images/port_city_merchant_with_guild_master_008.png", True),
	"port_city_merchant_with_guild_master_009":        _load("images/port_city_merchant_with_guild_master_009.png", True),
	"port_city_merchant_with_guild_master_010":        _load("images/port_city_merchant_with_guild_master_010.png", True),
	"port_city_merchant_with_guild_master_011":        _load("images/port_city_merchant_with_guild_master_011.png", True),
	"port_city_merchant_with_guild_master_012":        _load("images/port_city_merchant_with_guild_master_012.png", True),
	"port_city_merchant_with_guild_master_013":        _load("images/port_city_merchant_with_guild_master_013.png", True),
	"port_city_merchant_with_guild_master_014":        _load("images/port_city_merchant_with_guild_master_014.png", True),
	"port_city_merchant_with_guild_master_015":        _load("images/port_city_merchant_with_guild_master_015.png", True),
	"port_city_merchant_with_guild_master_016":        _load("images/port_city_merchant_with_guild_master_016.png", True),
	"port_city_merchant_with_guild_master_017":        _load("images/port_city_merchant_with_guild_master_017.png", True),
	"port_city_merchant_with_guild_master_018":        _load("images/port_city_merchant_with_guild_master_018.png", True),
	"port_city_merchant_with_guild_master_019":        _load("images/port_city_merchant_with_guild_master_019.png", True),
	"port_city_merchant_with_guild_master_020":        _load("images/port_city_merchant_with_guild_master_020.png", True),
	"port_city_merchant_with_guild_master_021":        _load("images/port_city_merchant_with_guild_master_021.png", True),
	"port_city_merchant_with_guild_master_022":        _load("images/port_city_merchant_with_guild_master_022.png", True),
	"port_city_merchant_with_guild_master_023":        _load("images/port_city_merchant_with_guild_master_023.png", True),
	"port_city_merchant_with_guild_master_024":        _load("images/port_city_merchant_with_guild_master_024.png", True),
	"port_city_merchant_with_guild_master_025":        _load("images/port_city_merchant_with_guild_master_025.png", True),
	"port_city_merchant_with_guild_master_026":        _load("images/port_city_merchant_with_guild_master_026.png", True),
	"port_city_merchant_with_guild_master_027":        _load("images/port_city_merchant_with_guild_master_027.png", True),
	"port_city_merchant_with_tavern_keeper_001":        _load("images/port_city_merchant_with_tavern_keeper_001.png", True),
	"port_city_merchant_with_tavern_keeper_002":        _load("images/port_city_merchant_with_tavern_keeper_002.png", True),
	"port_city_merchant_with_tavern_keeper_003":        _load("images/port_city_merchant_with_tavern_keeper_003.png", True),
	"port_city_merchant_with_tavern_keeper_004":        _load("images/port_city_merchant_with_tavern_keeper_004.png", True),
	"port_city_merchant_with_tavern_keeper_005":        _load("images/port_city_merchant_with_tavern_keeper_005.png", True),
	"port_city_merchant_with_tavern_keeper_006":        _load("images/port_city_merchant_with_tavern_keeper_006.png", True),
	"port_city_merchant_with_tavern_keeper_007":        _load("images/port_city_merchant_with_tavern_keeper_007.png", True),
	"port_city_merchant_with_tavern_keeper_008":        _load("images/port_city_merchant_with_tavern_keeper_008.png", True),
	"port_city_merchant_with_tavern_keeper_009":        _load("images/port_city_merchant_with_tavern_keeper_009.png", True),
	"port_city_merchant_with_tavern_keeper_010":        _load("images/port_city_merchant_with_tavern_keeper_010.png", True),
	"port_city_merchant_decision_node_001":        _load("images/port_city_merchant_decision_node_001.png", True),
	"port_city_merchant_decision_node_002":        _load("images/port_city_merchant_decision_node_002.png", True),
	"port_city_merchant_decision_node_003":        _load("images/port_city_merchant_decision_node_003.png", True),
	"port_city_merchant_response_node_001":        _load("images/port_city_merchant_response_node_001.png", True),
	"port_city_merchant_response_node_002":        _load("images/port_city_merchant_response_node_002.png", True),
	"port_city_merchant_response_node_003":        _load("images/port_city_merchant_response_node_003.png", True),
	"walled_merchant_with_blacksmith_001":        _load("images/walled_merchant_with_blacksmith_001.png", True),
	"walled_merchant_with_blacksmith_002":        _load("images/walled_merchant_with_blacksmith_002.png", True),
	"walled_merchant_with_blacksmith_003":        _load("images/walled_merchant_with_blacksmith_003.png", True),
	"walled_merchant_with_blacksmith_004":        _load("images/walled_merchant_with_blacksmith_004.png", True),
	"walled_merchant_with_blacksmith_005":        _load("images/walled_merchant_with_blacksmith_005.png", True),
	"walled_merchant_with_blacksmith_006":        _load("images/walled_merchant_with_blacksmith_006.png", True),
	"walled_merchant_with_blacksmith_007":        _load("images/walled_merchant_with_blacksmith_007.png", True),
	"walled_merchant_with_blacksmith_008":        _load("images/walled_merchant_with_blacksmith_008.png", True),
	"walled_merchant_with_blacksmith_009":        _load("images/walled_merchant_with_blacksmith_009.png", True),
	"walled_merchant_with_blacksmith_010":        _load("images/walled_merchant_with_blacksmith_010.png", True),
	"walled_merchant_with_blacksmith_011":        _load("images/walled_merchant_with_blacksmith_011.png", True),
	"outskirts_village_merchant_with_village_chief_001":        _load("images/outskirts_village_merchant_with_village_chief_001.png", True),
	"outskirts_village_merchant_with_village_chief_002":        _load("images/outskirts_village_merchant_with_village_chief_002.png", True),
	"outskirts_village_merchant_with_village_chief_003":        _load("images/outskirts_village_merchant_with_village_chief_003.png", True),
	"outskirts_village_merchant_with_village_chief_004":        _load("images/outskirts_village_merchant_with_village_chief_004.png", True),
	"outskirts_village_merchant_with_village_chief_005":        _load("images/outskirts_village_merchant_with_village_chief_005.png", True),
	"outskirts_village_merchant_with_village_chief_006":        _load("images/outskirts_village_merchant_with_village_chief_006.png", True),
	"outskirts_village_merchant_with_village_chief_007":        _load("images/outskirts_village_merchant_with_village_chief_007.png", True),
	"zone_terrors_merchant_to_himself_001":        _load("images/zone_terrors_merchant_to_himself_001.png", True),
	"zone_terrors_merchant_to_himself_002":        _load("images/zone_terrors_merchant_to_himself_002.png", True),
	"port_city_merchant_with_harbor_captain_001":        _load("images/port_city_merchant_with_harbor_captain_001.png", True),
	"port_city_merchant_with_harbor_captain_002":        _load("images/port_city_merchant_with_harbor_captain_002.png", True),
	"port_city_merchant_with_harbor_captain_003":        _load("images/port_city_merchant_with_harbor_captain_003.png", True),
	"port_city_merchant_with_harbor_captain_004":        _load("images/port_city_merchant_with_harbor_captain_004.png", True),
	"home_village_merchant_to_himself_001":        _load("images/home_village_merchant_to_himself_001.png", True),
	"home_village_merchant_to_himself_002":        _load("images/home_village_merchant_to_himself_002.png", True),
	"home_village_merchant_to_himself_003":        _load("images/home_village_merchant_to_himself_003.png", True),
	"home_village_merchant_to_himself_004":        _load("images/home_village_merchant_to_himself_004.png", True),
	"port_outpost_merchant_with_church_spy_001":        _load("images/port_outpost_mechant_with_church_spy_001.png", True),
	"port_outpost_merchant_with_church_spy_002":        _load("images/port_outpost_mechant_with_church_spy_002.png", True),
	"port_outpost_merchant_with_church_spy_003":        _load("images/port_outpost_mechant_with_church_spy_003.png", True),
	"port_outpost_merchant_with_church_spy_004":        _load("images/port_outpost_mechant_with_church_spy_004.png", True),
	"port_outpost_merchant_with_church_spy_005":        _load("images/port_outpost_mechant_with_church_spy_005.png", True),
	"port_outpost_merchant_with_church_spy_006":        _load("images/port_outpost_mechant_with_church_spy_006.png", True),
	"port_outpost_merchant_with_church_spy_007":        _load("images/port_outpost_mechant_with_church_spy_007.png", True),
	"port_outpost_merchant_with_church_spy_008":        _load("images/port_outpost_mechant_with_church_spy_008.png", True),
	"port_outpost_merchant_with_church_spy_009":        _load("images/port_outpost_mechant_with_church_spy_009.png", True),
	"port_outpost_merchant_with_church_spy_010":        _load("images/port_outpost_mechant_with_church_spy_010.png", True),
	"port_outpost_merchant_with_church_spy_011":        _load("images/port_outpost_mechant_with_church_spy_011.png", True),
	"port_outpost_merchant_with_church_spy_012":        _load("images/port_outpost_mechant_with_church_spy_012.png", True),
	"port_outpost_merchant_with_church_spy_013":        _load("images/port_outpost_mechant_with_church_spy_013.png", True),
	"port_outpost_merchant_with_church_spy_014":        _load("images/port_outpost_mechant_with_church_spy_014.png", True),
	"port_outpost_merchant_with_church_spy_015":        _load("images/port_outpost_mechant_with_church_spy_015.png", True),
	"port_outpost_merchant_with_church_spy_016":        _load("images/port_outpost_mechant_with_church_spy_016.png", True),
	"port_outpost_merchant_with_church_spy_017":        _load("images/port_outpost_mechant_with_church_spy_017.png", True),
	"port_outpost_merchant_with_church_spy_018":        _load("images/port_outpost_mechant_with_church_spy_018.png", True),
	"port_city_merchant_with_captain_and_spy_001":        _load("images/port_city_merchant_with_captain_and_spy_001.png", True),
	"port_city_merchant_with_captain_and_spy_002":        _load("images/port_city_merchant_with_captain_and_spy_002.png", True),
	"port_city_merchant_with_captain_and_spy_003":        _load("images/port_city_merchant_with_captain_and_spy_003.png", True),
	"port_city_merchant_with_captain_and_spy_004":        _load("images/port_city_merchant_with_captain_and_spy_004.png", True),
	"port_city_merchant_with_captain_and_spy_005":        _load("images/port_city_merchant_with_captain_and_spy_005.png", True),
	"port_city_merchant_with_captain_and_spy_006":        _load("images/port_city_merchant_with_captain_and_spy_006.png", True),
	"port_city_merchant_with_captain_and_spy_007":        _load("images/port_city_merchant_with_captain_and_spy_007.png", True),
	"port_city_merchant_with_captain_and_spy_008":        _load("images/port_city_merchant_with_captain_and_spy_008.png", True),
	"port_city_merchant_with_captain_and_spy_009":        _load("images/port_city_merchant_with_captain_and_spy_009.png", True),
	"port_city_merchant_with_captain_and_spy_010":        _load("images/port_city_merchant_with_captain_and_spy_010.png", True),
	"port_city_merchant_with_captain_and_spy_011":        _load("images/port_city_merchant_with_captain_and_spy_011.png", True),
	"port_city_merchant_with_captain_and_spy_012":        _load("images/port_city_merchant_with_captain_and_spy_012.png", True),
	"port_city_merchant_with_captain_and_spy_013":        _load("images/port_city_merchant_with_captain_and_spy_013.png", True),
	"port_city_merchant_with_captain_and_spy_014":        _load("images/port_city_merchant_with_captain_and_spy_014.png", True),
	"port_city_merchant_with_captain_and_spy_015":        _load("images/port_city_merchant_with_captain_and_spy_015.png", True),
	"port_city_merchant_with_captain_and_spy_016":        _load("images/port_city_merchant_with_captain_and_spy_016.png", True),
	"port_city_merchant_with_captain_and_spy_017":        _load("images/port_city_merchant_with_captain_and_spy_017.png", True),
	"port_city_merchant_with_captain_and_spy_018":        _load("images/port_city_merchant_with_captain_and_spy_018.png", True),
	"port_city_merchant_with_captain_and_spy_019":        _load("images/port_city_merchant_with_captain_and_spy_019.png", True),
	"port_city_merchant_with_captain_and_spy_020":        _load("images/port_city_merchant_with_captain_and_spy_020.png", True),
	"port_city_merchant_with_mercenary_001":        _load("images/port_city_merchant_with_mercenary_001.png", True),
	"port_city_merchant_with_mercenary_002":        _load("images/port_city_merchant_with_mercenary_002.png", True),
	"port_city_merchant_with_mercenary_003":        _load("images/port_city_merchant_with_mercenary_003.png", True),
	"port_city_merchant_with_mercenary_004":        _load("images/port_city_merchant_with_mercenary_004.png", True),
	"port_city_merchant_with_mercenary_005":        _load("images/port_city_merchant_with_mercenary_005.png", True),
	"port_city_merchant_with_mercenary_006":        _load("images/port_city_merchant_with_mercenary_006.png", True),
	"port_city_merchant_with_mercenary_007":        _load("images/port_city_merchant_with_mercenary_007.png", True),
	"port_city_merchant_with_mercenary_008":        _load("images/port_city_merchant_with_mercenary_008.png", True),
	"port_city_merchant_with_mercenary_009":        _load("images/port_city_merchant_with_mercenary_009.png", True),
	"port_city_merchant_with_mercenary_010":        _load("images/port_city_merchant_with_mercenary_010.png", True),
	"port_city_merchant_with_mercenary_011":        _load("images/port_city_merchant_with_mercenary_011.png", True),
	"port_city_merchant_with_mercenary_012":        _load("images/port_city_merchant_with_mercenary_012.png", True),
	"port_city_merchant_with_mercenary_013":        _load("images/port_city_merchant_with_mercenary_013.png", True),
	"port_city_merchant_with_mercenary_014":        _load("images/port_city_merchant_with_mercenary_014.png", True),
	"port_city_merchant_with_mercenary_015":        _load("images/port_city_merchant_with_mercenary_015.png", True),
	"port_city_merchant_with_mercenary_016":        _load("images/port_city_merchant_with_mercenary_016.png", True),
	"port_city_merchant_with_mercenary_017":        _load("images/port_city_merchant_with_mercenary_017.png", True),
	"port_city_merchant_with_mercenary_018":        _load("images/port_city_merchant_with_mercenary_018.png", True),
	"port_city_merchant_with_mercenary_019":        _load("images/port_city_merchant_with_mercenary_019.png", True),
	"port_city_merchant_with_mercenary_020":        _load("images/port_city_merchant_with_mercenary_020.png", True),
	"theocratic_merchant_with_archive_001":        _load("images/theocratic_merchant_with_archive_001.png", True),
	"theocratic_merchant_with_archive_002":        _load("images/theocratic_merchant_with_archive_002.png", True),
	"theocratic_merchant_with_archive_003":        _load("images/theocratic_merchant_with_archive_003.png", True),
	"theocratic_merchant_with_archive_004":        _load("images/theocratic_merchant_with_archive_004.png", True),
	"theocratic_merchant_with_archive_005":        _load("images/theocratic_merchant_with_archive_005.png", True),
	"theocratic_merchant_with_archive_006":        _load("images/theocratic_merchant_with_archive_006.png", True),
	"theocratic_merchant_with_archive_007":        _load("images/theocratic_merchant_with_archive_007.png", True),
	"theocratic_merchant_with_archive_008":        _load("images/theocratic_merchant_with_archive_008.png", True),
	"theocratic_merchant_with_archive_009":        _load("images/theocratic_merchant_with_archive_009.png", True),
	"theocratic_merchant_with_church_knight_001":        _load("images/theocratic_merchant_with_church_knight_001.png", True),
	"theocratic_merchant_with_church_knight_002":        _load("images/theocratic_merchant_with_church_knight_002.png", True),
	"theocratic_merchant_with_church_knight_003":        _load("images/theocratic_merchant_with_church_knight_003.png", True),
	"theocratic_merchant_with_church_knight_004":        _load("images/theocratic_merchant_with_church_knight_004.png", True),
	"theocratic_merchant_with_church_knight_005":        _load("images/theocratic_merchant_with_church_knight_005.png", True),
	"theocratic_merchant_with_church_knight_006":        _load("images/theocratic_merchant_with_church_knight_006.png", True),
	"theocratic_merchant_with_church_knight_007":        _load("images/theocratic_merchant_with_church_knight_007.png", True),
	"theocratic_merchant_with_church_knight_008":        _load("images/theocratic_merchant_with_church_knight_008.png", True),
	"theocratic_merchant_with_church_knight_009":        _load("images/theocratic_merchant_with_church_knight_009.png", True),
	"theocratic_merchant_with_church_knight_010":        _load("images/theocratic_merchant_with_church_knight_010.png", True),
	"theocratic_merchant_with_church_knight_011":        _load("images/theocratic_merchant_with_church_knight_011.png", True),
	"theocratic_merchant_with_church_knight_012":        _load("images/theocratic_merchant_with_church_knight_012.png", True),
	"theocratic_merchant_with_church_knight_013":        _load("images/theocratic_merchant_with_church_knight_013.png", True),
	"theocratic_merchant_with_church_knight_014":        _load("images/theocratic_merchant_with_church_knight_014.png", True),
	"theocratic_merchant_with_church_knight_015":        _load("images/theocratic_merchant_with_church_knight_015.png", True),
	"theocratic_merchant_with_priest_001":        _load("images/theocratic_merchant_with_priest_001.png", True),
	"theocratic_merchant_with_priest_002":        _load("images/theocratic_merchant_with_priest_002.png", True),
	"theocratic_merchant_with_priest_003":        _load("images/theocratic_merchant_with_priest_003.png", True),
	"theocratic_merchant_with_priest_004":        _load("images/theocratic_merchant_with_priest_004.png", True),
	"theocratic_merchant_with_priest_005":        _load("images/theocratic_merchant_with_priest_005.png", True),
	"theocratic_merchant_with_priest_006":        _load("images/theocratic_merchant_with_priest_006.png", True),
	"theocratic_merchant_with_priest_007":        _load("images/theocratic_merchant_with_priest_007.png", True),
	"theocratic_merchant_with_priest_008":        _load("images/theocratic_merchant_with_priest_008.png", True),
	"theocratic_merchant_with_priest_009":        _load("images/theocratic_merchant_with_priest_009.png", True),
	"theocratic_merchant_with_priest_010":        _load("images/theocratic_merchant_with_priest_010.png", True),
	"theocratic_merchant_with_priest_011":        _load("images/theocratic_merchant_with_priest_011.png", True),
	"theocratic_merchant_with_priest_012":        _load("images/theocratic_merchant_with_priest_012.png", True),
	"theocratic_merchant_with_priest_013":        _load("images/theocratic_merchant_with_priest_013.png", True),
	"theocratic_merchant_with_priest_014":        _load("images/theocratic_merchant_with_priest_014.png", True),
	"theocratic_merchant_with_priest_015":        _load("images/theocratic_merchant_with_priest_015.png", True),
	"theocratic_merchant_with_priest_016":        _load("images/theocratic_merchant_with_priest_016.png", True),
	"theocratic_merchant_with_priest_017":        _load("images/theocratic_merchant_with_priest_017.png", True),
	"theocratic_merchant_with_priest_018":        _load("images/theocratic_merchant_with_priest_018.png", True),
	"theocratic_merchant_with_priest_019":        _load("images/theocratic_merchant_with_priest_019.png", True),
	"theocratic_merchant_with_priest_020":        _load("images/theocratic_merchant_with_priest_020.png", True),
	"theocratic_merchant_with_priest_021":        _load("images/theocratic_merchant_with_priest_021.png", True),
	"theocratic_merchant_with_priest_022":        _load("images/theocratic_merchant_with_priest_022.png", True),
	"theocratic_merchant_with_priest_023":        _load("images/theocratic_merchant_with_priest_023.png", True),
	"theocratic_merchant_with_priest_024":        _load("images/theocratic_merchant_with_priest_024.png", True),
	"theocratic_merchant_with_priest_025":        _load("images/theocratic_merchant_with_priest_025.png", True),
	"theocratic_merchant_with_priest_026":        _load("images/theocratic_merchant_with_priest_026.png", True),
	"theocratic_merchant_with_priest_027":        _load("images/theocratic_merchant_with_priest_027.png", True),
	"theocratic_merchant_with_priest_028":        _load("images/theocratic_merchant_with_priest_028.png", True),
	"theocratic_merchant_with_priest_029":        _load("images/theocratic_merchant_with_priest_029.png", True),
	"theocratic_merchant_with_priest_030":        _load("images/theocratic_merchant_with_priest_030.png", True),
	"theocratic_merchant_with_priest_031":        _load("images/theocratic_merchant_with_priest_031.png", True),
	"theocratic_merchant_with_priest_032":        _load("images/theocratic_merchant_with_priest_032.png", True),
	"theocratic_merchant_with_priest_033":        _load("images/theocratic_merchant_with_priest_033.png", True),
	"theocratic_merchant_with_priest_034":        _load("images/theocratic_merchant_with_priest_034.png", True),
	"theocratic_merchant_with_priest_035":        _load("images/theocratic_merchant_with_priest_035.png", True),
	"theocratic_merchant_with_priest_036":        _load("images/theocratic_merchant_with_priest_036.png", True),
	"theocratic_merchant_with_priest_037":        _load("images/theocratic_merchant_with_priest_037.png", True),
	"theocratic_merchant_with_priest_038":        _load("images/theocratic_merchant_with_priest_038.png", True),
	"theocratic_merchant_with_priest_039":        _load("images/theocratic_merchant_with_priest_039.png", True),
	"theocratic_merchant_with_priest_040":        _load("images/theocratic_merchant_with_priest_040.png", True),
	"theocratic_merchant_with_priest_041":        _load("images/theocratic_merchant_with_priest_041.png", True),
	"theocratic_merchant_with_priest_042":        _load("images/theocratic_merchant_with_priest_042.png", True),
	"theocratic_merchant_with_priest_043":        _load("images/theocratic_merchant_with_priest_043.png", True),
	"weapon_1handed_short_sword":		_load("images/weapon_1handed_short_sword.png", True),
	"weapon_1handed_cleaver":		_load("images/weapon_1handed_cleaver.png", True),
	"weapon_1handed_knife":		_load("images/weapon_1handed_knife.png", True),
	"materials_sheet_ancient_paper":		_load("images/materials_sheet_ancient_paper.png", True),
	"armour_headware_iron_mask":		_load("images/armour_headware_iron_mask.png", True),
	"armour_body_armour_dark_priests_robe":		_load("images/armour_body_armour_dark_priests_robe.png", True),
	"armour_body_armour_priests_robe":		_load("images/armour_body_armour_priests_robe.png", True),
	"armour_headware_plate_helmet":		_load("images/armour_headware_plate_helmet.png", True),
	"armour_headware_padded_cap":		_load("images/armour_headware_padded_cap.png", True),
	"armour_body_armour_iron_cuirass":		_load("images/armour_body_armour_iron_cuirass.png", True),
	"armour_body_armour_loincloth":		_load("images/armour_body_armour_loincloth.png", True),
	"armour_accessories_red_scarf":		_load("images/armour_accessories_red_scarf.png", True),
	"armour_headware_iron_helmet":		_load("images/armour_headware_iron_helmet.png", True),
	"armour_headware_guard_bascinet":		_load("images/armour_headware_guard_bascinet.png", True),
	"armour_headware_guard_coif":		_load("images/armour_headware_guard_coif.png", True),
	"armour_headware_chainmail_hood":		_load("images/armour_headware_chainmail_hood.png", True),
	"armour_body_armour_black_dress":		_load("images/armour_body_armour_black_dress.png", True),
	"armour_body_armour_trench_coat":		_load("images/armour_body_armour_trench_coat.png", True),
	"weapon_1handed_corsairs_saber":		_load("images/weapon_1handed_corsairs_saber.png", True),
	"weapon_1handed_cloth_hood":		_load("images/weapon_1handed_cloth_hood.png", True),
	"armour_body_armour_leather_coat":		_load("images/armour_body_armour_leather_coat.png", True),
	"armour_body_armour_leather_jvest":		_load("images/armour_body_armour_leather_jvest.png", True),
	"armour_body_armour_plated_mail":		_load("images/armour_body_armour_plated_mail.png", True),
	"armour_shield_scutum":		_load("images/armour_shield_scutum.png", True),
	"weapon_longrange_musket":		_load("images/weapon_longrange_musket.png", True),
	"weapon_2handed_spear":		_load("images/weapon_2handed_spear.png", True),
	"armour_body_armour_hard_leather_armor":		_load("images/armour_body_armour_hard_leather_armor.png", True),
	"armour_body_armour_iron_plate":		_load("images/armour_body_armour_iron_plate.png", True),
	"weapon_1handed_stiletto":		_load("images/weapon_1handed_stiletto.png", True),
	"armour_armwear_arm_guard":		_load("images/armour_armwear_arm_guard.png", True),
	"weapon_1handed_iron_axe":		_load("images/weapon_1handed_iron_axe.png", True),
	"weapon_longrange_short_bow":		_load("images/weapon_longrange_short_bow.png", True),
	"materials_scrap_leather_scraps":		_load("images/materials_scrap_leather_scraps.png", True),
	"materials_skill_book_of_rapid_fire":		_load("images/materials_skill_book_of_rapid_fire.png", True),
	"materials_skill_book_of_instincts":		_load("images/materials_skill_book_of_instincts.png", True),
	"armour_accessories_swift_boots":		_load("images/armour_accessories_swift_boots.png", True),
	"weapon_longrange_heavy_crossbow":		_load("images/weapon_longrange_heavy_crossbow.png", True),
	"weapon_longrange_longbow":		_load("images/weapon_longrange_longbow.png", True),
	"weapon_2handed_maul":		_load("images/weapon_2handed_maul.png", True),
	"weapon_2handed_claymore":		_load("images/weapon_2handed_claymore.png", True),
	"weapon_1handed_scimitar":		_load("images/weapon_1handed_scimitar.png", True),
	"weapon_1handed_improvised_shiv":		_load("images/weapon_1handed_improvised_shiv.png", True),
	"weapon_1handed_steel_hammer":		_load("images/weapon_1handed_steel_hammer.png", True),
	"material_toy_black_dressed_doll":		_load("images/material_toy_black_dressed_doll.png", True),
	"weapon_1handed_dirk":		_load("images/weapon_1handed_dirk.png", True),
	"materials_plank_wooden_plank":		_load("images/materials_plank_wooden_plank.png", True),
	"weapon_1handed_dagger":		_load("images/weapon_1handed_dagger.png", True),
	"materials_component_silver_wire":		_load("images/materials_component_silver_wire.png", True),
	"armour_accessories_red_amulet":		_load("images/armour_accessories_red_amulet.png", True),
	"armour_accessories_blue_amulet":		_load("images/armour_accessories_blue_amulet.png", True),
	"materials_component_stick":		_load("images/materials_component_stick.png", True),
	"armour_accessories_ring":		_load("images/armour_accessories_ring.png", True),
	"materials_skill_book_of_marksmanship":		_load("images/materials_skill_book_of_marksmanship.png", True),
	"materials_skill_book_of_stars":		_load("images/materials_skill_book_of_stars.png", True),
	"materials_skill_book_of_crafsmanship":		_load("images/materials_skill_book_of_crafsmanship.png", True),
	"materials_skill_book_of_agility":		_load("images/materials_skill_book_of_agility.png", True),
	"materials_skill_book_of_healing":		_load("images/materials_skill_book_of_healing.png", True),
	"materials_skill_book_of_the_secrets":		_load("images/materials_skill_book_of_the_secrets.png", True),
	"materials_save_book_of_enlightenment":		_load("images/materials_save_book_of_enlightenment.png", True),
	"materials_skill_book_of_cowardice_i":		_load("images/materials_skill_book_of_cowardice_i.png", True),
	"materials_skill_book_of_cowardice_ii":		_load("images/materials_skill_book_of_cowardice_ii.png", True),
	"materials_skill_book_of_pestilence_i":		_load("images/materials_skill_book_of_pestilence_i.png", True),
	"materials_skill_book_of_pestilence_ii":		_load("images/materials_skill_book_of_pestilence_ii.png", True),
	"materials_skill_book_of_pestilence_iii":		_load("images/materials_skill_book_of_pestilence_iii.png", True),
	"materials_skill_book_of_pestilence_iv":		_load("images/materials_skill_book_of_pestilence_iv.png", True),
	"materials_skill_book_of_pestilence_v":		_load("images/materials_skill_book_of_pestilence_v.png", True),
	"materials_skill_book_of_pestilence_vi":		_load("images/materials_skill_book_of_pestilence_vi.png", True),
	"materials_skill_book_of_pestilence_vii":		_load("images/materials_skill_book_of_pestilence_vii.png", True),
	"materials_skill_book_of_pestilence_viii":		_load("images/materials_skill_book_of_pestilence_viii.png", True),
	"materials_skill_book_of_trade_i":		_load("images/materials_skill_book_of_trade_i.png", True),
	"materials_skill_book_of_trade_ii":		_load("images/materials_skill_book_of_trade_ii.png", True),
	"materials_skill_book_of_trade_iii":		_load("images/materials_skill_book_of_trade_iii.png", True),
	"materials_gem_red_gem":		_load("images/materials_gem_red_gem.png", True),
	"materials_gem_blue_gem":		_load("images/materials_gem_blue_gem.png", True),
	"materials_beverage_ale":		_load("images/materials_beverage_ale.png", True),
	"materials_beverage_wine":		_load("images/materials_beverage_wine.png", True),
	"materials_beverage_rum":		_load("images/materials_beverage_rum.png", True),
	"materials_bar_iron_ingot":		_load("images/materials_bar_iron_ingot.png", True),
	"materials_ore_raw_iron":		_load("images/materials_ore_raw_iron.png", True),
	"materials_foliage_blue_herb-1":		_load("images/materials_foliage_blue_herb-1.png", True),
	"materials_foliage_green_herb":		_load("images/materials_foliage_green_herb.png", True),
	"materials_sheet_paper":		_load("images/materials_sheet_paper.png", True),
	"materials_potion_antibiotics":		_load("images/materials_potion_antibiotics.png", True),
	"materials_potion_betadine":		_load("images/materials_potion_betadine.png", True),
	"materials_potion_red_vial":		_load("images/materials_potion_red_vial.png", True),
	"materials_container_empty_vial":		_load("images/materials_container_empty_vial.png", True),
	"weapon_2handed_longsword":		_load("images/weapon_2handed_longsword.png", True),
	"armour_shield_wooden_buckler":		_load("images/armour_shield_wooden_buckler.png", True),
	"weapon_1handed_cultist_dagger":		_load("images/weapon_1handed_cultist_dagger.png", True),
	"weapon_longrange_flintlock":		_load("images/weapon_longrange_flintlock.png", True),
	"weapon_2handed_makeshift_spear":		_load("images/weapon_2handed_makeshift_spear.png", True),
	"weapon_longrange_blunderbuss":		_load("images/weapon_longrange_blunderbuss.png", True),
	"weapon_1handed_shaman_dagger":		_load("images/weapon_1handed_shaman_dagger.png", True),
	"weapon_2handed_priest_staff":		_load("images/weapon_2handed_priest_staff.png", True),
	"weapon_longrange_cultist_crossbow":		_load("images/weapon_longrange_cultist_crossbow.png", True),
	"materials_component_bow_string":		_load("images/materials_component_bow_string.png", True),
	"user_item_short_sword":        _load("items/weapon_1handed_short_sword.png", True),
	"user_item_cleaver":        _load("items/weapon_1handed_cleaver.png", True),
	"user_item_knife":        _load("items/weapon_1handed_knife.png", True),
	"user_item_ancient_paper":        _load("items/materials_sheet_ancient_paper.png", True),
	"user_item_iron_mask":        _load("items/armour_headware_iron_mask.png", True),
	"user_item_dark_priests_robe":        _load("items/armour_body_armour_dark_priests_robe.png", True),
	"user_item_priests_robe":        _load("items/armour_body_armour_priests_robe.png", True),
	"user_item_plate_helmet":        _load("items/armour_headware_plate_helmet.png", True),
	"user_item_padded_cap":        _load("items/armour_headware_padded_cap.png", True),
	"user_item_iron_cuirass":        _load("items/armour_body_armour_iron_cuirass.png", True),
	"user_item_loincloth":        _load("items/armour_body_armour_loincloth.png", True),
	"user_item_red_scarf":        _load("items/armour_accessories_red_scarf.png", True),
	"user_item_iron_helmet":        _load("items/armour_headware_iron_helmet.png", True),
	"user_item_guard_bascinet":        _load("items/armour_headware_guard_bascinet.png", True),
	"user_item_guard_coif":        _load("items/armour_headware_guard_coif.png", True),
	"user_item_chainmail_hood":        _load("items/armour_headware_chainmail_hood.png", True),
	"user_item_black_dress":        _load("items/armour_body_armour_black_dress.png", True),
	"user_item_trench_coat":        _load("items/armour_body_armour_trench_coat.png", True),
	"user_item_corsairs_saber":        _load("items/weapon_1handed_corsairs_saber.png", True),
	"user_item_cloth_hood":        _load("items/weapon_1handed_cloth_hood.png", True),
	"user_item_leather_coat":        _load("items/armour_body_armour_leather_coat.png", True),
	"user_item_leather_vest":        _load("items/armour_body_armour_leather_vest.png", True),
	"user_item_plated_mail":        _load("items/armour_body_armour_plated_mail.png", True),
	"user_item_shield_scutum":        _load("items/armour_shield_scutum.png", True),
	"user_item_musket":        _load("items/weapon_longrange_musket.png", True),
	"user_item_spear":        _load("items/weapon_2handed_spear.png", True),
	"user_item_hard_leather_armor":        _load("items/armour_body_armour_hard_leather_armor.png", True),
	"user_item_iron_plate":        _load("items/armour_body_armour_iron_plate.png", True),
	"user_item_stiletto":        _load("items/weapon_1handed_stiletto.png", True),
	"user_item_arm_guard":        _load("items/armour_armwear_arm_guard.png", True),
	"user_item_iron_axe":        _load("items/weapon_1handed_iron_axe.png", True),
	"user_item_short_bow":        _load("items/weapon_longrange_short_bow.png", True),
	"user_item_leather_scraps":        _load("items/materials_scrap_leather_scraps.png", True),
	"user_item_book_of_rapid_fire":        _load("items/materials_skill_book_of_rapid_fire.png", True),
	"user_item_book_of_instincts":        _load("items/materials_skill_book_of_instincts.png", True),
	"user_item_swift_boots":        _load("items/armour_accessories_swift_boots.png", True),
	"user_item_heavy_crossbow":        _load("items/weapon_longrange_heavy_crossbow.png", True),
	"user_item_longbow":        _load("items/weapon_longrange_longbow.png", True),
	"user_item_maul":        _load("items/weapon_2handed_maul.png", True),
	"user_item_claymore":        _load("items/weapon_2handed_claymore.png", True),
	"user_item_scimitar":        _load("items/weapon_1handed_scimitar.png", True),
	"user_item_improvised_shiv":        _load("items/weapon_1handed_improvised_shiv.png", True),
	"user_item_steel_hammer":        _load("items/weapon_1handed_steel_hammer.png", True),
	"user_item_black_dressed_doll":        _load("items/material_toy_black_dressed_doll.png", True),
	"user_item_dirk":        _load("items/weapon_1handed_dirk.png", True),
	"user_item_wooden_plank":        _load("items/materials_plank_wooden_plank.png", True),
	"user_item_dagger":        _load("items/weapon_1handed_dagger.png", True),
	"user_item_silver_wire":        _load("items/materials_component_silver_wire.png", True),
	"user_item_red_amulet":        _load("items/armour_accessories_red_amulet.png", True),
	"user_item_blue_amulet":        _load("items/armour_accessories_blue_amulet.png", True),
	"user_item_stick":        _load("items/materials_component_stick.png", True),
	"user_item_ring":        _load("items/armour_accessories_ring.png", True),
	"user_item_book_of_marksmanship":        _load("items/materials_skill_book_of_marksmanship.png", True),
	"user_item_book_of_stars":        _load("items/materials_skill_book_of_stars.png", True),
	"user_item_book_of_craftsmanship":        _load("items/materials_skill_book_of_craftsmanship.png", True),
	"user_item_book_of_agility":        _load("items/materials_skill_book_of_agility.png", True),
	"user_item_book_of_healing":        _load("items/materials_skill_book_of_healing.png", True),
	"user_item_book_of_the_secrets":        _load("items/materials_skill_book_of_the_secrets.png", True),
	"user_item_book_of_enlightenment":        _load("items/materials_save_book_of_enlightenment.png", True),
	"user_item_book_of_cowardice_i":        _load("items/materials_skill_book_of_cowardice_i.png", True),
	"user_item_book_of_cowardice_ii":        _load("items/materials_skill_book_of_cowardice_ii.png", True),
	"user_item_book_of_pestilence_i":        _load("items/materials_skill_book_of_pestilence_i.png", True),
	"user_item_book_of_pestilence_ii":        _load("items/materials_skill_book_of_pestilence_ii.png", True),
	"user_item_book_of_pestilence_iii":        _load("items/materials_skill_book_of_pestilence_iii.png", True),
	"user_item_book_of_pestilence_iv":        _load("items/materials_skill_book_of_pestilence_iv.png", True),
	"user_item_book_of_pestilence_v":        _load("items/materials_skill_book_of_pestilence_v.png", True),
	"user_item_book_of_pestilence_vi":        _load("items/materials_skill_book_of_pestilence_vi.png", True),
	"user_item_book_of_pestilence_vii":        _load("items/materials_skill_book_of_pestilence_vii.png", True),
	"user_item_book_of_pestilence_viii":        _load("items/materials_skill_book_of_pestilence_viii.png", True),
	"user_item_book_of_trade_i":        _load("items/materials_skill_book_of_trade_i.png", True),
	"user_item_book_of_trade_ii":        _load("items/materials_skill_book_of_trade_ii.png", True),
	"user_item_book_of_trade_iii":        _load("items/materials_skill_book_of_trade_iii.png", True),
	"user_item_red_gem":        _load("items/materials_gem_red_gem.png", True),
	"user_item_blue_gem":        _load("items/materials_gem_blue_gem.png", True),
	"user_item_ale":        _load("items/materials_beverage_ale.png", True),
	"user_item_wine":        _load("items/materials_beverage_wine.png", True),
	"user_item_rum":        _load("items/materials_beverage_rum.png", True),
	"user_item_iron_ingot":        _load("items/materials_bar_iron_ingot.png", True),
	"user_item_raw_iron":        _load("items/materials_ore_raw_iron.png", True),
	"user_item_blue_herb":        _load("items/materials_foliage_blue_herb-1.png", True),
	"user_item_green_herb":        _load("items/materials_foliage_green_herb.png", True),
	"user_item_paper":        _load("items/materials_sheet_paper.png", True),
	"user_item_antibiotics":        _load("items/materials_potion_antibiotics.png", True),
	"user_item_betadine":        _load("items/materials_potion_betadine.png", True),
	"user_item_red_vial":        _load("items/materials_potion_red_vial.png", True),
	"user_item_empty_vial":        _load("items/materials_container_empty_vial.png", True),
	"user_item_longsword":        _load("items/weapon_2handed_longsword.png", True),
	"user_item_wooden_buckler":        _load("items/armour_shield_wooden_buckler.png", True),
	"user_item_cultist_dagger":        _load("items/weapon_1handed_cultist_dagger.png", True),
	"user_item_flintlock":        _load("items/weapon_longrange_flintlock.png", True),
	"user_item_makeshift_spear":        _load("items/weapon_2handed_makeshift_spear.png", True),
	"user_item_blunderbuss":        _load("items/weapon_longrange_blunderbuss.png", True),
	"user_item_shaman_dagger":        _load("items/weapon_1handed_shaman_dagger.png", True),
	"user_item_priest_staff":        _load("items/weapon_2handed_priest_staff.png", True),
	"user_item_cultist_crossbow":        _load("items/weapon_longrange_cultist_crossbow.png", True),
	"user_item_bow_string":        _load("items/materials_component_bow_string.png", True),
	"silver_chest_closed":        _load("sprites/elucidate_silver_chest_closed_001.png", True),
	"silver_chest_opened":        _load("sprites/elucidate_silver_chest_opened_002.png", True),
	"gold_chest_closed":        _load("sprites/elucidate_gold_chest_closed_003.png", True),
	"gold_chest_opened":        _load("sprites/elucidate_gold_chest_opened_004.png", True),
	"idle_cult_leader_npc_down":        _load("sprites/npc_e_cult_leader/elucidate_idle_cult_leader_npc_down.png", True),
	"idle_cult_leader_npc_up":        _load("sprites/npc_e_cult_leader/elucidate_idle_cult_leader_npc_up.png", True),
	"idle_cult_leader_npc_left":        _load("sprites/npc_e_cult_leader/elucidate_idle_cult_leader_npc_left.png", True),
	"idle_cult_leader_npc_right":        _load("sprites/npc_e_cult_leader/elucidate_idle_cult_leader_npc_right.png", True),
	"idle_cultist_npc_up":        _load("sprites/npc_e_cult_soldier/elucidate_idle_cultist_npc_up.png", True),
	"idle_cultist_npc_right":        _load("sprites/npc_e_cult_soldier/elucidate_idle_cultist_npc_right.png", True),
	"idle_cultist_npc_left":        _load("sprites/npc_e_cult_soldier/elucidate_idle_cultist_npc_left.png", True),
	"idle_cultist_npc_down":        _load("sprites/npc_e_cult_soldier/elucidate_idle_cultist_npc_down.png", True),
	"idle_corrupted1_cultist_npc_right":        _load("sprites/npc_e_s1_corrupted_cultist/elucidate_idle_corrupted1_cultist_npc_right.png", True),
	"idle_corrupted1_cultist_npc_left":        _load("sprites/npc_e_s1_corrupted_cultist/elucidate_idle_corrupted1_cultist_npc_left.png", True),
	"idle_corrupted1_cultist_npc_down":        _load("sprites/npc_e_s1_corrupted_cultist/elucidate_idle_corrupted1_cultist_npc_down.png", True),
	"idle_corrupted1_cultist_npc_up":        _load("sprites/npc_e_s1_corrupted_cultist/elucidate_idle_corrupted1_cultist_npc_up.png", True),
	"idle_amalgamated_villagers_npc_right":        _load("sprites/npc_e_amalgamated_villagers/elucidate_idle_amalgamated_villagers_npc_right.png", True),
	"idle_amalgamated_villagers_npc_left":        _load("sprites/npc_e_amalgamated_villagers/elucidate_idle_amalgamated_villagers_npc_left.png", True),
	"idle_amalgamated_knights_npc_right":        _load("sprites/npc_e_amalgamated_knights/elucidate_idle_amalgamated_knights_npc_right.png", True),
	"idle_amalgamated_knights_npc_left":        _load("sprites/npc_e_amalgamated_knights/elucidate_idle_amalgamated_knights_npc_left.png", True),
	"idle_amalgamated_civillians_npc_right":        _load("sprites/npc_e_amalgamated_civilians/elucidate_idle_amalgamated_civillians_npc_right.png", True),
	"idle_amalgamated_civillians_npc_left":        _load("sprites/npc_e_amalgamated_civilians/elucidate_idle_amalgamated_civillians_npc_left.png", True),
	"idle_melted_male_villager_npc_right":        _load("sprites/npc_e_melted_villager_male/elucidate_idle_melted_male_villager_npc_right.png", True),
	"idle_melted_male_villager_npc_left":        _load("sprites/npc_e_melted_villager_male/elucidate_idle_melted_male_villager_npc_left.png", True),
	"idle_melted_male_villager_npc_up":        _load("sprites/npc_e_melted_villager_male/elucidate_idle_melted_male_villager_npc_up.png", True),
	"idle_melted_male_villager_npc_down":        _load("sprites/npc_e_melted_villager_male/elucidate_idle_melted_male_villager_npc_down.png", True),
	"idle_melted_female_villager_npc_up":        _load("sprites/npc_e_melted_villager_female/elucidate_idle_melted_female_villager_npc_up.png", True),
	"idle_melted_female_villager_npc_right":        _load("sprites/npc_e_melted_villager_female/elucidate_idle_melted_female_villager_npc_right.png", True),
	"idle_melted_female_villager_npc_left":        _load("sprites/npc_e_melted_villager_female/elucidate_idle_melted_female_villager_npc_left.png", True),
	"idle_melted_female_villager_npc_down":        _load("sprites/npc_e_melted_villager_female/elucidate_idle_melted_female_villager_npc_down.png", True),
	"idle_corrupted3_cultist_npc_up":        _load("sprites/npc_e_s3_corrupted_cultist/elucidate_idle_corrupted3_cultist_npc_up.png", True),
	"idle_corrupted3_cultist_npc_right":        _load("sprites/npc_e_s3_corrupted_cultist/elucidate_idle_corrupted3_cultist_npc_right.png", True),
	"idle_corrupted3_cultist_npc_left":        _load("sprites/npc_e_s3_corrupted_cultist/elucidate_idle_corrupted3_cultist_npc_left.png", True),
	"idle_corrupted3_cultist_npc_down":        _load("sprites/npc_e_s3_corrupted_cultist/elucidate_idle_corrupted3_cultist_npc_down.png", True),
	"idle_corrupted2_cultist_npc_up":        _load("sprites/npc_e_s2_corrupted_cultist/elucidate_idle_corrupted2_cultist_npc_up.png", True),
	"idle_corrupted2_cultist_npc_right":        _load("sprites/npc_e_s2_corrupted_cultist/elucidate_idle_corrupted2_cultist_npc_right.png", True),
	"idle_corrupted2_cultist_npc_left":        _load("sprites/npc_e_s2_corrupted_cultist/elucidate_idle_corrupted2_cultist_npc_left.png", True),
	"idle_corrupted2_cultist_npc_down":        _load("sprites/npc_e_s2_corrupted_cultist/elucidate_idle_corrupted2_cultist_npc_down.png", True),
	"idle_librarian_scholar_npc_up":        _load("sprites/npc_n_librarian_scholar/elucidate_idle_librarian_scholar_npc_up.png", True),
	"idle_librarian_scholar_npc_right":        _load("sprites/npc_n_librarian_scholar/elucidate_idle_librarian_scholar_npc_right.png", True),
	"idle_librarian_scholar_npc_left":        _load("sprites/npc_n_librarian_scholar/elucidate_idle_librarian_scholar_npc_left.png", True),
	"idle_librarian_scholar_npc_down":        _load("sprites/npc_n_librarian_scholar/elucidate_idle_librarian_scholar_npc_down.png", True),
	"idle_holyknight_npc_up":        _load("sprites/npc_e_luminarian_knight/elucidate_idle_holyknight_npc_up.png", True),
	"idle_holyknight_npc_right":        _load("sprites/npc_e_luminarian_knight/elucidate_idle_holyknight_npc_right.png", True),
	"idle_holyknight_npc_left":        _load("sprites/npc_e_luminarian_knight/elucidate_idle_holyknight_npc_left.png", True),
	"idle_holyknight_npc_down":        _load("sprites/npc_e_luminarian_knight/elucidate_idle_holyknight_npc_down.png", True),
	"idle_male_faithful_citizen_npc_up":        _load("sprites/npc_n_faithful_luminarian/elucidate_idle_male_faithful_citizen_npc_up.png", True),
	"idle_male_faithful_citizen_npc_right":        _load("sprites/npc_n_faithful_luminarian/elucidate_idle_male_faithful_citizen_npc_right.png", True),
	"idle_male_faithful_citizen_npc_left":        _load("sprites/npc_n_faithful_luminarian/elucidate_idle_male_faithful_citizen_npc_left.png", True),
	"idle_male_faithful_citizen_npc_down":        _load("sprites/npc_n_faithful_luminarian/elucidate_idle_male_faithful_citizen_npc_down.png", True),
	"idle_female_faithful_citizen_npc_up":        _load("sprites/npc_n_faithful_luminarie/elucidate_idle_female_faithful_citizen_npc_up.png", True),
	"idle_female_faithful_citizen_npc_right":        _load("sprites/npc_n_faithful_luminarie/elucidate_idle_female_faithful_citizen_npc_right.png", True),
	"idle_female_faithful_citizen_npc_left":        _load("sprites/npc_n_faithful_luminarie/elucidate_idle_female_faithful_citizen_npc_left.png", True),
	"idle_female_faithful_citizen_npc_down":        _load("sprites/npc_n_faithful_luminarie/elucidate_idle_female_faithful_citizen_npc_down.png", True),
	"idle_sprite_chuAttendants_up":        _load("sprites/npc_n_luminarian_priest/elucidate_idle_sprite_chuAttendants_up.png", True),
	"idle_sprite_chuAttendants_right":        _load("sprites/npc_n_luminarian_priest/elucidate_idle_sprite_chuAttendants_right.png", True),
	"idle_sprite_chuAttendants_left":        _load("sprites/npc_n_luminarian_priest/elucidate_idle_sprite_chuAttendants_left.png", True),
	"idle_sprite_chuAttendants_down":        _load("sprites/npc_n_luminarian_priest/elucidate_idle_sprite_chuAttendants_down.png", True),
	"idle_assassin_npc_up":        _load("sprites/npc_e_lunar_assasin/elucidate_idle_assassin_npc_up.png", True),
	"idle_assassin_npc_right":        _load("sprites/npc_e_lunar_assasin/elucidate_idle_assassin_npc_right.png", True),
	"idle_assassin_npc_left":        _load("sprites/npc_e_lunar_assasin/elucidate_idle_assassin_npc_left.png", True),
	"idle_assassin_npc_down":        _load("sprites/npc_e_lunar_assasin/elucidate_idle_assassin_npc_down.png", True),
	"idle_tribe_warrior_npc_up":        _load("sprites/npc_n_seekers_warrior_male/elucidate_idle_tribe_warrior_npc_up.png", True),
	"idle_tribe_warrior_npc_right":        _load("sprites/npc_n_seekers_warrior_male/elucidate_idle_tribe_warrior_npc_right.png", True),
	"idle_tribe_warrior_npc_left":        _load("sprites/npc_n_seekers_warrior_male/elucidate_idle_tribe_warrior_npc_left.png", True),
	"idle_tribe_warrior_npc_down":        _load("sprites/npc_n_seekers_warrior_male/elucidate_idle_tribe_warrior_npc_down.png", True),
	"idle_tribe_elder_npc_up":        _load("sprites/npc_n_seekers_elder/elucidate_idle_tribe_elder_npc_up.png", True),
	"idle_tribe_elder_npc_right":        _load("sprites/npc_n_seekers_elder/elucidate_idle_tribe_elder_npc_right.png", True),
	"idle_tribe_elder_npc_left":        _load("sprites/npc_n_seekers_elder/elucidate_idle_tribe_elder_npc_left.png", True),
	"idle_tribe_elder_npc_down":        _load("sprites/npc_n_seekers_elder/elucidate_idle_tribe_elder_npc_down.png", True),
	"idle_tribe_chief_npc_up":        _load("sprites/npc_n_seekers_chieftain/elucidate_idle_tribe_chief_npc_up.png", True),
	"idle_tribe_chief_npc_right":        _load("sprites/npc_n_seekers_chieftain/elucidate_idle_tribe_chief_npc_right.png", True),
	"idle_tribe_chief_npc_left":        _load("sprites/npc_n_seekers_chieftain/elucidate_idle_tribe_chief_npc_left.png", True),
	"idle_tribe_chief_npc_down":        _load("sprites/npc_n_seekers_chieftain/elucidate_idle_tribe_chief_npc_down.png", True),
	"idle_supply_merchant_npc_down":        _load("sprites/npc_n_traveling_merchant/elucidate_idle_supply_merchant_npc_down.png", True),
	"idle_supply_merchant_npc_up":        _load("sprites/npc_n_traveling_merchant/elucidate_idle_supply_merchant_npc_up.png", True),
	"idle_supply_merchant_npc_right":        _load("sprites/npc_n_traveling_merchant/elucidate_idle_supply_merchant_npc_right.png", True),
	"idle_supply_merchant_npc_left":        _load("sprites/npc_n_traveling_merchant/elucidate_idle_supply_merchant_npc_left.png", True),
	"idle_merchant_guild_member_npc_up":        _load("sprites/npc_n_merchant_guild_member/elucidate_idle_merchant_guild_npc_up.png", True),
	"idle_merchant_guild_member_npc_right":        _load("sprites/npc_n_merchant_guild_member/elucidate_idle_merchant_guild_npc_right.png", True),
	"idle_merchant_guild_member_npc_left":        _load("sprites/npc_n_merchant_guild_member/elucidate_idle_merchant_guild_npc_left.png", True),
	"idle_merchant_guild_member_npc_down":        _load("sprites/npc_n_merchant_guild_member/elucidate_idle_merchant_guild_npc_down.png", True),
	"idle_merchant_guild_master_npc_up":        _load("sprites/npc_n_merchant_guild_director/elucidate_idle_merchant_guild_master_npc_up.png", True),
	"idle_merchant_guild_master_npc_right":        _load("sprites/npc_n_merchant_guild_director/elucidate_idle_merchant_guild_master_npc_right.png", True),
	"idle_merchant_guild_master_npc_left":        _load("sprites/npc_n_merchant_guild_director/elucidate_idle_merchant_guild_master_npc_left.png", True),
	"idle_merchant_guild_master_npc_down":        _load("sprites/npc_n_merchant_guild_director/elucidate_idle_merchant_guild_master_npc_down.png", True),
	"idle_harbor_captain_npc_up":        _load("sprites/npc_n_harbor_captain/elucidate_idle_harbor_captain_npc_up.png", True),
	"idle_harbor_captain_npc_right":        _load("sprites/npc_n_harbor_captain/elucidate_idle_harbor_captain_npc_right.png", True),
	"idle_harbor_captain_npc_left":        _load("sprites/npc_n_harbor_captain/elucidate_idle_harbor_captain_npc_left.png", True),
	"idle_harbor_captain_npc_down":        _load("sprites/npc_n_harbor_captain/elucidate_idle_harbor_captain_npc_down.png", True),
	"idle_male_villager_variant_npc_up":        _load("sprites/npc_n_s2_outskirts_villagers/elucidate_idle_male_villager_variant_npc_up.png", True),
	"idle_male_villager_variant_npc_right":        _load("sprites/npc_n_s2_outskirts_villagers/elucidate_idle_male_villager_variant_npc_right.png", True),
	"idle_male_villager_variant_npc_left":        _load("sprites/npc_n_s2_outskirts_villagers/elucidate_idle_male_villager_variant_npc_left.png", True),
	"idle_male_villager_variant_npc_down":        _load("sprites/npc_n_s2_outskirts_villagers/elucidate_idle_male_villager_variant_npc_down.png", True),
	"idle_male_villager_npc_up":        _load("sprites/npc_n_s1_outskirts_villagers/elucidate_idle_male_villager_npc_up.png", True),
	"idle_male_villager_npc_right":        _load("sprites/npc_n_s1_outskirts_villagers/elucidate_idle_male_villager_npc_right.png", True),
	"idle_male_villager_npc_left":        _load("sprites/npc_n_s1_outskirts_villagers/elucidate_idle_male_villager_npc_left.png", True),
	"idle_male_villager_npc_down":        _load("sprites/npc_n_s1_outskirts_villagers/elucidate_idle_male_villager_npc_down.png", True),
	"idle_female_villager_variant_npc_up":        _load("sprites/npc_n_s2_outskirts_villagers/elucidate_idle_female_villager_variant_npc_up.png", True),
	"idle_female_villager_variant_npc_right":        _load("sprites/npc_n_s2_outskirts_villagers/elucidate_idle_female_villager_variant_npc_right.png", True),
	"idle_female_villager_variant_npc_left":        _load("sprites/npc_n_s2_outskirts_villagers/elucidate_idle_female_villager_variant_npc_left.png", True),
	"idle_female_villager_variant_npc_down":        _load("sprites/npc_n_s2_outskirts_villagers/elucidate_idle_female_villager_variant_npc_down.png", True),
	"idle_female_villager_npc_up":        _load("sprites/npc_n_s1_outskirts_villagers/elucidate_idle_female_villager_npc_up.png", True),
	"idle_female_villager_npc_right":        _load("sprites/npc_n_s1_outskirts_villagers/elucidate_idle_female_villager_npc_right.png", True),
	"idle_female_villager_npc_left":        _load("sprites/npc_n_s1_outskirts_villagers/elucidate_idle_female_villager_npc_left.png", True),
	"idle_female_villager_npc_down":        _load("sprites/npc_n_s1_outskirts_villagers/elucidate_idle_female_villager_npc_down.png", True),
	"idle_guards_npc_up":        _load("sprites/npc_n_guards/elucidate_idle_guards_npc_up.png", True),
	"idle_guards_npc_right":        _load("sprites/npc_n_guards/elucidate_idle_guards_npc_right.png", True),
	"idle_guards_npc_left":        _load("sprites/npc_n_guards/elucidate_idle_guards_npc_left.png", True),
	"idle_guards_npc_down":        _load("sprites/npc_n_guards/elucidate_idle_guards_npc_down.png", True),
	"idle_guard_captain_npc_up":        _load("sprites/npc_n_guard_captain/elucidate_idle_guard_captain_npc_up.png", True),
	"idle_guard_captain_npc_right":        _load("sprites/npc_n_guard_captain/elucidate_idle_guard_captain_npc_right.png", True),
	"idle_guard_captain_npc_left":        _load("sprites/npc_n_guard_captain/elucidate_idle_guard_captain_npc_left.png", True),
	"idle_guard_captain_npc_down":        _load("sprites/npc_n_guard_captain/elucidate_idle_guard_captain_npc_down.png", True),
	"idle_draft_officer_npc_up":        _load("sprites/npc_n_draft_officer/elucidate_idle_draft_officer_npc_up.png", True),
	"idle_draft_officer_npc_right":        _load("sprites/npc_n_draft_officer/elucidate_idle_draft_officer_npc_right.png", True),
	"idle_draft_officer_npc_left":        _load("sprites/npc_n_draft_officer/elucidate_idle_draft_officer_npc_left.png", True),
	"idle_draft_officer_npc_down":        _load("sprites/npc_n_draft_officer/elucidate_idle_draft_officer_npc_down.png", True),
	"idle_male_civilian_npc_up":        _load("sprites/npc_n_s1_walled_city_civilians_male/elucidate_idle_male_civilian_npc_up.png", True),
	"idle_male_civilian_npc_right":        _load("sprites/npc_n_s1_walled_city_civilians_male/elucidate_idle_male_civilian_npc_right.png", True),
	"idle_male_civilian_npc_left":        _load("sprites/npc_n_s1_walled_city_civilians_male/elucidate_idle_male_civilian_npc_left.png", True),
	"idle_male_civilian_npc_down":        _load("sprites/npc_n_s1_walled_city_civilians_male/elucidate_idle_male_civilian_npc_down.png", True),
	"idle_female_civilian_npc_up":        _load("sprites/npc_n_s1_walled_city_civilians_female/elucidate_idle_female_civilian_npc_up.png", True),
	"idle_female_civilian_npc_right":        _load("sprites/npc_n_s1_walled_city_civilians_female/elucidate_idle_female_civilian_npc_right.png", True),
	"idle_female_civilian_npc_left":        _load("sprites/npc_n_s1_walled_city_civilians_female/elucidate_idle_female_civilian_npc_left.png", True),
	"idle_female_civilian_npc_down":        _load("sprites/npc_n_s1_walled_city_civilians_female/elucidate_idle_female_civilian_npc_down.png", True),
	"idle_blacksmith_npc_up":        _load("sprites/npc_n_blacksmith_conrad/elucidate_idle_blacksmith_npc_up.png", True),
	"idle_blacksmith_npc_right":        _load("sprites/npc_n_blacksmith_conrad/elucidate_idle_blacksmith_npc_right.png", True),
	"idle_blacksmith_npc_left":        _load("sprites/npc_n_blacksmith_conrad/elucidate_idle_blacksmith_npc_left.png", True),
	"idle_blacksmith_npc_down":        _load("sprites/npc_n_blacksmith_conrad/elucidate_idle_blacksmith_npc_down.png", True),
	"idle_caligo_manifestation_npc_down":        _load("sprites/npc_e_caligo_manifestation/elucidate_idle_caligo_manifestation.png", True),
	"idle_caligo_manifestation_black_bg":        _load("sprites/npc_e_caligo_manifestation/elucidate_idle_caligo_manifestation_black_bg.png", True),
	"idle_imprisoned_experiment_1_npc_down":        _load("sprites/npc_e_imprisoned_experiment/elucidate_idle_imprisoned_experiment_1_npc_down.png", True),
	"idle_imprisoned_experiment_2_npc_down":        _load("sprites/npc_e_imprisoned_experiment/elucidate_idle_imprisoned_experiment_2_npc_down.png", True),
	"idle_imprisoned_experiment_hostile_npc_down":        _load("sprites/npc_e_imprisoned_experiment/elucidate_idle_imprisoned_experiment_hostile_npc_down.png", True),
	"idle_church_medical_staff_npc_down":        _load("sprites/npc_n_luminarian_scientist/elucidate_idle_church_medical_staff_npc_down.png", True),
	"idle_church_medical_staff_npc_right":        _load("sprites/npc_n_luminarian_scientist/elucidate_idle_church_medical_staff_npc_right.png", True),
	"idle_church_medical_staff_npc_left":        _load("sprites/npc_n_luminarian_scientist/elucidate_idle_church_medical_staff_npc_left.png", True),
	"idle_church_medical_staff_npc_up":        _load("sprites/npc_n_luminarian_scientist/elucidate_idle_church_medical_staff_npc_up.png", True),
	"idle_church_spy_npc_down":        _load("sprites/npc_e_luminarian_spy/elucidate_idle_church_spy_npc_down.png", True),
	"walk_church_spy_npc_down_001":        _load("sprites/npc_e_luminarian_spy/elucidate_walk_church_spy_npc_down_001.png", True),
	"walk_church_spy_npc_down_002":        _load("sprites/npc_e_luminarian_spy/elucidate_walk_church_spy_npc_down_002.png", True),
	"idle_church_spy_npc_right":        _load("sprites/npc_e_luminarian_spy/elucidate_idle_church_spy_npc_right.png", True),
	"walk_church_spy_npc_right_001":        _load("sprites/npc_e_luminarian_spy/elucidate_walk_church_spy_npc_right_001.png", True),
	"walk_church_spy_npc_right_002":        _load("sprites/npc_e_luminarian_spy/elucidate_walk_church_spy_npc_right_002.png", True),
	"idle_church_spy_npc_left":        _load("sprites/npc_e_luminarian_spy/elucidate_idle_church_spy_npc_left.png", True),
	"walk_church_spy_npc_left_001":        _load("sprites/npc_e_luminarian_spy/elucidate_walk_church_spy_npc_left_001.png", True),
	"walk_church_spy_npc_left_002":        _load("sprites/npc_e_luminarian_spy/elucidate_walk_church_spy_npc_left_002.png", True),
	"idle_church_spy_npc_up":        _load("sprites/npc_e_luminarian_spy/elucidate_idle_church_spy_npc_up.png", True),
	"walk_church_spy_npc_up_001":        _load("sprites/npc_e_luminarian_spy/elucidate_walk_church_spy_npc_up_001.png", True),
	"walk_church_spy_npc_up_002":        _load("sprites/npc_e_luminarian_spy/elucidate_walk_church_spy_npc_up_002.png", True),
	"idle_female_market_merchant_npc_down":        _load("sprites/npc_n_market_merchant_female/elucidate_idle_female_market_merchant_npc_down.png", True),
	"idle_female_market_merchant_npc_right":        _load("sprites/npc_n_market_merchant_female/elucidate_idle_female_market_merchant_npc_right.png", True),
	"idle_female_market_merchant_npc_left":        _load("sprites/npc_n_market_merchant_female/elucidate_idle_female_market_merchant_npc_left.png", True),
	"idle_female_market_merchant_npc_up":        _load("sprites/npc_n_market_merchant_female/elucidate_idle_female_market_merchant_npc_up.png", True),
	"idle_male_market_merchant_npc_down":        _load("sprites/npc_n_market_merchant_male/elucidate_idle_male_market_merchant_npc_down.png", True),
	"idle_male_market_merchant_npc_right":        _load("sprites/npc_n_market_merchant_male/elucidate_idle_male_market_merchant_npc_right.png", True),
	"idle_male_market_merchant_npc_left":        _load("sprites/npc_n_market_merchant_male/elucidate_idle_male_market_merchant_npc_left.png", True),
	"idle_male_market_merchant_npc_up":        _load("sprites/npc_n_market_merchant_male/elucidate_idle_male_market_merchant_npc_up.png", True),
	"idle_ghost_memory1_npc_left":        _load("sprites/npc_n_ghost_memories/elucidate_idle_ghost_memory1_npc_left.png", True),
	"idle_ghost_memory1_npc_right":        _load("sprites/npc_n_ghost_memories/elucidate_idle_ghost_memory1_npc_right.png", True),
	"idle_ghost_memory2_npc_left":        _load("sprites/npc_n_ghost_memories/elucidate_idle_ghost_memory2_npc_left.png", True),
	"idle_ghost_memory2_npc_right":        _load("sprites/npc_n_ghost_memories/elucidate_idle_ghost_memory2_npc_right.png", True),
	"idle_female_tribal_warrior_npc_down":        _load("sprites/npc_n_seekers_warrior_female/elucidate_idle_female_tribal_warrior_npc_down.png", True),
	"idle_female_tribal_warrior_npc_left":        _load("sprites/npc_n_seekers_warrior_female/elucidate_idle_female_tribal_warrior_npc_left.png", True),
	"idle_female_tribal_warrior_npc_right":        _load("sprites/npc_n_seekers_warrior_female/elucidate_idle_female_tribal_warrior_npc_right.png", True),
	"idle_female_tribal_warrior_npc_up":        _load("sprites/npc_n_seekers_warrior_female/elucidate_idle_female_tribal_warrior_npc_up.png", True),
	"idle_travelling_bard_npc_down":        _load("sprites/npc_n_travelling_bard/elucidate_idle_travelling_merchant_npc_down.png", True),
	"idle_travelling_bard_npc_left":        _load("sprites/npc_n_travelling_bard/elucidate_idle_travelling_merchant_npc_left.png", True),
	"idle_travelling_bard_npc_right":        _load("sprites/npc_n_travelling_bard/elucidate_idle_travelling_merchant_npc_right.png", True),
	"idle_travelling_bard_npc_up":        _load("sprites/npc_n_travelling_bard/elucidate_idle_travelling_merchant_npc_up.png", True),
	"idle_cultist_priest_npc_down":        _load("sprites/npc_n_cult_priest/elucidate_idle_cultist_priest_npc_down.png", True),
	"idle_cultist_priest_npc_left":        _load("sprites/npc_n_cult_priest/elucidate_idle_cultist_priest_npc_left.png", True),
	"idle_cultist_priest_npc_right":        _load("sprites/npc_n_cult_priest/elucidate_idle_cultist_priest_npc_right.png", True),
	"idle_cultist_priest_npc_up":        _load("sprites/npc_n_cult_priest/elucidate_idle_cultist_priest_npc_up.png", True),
	"idle_tavern_keeper_npc_down":        _load("sprites/npc_n_tavern_keeper/elucidate_idle_tavern_keeper_npc_down.png", True),
	"idle_tavern_keeper_npc_left":        _load("sprites/npc_n_tavern_keeper/elucidate_idle_tavern_keeper_npc_left.png", True),
	"idle_tavern_keeper_npc_right":        _load("sprites/npc_n_tavern_keeper/elucidate_idle_tavern_keeper_npc_right.png", True),
	"idle_tavern_keeper_npc_up":        _load("sprites/npc_n_tavern_keeper/elucidate_idle_tavern_keeper_npc_up.png", True),
	"idle_cultist_archer_npc_down":        _load("sprites/npc_e_cult_archers/elucidate_idle_cultist_archer_npc_down.png", True),
	"walk_cultist_archer_npc_down_001":        _load("sprites/npc_e_cult_archers/elucidate_walk_cultist_archer_npc_down_001.png", True),
	"walk_cultist_archer_npc_down_002":        _load("sprites/npc_e_cult_archers/elucidate_walk_cultist_archer_npc_down_002.png", True),
	"idle_cultist_archer_npc_left":        _load("sprites/npc_e_cult_archers/elucidate_idle_cultist_archer_npc_left.png", True),
	"walk_cultist_archer_npc_left_001":        _load("sprites/npc_e_cult_archers/elucidate_walk_cultist_archer_npc_left_001.png", True),
	"walk_cultist_archer_npc_left_002":        _load("sprites/npc_e_cult_archers/elucidate_walk_cultist_archer_npc_left_002.png", True),
	"idle_cultist_archer_npc_right":        _load("sprites/npc_e_cult_archers/elucidate_idle_cultist_archer_npc_right.png", True),
	"walk_cultist_archer_npc_right_001":        _load("sprites/npc_e_cult_archers/elucidate_walk_cultist_archer_npc_right_001.png", True),
	"walk_cultist_archer_npc_right_002":        _load("sprites/npc_e_cult_archers/elucidate_walk_cultist_archer_npc_right_002.png", True),
	"idle_cultist_archer_npc_up":        _load("sprites/npc_e_cult_archers/elucidate_idle_cultist_archer_npc_up.png", True),
	"walk_cultist_archer_npc_up_001":        _load("sprites/npc_e_cult_archers/elucidate_walk_cultist_archer_npc_up_001.png", True),
	"walk_cultist_archer_npc_up_002":        _load("sprites/npc_e_cult_archers/elucidate_walk_cultist_archer_npc_up_002.png", True),
	"idle_cultist_channeler_npc_down":        _load("sprites/npc_e_cult_eldritch_channelers/elucidate_idle_cultist_channeler_npc_down.png", True),
	"walk_cultist_chaneller_npc_down_001":        _load("sprites/npc_e_cult_eldritch_channelers/elucidate_walk_cultist_chaneller_npc_down_001.png", True),
	"walk_cultist_chaneller_npc_down_002":        _load("sprites/npc_e_cult_eldritch_channelers/elucidate_walk_cultist_chaneller_npc_down_002.png", True),
	"idle_cultist_channeler_npc_right":        _load("sprites/npc_e_cult_eldritch_channelers/elucidate_idle_cultist_channeler_npc_right.png", True),
	"walk_cultist_chaneller_npc_right_001":        _load("npc_e_cult_eldritch_channelers/elucidate_walk_cultist_chaneller_npc_right_001.png", True),
	"walk_cultist_chaneller_npc_right_002":        _load("npc_e_cult_eldritch_channelers/elucidate_walk_cultist_chaneller_npc_right_002.png", True),
	"idle_cultist_channeler_npc_left":        _load("sprites/npc_e_cult_eldritch_channelers/elucidate_idle_cultist_channeler_npc_left.png", True),
	"walk_cultist_chaneller_npc_left_001":        _load("sprites/npc_e_cult_eldritch_channelers/elucidate_walk_cultist_chaneller_npc_left_001.png", True),
	"walk_cultist_chaneller_npc_left_002":        _load("sprites/npc_e_cult_eldritch_channelers/elucidate_walk_cultist_chaneller_npc_left_002.png", True),
	"idle_cultist_channeler_npc_up":        _load("sprites/npc_e_cult_eldritch_channelers/elucidate_idle_cultist_channeler_npc_up.png", True),
	"walk_cultist_chaneller_npc_up_001":        _load("sprites/npc_e_cult_eldritch_channelers/elucidate_walk_cultist_chaneller_npc_up_001.png", True),
	"walk_cultist_chaneller_npc_up_001":        _load("sprites/npc_e_cult_eldritch_channelers/elucidate_walk_cultist_chaneller_npc_up_002.png", True),
	"idle_assassin_npc_down":        _load("sprites/npc_e_lunar_assasin/elucidate_idle_assassin_npc_down.png", True),
	"walk_church_assassin_npc_down_001":        _load("sprites/npc_e_lunar_assasin/elucidate_walk_church_assassin_npc_down_001.png", True),
	"walk_church_assassin_npc_down_002":        _load("sprites/npc_e_lunar_assasin/elucidate_walk_church_assassin_npc_down_002.png", True),
	"idle_assassin_npc_left":        _load("sprites/npc_e_lunar_assasin/elucidate_idle_assassin_npc_left.png", True),
	"walk_church_assassin_npc_left_001":        _load("sprites/npc_e_lunar_assasin/elucidate_walk_church_assassin_npc_left_001.png", True),
	"walk_church_assassin_npc_left_002":        _load("sprites/npc_e_lunar_assasin/elucidate_walk_church_assassin_npc_left_002.png", True),
	"idle_assassin_npc_right":        _load("sprites/npc_e_lunar_assasin/elucidate_idle_assassin_npc_right.png", True),
	"walk_church_assassin_npc_right_002":        _load("sprites/npc_e_lunar_assasin/elucidate_walk_church_assassin_npc_right_001.png", True),
	"walk_church_assassin_npc_right_002":        _load("sprites/npc_e_lunar_assasin/elucidate_walk_church_assassin_npc_right_002.png", True),
	"idle_assassin_npc_up":        _load("sprites/npc_e_lunar_assasin/elucidate_idle_assassin_npc_up.png", True),
	"walk_church_assassin_npc_up_001":        _load("sprites/npc_e_lunar_assasin/elucidate_walk_church_assassin_npc_up_001.png", True),
	"walk_church_assassin_npc_up_002":        _load("sprites/npc_e_lunar_assasin/elucidate_walk_church_assassin_npc_up_002.png", True),
	"walk_shaman_left_001":        _load("sprites/player_shaman/elucidate_sprite_shaman_left_001.png", True),
	"walk_shaman_left_002":        _load("sprites/player_shaman/elucidate_sprite_shaman_left_002.png", True),
	"idle_shaman_left":        _load("sprites/player_shaman/elucidate_sprite_shaman_left_003.png", True),
	"attack_shaman_left_001":        _load("sprites/player_shaman/elucidate_attack_shaman_left_001.png", True),
	"attack_shaman_left_002":        _load("sprites/player_shaman/elucidate_attack_shaman_left_002.png", True),
	"walk_shaman_down_001":        _load("sprites/player_shaman/elucidate_sprite_shaman_down_001.png", True),
	"walk_shaman_down_002":        _load("sprites/player_shaman/elucidate_sprite_shaman_down_002.png", True),
	"idle_shaman_down":        _load("sprites/player_shaman/elucidate_sprite_shaman_down.png", True),
	"attack_shaman_down_001":        _load("sprites/player_shaman/elucidate_attack_shaman_down_001.png", True),
	"attack_shaman_down_002":        _load("sprites/player_shaman/elucidate_attack_shaman_down_002.png", True),
	"walk_shaman_up_001":        _load("sprites/player_shaman/elucidate_sprite_shaman_up_001.png", True),
	"walk_shaman_up_002":        _load("sprites/player_shaman/elucidate_sprite_shaman_up_002.png", True),
	"idle_shaman_up":        _load("sprites/player_shaman/elucidate_sprite_shaman_up.png", True),
	"attack_shaman_up_001":        _load("sprites/player_shaman/elucidate_attack_shaman_up_001.png", True),
	"attack_shaman_up_002":        _load("sprites/player_shaman/elucidate_attack_shaman_up_002.png", True),
	"walk_shaman_right_001":        _load("sprites/player_shaman/elucidate_sprite_shaman_right_001.png", True),
	"walk_shaman_right_002":        _load("sprites/player_shaman/elucidate_sprite_shaman_right_002.png", True),
	"idle_shaman_right":        _load("sprites/player_shaman/elucidate_sprite_shaman_right_004.png", True),
	"attack_shaman_right_001":        _load("sprites/player_shaman/elucidate_attack_shaman_right_001.png", True),
	"attack_shaman_right_002":        _load("sprites/player_shaman/elucidate_attack_shaman_right_002.png", True),
	"walk_merchant_up_001":        _load("sprites/player_merchant/elucidate_sprite_merchant_up_001.png", True),
	"walk_merchant_up_002":        _load("sprites/player_merchant/elucidate_sprite_merchant_up_002.png", True),
	"idle_merchant_up":        _load("sprites/player_merchant/elucidate_sprite_merchant_up.png", True),
	"attack_merchant_up_001":        _load("sprites/player_merchant/elucidate_attack_merchant_up_001.png", True),
	"attack_merchant_up_002":        _load("sprites/player_merchant/elucidate_attack_merchant_up_002.png", True),
	"walk_merchant_right_001":        _load("sprites/player_merchant/elucidate_sprite_merchant_right_001.png", True),
	"walk_merchant_right_002":        _load("sprites/player_merchant/elucidate_sprite_merchant_right_002.png", True),
	"idle_merchant_right":        _load("sprites/player_merchant/elucidate_sprite_merchant_right_004.png", True),
	"attack_merchant_right_001":        _load("sprites/player_merchant/elucidate_attack_merchant_right_001.png", True),
	"attack_merchant_right_002":        _load("sprites/player_merchant/elucidate_attack_merchant_right_002.png", True),
	"walk_merchant_left_001":        _load("sprites/player_merchant/elucidate_sprite_merchant_left_001.png", True),
	"walk_merchant_left_002":        _load("sprites/player_merchant/elucidate_sprite_merchant_left_002.png", True),
	"idle_merchant_left":        _load("sprites/player_merchant/elucidate_sprite_merchant_left_003.png", True),
	"attack_merchant_left_001":        _load("sprites/player_merchant/elucidate_attack_merchant_left_001.png", True),
	"attack_merchant_left_002":        _load("sprites/player_merchant/elucidate_attack_merchant_left_002.png", True),
	"walk_merchant_down_001":        _load("sprites/player_merchant/elucidate_sprite_merchant_down_001.png", True),
	"walk_merchant_down_002":        _load("sprites/player_merchant/elucidate_sprite_merchant_down_002.png", True),
	"idle_merchant_down":        _load("sprites/player_merchant/elucidate_sprite_merchant_down_002.png", True),
	"attack_merchant_down_001":        _load("sprites/player_merchant/elucidate_attack_merchant_down_001.png", True),
	"attack_merchant_down_002":        _load("sprites/player_merchant/elucidate_attack_merchant_down_002.png", True),
	"walk_priest_left_001":        _load("sprites/player_priest/elucidate_sprite_priest_left_001.png", True),
	"walk_priest_left_002":        _load("sprites/player_priest/elucidate_sprite_priest_left_002.png", True),
	"idle_priest_left":        _load("sprites/player_priest/elucidate_sprite_priest_left.png", True),
	"attack_priest_left_001":        _load("sprites/player_priest/elucidate_attack_priest_left_001.png", True),
	"attack_priest_left_002":        _load("sprites/player_priest/elucidate_attack_priest_left_002.png", True),
	"walk_priest_down_001":        _load("sprites/player_priest/elucidate_sprite_priest_down_001.png", True),
	"walk_priest_down_002":        _load("sprites/player_priest/elucidate_sprite_priest_down_002.png", True),
	"idle_priest_down":        _load("sprites/player_priest/elucidate_sprite_priest_down.png", True),
	"attack_priest_down_001":        _load("sprites/player_priest/elucidate_attack_priest_down_001.png", True),
	"attack_priest_down_002":        _load("sprites/player_priest/elucidate_attack_priest_down_002.png", True),
	"walk_priest_up_001":        _load("sprites/player_priest/elucidate_sprite_priest_up_001.png", True),
	"walk_priest_up_002":        _load("sprites/player_priest/elucidate_sprite_priest_up_002.png", True),
	"idle_priest_up":        _load("sprites/player_priest/elucidate_sprite_priest_up.png", True),
	"attack_priest_up_001":        _load("sprites/player_priest/elucidate_attack_priest_up_001.png", True),
	"attack_priest_up_002":        _load("sprites/player_priest/elucidate_attack_priest_up_002.png", True),
	"walk_priest_right_001":        _load("sprites/player_priest/elucidate_sprite_priest_right_001.png", True),
	"walk_priest_right_002":        _load("sprites/player_priest/elucidate_sprite_priest_right_002.png", True),
	"idle_priest_right":        _load("sprites/player_priest/elucidate_sprite_priest_right.png", True),
	"attack_priest_right_001":        _load("sprites/player_priest/elucidate_attack_priest_right_001.png", True),
	"attack_priest_right_002":        _load("sprites/player_priest/elucidate_attack_priest_right_002.png", True),
	"walk_cultist_down_001":        _load("sprites/player_cultist/elucidate_walking_sprite_cultist_down_001.png", True),
	"walk_cultist_down_002":        _load("sprites/player_cultist/elucidate_walking_sprite_cultist_down_002.png", True),
	"idle_cultist_down":        _load("sprites/player_cultist/elucidate_sprite_cultist_down_002.png", True),
	"attack_cultist_down_001":        _load("sprites/player_cultist/elucidate_attack_cultist_down_001.png", True),
	"attack_cultist_down_002":        _load("sprites/player_cultist/elucidate_attack_cultist_down_002.png", True),
	"walk_cultist_up_001":        _load("sprites/player_cultist/elucidate_walking_sprite_cultist_up_001.png", True),
	"walk_cultist_up_002":        _load("sprites/player_cultist/elucidate_walking_sprite_cultist_up_002.png", True),
	"idle_cultist_up":        _load("sprites/player_cultist/elucidate_sprite_cultist_up_001.png", True),
	"attack_cultist_up_001":        _load("sprites/player_cultist/elucidate_attack_cultist_up_001.png", True),
	"attack_cultist_up_002":        _load("sprites/player_cultist/elucidate_attack_cultist_up_002.png", True),
	"walk_cultist_right_001":        _load("sprites/player_cultist/elucidate_walking_sprite_cultist_right_001.png", True),
	"walk_cultist_right_002":        _load("sprites/player_cultist/elucidate_walking_sprite_cultist_right_002.png", True),
	"idle_cultist_right":        _load("sprites/player_cultist/elucidate_sprite_cultist_right_004.png", True),
	"attack_cultist_right_001":        _load("sprites/player_cultist/elucidate_attack_cultist_right_001.png", True),
	"attack_cultist_right_002":        _load("sprites/player_cultist/elucidate_attack_cultist_right_002.png", True),
	"walk_cultist_left_001":        _load("sprites/player_cultist/elucidate_walking_sprite_cultist_left_001.png", True),
	"walk_cultist_left_002":        _load("sprites/player_cultist/elucidate_walking_sprite_cultist_left_002.png", True),
	"idle_cultist_left":        _load("sprites/player_cultist/elucidate_sprite_cultist_left_003.png", True),
	"attack_cultist_left_001":        _load("sprites/player_cultist/elucidate_attack_cultist_left_001.png", True),
	"attack_cultist_left_002":        _load("sprites/player_cultist/elucidate_attack_cultist_left_002.png", True),
	"attack_sprite_mercenary_up_001":        _load("sprites/player_mercenary/elucidate_atk_sprite_mercenary_up_001.png", True),
	"attack_sprite_mercenary_up_002":        _load("sprites/player_mercenary/elucidate_atk_sprite_mercenary_up_002.png", True),
	"attack_sprite_mercenary_right_001":        _load("sprites/player_mercenary/elucidate_atk_sprite_mercenary_right_001.png", True),
	"attack_sprite_mercenary_right_002":        _load("sprites/player_mercenary/elucidate_atk_sprite_mercenary_right_002.png", True),
	"attack_sprite_mercenary_left_001":        _load("sprites/player_mercenary/elucidate_atk_sprite_mercenary_left_001.png", True),
	"attack_sprite_mercenary_left_002":        _load("sprites/player_mercenary/elucidate_atk_sprite_mercenary_left_002.png", True),
	"attack_sprite_mercenary_down_001":        _load("sprites/player_mercenary/elucidate_atk_sprite_mercenary_down_001.png", True),
	"attack_sprite_mercenary_down_002":        _load("sprites/player_mercenary/elucidate_atk_sprite_mercenary_down_002.png", True),
}
		
_sc = pygame.transform.scale
_scaled_images = {
	"elucidate_title_full":  _sc(_preloaded_images["elucidate_title"], (1275, 710)),
	"elucidate_title_1":     _sc(_preloaded_images["elucidate_title"], (screen_x // 2, screen_y // 2)),
	"elucidate_select_load": _sc(_preloaded_images["elucidate_select_full"], (screen_x // 2, 30)),
	"elucidate_select_home": _sc(_preloaded_images["elucidate_select"], (250, 35)),
	"elucidate_select_inv":  _sc(_preloaded_images["elucidate_select"], (280, 35)),
	"elucidate_select_exit": _sc(_preloaded_images["elucidate_select_full"], (200, 30)),
	"elucidate_select_ui_002_play_select": _sc(_preloaded_images["elucidate_select_ui_002"], (500, 300)),
	"elucidate_mcguy_001_999": _sc(_preloaded_images["elucidate_mcguy_001"], (300, 500)),
	"elucidate_select_home_1": _sc(_preloaded_images["elucidate_select"], (250, 30)),
	"elucidate_no_sprite_idle_1":     _sc(_preloaded_images["elucidate_no_sprite_idle_1"],     (72, 72)),
	"elucidate_no_sprite_idle_2":     _sc(_preloaded_images["elucidate_no_sprite_idle_2"],     (72, 72)),
	"elucidate_no_sprite_idle_3":     _sc(_preloaded_images["elucidate_no_sprite_idle_3"],     (72, 72)),
	"elucidate_no_sprite_idle_4":     _sc(_preloaded_images["elucidate_no_sprite_idle_4"],     (72, 72)),
	"elucidate_no_sprite_walk_1_1":   _sc(_preloaded_images["elucidate_no_sprite_walk_1_1"],   (72, 72)),
	"elucidate_no_sprite_walk_1_2":   _sc(_preloaded_images["elucidate_no_sprite_walk_1_2"],   (72, 72)),
	"elucidate_no_sprite_walk_2_1":   _sc(_preloaded_images["elucidate_no_sprite_walk_2_1"],   (72, 72)),
	"elucidate_no_sprite_walk_2_2":   _sc(_preloaded_images["elucidate_no_sprite_walk_2_2"],   (72, 72)),
	"elucidate_no_sprite_walk_3_1":   _sc(_preloaded_images["elucidate_no_sprite_walk_3_1"],   (72, 72)),
	"elucidate_no_sprite_walk_3_2":   _sc(_preloaded_images["elucidate_no_sprite_walk_3_2"],   (72, 72)),
	"elucidate_no_sprite_walk_4_1":   _sc(_preloaded_images["elucidate_no_sprite_walk_4_1"],   (72, 72)),
	"elucidate_no_sprite_walk_4_2":   _sc(_preloaded_images["elucidate_no_sprite_walk_4_2"],   (72, 72)),
	"elucidate_no_sprite_attack_1_1": _sc(_preloaded_images["elucidate_no_sprite_attack_1_1"], (72, 72)),
	"elucidate_no_sprite_attack_1_2": _sc(_preloaded_images["elucidate_no_sprite_attack_1_2"], (72, 72)),
	"elucidate_no_sprite_attack_2_1": _sc(_preloaded_images["elucidate_no_sprite_attack_2_1"], (72, 72)),
	"elucidate_no_sprite_attack_2_2": _sc(_preloaded_images["elucidate_no_sprite_attack_2_2"], (72, 72)),
	"elucidate_no_sprite_attack_3_1": _sc(_preloaded_images["elucidate_no_sprite_attack_3_1"], (72, 72)),
	"elucidate_no_sprite_attack_3_2": _sc(_preloaded_images["elucidate_no_sprite_attack_3_2"], (72, 72)),
	"elucidate_no_sprite_attack_4_1": _sc(_preloaded_images["elucidate_no_sprite_attack_4_1"], (72, 72)),
	"elucidate_no_sprite_attack_4_2": _sc(_preloaded_images["elucidate_no_sprite_attack_4_2"], (72, 72)),
	"elucidate_dungeon_area_001": _sc(_preloaded_images["elucidate_dungeon_area_001"], (1275, 710)),
	"elucidate_dungeon_area_002": _sc(_preloaded_images["elucidate_dungeon_area_002"], (1275, 710)),
	"elucidate_mercenary_sprite_idle_1":     _sc(_preloaded_images["elucidate_mercenary_sprite_idle_1"],     (72, 72)),
	"elucidate_mercenary_sprite_idle_2":     _sc(_preloaded_images["elucidate_mercenary_sprite_idle_2"],     (72, 72)),
	"elucidate_mercenary_sprite_idle_3":     _sc(_preloaded_images["elucidate_mercenary_sprite_idle_3"],     (72, 72)),
	"elucidate_mercenary_sprite_idle_4":     _sc(_preloaded_images["elucidate_mercenary_sprite_idle_4"],     (72, 72)),
	"elucidate_mercenary_sprite_walk_1_1":   _sc(_preloaded_images["elucidate_mercenary_sprite_walk_1_1"],   (72, 72)),
	"elucidate_mercenary_sprite_walk_1_2":   _sc(_preloaded_images["elucidate_mercenary_sprite_walk_1_2"],   (72, 72)),
	"elucidate_mercenary_sprite_walk_2_1":   _sc(_preloaded_images["elucidate_mercenary_sprite_walk_2_1"],   (72, 72)),
	"elucidate_mercenary_sprite_walk_2_2":   _sc(_preloaded_images["elucidate_mercenary_sprite_walk_2_2"],   (72, 72)),
	"elucidate_mercenary_sprite_walk_3_1":   _sc(_preloaded_images["elucidate_mercenary_sprite_walk_3_1"],   (72, 72)),
	"elucidate_mercenary_sprite_walk_3_2":   _sc(_preloaded_images["elucidate_mercenary_sprite_walk_3_2"],   (72, 72)),
	"elucidate_mercenary_sprite_walk_4_1":   _sc(_preloaded_images["elucidate_mercenary_sprite_walk_4_1"],   (72, 72)),
	"elucidate_mercenary_sprite_walk_4_2":   _sc(_preloaded_images["elucidate_mercenary_sprite_walk_4_2"],   (72, 72)),
	"elucidate_mercenary_sprite_attack_1_1": _sc(_preloaded_images["elucidate_mercenary_sprite_attack_1_1"], (72, 72)),
	"elucidate_mercenary_sprite_attack_1_2": _sc(_preloaded_images["elucidate_mercenary_sprite_attack_1_2"], (72, 72)),
	"elucidate_mercenary_sprite_attack_2_1": _sc(_preloaded_images["elucidate_mercenary_sprite_attack_2_1"], (72, 72)),
	"elucidate_mercenary_sprite_attack_2_2": _sc(_preloaded_images["elucidate_mercenary_sprite_attack_2_2"], (72, 72)),
	"elucidate_mercenary_sprite_attack_3_1": _sc(_preloaded_images["elucidate_mercenary_sprite_attack_3_1"], (72, 72)),
	"elucidate_mercenary_sprite_attack_3_2": _sc(_preloaded_images["elucidate_mercenary_sprite_attack_3_2"], (72, 72)),
	"elucidate_mercenary_sprite_attack_4_1": _sc(_preloaded_images["elucidate_mercenary_sprite_attack_4_1"], (72, 72)),
	"elucidate_mercenary_sprite_attack_4_2": _sc(_preloaded_images["elucidate_mercenary_sprite_attack_4_2"], (72, 72)),
	"elucidate_npc_test_no_sprite": _sc(_preloaded_images["elucidate_no_texture"], (72, 72)),
	"weapon_1handed_short_sword":_sc(_preloaded_images["weapon_1handed_short_sword"],(48,48)),
	"weapon_1handed_cleaver":_sc(_preloaded_images["weapon_1handed_cleaver"],(48,48)),
	"weapon_1handed_knife":_sc(_preloaded_images["weapon_1handed_knife"],(48,48)),
	"materials_sheet_ancient_paper":_sc(_preloaded_images["materials_sheet_ancient_paper"],(48,48)),
	"armour_headware_iron_mask":_sc(_preloaded_images["armour_headware_iron_mask"],(48,48)),
	"armour_body_armour_dark_priests_robe":_sc(_preloaded_images["armour_body_armour_dark_priests_robe"],(48,48)),
	"armour_body_armour_priests_robe":_sc(_preloaded_images["armour_body_armour_priests_robe"],(48,48)),
	"armour_headware_plate_helmet":_sc(_preloaded_images["armour_headware_plate_helmet"],(48,48)),
	"armour_headware_padded_cap":_sc(_preloaded_images["armour_headware_padded_cap"],(48,48)),
	"armour_body_armour_iron_cuirass":_sc(_preloaded_images["armour_body_armour_iron_cuirass"],(48,48)),
	"armour_body_armour_loincloth":_sc(_preloaded_images["armour_body_armour_loincloth"],(48,48)),
	"armour_accessories_red_scarf":_sc(_preloaded_images["armour_accessories_red_scarf"],(48,48)),
	"armour_headware_iron_helmet":_sc(_preloaded_images["armour_headware_iron_helmet"],(48,48)),
	"armour_headware_guard_bascinet":_sc(_preloaded_images["armour_headware_guard_bascinet"],(48,48)),
	"armour_headware_guard_coif":_sc(_preloaded_images["armour_headware_guard_coif"],(48,48)),
	"armour_headware_chainmail_hood":_sc(_preloaded_images["armour_headware_chainmail_hood"],(48,48)),
	"armour_body_armour_black_dress":_sc(_preloaded_images["armour_body_armour_black_dress"],(48,48)),
	"armour_body_armour_trench_coat":_sc(_preloaded_images["armour_body_armour_trench_coat"],(48,48)),
	"weapon_1handed_corsairs_saber":_sc(_preloaded_images["weapon_1handed_corsairs_saber"],(48,48)),
	"weapon_1handed_cloth_hood":_sc(_preloaded_images["weapon_1handed_cloth_hood"],(48,48)),
	"armour_body_armour_leather_coat":_sc(_preloaded_images["armour_body_armour_leather_coat"],(48,48)),
	"armour_body_armour_leather_jvest":_sc(_preloaded_images["armour_body_armour_leather_jvest"],(48,48)),
	"armour_body_armour_plated_mail":_sc(_preloaded_images["armour_body_armour_plated_mail"],(48,48)),
	"armour_shield_scutum":_sc(_preloaded_images["armour_shield_scutum"],(48,48)),
	"weapon_longrange_musket":_sc(_preloaded_images["weapon_longrange_musket"],(48,48)),
	"weapon_2handed_spear":_sc(_preloaded_images["weapon_2handed_spear"],(48,48)),
	"armour_body_armour_hard_leather_armor":_sc(_preloaded_images["armour_body_armour_hard_leather_armor"],(48,48)),
	"armour_body_armour_iron_plate":_sc(_preloaded_images["armour_body_armour_iron_plate"],(48,48)),
	"weapon_1handed_stiletto":_sc(_preloaded_images["weapon_1handed_stiletto"],(48,48)),
	"armour_armwear_arm_guard":_sc(_preloaded_images["armour_armwear_arm_guard"],(48,48)),
	"weapon_1handed_iron_axe":_sc(_preloaded_images["weapon_1handed_iron_axe"],(48,48)),
	"weapon_longrange_short_bow":_sc(_preloaded_images["weapon_longrange_short_bow"],(48,48)),
	"materials_scrap_leather_scraps":_sc(_preloaded_images["materials_scrap_leather_scraps"],(48,48)),
	"materials_skill_book_of_rapid_fire":_sc(_preloaded_images["materials_skill_book_of_rapid_fire"],(48,48)),
	"materials_skill_book_of_instincts":_sc(_preloaded_images["materials_skill_book_of_instincts"],(48,48)),
	"armour_accessories_swift_boots":_sc(_preloaded_images["armour_accessories_swift_boots"],(48,48)),
	"weapon_longrange_heavy_crossbow":_sc(_preloaded_images["weapon_longrange_heavy_crossbow"],(48,48)),
	"weapon_longrange_longbow":_sc(_preloaded_images["weapon_longrange_longbow"],(48,48)),
	"weapon_2handed_maul":_sc(_preloaded_images["weapon_2handed_maul"],(48,48)),
	"weapon_2handed_claymore":_sc(_preloaded_images["weapon_2handed_claymore"],(48,48)),
	"weapon_1handed_scimitar":_sc(_preloaded_images["weapon_1handed_scimitar"],(48,48)),
	"weapon_1handed_improvised_shiv":_sc(_preloaded_images["weapon_1handed_improvised_shiv"],(48,48)),
	"weapon_1handed_steel_hammer":_sc(_preloaded_images["weapon_1handed_steel_hammer"],(48,48)),
	"material_toy_black_dressed_doll":_sc(_preloaded_images["material_toy_black_dressed_doll"],(48,48)),
	"weapon_1handed_dirk":_sc(_preloaded_images["weapon_1handed_dirk"],(48,48)),
	"materials_plank_wooden_plank":_sc(_preloaded_images["materials_plank_wooden_plank"],(48,48)),
	"weapon_1handed_dagger":_sc(_preloaded_images["weapon_1handed_dagger"],(48,48)),
	"materials_component_silver_wire":_sc(_preloaded_images["materials_component_silver_wire"],(48,48)),
	"armour_accessories_red_amulet":_sc(_preloaded_images["armour_accessories_red_amulet"],(48,48)),
	"armour_accessories_blue_amulet":_sc(_preloaded_images["armour_accessories_blue_amulet"],(48,48)),
	"materials_component_stick":_sc(_preloaded_images["materials_component_stick"],(48,48)),
	"armour_accessories_ring":_sc(_preloaded_images["armour_accessories_ring"],(48,48)),
	"materials_skill_book_of_marksmanship":_sc(_preloaded_images["materials_skill_book_of_marksmanship"],(48,48)),
	"materials_skill_book_of_stars":_sc(_preloaded_images["materials_skill_book_of_stars"],(48,48)),
	"materials_skill_book_of_crafsmanship":_sc(_preloaded_images["materials_skill_book_of_crafsmanship"],(48,48)),
	"materials_skill_book_of_agility":_sc(_preloaded_images["materials_skill_book_of_agility"],(48,48)),
	"materials_skill_book_of_healing":_sc(_preloaded_images["materials_skill_book_of_healing"],(48,48)),
	"materials_skill_book_of_the_secrets":_sc(_preloaded_images["materials_skill_book_of_the_secrets"],(48,48)),
	"materials_save_book_of_enlightenment":_sc(_preloaded_images["materials_save_book_of_enlightenment"],(48,48)),
	"materials_skill_book_of_cowardice_i":_sc(_preloaded_images["materials_skill_book_of_cowardice_i"],(48,48)),
	"materials_skill_book_of_cowardice_ii":_sc(_preloaded_images["materials_skill_book_of_cowardice_ii"],(48,48)),
	"materials_skill_book_of_pestilence_i":_sc(_preloaded_images["materials_skill_book_of_pestilence_i"],(48,48)),
	"materials_skill_book_of_pestilence_ii":_sc(_preloaded_images["materials_skill_book_of_pestilence_ii"],(48,48)),
	"materials_skill_book_of_pestilence_iii":_sc(_preloaded_images["materials_skill_book_of_pestilence_iii"],(48,48)),
	"materials_skill_book_of_pestilence_iv":_sc(_preloaded_images["materials_skill_book_of_pestilence_iv"],(48,48)),
	"materials_skill_book_of_pestilence_v":_sc(_preloaded_images["materials_skill_book_of_pestilence_v"],(48,48)),
	"materials_skill_book_of_pestilence_vi":_sc(_preloaded_images["materials_skill_book_of_pestilence_vi"],(48,48)),
	"materials_skill_book_of_pestilence_vii":_sc(_preloaded_images["materials_skill_book_of_pestilence_vii"],(48,48)),
	"materials_skill_book_of_pestilence_viii":_sc(_preloaded_images["materials_skill_book_of_pestilence_viii"],(48,48)),
	"materials_skill_book_of_trade_i":_sc(_preloaded_images["materials_skill_book_of_trade_i"],(48,48)),
	"materials_skill_book_of_trade_ii":_sc(_preloaded_images["materials_skill_book_of_trade_ii"],(48,48)),
	"materials_skill_book_of_trade_iii":_sc(_preloaded_images["materials_skill_book_of_trade_iii"],(48,48)),
	"materials_gem_red_gem":_sc(_preloaded_images["materials_gem_red_gem"],(48,48)),
	"materials_gem_blue_gem":_sc(_preloaded_images["materials_gem_blue_gem"],(48,48)),
	"materials_beverage_ale":_sc(_preloaded_images["materials_beverage_ale"],(48,48)),
	"materials_beverage_wine":_sc(_preloaded_images["materials_beverage_wine"],(48,48)),
	"materials_beverage_rum":_sc(_preloaded_images["materials_beverage_rum"],(48,48)),
	"materials_bar_iron_ingot":_sc(_preloaded_images["materials_bar_iron_ingot"],(48,48)),
	"materials_ore_raw_iron":_sc(_preloaded_images["materials_ore_raw_iron"],(48,48)),
	"materials_foliage_blue_herb-1":_sc(_preloaded_images["materials_foliage_blue_herb-1"],(48,48)),
	"materials_foliage_green_herb":_sc(_preloaded_images["materials_foliage_green_herb"],(48,48)),
	"materials_sheet_paper":_sc(_preloaded_images["materials_sheet_paper"],(48,48)),
	"materials_potion_antibiotics":_sc(_preloaded_images["materials_potion_antibiotics"],(48,48)),
	"materials_potion_betadine":_sc(_preloaded_images["materials_potion_betadine"],(48,48)),
	"materials_potion_red_vial":_sc(_preloaded_images["materials_potion_red_vial"],(48,48)),
	"materials_container_empty_vial":_sc(_preloaded_images["materials_container_empty_vial"],(48,48)),
	"weapon_2handed_longsword":_sc(_preloaded_images["weapon_2handed_longsword"],(48,48)),
	"armour_shield_wooden_buckler":_sc(_preloaded_images["armour_shield_wooden_buckler"],(48,48)),
	"weapon_1handed_cultist_dagger":_sc(_preloaded_images["weapon_1handed_cultist_dagger"],(48,48)),
	"weapon_longrange_flintlock":_sc(_preloaded_images["weapon_longrange_flintlock"],(48,48)),
	"weapon_2handed_makeshift_spear":_sc(_preloaded_images["weapon_2handed_makeshift_spear"],(48,48)),
	"weapon_longrange_blunderbuss":_sc(_preloaded_images["weapon_longrange_blunderbuss"],(48,48)),
	"weapon_1handed_shaman_dagger":_sc(_preloaded_images["weapon_1handed_shaman_dagger"],(48,48)),
	"weapon_2handed_priest_staff":_sc(_preloaded_images["weapon_2handed_priest_staff"],(48,48)),
	"weapon_longrange_cultist_crossbow":_sc(_preloaded_images["weapon_longrange_cultist_crossbow"],(48,48)),
	"materials_component_bow_string":_sc(_preloaded_images["materials_component_bow_string"],(48,48)),
	"elucidate_silver_chest_closed_001":     _sc(_preloaded_images["silver_chest_closed"],     (48, 48)),
	"elucidate_silver_chest_opened_002":     _sc(_preloaded_images["silver_chest_opened"],     (48, 48)),
	"elucidate_gold_chest_closed_003":     _sc(_preloaded_images["gold_chest_closed"],     (48, 48)),
	"elucidate_gold_chest_opened_004":     _sc(_preloaded_images["gold_chest_opened"],     (48, 48)),
	"elucidate_idle_cult_leader_npc_down":     _sc(_preloaded_images["idle_cult_leader_npc_down"],     (72, 72)),
	"elucidate_idle_cult_leader_npc_up":     _sc(_preloaded_images["idle_cult_leader_npc_up"],     (72, 72)),
	"elucidate_idle_cult_leader_npc_left":     _sc(_preloaded_images["idle_cult_leader_npc_left"],     (72, 72)),
	"elucidate_idle_cult_leader_npc_right":     _sc(_preloaded_images["idle_cult_leader_npc_right"],     (72, 72)),
	"elucidate_idle_cultist_npc_up":     _sc(_preloaded_images["idle_cultist_npc_up"],     (72, 72)),
	"elucidate_idle_cultist_npc_right":     _sc(_preloaded_images["idle_cultist_npc_right"],     (72, 72)),
	"elucidate_idle_cultist_npc_left":     _sc(_preloaded_images["idle_cultist_npc_left"],     (72, 72)),
	"elucidate_idle_cultist_npc_down":     _sc(_preloaded_images["idle_cultist_npc_down"],     (72, 72)),
	"elucidate_idle_corrupted1_cultist_npc_right":     _sc(_preloaded_images["idle_corrupted1_cultist_npc_right"],     (72, 72)),
	"elucidate_idle_corrupted1_cultist_npc_left":     _sc(_preloaded_images["idle_corrupted1_cultist_npc_left"],     (72, 72)),
	"elucidate_idle_corrupted1_cultist_npc_down":     _sc(_preloaded_images["idle_corrupted1_cultist_npc_down"],     (72, 72)),
	"elucidate_idle_corrupted1_cultist_npc_up":     _sc(_preloaded_images["idle_corrupted1_cultist_npc_up"],     (72, 72)),
	"elucidate_idle_amalgamated_villagers_npc_right":     _sc(_preloaded_images["idle_amalgamated_villagers_npc_right"],     (72, 72)),
	"elucidate_idle_amalgamated_villagers_npc_left":     _sc(_preloaded_images["idle_amalgamated_villagers_npc_left"],     (72, 72)),
	"elucidate_idle_amalgamated_knights_npc_right":     _sc(_preloaded_images["idle_amalgamated_knights_npc_right"],     (72, 72)),
	"elucidate_idle_amalgamated_knights_npc_left":     _sc(_preloaded_images["idle_amalgamated_knights_npc_left"],     (72, 72)),
	"elucidate_idle_amalgamated_civillians_npc_right":     _sc(_preloaded_images["idle_amalgamated_civillians_npc_right"],     (72, 72)),
	"elucidate_idle_amalgamated_civillians_npc_left":     _sc(_preloaded_images["idle_amalgamated_civillians_npc_left"],     (72, 72)),
	"elucidate_idle_melted_male_villager_npc_right":     _sc(_preloaded_images["idle_melted_male_villager_npc_right"],     (72, 72)),
	"elucidate_idle_melted_male_villager_npc_left":     _sc(_preloaded_images["idle_melted_male_villager_npc_left"],     (72, 72)),
	"elucidate_idle_melted_male_villager_npc_up":     _sc(_preloaded_images["idle_melted_male_villager_npc_up"],     (72, 72)),
	"elucidate_idle_melted_male_villager_npc_down":     _sc(_preloaded_images["idle_melted_male_villager_npc_down"],     (72, 72)),
	"elucidate_idle_melted_female_villager_npc_up":     _sc(_preloaded_images["idle_melted_female_villager_npc_up"],     (72, 72)),
	"elucidate_idle_melted_female_villager_npc_right":     _sc(_preloaded_images["idle_melted_female_villager_npc_right"],     (72, 72)),
	"elucidate_idle_melted_female_villager_npc_left":     _sc(_preloaded_images["idle_melted_female_villager_npc_left"],     (72, 72)),
	"elucidate_idle_melted_female_villager_npc_down":     _sc(_preloaded_images["idle_melted_female_villager_npc_down"],     (72, 72)),
	"elucidate_idle_corrupted3_cultist_npc_up":     _sc(_preloaded_images["idle_corrupted3_cultist_npc_up"],     (72, 72)),
	"elucidate_idle_corrupted3_cultist_npc_right":     _sc(_preloaded_images["idle_corrupted3_cultist_npc_right"],     (72, 72)),
	"elucidate_idle_corrupted3_cultist_npc_left":     _sc(_preloaded_images["idle_corrupted3_cultist_npc_left"],     (72, 72)),
	"elucidate_idle_corrupted3_cultist_npc_down":     _sc(_preloaded_images["idle_corrupted3_cultist_npc_down"],     (72, 72)),
	"elucidate_idle_corrupted2_cultist_npc_up":     _sc(_preloaded_images["idle_corrupted2_cultist_npc_up"],     (72, 72)),
	"elucidate_idle_corrupted2_cultist_npc_right":     _sc(_preloaded_images["idle_corrupted2_cultist_npc_right"],     (72, 72)),
	"elucidate_idle_corrupted2_cultist_npc_left":     _sc(_preloaded_images["idle_corrupted2_cultist_npc_left"],     (72, 72)),
	"elucidate_idle_corrupted2_cultist_npc_down":     _sc(_preloaded_images["idle_corrupted2_cultist_npc_down"],     (72, 72)),
	"elucidate_idle_librarian_scholar_npc_up":     _sc(_preloaded_images["idle_librarian_scholar_npc_up"],     (72, 72)),
	"elucidate_idle_librarian_scholar_npc_right":     _sc(_preloaded_images["idle_librarian_scholar_npc_right"],     (72, 72)),
	"elucidate_idle_librarian_scholar_npc_left":     _sc(_preloaded_images["idle_librarian_scholar_npc_left"],     (72, 72)),
	"elucidate_idle_librarian_scholar_npc_down":     _sc(_preloaded_images["idle_librarian_scholar_npc_down"],     (72, 72)),
	"elucidate_idle_holyknight_npc_up":     _sc(_preloaded_images["idle_holyknight_npc_up"],     (72, 72)),
	"elucidate_idle_holyknight_npc_right":     _sc(_preloaded_images["idle_holyknight_npc_right"],     (72, 72)),
	"elucidate_idle_holyknight_npc_left":     _sc(_preloaded_images["idle_holyknight_npc_left"],     (72, 72)),
	"elucidate_idle_holyknight_npc_down":     _sc(_preloaded_images["idle_holyknight_npc_down"],     (72, 72)),
	"elucidate_idle_male_faithful_citizen_npc_up":     _sc(_preloaded_images["idle_male_faithful_citizen_npc_up"],     (72, 72)),
	"elucidate_idle_male_faithful_citizen_npc_right":     _sc(_preloaded_images["idle_male_faithful_citizen_npc_right"],     (72, 72)),
	"elucidate_idle_male_faithful_citizen_npc_left":     _sc(_preloaded_images["idle_male_faithful_citizen_npc_left"],     (72, 72)),
	"elucidate_idle_male_faithful_citizen_npc_down":     _sc(_preloaded_images["idle_male_faithful_citizen_npc_down"],     (72, 72)),
	"elucidate_idle_female_faithful_citizen_npc_up":     _sc(_preloaded_images["idle_female_faithful_citizen_npc_up"],     (72, 72)),
	"elucidate_idle_female_faithful_citizen_npc_right":     _sc(_preloaded_images["idle_female_faithful_citizen_npc_right"],     (72, 72)),
	"elucidate_idle_female_faithful_citizen_npc_left":     _sc(_preloaded_images["idle_female_faithful_citizen_npc_left"],     (72, 72)),
	"elucidate_idle_female_faithful_citizen_npc_down":     _sc(_preloaded_images["idle_female_faithful_citizen_npc_down"],     (72, 72)),
	"elucidate_idle_sprite_chuAttendants_up":     _sc(_preloaded_images["idle_sprite_chuAttendants_up"],     (72, 72)),
	"elucidate_idle_sprite_chuAttendants_right":     _sc(_preloaded_images["idle_sprite_chuAttendants_right"],     (72, 72)),
	"elucidate_idle_sprite_chuAttendants_left":     _sc(_preloaded_images["idle_sprite_chuAttendants_left"],     (72, 72)),
	"elucidate_idle_sprite_chuAttendants_down":     _sc(_preloaded_images["idle_sprite_chuAttendants_down"],     (72, 72)),
	"elucidate_idle_assassin_npc_up":     _sc(_preloaded_images["idle_assassin_npc_up"],     (72, 72)),
	"elucidate_idle_assassin_npc_right":     _sc(_preloaded_images["idle_assassin_npc_right"],     (72, 72)),
	"elucidate_idle_assassin_npc_left":     _sc(_preloaded_images["idle_assassin_npc_left"],     (72, 72)),
	"elucidate_idle_assassin_npc_down":     _sc(_preloaded_images["idle_assassin_npc_down"],     (72, 72)),
	"elucidate_idle_tribe_warrior_npc_up":     _sc(_preloaded_images["idle_tribe_warrior_npc_up"],     (72, 72)),
	"elucidate_idle_tribe_warrior_npc_right":     _sc(_preloaded_images["idle_tribe_warrior_npc_right"],     (72, 72)),
	"elucidate_idle_tribe_warrior_npc_left":     _sc(_preloaded_images["idle_tribe_warrior_npc_left"],     (72, 72)),
	"elucidate_idle_tribe_warrior_npc_down":     _sc(_preloaded_images["idle_tribe_warrior_npc_down"],     (72, 72)),
	"elucidate_idle_tribe_elder_npc_up":     _sc(_preloaded_images["idle_tribe_elder_npc_up"],     (72, 72)),
	"elucidate_idle_tribe_elder_npc_right":     _sc(_preloaded_images["idle_tribe_elder_npc_right"],     (72, 72)),
	"elucidate_idle_tribe_elder_npc_left":     _sc(_preloaded_images["idle_tribe_elder_npc_left"],     (72, 72)),
	"elucidate_idle_tribe_elder_npc_down":     _sc(_preloaded_images["idle_tribe_elder_npc_down"],     (72, 72)),
	"elucidate_idle_tribe_chief_npc_up":     _sc(_preloaded_images["idle_tribe_chief_npc_up"],     (72, 72)),
	"elucidate_idle_tribe_chief_npc_right":     _sc(_preloaded_images["idle_tribe_chief_npc_right"],     (72, 72)),
	"elucidate_idle_tribe_chief_npc_left":     _sc(_preloaded_images["idle_tribe_chief_npc_left"],     (72, 72)),
	"elucidate_idle_tribe_chief_npc_down":     _sc(_preloaded_images["idle_tribe_chief_npc_down"],     (72, 72)),
	"elucidate_idle_supply_merchant_npc_down":     _sc(_preloaded_images["idle_supply_merchant_npc_down"],     (72, 72)),
	"elucidate_idle_supply_merchant_npc_up":     _sc(_preloaded_images["idle_supply_merchant_npc_up"],     (72, 72)),
	"elucidate_idle_supply_merchant_npc_right":     _sc(_preloaded_images["idle_supply_merchant_npc_right"],     (72, 72)),
	"elucidate_idle_supply_merchant_npc_left":     _sc(_preloaded_images["idle_supply_merchant_npc_left"],     (72, 72)),
	"elucidate_idle_merchant_guild_npc_up":     _sc(_preloaded_images["idle_merchant_guild_member_npc_up"],     (72, 72)),
	"elucidate_idle_merchant_guild_npc_right":     _sc(_preloaded_images["idle_merchant_guild_member_npc_right"],     (72, 72)),
	"elucidate_idle_merchant_guild_npc_left":     _sc(_preloaded_images["idle_merchant_guild_member_npc_left"],     (72, 72)),
	"elucidate_idle_merchant_guild_npc_down":     _sc(_preloaded_images["idle_merchant_guild_member_npc_down"],     (72, 72)),
	"elucidate_idle_merchant_guild_master_npc_up":     _sc(_preloaded_images["idle_merchant_guild_master_npc_up"],     (72, 72)),
	"elucidate_idle_merchant_guild_master_npc_right":     _sc(_preloaded_images["idle_merchant_guild_master_npc_right"],     (72, 72)),
	"elucidate_idle_merchant_guild_master_npc_left":     _sc(_preloaded_images["idle_merchant_guild_master_npc_left"],     (72, 72)),
	"elucidate_idle_merchant_guild_master_npc_down":     _sc(_preloaded_images["idle_merchant_guild_master_npc_down"],     (72, 72)),
	"elucidate_idle_harbor_captain_npc_up":     _sc(_preloaded_images["idle_harbor_captain_npc_up"],     (72, 72)),
	"elucidate_idle_harbor_captain_npc_right":     _sc(_preloaded_images["idle_harbor_captain_npc_right"],     (72, 72)),
	"elucidate_idle_harbor_captain_npc_left":     _sc(_preloaded_images["idle_harbor_captain_npc_left"],     (72, 72)),
	"elucidate_idle_harbor_captain_npc_down":     _sc(_preloaded_images["idle_harbor_captain_npc_down"],     (72, 72)),
	"elucidate_idle_male_villager_variant_npc_up":     _sc(_preloaded_images["idle_male_villager_variant_npc_up"],     (72, 72)),
	"elucidate_idle_male_villager_variant_npc_right":     _sc(_preloaded_images["idle_male_villager_variant_npc_right"],     (72, 72)),
	"elucidate_idle_male_villager_variant_npc_left":     _sc(_preloaded_images["idle_male_villager_variant_npc_left"],     (72, 72)),
	"elucidate_idle_male_villager_variant_npc_down":     _sc(_preloaded_images["idle_male_villager_variant_npc_down"],     (72, 72)),
	"elucidate_idle_male_villager_npc_up":     _sc(_preloaded_images["idle_male_villager_npc_up"],     (72, 72)),
	"elucidate_idle_male_villager_npc_right":     _sc(_preloaded_images["idle_male_villager_npc_right"],     (72, 72)),
	"elucidate_idle_male_villager_npc_left":     _sc(_preloaded_images["idle_male_villager_npc_left"],     (72, 72)),
	"elucidate_idle_male_villager_npc_down":     _sc(_preloaded_images["idle_male_villager_npc_down"],     (72, 72)),
	"elucidate_idle_female_villager_variant_npc_up":     _sc(_preloaded_images["idle_female_villager_variant_npc_up"],     (72, 72)),
	"elucidate_idle_female_villager_variant_npc_right":     _sc(_preloaded_images["idle_female_villager_variant_npc_right"],     (72, 72)),
	"elucidate_idle_female_villager_variant_npc_left":     _sc(_preloaded_images["idle_female_villager_variant_npc_left"],     (72, 72)),
	"elucidate_idle_female_villager_variant_npc_down":     _sc(_preloaded_images["idle_female_villager_variant_npc_down"],     (72, 72)),
	"elucidate_idle_female_villager_npc_up":     _sc(_preloaded_images["idle_female_villager_npc_up"],     (72, 72)),
	"elucidate_idle_female_villager_npc_right":     _sc(_preloaded_images["idle_female_villager_npc_right"],     (72, 72)),
	"elucidate_idle_female_villager_npc_left":     _sc(_preloaded_images["idle_female_villager_npc_left"],     (72, 72)),
	"elucidate_idle_female_villager_npc_down":     _sc(_preloaded_images["idle_female_villager_npc_down"],     (72, 72)),
	"elucidate_idle_guards_npc_up":     _sc(_preloaded_images["idle_guards_npc_up"],     (72, 72)),
	"elucidate_idle_guards_npc_right":     _sc(_preloaded_images["idle_guards_npc_right"],     (72, 72)),
	"elucidate_idle_guards_npc_left":     _sc(_preloaded_images["idle_guards_npc_left"],     (72, 72)),
	"elucidate_idle_guards_npc_down":     _sc(_preloaded_images["idle_guards_npc_down"],     (72, 72)),
	"elucidate_idle_guard_captain_npc_up":     _sc(_preloaded_images["idle_guard_captain_npc_up"],     (72, 72)),
	"elucidate_idle_guard_captain_npc_right":     _sc(_preloaded_images["idle_guard_captain_npc_right"],     (72, 72)),
	"elucidate_idle_guard_captain_npc_left":     _sc(_preloaded_images["idle_guard_captain_npc_left"],     (72, 72)),
	"elucidate_idle_guard_captain_npc_down":     _sc(_preloaded_images["idle_guard_captain_npc_down"],     (72, 72)),
	"elucidate_idle_draft_officer_npc_up":     _sc(_preloaded_images["idle_draft_officer_npc_up"],     (72, 72)),
	"elucidate_idle_draft_officer_npc_right":     _sc(_preloaded_images["idle_draft_officer_npc_right"],     (72, 72)),
	"elucidate_idle_draft_officer_npc_left":     _sc(_preloaded_images["idle_draft_officer_npc_left"],     (72, 72)),
	"elucidate_idle_draft_officer_npc_down":     _sc(_preloaded_images["idle_draft_officer_npc_down"],     (72, 72)),
	"elucidate_idle_male_civilian_npc_up":     _sc(_preloaded_images["idle_male_civilian_npc_up"],     (72, 72)),
	"elucidate_idle_male_civilian_npc_right":     _sc(_preloaded_images["idle_male_civilian_npc_right"],     (72, 72)),
	"elucidate_idle_male_civilian_npc_left":     _sc(_preloaded_images["idle_male_civilian_npc_left"],     (72, 72)),
	"elucidate_idle_male_civilian_npc_down":     _sc(_preloaded_images["idle_male_civilian_npc_down"],     (72, 72)),
	"elucidate_idle_female_civilian_npc_up":     _sc(_preloaded_images["idle_female_civilian_npc_up"],     (72, 72)),
	"elucidate_idle_female_civilian_npc_right":     _sc(_preloaded_images["idle_female_civilian_npc_right"],     (72, 72)),
	"elucidate_idle_female_civilian_npc_left":     _sc(_preloaded_images["idle_female_civilian_npc_left"],     (72, 72)),
	"elucidate_idle_female_civilian_npc_down":     _sc(_preloaded_images["idle_female_civilian_npc_down"],     (72, 72)),
	"elucidate_idle_blacksmith_npc_up":     _sc(_preloaded_images["idle_blacksmith_npc_up"],     (72, 72)),
	"elucidate_idle_blacksmith_npc_right":     _sc(_preloaded_images["idle_blacksmith_npc_right"],     (72, 72)),
	"elucidate_idle_blacksmith_npc_left":     _sc(_preloaded_images["idle_blacksmith_npc_left"],     (72, 72)),
	"elucidate_idle_blacksmith_npc_down":     _sc(_preloaded_images["idle_blacksmith_npc_down"],     (72, 72)),
	"elucidate_idle_caligo_manifestation":     _sc(_preloaded_images["idle_caligo_manifestation_npc_down"],     (72, 192)),
	"elucidate_idle_caligo_manifestation_black_bg":     _sc(_preloaded_images["idle_caligo_manifestation_black_bg"],     (72, 192)),
	"elucidate_idle_imprisoned_experiment_1_npc_down":     _sc(_preloaded_images["idle_imprisoned_experiment_1_npc_down"],     (72, 72)),
	"elucidate_idle_imprisoned_experiment_2_npc_down":     _sc(_preloaded_images["idle_imprisoned_experiment_2_npc_down"],     (72, 72)),
	"elucidate_idle_imprisoned_experiment_hostile_npc_down":     _sc(_preloaded_images["idle_imprisoned_experiment_hostile_npc_down"],     (72, 72)),
	"elucidate_idle_church_medical_staff_npc_down":     _sc(_preloaded_images["idle_church_medical_staff_npc_down"],     (72, 72)),
	"elucidate_idle_church_medical_staff_npc_right":     _sc(_preloaded_images["idle_church_medical_staff_npc_right"],     (72, 72)),
	"elucidate_idle_church_medical_staff_npc_left":     _sc(_preloaded_images["idle_church_medical_staff_npc_left"],     (72, 72)),
	"elucidate_idle_church_medical_staff_npc_up":     _sc(_preloaded_images["idle_church_medical_staff_npc_up"],     (72, 72)),
	"elucidate_idle_church_spy_npc_down":     _sc(_preloaded_images["idle_church_spy_npc_down"],     (72, 72)),
	"elucidate_walk_church_spy_npc_down_001":     _sc(_preloaded_images["walk_church_spy_npc_down_001"],     (72, 72)),
	"elucidate_walk_church_spy_npc_down_002":     _sc(_preloaded_images["walk_church_spy_npc_down_002"],     (72, 72)),
	"elucidate_idle_church_spy_npc_right":     _sc(_preloaded_images["idle_church_spy_npc_right"],     (72, 72)),
	"elucidate_walk_church_spy_npc_right_001":     _sc(_preloaded_images["walk_church_spy_npc_right_001"],     (72, 72)),
	"elucidate_walk_church_spy_npc_right_002":     _sc(_preloaded_images["walk_church_spy_npc_right_002"],     (72, 72)),
	"elucidate_idle_church_spy_npc_left":     _sc(_preloaded_images["idle_church_spy_npc_left"],     (72, 72)),
	"elucidate_walk_church_spy_npc_left_001":     _sc(_preloaded_images["walk_church_spy_npc_left_001"],     (72, 72)),
	"elucidate_walk_church_spy_npc_left_002":     _sc(_preloaded_images["walk_church_spy_npc_left_002"],     (72, 72)),
	"elucidate_idle_church_spy_npc_up":     _sc(_preloaded_images["idle_church_spy_npc_up"],     (72, 72)),
	"elucidate_walk_church_spy_npc_up_001":     _sc(_preloaded_images["walk_church_spy_npc_up_001"],     (72, 72)),
	"elucidate_walk_church_spy_npc_up_002":     _sc(_preloaded_images["walk_church_spy_npc_up_002"],     (72, 72)),
	"elucidate_idle_female_market_merchant_npc_down":     _sc(_preloaded_images["idle_female_market_merchant_npc_down"],     (72, 72)),
	"elucidate_idle_female_market_merchant_npc_right":     _sc(_preloaded_images["idle_female_market_merchant_npc_right"],     (72, 72)),
	"elucidate_idle_female_market_merchant_npc_left":     _sc(_preloaded_images["idle_female_market_merchant_npc_left"],     (72, 72)),
	"elucidate_idle_female_market_merchant_npc_up":     _sc(_preloaded_images["idle_female_market_merchant_npc_up"],     (72, 72)),
	"elucidate_idle_male_market_merchant_npc_down":     _sc(_preloaded_images["idle_male_market_merchant_npc_down"],     (72, 72)),
	"elucidate_idle_male_market_merchant_npc_right":     _sc(_preloaded_images["idle_male_market_merchant_npc_right"],     (72, 72)),
	"elucidate_idle_male_market_merchant_npc_left":     _sc(_preloaded_images["idle_male_market_merchant_npc_left"],     (72, 72)),
	"elucidate_idle_male_market_merchant_npc_up":     _sc(_preloaded_images["idle_male_market_merchant_npc_up"],     (72, 72)),
	"elucidate_idle_ghost_memory1_npc_left":     _sc(_preloaded_images["idle_ghost_memory1_npc_left"],     (72, 72)),
	"elucidate_idle_ghost_memory1_npc_right":     _sc(_preloaded_images["idle_ghost_memory1_npc_right"],     (72, 72)),
	"elucidate_idle_ghost_memory2_npc_left":     _sc(_preloaded_images["idle_ghost_memory2_npc_left"],     (72, 72)),
	"elucidate_idle_ghost_memory2_npc_right":     _sc(_preloaded_images["idle_ghost_memory2_npc_right"],     (72, 72)),
	"elucidate_idle_female_tribal_warrior_npc_down":     _sc(_preloaded_images["idle_female_tribal_warrior_npc_down"],     (72, 72)),
	"elucidate_idle_female_tribal_warrior_npc_left":     _sc(_preloaded_images["idle_female_tribal_warrior_npc_left"],     (72, 72)),
	"elucidate_idle_female_tribal_warrior_npc_right":     _sc(_preloaded_images["idle_female_tribal_warrior_npc_right"],     (72, 72)),
	"elucidate_idle_female_tribal_warrior_npc_up":     _sc(_preloaded_images["idle_female_tribal_warrior_npc_up"],     (72, 72)),
	"elucidate_idle_travelling_merchant_npc_down":     _sc(_preloaded_images["idle_supply_merchant_npc_down"],     (72, 72)),
	"elucidate_idle_travelling_merchant_npc_left":     _sc(_preloaded_images["idle_supply_merchant_npc_left"],     (72, 72)),
	"elucidate_idle_travelling_merchant_npc_right":     _sc(_preloaded_images["idle_supply_merchant_npc_right"],     (72, 72)),
	"elucidate_idle_travelling_merchant_npc_up":     _sc(_preloaded_images["idle_supply_merchant_npc_up"],     (72, 72)),
	"elucidate_idle_cultist_priest_npc_down":     _sc(_preloaded_images["idle_cultist_priest_npc_down"],     (72, 72)),
	"elucidate_idle_cultist_priest_npc_left":     _sc(_preloaded_images["idle_cultist_priest_npc_left"],     (72, 72)),
	"elucidate_idle_cultist_priest_npc_right":     _sc(_preloaded_images["idle_cultist_priest_npc_right"],     (72, 72)),
	"elucidate_idle_cultist_priest_npc_up":     _sc(_preloaded_images["idle_cultist_priest_npc_up"],     (72, 72)),
	"elucidate_idle_tavern_keeper_npc_down":     _sc(_preloaded_images["idle_tavern_keeper_npc_down"],     (72, 72)),
	"elucidate_idle_tavern_keeper_npc_left":     _sc(_preloaded_images["idle_tavern_keeper_npc_left"],     (72, 72)),
	"elucidate_idle_tavern_keeper_npc_right":     _sc(_preloaded_images["idle_tavern_keeper_npc_right"],     (72, 72)),
	"elucidate_idle_tavern_keeper_npc_up":     _sc(_preloaded_images["idle_tavern_keeper_npc_up"],     (72, 72)),
	"elucidate_idle_cultist_archer_npc_down":     _sc(_preloaded_images["idle_cultist_archer_npc_down"],     (72, 72)),
	"elucidate_walk_cultist_archer_npc_down_001":     _sc(_preloaded_images["walk_cultist_archer_npc_down_001"],     (72, 72)),
	"elucidate_walk_cultist_archer_npc_down_002":     _sc(_preloaded_images["walk_cultist_archer_npc_down_002"],     (72, 72)),
	"elucidate_idle_cultist_archer_npc_left":     _sc(_preloaded_images["idle_cultist_archer_npc_left"],     (72, 72)),
	"elucidate_walk_cultist_archer_npc_left_001":     _sc(_preloaded_images["walk_cultist_archer_npc_left_001"],     (72, 72)),
	"elucidate_walk_cultist_archer_npc_left_002":     _sc(_preloaded_images["walk_cultist_archer_npc_left_002"],     (72, 72)),
	"elucidate_idle_cultist_archer_npc_right":     _sc(_preloaded_images["idle_cultist_archer_npc_right"],     (72, 72)),
	"elucidate_walk_cultist_archer_npc_right_001":     _sc(_preloaded_images["walk_cultist_archer_npc_right_001"],     (72, 72)),
	"elucidate_walk_cultist_archer_npc_right_002":     _sc(_preloaded_images["walk_cultist_archer_npc_right_002"],     (72, 72)),
	"elucidate_idle_cultist_archer_npc_up":     _sc(_preloaded_images["idle_cultist_archer_npc_up"],     (72, 72)),
	"elucidate_walk_cultist_archer_npc_up_001":     _sc(_preloaded_images["walk_cultist_archer_npc_up_001"],     (72, 72)),
	"elucidate_walk_cultist_archer_npc_up_002":     _sc(_preloaded_images["walk_cultist_archer_npc_up_002"],     (72, 72)),
	"elucidate_idle_cultist_channeler_npc_down":     _sc(_preloaded_images["idle_cultist_channeler_npc_down"],     (72, 72)),
	"elucidate_walk_cultist_chaneller_npc_down_001":     _sc(_preloaded_images["walk_cultist_chaneller_npc_down_001"],     (72, 72)),
	"elucidate_walk_cultist_chaneller_npc_down_002":     _sc(_preloaded_images["walk_cultist_chaneller_npc_down_002"],     (72, 72)),
	"elucidate_idle_cultist_channeler_npc_right":     _sc(_preloaded_images["idle_cultist_channeler_npc_right"],     (72, 72)),
	"elucidate_walk_cultist_chaneller_npc_right_001":     _sc(_preloaded_images["walk_cultist_chaneller_npc_right_001"],     (72, 72)),
	"elucidate_walk_cultist_chaneller_npc_right_002":     _sc(_preloaded_images["walk_cultist_chaneller_npc_right_002"],     (72, 72)),
	"elucidate_idle_cultist_channeler_npc_left":     _sc(_preloaded_images["idle_cultist_channeler_npc_left"],     (72, 72)),
	"elucidate_walk_cultist_chaneller_npc_left_001":     _sc(_preloaded_images["walk_cultist_chaneller_npc_left_001"],     (72, 72)),
	"elucidate_walk_cultist_chaneller_npc_left_002":     _sc(_preloaded_images["walk_cultist_chaneller_npc_left_002"],     (72, 72)),
	"elucidate_idle_cultist_channeler_npc_up":     _sc(_preloaded_images["idle_cultist_channeler_npc_up"],     (72, 72)),
	"elucidate_walk_cultist_chaneller_npc_up_001":     _sc(_preloaded_images["walk_cultist_chaneller_npc_up_001"],     (72, 72)),
	"elucidate_walk_cultist_chaneller_npc_up_002":     _sc(_preloaded_images["walk_cultist_chaneller_npc_up_001"],     (72, 72)),
	"elucidate_idle_assassin_npc_down":     _sc(_preloaded_images["idle_assassin_npc_down"],     (72, 72)),
	"elucidate_walk_church_assassin_npc_down_001":     _sc(_preloaded_images["walk_church_assassin_npc_down_001"],     (72, 72)),
	"elucidate_walk_church_assassin_npc_down_002":     _sc(_preloaded_images["walk_church_assassin_npc_down_002"],     (72, 72)),
	"elucidate_idle_assassin_npc_left":     _sc(_preloaded_images["idle_assassin_npc_left"],     (72, 72)),
	"elucidate_walk_church_assassin_npc_left_001":     _sc(_preloaded_images["walk_church_assassin_npc_left_001"],     (72, 72)),
	"elucidate_walk_church_assassin_npc_left_002":     _sc(_preloaded_images["walk_church_assassin_npc_left_002"],     (72, 72)),
	"elucidate_idle_assassin_npc_right":     _sc(_preloaded_images["idle_assassin_npc_right"],     (72, 72)),
	"elucidate_walk_church_assassin_npc_right_001":     _sc(_preloaded_images["walk_church_assassin_npc_right_002"],     (72, 72)),
	"elucidate_walk_church_assassin_npc_right_002":     _sc(_preloaded_images["walk_church_assassin_npc_right_002"],     (72, 72)),
	"elucidate_idle_assassin_npc_up":     _sc(_preloaded_images["idle_assassin_npc_up"],     (72, 72)),
	"elucidate_walk_church_assassin_npc_up_001":     _sc(_preloaded_images["walk_church_assassin_npc_up_001"],     (72, 72)),
	"elucidate_walk_church_assassin_npc_up_002":     _sc(_preloaded_images["walk_church_assassin_npc_up_002"],     (72, 72)),
	"walk_shaman_left_001":     _sc(_preloaded_images["walk_shaman_left_001"],     (72, 72)),
	"walk_shaman_left_002":     _sc(_preloaded_images["walk_shaman_left_002"],     (72, 72)),
	"idle_shaman_left":     _sc(_preloaded_images["idle_shaman_left"],     (72, 72)),
	"attack_shaman_left_001":     _sc(_preloaded_images["attack_shaman_left_001"],     (72, 72)),
	"attack_shaman_left_002":     _sc(_preloaded_images["attack_shaman_left_002"],     (72, 72)),
	"walk_shaman_down_001":     _sc(_preloaded_images["walk_shaman_down_001"],     (72, 72)),
	"walk_shaman_down_002":     _sc(_preloaded_images["walk_shaman_down_002"],     (72, 72)),
	"idle_shaman_down":     _sc(_preloaded_images["idle_shaman_down"],     (72, 72)),
	"attack_shaman_down_001":     _sc(_preloaded_images["attack_shaman_down_001"],     (72, 72)),
	"attack_shaman_down_002":     _sc(_preloaded_images["attack_shaman_down_002"],     (72, 72)),
	"walk_shaman_up_001":     _sc(_preloaded_images["walk_shaman_up_001"],     (72, 72)),
	"walk_shaman_up_002":     _sc(_preloaded_images["walk_shaman_up_002"],     (72, 72)),
	"idle_shaman_up":     _sc(_preloaded_images["idle_shaman_up"],     (72, 72)),
	"attack_shaman_up_001":     _sc(_preloaded_images["attack_shaman_up_001"],     (72, 72)),
	"attack_shaman_up_002":     _sc(_preloaded_images["attack_shaman_up_002"],     (72, 72)),
	"walk_shaman_right_001":     _sc(_preloaded_images["walk_shaman_right_001"],     (72, 72)),
	"walk_shaman_right_002":     _sc(_preloaded_images["walk_shaman_right_002"],     (72, 72)),
	"idle_shaman_right":     _sc(_preloaded_images["idle_shaman_right"],     (72, 72)),
	"attack_shaman_right_001":     _sc(_preloaded_images["attack_shaman_right_001"],     (72, 72)),
	"attack_shaman_right_002":     _sc(_preloaded_images["attack_shaman_right_002"],     (72, 72)),
	"walk_merchant_up_001":     _sc(_preloaded_images["walk_merchant_up_001"],     (72, 72)),
	"walk_merchant_up_002":     _sc(_preloaded_images["walk_merchant_up_002"],     (72, 72)),
	"idle_merchant_up":     _sc(_preloaded_images["idle_merchant_up"],     (72, 72)),
	"attack_merchant_up_001":     _sc(_preloaded_images["attack_merchant_up_001"],     (72, 72)),
	"attack_merchant_up_002":     _sc(_preloaded_images["attack_merchant_up_002"],     (72, 72)),
	"walk_merchant_right_001":     _sc(_preloaded_images["walk_merchant_right_001"],     (72, 72)),
	"walk_merchant_right_002":     _sc(_preloaded_images["walk_merchant_right_002"],     (72, 72)),
	"idle_merchant_right":     _sc(_preloaded_images["idle_merchant_right"],     (72, 72)),
	"attack_merchant_right_001":     _sc(_preloaded_images["attack_merchant_right_001"],     (72, 72)),
	"attack_merchant_right_002":     _sc(_preloaded_images["attack_merchant_right_002"],     (72, 72)),
	"walk_merchant_left_001":     _sc(_preloaded_images["walk_merchant_left_001"],     (72, 72)),
	"walk_merchant_left_002":     _sc(_preloaded_images["walk_merchant_left_002"],     (72, 72)),
	"idle_merchant_left":     _sc(_preloaded_images["idle_merchant_left"],     (72, 72)),
	"attack_merchant_left_001":     _sc(_preloaded_images["attack_merchant_left_001"],     (72, 72)),
	"attack_merchant_left_002":     _sc(_preloaded_images["attack_merchant_left_002"],     (72, 72)),
	"walk_merchant_down_001":     _sc(_preloaded_images["walk_merchant_down_001"],     (72, 72)),
	"walk_merchant_down_002":     _sc(_preloaded_images["walk_merchant_down_002"],     (72, 72)),
	"walk_merchant_down_002":     _sc(_preloaded_images["walk_merchant_down_002"],     (72, 72)),
	"attack_merchant_down_001":     _sc(_preloaded_images["attack_merchant_down_001"],     (72, 72)),
	"attack_merchant_down_002":     _sc(_preloaded_images["attack_merchant_down_002"],     (72, 72)),
	"walk_priest_left_001":     _sc(_preloaded_images["walk_priest_left_001"],     (72, 72)),
	"walk_priest_left_002":     _sc(_preloaded_images["walk_priest_left_002"],     (72, 72)),
	"idle_priest_left":     _sc(_preloaded_images["idle_priest_left"],     (72, 72)),
	"attack_priest_left_001":     _sc(_preloaded_images["attack_priest_left_001"],     (72, 72)),
	"attack_priest_left_002":     _sc(_preloaded_images["attack_priest_left_002"],     (72, 72)),
	"walk_priest_down_001":     _sc(_preloaded_images["walk_priest_down_001"],     (72, 72)),
	"walk_priest_down_002":     _sc(_preloaded_images["walk_priest_down_002"],     (72, 72)),
	"idle_priest_down":     _sc(_preloaded_images["idle_priest_down"],     (72, 72)),
	"attack_priest_down_001":     _sc(_preloaded_images["attack_priest_down_001"],     (72, 72)),
	"attack_priest_down_002":     _sc(_preloaded_images["attack_priest_down_002"],     (72, 72)),
	"walk_priest_up_001":     _sc(_preloaded_images["walk_priest_up_001"],     (72, 72)),
	"walk_priest_up_002":     _sc(_preloaded_images["walk_priest_up_002"],     (72, 72)),
	"idle_priest_up":     _sc(_preloaded_images["idle_priest_up"],     (72, 72)),
	"attack_priest_up_001":     _sc(_preloaded_images["attack_priest_up_001"],     (72, 72)),
	"attack_priest_up_002":     _sc(_preloaded_images["attack_priest_up_002"],     (72, 72)),
	"walk_priest_right_001":     _sc(_preloaded_images["walk_priest_right_001"],     (72, 72)),
	"walk_priest_right_002":     _sc(_preloaded_images["walk_priest_right_002"],     (72, 72)),
	"idle_priest_right":     _sc(_preloaded_images["idle_priest_right"],     (72, 72)),
	"attack_priest_right_001":     _sc(_preloaded_images["attack_priest_right_001"],     (72, 72)),
	"attack_priest_right_002":     _sc(_preloaded_images["attack_priest_right_002"],     (72, 72)),
	"walk_cultist_down_001":     _sc(_preloaded_images["walk_cultist_down_001"],     (72, 72)),
	"walk_cultist_down_002":     _sc(_preloaded_images["walk_cultist_down_002"],     (72, 72)),
	"idle_cultist_down":     _sc(_preloaded_images["idle_cultist_down"],     (72, 72)),
	"elucidate_attack_cultist_down_001":     _sc(_preloaded_images["attack_cultist_down_001"],     (72, 72)),
	"elucidate_attack_cultist_down_002":     _sc(_preloaded_images["attack_cultist_down_002"],     (72, 72)),
	"walk_cultist_up_001":     _sc(_preloaded_images["walk_cultist_up_001"],     (72, 72)),
	"walk_cultist_up_002":     _sc(_preloaded_images["walk_cultist_up_002"],     (72, 72)),
	"idle_cultist_up":     _sc(_preloaded_images["idle_cultist_up"],     (72, 72)),
	"elucidate_attack_cultist_up_001":     _sc(_preloaded_images["attack_cultist_up_001"],     (72, 72)),
	"elucidate_attack_cultist_up_002":     _sc(_preloaded_images["attack_cultist_up_002"],     (72, 72)),
	"walk_cultist_right_001":     _sc(_preloaded_images["walk_cultist_right_001"],     (72, 72)),
	"walk_cultist_right_002":     _sc(_preloaded_images["walk_cultist_right_002"],     (72, 72)),
	"idle_cultist_right":     _sc(_preloaded_images["idle_cultist_right"],     (72, 72)),
	"elucidate_attack_cultist_right_001":     _sc(_preloaded_images["attack_cultist_right_001"],     (72, 72)),
	"elucidate_attack_cultist_right_002":     _sc(_preloaded_images["attack_cultist_right_002"],     (72, 72)),
	"walk_cultist_left_001":     _sc(_preloaded_images["walk_cultist_left_001"],     (72, 72)),
	"walk_cultist_left_002":     _sc(_preloaded_images["walk_cultist_left_002"],     (72, 72)),
	"idle_cultist_left":     _sc(_preloaded_images["idle_cultist_left"],     (72, 72)),
	"elucidate_attack_cultist_left_001":     _sc(_preloaded_images["attack_cultist_left_001"],     (72, 72)),
	"elucidate_attack_cultist_left_002":     _sc(_preloaded_images["attack_cultist_left_002"],     (72, 72)),
}
	
_rotated_images = {
	"elucidate_title_1_r": pygame.transform.rotate(_scaled_images["elucidate_title_1"], 360),
	"elucidate_select_ui_002_play_select_r": pygame.transform.rotate(_scaled_images["elucidate_select_ui_002_play_select"], 90),
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
		screen.blit(_scaled_images["elucidate_select_exit"], ((screen_x // 2) - 100, (screen_y/2)-35))
		static_text_raw_center("PLAY", color=(0, 0, 0), position=(screen_x / 2, int((screen_y / 2)) - 20), size=30)
		for event in events:
			if event.type == pygame.MOUSEBUTTONDOWN:
				from main import *
	pygame.draw.rect(screen, (0, 255, 0), ((screen_x/2)-50, (screen_y/2)-35, 100, 30), 1)
	pygame.draw.rect(screen, (0, 255, 0), ((screen_x / 2) - 150, (screen_y / 2) + 5, 300, 30), 1)
	mouse()
	display()