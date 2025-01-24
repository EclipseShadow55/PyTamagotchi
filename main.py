import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame
import time
import json
import misc
from pet import Pet
from game import Game

misc.convertAll()

pygame.init()

with open("data.json", "r") as f:
    timings = json.load(f)["timings"]
    t_colors = json.load(f)["t_colors"]

def load_bmp(file_path):
    back_color = t_colors.get(file_path[file_path.findLast("/") + 1:], None)
    bmp = displayio.OnDiskBitmap(file_path)
    palette = displayio.Palette(256)
    for i in range(256):
        palette[i] = bmp.pixel_shader[i]
    if back_color is not None:
        palette.make_transparent(back_color)
    return bmp, palette

display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()
display.show(splash)


tile_width = 128
tile_height = 128

intro_sheet, intro_palette = load_bmp("BMPs/Intro.bmp")
happy_idle_sheet, happy_idle_palette = load_bmp("BMPs/HappyIdle.bmp")
open_back_sheet, open_back_palette = load_bmp("BMPs/OpenBack.bmp")
neutral_idle_sheet, neutral_idle_palette = load_bmp("BMPs/NeutralIdle.bmp")
sad_idle_sheet, sad_idle_palette = load_bmp("BMPs/SadIdle.bmp")


intro_animation = displayio.TileGrid(
    bitmap=intro_sheet,
    pixel_shader=intro_palette,
    width=1,
    height=1,
    tile_width=tile_width,
    tile_height=tile_height,
    default_tile=0,
    x=0,
    y=0
)

happy_idle_animation = displayio.TileGrid(
    happy_idle_sheet,
    pixel_shader=happy_idle_palette,
    width=1,
    height=1,
    tile_width=tile_width,
    tile_height=tile_height,
    default_tile=0,
    x=0,
    y=0
)

neutral_idle_animation = displayio.TileGrid(
	neutral_idle_sheet,
    pixel_shader=neutral_idle_palette,
    width=1,
    height=1,
    tile_width=tile_width,
    tile_height=tile_height,
    default_tile=0,
    x=0,
    y=0
)

sad_idle_animation = displayio.TileGrid(
	neutral_idle_sheet,
    pixel_shader=neutral_idle_palette,
    width=1,
    height=1,
    tile_width=tile_width,
    tile_height=tile_height,
    default_tile=0,
    x=0,
    y=0
)

open_background = displayio.TileGrid(open_back_sheet, pixel_shader=open_back_palette)

splash.append(intro_animation)
display.refresh()
for i in range(intro_sheet.width // tile_width):

    intro_animation[0] = i
    display.refresh()
    time.sleep(timings["intro"][i % len(timings["intro"])])

splash.remove(intro_animation)
splash.append(open_background)

settings = {"backyard": open_background, "inside": open_background, "fridge": open_background}
setting = 1
anims = {"eating": eating_sheet, "petting": petting_sheet, "game": game_sheet}
busy = False
total_time = 0
time = 0
game = None
idles = {"sad": [sad_idle_animation, sad_idle_sheet, "sad_idle"], "neutral": [neutral_idle_animation, neutral_idle_sheet, "neutral_idle"], "happy": [happy_idle_animation, happy_idle_sheet, "happy_idle"]}
pet = Pet(idles, splash, input("Enter a name for your pet (or enter for default name): "))

while True:
	up = False
	left = False
	right = False
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit(0)
		elif event.type == pygame.KEYDOWN:
			match event.key:
				case pygame.K_LEFT:
					left = True
				case pygame.K_RIGHT:
					right = True
				case pygame.K_UP:
					up = True
	
	if right and setting < 2:
		if not busy:
			setting += 1
			splash.remove(pet.get("anim")[0])
			splash.remove(setting[settings.keys()[setting - 1]])
			splash.append(setting[settings.keys()[setting]])
			splash.append(pet.get("anim")[0])
	elif left and setting > 0:
		if not busy:
			setting -= 1
			splash.remove(pet.get("anim")[0])
			splash.remove(setting[settings.keys()[setting + 1]])
			splash.append(setting[settings.keys()[setting]])
			splash.append(pet.get("anim")[0])
	match setting:
		case 0:
			if up:
				if not busy:
					busy = True
					game = Game(pet)
				else:
					game.jump()
			if busy:
				game.run()
		case 1:
			if not busy and up:
				busy = True
				start_petting(pet)
		case 2:
			if not busy and up:
				busy = True
				start_eating(pet)
	time_dif, time = pet.runFrame(time)
	total_time += time_dif
	time.sleep(time_dif)